import os
import requests
import subprocess
from pathlib import Path
from src.config import PEXELS_API_KEY, TEMP_DIR

def fetch_stock_video_pexels(query: str, output_path: Path) -> bool:
    """
    Search and download a vertical 9:16 HD stock video from Pexels API.
    Pexels API is 100% free (200 requests/hour, 20,000/month).
    """
    if not PEXELS_API_KEY:
        print("[Footage] PEXELS_API_KEY not set. Will use atmospheric procedural background.")
        return False

    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&size=medium&per_page=5"

    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            videos = data.get("videos", [])
            for video in videos:
                video_files = video.get("video_files", [])
                for vf in video_files:
                    if vf.get("width") and vf.get("height") and vf["height"] > vf["width"]:
                        link = vf.get("link")
                        if link:
                            print(f"[Footage] Downloading stock video for '{query}'...")
                            v_res = requests.get(link, stream=True, timeout=30)
                            if v_res.status_code == 200:
                                with open(output_path, "wb") as f:
                                    for chunk in v_res.iter_content(chunk_size=1024 * 1024):
                                        f.write(chunk)
                                return True
    except Exception as e:
        print(f"[Footage] Pexels download error for '{query}': {e}")
    return False

def generate_fallback_procedural_clip(duration: float, output_path: Path, scene_index: int):
    """
    Generates an atmospheric dark mystery gradient with subtle vignette.
    Super fast and produces compact, high quality 9:16 vertical clips.
    """
    # Palette of dark mysterious shades (dark navy, deep crimson/purple, obsidian, dark cyan)
    palettes = ["#080e14", "#120a1c", "#081b24", "#180f08", "#0d1b1e"]
    color = palettes[(scene_index - 1) % len(palettes)]

    # Clean dark vignette filter
    vf = f"color=c={color}:s=1080x1920:d={duration},vignette=PI/4,fps=30"
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", vf,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
        "-t", str(duration), "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def prepare_scene_footage(scene_timings: list) -> list:
    """
    Ensures each scene has a vertical video clip of the exact required duration.
    """
    clip_paths = []
    for scene in scene_timings:
        i = scene["index"]
        duration = scene["duration"]
        query = scene["query"]
        raw_clip = TEMP_DIR / f"raw_clip_{i}.mp4"
        ready_clip = TEMP_DIR / f"scene_clip_{i}.mp4"

        downloaded = fetch_stock_video_pexels(query, raw_clip)
        if downloaded and raw_clip.exists():
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
            cmd = [
                "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(raw_clip),
                "-vf", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "22",
                "-t", str(duration), "-an", "-pix_fmt", "yuv420p",
                str(ready_clip)
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            generate_fallback_procedural_clip(duration, ready_clip, i)

        clip_paths.append(ready_clip)
    return clip_paths
