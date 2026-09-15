# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 2. VIDEO PRODUCTION ENGINE (ভিডিও তৈরি ও এডিটিং) - ২০২৬/২০৩০ সাইবার রেড এডিশন
=============================================================================
এই ফাইলে ফেসবুক রিলসের সম্পূর্ণ হাই-টেক ভিডিও রেন্ডারিংয়ের কাজ সম্পন্ন হয়:
  - মাল্টি-সিন ডাইনামিক B-roll ফুটেজ (রোবোটিক্স, হাতের উপর ৩ডি হলোগ্রাম, লাল মাইক্রোচিপ, ব্রেইন স্ক্যান, লেজার টানেল)
  - একদম ঝাকানাকা সাইবার রেড ও নিয়ন ক্রিস্টাল কালার গ্রেডিং
  - সম্পূর্ণ টেক্সট-মুক্ত (ভিডিওতে কোনো সাবটাইটেল বা ক্যাপশন থাকবে না)
  - জুবায়েরের নিয়ন রেড ও গোল্ড HUD রিং যুক্ত প্রেজেন্টার ব্যাজ
  - টিভি নিউজ বুলেটিন ভয়েসওভার এবং ব্যাকগ্রাউন্ড মিস্ট্রি মিউজিকের নিখুঁত সাউন্ড মিক্সিং

টেস্ট করার জন্য টার্মিনালে চালান:
    python video_production/video_maker.py
=============================================================================
"""

import os
import sys
import math
import subprocess
import urllib.request
from pathlib import Path

# Ensure project root is in sys.path for standalone runs
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PIL import Image, ImageDraw
from src.config import BGM_PATH, OUTPUT_DIR, TEMP_DIR

ASSETS_DIR = BASE_DIR / "assets"
TECH_CLIPS_DIR = ASSETS_DIR / "tech_clips"
PRESENTER_IMG_PATH = ASSETS_DIR / "presenter.jpg"

# Curated high-tech royalty-free clips repository
CURATED_TECH_CLIPS = {
    "red_laser_tunnel.mp4": "https://assets.mixkit.co/videos/35644/35644-720.mp4",
    "sci_fi_hand_gestures.mp4": "https://assets.mixkit.co/videos/51209/51209-720.mp4",
    "red_circuit_board.mp4": "https://assets.mixkit.co/videos/11821/11821-720.mp4",
    "brain_3d_screen.mp4": "https://assets.mixkit.co/videos/5665/5665-720.mp4",
    "red_mesh_3d.mp4": "https://assets.mixkit.co/videos/34302/34302-720.mp4",
    "hologram_gestures.mp4": "https://assets.mixkit.co/videos/5427/5427-720.mp4",
    "humanoid_robot.mp4": "https://assets.mixkit.co/videos/49042/49042-720.mp4",
    "cyber_laser_glasses.mp4": "https://assets.mixkit.co/videos/50460/50460-720.mp4",
    "hand_projecting_hologram.mp4": "https://assets.mixkit.co/videos/40277/40277-1080.mp4",
    "cyborg_hologram.mp4": "https://assets.mixkit.co/videos/40202/40202-720.mp4"
}


def ensure_tech_clips_available():
    """
    নিশ্চিত করে যে হাই-টেক ভিডিও ফুটেজ ফোল্ডারে উপস্থিত আছে।
    না থাকলে স্বয়ংক্রিয়ভাবে ব্যাকগ্রাউন্ডে ডাউনলোড করে নেয় (জিরো হ্যাসেল)।
    """
    TECH_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    existing = list(TECH_CLIPS_DIR.glob("*.mp4"))
    if len(existing) >= 4:
        return

    print("[VideoEngine] প্রয়োজনীয় হাই-টেক ভিডিও ফুটেজ ব্যাকগ্রাউন্ডে রেডি করা হচ্ছে...")
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
                print(f"[VideoEngine] ফুটেজ সংরক্ষিত: {fname}")
            except Exception as e:
                print(f"[VideoEngine] ফুটেজ ডাউনলোড স্কিপ: {fname} ({e})")


def prepare_circular_presenter_badge() -> Path:
    """
    জুবায়েরের প্রতিকৃতির চারপাশে ২০২৬/২০৩০ সাইবার রেড ও গোল্ড HUD রিং তৈরি করে।
    কোনো টেক্সট বা নেমট্যাগ থাকবে না (১০০% ক্লিন ও পিওর ভিজ্যুয়াল)।
    """
    badge_path = TEMP_DIR / "presenter_badge_cyber_red.png"
    if badge_path.exists():
        return badge_path

    if not PRESENTER_IMG_PATH.exists():
        img = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
        img.save(badge_path)
        return badge_path

    # ক্রপ ও রিসাইজ
    user_img = Image.open(PRESENTER_IMG_PATH).convert("RGBA")
    w, h = user_img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = 30
    cropped = user_img.crop((left, top, left + min_dim, top + min_dim)).resize((300, 300), Image.Resampling.LANCZOS)

    mask = Image.new("L", (300, 300), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 300, 300), fill=255)

    circular_avatar = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    circular_avatar.paste(cropped, (0, 0), mask)

    canvas = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 180, 180

    # ১. আউটার নিয়ন ক্রিস্টাল রেড গ্লো
    for r_offset, alpha in [(8, 40), (6, 80), (4, 140), (2, 200)]:
        r = 168 + r_offset
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 23, 68, alpha), width=2)

    # ২. মেইন সাইবার রেড বর্ডার
    draw.ellipse((cx - 165, cy - 165, cx + 165, cy + 165), outline="#FF1744", width=4)

    # ৩. গোল্ডেন HUD অ্যাকসেন্ট রিং
    draw.ellipse((cx - 156, cy - 156, cx + 156, cy + 156), outline="#FFD700", width=2)

    # ৪. সায়েন্স ফিকশন HUD টিক মার্কস
    num_ticks = 24
    for i in range(num_ticks):
        angle = (2 * math.pi / num_ticks) * i
        if i % 6 == 0:
            continue
        r1 = 166
        r2 = 173 if i % 2 == 0 else 170
        x1 = cx + r1 * math.cos(angle)
        y1 = cy + r1 * math.sin(angle)
        x2 = cx + r2 * math.cos(angle)
        y2 = cy + r2 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill="#FF5252", width=2)

    # ৫. পোর্ট্রেট পেস্ট করা
    canvas.paste(circular_avatar, (30, 30), circular_avatar)
    draw.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), outline=(255, 255, 255, 180), width=2)

    canvas.save(badge_path, format="PNG")
    return badge_path


def get_scene_clip(scene_idx: int, scene_text: str = "", prev_clip_name: str = "") -> Path:
    """
    স্ক্রিপ্টের বিষয়বস্তু অনুযায়ী নিখুঁত রোবোটিক্স, হলোগ্রাম বা সাইবার রেড ফুটেজ নির্বাচন করে।
    """
    ensure_tech_clips_available()
    text_lower = scene_text.lower()

    if any(k in text_lower for k in ["চিপ", "মাইক্রোচিপ", "সার্কিট", "কম্পিউটার", "হার্ডওয়্যার"]):
        target = "red_circuit_board.mp4"
    elif any(k in text_lower for k in ["ব্রেইন", "মস্তিষ্ক", "চিন্তা", "নিউরাল", "ভাবনা"]):
        target = "brain_3d_screen.mp4"
    elif any(k in text_lower for k in ["হাত", "ঘোরা", "স্পর্শ", "ইন্টারফেস", "স্ক্রিন", "হলোগ্রাম"]):
        target = "sci_fi_hand_gestures.mp4"
    elif any(k in text_lower for k in ["রোবট", "যন্ত্র", "সহকারী", "রোবটিক্স", "হিউম্যানয়েড"]):
        target = "humanoid_robot.mp4"
    else:
        # ডায়নামিক সাইবার রেড সিকোয়েন্স
        sequence = [
            "red_laser_tunnel.mp4",
            "sci_fi_hand_gestures.mp4",
            "red_circuit_board.mp4",
            "brain_3d_screen.mp4",
            "red_mesh_3d.mp4"
        ]
        target = sequence[(scene_idx - 1) % len(sequence)]

    # আগের সিনের সাথে হুবহু এক যেন না হয়
    if target == prev_clip_name:
        alternatives = ["red_mesh_3d.mp4", "hologram_gestures.mp4", "cyber_laser_glasses.mp4", "red_laser_tunnel.mp4"]
        for alt in alternatives:
            if alt != prev_clip_name and (TECH_CLIPS_DIR / alt).exists():
                target = alt
                break

    clip_path = TECH_CLIPS_DIR / target
    if clip_path.exists():
        return clip_path

    # ফলব্যাক
    all_clips = list(TECH_CLIPS_DIR.glob("*.mp4"))
    if all_clips:
        return all_clips[0]
    return BASE_DIR / "assets" / "tech_clip_1.mp4"


def generate_dynamic_tech_montage(scene_timings: list, total_duration: float, output_path: Path):
    """
    প্রতিটি সিনের জন্য আলাদা আলাদা আধুনিক সাইবার রেড ও হলোগ্রাফিক ভিডিও জুড়ে একটি পূর্ণাঙ্গ মন্টেজ তৈরি করে।
    ১০৮০x১৯২০ (৯:১৬) রেশিও ও হাই-কনট্রাস্ট সাইবার রেড কালার গ্রেডিং প্রয়োগ করা হয়।
    """
    concat_list_file = TEMP_DIR / "montage_concat_list.txt"
    rendered_parts = []
    prev_clip = ""

    # কালার গ্রেড ফিল্টার: ১০৮০x১৯২০ ক্রপ + উচ্চ কনট্রাস্ট + নিয়ন লাল রঙের উজ্জ্বলতা
    vf_template = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,"
        "eq=contrast=1.18:saturation=1.25:brightness=-0.02"
    )

    for i, sc in enumerate(scene_timings, start=1):
        dur = sc.get("duration", sc.get("end", 0) - sc.get("start", 0))
        if dur <= 0:
            dur = 5.0
        text = sc.get("text", "")
        clip_file = get_scene_clip(i, text, prev_clip)
        prev_clip = clip_file.name

        part_out = TEMP_DIR / f"montage_scene_{i}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", str(clip_file),
            "-vf", vf_template,
            "-t", f"{dur:.3f}",
            "-r", "30",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-an",
            str(part_out)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rendered_parts.append(part_out)

    with open(concat_list_file, "w", encoding="utf-8") as f:
        for p in rendered_parts:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(output_path)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    """
    ১০০% সাবটাইটেল-মুক্ত, ঝাকানাকা সাইবার রেড এআই রিলস ভিডিও রেন্ডার করে।
    """
    print("[VideoEngine] আধুনিক সাইবার রেড ও হলোগ্রাফিক ভিডিও মন্টেজ তৈরি হচ্ছে...")
    bg_video_path = TEMP_DIR / "cyber_red_montage_bg.mp4"
    generate_dynamic_tech_montage(scene_timings, total_duration, bg_video_path)

    # ২. প্রেজেন্টার ব্যাজ (নিয়ন সাইবার রেড HUD রিং, কোনো টেক্সট নেই)
    badge_path = prepare_circular_presenter_badge()

    # ৩. অডিও মিক্সিং (টিভি নিউজ ভয়েসওভার + ১০% ব্যাকগ্রাউন্ড মিউজিক)
    mixed_audio_path = TEMP_DIR / "final_mixed_audio.mp3"
    if BGM_PATH.exists():
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", str(narration_path),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex",
            f"[0:a]volume=1.0[narr];[1:a]volume=0.10[bgm];[narr][bgm]amix=inputs=2:duration=first:dropout_transition=2",
            "-t", str(total_duration),
            str(mixed_audio_path)
        ]
        subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        mixed_audio_path = narration_path

    # ৪. ফাইনাল কম্পোজিশন: ব্যাকগ্রাউন্ড ভিডিও + কর্নারে প্রেজেন্টার ব্যাজ + অডিও
    # (কোনো drawtext বা সাবটাইটেল নেই — ১০০% ক্লিন ও সিনেমাটিক!)
    filter_complex = "[0:v][1:v]overlay=680:1500:shortest=1[v_out]"

    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    if not safe_title:
        safe_title = "ai_tech_reel"
    output_path = OUTPUT_DIR / f"{safe_title}.mp4"

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(bg_video_path),
        "-loop", "1", "-i", str(badge_path),
        "-i", str(mixed_audio_path),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "2:a",
        "-t", str(total_duration),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]

    print("[VideoEngine] ১০০% ক্লিন সিনেমাটিক রিলস ভিডিও রেন্ডারিং হচ্ছে...")
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[VideoEngine] রেন্ডার সম্পন্ন! ভিডিও সংরক্ষিত: {output_path}")
    return output_path


# Compatibility alias for external callers
def generate_dynamic_tech_bg(duration: float, output_path: Path):
    """Legacy compatibility helper."""
    dummy_timings = [{"duration": duration, "text": "Future tech robotics"}]
    generate_dynamic_tech_montage(dummy_timings, duration, output_path)


# =============================================================================
# স্বতন্ত্র টেস্ট কোড (টার্মিনালে সরাসরি চালিয়ে চেক করার জন্য)
# =============================================================================
if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 60)
    print("🎬 [VIDEO MAKER TEST] ২০২৬/২০৩০ সাইবার রেড রিলস ভিডিও টেস্ট")
    print("=" * 60)

    from content_writing.script_writer import get_reel_content
    from src.audio_engine import generate_voiceover_and_subtitles

    reel = get_reel_content()
    print(f"📌 টপিক: {reel['title']}")
    print("\n[১/২] টিভি নিউজ ভয়েসওভার তৈরি হচ্ছে...")
    audio_data = generate_voiceover_and_subtitles(reel["scenes"])

    print("\n[২/২] সাইবার রেড মাল্টি-সিন রিলস ভিডিও রেন্ডারিং হচ্ছে...")
    test_video = render_final_reel(
        scene_timings=audio_data["scene_timings"],
        narration_path=audio_data["narration_path"],
        total_duration=audio_data["total_duration"],
        title="cyber_red_reel_sample"
    )

    print("=" * 60)
    print(f"✅ ঝাকানাকা সাইবার রেড রিলস ভিডিও তৈরি সম্পন্ন!")
    print(f"📂 ভিডিও ফাইল: {test_video}")
    print(f"📏 ফাইল সাইজ: {test_video.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 60)
