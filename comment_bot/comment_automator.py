# -*- coding: utf-8 -*-
"""
=============================================================================
💬 JUBAYER.DEV - FACEBOOK VIDEO & REEL AI COMMENT AUTOMATOR (PRODUCTION)
=============================================================================
এই ইঞ্জিনটি জুবায়ের ভাইয়ের ফেসবুকের ভিডিও, রিলস ও পোস্টের নতুন কমেন্ট স্ক্যান করে:
  ১. ক্রোম সেশন ব্যবহার করে রিসেন্ট রিলস ও নোটিফিকেশন পেজ স্ক্যান করে
  ২. কোনো আন-রিপ্লাইড কমেন্ট পাওয়া মাত্রই জেমিনি এআই দিয়ে প্রফেশনাল ও সাবলীল বাংলা উত্তর তৈরি করে
  ৩. হিউম্যান-লাইক স্বাভাবিক গতিতে 'Reply' বক্সে টাইপ করে পোস্ট করে
  ৪. সুরক্ষার জন্য প্রতি রিপ্লাইয়ের মাঝে নিরাপদ বিরতি (Anti-Bot Safe Delay) বজায় রাখে
  ৫. সাথে সাথে জুবায়ের ভাইয়ের টেলিগ্রামে রিয়েলটাইম নোটিফিকেশন পাঠায়
=============================================================================
"""

import os
import sys
import json
import time
import random
import argparse
from datetime import datetime
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests
from playwright.sync_api import sync_playwright
from messenger_bot.agent_brain import call_comment_ai
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

PROFILE_DIR = ROOT_DIR / "messenger_bot" / "chrome_profile"
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPLIED_COMMENTS_FILE = DATA_DIR / "replied_comments.json"

JUBAYER_PROFILE_REELS_URL = "https://www.facebook.com/profile.php?id=61593846507081&sk=reels_tab"
NOTIFICATIONS_URL = "https://www.facebook.com/notifications"


def load_replied_comments() -> dict:
    if REPLIED_COMMENTS_FILE.exists():
        try:
            with open(REPLIED_COMMENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_replied_comments(data: dict):
    try:
        with open(REPLIED_COMMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Storage Error] {e}")


def send_telegram_comment_alert(commenter: str, comment_text: str, ai_reply: str, post_title: str = "", is_dry_run: bool = False):
    """টেলিগ্রামে রিয়েলটাইম কমেন্ট রিপ্লাই নোটিফিকেশন পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    tag = "🧪 <b>[DRY-RUN টেস্ট] নতুন ফেসবুক কমেন্ট পাওয়া গেছে:</b>" if is_dry_run else "💬 <b>ফেসবুক ভিডিও/রিলসে এআই কমেন্ট রিপ্লাই দেওয়া হয়েছে!</b>"
    alert_text = (
        f"{tag}\n\n"
        f"👤 <b>মন্তব্যকারী:</b> {commenter}\n"
        f"📝 <b>মন্তব্য:</b> {comment_text}\n"
        f"🤖 <b>এআই রিপ্লাই:</b>\n{ai_reply}\n\n"
    )
    if post_title:
        alert_text += f"🎬 <b>ভিডিও/রিলস:</b> {post_title[:60]}...\n\n"
    alert_text += f"⏰ <i>সময়: {datetime.now().strftime('%I:%M %p, %d %b %Y')}</i>"

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": alert_text,
            "parse_mode": "HTML"
        }, timeout=10)
    except Exception as e:
        print(f"[Telegram Alert Error] {e}")


class FacebookCommentAutomator:
    def __init__(self, dry_run: bool = False, headless: bool = False):
        self.dry_run = dry_run
        self.headless = headless
        self.playwright = None
        self.browser_context = None
        self.page = None
        self.replied_comments = load_replied_comments()

    def start_browser(self):
        print("\n🌐 গুগল ক্রোম চালু করা হচ্ছে (Facebook Comment Engine)...")
        self.playwright = sync_playwright().start()
        self.browser_context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=self.headless,
            viewport={"width": 1280, "height": 850},
            args=[
                "--disable-notifications",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        self.page = self.browser_context.pages[0] if self.browser_context.pages else self.browser_context.new_page()

    def close(self):
        if self.browser_context:
            try:
                self.browser_context.close()
            except Exception:
                pass
        if self.playwright:
            try:
                self.playwright.stop()
            except Exception:
                pass

    def scan_reels_and_reply(self, max_reels_to_check: int = 4) -> int:
        """জুবায়ের ভাইয়ের রিসেন্ট রিলসগুলোর কমেন্ট সেকশন স্ক্যান করে রিপ্লাই দেয়।"""
        print(f"\n🎬 জুবায়ের ভাইয়ের রিসেন্ট রিলস পেজ স্ক্যান করা হচ্ছে: {JUBAYER_PROFILE_REELS_URL}")
        try:
            self.page.goto(JUBAYER_PROFILE_REELS_URL, wait_until="domcontentloaded", timeout=15000)
        except Exception:
            pass

        time.sleep(3)

        # রিলসের লিংকগুলো সংগ্রহ করা
        reel_elements = self.page.locator('a[href*="/reel/"]').all()
        reel_urls = []
        for r in reel_elements:
            try:
                href = r.get_attribute("href") or ""
                if href and "/reel/" in href and href not in reel_urls:
                    reel_urls.append(href)
            except Exception:
                pass

        print(f"📹 মোট {len(reel_urls)}টি রিলস পাওয়া গেছে। প্রথম {min(len(reel_urls), max_reels_to_check)}টি স্ক্যান করা হচ্ছে...", flush=True)

        total_replies = 0
        for idx, r_url in enumerate(reel_urls[:max_reels_to_check]):
            full_reel_url = r_url if r_url.startswith("http") else f"https://www.facebook.com{r_url}"
            print(f"\n--- [রিলস {idx+1}/{min(len(reel_urls), max_reels_to_check)}] ওপেন করা হচ্ছে: {full_reel_url[:60]}... ---", flush=True)

            try:
                self.page.goto(full_reel_url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(3)

                # রিলসের টাইটেল বা ক্যাপশন নেওয়া
                reel_title = ""
                try:
                    title_el = self.page.locator('div[role="main"] h1, div[role="main"] div[dir="auto"]').first
                    if title_el.is_visible():
                        reel_title = title_el.inner_text().strip()[:80]
                except Exception:
                    pass

                # কমেন্টগুলো খোঁজা
                comment_articles = self.page.locator('div[role="article"]').all()
                print(f"💬 মোট {len(comment_articles)}টি কমেন্ট এলিমেন্ট পাওয়া গেছে।")

                for c_idx, article in enumerate(comment_articles):
                    try:
                        raw_text = article.inner_text().strip()
                        if not raw_text:
                            continue

                        # জুবায়ের ভাইয়ের নিজের কমেন্ট বা অথর কমেন্ট এড়িয়ে চলা
                        if "author" in raw_text.lower() or "jubayer ahmad" in raw_text.lower():
                            continue

                        # কমেন্টের লাইনগুলো আলাদা করে নাম ও মেসেজ বের করা
                        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
                        commenter_name = lines[0] if lines else "ফেসবুক ব্যবহারকারী"

                        # কমেন্ট টেক্সট নিখুঁতভাবে বের করা
                        clean_lines = []
                        for l in lines[1:]:
                            if l.isdigit() and len(l) < 4:
                                continue
                            if not any(btn_w in l.lower() for btn_w in ["reply", "hide", "like", "share", "author", "উত্তর দিন", "লুকান", "লাইক", "1h", "2h", "3h", "d", "w"]):
                                l_cleaned = l.lstrip("· •-  ").strip()
                                if l_cleaned and not l_cleaned.isdigit():
                                    clean_lines.append(l_cleaned)
                        comment_body = " ".join(clean_lines) if clean_lines else raw_text

                        # ইতিমধ্যে রিপ্লাই দেওয়া হয়েছে কিনা চেক (হ্যাশ কী দিয়ে)
                        comment_key = f"{full_reel_url}_{commenter_name}_{comment_body[:30]}"
                        if comment_key in self.replied_comments:
                            continue

                        print(f"\n👉 [নতুন কমেন্ট পাওয়া গেছে!]")
                        print(f"👤 মন্তব্যকারী: {commenter_name}")
                        print(f"📝 মন্তব্য: \"{comment_body}\"")

                        # জেমিনি এআই দিয়ে উত্তর প্রস্তুত করা
                        print("🧠 জেমিনি এআই উত্তর তৈরি করছে...")
                        ai_reply = call_comment_ai(
                            commenter_name=commenter_name,
                            comment_text=comment_body,
                            post_context=reel_title
                        )
                        print(f"🤖 [এআই উত্তর]: \"{ai_reply}\"")

                        if self.dry_run:
                            print("🧪 [DRY-RUN] কমেন্টটি ফেসবুক পেজে পোস্ট করা হয়নি (সফলভাবে টেস্ট সম্পন্ন)।")
                            send_telegram_comment_alert(
                                commenter=commenter_name,
                                comment_text=comment_body,
                                ai_reply=ai_reply,
                                post_title=reel_title,
                                is_dry_run=True
                            )
                            self.replied_comments[comment_key] = {
                                "commenter": commenter_name,
                                "comment": comment_body,
                                "reply": ai_reply,
                                "mode": "dry_run",
                                "time": datetime.now().isoformat()
                            }
                            save_replied_comments(self.replied_comments)
                            total_replies += 1
                            continue

                        # লাইভ মোড: Reply বাটনে ক্লিক করা
                        reply_btn = article.locator('div[role="button"]:has-text("Reply"), span:has-text("Reply"), div[role="button"]:has-text("উত্তর দিন")').first
                        if reply_btn.is_visible():
                            reply_btn.click()
                            time.sleep(1.5)

                            # নেস্টেড রিপ্লাই ইনপুট বক্স খোঁজা
                            textboxes = self.page.locator('div[role="textbox"][contenteditable="true"]').all()
                            if textboxes:
                                reply_box = textboxes[-1] # সর্বশেষ ওপেন হওয়া বক্সটিই রিপ্লাই বক্স
                                reply_box.click()
                                time.sleep(0.5)

                                # মানুষের মতো টাইপ করা
                                for char in ai_reply:
                                    self.page.keyboard.type(char, delay=random.randint(15, 45))
                                time.sleep(1)

                                self.page.keyboard.press("Enter")
                                time.sleep(3)
                                print("✅ ফেসবুকে সফলভাবে কমেন্ট রিপ্লাই পোস্ট হয়েছে!")

                                # টেলিগ্রামে নোটিফিকেশন পাঠানো
                                send_telegram_comment_alert(
                                    commenter=commenter_name,
                                    comment_text=comment_body,
                                    ai_reply=ai_reply,
                                    post_title=reel_title,
                                    is_dry_run=False
                                )

                                self.replied_comments[comment_key] = {
                                    "commenter": commenter_name,
                                    "comment": comment_body,
                                    "reply": ai_reply,
                                    "mode": "live",
                                    "time": datetime.now().isoformat()
                                }
                                save_replied_comments(self.replied_comments)
                                total_replies += 1

                                # অ্যান্টি-বট সেফটি ডিলে: ১ থেকে ২ মিনিট বিরতি
                                delay = random.randint(60, 120)
                                print(f"⏳ নিরাপত্তার স্বার্থে পরবর্তী কমেন্টের আগে {delay} সেকেন্ড বিরতি...")
                                time.sleep(delay)

                    except Exception as ex:
                        print(f"⚠️ কমেন্ট প্রসেস করতে সমস্যা: {ex}")

            except Exception as e:
                print(f"⚠️ রিলস ওপেন করতে সমস্যা: {e}")

        return total_replies

    def run_loop(self, poll_interval_minutes: int = 10):
        print("=================================================================")
        print("🤖 JUBAYER.DEV FACEBOOK AI COMMENT AUTOMATOR STARTED")
        print(f"Mode: {'🧪 DRY-RUN (টেস্ট মোড)' if self.dry_run else '🚀 LIVE PRODUCTION'}")
        print(f"Check Interval: প্রতি {poll_interval_minutes} মিনিট পর পর")
        print("=================================================================")

        self.start_browser()
        try:
            while True:
                self.scan_reels_and_reply()
                print(f"\n😴 পরবর্তী স্ক্যান {poll_interval_minutes} মিনিট পর... ({datetime.now().strftime('%I:%M %p')})")
                time.sleep(poll_interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n🛑 ব্যবহারকারী দ্বারা ইঞ্জিন বন্ধ করা হয়েছে।")
        finally:
            self.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facebook AI Comment Automator")
    parser.add_argument("--dry-run", action="store_true", help="Run in test mode without posting comments")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--interval", type=int, default=10, help="Interval in minutes between scans")
    args = parser.parse_args()

    automator = FacebookCommentAutomator(dry_run=args.dry_run, headless=args.headless)
    automator.run_loop(poll_interval_minutes=args.interval)
