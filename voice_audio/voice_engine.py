# -*- coding: utf-8 -*-
"""
=============================================================================
🎙️ 4. VOICE & AUDIO ENGINE (ভয়েস ও অডিও মডিউল)
=============================================================================
এই ফাইলে ফেসবুক রিলসের সমস্ত বাংলা ভয়েসওভার এবং অডিও তৈরির কোড সংরক্ষিত থাকে।
এখানে গম্ভীর ও ধীর কণ্ঠের বদলে প্রাণবন্ত, উদ্যমী ও আকর্ষণীয় স্পিড (+14%)
এবং পিচ সেট করা হয়েছে যাতে দর্শক মুগ্ধ হয়ে সম্পূর্ণ ভিডিও দেখে।

ভয়েসের স্পিড বা কণ্ঠ বদলাতে এই ফাইলে কাজ করবেন।
টেস্ট করার জন্য টার্মিনালে চালান:
    python voice_audio/voice_engine.py
=============================================================================
"""

import os
import sys
import asyncio
import subprocess
import requests
from pathlib import Path

# Ensure project root is in sys.path for standalone runs
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import edge_tts
from src.config import TEMP_DIR, OUTPUT_DIR, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

FISH_API_KEY = os.getenv("FISH_API_KEY", "").strip()
FISH_VOICE_ID = os.getenv("FISH_VOICE_ID", "").strip()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "").strip()

# আকর্ষণীয় ভয়েস প্রোফাইলসমূহ
VOICE_PROFILES = {
    # ১. উদ্যমী ও স্মার্ট টেক পুরুষ কণ্ঠ (দ্রুত ও আকর্ষণীয়)
    "male_energetic": {
        "voice": "bn-BD-PradeepNeural",
        "rate": "+14%",
        "pitch": "+2Hz",
        "label": "স্মার্ট ও উদ্যমী পুরুষ কণ্ঠ (প্রদীপ)"
    },
    # ২. প্রাণবন্ত ও অত্যন্ত আকর্ষণীয় নারী কণ্ঠ (খুবই মিষ্টি ও চটপটে)
    "female_lively": {
        "voice": "bn-BD-NabanitaNeural",
        "rate": "+12%",
        "pitch": "+0Hz",
        "label": "প্রাণবন্ত ও মিষ্টি কথক কণ্ঠ (নবনীতা)"
    },
    # ৩. গল্প বলার মতো রোমাঞ্চকর পুরুষ কণ্ঠ
    "male_storyteller": {
        "voice": "bn-IN-BashkarNeural",
        "rate": "+14%",
        "pitch": "+1Hz",
        "label": "রোমাঞ্চকর গল্প কথক পুরুষ কণ্ঠ (ভাস্কর)"
    }
}

# ডিফল্ট সক্রিয় ভয়েস প্রোফাইল (চাইলে 'female_lively' অথবা 'male_storyteller' দিতে পারেন)
CURRENT_PROFILE_KEY = os.getenv("VOICE_PROFILE", "male_energetic")

def format_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


async def generate_edge_tts(text: str, output_path: Path, profile_key: str = None):
    """Generates lively, fast-paced, high-retention Bengali neural voiceover."""
    key = profile_key or CURRENT_PROFILE_KEY
    cfg = VOICE_PROFILES.get(key, VOICE_PROFILES["male_energetic"])
    
    communicate = edge_tts.Communicate(
        text=text,
        voice=cfg["voice"],
        rate=cfg["rate"],
        pitch=cfg["pitch"]
    )
    await communicate.save(str(output_path))

def generate_fish_audio_voice(text: str, output_path: Path) -> bool:
    """Generate cloned user voice using Fish Audio 100% Free API."""
    if not FISH_API_KEY or not FISH_VOICE_ID:
        return False
    try:
        url = "https://api.fish.audio/v1/tts"
        headers = {
            "Authorization": f"Bearer {FISH_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "reference_id": FISH_VOICE_ID,
            "format": "mp3",
            "mp3_bitrate": 192
        }
        res = requests.post(url, headers=headers, json=payload, timeout=45)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
            return True
        else:
            print(f"[FishAudio] API error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[FishAudio] Request exception: {e}")
    return False

def generate_elevenlabs_voice(text: str, output_path: Path) -> bool:
    """Generate cloned user voice using ElevenLabs API."""
    if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
        return False
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.85}
        }
        res = requests.post(url, headers=headers, json=data, timeout=30)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
            return True
        else:
            print(f"[VoiceClone] ElevenLabs API returned {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[VoiceClone] Error with ElevenLabs: {e}")
    return False

def generate_voiceover_and_subtitles(scenes: list):
    scene_audios = []
    srt_entries = []
    current_time = 0.0
    scene_timings = []

    for i, scene in enumerate(scenes, start=1):
        scene_audio_path = TEMP_DIR / f"scene_{i}.mp3"

        # 1. Try Fish Audio (Free Cloned User Voice)
        cloned = generate_fish_audio_voice(scene["text"], scene_audio_path)
        # 2. Try ElevenLabs
        if not cloned or not scene_audio_path.exists() or scene_audio_path.stat().st_size == 0:
            cloned = generate_elevenlabs_voice(scene["text"], scene_audio_path)
        # 3. Fallback to lively Edge-TTS
        if not cloned or not scene_audio_path.exists() or scene_audio_path.stat().st_size == 0:
            asyncio.run(generate_edge_tts(scene["text"], scene_audio_path))

        duration = get_audio_duration(scene_audio_path)
        start_time = current_time
        end_time = current_time + duration

        srt_entry = f"{i}\n{format_srt_time(start_time)} --> {format_srt_time(end_time)}\n{scene['text']}\n"
        srt_entries.append(srt_entry)

        scene_timings.append({
            "index": i,
            "text": scene["text"],
            "query": scene["query"],
            "audio_path": scene_audio_path,
            "start": start_time,
            "end": end_time,
            "duration": duration
        })

        scene_audios.append(scene_audio_path)
        current_time = end_time

    full_narration_path = TEMP_DIR / "full_narration.mp3"
    concat_list_file = TEMP_DIR / "concat_audio.txt"

    with open(concat_list_file, "w", encoding="utf-8") as f:
        for audio in scene_audios:
            f.write(f"file '{str(audio).replace(chr(92), '/')}'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(full_narration_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    srt_path = TEMP_DIR / "subtitles.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))

    total_duration = current_time
    return {
        "narration_path": full_narration_path,
        "srt_path": srt_path,
        "total_duration": total_duration,
        "scene_timings": scene_timings
    }

# =============================================================================
# স্বতন্ত্র টেস্ট কোড (টার্মিনালে সরাসরি চালিয়ে ভয়েস টেস্ট করার জন্য)
# =============================================================================
if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 60)
    print("🎙️ [VOICE ENGINE TEST] ৩টি আকর্ষণীয় বাংলা ভয়েস স্যাম্পল তৈরি")
    print("=" * 60)

    sample_text = (
        "আগামী ৫ বছরে কোন কোন পেশা পুরোপুরি বদলে দেবে কৃত্রিম বুদ্ধিমত্তা? "
        "এই তথ্যটি প্রত্যেকের জানা দরকার। ভিডিওটি শেষ পর্যন্ত দেখুন!"
    )

    for profile_key, p_info in VOICE_PROFILES.items():
        sample_path = TEMP_DIR / f"voice_sample_{profile_key}.mp3"
        print(f"\n🔊 তৈরি হচ্ছে: {p_info['label']} (স্পিড: {p_info['rate']})")
        asyncio.run(generate_edge_tts(sample_text, sample_path, profile_key=profile_key))
        print(f"✅ তৈরি হয়েছে: {sample_path}")

        # Send to Telegram directly so Jubayer can listen on mobile
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            try:
                base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
                cap = (
                    f"🎙️ *ভয়েস স্যাম্পল:* {p_info['label']}\n"
                    f"⚡ স্পিড: {p_info['rate']} | পিচ: {p_info['pitch']}\n\n"
                    f"প্লে করে শুনুন এই কণ্ঠটি আপনার কেমন লাগছে!"
                )
                with open(sample_path, "rb") as af:
                    requests.post(
                        f"{base_url}/sendAudio",
                        data={"chat_id": TELEGRAM_CHAT_ID, "caption": cap, "parse_mode": "Markdown"},
                        files={"audio": af},
                        timeout=30
                    )
                print(f"📲 টেলিগ্রামে পাঠানো হয়েছে: {p_info['label']}")
            except Exception as ex:
                print(f"টেলিগ্রামে পাঠানো সম্ভব হয়নি: {ex}")

    print("\n" + "=" * 60)
    print("🎉 ৩টি ভিন্ন স্টাইলের প্রাণবন্ত বাংলা ভয়েস স্যাম্পল টেলিগ্রামে পৌঁছে গেছে!")
    print("আপনার ফোনে টেলিগ্রাম খুলে শুনে দেখুন কোনটি আপনার সবচেয়ে বেশি পছন্দ।")
    print("=" * 60)

