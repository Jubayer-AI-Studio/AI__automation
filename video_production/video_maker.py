# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 VIDEO PRODUCTION ENGINE (ন্যাচারাল টকিং প্রেজেন্টার ও হাই-টেক এডিশন)
=============================================================================
এই ইঞ্জিনে ফেসবুক রিলসের ১০০% নিখুঁত ও মর্যাদাপূর্ণ এআই ভিডিও তৈরি হয়:
  - A-Roll: জুবায়েরের ফুল স্ক্রিন সিনেমাটিক স্টুডিও প্রেজেন্টার (মাইক ও মনিটরের সামনে)
  - মানুষের স্বাভাবিক কথা বলার ছন্দে (Syllable Cadence ~2-3/sec) ঠোঁট ও চোয়ালের নিখুঁত নড়াচড়া
  - কথা থামলে বা বিরতিতে স্বয়ংক্রিয়ভাবে স্বাভাবিক বন্ধ অবস্থানে প্রত্যাবর্তন (কখনোই হা করে থাকবে না)
  - সিমলেস গাউসিয়ান ফেদার মাস্কিং—শরীর, হাত বা কাপড়ে ১ পিক্সেলও অযাচিত ঝাঁকুনি নেই
  - B-Roll: রোবোটিক্স, সাই-ফাই হলোগ্রাম ও ফিউচারিস্টিক হাই-টেক ভিডিও ফুটেজ
  - কর্নার HUD ব্যাজ: B-Roll চলাকালীন নিচে ডান কোনায় সাইবার সায়ান ও গোল্ডেন HUD রিংসহ জুবায়েরের ন্যাচারাল টকিং অবতার
  - কোনো কার্টুনিশ দ্রুত পুতুল-নাচ নেই
  - কোনো বিরক্তিকর লাল ফিল্টার নেই—ন্যাচারাল স্কিন টোন ও সাইবার কুল ব্লু/সায়ান লাইটিং
  - ১০০% সাবটাইটেল ও টেক্সট মুক্ত (একদম ক্লিন সিনেমাটিক লুক)
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
from itertools import groupby
import numpy as np

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PIL import Image, ImageDraw, ImageFilter
from src.config import BGM_PATH, OUTPUT_DIR, TEMP_DIR

ASSETS_DIR = BASE_DIR / "assets"
TECH_CLIPS_DIR = ASSETS_DIR / "tech_clips"
POSES_DIR = ASSETS_DIR / "presenter_poses"
PRESENTER_IMG_PATH = ASSETS_DIR / "presenter.jpg"
ALIGNED_DIR = TEMP_DIR / "aligned_states"

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


def generate_aligned_presenter_assets():
    """
    একই বডি ফ্রেমের ওপর শুধুমাত্র মুখ ও চোয়ালের অংশ ফেদার মাস্ক দিয়ে পারফেক্ট অ্যালাইন করে।
    এর ফলে কথা বলার সময় শরীর বা হাতের বিন্দুমাত্র ঝাঁকুনি হয় না এবং ট্রানজিশন ১০০% সিমলেস থাকে।
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    ALIGNED_DIR.mkdir(parents=True, exist_ok=True)

    test_file = ALIGNED_DIR / "aligned_closed.jpg"
    if test_file.exists():
        return

    pose_mid_path = POSES_DIR / "pose_talk_mid.jpg"
    pose_closed_path = POSES_DIR / "pose_closed.jpg"
    pose_open_path = POSES_DIR / "pose_talk_open.jpg"

    if not pose_mid_path.exists():
        pose_mid_path = PRESENTER_IMG_PATH
    if not pose_closed_path.exists():
        pose_closed_path = pose_mid_path
    if not pose_open_path.exists():
        pose_open_path = pose_mid_path

    base = Image.open(pose_mid_path).convert("RGBA")
    closed = Image.open(pose_closed_path).convert("RGBA")
    open_img = Image.open(pose_open_path).convert("RGBA")

    # সিমলেস লিপ/চিন বাউন্ডিং বক্স ও সফট ফেদার মাস্ক
    box = (325, 520, 445, 625)
    bw = box[2] - box[0]
    bh = box[3] - box[1]

    mask = Image.new("L", (bw, bh), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((6, 6, bw - 6, bh - 6), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(8))

    # ৩টি সম্পূর্ণ অ্যালাইনড ফুল ছবি (একই শরীর ও হাত, কেবল মুখ পরিবর্তন)
    aligned_imgs = {
        "closed": base.copy(),
        "mid": base.copy(),
        "open": base.copy()
    }
    aligned_imgs["closed"].paste(closed.crop(box), box, mask)
    aligned_imgs["open"].paste(open_img.crop(box), box, mask)

    for state, img in aligned_imgs.items():
        img.convert("RGB").save(ALIGNED_DIR / f"aligned_{state}.jpg", quality=95)

    # কর্নার HUD গোল ব্যাজ তৈরি
    for state, img in aligned_imgs.items():
        w, h = img.size
        face_size = int(h * 0.38)
        cx = w // 2
        cy = int(h * 0.38)
        cropped = img.crop((cx - face_size//2, cy - face_size//2, cx + face_size//2, cy + face_size//2)).resize((300, 300), Image.Resampling.LANCZOS)

        cmask = Image.new("L", (300, 300), 0)
        cdraw = ImageDraw.Draw(cmask)
        cdraw.ellipse((0, 0, 300, 300), fill=255)

        circular = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        circular.paste(cropped, (0, 0), cmask)

        canvas = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(canvas)
        ccx, ccy = 180, 180

        # আউটার সাইবার গ্লো
        for r_offset, alpha in [(8, 40), (6, 80), (4, 140), (2, 200)]:
            r = 168 + r_offset
            bdraw.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=(0, 240, 255, alpha), width=2)

        bdraw.ellipse((ccx - 165, ccy - 165, ccx + 165, ccy + 165), outline="#00F0FF", width=4)
        bdraw.ellipse((ccx - 156, ccy - 156, ccx + 156, ccy + 156), outline="#FFD700", width=2)

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
            bdraw.line([(x1, y1), (x2, y2)], fill="#38BDF8", width=2)

        canvas.paste(circular, (30, 30), circular)
        bdraw.ellipse((ccx - 150, ccy - 150, ccx + 150, ccy + 150), outline=(255, 255, 255, 180), width=2)
        canvas.save(ALIGNED_DIR / f"badge_{state}.png", format="PNG")


def get_natural_speech_segments(audio_path: Path, scene_dur: float, fps: int = 30) -> list:
    """
    ভয়েসের শব্দশক্তি ও মানবীয় স্বাভাবিক কথার ছন্দে (প্রতি সেকেন্ডে ২-৩টি স্বাভাবিক নড়াচড়া)
    লিপ-সিঙ্ক সেগমেন্ট তৈরি করে। কথা না বললে স্বয়ংক্রিয়ভাবে স্বাভাবিক বন্ধ অবস্থানে থাকে।
    """
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
    samples_per_frame = sample_rate // fps
    num_frames = max(1, int(scene_dur * fps))
    samples = struct.unpack(f"<{total_samples}h", data)

    rms_vals = []
    for i in range(num_frames):
        st = i * samples_per_frame
        chunk = samples[st:st + samples_per_frame] if st < total_samples else []
        rms = math.sqrt(sum(s**2 for s in chunk) / len(chunk)) if chunk else 0.0
        rms_vals.append(rms)

    # মুভিং অ্যাভারেজ স্মুথিং (৫ ফ্রেম = ১৬৭ মিলিসেকেন্ড) যা মাইক্রো-ফ্লিকারিং সম্পূর্ণ দূর করে
    w = 5
    smoothed = np.convolve(rms_vals, np.ones(w)/w, mode="same")

    active = [r for r in smoothed if r > 300]
    avg_r = float(np.mean(active)) if len(active) > 0 else 1000.0
    low_th = avg_r * 0.35
    high_th = avg_r * 0.85

    raw_states = []
    for r in smoothed:
        if r < low_th:
            raw_states.append("closed")
        elif r < high_th:
            raw_states.append("mid")
        else:
            raw_states.append("open")

    # মিনিমাম হোল্ড ফিল্টার (কমপক্ষে ৫ ফ্রেম = ১৬৭ মিলিসেকেন্ড) যা স্বাভাবিক মানুষের উচ্চারণের গতির সাথে মিলে
    min_hold = 5
    filtered_states = []
    idx = 0
    while idx < len(raw_states):
        curr = raw_states[idx]
        count = 1
        while idx + count < len(raw_states) and raw_states[idx + count] == curr:
            count += 1
        if count < min_hold:
            count = min(min_hold, len(raw_states) - idx)
        filtered_states.extend([curr] * count)
        idx += count

    filtered_states = filtered_states[:num_frames]

    # একই স্টেটের ফ্রেমগুলোকে সেগমেন্টে রূপান্তর (state, duration)
    segments = []
    for k, g in groupby(filtered_states):
        dur = len(list(g)) / fps
        segments.append((k, dur))

    return segments


def render_aroll_presenter_scene(audio_path: Path, duration: float, out_path: Path, fps: int = 30):
    """
    ফুল স্ক্রিন স্টুডিও প্রেজেন্টার শট:
      - জুবায়ের মাইকের সামনে কথা বলছেন, পেছনে কোডিং মনিটর
      - ঠোঁটের নড়াচড়া ১০০% স্বাভাবিক ও জীবন্ত
      - শরীর, হাত বা কাপড়ে কোনো ঝাঁকুনি নেই (০ পিক্সেল জাম্প)
      - বিরতিতে মুখ স্বাভাবিকভাবে বন্ধ, কথা বলার সময় স্বরধ্বনির সাথে মিল রেখে মুভমেন্ট
    """
    generate_aligned_presenter_assets()
    segments = get_natural_speech_segments(audio_path, duration, fps)

    img_map = {
        "closed": (ALIGNED_DIR / "aligned_closed.jpg").resolve().as_posix(),
        "mid": (ALIGNED_DIR / "aligned_mid.jpg").resolve().as_posix(),
        "open": (ALIGNED_DIR / "aligned_open.jpg").resolve().as_posix()
    }

    concat_txt = TEMP_DIR / f"concat_aroll_{out_path.stem}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for st, dur in segments:
            f.write(f"file '{img_map[st]}'\n")
            f.write(f"duration {dur:.3f}\n")
        f.write(f"file '{img_map[segments[-1][0]]}'\n")

    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,eq=contrast=1.06:saturation=1.10"
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
    হাই-টেক B-roll ফুটেজ + নিচে ডান কোনায় জুবায়েরের ন্যাচারাল টকিং HUD ব্যাজ।
    """
    generate_aligned_presenter_assets()
    segments = get_natural_speech_segments(audio_path, duration, fps)

    badge_map = {
        "closed": (ALIGNED_DIR / "badge_closed.png").resolve().as_posix(),
        "mid": (ALIGNED_DIR / "badge_mid.png").resolve().as_posix(),
        "open": (ALIGNED_DIR / "badge_open.png").resolve().as_posix()
    }

    concat_badge = TEMP_DIR / f"concat_badge_{out_path.stem}.txt"
    with open(concat_badge, "w", encoding="utf-8") as f:
        for st, dur in segments:
            f.write(f"file '{badge_map[st]}'\n")
            f.write(f"duration {dur:.3f}\n")
        f.write(f"file '{badge_map[segments[-1][0]]}'\n")

    vf = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,"
        "eq=contrast=1.10:saturation=1.12[bg];"
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
        # নীল ও সায়ান হাই-টেক ক্লিপগুলোর সিকোয়েন্স
        sequence = [
            "sci_fi_hand_gestures.mp4",
            "humanoid_robot.mp4",
            "brain_3d_screen.mp4",
            "cyborg_hologram.mp4",
            "hand_projecting_hologram.mp4",
            "smartwatch_hologram.mp4"
        ]
        target = sequence[(scene_idx - 1) % len(sequence)]

    if target == prev_clip_name:
        alternatives = ["sci_fi_hand_gestures.mp4", "brain_3d_screen.mp4", "cyborg_hologram.mp4", "humanoid_robot.mp4"]
        for alt in alternatives:
            if alt != prev_clip_name and (TECH_CLIPS_DIR / alt).exists():
                target = alt
                break

    clip_path = TECH_CLIPS_DIR / target
    if clip_path.exists():
        return clip_path

    all_clips = [c for c in TECH_CLIPS_DIR.glob("*.mp4") if "red_" not in c.name]
    if all_clips:
        return all_clips[0]
    return list(TECH_CLIPS_DIR.glob("*.mp4"))[0]


def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    """
    ১০০% সাবটাইটেল-মুক্ত, আল্ট্রা-প্রফেশনাল হাইব্রিড রিলস ভিডিও রেন্ডার করে।
    একবার জুবায়ের ফুল স্ক্রিন মাইকে কথা বলবে (A-Roll), একবার রোবট/হলোগ্রাম ফুটেজ দেখাবে (B-Roll)।
    """
    print("[VideoEngine] ন্যাচারাল প্রেজেন্টার ও B-roll রিলস তৈরি হচ্ছে...")
    ensure_tech_clips_available()
    generate_aligned_presenter_assets()
    rendered_parts = []
    prev_clip = ""

    for i, sc in enumerate(scene_timings, start=1):
        dur = sc.get("duration", sc.get("end", 0) - sc.get("start", 0))
        if dur <= 0:
            dur = 5.0
        text = sc.get("text", "")
        part_audio = TEMP_DIR / f"scene_{i}.mp3"
        part_out = TEMP_DIR / f"hybrid_scene_{i}.mp4"

        # সিন ১ এবং ৪: ফুল স্ক্রিন সিনেমাটিক প্রেজেন্টার (A-Roll)
        # সিন ২, ৩, ৫: রোবোটিক্স ও হলোগ্রাম ফুটেজ + নিচে কর্নারে ন্যাচারাল HUD ব্যাজ (B-Roll)
        if i in (1, 4):
            print(f"[VideoEngine] সিন {i}: ফুল স্ক্রিন প্রেজেন্টার রেন্ডারিং (ন্যাচারাল টকিং)...")
            render_aroll_presenter_scene(part_audio, dur, part_out)
        else:
            clip = get_scene_clip(i, text, prev_clip)
            prev_clip = clip.name
            print(f"[VideoEngine] সিন {i}: সাই-ফাই টেক ফুটেজ ({clip.name}) + কর্নার HUD ব্যাজ রেন্ডারিং...")
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
    generate_aligned_presenter_assets()
    return ALIGNED_DIR / "badge_closed.png"

def generate_dynamic_tech_bg(duration: float, output_path: Path):
    clip = TECH_CLIPS_DIR / "sci_fi_hand_gestures.mp4"
    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(clip), "-t", str(duration), "-c", "copy", str(output_path)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    print("=" * 60)
    print("🎬 [VIDEO MAKER TEST] ন্যাচারাল প্রেজেন্টার ও B-Roll টেস্ট")
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
        title="natural_talking_reel_test"
    )

    print("=" * 60)
    print("✅ ন্যাচারাল টকিং রিলস তৈরি সম্পন্ন!")
    print(f"📂 ভিডিও ফাইল: {test_video}")
    print(f"📏 ফাইল সাইজ: {test_video.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 60)
