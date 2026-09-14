import asyncio
import os
import subprocess
from pathlib import Path
import edge_tts
from src.config import VOICE_NAME, TEMP_DIR

def format_srt_time(seconds: float) -> str:
    """Format seconds into SRT timestamp HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def get_audio_duration(file_path: Path) -> float:
    """Get exact duration of an audio file using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def generate_scene_audio(text: str, output_path: Path, voice: str = VOICE_NAME):
    """Generate audio file for a single scene using edge-tts."""
    # Slight rate reduction (-3%) and pitch reduction (-2Hz) for a suspenseful mystery tone
    communicate = edge_tts.Communicate(text, voice, rate="-3%", pitch="-2Hz")
    await communicate.save(str(output_path))

def generate_voiceover_and_subtitles(scenes: list):
    """
    Generates audio for each scene, measures duration, creates full narration MP3,
    and produces an SRT subtitle file perfectly synchronized to each scene.
    """
    scene_audios = []
    srt_entries = []
    current_time = 0.0
    scene_timings = []

    for i, scene in enumerate(scenes, start=1):
        scene_audio_path = TEMP_DIR / f"scene_{i}.mp3"
        asyncio.run(generate_scene_audio(scene["text"], scene_audio_path))
        
        duration = get_audio_duration(scene_audio_path)
        start_time = current_time
        end_time = current_time + duration
        
        # Subtitle entry for this scene
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

    # Combine all scene audios into one master narration track
    full_narration_path = TEMP_DIR / "full_narration.mp3"
    concat_list_file = TEMP_DIR / "concat_audio.txt"
    
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for audio in scene_audios:
            # Escape path for ffmpeg concat
            f.write(f"file '{str(audio).replace(chr(92), '/')}'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(full_narration_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Save SRT subtitles file
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
