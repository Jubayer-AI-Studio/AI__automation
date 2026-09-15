# -*- coding: utf-8 -*-
"""
=============================================================================
⏰ JUBAYER.DEV AUTOMATED DAILY CREATOR SUITE DISPATCHER
=============================================================================
প্রতিদিন নির্ধারিত সময়ে (দুপুর ১২:০০ ও রাত ৮:০০) স্বয়ংক্রিয়ভাবে:
  ১. ৫-৭ মিনিটের মাস্টার সিনেমাটিক ইউটিউব ভিডিও
  ২. ১২৮০x৭২০ হাই-সিটিআর ইউটিউব থাম্বনেইল
  ৩. ৩টি ৯:১৬ ভাইরাল ভার্টিক্যাল শর্টস (TikTok, Reels, Shorts)
  ৪. ক্লিকযোগ্য টাইমস্ট্যাম্প সহ ইউটিউব এসইও ডেসক্রিপশন
  ৫. ফেসবুক ১০৮০x১০৮০ ইনফোগ্রাফিক ফটো পোস্ট ও টেক্সট
সবকিছু একসাথে তৈরি করে সরাসরি জুবায়ের স্যারের টেলিগ্রাম বটে পৌঁছে দেয়।
=============================================================================
"""

import os
import sys
import time
import requests
from datetime import datetime
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
from youtube_production.run_youtube_engine import run_full_youtube_pipeline
from thumbnail_card.thumbnail_maker import create_ai_photocard

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_telegram_msg(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=25
        )
    except Exception as e:
        print(f"[Telegram] Error: {e}")


def send_telegram_photo(photo_path: Path, caption: str):
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
        print(f"[Telegram] Photo Error: {e}")


def dispatch_daily_creator_suite():
    now_str = datetime.now().strftime("%I:%M %p, %d %B %Y")
    print("=" * 70)
    print(f"🚀 [SCHEDULED RUN] স্বয়ংক্রিয় দৈনিক ক্রিয়েটর স্যুট শুরু হচ্ছে: {now_str}")
    print("=" * 70)

    # টেলিগ্রামে সূচনার নোটিশ
    slot_label = "দুপুর ১২:০০" if datetime.now().hour < 15 else "রাত ০৮:০০"
    start_alert = (
        f"⚡ <b>Jubayer.dev Daily Automation Slot ({slot_label}):</b>\n"
        f"আজকের শিডিউল অনুযায়ী ইউটিউব মাস্টার ডকুমেন্টারি, ৩টি শর্টস ও সোশ্যাল মিডিয়া কিট তৈরি শুরু হয়েছে..."
    )
    send_telegram_msg(start_alert)

    # ১. সম্পূর্ণ ইউটিউব ও শর্টস পাইপলাইন রান
    print("\n▶ [1/2] ইউটিউব লং-ফর্ম ও ৩-শর্টস ইঞ্জিন চালু হচ্ছে...")
    run_full_youtube_pipeline()

    # ২. ফেসবুক ইনফোগ্রাফিক ফটো পোস্ট জেনারেশন ও ডেলিভারি
    print("\n▶ [2/2] ফেসবুক ১০৮০x১০৮০ ইনফোগ্রাফিক ফটো কার্ড তৈরি হচ্ছে...")
    fb_title = "২০২৬ সালে যে ৪টি প্রযুক্তি ক্ষেত্রে সবচেয়ে বড় বিপ্লব ঘটছে"
    fb_points = [
        "১. কোয়ান্টাম ক্লাউড প্রসেসিং ও পোস্ট-কোয়ান্টাম ক্রিপ্টোগ্রাফি",
        "২. জেনারেটিভ এআই এজেন্ট ও ফুল-স্ট্যাক কোডিং অটোমেশন",
        "৩. হিউম্যানয়েড রোবোটিক্স ও স্প্যাশিয়াল ভিশন কম্পিউটিং",
        "৪. ব্রেন-কম্পিউটার ইন্টারফেস ও এজ নিউরাল মাইক্রোচিপস"
    ]
    photo_card_path = create_ai_photocard(fb_title, fb_points, category="JUBAYER.DEV TECH LAB // 2026")
    
    fb_caption = (
        f"🖼️ <b>Facebook Feed Infographic Photo Post (1080x1080)</b>\n\n"
        f"<b>{fb_title}</b>\n\n"
        f"ফেসবুক পেজে পোস্ট করার জন্য রেডি করা ইনফোগ্রাফিক কার্ড।\n"
        f"#TechTrends2026 #JubayerDev #AIAutomation #QuantumTech"
    )
    send_telegram_photo(photo_card_path, fb_caption)

    # সমাপনী রিপোর্ট
    finish_alert = (
        f"✅ <b>Jubayer.dev Daily Automation Complete!</b>\n\n"
        f"আজকের সমস্ত মেটেরিয়াল (ইউটিউব ডকুমেন্টারি, থাম্বনেইল, ৩টি ভাইরাল শর্টস, ফটো পোস্ট ও এসইও ডেসক্রিপশন) আপনার টেলিগ্রামে সাফল্যের সাথে ডেলিভার করা হয়েছে।"
    )
    send_telegram_msg(finish_alert)
    print("\n✅ সমস্ত শিডিউল কাজ সম্পন্ন হয়েছে!")


if __name__ == "__main__":
    dispatch_daily_creator_suite()
