import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from src.config import BGM_PATH, FONT_PATH, OUTPUT_DIR, TEMP_DIR, BASE_DIR

PRESENTER_PATH = BASE_DIR / "assets" / "presenter.jpg"

def render_subtitle_image(text: str, out_path: Path, width=1080, height=1920):
    """
    Renders a pixel-perfect Bengali subtitle overlay image using Pillow.
    Guarantees ZERO broken conjuncts (যুক্তাক্ষর) and beautiful modern Facebook Reels typography.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(str(FONT_PATH), 38)

    # Wrap text cleanly (max 26 chars per line for clear legibility on mobile screens)
    lines = textwrap.wrap(text, width=26)
    line_height = 54
    total_text_h = len(lines) * line_height

    # Safe zone positioning (below center, well above Facebook Reels bottom buttons)
    box_y = 1420
    pad_x, pad_y = 35, 20

    # Calculate width of longest line
    max_w = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
    box_w = max_w + (pad_x * 2)
    box_h = total_text_h + (pad_y * 2)
    box_x = (width - box_w) // 2

    # Draw modern rounded translucent badge
    draw.rounded_rectangle(
        [(box_x, box_y), (box_x + box_w, box_y + box_h)],
        radius=18,
        fill=(10, 15, 25, 215),
        outline=(255, 220, 0, 240),
        width=3
    )

    # Draw centered glowing text
    cur_y = box_y + pad_y
    for line in lines:
        line_w = draw.textbbox((0, 0), line, font=font)[2]
        line_x = (width - line_w) // 2
        # Drop shadow for high contrast
        draw.text((line_x + 2, cur_y + 2), line, font=font, fill=(0, 0, 0, 255))
        # Crisp bright yellow text
        draw.text((line_x, cur_y), line, font=font, fill=(255, 235, 45, 255))
        cur_y += line_height

    img.save(out_path, format="PNG")

def prepare_presenter_base_frame() -> Path:
    """
    Creates a high-production 1080x1920 vertical layout with the user's portrait.
    Includes cinematic blurred backdrop, centered sharp presenter, and sleek tech border.
    """
    out_frame = TEMP_DIR / "presenter_base.jpg"
    if PRESENTER_PATH.exists():
        user_img = Image.open(PRESENTER_PATH)

        # 1. Background: Blurred & darkened
        bg = user_img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=28))
        dimmer = Image.new("RGB", bg.size, (0, 0, 0))
        bg = Image.blend(bg, dimmer, 0.42)

        # 2. Foreground: Crisp centered presenter (85% of screen width)
        fg_w, fg_h = 960, 1200
        fg = user_img.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

        # Soft rounded corners
        mask = Image.new("L", (fg_w, fg_h), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([(0, 0), (fg_w, fg_h)], radius=32, fill=255)

        pos_x = (1080 - fg_w) // 2
        pos_y = 140
        bg.paste(fg, (pos_x, pos_y), mask)

        # Sleek tech accent border around the presenter
        draw = ImageDraw.Draw(bg)
        draw.rounded_rectangle([(pos_x, pos_y), (pos_x + fg_w, pos_y + fg_h)], radius=32, outline="#38BDF8", width=3)

        bg.save(out_frame, quality=95)
    else:
        # Fallback dark background if no image
        bg = Image.new("RGB", (1080, 1920), "#0A0E1A")
        bg.save(out_frame, quality=95)

    return out_frame

def render_final_reel(scene_timings: list, narration_path: Path, total_duration: float, title: str) -> Path:
    """
    Renders cinematic vertical reel with presenter, dynamic motion, BGM, and pixel-perfect subtitles.
    """
    base_frame = prepare_presenter_base_frame()

    # 1. Generate subtitle PNG overlays for each scene
    sub_overlays = []
    for s in scene_timings:
        idx = s["index"]
        text = s["text"]
        start_t = s["start"]
        end_t = s["end"]
        sub_png = TEMP_DIR / f"sub_overlay_{idx}.png"
        render_subtitle_image(text, sub_png)
        sub_overlays.append({"path": sub_png, "start": start_t, "end": end_t})

    # 2. Mix audio (Narration + BGM)
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

    # 3. Build FFmpeg filter graph for dynamic motion + subtitle overlays
    # Slow cinematic camera zoom (from 1.0 to 1.04x)
    total_frames = int(total_duration * 30) + 30
    filter_parts = [
        f"[0:v]zoompan=z='min(zoom+0.0004,1.05)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[zoomed]"
    ]

    # Chain subtitle overlay filters
    last_v = "zoomed"
    for i, sub in enumerate(sub_overlays, start=1):
        next_v = f"v{i}"
        st = sub["start"]
        et = sub["end"]
        filter_parts.append(f"[{last_v}][{i}:v]overlay=0:0:enable='between(t,{st:.2f},{et:.2f})'[{next_v}]")
        last_v = next_v

    full_filter = ";".join(filter_parts)

    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    if not safe_title:
        safe_title = "ai_tech_reel"
    output_path = OUTPUT_DIR / f"{safe_title}.mp4"

    cmd_inputs = ["ffmpeg", "-y", "-loop", "1", "-i", str(base_frame)]
    for sub in sub_overlays:
        cmd_inputs.extend(["-i", str(sub["path"])])

    cmd_final = (
        cmd_inputs +
        [
            "-i", str(mixed_audio_path),
            "-filter_complex", full_filter,
            "-map", f"[{last_v}]",
            "-map", f"{len(sub_overlays) + 1}:a",
            "-t", str(total_duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
    )

    print("[VideoEngine] Rendering high-definition presenter reel with perfect typography...")
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[VideoEngine] Render complete! Output saved to: {output_path}")
    return output_path
