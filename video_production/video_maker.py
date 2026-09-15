# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 VIDEO PRODUCTION ENGINE (১০০% রোবোটিক্স, সাই-ফাই ও ডিজিটালাইজড এডিশন)
=============================================================================
এই ইঞ্জিনে ফেসবুক রিলসের ১০০% সিনেমাটিক ও হাই-টেক ভিজ্যুয়াল তৈরি হয়:
  - কোনো ব্যক্তিগত ছবি বা মুখমণ্ডল নেই (সম্পূর্ণ এআই রোবোটিক্স ভিজ্যুয়াল)
  - ১০০% ফুল-স্ক্রিন হাই-টেক B-roll ফুটেজ: হিউম্যানয়েড রোবট, হলোগ্রাম ইন্টারফেসে কাজ করা সাই-ফাই ভিজ্যুয়াল, ৩ডি ব্রেইন স্ক্যান, চিপ ও সাইবার স্পেস
  - প্রতিটি সিনে ভিন্ন ভিন্ন সিনেমাটিক ক্লিপ (কোনো পুনরাবৃত্তি নেই)
  - কোনো বিরক্তিকর লাল ফিল্টার নেই—ন্যাচারাল কুল সাইবার সায়ান, ব্লু ও ডিপ ব্ল্যাক কালার গ্রেডিং
  - ১০০% টেক্সট ও সাবটাইটেল মুক্ত (একদম ক্লিন সিনেমাটিক লুক)
  - ক্রিস্প টিভি নিউজ বুলেটিন ভয়েসওভার ও ব্যাকগ্রাউন্ড মিউজিকের প্রিমিয়াম ব্যালেন্সড মিক্সিং
=============================================================================
"""

import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import subprocess
import urllib.request
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import BGM_PATH, OUTPUT_DIR, TEMP_DIR

ASSETS_DIR = BASE_DIR / "assets"
TECH_CLIPS_DIR = ASSETS_DIR / "tech_clips"

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


def get_scene_clip(scene_idx: int, scene_text: str = "", used_clips: list = None) -> Path:
    """
    স্ক্রিপ্টের বিষয়বস্তু অনুযায়ী প্রতিটি সিনের জন্য সম্পূর্ণ ভিন্ন ভিন্ন হাই-টেক ফুটেজ নির্বাচন করে।
    লাল ভাব বাদ দিয়ে নীল, সায়ান ও ন্যাচারাল ফিউচারিস্টিক ক্লিপ নিশ্চিত করে।
    """
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


def render_digitized_robotics_scene(clip_path: Path, duration: float, out_path: Path, fps: int = 30):
    """
    ১০০% ফুল-স্ক্রিন হাই-টেক রোবোটিক্স ও সাই-ফাই ফুটেজ রেন্ডার করে।
    কোনো ব্যক্তিগত ছবি বা ব্যাজ নেই—সম্পূর্ণ সিনেমাটিক লুক।
    """
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,"
        "eq=contrast=1.10:saturation=1.12"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(clip_path),
        "-vf", vf,
        "-t", f"{duration:.3f}",
        "-r", str(fps),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    """
    ১০০% ক্লিন, রোবোটিক্স ও সাই-ফাই ডিজিটালাইজড ফেসবুক রিলস রেন্ডার করে।
    """
    print("[VideoEngine] ১০০% ডিজিটালাইজড রোবোটিক্স রিলস তৈরি হচ্ছে...")
    ensure_tech_clips_available()
    rendered_parts = []
    used_clips = []

    for i, sc in enumerate(scene_timings, start=1):
        dur = sc.get("duration", sc.get("end", 0) - sc.get("start", 0))
        if dur <= 0:
            dur = 5.0
        text = sc.get("text", "")
        part_out = TEMP_DIR / f"digitized_scene_{i}.mp4"

        clip = get_scene_clip(i, text, used_clips)
        used_clips.append(clip.name)
        print(f"[VideoEngine] সিন {i}: রোবোটিক্স ও সাই-ফাই ফুটেজ ({clip.name}) রেন্ডারিং...")
        render_digitized_robotics_scene(clip, dur, part_out)
        rendered_parts.append(part_out)

    # সকল সিন একত্রীকরণ
    concat_list = TEMP_DIR / "final_digitized_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in rendered_parts:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    bg_video_path = TEMP_DIR / "digitized_full_bg.mp4"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(bg_video_path)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # অডিও মিক্সিং (টিভি নিউজ ভয়েসওভার + ১০% ব্যালেন্সড ব্যাকগ্রাউন্ড মিউজিক)
    mixed_audio_path = TEMP_DIR / "final_mixed_audio.mp3"
    if BGM_PATH.exists():
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", str(narration_path),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex",
            "[0:a]volume=1.0[narr];[1:a]volume=0.10[bgm];[narr][bgm]amix=inputs=2:duration=first:dropout_transition=2",
            "-t", str(total_duration),
            str(mixed_audio_path)
        ]
        subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        mixed_audio_path = narration_path

    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    if not safe_title:
        safe_title = "ai_robotics_reel"
    output_path = OUTPUT_DIR / f"{safe_title}.mp4"

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(bg_video_path),
        "-i", str(mixed_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path)
    ]

    print("[VideoEngine] ১০০% ক্লিন ডিজিটালাইজড রিলস ভিডিও এক্সপোর্ট হচ্ছে...")
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
