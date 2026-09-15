# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 VIDEO PRODUCTION ENGINE (JUBAYER.DEV DEVELOPER EDITION - FINAL)
=============================================================================
এই ইঞ্জিনে ফেসবুক রিলসের নিখুঁত সিনেমাটিক ও ডেভেলপার ব্র্যান্ডেড ভিজ্যুয়াল তৈরি হয়:
  ১. শুরুতে সরাসরি হাই-টেক ভিজ্যুয়াল ও ভয়েস দিয়ে ভিডিও শুরু (কোনো টার্মিনাল ইন্ট্রো নেই)
  ২. পুরো ভিডিও জুড়ে টপ-রাইট কর্নারে স্টাইলিশ কোড ওয়াটারমার্ক: `</> JUBAYER.DEV`
  ৩. ভিডিওর ৩ নম্বর সিনে মাঝখানে মাত্র ১.৫ সেকেন্ডের জন্য দ্রুত পাইথন কোড এডিটর ঝলক
  ৪. ফিউচারিস্টিক রোবোটিক্স, সাই-ফাই হলোগ্রাম ও ৩ডি ব্রেইন স্ক্যান
  ৫. ভিডিওর শেষে ২.৮ সেকেন্ডের সিনেমাটিক ডেভেলপার আউটরো কার্ড:
     ল্যাপটপে কোড করা জুবায়েরের আত্মবিশ্বাসী স্টুডিও ফটো (HUD সাইবার রিং) +
     "ENGINEERED BY JUBAYER.DEV | AI & AUTOMATION LAB"
  ৬. ব্যাকগ্রাউন্ড মিউজিক আউটরো কার্ড শেষ হওয়া পর্যন্ত বাজবে এবং মসৃণভাবে ফেইড হবে
=============================================================================
"""

import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import math
import subprocess
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import BGM_PATH, OUTPUT_DIR, TEMP_DIR

ASSETS_DIR = BASE_DIR / "assets"
TECH_CLIPS_DIR = ASSETS_DIR / "tech_clips"

font_mono_path = "C:/Windows/Fonts/consola.ttf"
font_bold_path = "C:/Windows/Fonts/consolab.ttf"
font_sans_path = "C:/Windows/Fonts/arialbd.ttf"

CURATED_TECH_CLIPS = {
    "sci_fi_hand_gestures.mp4": "https://assets.mixkit.co/videos/51209/51209-720.mp4",
    "humanoid_robot.mp4": "https://assets.mixkit.co/videos/49042/49042-720.mp4",
    "brain_3d_screen.mp4": "https://assets.mixkit.co/videos/5665/5665-720.mp4",
    "hand_projecting_hologram.mp4": "https://assets.mixkit.co/videos/40277/40277-1080.mp4",
    "cyborg_hologram.mp4": "https://assets.mixkit.co/videos/40202/40202-720.mp4",
    "hologram_gestures.mp4": "https://assets.mixkit.co/videos/5427/5427-720.mp4",
    "smartwatch_hologram.mp4": "https://assets.mixkit.co/videos/4364/4364-720.mp4",
    "robot_walking.mp4": "https://assets.mixkit.co/videos/49040/49040-720.mp4"
}


def ensure_tech_clips_available():
    """নিশ্চিত করে যে হাই-টেক ভিডিও ফুটেজ ফোল্ডারে উপস্থিত আছে।"""
    TECH_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    existing = list(TECH_CLIPS_DIR.glob("*.mp4"))
    if len(existing) >= 4:
        return

    headers = {'User-Agent': 'Mozilla/5.0'}
    for fname, url in CURATED_TECH_CLIPS.items():
        out_path = TECH_CLIPS_DIR / fname
        if not out_path.exists():
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = resp.read()
                    with open(out_path, "wb") as f:
                        f.write(data)
            except Exception:
                pass


def create_watermark_badge() -> Path:
    """Creates a sleek, semi-transparent HUD watermark for the top-right corner."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / "watermark_badge.png"
    if out_path.exists():
        return out_path

    bw, bh = 290, 56
    img = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((0, 0, bw, bh), radius=14, fill="#080D1AEE", outline="#00F0FF88", width=2)
    font = ImageFont.truetype(font_bold_path, 24)
    draw.text((18, 14), "</>", fill="#00F0FF", font=font)
    draw.text((70, 14), "JUBAYER.DEV", fill="#F8FAFC", font=font)

    img.save(out_path, format="PNG")
    return out_path


def create_code_ide_image() -> Path:
    """Creates a full 1080x1920 Dark Mode VS Code IDE showing genuine Python automation code."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / "code_ide_screen.png"
    if out_path.exists():
        return out_path

    w, h = 1080, 1920
    img = Image.new("RGBA", (w, h), "#0D1117")
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, w, 60), fill="#161B22")
    draw.text((w//2 - 120, 18), "jubayer-ai-engine — main.py", fill="#8B949E", font=ImageFont.truetype(font_mono_path, 20))

    draw.rectangle((0, 60, w, 110), fill="#1E232B")
    draw.rectangle((60, 60, 310, 110), fill="#0D1117")
    draw.line([(60, 60), (310, 60)], fill="#00F0FF", width=3)
    draw.text((85, 75), "🐍 jubayer_pipeline.py", fill="#F0F6FC", font=ImageFont.truetype(font_mono_path, 20))

    draw.rectangle((315, 60, 530, 110), fill="#161B22")
    draw.text((335, 75), "⚡ neural_core.py", fill="#8B949E", font=ImageFont.truetype(font_mono_path, 20))

    font_code = ImageFont.truetype(font_mono_path, 26)

    code_lines = [
        ("01", "#!/usr/bin/env python3", "#8B949E"),
        ("02", "# -*- coding: utf-8 -*-", "#8B949E"),
        ("03", "# Architecture by Jubayer (AI & Software Developer)", "#00F0FF"),
        ("04", "", "#000"),
        ("05", "import torch", "#FF7B72"),
        ("06", "from neural_robotics import VisionEngine, SpeechModel", "#FFA657"),
        ("07", "from content_core import ScriptPlanner", "#FFA657"),
        ("08", "", "#000"),
        ("09", "class JubayerAIPipeline:", "#79C0FF"),
        ("10", "    def __init__(self, creator='Jubayer'):", "#D2A8FF"),
        ("11", "        self.creator = creator", "#E6EDF3"),
        ("12", "        self.vision = VisionEngine(fps=30, res='1080p')", "#7EE787"),
        ("13", "        self.speech = SpeechModel.load_weights()", "#7EE787"),
        ("14", "", "#000"),
        ("15", "    def generate_automated_reel(self, topic: str):", "#D2A8FF"),
        ("16", "        print(f'[AI] Synthesizing: {topic}')", "#A5D6FF"),
        ("17", "        narration = self.speech.synthesize_anchor()", "#E6EDF3"),
        ("18", "        visuals = self.vision.render_holograms()", "#E6EDF3"),
        ("19", "        return self.vision.compose_reel(narration)", "#7EE787"),
        ("20", "", "#000"),
        ("21", "if __name__ == '__main__':", "#FF7B72"),
        ("22", "    engine = JubayerAIPipeline()", "#E6EDF3"),
        ("23", "    engine.generate_automated_reel('Future_Tech')", "#A5D6FF"),
        ("24", "    print('[SUCCESS] Engineered by Jubayer.dev')", "#7EE787")
    ]

    curr_y = 140
    for num, code, color in code_lines:
        draw.text((25, curr_y), num, fill="#484F58", font=font_code)
        draw.text((95, curr_y), code, fill=color, font=font_code)
        curr_y += 46

    draw.rectangle((0, 1300, w, h), fill="#0A0D14", outline="#30363D", width=2)
    draw.rectangle((0, 1300, w, 1350), fill="#161B22")
    draw.text((30, 1315), "TERMINAL  |  PYTHON INTERPRETER (v3.14) — 200 OK", fill="#58A6FF", font=ImageFont.truetype(font_bold_path, 20))

    term_lines = [
        ("root@jubayer-lab:~$ ", "#3FB950", "python -m jubayer_engine --stream", "#E6EDF3"),
        ("[AI Engine] ", "#D2A8FF", "Neural tensor cores active: 100%", "#8B949E"),
        ("[Hologram] ", "#79C0FF", "3D Gesture tracking pipeline online", "#8B949E"),
        ("[Robotics] ", "#FFA657", "Kinematic humanoid balance synchronized", "#8B949E"),
        ("[Build] ", "#3FB950", "STATUS: 200 OK | Engineered by Jubayer.dev", "#3FB950")
    ]

    ty = 1380
    for p, pc, t, tc in term_lines:
        draw.text((30, ty), p, fill=pc, font=font_code)
        pw = draw.textlength(p, font=font_code)
        draw.text((30 + pw, ty), t, fill=tc, font=font_code)
        ty += 52

    img.save(out_path, format="PNG")
    return out_path


def create_outro_slate_image() -> Path:
    """
    Creates the prestigious 1080x1920 developer end-slate with Jubayer's laptop photo,
    glowing cyan/gold HUD rings, and 'ENGINEERED BY JUBAYER.DEV'.
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / "outro_slate.png"

    # Always generate or update with Jubayer's laptop photo
    w, h = 1080, 1920
    img = Image.new("RGBA", (w, h), "#080B14")
    draw = ImageDraw.Draw(img)

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((w//2 - 450, 250, w//2 + 450, 1150), fill=(0, 240, 255, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    img.paste(glow, (0, 0), glow)

    # Use Jubayer's uploaded laptop developer photo
    p_img_path = ASSETS_DIR / "jubayer_dev_laptop.jpg"
    if not p_img_path.exists():
        p_img_path = ASSETS_DIR / "presenter_poses/pose_closed.jpg"
    if not p_img_path.exists():
        p_img_path = ASSETS_DIR / "presenter.jpg"

    p_img = Image.open(p_img_path).convert("RGBA")
    face_size = 540
    cropped = p_img.resize((face_size, face_size), Image.Resampling.LANCZOS)

    mask = Image.new("L", (face_size, face_size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0, face_size, face_size), fill=255)

    circular = Image.new("RGBA", (face_size, face_size), (0, 0, 0, 0))
    circular.paste(cropped, (0, 0), mask)

    ccx, ccy = w // 2, 600
    r_base = face_size // 2

    # HUD Rings
    for r_offset, alpha in [(14, 40), (10, 80), (6, 150), (2, 220)]:
        r = r_base + 6 + r_offset
        draw.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=(0, 240, 255, alpha), width=3)

    draw.ellipse((ccx - r_base - 6, ccy - r_base - 6, ccx + r_base + 6, ccy + r_base + 6), outline="#00F0FF", width=5)
    draw.ellipse((ccx - r_base - 14, ccy - r_base - 14, ccx + r_base + 14, ccy + r_base + 14), outline="#FFD700", width=2)

    for i in range(36):
        if i % 9 == 0:
            continue
        angle = (2 * math.pi / 36) * i
        r1 = r_base + 8
        r2 = r_base + 18 if i % 3 == 0 else r_base + 14
        x1 = ccx + r1 * math.cos(angle)
        y1 = ccy + r1 * math.sin(angle)
        x2 = ccx + r2 * math.cos(angle)
        y2 = ccy + r2 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill="#38BDF8", width=2)

    img.paste(circular, (ccx - r_base, ccy - r_base), circular)
    draw.ellipse((ccx - r_base, ccy - r_base, ccx + r_base, ccy + r_base), outline=(255, 255, 255, 180), width=2)

    font_sub = ImageFont.truetype(font_mono_path, 28)
    font_hero = ImageFont.truetype(font_sans_path, 62)
    font_lab = ImageFont.truetype(font_mono_path, 32)
    font_cta = ImageFont.truetype(font_bold_path, 30)

    sub_text = "ENGINEERED & PRODUCED BY"
    sw = draw.textlength(sub_text, font=font_sub)
    draw.text((w//2 - sw//2, 940), sub_text, fill="#94A3B8", font=font_sub)

    hero_text = "JUBAYER.DEV"
    hw = draw.textlength(hero_text, font=font_hero)
    draw.text((w//2 - hw//2, 990), hero_text, fill="#00F0FF", font=font_hero)

    lab_text = "AI & AUTOMATION LAB"
    lw = draw.textlength(lab_text, font=font_lab)
    draw.text((w//2 - lw//2, 1075), lab_text, fill="#F8FAFC", font=font_lab)

    badge_y = 1160
    badges = ["SOFTWARE ENGINEER", "AI AUTOMATION", "PYTHON"]
    total_w = sum(draw.textlength(b, font=font_sub) + 40 for b in badges) + 20 * (len(badges) - 1)
    bx = w // 2 - total_w // 2

    for b in badges:
        bw = draw.textlength(b, font=font_sub) + 40
        draw.rounded_rectangle((bx, badge_y, bx + bw, badge_y + 54), radius=12, fill="#0F172A", outline="#38BDF866", width=2)
        draw.text((bx + 20, badge_y + 12), b, fill="#38BDF8", font=font_sub)
        bx += bw + 20

    cta_y = 1320
    cta_w = 480
    draw.rounded_rectangle((w//2 - cta_w//2, cta_y, w//2 + cta_w//2, cta_y + 70), radius=16, fill="#00F0FF")
    cta_text = "FOLLOW FOR FUTURE TECH"
    cw = draw.textlength(cta_text, font=font_cta)
    draw.text((w//2 - cw//2, cta_y + 18), cta_text, fill="#080B14", font=font_cta)

    img.save(out_path, format="PNG")
    return out_path


def render_still_with_zoom(img_path: Path, duration: float, out_path: Path, fps: int = 30):
    """Renders a static image with smooth subtle cinematic camera push-in."""
    vf = (
        f"zoompan=z='min(zoom+0.0004,1.05)':d={int(duration*fps)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},"
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "eq=contrast=1.06:saturation=1.10"
    )
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-vf", vf,
        "-t", f"{duration:.3f}",
        "-r", str(fps),
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_broll_scene_with_watermark(clip_path: Path, duration: float, out_path: Path, fps: int = 30):
    """Renders high-tech robotics footage with top-right </> JUBAYER.DEV watermark."""
    watermark = create_watermark_badge()
    vf = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,"
        "eq=contrast=1.10:saturation=1.12[bg];"
        "[bg][1:v]overlay=1080-w-40:50:shortest=1[v]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(clip_path),
        "-loop", "1", "-i", str(watermark),
        "-filter_complex", vf,
        "-map", "[v]",
        "-t", f"{duration:.3f}",
        "-r", str(fps),
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_split_code_scene(broll_clip: Path, total_dur: float, out_path: Path, fps: int = 30):
    """
    সিন ৩-এ মাঝখানে মাত্র ১.৫ সেকেন্ডের জন্য দ্রুত পাইথন কোড এডিটর ঝলক দেখাবে,
    এরপর বাকি সময়ে হাই-টেক B-roll ফুটেজ চলবে।
    """
    code_img = create_code_ide_image()
    part_code = TEMP_DIR / "split_code_1_5s.mp4"
    part_broll = TEMP_DIR / "split_broll_rest.mp4"

    code_dur = 1.5
    broll_dur = max(1.0, total_dur - code_dur)

    # ১.৫ সে. কোড
    render_still_with_zoom(code_img, code_dur, part_code, fps=fps)
    # বাকি সময়ে রোবোটিক্স ফুটেজ + ওয়াটারমার্ক
    render_broll_scene_with_watermark(broll_clip, broll_dur, part_broll, fps=fps)

    concat_txt = TEMP_DIR / "concat_split_code.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        f.write(f"file '{part_code.resolve().as_posix()}'\n")
        f.write(f"file '{part_broll.resolve().as_posix()}'\n")

    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(out_path)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_scene_clip(scene_idx: int, scene_text: str = "", used_clips: list = None) -> Path:
    """স্ক্রিপ্টের বিষয়বস্তু অনুযায়ী প্রতিটি সিনের জন্য সম্পূর্ণ ভিন্ন ভিন্ন ফুটেজ নির্বাচন করে।"""
    ensure_tech_clips_available()
    if used_clips is None:
        used_clips = []

    priority_order = [
        "sci_fi_hand_gestures.mp4",
        "humanoid_robot.mp4",
        "brain_3d_screen.mp4",
        "hand_projecting_hologram.mp4",
        "cyborg_hologram.mp4",
        "robot_walking.mp4",
        "smartwatch_hologram.mp4",
        "hologram_gestures.mp4"
    ]

    text_lower = scene_text.lower()
    candidate = None

    if any(k in text_lower for k in ["রোবট", "যন্ত্র", "সহকারী", "হিউম্যানয়েড"]):
        for c in ["humanoid_robot.mp4", "robot_walking.mp4"]:
            if c not in used_clips and (TECH_CLIPS_DIR / c).exists():
                candidate = c
                break
    elif any(k in text_lower for k in ["ব্রেইন", "মস্তিষ্ক", "চিন্তা", "নিউরাল"]):
        if "brain_3d_screen.mp4" not in used_clips and (TECH_CLIPS_DIR / "brain_3d_screen.mp4").exists():
            candidate = "brain_3d_screen.mp4"
    elif any(k in text_lower for k in ["হাত", "ঘোরা", "স্পর্শ", "ইন্টারফেস", "স্ক্রিন", "হলোগ্রাম"]):
        for c in ["sci_fi_hand_gestures.mp4", "hand_projecting_hologram.mp4", "hologram_gestures.mp4"]:
            if c not in used_clips and (TECH_CLIPS_DIR / c).exists():
                candidate = c
                break

    if not candidate:
        for c in priority_order:
            if c not in used_clips and (TECH_CLIPS_DIR / c).exists():
                candidate = c
                break

    if not candidate:
        candidate = priority_order[(scene_idx - 1) % len(priority_order)]

    return TECH_CLIPS_DIR / candidate


def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    """
    ১০০% সিনেমাটিক, রোবোটিক্স ও জুবায়েরের ডেভেলপার ব্র্যান্ডেড রিলস ভিডিও রেন্ডার করে।
      - শুরুতে সরাসরি মূল ভিডিও ও ভয়েসওভার (কোনো টার্মিনাল ইন্ট্রো নেই)
      - টপ কর্নারে </> JUBAYER.DEV ওয়াটারমার্ক
      - সিন ৩-এর মাঝে মাত্র ১.৫ সেকেন্ড কোড ফ্ল্যাশ
      - ভিডিওর শেষে নিশ্চিতভাবে ২.৮ সেকেন্ডের সিনেমাটিক আউটরো কার্ড (জুবায়েরের ল্যাপটপ ফটো ও HUD)
    """
    print("[VideoEngine] JUBAYER.DEV সিনেমাটিক ডেভেলপার রিলস তৈরি হচ্ছে...")
    ensure_tech_clips_available()
    rendered_parts = []
    used_clips = []

    # ১. মূল ৫টি রোবোটিক্স ও কোডিং সিন (শুরুতেই সরাসরি সিন ১ দিয়ে স্টার্ট)
    total_scenes_dur = 0.0
    for i, sc in enumerate(scene_timings, start=1):
        dur = sc.get("duration", sc.get("end", 0) - sc.get("start", 0))
        if dur <= 0:
            dur = 5.0
        total_scenes_dur += dur
        text = sc.get("text", "")
        part_out = TEMP_DIR / f"final_part_{i}_scene.mp4"

        clip = get_scene_clip(i, text, used_clips)
        used_clips.append(clip.name)

        if i == 3:
            # সিন ৩-এ মাত্র ১.৫ সেকেন্ড কোড ঝলক + বাকিটা রোবোটিক্স ফুটেজ
            print(f"[VideoEngine] সিন {i}: ১.৫ সেকেন্ড কোড ঝলক + রোবোটিক্স ফুটেজ ({clip.name}) রেন্ডারিং...")
            render_split_code_scene(clip, dur, part_out)
        else:
            print(f"[VideoEngine] সিন {i}: সাই-ফাই রোবোটিক্স ফুটেজ ({clip.name}) + ওয়াটারমার্ক রেন্ডারিং...")
            render_broll_scene_with_watermark(clip, dur, part_out)

        rendered_parts.append(part_out)

    # ২. সিনেমাটিক আউটরো কার্ড (২.৮ সেকেন্ড - ১০০% দৃশ্যমান)
    outro_img = create_outro_slate_image()
    outro_vid = TEMP_DIR / "final_outro_slate.mp4"
    outro_dur = 2.8
    print("[VideoEngine] সিনেমাটিক ডেভেলপার আউটরো কার্ড (জুবায়েরের ল্যাপটপ পোর্ট্রেট) রেন্ডারিং...")
    render_still_with_zoom(outro_img, outro_dur, outro_vid)
    rendered_parts.append(outro_vid)

    # ভিডিও ক্লিপগুলো কনক্যাট করা
    concat_list = TEMP_DIR / "final_developer_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in rendered_parts:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    bg_video_path = TEMP_DIR / "developer_full_bg.mp4"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(bg_video_path)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # মোট ভিডিও দৈর্ঘ্য (সিনসমূহ + আউটরো কার্ড)
    total_video_dur = total_scenes_dur + outro_dur
    mixed_audio_path = TEMP_DIR / "final_mixed_audio.mp3"

    # অডিও মিক্সিং:
    # ভয়েস শুরু হবে ঠিক ০.০ সেকেন্ডে।
    # ভয়েস শেষ হওয়ার পর আউটরো কার্ডের শেষ পর্যন্ত ব্যাকগ্রাউন্ড মিউজিক বাজবে এবং শেষ ০.৮ সেকেন্ডে ফেইড আউট হবে।
    fade_start = max(1.0, total_video_dur - 0.8)
    if BGM_PATH.exists():
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", str(narration_path),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex",
            f"[0:a]volume=1.0[narr];[1:a]volume=0.12,afade=t=out:st={fade_start:.2f}:d=0.8[bgm];[narr][bgm]amix=inputs=2:duration=longest:dropout_transition=2",
            "-t", f"{total_video_dur:.3f}",
            str(mixed_audio_path)
        ]
        subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        mixed_audio_path = narration_path

    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    if not safe_title:
        safe_title = "jubayer_dev_ai_reel"
    output_path = OUTPUT_DIR / f"{safe_title}.mp4"

    # আউটরো কার্ড যাতে কখনো কাটা না পড়ে, তাই -t দিয়ে সম্পূর্ণ ভিডিও দৈর্ঘ্য নিশ্চিত করা হয়েছে
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(bg_video_path),
        "-i", str(mixed_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{total_video_dur:.3f}",
        str(output_path)
    ]

    print("[VideoEngine] JUBAYER.DEV ১০০% মাস্টার্ড ভিডিও এক্সপোর্ট হচ্ছে...")
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[VideoEngine] রেন্ডার সম্পন্ন! ভিডিও সংরক্ষিত: {output_path}")
    return output_path


# Compatibility aliases
def prepare_circular_presenter_badge() -> Path:
    return None

def generate_dynamic_tech_bg(duration: float, output_path: Path):
    clip = TECH_CLIPS_DIR / "sci_fi_hand_gestures.mp4"
    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(clip), "-t", str(duration), "-c", "copy", str(output_path)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    print("=" * 60)
    print("🎬 [JUBAYER.DEV] সিনেমাটিক ডেভেলপার এডিশন টেস্ট")
    print("=" * 60)

    from content_writing.script_writer import get_reel_content
    from voice_audio.voice_engine import generate_voiceover_and_subtitles

    reel = get_reel_content()
    print(f"📌 টপিক: {reel['title']}")
    print("\n[১/২] টিভি নিউজ ভয়েসওভার তৈরি হচ্ছে...")
    audio_data = generate_voiceover_and_subtitles(reel["scenes"])

    print("\n[২/২] সিনেমাটিক ডেভেলপার রিলস ভিডিও রেন্ডারিং হচ্ছে...")
    test_video = render_final_reel(
        scene_timings=audio_data["scene_timings"],
        narration_path=audio_data["narration_path"],
        total_duration=audio_data["total_duration"],
        title="jubayer_dev_final_test"
    )

    print("=" * 60)
    print("✅ JUBAYER.DEV সিনেমাটিক রিলস তৈরি সম্পন্ন!")
    print(f"📂 ভিডিও ফাইল: {test_video}")
    print(f"📏 ফাইল সাইজ: {test_video.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 60)
