# -*- coding: utf-8 -*-
"""
=============================================================================
🎬 YOUTUBE MASTER VIDEO ENGINE & AUTO-SHORTS REPURPOSER (16:9 + 9:16)
=============================================================================
১. ১৬:৯ ১৯২০x১০৮০ ফুল এইচডি সিনেমাটিক ইউটিউব ডকুমেন্টারি ভিডিও রেন্ডার করে:
   - অধ্যায়ভিত্তিক সিনেমাটিক দৃশ্য ও বি-রোল ট্রানজিশন
   - অধ্যায় পরিবর্তনের সময় সাই-ফাই গ্লাস লোয়ার-থার্ড মোশন ব্যানার
   - আসল পাইথন কোড ওয়াকথ্রু ডেমো স্ক্রিন
   - জুবায়ের স্যারের আত্মবিশ্বাসী স্টুডিও ফটো ও HUD সাইবার আউটরো সিট
   - স্টুডিও ভয়েসওভার ও ব্যাকগ্রাউন্ড মিউজিক ডাকিং
২. ১-ক্লিক ৩-শর্টস রিপারপোজার:
   - মাস্টার ভিডিও থেকে ভাইরাল ৩টি সেকশন কেটে স্বয়ংক্রিয়ভাবে ৩টি ৯:১৬ ভার্টিক্যাল
     শর্টস/রিলস/টিকটক ভিডিও রেন্ডার করে।
=============================================================================
"""

import os
import sys
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import OUTPUT_DIR, TEMP_DIR, BGM_PATH

FONT_REL_PATH = "assets/fonts/HindSiliguri-Bold.ttf"
FONT_BOLD_SYS = "C:/Windows/Fonts/consolab.ttf"
FONT_MONO_SYS = "C:/Windows/Fonts/consola.ttf"
PRESENTER_IMG_PATH = ROOT_DIR / "assets" / "jubayer_dev_laptop.jpg"
TECH_CLIPS_DIR = ROOT_DIR / "assets" / "tech_clips"


def create_widescreen_watermark(w: int = 1920, h: int = 1080) -> Path:
    """১৯২০x১০৮০ ক্যানভাসের জন্য টপ-রাইট কর্নারে ওয়াটারমার্ক তৈরি করে।"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / "yt_watermark_overlay.png"
    if out_path.exists():
        return out_path

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # টপ রাইট পিল (x: 1540, y: 35, w: 340, h: 54)
    px, py, pw, ph = 1540, 35, 340, 54
    draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=14, fill=(10, 16, 30, 210), outline=(0, 240, 255, 180), width=2)
    
    font_b = ImageFont.truetype(FONT_BOLD_SYS, 22)
    draw.text((px + 20, py + 14), "</>", fill=(0, 240, 255, 255), font=font_b)
    draw.text((px + 70, py + 14), "JUBAYER.DEV | TECH LAB", fill=(240, 246, 252, 255), font=font_b)

    img.save(out_path, format="PNG")
    return out_path


def create_widescreen_code_ide(w: int = 1920, h: int = 1080) -> Path:
    """১৯২০x১০৮০ ফুল এইচডি ডার্ক মোড VS Code স্ক্রিন তৈরি করে।"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / "yt_code_ide_1080p.png"
    if out_path.exists():
        return out_path

    img = Image.new("RGBA", (w, h), "#0D1117")
    draw = ImageDraw.Draw(img)

    # টপ উইন্ডো বার
    draw.rectangle((0, 0, w, 48), fill="#161B22")
    # উইন্ডো বাটন
    draw.ellipse([(20, 16), (34, 30)], fill="#FF5F56")
    draw.ellipse([(44, 16), (58, 30)], fill="#FFBD2E")
    draw.ellipse([(68, 16), (82, 30)], fill="#27C93F")

    font_sys = ImageFont.truetype(FONT_MONO_SYS, 18)
    font_bold = ImageFont.truetype(FONT_BOLD_SYS, 20)
    font_code = ImageFont.truetype(FONT_MONO_SYS, 22)

    draw.text((w // 2 - 180, 14), "jubayer-quantum-lab — main.py (Workspace)", fill="#8B949E", font=font_sys)

    # বাম সাইডবার (ফাইল এক্সপ্লোরার)
    draw.rectangle((0, 48, 320, h), fill="#12161F", outline="#21262D", width=1)
    draw.text((25, 68), "EXPLORER", fill="#8B949E", font=font_bold)
    draw.text((25, 110), "▼ JUBAYER-QUANTUM-LAB", fill="#C9D1D9", font=font_bold)

    files = [
        ("  [py] quantum_circuit.py", "#7EE787"),
        ("  [py] shor_algorithm.py", "#58A6FF"),
        ("  [py] supercomputer_bench.py", "#C9D1D9"),
        ("  [data] telemetry_matrix.json", "#E3B341"),
        ("  [cfg] qiskit_config.yaml", "#FFA657"),
        ("  [doc] README.md", "#8B949E"),
    ]
    fy = 150
    for fn, col in files:
        draw.text((35, fy), fn, fill=col, font=font_sys)
        fy += 36

    # কোড এরিয়া ট্যাব বার
    draw.rectangle((320, 48, w, 92), fill="#1E232B")
    draw.rectangle((320, 48, 620, 92), fill="#0D1117")
    draw.line([(320, 48), (620, 48)], fill="#00F0FF", width=3)
    draw.text((345, 60), "quantum_circuit.py", fill="#F0F6FC", font=font_sys)

    draw.rectangle((625, 48, 900, 92), fill="#161B22")
    draw.text((645, 60), "shor_algorithm.py", fill="#8B949E", font=font_sys)

    # কোড লাইনস
    code_lines = [
        ("01", "#!/usr/bin/env python3", "#8B949E"),
        ("02", "# -*- coding: utf-8 -*-", "#8B949E"),
        ("03", "# Quantum State Vector Simulation Engine // By Jubayer (AI & Software Dev)", "#00F0FF"),
        ("04", "", "#000"),
        ("05", "import numpy as np", "#FF7B72"),
        ("06", "from qiskit import QuantumCircuit, Aer, execute", "#FFA657"),
        ("07", "from jubayer_core import QuantumStateEngine, TelemetryMonitor", "#FFA657"),
        ("08", "", "#000"),
        ("09", "class QuantumSuperpositionMatrix:", "#79C0FF"),
        ("10", "    def __init__(self, num_qubits: int = 128):", "#D2A8FF"),
        ("11", "        self.qubits = num_qubits", "#E6EDF3"),
        ("12", "        self.circuit = QuantumCircuit(num_qubits, num_qubits)", "#7EE787"),
        ("13", "        self.telemetry = TelemetryMonitor(lab='Jubayer AI Lab')", "#7EE787"),
        ("14", "", "#000"),
        ("15", "    def execute_parallel_calculation(self, problem_matrix: np.ndarray):", "#D2A8FF"),
        ("16", "        print(f'[QUANTUM CORE] Initializing {self.qubits} entangled qubits...')", "#A5D6FF"),
        ("17", "        self.circuit.h(range(self.qubits))  # Hadamard Gates Superposition", "#79C0FF"),
        ("18", "        result = execute(self.circuit, backend=Aer.get_backend('qasm_simulator')).result()", "#E6EDF3"),
        ("19", "        return self.telemetry.benchmark_speedup(classical_years=10000, quantum_minutes=3.2)", "#7EE787"),
        ("20", "", "#000"),
        ("21", "if __name__ == '__main__':", "#FF7B72"),
        ("22", "    engine = QuantumSuperpositionMatrix(num_qubits=256)", "#E6EDF3"),
        ("23", "    benchmark = engine.execute_parallel_calculation(np.eye(256))", "#A5D6FF"),
        ("24", "    print('[SUCCESS] Supercomputer 10,000 Year Task Solved in 3.2 Minutes!')", "#3FB950")
    ]

    cy = 115
    for num, code, color in code_lines:
        draw.text((345, cy), num, fill="#484F58", font=font_code)
        draw.text((410, cy), code, fill=color, font=font_code)
        cy += 28

    # নিচের টার্মিনাল কনসোল (x: 320 to w, y: 820 to h)
    draw.rectangle((320, 800, w, h), fill="#0A0D14", outline="#21262D", width=2)
    draw.rectangle((320, 800, w, 840), fill="#161B22")
    draw.text((340, 812), "TERMINAL  |  BASH (JUBAYER-QUANTUM-NODE-01) — 🟢 ONLINE", fill="#58A6FF", font=font_bold)

    term_lines = [
        ("root@jubayer-quantum-lab:~$ ", "#3FB950", "python3 quantum_circuit.py --accelerate --gpu-tensor", "#E6EDF3"),
        ("[QUANTUM CORE] ", "#D2A8FF", "Initializing 256 entangled qubits in absolute zero cryo-chamber...", "#8B949E"),
        ("[HADAMARD GATE] ", "#79C0FF", "Superposition active across 2^256 simultaneous quantum states", "#8B949E"),
        ("[SPEEDUP REPORT] ", "#FFA657", "Classical Supercomputer: ~10,000 Years | Quantum Engine: 00:03:12", "#FFA657"),
        ("[STATUS 200 OK] ", "#3FB950", "CALCULATION VERIFIED | Architecture Engineered by Jubayer.dev", "#3FB950")
    ]

    ty = 858
    for p, pc, t, tc in term_lines:
        draw.text((340, ty), p, fill=pc, font=font_code)
        pw = draw.textlength(p, font=font_code)
        draw.text((340 + pw, ty), t, fill=tc, font=font_code)
        ty += 38

    img.save(out_path, format="PNG")
    return out_path


def create_widescreen_outro_slate(w: int = 1920, h: int = 1080) -> Path:
    """১৯২০x১০৮০ সিনেমাটিক আউটরো সিট তৈরি করে (জুবায়ের স্যারের পোর্ট্রেট ও সোশ্যাল ব্রান্ডিং)।"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / "yt_outro_slate_1080p.png"

    img = Image.new("RGBA", (w, h), "#080C18")

    # অ্যাম্বিয়েন্ট ব্যাকগ্রাউন্ড ব্লুম
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((1100, 100, 1850, 980), fill=(0, 240, 255, 45))
    gdraw.ellipse((150, 200, 850, 900), fill=(255, 0, 110, 35))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # কর্নার ব্র্যাকেটস
    blen = 40
    for bx, by, dx, dy in [(40, 40, 1, 1), (w - 40, 40, -1, 1), (40, h - 40, 1, -1), (w - 40, h - 40, -1, -1)]:
        draw.line([(bx, by), (bx + dx * blen, by)], fill=(0, 240, 255, 240), width=3)
        draw.line([(bx, by), (bx, by + dy * blen)], fill=(0, 240, 255, 240), width=3)

    # ডান পাশে জুবায়ের স্যারের সার্কুলার HUD পোর্ট্রেট
    if PRESENTER_IMG_PATH.exists():
        p_img = Image.open(PRESENTER_IMG_PATH).convert("RGBA")
        dia = 620
        mask = Image.new("L", (dia, dia), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse([(0, 0), (dia, dia)], fill=255)

        p_resized = p_img.resize((dia, dia), Image.Resampling.LANCZOS)
        p_crop = Image.new("RGBA", (dia, dia), (0, 0, 0, 0))
        p_crop.paste(p_resized, (0, 0), mask)

        px = 1180
        py = (h - dia) // 2
        img.paste(p_crop, (px, py), p_crop)

        cx = px + dia // 2
        cy = py + dia // 2
        r_outer = dia // 2 + 10
        draw.ellipse([(cx - r_outer, cy - r_outer), (cx + r_outer, cy + r_outer)], outline=(0, 240, 255, 230), width=4)
        r_glow = dia // 2 + 18
        draw.ellipse([(cx - r_glow, cy - r_glow), (cx + r_glow, cy + r_glow)], outline=(255, 0, 110, 180), width=2)

        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            x1 = cx + int((r_outer + 5) * math.cos(rad))
            y1 = cy + int((r_outer + 5) * math.sin(rad))
            x2 = cx + int((r_outer + 16) * math.cos(rad))
            y2 = cy + int((r_outer + 16) * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=(0, 240, 255, 180), width=2)

        # নেমপ্লেট
        bw, bh = 340, 56
        bx = cx - bw // 2
        by = py + dia - 28
        draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=14, fill=(10, 16, 32, 245), outline=(0, 240, 255, 220), width=2)
        font_b = ImageFont.truetype(FONT_BOLD_SYS, 22)
        draw.text((bx + 30, by + 16), "JUBAYER // DEV & AI LAB", fill=(0, 240, 255, 255), font=font_b)

    # বাম পাশে সাবস্ক্রাইব ও আউটরো তথ্য
    draw.rounded_rectangle([(90, 160), (450, 215)], radius=12, fill=(15, 23, 42, 230), outline=(255, 0, 110, 220), width=2)
    font_bold = ImageFont.truetype(FONT_BOLD_SYS, 22)
    draw.ellipse([(110, 180), (126, 196)], fill=(255, 0, 110, 255))
    draw.text((142, 178), "OFFICIAL OUTRO // 2026", fill="#FFFFFF", font=font_bold)

    # সাবস্ক্রাইব বাটন
    draw.rounded_rectangle([(90, 680), (460, 755)], radius=16, fill="#FF0000", outline="#FFA0A0", width=2)
    font_sub = ImageFont.truetype(FONT_BOLD_SYS, 28)
    draw.text((120, 702), "SUBSCRIBE NOW", fill="#FFFFFF", font=font_sub)

    # পোর্টফোলিও লিঙ্ক পিল
    draw.rounded_rectangle([(90, 780), (560, 845)], radius=14, fill=(12, 20, 38, 230), outline=(0, 240, 255, 180), width=2)
    font_link = ImageFont.truetype(FONT_BOLD_SYS, 24)
    draw.text((120, 800), "PORTFOLIO: https://jubayer.dev", fill="#00E5FF", font=font_link)

    temp_base = TEMP_DIR / "yt_outro_base.png"
    img.convert("RGB").save(temp_base, format="PNG")

    # FFmpeg HarfBuzz দিয়ে চমৎকার বাংলা লেখা
    filters = []
    f1 = TEMP_DIR / "yt_outro_h1.txt"
    with open(f1, "w", encoding="utf-8") as f:
        f.write("প্রযুক্তির ভবিষ্যৎ দেখতে সাথে থাকুন")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_outro_h1.txt':fontsize=56:fontcolor=#FDE047:x=90:y=260")

    f2 = TEMP_DIR / "yt_outro_h2.txt"
    with open(f2, "w", encoding="utf-8") as f:
        f.write("পরবর্তী বিশেষ পর্ব মিস না করতে এখনই সাবস্ক্রাইব করুন!")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_outro_h2.txt':fontsize=36:fontcolor=#FFFFFF:x=90:y=360")

    f3 = TEMP_DIR / "yt_outro_h3.txt"
    with open(f3, "w", encoding="utf-8") as f:
        f.write("লাইক, কমেন্ট ও শেয়ার করে দেশের তরুণদের প্রযুক্তি যাত্রায় যুক্ত করুন।")
    filters.append(f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_outro_h3.txt':fontsize=28:fontcolor=#38BDF8:x=90:y=440")

    filter_chain = ",".join(filters)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_base),
        "-vf", filter_chain,
        "-frames:v", "1",
        str(out_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return out_path


def create_chapter_lower_third(chapter_id: int, title: str, w: int = 1920, h: int = 1080) -> Path:
    """অধ্যায় সূচনার প্রথম ৪-৫ সেকেন্ডে স্ক্রিনের নিচে গ্লাস লোয়ার-থার্ড ব্যানার তৈরি করে।"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEMP_DIR / f"yt_lower_third_{chapter_id}.png"

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # লোয়ার থার্ড ব্যানার বক্স (x: 70, y: 880, w: 760, h: 120)
    bx, by, bw, bh = 70, 880, 760, 120
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=16, fill=(10, 16, 32, 235), outline=(0, 240, 255, 200), width=2)
    # অ্যাকসেন্ট সাইড স্ট্রাইপ
    draw.rounded_rectangle([(bx, by), (bx + 12, by + bh)], radius=6, fill=(255, 0, 110, 255))

    # চ্যাপ্টার ট্যাগ
    font_bold = ImageFont.truetype(FONT_BOLD_SYS, 18)
    ch_label = f"CHAPTER 0{chapter_id} // JUBAYER.DEV EXCLUSIVE" if chapter_id > 0 else "PROLOGUE // JUBAYER.DEV EXCLUSIVE"
    draw.text((bx + 30, by + 18), ch_label, fill="#00F0FF", font=font_bold)

    temp_base = TEMP_DIR / f"yt_lt_base_{chapter_id}.png"
    img.save(temp_base, format="PNG")

    # বাংলা শিরোনাম টেক্সট হার্ফবাজ দিয়ে বসানো
    f_title = TEMP_DIR / f"yt_lt_txt_{chapter_id}.txt"
    with open(f_title, "w", encoding="utf-8") as f:
        f.write(title)

    filter_str = f"drawtext=fontfile='{FONT_REL_PATH}':textfile='temp/yt_lt_txt_{chapter_id}.txt':fontsize=34:fontcolor=#FFFFFF:x={bx + 30}:y={by + 52}"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_base),
        "-vf", filter_str,
        "-frames:v", "1",
        str(out_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return out_path


def render_scene_segment(scene: dict, out_segment_path: Path):
    """একটি নির্দিষ্ট সিনের জন্য ভিডিও ক্লিপ, জুমিং ও লোয়ার থার্ড ব্যানার তৈরি করে।"""
    clip_name = scene["clip"]
    dur = scene["duration"]
    ch_id = scene["chapter_id"]
    ch_title = scene["chapter_title"]

    watermark_path = create_widescreen_watermark()
    is_chapter_start = (scene["scene_id"] == 1 or scene["text"].startswith("অধ্যায়") or "ভূমিকা" in ch_title)

    # ভিডিও সোর্স বা ইমেজ নির্ধারণ
    if clip_name == "code_walkthrough":
        src_path = create_widescreen_code_ide()
        is_image = True
    elif clip_name == "outro_slate":
        src_path = create_widescreen_outro_slate()
        is_image = True
    else:
        src_path = TECH_CLIPS_DIR / clip_name
        if not src_path.exists():
            # ফলব্যাক
            src_path = TECH_CLIPS_DIR / "quantum_server_room.mp4"
        is_image = False

    show_lt = scene.get("is_chapter_first_scene", False)

    # লোয়ার থার্ড ব্যানার
    if show_lt:
        lt_path = create_chapter_lower_third(ch_id, ch_title)

    # এফএফএমপেক ফিল্টার চেইন
    if is_image:
        if show_lt:
            filter_complex = (
                f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[v0];"
                f"[1:v]scale=1920:1080[wm];"
                f"[v0][wm]overlay=0:0[v1];"
                f"[2:v]scale=1920:1080[lt];"
                f"[v1][lt]overlay=0:0:enable='between(t,0,4.5)'[outv]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(src_path),
                "-i", str(watermark_path),
                "-i", str(lt_path),
                "-t", str(dur),
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-r", "30",
                str(out_segment_path)
            ]
        else:
            filter_complex = (
                f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[v0];"
                f"[1:v]scale=1920:1080[wm];"
                f"[v0][wm]overlay=0:0[outv]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(src_path),
                "-i", str(watermark_path),
                "-t", str(dur),
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-r", "30",
                str(out_segment_path)
            ]
    else:
        if show_lt:
            filter_complex = (
                f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[v0];"
                f"[1:v]scale=1920:1080[wm];"
                f"[v0][wm]overlay=0:0[v1];"
                f"[2:v]scale=1920:1080[lt];"
                f"[v1][lt]overlay=0:0:enable='between(t,0,4.5)'[outv]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1", "-i", str(src_path),
                "-i", str(watermark_path),
                "-i", str(lt_path),
                "-t", str(dur),
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-r", "30",
                str(out_segment_path)
            ]
        else:
            filter_complex = (
                f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[v0];"
                f"[1:v]scale=1920:1080[wm];"
                f"[v0][wm]overlay=0:0[outv]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1", "-i", str(src_path),
                "-i", str(watermark_path),
                "-t", str(dur),
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-r", "30",
                str(out_segment_path)
            ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def render_master_youtube_video(doc_data: dict, voice_data: dict, out_path: Path = None) -> Path:
    """
    সমস্ত সিনের ভিডিও সেগমেন্ট তৈরি করে, তাদের জোড়া লাগিয়ে পূর্ণাঙ্গ ১৬:৯ ফুল এইচডি
    ইউটিউব ডকুমেন্টারি ভিডিও রেন্ডার করে।
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if out_path is None:
        out_path = OUTPUT_DIR / "youtube_master_documentary.mp4"

    scenes = voice_data["scene_timings"]
    total_scenes = len(scenes)
    print(f"[YouTubeMaker] মোট {total_scenes} টি দৃশ্য রেন্ডারিং শুরু হচ্ছে...")

    segment_files = []
    for i, sc in enumerate(scenes, start=1):
        seg_p = TEMP_DIR / f"yt_seg_{i}.mp4"
        print(f"  ▶ [Scene {i}/{total_scenes}] {sc['chapter_title']} ({sc['duration']:.1f}s) - {sc['clip']}")
        render_scene_segment(sc, seg_p)
        segment_files.append(seg_p)

    # কনক্যাট টেক্সট ফাইল তৈরি
    concat_txt = TEMP_DIR / "yt_video_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in segment_files:
            f.write("file '" + p.resolve().as_posix() + "'\n")

    temp_raw_video = TEMP_DIR / "yt_video_raw_visual.mp4"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(temp_raw_video)
    ]
    subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # অডিও মিক্সিং (স্টুডিও ভয়েসওভার + ডাকড ব্যাকগ্রাউন্ড মিউজিক)
    narration_path = voice_data["full_narration_path"]
    total_dur = voice_data["total_duration"]

    print(f"[YouTubeMaker] ভিডিও ও ব্যাকগ্রাউন্ড মিউজিক মাস্টারিং হচ্ছে (দৈর্ঘ্য: {total_dur:.1f}s)...")

    # BGM -22dB ডাকড এবং শেষের দিকে ফেইড আউট
    audio_filter = (
        f"[1:a]volume=1.0[v_voice];"
        f"[2:a]volume=0.10,afade=t=in:ss=0:d=2,afade=t=out:st={max(0, total_dur - 4)}:d=4[v_bgm];"
        f"[v_voice][v_bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]"
    )

    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(temp_raw_video),
        "-i", str(narration_path),
        "-stream_loop", "-1", "-i", str(BGM_PATH),
        "-filter_complex", audio_filter,
        "-map", "0:v",
        "-map", "[outa]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_dur),
        str(out_path)
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[YouTubeMaker] ✅ মাস্টার ভিডিও সফলভাবে তৈরি হয়েছে: {out_path} ({out_path.stat().st_size / (1024*1024):.1f} MB)")
    return out_path


def repurpose_shorts_from_master(master_video_path: Path, viral_shorts: list, scene_timings: list) -> list:
    """
    মাস্টার ১৬:৯ ভিডিও থেকে নির্দিষ্ট ভাইরাল অংশগুলো কেটে ৯:১৬ সাইজের ৩টি আলাদা শর্টস ভিডিও তৈরি করে।
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    created_shorts = []

    for v_short in viral_shorts:
        label = v_short["short_label"]
        ch_id = v_short["chapter_id"]
        ch_title = v_short["chapter_title"]

        # সিনের শুরু ও শেষ সময় বের করা
        ch_scenes = [s for s in scene_timings if s["chapter_id"] == ch_id]
        if not ch_scenes:
            continue

        start_time = ch_scenes[0]["start"]
        end_time = ch_scenes[-1]["end"]
        duration = end_time - start_time

        out_short_path = OUTPUT_DIR / f"{label}.mp4"
        print(f"[AutoShorts] রেন্ডার হচ্ছে: {label} (সময়সীমা: {start_time:.1f}s - {end_time:.1f}s, মোট: {duration:.1f}s)...")

        # ১৬:৯ থেকে ৯:১৬ কনভার্সন ফিল্টার (সেন্টার ক্রপ এবং টপ/বটম টেক্সট ব্যান্ড)
        # crop=ih*9/16:ih:iw/2-ow/2:0, scale=1080:1920
        # এবং টপ ও বটমে ব্র্যান্ডিং ব্যাজ
        short_filter = (
            f"crop=ih*9/16:ih:iw/2-ow/2:0,scale=1080:1920,"
            f"drawbox=y=0:h=160:color=black@0.65:t=fill,"
            f"drawtext=fontfile='{FONT_REL_PATH}':text='</> JUBAYER.DEV // VIRAL SHORT':fontsize=36:fontcolor=#00F0FF:x=(w-text_w)/2:y=60,"
            f"drawbox=y=1740:h=180:color=black@0.70:t=fill,"
            f"drawtext=fontfile='{FONT_REL_PATH}':text='সম্পূর্ণ ভিডিও ইউটিউবে দেখুন':fontsize=36:fontcolor=#FDE047:x=(w-text_w)/2:y=1800"
        )

        cmd_short = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", str(master_video_path),
            "-t", str(duration),
            "-vf", short_filter,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            str(out_short_path)
        ]
        subprocess.run(cmd_short, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"[AutoShorts] ✅ প্রস্তুত: {out_short_path} ({out_short_path.stat().st_size / (1024*1024):.1f} MB)")
        created_shorts.append(out_short_path)

    return created_shorts


if __name__ == "__main__":
    print("=" * 60)
    print("🎬 [TEST] ইউটিউব মাস্টার মেকার উপাদান পরীক্ষা")
    print("=" * 60)
    p_wm = create_widescreen_watermark()
    p_code = create_widescreen_code_ide()
    p_outro = create_widescreen_outro_slate()
    p_lt = create_chapter_lower_third(1, "কিউবিট ও কোয়ান্টাম মেকানিক্সের রহস্য")
    print(f"✅ ওয়াটারমার্ক: {p_wm.name}")
    print(f"✅ কোড IDE স্ক্রিন: {p_code.name}")
    print(f"✅ আউটরো সিট: {p_outro.name}")
    print(f"✅ চ্যাপ্টার লোয়ার-থার্ড: {p_lt.name}")
