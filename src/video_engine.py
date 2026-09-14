import os
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.config import BGM_PATH, FONT_PATH, OUTPUT_DIR, TEMP_DIR, BASE_DIR

PRESENTER_IMG_PATH = BASE_DIR / "assets" / "presenter.jpg"
REAL_TECH_CLIP = BASE_DIR / "assets" / "tech_clip_1.mp4"

def prepare_circular_presenter_badge() -> Path:
    badge_path = TEMP_DIR / "presenter_badge.png"
    if badge_path.exists():
        return badge_path

    if not PRESENTER_IMG_PATH.exists():
        img = Image.new("RGBA", (404, 404), (0, 0, 0, 0))
        img.save(badge_path)
        return badge_path

    user_img = Image.open(PRESENTER_IMG_PATH).convert("RGBA")
    w, h = user_img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = 30
    crop_box = (left, top, left + min_dim, top + min_dim)
    cropped = user_img.crop(crop_box).resize((380, 380), Image.Resampling.LANCZOS)

    mask = Image.new("L", (380, 380), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 380, 380), fill=255)

    circular_fg = Image.new("RGBA", (380, 380), (0, 0, 0, 0))
    circular_fg.paste(cropped, (0, 0), mask)

    ring_img = Image.new("RGBA", (404, 404), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_img)
    ring_draw.ellipse((2, 2, 402, 402), outline="#00F0FF", width=6)
    ring_img.paste(circular_fg, (12, 12), circular_fg)

    font_path = "C:/Windows/Fonts/Nirmala.ttc" if os.path.exists("C:/Windows/Fonts/Nirmala.ttc") else str(FONT_PATH)
    font_tag = ImageFont.truetype(font_path, 22)
    draw_badge = ImageDraw.Draw(ring_img)
    badge_box = [(82, 355), (322, 395)]
    draw_badge.rounded_rectangle(badge_box, radius=12, fill="#0F172A", outline="#38BDF8", width=2)
    draw_badge.text((105, 362), "Jubayer | Tech AI", font=font_tag, fill="#FFFFFF")

    ring_img.save(badge_path, format="PNG")
    return badge_path

def generate_dynamic_tech_bg(duration: float, output_path: Path):
    """Prepares real moving 1080x1920 tech video background."""
    if REAL_TECH_CLIP.exists():
        # Scale & crop 16:9 clip to 9:16 vertical 1080x1920 with high contrast
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.15:brightness=-0.05"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", str(REAL_TECH_CLIP),
            "-vf", vf,
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-an",
            str(output_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # Fallback fast gradients
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"gradients=s=1080x1920:d={duration}:c0=0x081128:c1=0x1a0928:speed=0.005",
            "-vf", "vignette=PI/4",
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            str(output_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    # 1. Real moving video background
    bg_video_path = TEMP_DIR / "dynamic_bg.mp4"
    generate_dynamic_tech_bg(total_duration, bg_video_path)

    # 2. Presenter badge
    badge_path = prepare_circular_presenter_badge()

    # 3. Audio mix
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

    # 4. Bengali subtitle text with HarfBuzz
    font_file = "assets/fonts/HindSiliguri-Bold.ttf"
    filter_chains = [
        "[0:v]scale=1080:1920[bg]",
        "[bg][1:v]overlay=620:1440[v_base]"
    ]

    last_v = "v_base"
    for i, scene in enumerate(scene_timings, start=1):
        wrapped = "\n".join(textwrap.wrap(scene["text"], width=24))
        scene_rel_path = f"temp/sub_txt_{i}.txt"
        scene_full_path = TEMP_DIR / f"sub_txt_{i}.txt"
        with open(scene_full_path, "w", encoding="utf-8") as f:
            f.write(wrapped)

        st = scene["start"]
        et = scene["end"]
        next_v = f"v_sub_{i}"

        dt_filter = (
            f"drawtext=fontfile='{font_file}':textfile='{scene_rel_path}':"
            "fontsize=52:fontcolor=yellow:borderw=4:bordercolor=black:"
            "box=1:boxcolor=black@0.75:boxborderw=20:line_spacing=18:"
            f"x=(w-text_w)/2:y=760:enable='between(t,{st:.2f},{et:.2f})'"
        )
        filter_chains.append(f"[{last_v}]{dt_filter}[{next_v}]")
        last_v = next_v

    full_filter = ";".join(filter_chains)

    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    if not safe_title:
        safe_title = "ai_tech_reel"
    output_path = OUTPUT_DIR / f"{safe_title}.mp4"

    cmd_final = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(bg_video_path),
        "-i", str(badge_path),
        "-i", str(mixed_audio_path),
        "-filter_complex", full_filter,
        "-map", f"[{last_v}]",
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

    print("[VideoEngine] Rendering real video background presenter reel...")
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[VideoEngine] Render complete! Video saved to: {output_path}")
    return output_path
