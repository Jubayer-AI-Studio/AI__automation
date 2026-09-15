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

def create_ai_photocard(title: str, points: list, category: str = "সিলিকন ভ্যালি টেক ল্যাব ২০৩০") -> Path:
    """
    Creates an elite Computer Science Lab & Silicon Microchip Developer Edition 1080x1080 Facebook Card.
    Features:
    - PCB copper & neon circuit traces with solder pads
    - Terminal window status controls (Ruby, Amber, Emerald) and system telemetry
    - Golden microchip contact pins and glowing processor die cores
    - High-contrast Cyber Gold and Pure White HarfBuzz Bengali typography
    - 100% flawless Indic ligatures via FFmpeg drawtext
    """
    width, height = 1080, 1080
    
    # 1. Base dark silicon substrate canvas (#070913)
    img = Image.new("RGBA", (width, height), (7, 9, 19, 255))

    # Glowing lab ambient lighting (Cyan & Deep Indigo glow)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)

    # High-tech cyan lab glow top-left (chip fabrication chamber feel)
    for r in range(450, 0, -15):
        alpha = int(70 * (1 - r / 450))
        g_draw.ellipse([(150 - r, 100 - r), (150 + r, 100 + r)], fill=(0, 240, 255, alpha))

    # Hot Magenta/Purple quantum core glow bottom-right
    for r in range(450, 0, -15):
        alpha = int(75 * (1 - r / 450))
        g_draw.ellipse([(920 - r, 950 - r), (920 + r, 950 + r)], fill=(236, 72, 153, alpha))

    # Center tensor engine glow
    for r in range(350, 0, -15):
        alpha = int(40 * (1 - r / 350))
        g_draw.ellipse([(540 - r, 500 - r), (540 + r, 500 + r)], fill=(124, 58, 237, alpha))

    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Silicon Wafer / Digital Circuit Grid (Subtle CS Lab Matrix)
    for x in range(40, width, 40):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 8), width=1)
    for y in range(40, height, 40):
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 8), width=1)

    # PCB Circuit Traces with solder pads (Microchip Board traces)
    trace_color = (0, 240, 255, 60)
    draw.line([(40, 40), (200, 40)], fill=trace_color, width=2)
    draw.line([(200, 40), (240, 80)], fill=trace_color, width=2)
    draw.ellipse([(36, 36), (44, 44)], fill=(0, 240, 255, 180))

    draw.line([(width - 40, height - 40), (width - 220, height - 40)], fill=(236, 72, 153, 90), width=2)
    draw.line([(width - 220, height - 40), (width - 260, height - 80)], fill=(236, 72, 153, 90), width=2)
    draw.ellipse([(width - 44, height - 44), (width - 36, height - 36)], fill=(236, 72, 153, 200))

    # Outer Lab Frame with Chamfered Style (GPU Server Chassis style)
    draw.rounded_rectangle([(24, 24), (width - 24, height - 24)], radius=24, outline=(0, 240, 255, 150), width=2)
    draw.rounded_rectangle([(30, 30), (width - 30, height - 30)], radius=20, outline=(139, 92, 246, 70), width=1)

    # Top Terminal Header Bar (Developer / CS Lab Style)
    draw.ellipse([(65, 55), (77, 67)], fill=(255, 95, 86, 255))
    draw.ellipse([(85, 55), (97, 67)], fill=(255, 189, 46, 255))
    draw.ellipse([(105, 55), (117, 67)], fill=(39, 201, 63, 255))

    # System Telemetry Pill (Lab ID)
    draw.rounded_rectangle([(140, 45), (490, 80)], radius=8, fill=(15, 23, 42, 220), outline=(0, 240, 255, 120), width=1)
    
    # Category Badge Pill
    draw.rounded_rectangle([(70, 95), (440, 145)], radius=14, fill=(15, 23, 42, 240), outline=(0, 240, 255, 220), width=2)
    # Chip Icon Graphic (Mini Microchip)
    draw.rectangle([(88, 110), (108, 130)], fill=(0, 240, 255, 255))
    draw.rectangle([(93, 115), (103, 125)], fill=(10, 15, 30, 255))
    for p in [-4, 0, 4]:
        draw.line([(88 + 10 + p, 106), (88 + 10 + p, 109)], fill=(0, 240, 255, 255), width=2)
        draw.line([(88 + 10 + p, 131), (88 + 10 + p, 134)], fill=(0, 240, 255, 255), width=2)

    # Title Separator Line (High-voltage Bus Bar look)
    draw.line([(70, 245), (1010, 245)], fill=(0, 240, 255, 180), width=2)
    draw.line([(70, 248), (480, 248)], fill=(236, 72, 153, 240), width=2)

    # 4 Microchip Architecture Module Cards
    module_configs = [
        {"badge": (0, 240, 255), "tag": "MODULE_01 // TENSOR_CORE_PROCESSING", "fill": (12, 20, 38, 220), "border": (0, 240, 255, 140)},
        {"badge": (236, 72, 153), "tag": "MODULE_02 // NEURAL_LANGUAGE_SYNAPSE", "fill": (25, 14, 38, 220), "border": (236, 72, 153, 140)},
        {"badge": (245, 158, 11), "tag": "MODULE_03 // CODE_COMPILER_AUTOMATION", "fill": (30, 20, 12, 220), "border": (245, 158, 11, 140)},
        {"badge": (16, 185, 129), "tag": "MODULE_04 // GENERATIVE_GRAPHICS_PIPELINE", "fill": (12, 30, 24, 220), "border": (16, 185, 129, 140)},
    ]

    y_positions = [270, 425, 580, 735]
    card_height = 125

    for i, (y_pos, cfg) in enumerate(zip(y_positions, module_configs[:len(points)]), 1):
        # Frosted Silicon Chip Panel
        draw.rounded_rectangle([(70, y_pos), (1010, y_pos + card_height)], radius=16, fill=cfg["fill"], outline=cfg["border"], width=2)
        
        # Golden Microchip Contact Pins (PCB Edge Connector style)
        for pin_y in range(y_pos + 18, y_pos + card_height - 15, 16):
            draw.rounded_rectangle([(62, pin_y), (69, pin_y + 8)], radius=2, fill=(245, 158, 11, 240))
            draw.line([(70, pin_y + 4), (78, pin_y + 4)], fill=cfg["badge"], width=2)
        
        # Glowing Microchip Core Die Badge
        b_left, b_top = 95, y_pos + 32
        draw.rounded_rectangle([(b_left, b_top), (b_left + 60, b_top + 60)], radius=12, fill=cfg["badge"])
        draw.rounded_rectangle([(b_left + 6, b_top + 6), (b_left + 54, b_top + 54)], radius=8, outline=(10, 15, 30, 150), width=2)

    # Modern CS Lab Telemetry Footer
    draw.rounded_rectangle([(70, 930), (1010, 1010)], radius=16, fill=(12, 18, 34, 240), outline=(0, 240, 255, 140), width=2)
    draw.line([(70, 930), (1010, 930)], fill=(236, 72, 153, 200), width=2)

    temp_base_path = TEMP_DIR / "card_base_frame.png"
    img.convert("RGB").save(temp_base_path, format="PNG")

    # 2. Text rendering via FFmpeg HarfBuzz for 100% Bengali ligature accuracy
    filters = []

    # Terminal Telemetry String
    with open(TEMP_DIR / "lab_telemetry.txt", "w", encoding="utf-8") as f:
        f.write("SYS::AI_R&D_LAB // SILICON_CHIP_V4.2")
    filters.append(
        f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/lab_telemetry.txt':fontsize=18:fontcolor=#38BDF8:x=155:y=52"
    )

    # Category Tag (next to microchip icon)
    clean_cat = category.replace("⚡", "").replace("💡", "").replace("📺", "").strip()
    cat_text_file = TEMP_DIR / "card_cat_txt.txt"
    with open(cat_text_file, "w", encoding="utf-8") as f:
        f.write(clean_cat)
    filters.append(
        f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_cat_txt.txt':fontsize=24:fontcolor=#00E5FF:x=120:y=107"
    )

    # Main Title in Cyber Gold
    title_lines = textwrap.wrap(title, width=32)
    if len(title_lines) == 1:
        f_path = TEMP_DIR / "card_title_1.txt"
        with open(f_path, "w", encoding="utf-8") as f:
            f.write(title_lines[0])
        filters.append(
            f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_title_1.txt':fontsize=42:fontcolor=#FDE047:x=70:y=162"
        )
    else:
        for idx, t_line in enumerate(title_lines[:2]):
            f_path = TEMP_DIR / f"card_title_{idx+1}.txt"
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(t_line)
            y_t = 145 + (idx * 48)
            filters.append(
                f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_title_{idx+1}.txt':fontsize=40:fontcolor=#FDE047:x=70:y={y_t}"
            )

    # 4 Silicon Module Cards
    bengali_digits = ["১", "২", "৩", "৪"]
    for i, (y_pos, pt, cfg) in enumerate(zip(y_positions, points[:4], module_configs), 1):
        clean_pt = pt
        for prefix in [f"{i}.", f"{i} .", f"{bengali_digits[i-1]}.", f"{bengali_digits[i-1]} ."]:
            if clean_pt.startswith(prefix):
                clean_pt = clean_pt[len(prefix):].strip()
                break

        # Module developer tag (above text)
        tag_f = TEMP_DIR / f"card_mod_{i}.txt"
        with open(tag_f, "w", encoding="utf-8") as f:
            f.write(cfg["tag"])
        filters.append(
            f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_mod_{i}.txt':fontsize=17:fontcolor=#38BDF8:x=185:y={y_pos + 16}"
        )

        # Digit inside micro-die
        num_f = TEMP_DIR / f"card_num_{i}.txt"
        with open(num_f, "w", encoding="utf-8") as f:
            f.write(bengali_digits[i - 1])
        filters.append(
            f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_num_{i}.txt':fontsize=36:fontcolor=#070913:x=112:y={y_pos + 42}"
        )

        # Point text (pure white bold)
        pt_lines = textwrap.wrap(clean_pt, width=36)
        if len(pt_lines) == 1:
            pt_f = TEMP_DIR / f"card_pt_{i}_1.txt"
            with open(pt_f, "w", encoding="utf-8") as f:
                f.write(pt_lines[0])
            filters.append(
                f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_pt_{i}_1.txt':fontsize=30:fontcolor=#FFFFFF:x=185:y={y_pos + 52}"
            )
        else:
            for l_idx, l_txt in enumerate(pt_lines[:2]):
                pt_f = TEMP_DIR / f"card_pt_{i}_{l_idx+1}.txt"
                with open(pt_f, "w", encoding="utf-8") as f:
                    f.write(l_txt)
                y_l = y_pos + 40 + (l_idx * 36)
                filters.append(
                    f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_pt_{i}_{l_idx+1}.txt':fontsize=28:fontcolor=#FFFFFF:x=185:y={y_l}"
                )

    # Footer CS Lab Telemetry
    footer_text_file = TEMP_DIR / "card_footer_txt.txt"
    with open(footer_text_file, "w", encoding="utf-8") as f:
        f.write("ARCH: NEURAL_TENSOR_NODE // প্রযুক্তির সবশেষ বিশ্লেষণ জানতে পেজটি ফলো রাখুন")
    filters.append(
        f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/card_footer_txt.txt':fontsize=23:fontcolor=#E2E8F0:x=135:y=958"
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

