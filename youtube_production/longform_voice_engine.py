# -*- coding: utf-8 -*-
"""
=============================================================================
🎙️ YOUTUBE LONG-FORM VOICE ENGINE (STUDIO MASTERED FULL-LENGTH AUDIO)
=============================================================================
ইউটিউব ডকুমেন্টারি ভিডিওর জন্য অধ্যায়ভিত্তিক দীর্ঘ ভয়েসওভার তৈরি করে,
প্রতিটি সিনের সঠিক টাইমস্ট্যাম্প গণনা করে এবং হাই-কোয়ালিটি অডিও মাস্টারিং প্রয়োগ করে।
=============================================================================
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import os
import asyncio
import subprocess
from pathlib import Path
import edge_tts

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import TEMP_DIR

VOICE_CONFIG = {
    "voice": "bn-IN-BashkarNeural",
    "rate": "+10%",
    "pitch": "+2Hz"
}


def get_audio_duration(file_path: Path) -> float:
    """ffmpeg / ffprobe দিয়ে অডিওর সুনির্দিষ্ট দৈর্ঘ্য বের করে।"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 5.0


def apply_studio_mastering(raw_path: Path, out_path: Path):
    """৩-ব্যান্ড ওয়ার্ম ইকুয়ালাইজার ও ব্রডকাস্ট লাউডনেস মাস্টারিং প্রয়োগ করে।"""
    eq_filter = (
        "highpass=f=90,lowpass=f=14000,"
        "equalizer=f=200:t=q:w=1.2:g=2.0,"
        "equalizer=f=1200:t=q:w=1.5:g=1.5,"
        "equalizer=f=4000:t=q:w=1.5:g=2.5,"
        "dynaudnorm=f=150:g=12:m=10:p=0.9,"
        "loudnorm=I=-16:TP=-1.5:LRA=9"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_path),
        "-af", eq_filter,
        "-b:a", "192k",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def _synthesize_scene_audio(text: str, out_raw: Path):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE_CONFIG["voice"],
        rate=VOICE_CONFIG["rate"],
        pitch=VOICE_CONFIG["pitch"]
    )
    await communicate.save(str(out_raw))


def generate_longform_voiceover(all_scenes: list) -> dict:
    """
    সমস্ত সিনের জন্য ধারাবাহিকভাবে স্টুডিও কোয়ালিটি ভয়েসওভার তৈরি করে
    এবং প্রতিটি সিনের নির্ভুল সময়সীমা (start, end, duration) রিটার্ন করে।
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    mastered_parts = []
    scene_timings = []
    current_time = 0.0

    print(f"[LongformVoice] মোট {len(all_scenes)} টি সিনের ভয়েসওভার সিন্থেসিস শুরু হচ্ছে...")

    for i, sc in enumerate(all_scenes, start=1):
        raw_scene_path = TEMP_DIR / f"yt_scene_raw_{i}.mp3"
        mst_scene_path = TEMP_DIR / f"yt_scene_mst_{i}.mp3"

        text = sc["text"]
        asyncio.run(_synthesize_scene_audio(text, raw_scene_path))
        apply_studio_mastering(raw_scene_path, mst_scene_path)

        dur = get_audio_duration(mst_scene_path)
        start_t = current_time
        end_t = current_time + dur
        current_time = end_t

        scene_timings.append({
            "scene_id": sc["scene_id"],
            "chapter_id": sc["chapter_id"],
            "chapter_title": sc["chapter_title"],
            "clip": sc["clip"],
            "text": text,
            "is_chapter_first_scene": sc.get("is_chapter_first_scene", False),
            "start": start_t,
            "end": end_t,
            "duration": dur,
            "audio_file": mst_scene_path
        })
        mastered_parts.append(mst_scene_path)

    # সমস্ত অডিওকে একটি সম্পূর্ণ মাস্টার অডিও ফাইলে সংযুক্ত করা
    concat_txt = TEMP_DIR / "yt_concat_narration.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in mastered_parts:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    full_narration_path = TEMP_DIR / "youtube_full_narration.mp3"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(full_narration_path)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_dur = get_audio_duration(full_narration_path)

    print(f"[LongformVoice] সম্পূর্ণ অডিও রেন্ডার সম্পন্ন! মোট দৈর্ঘ্য: {total_dur:.2f} সেকেন্ড ({total_dur/60:.1f} মিনিট)")

    return {
        "full_narration_path": full_narration_path,
        "total_duration": total_dur,
        "scene_timings": scene_timings
    }
