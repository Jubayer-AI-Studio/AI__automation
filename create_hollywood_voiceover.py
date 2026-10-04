import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import asyncio
import subprocess
from pathlib import Path
import edge_tts

scenes = [
    {
        "id": 1,
        "clip": "cybernetic_tech.mp4",
        "text": "অনেকে ভাবে সফটওয়্যার মানে শুধুই স্ক্রিনের কিছু কোড। কিন্তু কোড যখন মেটালের সাথে কানেক্ট হয়, তখনই শুরু হয় আসল রোবোটিক্স।",
        "sub_bn": "কোড যখন মেটালের সাথে কানেক্ট হয়, তখনই আসল রোবোটিক্স!",
        "sub_en": "When Code Connects to Metal, True Robotics Begins."
    },
    {
        "id": 2,
        "clip": "soldering.mp4",
        "text": "মাইক্রোচিপ, সেন্সর আর নিখুঁত সার্কিট ডিজাইনে আমরা তৈরি করি মেশিনের স্নায়ুতন্ত্র।",
        "sub_bn": "মাইক্রোচিপ ও সার্কিট ডিজাইনে মেশিনের স্নায়ুতন্ত্র!",
        "sub_en": "Precision Microchips: Engineering The Neural Core."
    },
    {
        "id": 3,
        "clip": "cnc_laser_welding.mp4",
        "text": "আয়রন ম্যান স্টাইল স্বয়ংক্রিয় রোবোটিক মেকানিক্স আর লেজার প্রিসিশন—যেখানে মিলিমিটারের নির্ভুলতায় জন্ম নেয় ফিউচার হার্ডওয়্যার।",
        "sub_bn": "আয়রন ম্যান স্টাইল রোবোটিক মেকানিক্স ও লেজার প্রিসিশন!",
        "sub_en": "Iron Man Style Robotic Mechanics & Laser Precision."
    },
    {
        "id": 4,
        "clip": "robotic_assembly.mp4",
        "text": "সফটওয়্যার আর হার্ডওয়্যারের এই পাওয়ারফুল ফিউশনই তৈরি করছে স্বয়ংক্রিয় ভবিষ্যত।",
        "sub_bn": "সফটওয়্যার ও হার্ডওয়্যার ফিউশন—স্বয়ংক্রিয় ভবিষ্যত!",
        "sub_en": "Software & Hardware Fusion: The Autonomous Future."
    },
    {
        "id": 5,
        "clip": "outro",
        "text": "আই এম জুবায়ের—ওয়েলকাম টু মাই এআই অ্যান্ড রোবোটিক্স ল্যাব!",
        "sub_bn": "Jubayer.dev // এআই ও রোবোটিক্স ল্যাব",
        "sub_en": "JUBAYER.DEV | Building Next-Gen Autonomous AI"
    }
]

async def generate_scene_audio(sc, idx):
    out_mp3 = Path(f"temp/voice_scene_{idx}.mp3")
    comm = edge_tts.Communicate(
        text=sc["text"],
        voice="bn-IN-BashkarNeural",
        rate="+12%",
        pitch="+2Hz"
    )
    await comm.save(str(out_mp3))
    
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(out_mp3)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    dur = float(res.stdout.strip())
    sc["audio_path"] = out_mp3
    sc["duration"] = dur
    print(f"Scene {idx} ({sc['clip']}): {dur:.2f}s -> {sc['text']}")

async def main():
    for i, sc in enumerate(scenes, 1):
        await generate_scene_audio(sc, i)

if __name__ == "__main__":
    asyncio.run(main())
