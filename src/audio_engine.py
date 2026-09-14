import os
import asyncio
import subprocess
import requests
from pathlib import Path
import edge_tts
from src.config import VOICE_NAME, TEMP_DIR

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "").strip()

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

async def generate_edge_tts(text: str, output_path: Path):
    communicate = edge_tts.Communicate(text, VOICE_NAME, rate="-2%", pitch="-2Hz")
    await communicate.save(str(output_path))

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

        # Try user's cloned voice first, fallback to Edge-TTS
        cloned = generate_elevenlabs_voice(scene["text"], scene_audio_path)
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
