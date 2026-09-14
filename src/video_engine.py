import subprocess
from pathlib import Path
from src.config import BGM_PATH, FONTS_DIR, OUTPUT_DIR, TEMP_DIR

def render_final_reel(clip_paths: list, narration_path: Path, srt_path: Path, total_duration: float, title: str) -> Path:
    """
    Concatenates clips, overlays styled Bengali subtitles, mixes narration with BGM,
    and renders the final 1080x1920 MP4 reel.
    """
    # 1. Create concat list for video clips
    concat_video_file = TEMP_DIR / "concat_video.txt"
    with open(concat_video_file, "w", encoding="utf-8") as f:
        for clip in clip_paths:
            f.write(f"file '{str(clip).replace(chr(92), '/')}'\n")

    video_only_path = TEMP_DIR / "combined_video.mp4"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_video_file),
        "-c", "copy",
        str(video_only_path)
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Prepare audio mix (Narration + BGM)
    mixed_audio_path = TEMP_DIR / "final_audio.mp3"
    
    # Check if BGM exists
    if BGM_PATH.exists():
        # Loop BGM, lower volume to 0.12, mix with narration (volume 1.0), trim to exact total_duration
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", str(narration_path),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex",
            f"[0:a]volume=1.0[narr];[1:a]volume=0.12[bgm];[narr][bgm]amix=inputs=2:duration=first:dropout_transition=2",
            "-t", str(total_duration),
            str(mixed_audio_path)
        ]
        subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        mixed_audio_path = narration_path

    # 3. Burn subtitles & assemble final MP4
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    if not safe_title:
        safe_title = "bangla_mystery_reel"
    output_path = OUTPUT_DIR / f"{safe_title}.mp4"

    # Relative path for subtitles and fonts to prevent FFmpeg Windows drive colon escaping issues
    srt_relative = str(srt_path).replace("\\", "/")
    fonts_dir_relative = str(FONTS_DIR).replace("\\", "/")

    # Style subtitle: Yellow text with black outline, bold, centered in lower-middle safe zone (Alignment=2)
    # MarginV=280 ensures it is well above the Facebook bottom buttons (like, share, comment)
    style = (
        "Fontname=Hind Siliguri Bold,FontSize=20,"
        "PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BackColour=&H80000000,"
        "BorderStyle=1,Outline=2.5,Shadow=1,Alignment=2,MarginV=300,Bold=1"
    )

    # Use subtitles filter with font directory
    # On Windows, drive letter colon (e.g. C:) must be escaped as C\\:
    escaped_srt = srt_relative.replace(":", "\\:")
    escaped_fonts = fonts_dir_relative.replace(":", "\\:")

    vf = f"subtitles='{escaped_srt}':fontsdir='{escaped_fonts}':force_style='{style}'"

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(video_only_path),
        "-i", str(mixed_audio_path),
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        str(output_path)
    ]
    
    print(f"[VideoEngine] Rendering final reel with subtitles and audio mix...")
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[VideoEngine] Reel successfully saved to {output_path}")
    return output_path
