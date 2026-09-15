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

def create_ai_photocard(title: str, points: list, category: str = "বিশেষ টেক বুলেটিন ২০৩০") -> Path:
    """
    Creates an ultra-modern 2026-2030 futuristic, high-engagement 1080x1080 Facebook infographic card.
    Features:
    - Glowing neon mesh gradients (Cyan, Magenta & Royal Violet)
    - 4 floating frosted-glass point cards with distinct neon badges
    - High-contrast Cyber Gold and Pure White HarfBuzz Bengali typography
    - 100% flawless ligatures on Windows via FFmpeg drawtext
    """
    width, height = 1080, 1080
    
    # 1. Base futuristic dark canvas
    img = Image.new("RGBA", (width, height), (10, 8, 28, 255))

    # Glowing neon mesh gradient bursts
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)

    # Top-right Hot Magenta/Pink glow
    for r in range(420, 0, -12):
        alpha = int(75 * (1 - r / 420))
        g_draw.ellipse([(860 - r, 110 - r), (860 + r, 110 + r)], fill=(236, 72, 153, alpha))

    # Bottom-left Electric Cyan glow
    for r in range(460, 0, -12):
        alpha = int(80 * (1 - r / 460))
        g_draw.ellipse([(140 - r, 930 - r), (140 + r, 930 + r)], fill=(0, 240, 255, alpha))

    # Center Royal Violet ambient warmth
    for r in range(500, 0, -15):
        alpha = int(45 * (1 - r / 500))
        g_draw.ellipse([(540 - r, 540 - r), (540 + r, 540 + r)], fill=(139, 92, 246, alpha))

    img = Image.alpha_composite(img, glow_layer)
    draw = ImageDraw.Draw(img)

    # Futuristic digital grid dot array
    for gx in range(60, width - 60, 60):
        for gy in range(60, height - 60, 60):
            draw.ellipse([(gx - 1, gy - 1), (gx + 1, gy + 1)], fill=(255, 255, 255, 22))

    # Double outer glowing frame (Cyan neon + Violet accent)
    draw.rounded_rectangle([(24, 24), (width - 24, height - 24)], radius=30, outline=(0, 240, 255, 180), width=3)
    draw.rounded_rectangle([(32, 32), (width - 32, height - 32)], radius=24, outline=(139, 92, 246, 80), width=1)

    # Top Category Badge (Glassmorphic Pill with Glowing Live Dot)
    draw.rounded_rectangle([(70, 60), (450, 120)], radius=25, fill=(15, 23, 42, 220), outline=(0, 240, 255, 255), width=2)
    draw.ellipse([(95, 82), (111, 98)], fill=(0, 240, 255, 255))
    draw.ellipse([(92, 79), (114, 101)], outline=(0, 240, 255, 120), width=2)

    # Title Separator Line (Gradient-style Cyan to Magenta)
    draw.line([(70, 240), (1010, 240)], fill=(0, 240, 255, 200), width=3)
    draw.line([(70, 244), (520, 244)], fill=(236, 72, 153, 220), width=2)

    # 4 Floating Glassmorphic Point Cards with Neon Badges
    card_colors = [
        {"badge": (0, 240, 255), "border": (0, 240, 255, 140), "fill": (15, 23, 42, 200)},
        {"badge": (236, 72, 153), "border": (236, 72, 153, 140), "fill": (24, 15, 38, 200)},
        {"badge": (245, 158, 11), "border": (245, 158, 11, 140), "fill": (30, 22, 15, 200)},
        {"badge": (16, 185, 129), "border": (16, 185, 129, 140), "fill": (15, 30, 26, 200)},
    ]

    y_positions = [270, 425, 580, 735]
    card_height = 125

    for i, (y_pos, col) in enumerate(zip(y_positions, card_colors[:len(points)]), 1):
        # Frosted glass card panel
        draw.rounded_rectangle([(70, y_pos), (1010, y_pos + card_height)], radius=20, fill=col["fill"], outline=col["border"], width=2)
        # Left accent glow bar
        draw.rounded_rectangle([(70, y_pos), (76, y_pos + card_height)], radius=3, fill=col["badge"])
        # Neon Number Badge
        b_left, b_top = 100, y_pos + 32
        draw.rounded_rectangle([(b_left, b_top), (b_left + 60, b_top + 60)], radius=15, fill=col["badge"])

    # Modern Footer Bar
    draw.rounded_rectangle([(70, 930), (1010, 1010)], radius=20, fill=(15, 23, 42, 230), outline=(0, 240, 255, 120), width=2)
    draw.line([(70, 930), (1010, 930)], fill=(236, 72, 153, 180), width=2)

    temp_base_path = TEMP_DIR / "card_base_frame.png"
    img.convert("RGB").save(temp_base_path, format="PNG")

    # 2. Text rendering via FFmpeg HarfBuzz for 100% Bengali ligature accuracy
    filters = []

    # Category Tag Text
    clean_cat = category.replace("⚡", "").replace("💡", "").replace("📺", "").strip()
    cat_text_file = TEMP_DIR / "card_cat_txt.txt"
    with open(cat_text_file, "w", encoding="utf-8") as f:
        f.write(clean_cat)
    filters.append(
        f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_cat_txt.txt':fontsize=24:fontcolor=#00E5FF:x=125:y=76"
    )

    # Main Title (High-contrast Cyber Gold for mobile feed eye-catch)
    title_lines = textwrap.wrap(title, width=32)
    if len(title_lines) == 1:
        f_path = TEMP_DIR / "card_title_1.txt"
        with open(f_path, "w", encoding="utf-8") as f:
            f.write(title_lines[0])
        filters.append(
            f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_title_1.txt':fontsize=42:fontcolor=#FDE047:x=70:y=160"
        )
    else:
        for idx, t_line in enumerate(title_lines[:2]):
            f_path = TEMP_DIR / f"card_title_{idx+1}.txt"
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(t_line)
            y_t = 142 + (idx * 48)
            filters.append(
                f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_title_{idx+1}.txt':fontsize=40:fontcolor=#FDE047:x=70:y={y_t}"
            )

    # Numbers and Points inside the 4 Glassmorphic cards
    bengali_digits = ["১", "২", "৩", "৪"]
    for i, (y_pos, pt) in enumerate(zip(y_positions, points[:4]), 1):
        clean_pt = pt
        for prefix in [f"{i}.", f"{i} .", f"{bengali_digits[i-1]}.", f"{bengali_digits[i-1]} ."]:
            if clean_pt.startswith(prefix):
                clean_pt = clean_pt[len(prefix):].strip()
                break

        # Number inside badge
        num_f = TEMP_DIR / f"card_num_{i}.txt"
        with open(num_f, "w", encoding="utf-8") as f:
            f.write(bengali_digits[i - 1])
        filters.append(
            f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_num_{i}.txt':fontsize=36:fontcolor=#090D1A:x=118:y={y_pos + 42}"
        )

        # Point text
        pt_lines = textwrap.wrap(clean_pt, width=36)
        if len(pt_lines) == 1:
            pt_f = TEMP_DIR / f"card_pt_{i}_1.txt"
            with open(pt_f, "w", encoding="utf-8") as f:
                f.write(pt_lines[0])
            filters.append(
                f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_pt_{i}_1.txt':fontsize=32:fontcolor=#FFFFFF:x=190:y={y_pos + 45}"
            )
        else:
            for l_idx, l_txt in enumerate(pt_lines[:2]):
                pt_f = TEMP_DIR / f"card_pt_{i}_{l_idx+1}.txt"
                with open(pt_f, "w", encoding="utf-8") as f:
                    f.write(l_txt)
                y_l = y_pos + 26 + (l_idx * 38)
                filters.append(
                    f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_pt_{i}_{l_idx+1}.txt':fontsize=29:fontcolor=#FFFFFF:x=190:y={y_l}"
                )

    # Footer CTA
    footer_text_file = TEMP_DIR / "card_footer_txt.txt"
    with open(footer_text_file, "w", encoding="utf-8") as f:
        f.write("প্রযুক্তির সবশেষ বিশ্লেষণ ও আপডেটের জন্য পেজটি ফলো রাখুন")
    filters.append(
        f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_footer_txt.txt':fontsize=25:fontcolor=#E2E8F0:x=200:y=958"
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

