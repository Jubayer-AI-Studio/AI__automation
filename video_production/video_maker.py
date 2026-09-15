# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 2. VIDEO PRODUCTION ENGINE (হাইব্রিড প্রেজেন্টার ও টকিং হেড এডিশন)
=============================================================================
এই ফাইলে ফেসবুক রিলসের আল্ট্রা-প্রফেশনাল হাইব্রিড ভিডিও তৈরি হয়:
  - একবার জুবায়েরের ফুল স্ক্রিন ভিডিও: মাইকে কথা বলছেন কম্পিউটার ও কোডিং মনিটরের সামনে
  - আরেকবার রোবোটিক্স, হলোগ্রাম ও মাইক্রোচিপের B-roll ফুটেজ
  - B-roll চলাকালীন নিচে কর্নারে জুবায়েরের অডিও-রিঅ্যাক্টিভ টকিং ব্যাজ (রিয়েল মুখ নাড়িয়ে কথা বলবে)
  - ১০০% টেক্সট ও সাবটাইটেল মুক্ত (ক্লিন সিনেমাটিক লুক)
  - টিভি নিউজ বুলেটিন ভয়েসওভার ও ব্যাকগ্রাউন্ড মিউজিকের ব্যালেন্সড মিক্সিং

টেস্ট করার জন্য টার্মিনালে চালান:
    python video_production/video_maker.py
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
import struct
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
POSES_DIR = ASSETS_DIR / "presenter_poses"
PRESENTER_IMG_PATH = ASSETS_DIR / "presenter.jpg"

# Curated high-tech royalty-free clips repository
CURATED_TECH_CLIPS = {
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


def prepare_circular_talking_badges() -> dict:
    """
    জুবায়েরের ৩টি টকিং পোজের জন্য সাইবার সায়ান ও গোল্ড HUD রিং যুক্ত ৩টি গোল ব্যাজ তৈরি করে:
    - closed (মুখ বন্ধ)
    - mid (মুখ সামান্য খোলা)
    - open (মুখ সম্পূর্ণ খোলা, কথা বলার পোজ)
    """
    badges = {}
    poses = {
        "closed": POSES_DIR / "pose_closed.jpg",
        "mid": POSES_DIR / "pose_talk_mid.jpg",
        "open": POSES_DIR / "pose_talk_open.jpg"
    }

    for state, img_path in poses.items():
        out_badge = TEMP_DIR / f"badge_{state}.png"
        if out_badge.exists():
            badges[state] = out_badge
            continue

        if not img_path.exists():
            # ফলব্যাক যদি পোজ না থাকে
            img_path = PRESENTER_IMG_PATH

        img = Image.open(img_path).convert("RGBA")
        w, h = img.size
        face_size = int(h * 0.38)
        cx = w // 2
        cy = int(h * 0.40)
        cropped = img.crop((cx - face_size//2, cy - face_size//2, cx + face_size//2, cy + face_size//2)).resize((300, 300), Image.Resampling.LANCZOS)

        mask = Image.new("L", (300, 300), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 300, 300), fill=255)

        circular = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        circular.paste(cropped, (0, 0), mask)

        # আল্ট্রা-ক্লিন সাইবার সায়ান ও গোল্ডেন HUD রিং (কোনো অতিরিক্ত লাল ফিল্টার নেই)
        canvas = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        ccx, ccy = 180, 180

        for r_offset, alpha in [(8, 40), (6, 80), (4, 140), (2, 200)]:
            r = 168 + r_offset
            draw.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=(0, 240, 255, alpha), width=2)

        draw.ellipse((ccx - 165, ccy - 165, ccx + 165, ccy + 165), outline="#00F0FF", width=4)
        draw.ellipse((ccx - 156, ccy - 156, ccx + 156, ccy + 156), outline="#FFD700", width=2)

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
        draw.ellipse((ccx - 150, ccy - 150, ccx + 150, cy + 150), outline=(255, 255, 255, 180), width=2)
        canvas.save(out_badge, format="PNG")
        badges[state] = out_badge

    return badges


def get_audio_phoneme_segments(audio_path: Path, scene_dur: float, fps: int = 30) -> list:
    """ভয়েসের অ্যাম্প্লিচিউড ও শক্তি মেপে লিপ-সিঙ্ক সেগমেন্ট তৈরি করে।"""
    raw_pcm = TEMP_DIR / f"pcm_{audio_path.stem}.raw"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(audio_path),
        "-f", "s16le",
        "-ac", "1",
        "-ar", "16000",
        str(raw_pcm)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(raw_pcm, "rb") as f:
        data = f.read()

    sample_rate = 16000
    total_samples = len(data) // 2
    num_frames = max(1, int(scene_dur * fps))
    samples_per_frame = max(1, sample_rate // fps)
    samples = struct.unpack(f"<{total_samples}h", data)

    rms_vals = []
    for i in range(num_frames):
        st = i * samples_per_frame
        chunk = samples[st:st + samples_per_frame] if st < total_samples else []
        rms = math.sqrt(sum(s**2 for s in chunk) / len(chunk)) if chunk else 0.0
        rms_vals.append(rms)

    active = [r for r in rms_vals if r > 200]
    avg_r = sum(active) / len(active) if active else 500
    low_th = avg_r * 0.4
    high_th = avg_r * 0.85

    segments = []
    curr_state = None
    curr_count = 0

    for r in rms_vals:
        st = "closed" if r < low_th else ("mid" if r < high_th else "open")
        if st == curr_state:
            curr_count += 1
        else:
            if curr_state is not None:
                segments.append((curr_state, curr_count / fps))
            curr_state = st
            curr_count = 1
    if curr_state is not None:
        segments.append((curr_state, curr_count / fps))

    return segments


def render_aroll_presenter_scene(audio_path: Path, duration: float, out_path: Path, fps: int = 30):
    """
    ফুল স্ক্রিন জুবায়ের: মাইকে কথা বলছেন কম্পিউটার মনিটরের সামনে।
    ভয়েসের সাথে তাল মিলিয়ে মুখ ও হাতের মুভমেন্ট এনিমেট হবে।
    """
    segments = get_audio_phoneme_segments(audio_path, duration, fps)
    pose_map = {
        "closed": (POSES_DIR / "pose_closed.jpg").resolve().as_posix(),
        "mid": (POSES_DIR / "pose_talk_mid.jpg").resolve().as_posix(),
        "open": (POSES_DIR / "pose_talk_open.jpg").resolve().as_posix()
    }

    concat_txt = TEMP_DIR / f"concat_aroll_{out_path.stem}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for st, dur in segments:
            f.write(f"file '{pose_map[st]}'\n")
            f.write(f"duration {dur:.3f}\n")
        f.write(f"file '{pose_map[segments[-1][0]]}'\n")

    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,eq=contrast=1.08:saturation=1.10"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
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


def render_broll_scene_with_badge(clip_path: Path, audio_path: Path, duration: float, out_path: Path, fps: int = 30):
    """
    রোবোটিক্স/হলোগ্রাম B-roll ফুটেজ + নিচে কর্নারে জুবায়েরের রিয়েল টকিং অবতার ব্যাজ।
    """
    badges = prepare_circular_talking_badges()
    segments = get_audio_phoneme_segments(audio_path, duration, fps)

    badge_map = {
        "closed": badges["closed"].resolve().as_posix(),
        "mid": badges["mid"].resolve().as_posix(),
        "open": badges["open"].resolve().as_posix()
    }

    concat_badge = TEMP_DIR / f"concat_badge_{out_path.stem}.txt"
    with open(concat_badge, "w", encoding="utf-8") as f:
        for st, dur in segments:
            f.write(f"file '{badge_map[st]}'\n")
            f.write(f"duration {dur:.3f}\n")
        f.write(f"file '{badge_map[segments[-1][0]]}'\n")

    # ক্লিয়ার ও ক্রিস্প টেক কালার (ন্যাচারাল ও ভাইব্র্যান্ট, কোনো জোরপূর্বক লাল ফিল্টার নেই)
    vf = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,"
        "eq=contrast=1.12:saturation=1.15[bg];"
        "[bg][1:v]overlay=680:1500:shortest=1[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(clip_path),
        "-f", "concat", "-safe", "0", "-i", str(concat_badge),
        "-filter_complex", vf,
        "-map", "[v]",
        "-t", f"{duration:.3f}",
        "-r", str(fps),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_scene_clip(scene_idx: int, scene_text: str = "", prev_clip_name: str = "") -> Path:
    """স্ক্রিপ্টের বিষয়বস্তু অনুযায়ী সেরা টেক B-roll ফুটেজ নির্বাচন করে।"""
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
        sequence = [
            "sci_fi_hand_gestures.mp4",
            "red_circuit_board.mp4",
            "brain_3d_screen.mp4",
            "humanoid_robot.mp4",
            "red_mesh_3d.mp4"
        ]
        target = sequence[(scene_idx - 1) % len(sequence)]

    if target == prev_clip_name:
        alternatives = ["sci_fi_hand_gestures.mp4", "brain_3d_screen.mp4", "hologram_gestures.mp4", "humanoid_robot.mp4"]
        for alt in alternatives:
            if alt != prev_clip_name and (TECH_CLIPS_DIR / alt).exists():
                target = alt
                break

    clip_path = TECH_CLIPS_DIR / target
    if clip_path.exists():
        return clip_path

    all_clips = list(TECH_CLIPS_DIR.glob("*.mp4"))
    if all_clips:
        return all_clips[0]
    return BASE_DIR / "assets" / "tech_clip_1.mp4"


def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    """
    ১০০% সাবটাইটেল-মুক্ত, হাইব্রিড প্রেজেন্টার এআই রিলস ভিডিও রেন্ডার করে।
    একবার জুবায়ের ফুল স্ক্রিন মাইকে কথা বলবে, একবার রোবট/হলোগ্রাম ফুটেজ দেখাবে।
    """
    print("[VideoEngine] হাইব্রিড প্রেজেন্টার ও B-roll ভিডিও মন্টেজ তৈরি হচ্ছে...")
    ensure_tech_clips_available()
    rendered_parts = []
    prev_clip = ""

    for i, sc in enumerate(scene_timings, start=1):
        dur = sc.get("duration", sc.get("end", 0) - sc.get("start", 0))
        if dur <= 0:
            dur = 5.0
        text = sc.get("text", "")
        part_audio = TEMP_DIR / f"scene_{i}.mp3"
        part_out = TEMP_DIR / f"hybrid_scene_{i}.mp4"

        # সিন ১ এবং ৪: ফুল স্ক্রিন প্রেজেন্টার (A-Roll)
        # সিন ২, ৩, ৫: রোবট / হলোগ্রাম ফুটেজ + নিচে কর্নারে কথা বলা অবতার (B-Roll)
        if i in (1, 4):
            print(f"[VideoEngine] সিন {i}: ফুল স্ক্রিন প্রেজেন্টার রেন্ডারিং (মাইকে বক্তব্য)...")
            render_aroll_presenter_scene(part_audio, dur, part_out)
        else:
            clip = get_scene_clip(i, text, prev_clip)
            prev_clip = clip.name
            print(f"[VideoEngine] সিন {i}: টেক ফুটেজ ({clip.name}) + কর্নার টকিং ব্যাজ রেন্ডারিং...")
            render_broll_scene_with_badge(clip, part_audio, dur, part_out)

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

    # অডিও মিক্সিং (টিভি নিউজ ভয়েসওভার + ১০% ব্যাকগ্রাউন্ড মিউজিক)
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
    badges = prepare_circular_talking_badges()
    return badges["closed"]

def generate_dynamic_tech_bg(duration: float, output_path: Path):
    clip = TECH_CLIPS_DIR / "sci_fi_hand_gestures.mp4"
    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(clip), "-t", str(duration), "-c", "copy", str(output_path)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# =============================================================================
# টেস্ট কোড
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🎬 [VIDEO MAKER TEST] হাইব্রিড প্রেজেন্টার ও টকিং হেড টেস্ট")
    print("=" * 60)

    from content_writing.script_writer import get_reel_content
    from src.audio_engine import generate_voiceover_and_subtitles

    reel = get_reel_content()
    print(f"📌 টপিক: {reel['title']}")
    print("\n[১/২] টিভি নিউজ ভয়েসওভার তৈরি হচ্ছে...")
    audio_data = generate_voiceover_and_subtitles(reel["scenes"])

    print("\n[২/২] হাইব্রিড প্রেজেন্টার রিলস ভিডিও রেন্ডারিং হচ্ছে...")
    test_video = render_final_reel(
        scene_timings=audio_data["scene_timings"],
        narration_path=audio_data["narration_path"],
        total_duration=audio_data["total_duration"],
        title="hybrid_presenter_reel_sample"
    )

    print("=" * 60)
    print(f"✅ হাইব্রিড টকিং প্রেজেন্টার রিলস তৈরি সম্পন্ন!")
    print(f"📂 ভিডিও ফাইল: {test_video}")
    print(f"📏 ফাইল সাইজ: {test_video.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 60)
