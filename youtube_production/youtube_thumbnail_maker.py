# -*- coding: utf-8 -*-
"""
=============================================================================
🖼️ YOUTUBE THUMBNAIL MAKER (HIGH-CTR 1280x720 16:9 MASTER EDITION)
=============================================================================
ইউটিউব ডকুমেন্টারি ভিডিওর জন্য উচ্চ-ক্লিক রেট (High-CTR) ১২৮০x৭২০ সাইজের
প্রফেশনাল থাম্বনেইল তৈরি করে।
এতে রয়েছে সাইবার নিয়ন ভিজ্যুয়াল, জুবায়েরের স্টুডিও পোর্ট্রেট, HUD রিং এবং
FFmpeg HarfBuzz ইঞ্জিন দ্বারা ১০০% নির্ভুল বাংলা যুক্তাক্ষর টাইপোগ্রাফি।
=============================================================================
"""

import os
import sys
import subprocess
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import OUTPUT_DIR, TEMP_DIR

FONT_REL_PATH = "assets/fonts/HindSiliguri-Bold.ttf"
PRESENTER_IMG_PATH = ROOT_DIR / "assets" / "jubayer_dev_laptop.jpg"


def extract_video_frame(video_path: Path, out_path: Path, time_sec: float = 1.0):
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(time_sec),
        "-i", str(video_path),
        "-frames:v", "1",
        "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720",
        str(out_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def generate_youtube_thumbnail(
    title: str = "কোয়ান্টাম কম্পিউটার: সুপারকম্পিউটারের সমাপ্তি?",
    short_title: str = "কোয়ান্টাম বিপ্লব",
    highlight_tag: str = "⚡ কোটি গুণ দ্রুত গতি!",
    theme: str = "quantum",
    bg_clip_name: str = "quantum_server_room.mp4",
    out_path: Path = None
) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if out_path is None:
        out_path = OUTPUT_DIR / "youtube_thumbnail.jpg"

    width, height = 1280, 720

    bg_clip_file = ROOT_DIR / "assets" / "tech_clips" / bg_clip_name
    extracted_bg = TEMP_DIR / "yt_thumb_extracted_bg.png"

    if bg_clip_file.exists():
        try:
            extract_video_frame(bg_clip_file, extracted_bg, time_sec=1.5)
            bg_img = Image.open(extracted_bg).convert("RGBA")
            bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=2.5))
            enhancer = ImageEnhance.Brightness(bg_img)
            bg_img = enhancer.enhance(0.45)
        except Exception:
            bg_img = Image.new("RGBA", (width, height), (4, 7, 18, 255))
    else:
        bg_img = Image.new("RGBA", (width, height), (4, 7, 18, 255))

    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)

    for x in range(0, 800):
        alpha = int(220 * (1 - (x / 800) ** 1.5))
        g_draw.line([(x, 0), (x, height)], fill=(4, 6, 16, alpha), width=1)

    for r in range(400, 0, -15):
        alpha = int(60 * (1 - r / 400))
        g_draw.ellipse([(150 - r, 100 - r), (150 + r, 100 + r)], fill=(0, 240, 255, alpha))

    for r in range(450, 0, -15):
        alpha = int(70 * (1 - r / 450))
        g_draw.ellipse([(1050 - r, 550 - r), (1050 + r, 550 + r)], fill=(255, 0, 110, alpha))

    for r in range(350, 0, -12):
        alpha = int(50 * (1 - r / 350))
        g_draw.ellipse([(1000 - r, 360 - r), (1000 + r, 360 + r)], fill=(120, 40, 240, alpha))

    canvas = Image.alpha_composite(bg_img, glow)
    draw = ImageDraw.Draw(canvas)

    for x in range(40, width - 40, 60):
        for y in range(40, height - 40, 60):
            draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=(255, 255, 255, 20))

    draw.line([(40, 40), (750, 40)], fill=(0, 240, 255, 120), width=2)
    draw.line([(40, 43), (250, 43)], fill=(255, 0, 110, 200), width=2)

    bracket_len = 30
    for bx, by, dx, dy in [(30, 30, 1, 1), (width - 30, 30, -1, 1), (30, height - 30, 1, -1), (width - 30, height - 30, -1, -1)]:
        draw.line([(bx, by), (bx + dx * bracket_len, by)], fill=(0, 240, 255, 220), width=3)
        draw.line([(bx, by), (bx, by + dy * bracket_len)], fill=(0, 240, 255, 220), width=3)

    if PRESENTER_IMG_PATH.exists():
        p_img = Image.open(PRESENTER_IMG_PATH).convert("RGBA")
        dia = 460
        mask = Image.new("L", (dia, dia), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.ellipse([(0, 0), (dia, dia)], fill=255)

        p_resized = p_img.resize((dia, dia), Image.Resampling.LANCZOS)
        p_crop = Image.new("RGBA", (dia, dia), (0, 0, 0, 0))
        p_crop.paste(p_resized, (0, 0), mask)

        px = width - dia - 60
        py = (height - dia) // 2
        canvas.paste(p_crop, (px, py), p_crop)

        cx = px + dia // 2
        cy = py + dia // 2
        r_outer = dia // 2 + 8
        draw.ellipse([(cx - r_outer, cy - r_outer), (cx + r_outer, cy + r_outer)], outline=(0, 240, 255, 230), width=3)
        
        r_glow = dia // 2 + 14
        draw.ellipse([(cx - r_glow, cy - r_glow), (cx + r_glow, cy + r_glow)], outline=(255, 0, 110, 150), width=2)

        for deg in range(0, 360, 20):
            rad = math.radians(deg)
            x1 = cx + int((r_outer + 4) * math.cos(rad))
            y1 = cy + int((r_outer + 4) * math.sin(rad))
            x2 = cx + int((r_outer + 12) * math.cos(rad))
            y2 = cy + int((r_outer + 12) * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=(0, 240, 255, 180), width=2)

        b_w, b_h = 280, 48
        b_x = cx - b_w // 2
        b_y = py + dia - 24
        draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=12, fill=(8, 14, 30, 245), outline=(0, 240, 255, 220), width=2)

    draw.rounded_rectangle([(50, 60), (380, 105)], radius=10, fill=(15, 23, 42, 230), outline=(255, 0, 110, 220), width=2)
    draw.ellipse([(66, 75), (80, 89)], fill=(255, 0, 110, 255))

    draw.rounded_rectangle([(50, 450), (640, 525)], radius=14, fill=(255, 183, 3, 235), outline=(255, 240, 150, 255), width=2)

    draw.rounded_rectangle([(50, 630), (190, 675)], radius=8, fill=(10, 25, 47, 230), outline=(0, 240, 255, 160), width=2)
    draw.rounded_rectangle([(210, 630), (420, 675)], radius=8, fill=(20, 10, 35, 230), outline=(255, 0, 110, 160), width=2)
    draw.rounded_rectangle([(440, 630), (660, 675)], radius=8, fill=(10, 30, 20, 230), outline=(0, 230, 150, 160), width=2)

    temp_base = TEMP_DIR / "yt_thumb_base.png"
    canvas.convert("RGB").save(temp_base, format="PNG")

    filters = []

    f_cat = TEMP_DIR / "yt_txt_cat.txt"
    with open(f_cat, "w", encoding="utf-8") as f:
        f.write("TECH DOCUMENTARY 2026")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_cat.txt':fontsize=20:fontcolor=#FFFFFF:x=95:y=72")

    f_wm = TEMP_DIR / "yt_txt_wm.txt"
    with open(f_wm, "w", encoding="utf-8") as f:
        f.write("</> JUBAYER.DEV | EXCLUSIVE")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_wm.txt':fontsize=20:fontcolor=#00E5FF:x=940:y=45")

    f_name = TEMP_DIR / "yt_txt_name.txt"
    with open(f_name, "w", encoding="utf-8") as f:
        f.write("JUBAYER // DEV & AI SPECIALIST")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_name.txt':fontsize=16:fontcolor=#38BDF8:x=875:y=594")

    f_title1 = TEMP_DIR / "yt_txt_title1.txt"
    with open(f_title1, "w", encoding="utf-8") as f:
        f.write(short_title)
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_title1.txt':fontsize=70:fontcolor=#000000:x=56:y=156")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_title1.txt':fontsize=70:fontcolor=#FDE047:x=50:y=150")

    sub_title = "সুপারকম্পিউটারের শেষ দিন?" if "সুপারকম্পিউটার" in title else "মানব সভ্যতার সবচেয়ে বড় বিপ্লব"
    f_title2 = TEMP_DIR / "yt_txt_title2.txt"
    with open(f_title2, "w", encoding="utf-8") as f:
        f.write(sub_title)
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_title2.txt':fontsize=48:fontcolor=#000000:x=54:y=274")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_title2.txt':fontsize=48:fontcolor=#FFFFFF:x=50:y=270")

    third_line = "দশ হাজার বছরের কাজ মাত্র ৩ মিনিটে!"
    f_title3 = TEMP_DIR / "yt_txt_title3.txt"
    with open(f_title3, "w", encoding="utf-8") as f:
        f.write(third_line)
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_title3.txt':fontsize=36:fontcolor=#00E5FF:x=50:y=360")

    clean_high = highlight_tag.replace("⚡", "").replace("🔥", "").replace("🚀", "").strip()
    f_high = TEMP_DIR / "yt_txt_high.txt"
    with open(f_high, "w", encoding="utf-8") as f:
        f.write(">> " + clean_high)
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_high.txt':fontsize=34:fontcolor=#000000:x=75:y=468")

    with open(TEMP_DIR / "yt_txt_b1.txt", "w", encoding="utf-8") as f:
        f.write("4K UHD")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_b1.txt':fontsize=22:fontcolor=#00E5FF:x=78:y=642")

    with open(TEMP_DIR / "yt_txt_b2.txt", "w", encoding="utf-8") as f:
        f.write("DEEP DIVE EXCLUSIVE")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_b2.txt':fontsize=20:fontcolor=#F43F5E:x=225:y=643")

    with open(TEMP_DIR / "yt_txt_b3.txt", "w", encoding="utf-8") as f:
        f.write("FULL EXPLANATION")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_txt_b3.txt':fontsize=20:fontcolor=#10B981:x=455:y=643")

    filter_chain = ",".join(filters)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_base),
        "-vf", filter_chain,
        "-frames:v", "1",
        "-q:v", "2",
        str(out_path)
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[ThumbnailMaker] সফলভাবে ১২৮০x৭২০ থাম্বনেইল তৈরি হয়েছে: {out_path}")
    return out_path


if __name__ == "__main__":
    print("=" * 60)
    print("🖼️ [TEST] ইউটিউব হাই-সিটিআর থাম্বনেইল জেনারেটর")
    print("=" * 60)
    res = generate_youtube_thumbnail()
    print(f"✅ থাম্বনেইল প্রস্তুত: {res} ({res.stat().st_size / 1024:.1f} KB)")
