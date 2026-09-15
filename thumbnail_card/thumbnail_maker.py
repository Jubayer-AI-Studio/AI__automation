# -*- coding: utf-8 -*-
"""
=============================================================================
🖼️ 3. THUMBNAIL & PHOTO POST ENGINE (থাম্বনেইল ও ফটো পোস্ট)
=============================================================================
এই ফাইলে ফেসবুক ফিডের জন্য ১০৮০x১০৮০ স্কয়ার ইনফোগ্রাফিক ফটো পোস্ট ও থাম্বনেইল
তৈরি করার কোড থাকে।

এখানে FFmpeg HarfBuzz ইঞ্জিন ব্যবহার করা হয়েছে, যার কারণে "বুদ্ধিমত্তা", "ভবিষ্যৎ",
"প্রযুক্তি" ইত্যাদি বাংলা যুক্তাক্ষর ১০০% নিখুঁতভাবে ও প্রফেশনাল ফন্টে প্রদর্শিত হয়।

কোনো কালার, ফন্ট সাইজ বা লেআউট পরিবর্তন করতে চাইলে এই ফাইলে পরিবর্তন করবেন।
টেস্ট করার জন্য টার্মিনালে চালান:
    python thumbnail_card/thumbnail_maker.py
=============================================================================
"""

import os
import sys
import subprocess
import textwrap
from pathlib import Path

# Ensure project root is in sys.path for standalone runs
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PIL import Image, ImageDraw, ImageFont
from src.config import FONT_PATH, OUTPUT_DIR, TEMP_DIR

FONT_REL_PATH = "assets/fonts/HindSiliguri-Bold.ttf"

def create_ai_photocard(title: str, points: list, category: str = "কৃত্রিম বুদ্ধিমত্তা ও ভবিষ্যৎ") -> Path:
    """
    Creates a premium 1080x1080 square Facebook infographic photo-card.
    Uses FFmpeg HarfBuzz to ensure 100% flawless Bengali ligature shaping.
    """
    width, height = 1080, 1080
    
    # 1. Generate base UI frame with PIL (shapes, borders, colors)
    base_img = Image.new("RGB", (width, height), "#080D1A")
    draw = ImageDraw.Draw(base_img)

    # Subtle neon grid pattern
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill="#0F172A", width=1)

    # Glowing outer border
    draw.rounded_rectangle([(24, 24), (width - 24, height - 24)], radius=24, outline="#00E5FF", width=3)

    # Category Pill Background
    draw.rounded_rectangle([(70, 55), (460, 115)], radius=20, fill="#132038", outline="#00E5FF", width=2)

    # Horizontal Divider
    draw.line([(70, 250), (1010, 250)], fill="#00E5FF", width=3)
    draw.line([(70, 254), (1010, 254)], fill="#1E293B", width=1)

    # Point Bullet Boxes (4 items)
    y_positions = [280, 430, 580, 730]
    font_num = ImageFont.truetype(str(FONT_PATH), 32)
    for i, y_pos in enumerate(y_positions[:len(points)], 1):
        # Cyan glowing number box
        draw.rounded_rectangle([(70, y_pos), (130, y_pos + 55)], radius=12, fill="#0284C7", outline="#38BDF8", width=2)
        draw.text((90, y_pos + 6), str(i), font=font_num, fill="#FFFFFF")

    # Footer CTA Box
    draw.rounded_rectangle([(70, 930), (1010, 1005)], radius=18, fill="#0F172A", outline="#38BDF8", width=2)

    temp_base_path = TEMP_DIR / "card_base_frame.png"
    base_img.save(temp_base_path, format="PNG")

    # 2. Prepare text files for FFmpeg HarfBuzz text rendering
    filters = []

    # Category
    clean_cat = category.replace("⚡", "").replace("💡", "").strip()
    cat_text_file = TEMP_DIR / "card_cat_txt.txt"
    with open(cat_text_file, "w", encoding="utf-8") as f:
        f.write(f"• {clean_cat}")
    filters.append(
        f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_cat_txt.txt':fontsize=24:fontcolor=#00E5FF:x=105:y=72"
    )

    # Title lines (explicit coordinates)
    title_lines = textwrap.wrap(title, width=32)
    if len(title_lines) == 1:
        f_path = TEMP_DIR / "card_title_1.txt"
        with open(f_path, "w", encoding="utf-8") as f:
            f.write(title_lines[0])
        filters.append(
            f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_title_1.txt':fontsize=38:fontcolor=white:x=70:y=165"
        )
    else:
        for idx, t_line in enumerate(title_lines[:2]):
            f_path = TEMP_DIR / f"card_title_{idx+1}.txt"
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(t_line)
            y_t = 145 + (idx * 48)
            filters.append(
                f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_title_{idx+1}.txt':fontsize=36:fontcolor=white:x=70:y={y_t}"
            )

    # Bullet points (explicit coordinates)
    for i, pt in enumerate(points[:4], 1):
        clean_pt = pt
        for prefix in [f"{i}.", f"{i} .", f"{['১','২','৩','৪'][i-1]}.", f"{['১','২','৩','৪'][i-1]} ."]:
            if clean_pt.startswith(prefix):
                clean_pt = clean_pt[len(prefix):].strip()
                break

        pt_lines = textwrap.wrap(clean_pt, width=38)
        y_pos = y_positions[i - 1]

        if len(pt_lines) == 1:
            pt_f = TEMP_DIR / f"card_pt_{i}_1.txt"
            with open(pt_f, "w", encoding="utf-8") as f:
                f.write(pt_lines[0])
            filters.append(
                f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_pt_{i}_1.txt':fontsize=28:fontcolor=#F1F5F9:x=155:y={y_pos + 12}"
            )
        else:
            for line_idx, line_txt in enumerate(pt_lines[:2]):
                pt_f = TEMP_DIR / f"card_pt_{i}_{line_idx+1}.txt"
                with open(pt_f, "w", encoding="utf-8") as f:
                    f.write(line_txt)
                y_line = y_pos + 4 + (line_idx * 34)
                filters.append(
                    f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_pt_{i}_{line_idx+1}.txt':fontsize=26:fontcolor=#F1F5F9:x=155:y={y_line}"
                )

    # Footer CTA
    footer_text_file = TEMP_DIR / "card_footer_txt.txt"
    with open(footer_text_file, "w", encoding="utf-8") as f:
        f.write("প্রযুক্তি ও এআই-এর নিত্যনতুন তথ্যের জন্য আমাদের পেজটি ফলো করুন")
    filters.append(
        f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_footer_txt.txt':fontsize=24:fontcolor=#94A3B8:x=115:y=954"
    )

    out_path = OUTPUT_DIR / "ai_photo_post.png"
    filter_chain = ",".join(filters)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_base_path),
        "-vf", filter_chain,
        "-frames:v", "1",
        str(out_path)
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_path

# =============================================================================
# স্বতন্ত্র টেস্ট কোড (টার্মিনালে সরাসরি চালিয়ে চেক করার জন্য)
# =============================================================================
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 60)
    print("🖼️ [THUMBNAIL TEST] ১০৮০x১০৮০ ফটো কার্ড ও থাম্বনেইল রেন্ডারিং")
    print("=" * 60)

    test_title = "২০৩০ সালে যে ৪টি চাকরি এআই আমূল বদলে দেবে"
    test_points = [
        "১. ডাটা এন্ট্রি ও বেসিক কাস্টমার সাপোর্ট অপারেটর",
        "২. সাধারণ অনুবাদ ও বেসিক প্রুফরিডিং কাজ",
        "৩. প্রাথমিক কোডিং ও সহজ ওয়েবসাইট বাগ ফিক্সিং",
        "৪. সাধারণ গ্রাফিক্স ডিজাইন ও রুটিন সোশ্যাল মিডিয়া পোস্ট"
    ]
    test_cat = "কৃত্রিম বুদ্ধিমত্তা ও ক্যারিয়ার"

    card_path = create_ai_photocard(test_title, test_points, test_cat)
    print(f"✅ সফলভাবে ফটো পোস্ট থাম্বনেইল রেন্ডার হয়েছে!")
    print(f"📂 ফাইল লোকেশন: {card_path}")
    print("=" * 60)

