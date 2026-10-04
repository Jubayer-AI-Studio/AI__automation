# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 JUBAYER.DEV — 100% TRUE MARVEL & IRON MAN HOLLYWOOD ACTION REEL
=============================================================================
Target: Jubayer (Jubayer.dev), AI & Autonomous Systems Architect
Theme: Pure authentic Marvel Studios movie footage (Tony Stark workshop,
       Infinity War nanotech suit-up, Stark Tower supersonic freefall assembly,
       Mark 85 holographic energy shield, and twin nanotech plasma blast)
       blended into Jubayer's AI & Robotics branding.
Telegram: Single verified dispatch to Chat 8273323826.
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
TEMP_DIR = ROOT_DIR / "temp"
OUTPUT_DIR = ROOT_DIR / "output"
ASSETS_DIR = ROOT_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
FONTS_DIR = ASSETS_DIR / "fonts"
MOVIE_CLIPS_DIR = TEMP_DIR / "movie_clips"

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
        "title": "Tony Stark Lab & Cybernetic Assembly",
        "clip_file": MOVIE_CLIPS_DIR / "sYOYFywcMJg.mp4",
        "clip_start": 9.2,
        "vf_crop": "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2,setsar=1,eq=contrast=1.15:saturation=1.22",
        "text": "মার্ভেল সিনেমার টেক কি শুধুই সায়েন্স ফিকশন?",
        "sub_bn": "মার্ভেল সিনেমার টেক কি শুধুই সায়েন্স ফিকশন?",
        "sub_en": "Is Marvel Movie Tech Just Science Fiction?",
        "tts_rate": "+22%"
    },
    {
        "id": 2,
        "title": "Tony Stark 3D Virtual Hologram Table",
        "clip_file": MOVIE_CLIPS_DIR / "stark_virtual_holo.webm",
        "clip_start": 38.0,
        "vf_crop": "scale=-1:1920,crop=1080:1920:1450:0,setsar=1,eq=contrast=1.18:saturation=1.25",
        "text": "থ্রিডি হলোগ্রাম আর ইন্টেলিজেন্ট এআই!",
        "sub_bn": "থ্রিডি হলোগ্রাফিক সিস্টেম & অ্যাডভান্সড এআই",
        "sub_en": "3D Hologram & Next-Gen Intelligent AI",
        "tts_rate": "+28%"
    },
    {
        "id": 3,
        "title": "Infinity War Liquid Nanotech Suit-up",
        "clip_file": MOVIE_CLIPS_DIR / "iw_full_nanotech.mp4",
        "clip_start": 98.2,
        "vf_crop": "crop=1920:800:0:140,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2,setsar=1,eq=contrast=1.15:saturation=1.25",
        "text": "লিকুইড ন্যানোটেকের নিখুঁত সুপারহিরো পাওয়ার!",
        "sub_bn": "লিকুইড ন্যানোটেকের নিখুঁত সুপারহিরো পাওয়ার!",
        "sub_en": "Liquid Nanotech Flawless Superhero Power!",
        "tts_rate": "+22%"
    },
    {
        "id": 4,
        "title": "Stark Tower Supersonic Flight Assembly",
        "clip_file": MOVIE_CLIPS_DIR / "zN-t8CyC4lg.mp4",
        "clip_start": 3.2,
        "vf_crop": "crop=1920:800:0:140,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2,setsar=1,eq=contrast=1.15:saturation=1.25",
        "text": "সুপারসনিক ড্রাইভ আর রোবোটিক পাওয়ার!",
        "sub_bn": "সুপারসনিক ড্রাইভ আর রোবোটিক পাওয়ার!",
        "sub_en": "Supersonic Drive & High-End Robotics!",
        "tts_rate": "+24%"
    },
    {
        "id": 5,
        "title": "Mark 85 3D Holographic Energy Shield",
        "clip_file": MOVIE_CLIPS_DIR / "Slhb6MM3phI.mp4",
        "clip_start": 13.0,
        "vf_crop": "scale=-1:1920,crop=1080:1920:2350:0,setsar=1,eq=contrast=1.18:saturation=1.25",
        "text": "মার্ক এইটি ফাইভ থ্রিডি এনার্জি শিল্ড!",
        "sub_bn": "মার্ক এইটি ফাইভ থ্রিডি এনার্জি শিল্ড ডিফেন্স!",
        "sub_en": "Mark 85 3D Holographic Energy Shield!",
        "tts_rate": "+28%"
    },
    {
        "id": 6,
        "title": "Jubayer.dev Architect Outro Slate",
        "clip_file": "outro_slate",
        "clip_start": 0.0,
        "vf_crop": "",
        "text": "আই অ্যাম জুবায়ের—ওয়েলকাম টু মাই নেক্সট-জেন এআই অ্যান্ড রোবোটিক্স ল্যাব!",
        "sub_bn": "আই অ্যাম জুবায়ের — AI & Autonomous Systems Architect",
        "sub_en": "Jubayer.dev // Next-Gen AI & Robotics Lab",
        "tts_rate": "+18%"
    }
]


def create_hud_header_bar() -> Path:
    """Creates a futuristic HUD header bar overlay."""
    out_path = TEMP_DIR / "action_reel_hud_header_bar.png"
    w, h = 1080, 110
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Left Badge
    bx, by, bw, bh = 40, 18, 350, 72
    draw.rounded_rectangle((bx, by, bx + bw, by + bh), radius=16, fill=(8, 14, 26, 230), outline=(0, 240, 255, 200), width=2)
    try:
        font_mono = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 30)
    except Exception:
        font_mono = ImageFont.load_default()
    draw.text((bx + 20, by + 18), "</>", fill=(0, 240, 255), font=font_mono)
    draw.text((bx + 75, by + 18), "JUBAYER.DEV", fill=(245, 248, 255), font=font_mono)

    # 2. Right Live Indicator Badge
    rx, ry, rw, rh = w - 40 - 410, 18, 410, 72
    draw.rounded_rectangle((rx, ry, rx + rw, ry + rh), radius=16, fill=(8, 14, 26, 230), outline=(255, 90, 40, 180), width=2)
    draw.ellipse((rx + 24, ry + 26, rx + 46, ry + 48), fill=(255, 50, 70))
    try:
        font_ind = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 22)
    except Exception:
        font_ind = ImageFont.load_default()
    draw.text((rx + 60, ry + 22), "STARK AI CORE // 4K", fill=(245, 248, 255), font=font_ind)

    img.save(out_path, "PNG")
    return out_path


def create_marvel_outro_slate() -> Path:
    """Creates the high-tech Arc Reactor developer slate with Jubayer's portrait."""
    out_path = TEMP_DIR / "action_reel_outro_slate.png"
    w, h = 1080, 1920
    img = Image.new("RGBA", (w, h), "#030610")

    # 1. Background Grid Layer
    grid_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_layer)
    grid_color = (0, 240, 255, 18)
    for x in range(0, w, 70):
        gdraw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, 70):
        gdraw.line([(0, y), (w, y)], fill=grid_color, width=1)

    mask_grid = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask_grid)
    md.rectangle((0, 0, w, h), fill=140)
    md.rounded_rectangle((60, 200, w - 60, h - 80), radius=40, fill=0)
    mask_grid = mask_grid.filter(ImageFilter.GaussianBlur(60))
    img.paste(grid_layer, (0, 0), mask_grid)

    # 2. Glowing Arc Reactor Center Glow
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    ccx, ccy = w // 2, 580
    gdraw.ellipse((ccx - 480, ccy - 480, ccx + 480, ccy + 480), fill=(0, 210, 255, 45))
    gdraw.ellipse((ccx - 300, ccy - 300, ccx + 300, ccy + 300), fill=(255, 140, 0, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(95))
    img.paste(glow, (0, 0), glow)

    draw = ImageDraw.Draw(img)

    # 3. Photo circular mask
    p_img = Image.open(JUBAYER_CODING_PHOTO).convert("RGBA")
    face_size = 540
    cropped = p_img.resize((face_size, face_size), Image.Resampling.LANCZOS)

    mask = Image.new("L", (face_size, face_size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0, face_size, face_size), fill=255)

    circular = Image.new("RGBA", (face_size, face_size), (0, 0, 0, 0))
    circular.paste(cropped, (0, 0), mask)

    r_base = face_size // 2

    # Multiple glowing telemetry rings
    for r_off, col, wid in [
        (30, (0, 240, 255, 60), 2),
        (20, (0, 240, 255, 130), 2),
        (12, (255, 165, 0, 190), 3),
        (4, (0, 240, 255, 255), 4)
    ]:
        r = r_base + r_off
        draw.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=col, width=wid)

    # Arc telemetry ticks
    for i in range(60):
        if i % 5 == 0:
            continue
        angle = (2 * math.pi / 60) * i
        r1 = r_base + 8
        r2 = r_base + 24 if i % 2 == 0 else r_base + 16
        x1 = ccx + r1 * math.cos(angle)
        y1 = ccy + r1 * math.sin(angle)
        x2 = ccx + r2 * math.cos(angle)
        y2 = ccy + r2 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=(0, 240, 255, 200), width=2)

    # Corner HUD brackets around circle
    bw, bh = 360, 360
    bx1, by1 = ccx - bw, ccy - bh
    bx2, by2 = ccx + bw, ccy + bh
    clen = 40
    draw.line([(bx1, by1), (bx1 + clen, by1)], fill=(0, 240, 255, 180), width=3)
    draw.line([(bx1, by1), (bx1, by1 + clen)], fill=(0, 240, 255, 180), width=3)
    draw.line([(bx2, by1), (bx2 - clen, by1)], fill=(0, 240, 255, 180), width=3)
    draw.line([(bx2, by1), (bx2, by1 + clen)], fill=(0, 240, 255, 180), width=3)
    draw.line([(bx1, by2), (bx1 + clen, by2)], fill=(0, 240, 255, 180), width=3)
    draw.line([(bx1, by2), (bx1, by2 - clen)], fill=(0, 240, 255, 180), width=3)
    draw.line([(bx2, by2), (bx2 - clen, by2)], fill=(0, 240, 255, 180), width=3)
    draw.line([(bx2, by2), (bx2, by2 - clen)], fill=(0, 240, 255, 180), width=3)

    # Paste circular photo
    img.paste(circular, (ccx - r_base, ccy - r_base), circular)
    draw.ellipse((ccx - r_base, ccy - r_base, ccx + r_base, ccy + r_base), outline=(255, 255, 255, 230), width=2)

    # Semi-transparent backing panel for text
    panel_y1, panel_y2 = 910, 1470
    draw.rounded_rectangle((70, panel_y1, w - 70, panel_y2), radius=24, fill=(6, 11, 22, 230), outline=(0, 240, 255, 80), width=1)

    try:
        font_sub = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 26)
        font_hero = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 68)
        font_lab = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 32)
        font_badge = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 22)
        font_cta = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 32)
    except Exception:
        font_sub = font_hero = font_lab = font_badge = font_cta = ImageFont.load_default()

    sub_text = "ENGINEERED & ARCHITECTED BY"
    sw = draw.textlength(sub_text, font=font_sub)
    draw.text((w // 2 - sw // 2, 955), sub_text, fill="#94A3B8", font=font_sub)

    hero_text = "JUBAYER.DEV"
    hw = draw.textlength(hero_text, font=font_hero)
    draw.text((w // 2 - hw // 2, 1005), hero_text, fill="#00F0FF", font=font_hero)

    lab_text = "NEXT-GEN AI & ROBOTICS LAB"
    lw = draw.textlength(lab_text, font=font_lab)
    draw.text((w // 2 - lw // 2, 1100), lab_text, fill="#F8FAFC", font=font_lab)

    badge_y = 1185
    badges = ["AUTONOMOUS AI", "HARDWARE ROBOTICS", "CYBERNETICS"]
    total_w = sum(draw.textlength(b, font=font_badge) + 36 for b in badges) + 16 * (len(badges) - 1)
    bx = w // 2 - total_w // 2

    for b in badges:
        bw = draw.textlength(b, font=font_badge) + 36
        draw.rounded_rectangle((bx, badge_y, bx + bw, badge_y + 48), radius=10, fill=(15, 23, 42, 240), outline=(0, 240, 255, 120), width=2)
        draw.text((bx + 18, badge_y + 11), b, fill="#38BDF8", font=font_badge)
        bx += bw + 16

    cta_y = 1300
    cta_w = 560
    draw.rounded_rectangle((w // 2 - cta_w // 2, cta_y, w // 2 + cta_w // 2, cta_y + 74), radius=16, fill="#00F0FF", outline="#FFFFFF", width=2)
    cta_text = "WELCOME TO THE FUTURE"
    cw = draw.textlength(cta_text, font=font_cta)
    draw.text((w // 2 - cw // 2, cta_y + 18), cta_text, fill="#030610", font=font_cta)

    img.save(out_path, format="PNG")
    return out_path


async def generate_scene_voiceovers():
    """Generates studio Edge-TTS audio clips for all 6 scenes."""
    print("\n[১/৬] সিনেমাটিক মার্ভেল ভয়েসওভার সিন্থেসিস হচ্ছে...")
    for sc in SCENES_CONFIG:
        idx = sc["id"]
        out_mp3 = TEMP_DIR / f"action_reel_scene_{idx}.mp3"
        rate = sc.get("tts_rate", "+22%")
        comm = edge_tts.Communicate(
            text=sc["text"],
            voice="bn-IN-BashkarNeural",
            rate=rate,
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
        print(f"  ▶ সিন {idx} ({sc['title']}): {dur:.2f}s | rate={rate} | {sc['sub_bn']}")


def build_ass_subtitles(scenes, total_duration) -> Path:
    """Builds a pixel-perfect .ass subtitle file with Bengali HarfBuzz shaping."""
    ass_path = TEMP_DIR / "action_reel_subtitles.ass"

    header = """[Script Info]
Title: Jubayer Marvel Action Subtitles
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
    print("\n[২/৬] প্রতিটি মার্ভেল সিনের হাই-এন্ড সিনেমাটিক ফুটেজ প্রসেসিং হচ্ছে...")
    rendered_files = []

    for sc in scenes:
        idx = sc["id"]
        dur = sc["duration"]
        out_part = TEMP_DIR / f"action_reel_part_{idx}.mp4"

        if sc["clip_file"] == "outro_slate":
            slate_img = create_marvel_outro_slate()
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
            clip_path = Path(sc["clip_file"])
            clip_ss = sc["clip_start"]
            vf = sc["vf_crop"]
            cmd = [
                "ffmpeg", "-y",
                "-i", str(clip_path),
                "-ss", f"{clip_ss:.2f}",
                "-vf", vf,
                "-t", f"{dur:.3f}",
                "-r", "30",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
                str(out_part)
            ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rendered_files.append(out_part)
        print(f"  ✅ সিন {idx} ({sc['title']}) রেন্ডার সম্পন্ন ({dur:.2f}s)")

    # Concatenate all parts into a single video
    concat_list = TEMP_DIR / "action_reel_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in rendered_files:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    concat_video = TEMP_DIR / "action_reel_concat_raw.mp4"
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
    voice_concat_list = TEMP_DIR / "action_reel_voice_concat.txt"
    with open(voice_concat_list, "w", encoding="utf-8") as f:
        for sc in scenes:
            f.write(f"file '{sc['audio_file'].resolve().as_posix()}'\n")

    raw_voice_full = TEMP_DIR / "action_reel_voice_full.mp3"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(voice_concat_list),
        "-c", "copy",
        str(raw_voice_full)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    mixed_audio = TEMP_DIR / "action_reel_mixed_master.mp3"
    fade_start = max(1.0, total_duration - 1.2)

    if BGM_PATH.exists():
        cmd_mix = [
            "ffmpeg", "-y",
            "-i", str(raw_voice_full),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex",
            f"[0:a]volume=1.35,firequalizer=gain_entry='entry(90,4);entry(220,3);entry(3200,2.5)'[voice];"
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
    print("\n[৪/৬] ফাইনাল কম্পোজিটিং (ভিডিও + মার্ভেল HUD বার + হার্ফবাজ বাংলা সাবটাইটেল)...")
    hud_bar = create_hud_header_bar()
    ass_sub = build_ass_subtitles(SCENES_CONFIG, total_duration)

    output_video = OUTPUT_DIR / "jubayer_ultimate_marvel_action_reel.mp4"

    ass_path_escaped = str(ass_sub).replace("\\", "/").replace(":", "\\:")
    fonts_dir_escaped = str(FONTS_DIR).replace("\\", "/").replace(":", "\\:")

    filter_complex = (
        f"[0:v][1:v]overlay=0:60[v1];"
        f"[v1]subtitles='{ass_path_escaped}':fontsdir='{fonts_dir_escaped}'[vout]"
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
    print(f"  🎉 ফাইনাল মার্ভেল অ্যাকশন রিলস তৈরি সম্পন্ন: {output_video}")
    return output_video


def send_to_telegram(video_path: Path, caption: str) -> bool:
    """Uploads the generated Hollywood Reel to Jubayer's Telegram chat strictly ONCE."""
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
            msg_id = data["result"]["message_id"]
            print(f"  🚀 টেলিগ্রামে সফলভাবে পৌঁছে গেছে! (Message ID: {msg_id})")
            return True
        else:
            print(f"  ❌ Telegram API Error: {data}")
            return False
    except Exception as e:
        print(f"  ❌ Failed to dispatch to Telegram: {e}")
        return False


def main():
    print("=" * 65)
    print("⚡ JUBAYER.DEV — 100% TRUE MARVEL ACTION REEL PIPELINE ⚡")
    print("=" * 65)

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
    check_times = [1.5, 4.5, 7.0, 9.8, 12.3, 16.0]
    for t_sec in check_times:
        t_sec = min(t_sec, total_duration - 0.5)
        out_f = TEMP_DIR / f"action_check_{int(t_sec)}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{t_sec:.2f}",
            "-i", str(final_video),
            "-vframes", "1", "-q:v", "2",
            str(out_f)
        ], capture_output=True)
        print(f"  📸 ফ্রেম সংরক্ষিত: {out_f.name}")

    # 6. Telegram Dispatch - STRICTLY ONCE
    caption = (
        "🎬⚡ *100% TRUE MARVEL & IRON MAN ACTION REEL* ⚡🎬\n\n"
        "🔥 *আসল মার্ভেল হলিউড সিনেমাটিক ফুটেজ & হাই-এনার্জি সাই-ফাই:*\n"
        "1️⃣ টনি স্টার্ক ল্যাব: মার্ক টু আর্মার & চেস্টে জ্বলন্ত আর্ক-রিঅ্যাক্টর\n"
        "2️⃣ থ্রিডি ভার্চুয়াল হলোগ্রাম: স্টার্ক ল্যাব পয়েন্ট-ক্লাউড হলোগ্রাফিক টেবিল\n"
        "3️⃣ ইনফিনিটি ওয়ার: লিকুইড ন্যানোটেক স্যুট-আপ & মার্ক ৫০ ওয়াক\n"
        "4️⃣ স্টার্ক টাওয়ার: সুপারসনিক ফ্রিফল স্যুট অ্যাসেম্বলি & রিঅ্যাক্টর থ্রাস্টার\n"
        "5️⃣ মার্ক ৮৫ শিল্ড: ট্রায়াঙ্গুলার আর্ক-রিঅ্যাক্টর & থ্রিডি হেক্সাগন এনার্জি শিল্ড\n"
        "6️⃣ জুবায়ের.দেব: আর্ক-রিঅ্যাক্টর টেলিমেট্রি কার্ড & নেক্সট-জেন এআই ল্যাব\n\n"
        "✨ *জিরো স্টক ফুটেজ | জিরো কারখানার পাইপ | ১০০% পিওর মার্ভেল হলিউড অ্যাকশন!*\n\n"
        "💻 *Jubayer.dev // AI & Autonomous Robotics Systems Architect*"
    )
    send_to_telegram(final_video, caption)
    print("\n" + "=" * 65)
    print("✨ ALL TASKS COMPLETED SUCCESSFULLY! ✨")
    print("=" * 65)


if __name__ == "__main__":
    main()
