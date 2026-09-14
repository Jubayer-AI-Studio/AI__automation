import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.config import FONT_PATH, OUTPUT_DIR, TEMP_DIR

def create_ai_photocard(title: str, points: list, category: str = "কৃত্রিম বুদ্ধিমত্তা ও ভবিষ্যৎ") -> Path:
    """
    Creates an ultra-sleek 1080x1080 square Facebook photo-card / infographic.
    Perfect for Facebook feed image posts!
    """
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height), "#0B0F19")
    draw = ImageDraw.Draw(image)

    # Subtle neon grid/gradient accents
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill="#111827", width=1)

    # Top category badge
    badge_bg = [(80, 80), (450, 135)]
    draw.rounded_rectangle(badge_bg, radius=25, fill="#1E293B", outline="#00FFFF", width=2)

    font_badge = ImageFont.truetype(str(FONT_PATH), 26)
    draw.text((100, 93), f"⚡ {category}", font=font_badge, fill="#00FFFF")

    # Main Title
    font_title = ImageFont.truetype(str(FONT_PATH), 46)
    draw.text((80, 170), title, font=font_title, fill="#FFFFFF")

    draw.line([(80, 245), (1000, 245)], fill="#334155", width=2)

    # Points / Body
    font_body = ImageFont.truetype(str(FONT_PATH), 32)
    font_bullet = ImageFont.truetype(str(FONT_PATH), 34)

    start_y = 285
    for i, pt in enumerate(points, start=1):
        # Bullet box
        draw.rounded_rectangle([(80, start_y), (130, start_y + 50)], radius=12, fill="#0284C7")
        draw.text((95, start_y + 5), str(i), font=font_bullet, fill="#FFFFFF")

        # Point text with word wrapping
        import textwrap
        lines = textwrap.wrap(pt, width=42)
        cur_y = start_y + 5
        for line in lines:
            draw.text((150, cur_y), line, font=font_body, fill="#E2E8F0")
            cur_y += 45

        start_y = max(cur_y + 35, start_y + 110)

    # Footer CTA
    footer_box = [(80, 940), (1000, 1010)]
    draw.rounded_rectangle(footer_box, radius=20, fill="#0F172A", outline="#38BDF8", width=1)
    font_footer = ImageFont.truetype(str(FONT_PATH), 28)
    draw.text((110, 955), "💡 এমন আরও প্রযুক্তি ও এআই তথ্যের জন্য আমাদের পেজটি ফলো করুন", font=font_footer, fill="#94A3B8")

    out_path = OUTPUT_DIR / "ai_photo_post.png"
    image.save(out_path, format="PNG")
    return out_path
