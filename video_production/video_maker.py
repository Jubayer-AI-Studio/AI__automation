# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 VIDEO PRODUCTION ENGINE (ডিগনিফাইড সিনেমাটিক প্রেজেন্টার ও হাই-টেক এডিশন)
=============================================================================
এই ইঞ্জিনে ফেসবুক রিলসের ১০০% প্রফেশনাল ও মর্যাদাপূর্ণ ভিডিও তৈরি হয়:
  - A-Roll: জুবায়েরের ফুল স্ক্রিন সিনেমাটিক স্টুডিও প্রেজেন্টার (মাইক ও মনিটরের সামনে মাল্টি-অ্যাঙ্গেল কাট ও মসৃণ ক্যামেরা পুশ-ইন)
  - B-Roll: রোবোটিক্স, সাই-ফাই হলোগ্রাম ও ফিউচারিস্টিক হাই-টেক ভিডিও ফুটেজ
  - কর্নার HUD ব্যাজ: B-Roll চলাকালীন নিচে ডান কোনায় সাইবার সায়ান ও গোল্ডেন HUD রিং সহ জুবায়েরের মর্যাদাপূর্ণ অবতার ব্যাজ
  - কোনো কার্টুনিশ বা দৃষ্টিকটূ মুখ খোলার পুতুল-নাচ (Puppet Flapping) নেই
  - কোনো বিরক্তিকর লাল ফিল্টার নেই—ন্যাচারাল স্কিন টোন ও সাইবার কুল ব্লু/সায়ান লাইটিং
  - ১০০% সাবটাইটেল ও টেক্সট মুক্ত (একদম ক্লিন সিনেমাটিক লুক)
  - ব্যালেন্সড টিভি নিউজ ভয়েসওভার ও ব্যাকগ্রাউন্ড মিউজিক মিক্সিং
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

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PIL import Image, ImageDraw
from src.config import BGM_PATH, OUTPUT_DIR, TEMP_DIR

ASSETS_DIR = BASE_DIR / "assets"
TECH_CLIPS_DIR = ASSETS_DIR / "tech_clips"
POSES_DIR = ASSETS_DIR / "presenter_poses"
PRESENTER_IMG_PATH = ASSETS_DIR / "presenter.jpg"

# ফিউচারিস্টিক রয়্যালটি-ফ্রি হাই-টেক ক্লিপের ভান্ডার (নীল, সায়ান ও ন্যাচারাল কুল কালার)
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


def create_dignified_corner_badge() -> Path:
    """
    জুবায়েরের জন্য একটি আল্ট্রা-প্রিমিয়াম সাইবার সায়ান ও গোল্ড HUD রিং যুক্ত গোল অবতার ব্যাজ তৈরি করে।
    এটি B-roll দৃশ্যে স্ক্রিনের কোনায় মার্জিতভাবে অবস্থান করে। কোনো পুতুল মার্কা মুখ নড়াচড়া নেই।
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    badge_path = TEMP_DIR / "dignified_presenter_badge.png"
    if badge_path.exists():
        return badge_path

    # পোজ বা মূল ছবি নির্বাচন
    img_path = POSES_DIR / "pose_talk_mid.jpg"
    if not img_path.exists():
        img_path = PRESENTER_IMG_PATH

    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    face_size = int(h * 0.38)
    cx = w // 2
    cy = int(h * 0.38)
    cropped = img.crop((cx - face_size//2, cy - face_size//2, cx + face_size//2, cy + face_size//2)).resize((300, 300), Image.Resampling.LANCZOS)

    mask = Image.new("L", (300, 300), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 300, 300), fill=255)

    circular = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    circular.paste(cropped, (0, 0), mask)

    # ৩৬০x৩৬০ ক্যানভাসে প্রিমিয়াম সাইবার সায়ান ও গোল্ডেন HUD রিং
    canvas = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    ccx, ccy = 180, 180

    # আউটার গ্লো
    for r_offset, alpha in [(8, 40), (6, 80), (4, 140), (2, 200)]:
        r = 168 + r_offset
        draw.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=(0, 240, 255, alpha), width=2)

    draw.ellipse((ccx - 165, ccy - 165, ccx + 165, ccy + 165), outline="#00F0FF", width=4)
    draw.ellipse((ccx - 156, ccy - 156, ccx + 156, ccy + 156), outline="#FFD700", width=2)

    # সাই-ফাই টিক্স ও মেজারমেন্ট মার্কস
    for i in range(24):
        if i % 6 == 0:
            continue
        angle = (2 * math.pi / 24) * i
        r1 = 166
        r2 = 173 if i % 2 == 0 else 170
        x1 = ccx + r1 * math.cos(angle)
        y1 = ccy + r1 * math.sin(angle)
        x2 = ccx + r2 * math.cos(angle)
        y2 = ccy + r2 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill="#38BDF8", width=2)

    canvas.paste(circular, (30, 30), circular)
    draw.ellipse((ccx - 150, ccy - 150, ccx + 150, ccy + 150), outline=(255, 255, 255, 180), width=2)
    canvas.save(badge_path, format="PNG")
    return badge_path


def render_cinematic_aroll(duration: float, out_path: Path, scene_num: int = 1, fps: int = 30):
    """
    ফুল স্ক্রিন সিনেমাটিক স্টুডিও প্রেজেন্টার শট:
      - জুবায়ের মাইকের সামনে কথা বলছেন, পেছনে কোডিং মনিটর ও স্টুডিও লাইট
      - মসৃণ ক্যামেরা পুশ-ইন (Ken Burns Effect)
      - বাক্য বা ক্লজের সাথে সামঞ্জস্যপূর্ণ মাল্টি-অ্যাঙ্গেল কাট (Angle 1: প্রেজেন্টার কথা বলছেন -> Angle 2: হাতের এক্সপ্রেসিভ অঙ্গভঙ্গি)
      - কোনো মেকানিক্যাল কার্টুন মুখ-নাড়াচাড়া নেই; শতভাগ মার্জিত ও মর্যাদাপূর্ণ লুক
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    pose1 = POSES_DIR / "pose_talk_mid.jpg"
    pose2 = POSES_DIR / "pose_talk_open.jpg"
    if not pose1.exists():
        pose1 = PRESENTER_IMG_PATH
    if not pose2.exists():
        pose2 = pose1

    # দৃশ্য ৩.৫ সেকেন্ডের বেশি হলে ২-ক্যামেরা স্টুডিও কাটিং
    if duration >= 3.5:
        dur_a = round(duration * 0.52, 3)
        dur_b = round(duration - dur_a, 3)

        # শট ১: মিডিয়াম শট - মসৃণ পুশ-ইন
        part_a = TEMP_DIR / f"aroll_{scene_num}_a.mp4"
        vf_a = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,setsar=1,"
            f"zoompan=z='min(zoom+0.0004,1.06)':d={int(dur_a*fps)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},"
            "eq=contrast=1.06:saturation=1.10"
        )
        cmd_a = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(pose1),
            "-vf", vf_a,
            "-t", f"{dur_a:.3f}",
            "-r", str(fps),
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
            str(part_a)
        ]
        subprocess.run(cmd_a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # শট ২: ক্লোজার এক্সপ্রেসিভ অ্যাঙ্গেল (কথা বলার পঞ্চলাইন শট)
        part_b = TEMP_DIR / f"aroll_{scene_num}_b.mp4"
        vf_b = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,setsar=1,"
            f"zoompan=z='min(zoom+0.0005,1.08)':d={int(dur_b*fps)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},"
            "eq=contrast=1.06:saturation=1.10"
        )
        cmd_b = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(pose2),
            "-vf", vf_b,
            "-t", f"{dur_b:.3f}",
            "-r", str(fps),
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
            str(part_b)
        ]
        subprocess.run(cmd_b, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # শট দুটি কনক্যাট করা
        concat_txt = TEMP_DIR / f"concat_aroll_{scene_num}.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            f.write(f"file '{part_a.resolve().as_posix()}'\n")
            f.write(f"file '{part_b.resolve().as_posix()}'\n")

        cmd_cat = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            str(out_path)
        ]
        subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # সিঙ্গেল ড্রামাটিক শট
        vf = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,setsar=1,"
            f"zoompan=z='min(zoom+0.0004,1.06)':d={int(duration*fps)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},"
            "eq=contrast=1.06:saturation=1.10"
        )
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(pose1),
            "-vf", vf,
            "-t", f"{duration:.3f}",
            "-r", str(fps),
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
            str(out_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_cinematic_broll(clip_path: Path, duration: float, out_path: Path, fps: int = 30):
    """
    হাই-টেক B-roll ফুটেজ রেন্ডার করে এবং নিচে ডান কোনায় জুবায়েরের গোল্ড-সায়ান HUD প্রেজেন্টার ব্যাজ বসায়।
    ন্যাচারাল ও ভাইব্র্যান্ট কালার—কোনো ভারী লাল ফিল্টার নেই।
    """
    badge = create_dignified_corner_badge()
    vf = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,"
        "eq=contrast=1.10:saturation=1.12[bg];"
        "[bg][1:v]overlay=680:1500:shortest=1[v]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(clip_path),
        "-loop", "1", "-i", str(badge),
        "-filter_complex", vf,
        "-map", "[v]",
        "-t", f"{duration:.3f}",
        "-r", str(fps),
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_scene_clip(scene_idx: int, scene_text: str = "", prev_clip_name: str = "") -> Path:
    """
    স্ক্রিপ্টের বিষয়বস্তু অনুযায়ী সেরা সাইবার/টেক B-roll ফুটেজ নির্বাচন করে।
    লাল ভাব বাদ দিয়ে নীল, সায়ান ও ন্যাচারাল ফিউচারিস্টিক ক্লিপ অগ্রাধিকার দেওয়া হয়।
    """
    ensure_tech_clips_available()
    text_lower = scene_text.lower()

    if any(k in text_lower for k in ["রোবট", "যন্ত্র", "সহকারী", "রোবটিক্স", "হিউম্যানয়েড"]):
        target = "humanoid_robot.mp4"
    elif any(k in text_lower for k in ["ব্রেইন", "মস্তিষ্ক", "চিন্তা", "নিউরাল", "ভাবনা"]):
        target = "brain_3d_screen.mp4"
    elif any(k in text_lower for k in ["হাত", "ঘোরা", "স্পর্শ", "ইন্টারফেস", "স্ক্রিন", "হলোগ্রাম"]):
        target = "sci_fi_hand_gestures.mp4"
    elif any(k in text_lower for k in ["চিপ", "মাইক্রোচিপ", "সার্কিট", "কম্পিউটার", "হার্ডওয়্যার"]):
        target = "hand_projecting_hologram.mp4"
    else:
        # লাল ছাড়া সেরা হাই-টেক ক্লিপগুলোর সিকোয়েন্স
        sequence = [
            "sci_fi_hand_gestures.mp4",
            "humanoid_robot.mp4",
            "brain_3d_screen.mp4",
            "cyborg_hologram.mp4",
            "hand_projecting_hologram.mp4",
            "smartwatch_hologram.mp4"
        ]
        target = sequence[(scene_idx - 1) % len(sequence)]

    # আগের ক্লিপের সাথে যেন হুবহু না মিলে
    if target == prev_clip_name:
        alternatives = ["sci_fi_hand_gestures.mp4", "brain_3d_screen.mp4", "cyborg_hologram.mp4", "humanoid_robot.mp4"]
        for alt in alternatives:
            if alt != prev_clip_name and (TECH_CLIPS_DIR / alt).exists():
                target = alt
                break

    clip_path = TECH_CLIPS_DIR / target
    if clip_path.exists():
        return clip_path

    # ফলব্যাক যদি টার্গেট ক্লিপ না থাকে
    all_clips = [c for c in TECH_CLIPS_DIR.glob("*.mp4") if "red_" not in c.name]
    if all_clips:
        return all_clips[0]
    return list(TECH_CLIPS_DIR.glob("*.mp4"))[0]


def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    """
    ১০০% সাবটাইটেল-মুক্ত, আল্ট্রা-প্রফেশনাল হাইব্রিড সিনেমাটিক রিলস ভিডিও রেন্ডার করে।
    একবার জুবায়ের ফুল স্ক্রিন মাইকে কথা বলবে (A-Roll), একবার রোবট/হলোগ্রাম ফুটেজ দেখাবে (B-Roll)।
    """
    print("[VideoEngine] সিনেমাটিক হাইব্রিড প্রেজেন্টার ও B-roll রিলস তৈরি হচ্ছে...")
    ensure_tech_clips_available()
    rendered_parts = []
    prev_clip = ""

    for i, sc in enumerate(scene_timings, start=1):
        dur = sc.get("duration", sc.get("end", 0) - sc.get("start", 0))
        if dur <= 0:
            dur = 5.0
        text = sc.get("text", "")
        part_out = TEMP_DIR / f"hybrid_scene_{i}.mp4"

        # সিন ১ এবং ৪: ফুল স্ক্রিন সিনেমাটিক প্রেজেন্টার (A-Roll)
        # সিন ২, ৩, ৫: রোবোটিক্স ও হলোগ্রাম ফুটেজ + নিচে কর্নারে HUD প্রেজেন্টার ব্যাজ (B-Roll)
        if i in (1, 4):
            print(f"[VideoEngine] সিন {i}: ফুল স্ক্রিন প্রেজেন্টার রেন্ডারিং (স্টুডিও মাইক ও মাল্টি-অ্যাঙ্গেল)...")
            render_cinematic_aroll(dur, part_out, scene_num=i)
        else:
            clip = get_scene_clip(i, text, prev_clip)
            prev_clip = clip.name
            print(f"[VideoEngine] সিন {i}: সাই-ফাই টেক ফুটেজ ({clip.name}) + কর্নার HUD ব্যাজ রেন্ডারিং...")
            render_cinematic_broll(clip, dur, part_out)

        rendered_parts.append(part_out)

    # সকল সিন একত্রীকরণ
    concat_list = TEMP_DIR / "final_hybrid_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in rendered_parts:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    bg_video_path = TEMP_DIR / "hybrid_full_bg.mp4"
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
        safe_title = "ai_tech_reel"
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

    print("[VideoEngine] ১০০% ক্লিন হাইব্রিড রিলস ভিডিও এক্সপোর্ট হচ্ছে...")
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[VideoEngine] রেন্ডার সম্পন্ন! ভিডিও সংরক্ষিত: {output_path}")
    return output_path


# Compatibility aliases
def prepare_circular_presenter_badge() -> Path:
    return create_dignified_corner_badge()

def generate_dynamic_tech_bg(duration: float, output_path: Path):
    clip = TECH_CLIPS_DIR / "sci_fi_hand_gestures.mp4"
    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(clip), "-t", str(duration), "-c", "copy", str(output_path)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    print("=" * 60)
    print("🎬 [VIDEO MAKER TEST] সিনেমাটিক প্রেজেন্টার ও B-Roll টেস্ট")
    print("=" * 60)

    from content_writing.script_writer import get_reel_content
    from voice_audio.voice_engine import generate_voiceover_and_subtitles

    reel = get_reel_content()
    print(f"📌 টপিক: {reel['title']}")
    print("\n[১/২] টিভি নিউজ ভয়েসওভার তৈরি হচ্ছে...")
    audio_data = generate_voiceover_and_subtitles(reel["scenes"])

    print("\n[২/২] সিনেমাটিক রিলস ভিডিও রেন্ডারিং হচ্ছে...")
    test_video = render_final_reel(
        scene_timings=audio_data["scene_timings"],
        narration_path=audio_data["narration_path"],
        total_duration=audio_data["total_duration"],
        title="dignified_cinematic_reel_test"
    )

    print("=" * 60)
    print("✅ সিনেমাটিক রিলস তৈরি সম্পন্ন!")
    print(f"📂 ভিডিও ফাইল: {test_video}")
    print(f"📏 ফাইল সাইজ: {test_video.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 60)
