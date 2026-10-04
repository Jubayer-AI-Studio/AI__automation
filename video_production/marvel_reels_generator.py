# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 JUBAYER.DEV MARVEL & HOLLYWOOD SCI-FI REELS ENGINE
=============================================================================
মার্ভেল / আয়রন ম্যান / জার্ভিস স্টাইলের ৩টি সিনেমাটিক এআই ও সফটওয়্যার
ইঞ্জিনিয়ারিং রিলস তৈরি করে সরাসরি জুবায়ের স্যারের টেলিগ্রামে পাঠিয়ে দেয়।
=============================================================================
"""

import os
import sys
import asyncio
import subprocess
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, OUTPUT_DIR, TEMP_DIR, BGM_PATH
import edge_tts

TECH_CLIPS_DIR = ROOT_DIR / "assets" / "tech_clips"
ASSETS_DIR = ROOT_DIR / "assets"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ৩টি দুর্দান্ত মার্ভেল/জার্ভিস স্টাইলের সিনেমাটিক স্ক্রিপ্ট
REELS_DATA = [
    {
        "id": "reel_marvel_1",
        "title": "The J.A.R.V.I.S Protocol: কোড থেকে সুপারইন্টেলিজেন্স",
        "caption": "🔥 টনি স্টার্কের জার্ভিস কি শুধু সাই-ফাই সিনেমায়? ওয়েলকাম টু মাই ল্যাব!\n\nসফটওয়্যার ইঞ্জিনিয়ারিং কেবল কোড লেখা নয়—ইটস আর্কিটেকটিং কনশাসনেস।\n\n#JubayerDev #SoftwareEngineering #IronManVibe #ArtificialIntelligence #MarvelTech #BanglaTech",
        "voice_script": "অনেকে ভাবে কোডিং মানে শুধু কতগুলো শুকনো লাইনের টাইপিং। বাট থিঙ্ক অ্যাগেইন! মার্ভেল সিনেমায় টনি স্টার্ক যেমন ল্যাবে একা দাঁড়িয়ে জার্ভিস তৈরি করেছিল—আজকের জেনারেটিভ এআই যুগে একজন সফটওয়্যার ডেভেলপারও ঠিক তাই! আমরা শুধু প্রোগ্রাম লিখি না, আমরা সিলিকন চিপের ভেতর একটা স্বয়ংক্রিয় বুদ্ধিমান মস্তিষ্ক তৈরি করি। কোড ইজ নো লঙ্গার জাস্ট টেক্সট—কোড ইজ সুপারপাওয়ার!",
        "clips": [
            "cyber_code_matrix.mp4",
            "hologram_gestures.mp4",
            "brain_3d_screen.mp4",
            "quantum_server_room.mp4"
        ],
        "hud_tag": "J.A.R.V.I.S PROTOCOL // AI LAB"
    },
    {
        "id": "reel_marvel_2",
        "title": "Code is My Superpower: ৩ এএম ডেভেলপার লাইফ",
        "caption": "⚡ রাত ৩টা বাজে। সারা পৃথিবী যখন ঘুমে, তখন স্ক্রিনে তৈরি হচ্ছে ভবিষ্যতের অটোমেশন।\n\nহলিউড সিনেমার মতো হাই-টেক সিস্টেম এখন আর কল্পনা নয়, বাস্তবতা!\n\n#DeveloperMindset #CyberPunk #AutomationLab #TechHero #JubayerDev #CodingLife",
        "voice_script": "রাত ৩টা বাজে। পুরো শহর এখন গভীর ঘুমে বিভোর। আর আমার স্ক্রিনে শত কোটি প্যারামিটারের নিউরাল নেটওয়ার্ক ট্রেইনিং চলছে। হলিউড সিনেমায় যে সাই-ফাই ডিভাইসগুলো দেখতে পেতেন, আজকের মডার্ন সফটওয়্যার আর্কিটেকচারে আমরা সেগুলোকে বাস্তবে রূপ দিচ্ছি। রোবোটিক অটোমেশন থেকে ক্লাউড ইন্টেলিজেন্স—ভবিষ্যতের পৃথিবীটা কোনো জাদুকর বানাবে না, বানাবে একজন কোডার!",
        "clips": [
            "hand_projecting_hologram.mp4",
            "cyber_laser_glasses.mp4",
            "red_circuit_board.mp4",
            "smartwatch_hologram.mp4"
        ],
        "hud_tag": "NEURAL CORE // 3 AM GRIND"
    },
    {
        "id": "reel_marvel_3",
        "title": "Humanoid Robotics & Superintelligence: নেক্সট ফ্রন্টিয়ার",
        "caption": "🤖 রোবট আর এআই যখন এক বিন্দুতে মিলিত হয়—শুরু হয় নতুন এক বিপ্লব!\n\nআমরা এখন ভবিষ্যতের দ্বারপ্রান্তে দাঁড়িয়ে। আর এই বিপ্লবের চালিকাশক্তি সফটওয়্যার।\n\n#Robotics #Superintelligence #SciFiReality #HollywoodTech #JubayerDev #FutureTech",
        "voice_script": "মানুষের তৈরি ইতিহাসের সবচেয়ে শক্তিশালী হাতিয়ার কী জানেন? রোবোটিক্স আর কৃত্রিম বুদ্ধিমত্তা। যখন একটা হিউম্যানয়েড রোবটের নিউরাল মেমোরিতে রিয়েল-টাইম ডিসিশন মেকিং কোড পুশ করা হয়, তখন কল্পবিজ্ঞান আর বাস্তবতার ভেদাভেদ মুছে যায়। সফটওয়্যার ইঞ্জিনিয়ারিং এখন শুধু ল্যাপটপে সীমাবদ্ধ নয়—এটি ধাতব রোবটকে জীবন্ত করে তোলার বিজ্ঞান!",
        "clips": [
            "humanoid_robot.mp4",
            "robot_walking.mp4",
            "cyborg_hologram.mp4",
            "sci_fi_hand_device.mp4"
        ],
        "hud_tag": "HUMANOID CORE // NEXT FRONTIER"
    }
]


async def generate_speech(text: str, output_mp3: Path):
    """উচ্চ এনার্জি ও আত্মবিশ্বাসী কণ্ঠে বাংলা ভয়েসওভার তৈরি করে।"""
    communicate = edge_tts.Communicate(
        text=text,
        voice="bn-IN-BashkarNeural",
        rate="+12%",
        pitch="+2Hz"
    )
    await communicate.save(str(output_mp3))


def get_audio_duration(audio_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 25.0


def create_hud_overlay_image(output_png: Path, tag_text: str):
    """১০৮০x১৯২০ রেজোলিউশনে হলিউড মার্ভেল স্টাইলের সাইবার HUD ফ্রেম ও ওয়াটারমার্ক তৈরি করে।"""
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ফন্ট লোড
    try:
        font_logo = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 36)
        font_tag = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22)
    except Exception:
        font_logo = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # ১. টপ হেডার বার: সাইবার গ্লোয়িং ওয়াটারমার্ক
    draw.rectangle([(40, 60), (450, 125)], fill=(10, 15, 25, 210), outline=(0, 230, 255, 240), width=2)
    draw.text((60, 75), "</> JUBAYER.DEV", fill=(0, 240, 255, 255), font=font_logo)

    # ২. ডানদিকের স্ট্যাটাস ইন্ডিকেটর
    draw.rectangle([(W - 320, 60), (W - 40, 125)], fill=(10, 15, 25, 210), outline=(255, 60, 80, 230), width=2)
    draw.text((W - 300, 80), "LIVE NEURAL LINK", fill=(255, 80, 100, 255), font=font_sub)

    # ৩. সেন্ট্রাল HUD ট্যাগ (লোয়ার-থার্ড গ্লো বক্স)
    box_w, box_h = 760, 75
    box_x = (W - box_w) // 2
    box_y = 1580
    draw.rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], fill=(12, 18, 32, 230), outline=(0, 255, 200, 240), width=2)
    draw.rectangle([(box_x + 4, box_y + 4), (box_x + box_w - 4, box_y + box_h - 4)], outline=(0, 160, 255, 120), width=1)
    draw.text((box_x + 40, box_y + 22), f"⚡ {tag_text}", fill=(255, 255, 255, 255), font=font_tag)

    img.save(output_png, "PNG")


def render_marvel_reel(reel_dict: dict) -> Path:
    reel_id = reel_dict["id"]
    print(f"\n[MarvelEngine] 🎬 রেন্ডারিং শুরু: {reel_dict['title']}...")

    # ১. ভয়েস তৈরি
    mp3_path = TEMP_DIR / f"{reel_id}_voice.mp3"
    asyncio.run(generate_speech(reel_dict["voice_script"], mp3_path))
    duration = get_audio_duration(mp3_path)
    print(f"  ▶ অডিও দৈর্ঘ্য: {duration:.2f} সেকেন্ড")

    # ২. অডিও মাস্টারিং (ভয়েস + BGM ডাক)
    mastered_audio = TEMP_DIR / f"{reel_id}_mixed_audio.mp3"
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(mp3_path),
        "-stream_loop", "-1", "-i", str(BGM_PATH),
        "-filter_complex",
        f"[0:a]volume=1.2,firequalizer=gain_entry='entry(100,6);entry(250,4);entry(3000,3)'[voice];"
        f"[1:a]volume=0.18,atrim=0:{duration + 1.5},afade=t=out:st={duration - 0.5}:d=1.5[bgm];"
        f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(mastered_audio)
    ]
    subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ৩. HUD ওভারলে তৈরি
    hud_overlay = TEMP_DIR / f"{reel_id}_hud.png"
    create_hud_overlay_image(hud_overlay, reel_dict["hud_tag"])

    # ৪. ভিডিও ক্লিপ সিলেকশন ও প্রিপারেশন (৪টি ক্লিপ মিলে ৯:১৬ ১০৮০x১৯২০)
    clips = reel_dict["clips"]
    clip_dur = duration / len(clips)

    filter_complex_parts = []
    inputs = []

    for idx, cname in enumerate(clips):
        cpath = TECH_CLIPS_DIR / cname
        inputs.extend(["-i", str(cpath)])
        filter_complex_parts.append(
            f"[{idx}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
            f"trim=0:{clip_dur:.2f},setpts=PTS-STARTPTS[v{idx}];"
        )

    concat_inputs = "".join([f"[v{i}]" for i in range(len(clips))])
    filter_complex_parts.append(f"{concat_inputs}concat=n={len(clips)}:v=1:a=0[vbase];")

    # HUD ওভারলে অ্যাড করা
    hud_input_idx = len(clips)
    inputs.extend(["-i", str(hud_overlay)])
    filter_complex_parts.append(f"[vbase][{hud_input_idx}:v]overlay=0:0[vfinal]")

    # ৫. ফুল রিলস কম্বাইন
    final_output = OUTPUT_DIR / f"{reel_id}.mp4"
    cmd_video = [
        "ffmpeg", "-y",
        *inputs,
        "-i", str(mastered_audio),
        "-filter_complex", "".join(filter_complex_parts),
        "-map", "[vfinal]",
        "-map", f"{len(clips) + 1}:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.2f}",
        str(final_output)
    ]
    subprocess.run(cmd_video, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"  ✅ রিলস রেন্ডার সম্পন্ন: {final_output} ({os.path.getsize(final_output) / (1024*1024):.1f} MB)")
    return final_output


def send_reel_to_telegram(video_path: Path, title: str, caption: str):
    """টেলিগ্রাম বটে সরাসরি ভিডিও ও টেক্সট পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    print(f"[Telegram] 🚀 ভিডিও আপলোড হচ্ছে: {title}...")

    with open(video_path, "rb") as vf:
        files = {"video": (video_path.name, vf, "video/mp4")}
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": f"🎬 <b>{title}</b>\n\n{caption}",
            "parse_mode": "HTML",
            "supports_streaming": True
        }
        res = requests.post(url, data=data, files=files, timeout=60)
        if res.status_code == 200:
            print(f"  ✅ টেলিগ্রামে সফলভাবে পৌঁছেছে: {title}!")
            return True
        else:
            print(f"  ❌ টেলিগ্রাম এরর: {res.status_code} - {res.text[:100]}")
            return False


def run_all_marvel_reels():
    print("==================================================")
    print("⚡ JUBAYER.DEV MARVEL HOLLYWOOD REELS ENGINE LAUNCH")
    print("==================================================")

    rendered_reels = []
    for r in REELS_DATA:
        vpath = render_marvel_reel(r)
        rendered_reels.append((vpath, r["title"], r["caption"]))
        send_reel_to_telegram(vpath, r["title"], r["caption"])

    print("\n🎉 সমস্ত ৩টি মার্ভেল রিলস সফলভাবে তৈরি ও টেলিগ্রামে পাঠানো হয়েছে!")
    return rendered_reels


if __name__ == "__main__":
    run_all_marvel_reels()
