import os
import requests
from pathlib import Path
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_full_creator_kit(video_path: Path, title: str, caption: str, hashtags: list, photo_card_path: Path, extras: dict) -> bool:
    """
    Sends the complete Daily Facebook Creator Kit directly to the user's Telegram chat:
    1. AI Reel Video (.mp4) with caption & hashtags
    2. AI Infographic Photo Card (.png) for feed image post
    3. High-Engagement Discussion Text Post & Story Poll
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not provided. Skipping Telegram dispatch.")
        print(f"[Telegram] Video saved at: {video_path}")
        print(f"[Telegram] Photo card saved at: {photo_card_path}")
        return False

    tags_str = " ".join(hashtags)
    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

    # 1. Send Video Reel
    print(f"[Telegram] Sending Video Reel to chat {TELEGRAM_CHAT_ID}...")
    video_msg = (
        f"ভিডিও শিরোনাম: {title}\n\n"
        f"ক্যাপশন:\n"
        f"{caption}\n\n"
        f"{tags_str}"
    )
    try:
        with open(video_path, "rb") as vf:
            res = requests.post(
                f"{base_url}/sendVideo",
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": video_msg, "supports_streaming": True},
                files={"video": vf},
                timeout=120
            )
            if res.status_code != 200:
                print(f"[Telegram] Video send warning: {res.text}")
    except Exception as e:
        print(f"[Telegram] Failed to send video: {e}")

    # 2. Send Infographic Photo Card
    if photo_card_path and photo_card_path.exists():
        print(f"[Telegram] Sending Photo Card...")
        photo_msg = (
            f"{extras['photo_card']['title']} সম্পর্কে বিস্তারিত তথ্য।\n\n"
            f"#Technology #TechBangladesh #BanglaTech #Infographic"
        )
        try:
            with open(photo_card_path, "rb") as pf:
                requests.post(
                    f"{base_url}/sendPhoto",
                    data={"chat_id": TELEGRAM_CHAT_ID, "caption": photo_msg},
                    files={"photo": pf},
                    timeout=60
                )
        except Exception as e:
            print(f"[Telegram] Failed to send photo card: {e}")

    # 3. Send Facebook Feed Post (Clean, ready to copy directly)
    print(f"[Telegram] Sending Discussion Post & Story Poll...")
    discussion_text = extras["discussion_post"]["text"]
    story_poll = extras["story_poll"]

    try:
        # ফেসবুক পোস্ট: সরাসরি কপি করার জন্য একদম নিখুঁত টেক্সট
        post_bundle = (
            f"[ফেসবুক পোস্ট - সরাসরি কপি করে আপলোড করুন]\n\n"
            f"{discussion_text}"
        )
        requests.post(
            f"{base_url}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": post_bundle},
            timeout=30
        )

        # ফেসবুক স্টোরি: সরাসরি কপি করার জন্য আলাদা মেসেজ
        story_bundle = (
            f"[ফেসবুক স্টোরি - সরাসরি কপি করার জন্য]\n\n"
            f"{story_poll}"
        )
        requests.post(
            f"{base_url}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": story_bundle},
            timeout=30
        )

        print("[Telegram] Complete Daily Creator Kit sent successfully to Telegram!")
        return True
    except Exception as e:
        print(f"[Telegram] Failed to send text bundle: {e}")
        return False
