# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 HOLLYWOOD ROBOTICS & HARDWARE LAB CINEMATIC REEL GENERATOR
=============================================================================
Target: Jubayer.dev (AI & Autonomous Systems Developer)
Theme: Hollywood Iron-Man Robotics Lab, Cybernetic Bionics, Microchip Soldering,
       Robotic CNC Laser Welding, Industrial Robotic Automation.
=============================================================================
"""

import sys
import os
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import math
import asyncio
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts

ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / "assets"
TECH_CLIPS_DIR = ASSETS_DIR / "tech_clips" / "hollywood"
TEMP_DIR = ROOT_DIR / "temp"
OUTPUT_DIR = ROOT_DIR / "output"
MUSIC_DIR = ASSETS_DIR / "music"
FONTS_DIR = ASSETS_DIR / "fonts"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BGM_PATH = MUSIC_DIR / "mystery_bgm.mp3"
FONT_BN_PATH = FONTS_DIR / "HindSiliguri-Bold.ttf"
JUBAYER_CODING_PHOTO = ASSETS_DIR / "jubayer_real_coding.jpg"

TELEGRAM_BOT_TOKEN = "8638569113:AAHwY2Rd9Ueyx9kWKAGv6VYDELKnfRdQtEc"
TELEGRAM_CHAT_ID = "8273323826"

SCENES_CONFIG = [
    {
        "id": 1,
        "clip_file": "cybernetic_tech.mp4",
        "clip_start": 0.0,
        "text": "অনেকে ভাবে সফটওয়্যার মানে শুধুই স্ক্রিনের কিছু কোড। কিন্তু কোড যখন মেটালের সাথে কানেক্ট হয়, তখনই শুরু হয় আসল রোবোটিক্স।",
        "sub_bn": "কোড যখন মেটালের সাথে কানেক্ট হয়, তখনই আসল রোবোটিক্স!",
        "sub_en": "When Code Connects to Metal, True Robotics Begins."
    },
    {
        "id": 2,
        "clip_file": "soldering.mp4",
        "clip_start": 2.0,
        "text": "মাইক্রোচিপ, সেন্সর আর নিখুঁত সার্কিট ডিজাইনে আমরা তৈরি করি মেশিনের স্নায়ুতন্ত্র।",
        "sub_bn": "মাইক্রোচিপ ও সার্কিট ডিজাইনে মেশিনের স্নায়ুতন্ত্র!",
        "sub_en": "Precision Microchips: Engineering The Neural Core."
    },
    {
        "id": 3,
        "clip_file": "cnc_laser_welding.mp4",
        "clip_start": 0.5,
        "text": "আয়রন ম্যান স্টাইল স্বয়ংক্রিয় রোবোটিক মেকানিক্স আর লেজার প্রিসিশন—যেখানে মিলিমিটারের নির্ভুলতায় জন্ম নেয় ফিউচার হার্ডওয়্যার।",
        "sub_bn": "আয়রন ম্যান স্টাইল রোবোটিক মেকানিক্স ও লেজার প্রিসিশন!",
        "sub_en": "Iron Man Style Robotic Mechanics & Laser Precision."
    },
    {
        "id": 4,
        "clip_file": "robotic_assembly.mp4",
        "clip_start": 2.0,
        "text": "সফটওয়্যার আর হার্ডওয়্যারের এই পাওয়ারফুল ফিউশনই তৈরি করছে স্বয়ংক্রিয় ভবিষ্যত।",
        "sub_bn": "সফটওয়্যার ও হার্ডওয়্যার ফিউশন—স্বয়ংক্রিয় ভবিষ্যত!",
        "sub_en": "Software & Hardware Fusion: The Autonomous Future."
    },
    {
        "id": 5,
        "clip_file": "outro_slate",
        "clip_start": 0.0,
        "text": "আই এম জুবায়ের—ওয়েলকাম টু মাই এআই অ্যান্ড রোবোটিক্স ল্যাব!",
        "sub_bn": "Jubayer.dev // এআই ও রোবোটিক্স ল্যাব",
        "sub_en": "JUBAYER.DEV | Building Next-Gen Autonomous AI"
    }
]


def create_hud_header_bar() -> Path:
    """Creates a high-tech HUD header bar with developer branding and live indicator."""
    out_path = TEMP_DIR / "hud_header_bar.png"
    w, h = 1080, 100
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Left Branding Badge
    bx, by, bw, bh = 40, 15, 340, 68
    draw.rounded_rectangle((bx, by, bx + bw, by + bh), radius=16, fill=(10, 16, 28, 220), outline=(0, 240, 255, 180), width=2)
    try:
        font_mono = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 30)
    except Exception:
        font_mono = ImageFont.load_default()
    draw.text((bx + 20, by + 16), "</>", fill=(0, 240, 255), font=font_mono)
    draw.text((bx + 75, by + 16), "JUBAYER.DEV", fill=(245, 248, 255), font=font_mono)

    # 2. Right Live Indicator Badge
    rx, ry, rw, rh = w - 40 - 380, 15, 380, 68
    draw.rounded_rectangle((rx, ry, rx + rw, ry + rh), radius=16, fill=(10, 16, 28, 220), outline=(255, 70, 90, 160), width=2)
    draw.ellipse((rx + 25, ry + 24, rx + 45, ry + 44), fill=(255, 45, 75))
    try:
        font_ind = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 22)
    except Exception:
        font_ind = ImageFont.load_default()
    draw.text((rx + 60, ry + 20), "ROBOTICS LAB // 4K", fill=(245, 248, 255), font=font_ind)

    img.save(out_path, "PNG")
    return out_path


def create_developer_outro_slate() -> Path:
    """Creates the cinematic Iron-Man style developer slate with Jubayer's real photo."""
    out_path = TEMP_DIR / "hollywood_outro_slate.png"
    w, h = 1080, 1920
    img = Image.new("RGBA", (w, h), "#060A14")
    draw = ImageDraw.Draw(img)

    # Glowing Cyber Background Blur
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((w//2 - 480, 240, w//2 + 480, 1200), fill=(0, 230, 255, 45))
    gdraw.ellipse((w//2 - 320, 360, w//2 + 320, 1000), fill=(255, 120, 0, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(glow, (0, 0), glow)

    # Jubayer Real Photo
    if JUBAYER_CODING_PHOTO.exists():
        p_img = Image.open(JUBAYER_CODING_PHOTO).convert("RGBA")
    else:
        p_img = Image.new("RGBA", (600, 600), (30, 40, 60))

    face_size = 560
    cropped = p_img.resize((face_size, face_size), Image.Resampling.LANCZOS)

    mask = Image.new("L", (face_size, face_size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0, face_size, face_size), fill=255)

    circular = Image.new("RGBA", (face_size, face_size), (0, 0, 0, 0))
    circular.paste(cropped, (0, 0), mask)

    ccx, ccy = w // 2, 600
    r_base = face_size // 2

    # Iron-Man HUD Arc Reactor / Telemetry Rings
    for r_offset, alpha in [(18, 40), (12, 90), (7, 160), (3, 230)]:
        r = r_base + 6 + r_offset
        draw.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=(0, 240, 255, alpha), width=3)

    draw.ellipse((ccx - r_base - 6, ccy - r_base - 6, ccx + r_base + 6, ccy + r_base + 6), outline="#00F0FF", width=5)
    draw.ellipse((ccx - r_base - 14, ccy - r_base - 14, ccx + r_base + 14, ccy + r_base + 14), outline="#FFB703", width=2)

    # Arc telemetry ticks
    for i in range(48):
        if i % 12 == 0:
            continue
        angle = (2 * math.pi / 48) * i
        r1 = r_base + 8
        r2 = r_base + 22 if i % 4 == 0 else r_base + 15
        x1 = ccx + r1 * math.cos(angle)
        y1 = ccy + r1 * math.sin(angle)
        x2 = ccx + r2 * math.cos(angle)
        y2 = ccy + r2 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill="#38BDF8", width=2)

    img.paste(circular, (ccx - r_base, ccy - r_base), circular)
    draw.ellipse((ccx - r_base, ccy - r_base, ccx + r_base, ccy + r_base), outline=(255, 255, 255, 200), width=2)

    try:
        font_mono_sub = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 26)
        font_hero = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64)
        font_lab = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 34)
        font_badge = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 24)
        font_cta = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 30)
    except Exception:
        font_mono_sub = font_hero = font_lab = font_badge = font_cta = ImageFont.load_default()

    sub_text = "ENGINEERED & ARCHITECTED BY"
    sw = draw.textlength(sub_text, font=font_mono_sub)
    draw.text((w//2 - sw//2, 940), sub_text, fill="#94A3B8", font=font_mono_sub)

    hero_text = "JUBAYER.DEV"
    hw = draw.textlength(hero_text, font=font_hero)
    draw.text((w//2 - hw//2, 990), hero_text, fill="#00F0FF", font=font_hero)

    lab_text = "AI & ROBOTICS AUTOMATION LAB"
    lw = draw.textlength(lab_text, font=font_lab)
    draw.text((w//2 - lw//2, 1080), lab_text, fill="#F8FAFC", font=font_lab)

    badge_y = 1170
    badges = ["HARDWARE ROBOTICS", "AI SYSTEMS", "AUTONOMOUS AGENTS"]
    total_w = sum(draw.textlength(b, font=font_badge) + 36 for b in badges) + 18 * (len(badges) - 1)
    bx = w // 2 - total_w // 2

    for b in badges:
        bw = draw.textlength(b, font=font_badge) + 36
        draw.rounded_rectangle((bx, badge_y, bx + bw, badge_y + 50), radius=12, fill="#0F172A", outline="#00F0FF66", width=2)
        draw.text((bx + 18, badge_y + 11), b, fill="#38BDF8", font=font_badge)
        bx += bw + 18

    # CTA Button
    cta_y = 1300
    cta_w = 520
    draw.rounded_rectangle((w//2 - cta_w//2, cta_y, w//2 + cta_w//2, cta_y + 70), radius=16, fill="#00F0FF")
    cta_text = "NEXT-GEN ENGINEERING"
    cw = draw.textlength(cta_text, font=font_cta)
    draw.text((w//2 - cw//2, cta_y + 18), cta_text, fill="#060A14", font=font_cta)

    img.save(out_path, format="PNG")
    return out_path


async def generate_scene_voiceovers():
    """Generates studio mastered Edge-TTS audio clips for all 5 scenes."""
    print("\n[১/৬] সিনেমাটিক বাংলা ভয়েসওভার সিন্থেসিস হচ্ছে...")
    for sc in SCENES_CONFIG:
        idx = sc["id"]
        out_mp3 = TEMP_DIR / f"hw_scene_{idx}.mp3"
        comm = edge_tts.Communicate(
            text=sc["text"],
            voice="bn-IN-BashkarNeural",
            rate="+12%",
            pitch="+2Hz"
        )
        await comm.save(str(out_mp3))

        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(out_mp3)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dur = float(res.stdout.strip())
        sc["audio_file"] = out_mp3
        sc["duration"] = dur
        print(f"  ▶ সিন {idx} ({sc['clip_file']}): {dur:.2f}s")


def build_ass_subtitles(scenes, total_duration) -> Path:
    """Builds a pixel-perfect .ass subtitle file with Bengali HarfBuzz shaping."""
    ass_path = TEMP_DIR / "hollywood_subtitles.ass"

    header = """[Script Info]
Title: Jubayer Hollywood Robotics Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleBn,Hind Siliguri,52,&H0000FFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3.8,2.2,2,40,40,240,1
Style: SubEn,Consolas,28,&H00FFFF00,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2.2,1.5,2,40,40,195,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def format_ass_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = int(round((sec - int(sec)) * 100))
        if cs >= 100:
            cs = 99
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    events = []
    curr = 0.0
    for sc in scenes:
        dur = sc["duration"]
        start_t = format_ass_time(curr)
        end_t = format_ass_time(curr + dur)
        curr += dur

        bn = sc["sub_bn"]
        en = sc["sub_en"]

        events.append(f"Dialogue: 0,{start_t},{end_t},TitleBn,,0,0,0,,{bn}")
        events.append(f"Dialogue: 0,{start_t},{end_t},SubEn,,0,0,0,,{en}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    return ass_path


def render_all_scene_videos(scenes):
    """Cuts and renders each scene video to exact duration at 1080x1920 30fps."""
    print("\n[২/৬] প্রতিটি সিনের সিনেমাটিক ফুটেজ প্রসেসিং হচ্ছে...")
    rendered_files = []

    for sc in scenes:
        idx = sc["id"]
        dur = sc["duration"]
        out_part = TEMP_DIR / f"hw_part_{idx}.mp4"

        if sc["clip_file"] == "outro_slate":
            slate_img = create_developer_outro_slate()
            vf = (
                f"zoompan=z='min(zoom+0.0006,1.06)':d={int(dur * 30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
                "scale=1080:1920,setsar=1"
            )
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(slate_img),
                "-vf", vf,
                "-t", f"{dur:.3f}",
                "-r", "30",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
                str(out_part)
            ]
        else:
            clip_path = TECH_CLIPS_DIR / sc["clip_file"]
            clip_ss = sc["clip_start"]
            vf = (
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,setsar=1,"
                "eq=contrast=1.08:saturation=1.12"
            )
            cmd = [
                "ffmpeg", "-y",
                "-ss", f"{clip_ss:.2f}",
                "-stream_loop", "-1", "-i", str(clip_path),
                "-vf", vf,
                "-t", f"{dur:.3f}",
                "-r", "30",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
                str(out_part)
            ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rendered_files.append(out_part)
        print(f"  ✅ সিন {idx} রেন্ডার সম্পন্ন ({dur:.2f}s)")

    # Concatenate all parts into a single video
    concat_list = TEMP_DIR / "hw_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in rendered_files:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    concat_video = TEMP_DIR / "hw_concat_raw.mp4"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(concat_video)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return concat_video


def mix_master_audio(scenes, total_duration) -> Path:
    """Concatenates voiceover clips and mixes with cinematic BGM."""
    print("\n[৩/৬] ভয়েসওভার ও সিনেমাটিক ট্রেইলার BGM মিক্সিং...")
    voice_concat_list = TEMP_DIR / "hw_voice_concat.txt"
    with open(voice_concat_list, "w", encoding="utf-8") as f:
        for sc in scenes:
            f.write(f"file '{sc['audio_file'].resolve().as_posix()}'\n")

    raw_voice_full = TEMP_DIR / "hw_voice_full.mp3"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(voice_concat_list),
        "-c", "copy",
        str(raw_voice_full)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    mixed_audio = TEMP_DIR / "hw_mixed_master.mp3"
    fade_start = max(1.0, total_duration - 1.2)

    if BGM_PATH.exists():
        cmd_mix = [
            "ffmpeg", "-y",
            "-i", str(raw_voice_full),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex",
            f"[0:a]volume=1.25,firequalizer=gain_entry='entry(90,4);entry(220,3);entry(3200,2.5)'[voice];"
            f"[1:a]volume=0.14,afade=t=out:st={fade_start:.2f}:d=1.2[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "[aout]",
            "-t", f"{total_duration:.3f}",
            "-c:a", "libmp3lame", "-q:a", "2",
            str(mixed_audio)
        ]
        subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        mixed_audio = raw_voice_full

    return mixed_audio


def render_final_composite(concat_video: Path, mixed_audio: Path, total_duration: float) -> Path:
    """Composites background video, HUD header overlay, and ASS subtitles."""
    print("\n[৪/৬] ফাইনাল কম্পোজিটিং (ভিডিও + HUD বার + হার্ফবাজ বাংলা সাবটাইটেল)...")
    hud_bar = create_hud_header_bar()
    ass_sub = build_ass_subtitles(SCENES_CONFIG, total_duration)

    output_video = OUTPUT_DIR / "jubayer_hollywood_robotics_reel.mp4"

    # Libass filter with HarfBuzz
    ass_path_escaped = str(ass_sub).replace("\\", "/").replace(":", "\\:")

    filter_complex = (
        f"[0:v][1:v]overlay=0:60[v1];"
        f"[v1]ass='{ass_path_escaped}'[vout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(concat_video),
        "-loop", "1", "-i", str(hud_bar),
        "-i", str(mixed_audio),
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "2:a",
        "-t", f"{total_duration:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(output_video)
    ]

    subprocess.run(cmd, check=True)
    print(f"  🎉 ফাইনাল রিলস তৈরি সম্পন্ন: {output_video}")
    return output_video


def send_to_telegram(video_path: Path, caption: str) -> bool:
    """Uploads the generated Hollywood Reel to Jubayer's Telegram chat."""
    print(f"\n[৫/৬] টেলিগ্রামে সরাসরি পাঠানো হচ্ছে (Chat ID: {TELEGRAM_CHAT_ID})...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    try:
        with open(video_path, "rb") as f:
            res = requests.post(
                url,
                data={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "caption": caption,
                    "supports_streaming": True
                },
                files={"video": f},
                timeout=180
            )
        data = res.json()
        if data.get("ok"):
            print("  🚀 টেলিগ্রামে সফলভাবে পৌঁছে গেছে!")
            return True
        else:
            print(f"  ❌ Telegram API Error: {data}")
            return False
    except Exception as e:
        print(f"  ❌ Failed to dispatch to Telegram: {e}")
        return False


def main():
    print("=" * 60)
    print("🤖 JUBAYER.DEV — HOLLYWOOD ROBOTICS LAB REEL PIPELINE")
    print("=" * 60)

    # 1. Voiceover
    asyncio.run(generate_scene_voiceovers())
    total_duration = sum(sc["duration"] for sc in SCENES_CONFIG)
    print(f"\n▶ মোট ভিডিও দৈর্ঘ্য: {total_duration:.2f} সেকেন্ড")

    # 2. Scene videos
    concat_video = render_all_scene_videos(SCENES_CONFIG)

    # 3. Audio mastering
    mixed_audio = mix_master_audio(SCENES_CONFIG, total_duration)

    # 4. Composite final video
    final_video = render_final_composite(concat_video, mixed_audio, total_duration)

    # 5. Extract preview frames for verification
    print("\n[৬/৬] কোয়ালিটি ভেরিফিকেশনের জন্য ফ্রেম এক্সট্র্যাক্ট করা হচ্ছে...")
    for t_sec in [2.0, 10.0, 16.0, 22.0, 28.0]:
        t_sec = min(t_sec, total_duration - 0.5)
        out_f = TEMP_DIR / f"hw_check_{int(t_sec)}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{t_sec:.2f}",
            "-i", str(final_video),
            "-vframes", "1", "-q:v", "2",
            str(out_f)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 6. Telegram Dispatch
    caption = (
        "🎬 **JUBAYER.DEV — HOLLYWOOD ROBOTICS & HARDWARE LAB REEL**\n\n"
        "⚡ **থিম:** সাইবারনেটিক রোবোটিক্স, মাইক্রোচিপ সার্কিট্রি, সিএনসি লেজার ও স্বয়ংক্রিয় মেকানিক্স\n"
        "🤖 **ভিজুয়ালস:**\n"
        "• নিওন সাইবারনেটিক রোবোটিক হ্যান্ড অ্যাক্টিভেশন\n"
        "• ম্যাক্রো মাইক্রোচিপ সোল্ডারিং ও রিয়েল স্মোক\n"
        "• আয়ন ম্যান স্টাইল সিএনসি রোবোটিক লেজার ওয়েল্ডিং স্পার্কস\n"
        "• ইন্ডাস্ট্রিয়াল নিউমেটিক রোবোটিক আর্ম অ্যাসেম্বলি\n"
        "• জুবায়ের ভাইয়ের কোডিং স্টুডিও আর্কিটেক্ট আউটরো\n\n"
        "🔊 **সাউন্ড:** স্টুডিও মাস্টার্ড ডেভেলপার ভয়েসওভার + সিনেমাটিক সিন্থ ট্রেইলার BGM\n"
        "✨ **সাবটাইটেল:** ১০০% নির্ভুল হার্ফবাজ বাংলা ফন্ট ও সাইবার HUD\n\n"
        "#Robotics #ArtificialIntelligence #HardwareEngineering #Cybernetics #JubayerDev #Innovation"
    )

    send_to_telegram(final_video, caption)

    print("\n==================================================")
    print("✅ সমস্ত প্রসেস ১০০% সফলভাবে সম্পন্ন হয়েছে!")
    print(f"📂 ভিডিও ফাইল: {final_video}")
    print("==================================================")


if __name__ == "__main__":
    main()
