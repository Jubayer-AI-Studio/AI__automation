# -*- coding: utf-8 -*-
"""
=============================================================================
🚀 YOUTUBE MASTER ENGINE & CREATOR SUITE RUNNER
=============================================================================
এই স্ক্রিপ্টটি সম্পূর্ণ পাইপলাইন পরিচালনা করে:
  ১. ৫-৭ মিনিটের গভীর টেকনিক্যাল স্ক্রিপ্ট ও চ্যাপ্টার মার্কার তৈরি
  ২. স্টুডিও কোয়ালিটি ভয়েসওভার ও টাইমস্ট্যাম্প গণনা
  ৩. ১২৮০x৭২০ হাই-সিটিআর ইউটিউব থাম্বনেইল জেনারেটর
  ৪. ১৬:৯ ১৯২০x১০৮০ ফুল এইচডি মাস্টার ডকুমেন্টারি ভিডিও রেন্ডারিং
  ৫. মাস্টার থেকে ৩টি ৯:১৬ ভাইরাল শর্টস/রিলস রিপারপোজিং
  ৬. জুবায়ের স্যারের টেলিগ্রাম বটে (@myai_reel_bot) সম্পূর্ণ ক্রিয়েটর কিট ডেলিভারি
=============================================================================
"""

import os
import sys
import time
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, OUTPUT_DIR
from youtube_production.longform_script_writer import get_longform_script
from youtube_production.longform_voice_engine import generate_longform_voiceover
from youtube_production.youtube_thumbnail_maker import generate_youtube_thumbnail
from youtube_production.youtube_maker import render_master_youtube_video, repurpose_shorts_from_master

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_telegram_msg(text: str):
    """টেলিগ্রামে টেক্সট মেসেজ পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=25
        )
    except Exception as e:
        print(f"[Telegram] মেসেজ পাঠানোতে ত্রুটি: {e}")


def send_telegram_photo(photo_path: Path, caption: str):
    """টেলিগ্রামে ছবি বা থাম্বনেইল পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not photo_path.exists():
        return
    try:
        with open(photo_path, "rb") as pf:
            requests.post(
                f"{BASE_URL}/sendPhoto",
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]},
                files={"photo": pf},
                timeout=60
            )
    except Exception as e:
        print(f"[Telegram] ফটো পাঠানোতে ত্রুটি: {e}")


def send_telegram_video(video_path: Path, caption: str):
    """টেলিগ্রামে ভিডিও ফাইল পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not video_path.exists():
        return
    
    file_size_mb = video_path.stat().st_size / (1024 * 1024)
    if file_size_mb > 49.5:
        print(f"[Telegram] ভিডিও ফাইলটি {file_size_mb:.1f} MB (টেলিগ্রাম বট লিমিট ৫০ MB এর বেশি)। লোকাল লিঙ্ক পাঠানো হচ্ছে...")
        send_telegram_msg(
            f"⚠️ <b>মাস্টার ভিডিও ফাইল সাইজ:</b> {file_size_mb:.1f} MB (টেলিগ্রাম বট লিমিট ৫০ MB এর বেশি)\n"
            f"📁 <b>পিসিতে সংরক্ষিত ফাইল:</b>\n<code>{video_path}</code>\n\n"
            f"💡 <i>ভার্টিক্যাল শর্টসগুলো নিচে সরাসরি পাঠিয়ে দেওয়া হচ্ছে।</i>"
        )
        return

    try:
        with open(video_path, "rb") as vf:
            requests.post(
                f"{BASE_URL}/sendVideo",
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024], "supports_streaming": True},
                files={"video": vf},
                timeout=180
            )
    except Exception as e:
        print(f"[Telegram] ভিডিও পাঠানোতে ত্রুটি: {e}")


def run_full_youtube_pipeline(doc_index: int = 0):
    start_time = time.time()
    print("=" * 70)
    print("🎬 JUBAYER.DEV YOUTUBE LONG-FORM & SHORTS PRODUCTION ENGINE")
    print("=" * 70)

    # ১. স্ক্রিপ্ট জেনারেশন
    print("\n[Step 1/5] স্ক্রিপ্ট ও চ্যাপ্টার মেটাডাটা তৈরি হচ্ছে...")
    doc = get_longform_script(doc_index)
    print(f"  ▶ শিরোনাম: {doc['title']}")
    print(f"  ▶ অধ্যায় সংখ্যা: {len(doc['chapters'])} টি | মোট দৃশ্য: {len(doc['all_scenes'])} টি")

    # ২. স্টুডিও ভয়েসওভার সিন্থেসিস
    print("\n[Step 2/5] স্টুডিও কোয়ালিটি ভয়েসওভার ও অডিও মাস্টারিং হচ্ছে...")
    voice_data = generate_longform_voiceover(doc["all_scenes"])
    print(f"  ▶ অডিও তৈরি সম্পন্ন! মোট সময়সীমা: {voice_data['total_duration']:.1f} সেকেন্ড")

    # ৩. হাই-সিটিআর থাম্বনেইল তৈরি
    print("\n[Step 3/5] ১২৮০x৭২০ হাই-সিটিআর থাম্বনেইল তৈরি হচ্ছে...")
    thumb_path = generate_youtube_thumbnail(
        title=doc["title"],
        short_title=doc["short_title"],
        theme=doc["theme"]
    )

    # ৪. ১৬:৯ মাস্টার ভিডিও রেন্ডারিং
    print("\n[Step 4/5] ১৯২০x১০৮০ ফুল এইচডি মাস্টার ভিডিও কম্পোজিশন...")
    master_video_path = render_master_youtube_video(doc, voice_data)

    # ৫. ৯:১৬ অটো-শর্টস রিপারপোজার
    print("\n[Step 5/5] মাস্টার ভিডিও থেকে ৩টি ভার্টিক্যাল শর্টস রিপারপোজিং...")
    short_paths = repurpose_shorts_from_master(
        master_video_path,
        doc["viral_shorts"],
        voice_data["scene_timings"]
    )

    total_elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"🎉 সম্পূর্ণ পাইপলাইন সফলভাবে সম্পন্ন হয়েছে! মোট সময় লেগেছে: {total_elapsed:.1f} সেকেন্ড")
    print("=" * 70)

    # ৬. টেলিগ্রামে ডেলিভারি
    print("\n📲 জুবায়ের স্যারের টেলিগ্রামে ক্রিয়েটর কিট পাঠানো হচ্ছে...")
    
    # নোটিফিকেশন
    notify_text = (
        f"🎬 <b>Jubayer.dev YouTube Studio Kit Ready!</b>\n\n"
        f"📌 <b>মূল ভিডিও:</b> {doc['title']}\n"
        f"⏱️ <b>দৈর্ঘ্য:</b> {voice_data['total_duration'] / 60:.1f} মিনিট ({voice_data['total_duration']:.0f}s)\n"
        f"✂️ <b>রিপারপোজড শর্টস:</b> {len(short_paths)} টি (TikTok, Reels, Shorts রেডি)\n"
        f"🖼️ <b>থাম্বনেইল:</b> 1280x720 High-CTR Cyber Neon"
    )
    send_telegram_msg(notify_text)

    # থাম্বনেইল ও এসইও ডেসক্রিপশন
    thumb_caption = (
        f"🖼️ <b>YouTube High-CTR Thumbnail (1280x720)</b>\n\n"
        f"<b>{doc['title']}</b>\n\n"
        f"ইউটিউবে আপলোড করার সময় এই থাম্বনেইলটি ব্যবহার করুন।"
    )
    send_telegram_photo(thumb_path, thumb_caption)

    # মাস্টার ভিডিও পাঠানো
    master_caption = f"🎬 <b>মাস্টার ডকুমেন্টারি (16:9 Full HD):</b>\n{doc['title']}"
    send_telegram_video(master_video_path, master_caption)

    # ৩টি শর্টস টেলিগ্রামে পাঠানো
    for idx, sp in enumerate(short_paths, 1):
        short_caption = (
            f"⚡ <b>Viral Short {idx}/3 (9:16 Vertical)</b>\n\n"
            f"📱 TikTok / Instagram Reels / YouTube Shorts-এর জন্য প্রস্তুত!\n"
            f"🏷️ <code>{sp.name}</code>"
        )
        send_telegram_video(sp, short_caption)

    # সম্পূর্ণ কপি-পেস্ট এসইও ডেসক্রিপশন
    seo_text = (
        f"📋 <b>YouTube SEO Description & Timestamps (কপি করে পেস্ট করুন):</b>\n\n"
        f"<pre>{doc['description']}</pre>\n\n"
        f"🏷️ <b>ট্যাগস:</b>\n<code>{', '.join(doc['tags'])}</code>"
    )
    send_telegram_msg(seo_text)

    print("✅ টেলিগ্রামে সফলভাবে সমস্ত মেটেরিয়াল পাঠানো হয়েছে!")


if __name__ == "__main__":
    run_full_youtube_pipeline()
