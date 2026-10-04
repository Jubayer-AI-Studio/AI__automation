# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 JUBAYER.DEV REAL DEVELOPER CINEMATIC REEL GENERATOR
=============================================================================
জুবায়ের স্যারের আপলোড করা আসল ২টি ছবি ব্যবহার করে সম্পূর্ণ হলিউড মার্ভেল
স্টাইলের ৩৫ সেকেন্ডের হাই-কোয়ালিটি ফেসবুক রিলস তৈরি করে।
কোনো এআই ফেস ডিস্টরশন নেই—আসল চেহারা ১০০% অবিকৃত থাকবে।
=============================================================================
"""

import os
import sys
import asyncio
import subprocess
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

ASSETS_DIR = ROOT_DIR / "assets"
FONT_BN = "C\\:/Users/ASSDI/Desktop/facebook/assets/fonts/HindSiliguri-Bold.ttf"
FONT_EN = "C\\:/Windows/Fonts/consola.ttf"
IMG_THINKING = ASSETS_DIR / "jubayer_real_thinking.jpg"
IMG_CODING = ASSETS_DIR / "jubayer_real_coding.jpg"

VOICE_SCRIPT = (
    "অনেকে কম্পিউটার স্ক্রিনে কেবল কিছু কোড আর ব্র্যাকেট দেখতে পায়। "
    "কিন্তু একজন সফটওয়্যার ইঞ্জিনিয়ার দেখে একটি সম্পূর্ণ নতুন জগত। "
    "মার্ভেল সিনেমায় টনি স্টার্ক যেমন ল্যাবে ঘণ্টার পর ঘণ্টা জেগে নতুন ইনভেনশন তৈরি করত—"
    "বাস্তব জীবনে একজন ডেভেলপারের কিবোর্ডই তার সবচেয়ে বড় পাওয়ার! "
    "রাত যখন গভীর হয়, পৃথিবী যখন ঘুমিয়ে পড়ে, তখন শুরু হয় আমাদের আসল কাজ। "
    "শত শত লাইনের লজিক, এআই অ্যালগরিদম আর আধুনিক অটোমেশন। "
    "আমরা শুধু কোড লিখি না—উই আর্কিটেক্ট দ্য ফিউচার। "
    "দিস ইজ জুবায়ের ডট ডেভ।"
)

# ৩৫ সেকেন্ডের জন্য দৃশ্য ও সাবটাইটেল শিডিউল (কোনো অ্যাপোস্ট্রফি ছাড়া)
SUBTITLE_CUES = [
    (0.0, 4.2, "অনেকে স্ক্রিনে কেবল কিছু কোড আর ব্র্যাকেট দেখতে পায়...", "Just dry syntax and brackets?"),
    (4.2, 8.5, "কিন্তু একজন ডেভেলপার দেখে একটি সম্পূর্ণ নতুন জগত!", "A Software Architect Sees A Whole New World."),
    (8.5, 12.8, "মার্ভেল সিনেমায় টনি স্টার্ক যেমন ল্যাবে ইনভেনশন বানাত—", "Like Tony Stark in his high-tech lab..."),
    (12.8, 17.5, "বাস্তব জীবনে ডেভেলপারের কিবোর্ডই তার সুপারপাওয়ার!", "Code is our real-life Superpower!"),
    (17.5, 21.8, "রাত যখন গভীর হয়, পৃথিবী যখন ঘুমিয়ে পড়ে...", "When the world sleeps at 3 AM..."),
    (21.8, 26.5, "তখন স্ক্রিনে জন্ম নেয় শত কোটি প্যারামিটারের এআই সিস্টেম।", "Neural networks come alive on our screens."),
    (26.5, 31.0, "আমরা শুধু কোড লিখি না—We Architect The Future!", "We do not just write code, We Build The Future!"),
    (31.0, 35.5, "This is Jubayer.dev | AI & Systems Architect", "Engineering Tomorrow, Today.")
]


def prepare_scene_image(img_path: Path, output_path: Path, is_square: bool = False):
    """
    ১০৮০x১৯২০ সাইজে ছবির আসল চেহারা অক্ষুণ্ণ রেখে একটি প্রিমিয়াম সিনেমাটিক ব্যাকড্রপ ফ্রেম বানায়।
    """
    W, H = 1080, 1920
    orig = Image.open(img_path).convert("RGB")

    # ১. ব্যাকগ্রাউন্ড: স্কেল ও ব্লার (সিনেমাটিক স্টুডিও ভাইব)
    scale_bg = max(W / orig.width, H / orig.height)
    bg_w, bg_h = int(orig.width * scale_bg), int(orig.height * scale_bg)
    bg = orig.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    l = (bg_w - W) // 2
    t = (bg_h - H) // 2
    bg = bg.crop((l, t, l + W, t + H))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=35))
    dark = Image.new("RGB", (W, H), (8, 12, 20))
    bg = Image.blend(bg, dark, alpha=0.55)

    # ২. ফোরগ্রাউন্ড: জুবায়ের ভাইয়ের আসল স্পষ্ট ছবি
    if is_square:
        fg_w = 1040
        fg_h = 1040
        fg_y = 300
    else:
        fg_w = 1040
        fg_h = int(orig.height * (fg_w / orig.width))
        fg_y = 360

    fg = orig.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
    fg_x = (W - fg_w) // 2

    # সাইবার নিয়ন বর্ডার ও শ্যাডো
    draw_bg = ImageDraw.Draw(bg)
    draw_bg.rectangle([(fg_x - 3, fg_y - 3), (fg_x + fg_w + 3, fg_y + fg_h + 3)], outline=(0, 220, 255), width=3)
    bg.paste(fg, (fg_x, fg_y))

    # ৩. টপ হেডার HUD
    draw = ImageDraw.Draw(bg)
    try:
        font_mono = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 36)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22)
    except Exception:
        font_mono = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # বামের লোগো
    draw.rectangle([(40, 65), (480, 135)], fill=(10, 16, 26), outline=(0, 240, 255), width=2)
    draw.text((60, 82), "</> JUBAYER.DEV", fill=(0, 255, 240), font=font_mono)

    # ডানের লাইভ ইন্ডিকেটর
    draw.rectangle([(W - 380, 65), (W - 40, 135)], fill=(10, 16, 26), outline=(255, 60, 80), width=2)
    draw.ellipse([(W - 355, 90), (W - 335, 110)], fill=(255, 50, 70))
    draw.text((W - 320, 87), "AI LAB // 4K LIVE", fill=(255, 255, 255), font=font_sub)

    # লোয়ার সাবটাইটেল ফ্রেম (কাঁচের মতো ডার্ক গ্লাস)
    sub_w, sub_h = 980, 175
    sub_x = (W - sub_w) // 2
    sub_y = 1430
    draw.rectangle([(sub_x, sub_y), (sub_x + sub_w, sub_y + sub_h)], fill=(10, 14, 22), outline=(0, 255, 200), width=2)
    draw.rectangle([(sub_x + 3, sub_y + 3), (sub_x + sub_w - 3, sub_y + sub_h - 3)], outline=(0, 160, 255), width=1)

    # ফুটার টেক্সট
    draw.text(((W - 680) // 2, 1750), "ENGINEERED BY JUBAYER.DEV | SOFTWARE ARCHITECT", fill=(150, 175, 200), font=font_sub)

    bg.save(output_path, "JPEG", quality=95)
    print(f"  Frame created: {output_path.name}")


async def create_voiceover(output_mp3: Path):
    """ভয়েসওভার সিন্থেসিস।"""
    comm = edge_tts.Communicate(
        text=VOICE_SCRIPT,
        voice="bn-IN-BashkarNeural",
        rate="+8%",
        pitch="+2Hz"
    )
    await comm.save(str(output_mp3))


def generate_full_reel() -> Path:
    print("==================================================")
    print("🚀 জুবায়ের স্যারের আসল ছবি দিয়ে টেস্ট রিলস তৈরি শুরু...")
    print("==================================================")

    # ১. দৃশ্য তৈরি (Scene 1: Thinking, Scene 2: Coding)
    frame_thinking = TEMP_DIR / "frame_real_thinking.jpg"
    frame_coding = TEMP_DIR / "frame_real_coding.jpg"
    prepare_scene_image(IMG_THINKING, frame_thinking, is_square=False)
    prepare_scene_image(IMG_CODING, frame_coding, is_square=True)

    # ২. ভয়েস তৈরি
    raw_voice = TEMP_DIR / "real_reel_raw_voice.mp3"
    print("\n[১/৪] স্টুডিও ভয়েসওভার তৈরি হচ্ছে...")
    asyncio.run(create_voiceover(raw_voice))

    # অডিও দৈর্ঘ্য যাচাই
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        str(raw_voice)
    ]
    dur_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True)
    total_duration = float(dur_res.stdout.strip())
    print(f"  ▶ মোট ভয়েস দৈর্ঘ্য: {total_duration:.2f} সেকেন্ড")

    # ৩. অডিও মাস্টারিং (ভয়েস + ব্যাকগ্রাউন্ড মিউজিক ডাক)
    print("\n[২/৪] ভয়েস ও হলিউড সিনেমাটিক BGM মাস্টারিং...")
    mixed_audio = TEMP_DIR / "real_reel_mixed_audio.mp3"
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(raw_voice),
        "-stream_loop", "-1", "-i", str(BGM_PATH),
        "-filter_complex",
        f"[0:a]volume=1.2,firequalizer=gain_entry='entry(100,5);entry(200,4);entry(3500,2.5)'[vclean];"
        f"[1:a]volume=0.17,atrim=0:{total_duration + 1.0},afade=t=out:st={total_duration - 0.5}:d=1.5[bgm];"
        f"[vclean][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(mixed_audio)
    ]
    subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # ৪. ভিডিও সিন ট্রানজিশন ও সাবটাইটেল ইন্টিগ্রেশন
    print("\n[৩/৪] ৪টি সিনেমাটিক সিন ও নিখুঁত বাংলা সাবটাইটেল রেন্ডার হচ্ছে...")

    s1_dur = 8.5
    s2_dur = 9.0
    s3_dur = 9.0
    s4_dur = total_duration - (s1_dur + s2_dur + s3_dur)

    # সাবটাইটেল ড্র-টেক্সট ফিল্টার চেইন (proper commas without escape)
    drawtext_filters = []
    for (st, et, bn_text, en_text) in SUBTITLE_CUES:
        if st >= total_duration:
            continue
        actual_et = min(et, total_duration)
        clean_bn = bn_text.replace("'", "")
        clean_en = en_text.replace("'", "")

        # বাংলা সাবটাইটেল
        drawtext_filters.append(
            f"drawtext=fontfile='{FONT_BN}':text='{clean_bn}':"
            f"fontsize=42:fontcolor=white:"
            f"x=(w-text_w)/2:y=1460:"
            f"enable='between(t,{st:.2f},{actual_et:.2f})'"
        )
        # ইংলিশ সাবটাইটেল
        drawtext_filters.append(
            f"drawtext=fontfile='{FONT_EN}':text='{clean_en}':"
            f"fontsize=24:fontcolor=0x00F0FF:"
            f"x=(w-text_w)/2:y=1530:"
            f"enable='between(t,{st:.2f},{actual_et:.2f})'"
        )

    full_drawtext = ",".join(drawtext_filters)

    # ভিডিও কম্পোজিশন এফএফএমপ্যাগ কমান্ড
    final_output = OUTPUT_DIR / "jubayer_developer_hero_reel.mp4"
    filter_complex = (
        f"[0:v]zoompan=z='min(zoom+0.0010,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(s1_dur*30)}:s=1080x1920:fps=30[v0];"
        f"[1:v]zoompan=z='min(zoom+0.0012,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(s2_dur*30)}:s=1080x1920:fps=30[v1];"
        f"[2:v]zoompan=z='min(zoom+0.0010,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(s3_dur*30)}:s=1080x1920:fps=30[v2];"
        f"[3:v]zoompan=z='min(zoom+0.0008,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(s4_dur*30)}:s=1080x1920:fps=30[v3];"
        f"[v0][v1][v2][v3]concat=n=4:v=1:a=0[vcat];"
        f"[vcat]{full_drawtext}[vfinal]"
    )

    cmd_video = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{s1_dur:.2f}", "-i", str(frame_thinking),
        "-loop", "1", "-t", f"{s2_dur:.2f}", "-i", str(frame_coding),
        "-loop", "1", "-t", f"{s3_dur:.2f}", "-i", str(frame_thinking),
        "-loop", "1", "-t", f"{s4_dur:.2f}", "-i", str(frame_coding),
        "-i", str(mixed_audio),
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "4:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{total_duration:.2f}",
        str(final_output)
    ]

    subprocess.run(cmd_video, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n[৪/৪] ✅ মাস্টার রিলস সফলভাবে তৈরি হয়েছে: {final_output.name} ({final_output.stat().st_size / (1024*1024):.1f} MB)")
    return final_output


def dispatch_to_telegram(video_path: Path):
    """টেলিগ্রাম বটে সরাসরি ভিডিও পাঠানো।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] Token or Chat ID not found!")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    caption = (
        "🎬 <b>[YOUR REAL HERO REEL // JUBAYER.DEV]</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ <b>The Developer Behind The Code // Jubayer.dev</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "আপনার দেওয়া আসল ২টি ছবি ও চেহারা ১০০% অবিকৃত রেখে হলিউড সিনেমাটিক স্টাইলে এই টেস্ট রিলসটি তৈরি করা হয়েছে।\n\n"
        "⏱ <b>দৈর্ঘ্য:</b> ৩৫ সেকেন্ড\n"
        "🖥 <b>রেজোলিউশন:</b> ১০৮০x১৯২০ ফুল এইচডি (Facebook Reels Ready)\n"
        "🎙 <b>ভয়েস:</b> স্টুডিও কোয়ালিটি ও অরিজিনাল বাংলা সাবটাইটেল\n\n"
        "#JubayerDev #DeveloperLife #SoftwareEngineer #AIArchitecture #CodeIsSuperpower"
    )

    print(f"\n[Telegram] 📲 টেলিগ্রামে ভিডিও আপলোড হচ্ছে ({video_path.stat().st_size / (1024*1024):.1f} MB)...")
    with open(video_path, "rb") as vf:
        files = {"video": (video_path.name, vf, "video/mp4")}
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption,
            "parse_mode": "HTML",
            "supports_streaming": True
        }
        res = requests.post(url, data=data, files=files, timeout=90)
        if res.status_code == 200:
            print("🎉 টেলিগ্রামে সফলভাবে পৌঁছে গেছে! আপনার ফোন চেক করুন।")
            return True
        else:
            print(f"❌ টেলিগ্রাম এরর: {res.status_code} - {res.text}")
            return False


if __name__ == "__main__":
    vid = generate_full_reel()
    dispatch_to_telegram(vid)
