import sys
import os
import time
import subprocess
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TEMP_DIR, OUTPUT_DIR
from content_writing.script_writer import get_reel_content, get_daily_extras
from video_production.video_maker import render_final_reel
from thumbnail_card.thumbnail_maker import create_ai_photocard
from src.telegram_engine import send_full_creator_kit

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def send_telegram_msg(text: str):
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"},
            timeout=20
        )
    except Exception as e:
        print(f"[Telegram] Error sending message: {e}")

def download_telegram_file(file_id: str, destination: Path) -> bool:
    try:
        res = requests.get(f"{BASE_URL}/getFile", params={"file_id": file_id}, timeout=20).json()
        if not res.get("ok"):
            print(f"[Telegram] getFile failed: {res}")
            return False
        file_path = res["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        file_data = requests.get(download_url, timeout=60).content
        with open(destination, "wb") as f:
            f.write(file_data)
        return True
    except Exception as e:
        print(f"[Telegram] Failed to download file: {e}")
        return False

def listen_and_build_reel():
    print("=" * 65)
    print("🎙️ টেলিগ্রাম ভয়েস রিসিভার ও পার্সোনাল রিলস বিল্ডার চালু হচ্ছে...")
    print("=" * 65)

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ত্রুটি: .env ফাইলে TELEGRAM_BOT_TOKEN বা TELEGRAM_CHAT_ID পাওয়া যায়নি!")
        return

    # 1. আজকের স্ক্রিপ্ট বাছাই
    reel_content = get_reel_content()
    title = reel_content["title"]
    scenes = reel_content["scenes"]
    caption = reel_content["caption"]
    hashtags = reel_content["hashtags"]
    extras = get_daily_extras()

    full_script_text = "\n\n".join([f"🔹 {s['text']}" for s in scenes])

    prompt_msg = (
        f"🎙️ *আপনার আজকের রিলসের স্ক্রিপ্ট প্রস্তুত!*\n\n"
        f"📌 *টপিক:* {title}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📄 *স্ক্রিপ্ট (দেখে দেখে স্বাভাবিক কণ্ঠে বলুন):*\n\n"
        f"{full_script_text}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 *এখন কী করবেন:*\n"
        f"নিচের মাইক আইকন (🎙️) চেপে ধরে সাধারণ ভয়েস মেসেজ হিসেবে ওপরের কথাগুলো রেকর্ড করে আমাকে পাঠিয়ে দিন।\n\n"
        f"*(আপনি ভয়েস পাঠালেই আপনার আসল কণ্ঠে ফুল রিলস ভিডিও তৈরি শুরু হবে)*"
    )

    print(f"\n[১/৩] টেলিগ্রামে স্ক্রিপ্ট পাঠানো হচ্ছে... ({title})")
    send_telegram_msg(prompt_msg)
    print("✅ স্ক্রিপ্ট সফলভাবে আপনার টেলিগ্রামে পাঠানো হয়েছে!")
    print("⏳ আপনার পাঠানো ভয়েস মেসেজের জন্য অপেক্ষা করা হচ্ছে...")

    # 2. লেটেস্ট অফসেট বের করা
    offset = 0
    try:
        up_res = requests.get(f"{BASE_URL}/getUpdates", timeout=10).json()
        if up_res.get("ok") and up_res.get("result"):
            offset = up_res["result"][-1]["update_id"] + 1
    except Exception:
        pass

    # 3. ভয়েস মেসেজের জন্য অপেক্ষা করা
    voice_file_id = None
    while True:
        try:
            updates = requests.get(
                f"{BASE_URL}/getUpdates",
                params={"offset": offset, "timeout": 20},
                timeout=25
            ).json()

            if updates.get("ok"):
                for upd in updates.get("result", []):
                    offset = upd["update_id"] + 1
                    msg = upd.get("message", {})
                    sender_id = str(msg.get("from", {}).get("id", ""))

                    if sender_id == str(TELEGRAM_CHAT_ID):
                        if "voice" in msg:
                            voice_file_id = msg["voice"]["file_id"]
                            print("\n[২/৩] 🎙️ আপনার ভয়েস মেসেজ সফলভাবে রিসিভ করা হয়েছে!")
                            break
                        elif "audio" in msg:
                            voice_file_id = msg["audio"]["file_id"]
                            print("\n[২/৩] 🎵 আপনার অডিও ফাইল সফলভাবে রিসিভ করা হয়েছে!")
                            break

            if voice_file_id:
                break

        except Exception as e:
            time.sleep(2)

        time.sleep(1)

    # 4. ইউজারকে তাৎক্ষণিক কনফার্মেশন পাঠানো
    send_telegram_msg(
        "⏳ *আপনার ভয়েস পেয়েছি!*\n\nআপনার আসল কণ্ঠের সাথে ব্যাকগ্রাউন্ড ভিডিও ও আপনার ছবি সিঙ্ক করে ফুল রিলস ভিডিও তৈরি হচ্ছে... একটু অপেক্ষা করুন!"
    )

    # 5. অডিও ডাউনলোড ও কনভার্ট
    raw_voice_path = TEMP_DIR / "user_incoming_voice.oga"
    clean_voice_path = TEMP_DIR / "user_clean_voice.mp3"

    print("[৩/৩] ভয়েস ফাইল ডাউনলোড ও প্রসেসিং হচ্ছে...")
    download_telegram_file(voice_file_id, raw_voice_path)

    cmd_conv = [
        "ffmpeg", "-y",
        "-i", str(raw_voice_path),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(clean_voice_path)
    ]
    subprocess.run(cmd_conv, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_duration = get_audio_duration(clean_voice_path)
    print(f"🎙️ মোট অডিও দৈর্ঘ্য: {total_duration:.2f} সেকেন্ড")

    # 6. সিন অনুযায়ী সাবটাইটেল টাইমিং বণ্টন
    char_counts = [len(s["text"]) for s in scenes]
    total_chars = sum(char_counts)

    scene_timings = []
    curr_time = 0.0
    for i, scene in enumerate(scenes, 1):
        scene_dur = (len(scene["text"]) / total_chars) * total_duration
        st = curr_time
        et = curr_time + scene_dur
        scene_timings.append({
            "index": i,
            "text": scene["text"],
            "start": st,
            "end": et,
            "duration": scene_dur
        })
        curr_time = et

    # 7. ফাইনাল রিলস ভিডিও রেন্ডারিং (ইউজারের আসল কণ্ঠে)
    print("🎬 রিলস ভিডিও রেন্ডারিং হচ্ছে (আপনার নিজের আসল কণ্ঠে)...")
    output_video_path = render_final_reel(
        scene_timings=scene_timings,
        narration_path=clean_voice_path,
        total_duration=total_duration,
        title=title
    )

    # 8. ফটো পোস্ট তৈরি
    card_info = extras["photo_card"]
    photo_card_path = create_ai_photocard(
        title=card_info["title"],
        points=card_info["points"],
        category=card_info["category"]
    )

    # 9. টেলিগ্রামে সম্পন্ন কিট পাঠানো
    print("📲 আপনার টেলিগ্রামে তৈরি করা ভিডিও ও পোস্ট পাঠানো হচ্ছে...")
    send_full_creator_kit(
        video_path=output_video_path,
        title=title,
        caption=caption,
        hashtags=hashtags,
        photo_card_path=photo_card_path,
        extras=extras
    )

    print("=" * 65)
    print("🎉 অভিনন্দন! আপনার নিজের আসল কণ্ঠের রিলস ভিডিও ডেলিভারি সম্পন্ন!")
    print("📲 আপনার ফোনের Telegram চেক করে ভিডিওটি দেখুন।")
    print("=" * 65)

if __name__ == "__main__":
    listen_and_build_reel()

