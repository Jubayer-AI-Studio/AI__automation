import sys
import os
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from pathlib import Path
from src.script_engine import get_reel_content, get_daily_extras
from src.audio_engine import generate_voiceover_and_subtitles
from src.footage_engine import prepare_scene_footage
from src.video_engine import render_final_reel
from src.image_engine import create_ai_photocard
from src.telegram_engine import send_full_creator_kit

def run_pipeline():
    start_time = time.time()
    print("==================================================")
    print("🚀 ফেসবুক এআই ও টেক কনটেন্ট কিট জেনারেটর শুরু হচ্ছে...")
    print("==================================================")

    # 1. টপিক ও স্ক্রিপ্ট তৈরি (এআই ও ফিউচার টেক ফোকাসড)
    print("\n[১/৬] এআই ও টেক স্ক্রিপ্ট প্ল্যান তৈরি হচ্ছে...")
    content = get_reel_content()
    title = content["title"]
    scenes = content["scenes"]
    caption = content["caption"]
    hashtags = content["hashtags"]
    print(f"🤖 নির্বাচিত এআই টপিক: {title}")
    print(f"📄 মোট সিনের সংখ্যা: {len(scenes)}")

    # 2. বাংলা ভয়েসওভার ও সাবটাইটেল তৈরি
    print("\n[২/৬] Edge-TTS দিয়ে প্রাকৃতিক বাংলা ভয়েসওভার তৈরি হচ্ছে...")
    audio_data = generate_voiceover_and_subtitles(scenes)
    narration_path = audio_data["narration_path"]
    srt_path = audio_data["srt_path"]
    total_duration = audio_data["total_duration"]
    scene_timings = audio_data["scene_timings"]
    print(f"🎙️ মোট অডিও দৈর্ঘ্য: {total_duration:.2f} সেকেন্ড")

    # 3. স্টক ফুটেজ সংগ্রহ
    print("\n[৩/৬] প্রাসঙ্গিক ৯:১৬ টেক ও ফিউচারিস্টিক ফুটেজ প্রস্তুত করা হচ্ছে...")
    clip_paths = prepare_scene_footage(scene_timings)
    print(f"🎥 প্রস্তুতকৃত ক্লিপ সংখ্যা: {len(clip_paths)}")

    # 4. ফাইনাল রিলস রেন্ডারিং
    print("\n[৪/৬] অডিও, ভিডিও, ব্যাকগ্রাউন্ড মিউজিক ও বাংলা সাবটাইটেল যুক্ত করা হচ্ছে...")
    output_video_path = render_final_reel(
        clip_paths=clip_paths,
        narration_path=narration_path,
        srt_path=srt_path,
        total_duration=total_duration,
        title=title
    )
    print(f"✅ এআই রিলস তৈরি সম্পন্ন: {output_video_path}")

    # 5. অতিরিক্ত কনটেন্ট তৈরি (ফটো কার্ড, টেক্সট পোস্ট ও স্টোরি পোল)
    print("\n[৫/৬] ফেসবুক ফিডের জন্য এআই ফটো কার্ড ও ডিসকাশন পোস্ট তৈরি হচ্ছে...")
    extras = get_daily_extras()
    card_info = extras["photo_card"]
    photo_card_path = create_ai_photocard(
        title=card_info["title"],
        points=card_info["points"],
        category=card_info["category"]
    )
    print(f"🖼️ ফটো কার্ড তৈরি সম্পন্ন: {photo_card_path}")

    # 6. টেলিগ্রামে ফুল ক্রিয়েটর কিট পাঠানো
    print("\n[৬/৬] মোবাইলের টেলিগ্রামে সম্পূর্ণ ডেইলি কিট পাঠানো হচ্ছে...")
    sent = send_full_creator_kit(
        video_path=output_video_path,
        title=title,
        caption=caption,
        hashtags=hashtags,
        photo_card_path=photo_card_path,
        extras=extras
    )

    elapsed = time.time() - start_time
    print("==================================================")
    print(f"🎉 সমস্ত কাজ সফলভাবে সম্পন্ন হয়েছে ({elapsed:.1f} সেকেন্ডে)!")
    if sent:
        print("📲 আপনার ফোনের Telegram চেক করুন! ভিডিও, ফটো কার্ড ও পোস্ট পৌঁছে গেছে।")
    else:
        print(f"📂 ভিডিও সংরক্ষিত: {output_video_path}")
        print(f"📂 ফটো কার্ড সংরক্ষিত: {photo_card_path}")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()
