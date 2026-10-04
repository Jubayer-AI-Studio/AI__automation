# -*- coding: utf-8 -*-
"""
=============================================================================
🤖 JUBAYER.DEV - FACEBOOK MESSENGER DESKTOP AI AUTOMATOR (STABLE PRODUCTION)
=============================================================================
এটি জুবায়ের স্যারের পিসি থেকে সরাসরি ফেসবুক মেসেঞ্জারে অটো-রিপ্লাই দেওয়ার ইঞ্জিন:
  ১. ক্রোম ব্রাউজারে মেসেঞ্জার সেশন স্বয়ংক্রিয়ভাবে ওপেন ও লগইন সেভ রাখে
  ২. কোনো ভুল লুপ নেই, শুধুমাত্র আনরেড চ্যাটে ক্লিক করে উত্তর দেয়
  ৩. ইনকামিং মেসেজ পাওয়া মাত্রই জেমিনি এআই দিয়ে প্রফেশনাল বাংলায় উত্তর টাইপ করে পাঠায়
  ৪. প্রতিটি রিপ্লাইয়ের সাথে সাথে স্যারের মোবাইলের টেলিগ্রামে সরাসরি নোটিফিকেশন পাঠায়
=============================================================================
"""

import os
import sys
import time
import traceback
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

from playwright.sync_api import sync_playwright
from messenger_bot.agent_brain import call_gemini_api
from messenger_bot.leads_db import save_or_update_lead
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

PROFILE_DIR = ROOT_DIR / "messenger_bot" / "chrome_profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

MESSENGER_URL = "https://www.facebook.com/messages"

def send_telegram_alert(sender_name: str, incoming_msg: str, ai_reply: str):
    """টেলিগ্রামে রিয়েলটাইম মেসেঞ্জার অ্যালার্ট পাঠায় যাতে জুবায়ের ভাই মোবাইলে দেখতে পারেন।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    alert_text = (
        f"⚡ <b>ফেসবুক মেসেঞ্জারে এআই অটো-রিপ্লাই দিয়েছে!</b>\n\n"
        f"👤 <b>ক্লায়েন্ট:</b> {sender_name}\n"
        f"💬 <b>মেসেজ:</b> {incoming_msg}\n"
        f"🤖 <b>এআই উত্তর:</b>\n{ai_reply}\n\n"
        f"⏰ <i>সময়: {datetime.now().strftime('%I:%M %p, %d %b %Y')}</i>"
    )
    try:
        import requests
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": alert_text,
            "parse_mode": "HTML"
        }, timeout=8)
    except Exception as e:
        pass


class MessengerAutomator:
    def __init__(self):
        self.playwright = None
        self.browser_context = None
        self.page = None
        self.replied_history = set()

    def start_browser(self, headless=False):
        """ব্রাউজার ওপেন করে এবং পারসিস্টেন্ট সেশন লোড করে।"""
        print("\n🌐 গুগল ক্রোম ব্রাউজার চালু হচ্ছে...")
        self.playwright = sync_playwright().start()
        self.browser_context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=headless,
            viewport={"width": 1280, "height": 850},
            args=[
                "--disable-notifications",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        self.page = self.browser_context.pages[0] if self.browser_context.pages else self.browser_context.new_page()

    def ensure_logged_in(self):
        """মেসেঞ্জারে ইউজার লগইন আছেন কিনা নিশ্চিত করে।"""
        print(f"🔗 মেসেঞ্জারে কানেক্ট করা হচ্ছে: {MESSENGER_URL}")
        self.page.goto(MESSENGER_URL, wait_until="networkidle", timeout=30000)

        if "login" in self.page.url.lower():
            print("\n" + "=" * 65)
            print("🔐 ফেসবুক অ্যাকাউন্টে লগইন অপেক্ষা করা হচ্ছে...")
            print("=" * 65 + "\n")

            while "login" in self.page.url.lower():
                time.sleep(2)
                try:
                    if "facebook.com/messages" in self.page.url:
                        break
                except Exception:
                    pass

        print("\n✅ ফেসবুক মেসেঞ্জারে সফলভাবে কানেক্টেড!")
        time.sleep(3)

    def scan_and_reply(self):
        """মেসেঞ্জারের চ্যাট লিস্ট স্ক্যান করে এবং নতুন আনরেড মেসেজের উত্তর দেয়।"""
        try:
            # কোনো খোলা নোটিফিকেশন ড্রপডাউন থাকলে বন্ধ করা
            try:
                if self.page.locator('div[aria-label="Notifications"]').is_visible():
                    self.page.keyboard.press("Escape")
            except Exception:
                pass

            # চ্যাট লিস্টের সব রো চেক করা
            rows = self.page.locator('div[role="grid"] div[role="row"]').all()
            
            unread_target = None
            for r in rows:
                try:
                    txt = r.inner_text()
                    # যদি টেক্সটে 'Unread message:' অথবা 'অপঠিত' থাকে
                    if "unread message:" in txt.lower() or "অপঠিত" in txt.lower():
                        unread_target = r
                        break
                except Exception:
                    pass

            if unread_target:
                unread_target.click()
                time.sleep(2.5)
                self.process_active_chat()
            else:
                # বর্তমানে ওপেন থাকা চ্যাটেও যদি কোনো নতুন ইনকামিং মেসেজ থাকে
                self.process_active_chat()

        except Exception as e:
            pass

    def process_active_chat(self):
        """বর্তমানে ওপেন থাকা চ্যাটের সর্বশেষ মেসেজ যাচাই করে রিপ্লাই পাঠানো।"""
        try:
            # চ্যাট পার্টনারের নাম বের করা
            sender_name = "Facebook User"
            try:
                header_el = self.page.locator('div[role="main"] h1, h2 span, span[dir="auto"].x193iq5w.xeuugli').first
                if header_el.is_visible():
                    t = header_el.inner_text().strip()
                    if t and len(t) < 40 and not any(k in t.lower() for k in ["chats", "messages", "find friends"]):
                        sender_name = t
            except Exception:
                pass

            # ইনকামিং মেসেজ বাবল খোঁজা
            # ইনকামিং মেসেজের পাশে সাধারণত পার্টনারের ডিপি বা বামে অ্যালাইনমেন্ট থাকে
            message_bubbles = self.page.locator('div[role="main"] div[dir="auto"], div[data-pagelet="MessagesWrapper"] div[dir="auto"]')
            count = message_bubbles.count()
            if count == 0:
                return

            # শেষ মেসেজ নেওয়া
            last_bubble = message_bubbles.nth(count - 1)
            last_text = last_bubble.inner_text().strip()

            if not last_text or len(last_text) < 1:
                return

            # আমাদের নিজস্ব এআই উত্তর হলে এড়িয়ে চলা
            if "জুবায়ের স্যার" in last_text or "আসসালামু আলাইকুম" in last_text or "automatic reply" in last_text.lower():
                return

            # ডুপ্লিকেট চেক
            history_key = (sender_name, last_text)
            if history_key in self.replied_history:
                return

            print(f"\n📩 [{sender_name} পাঠিয়েছেন]: \"{last_text}\"")
            print("🧠 জেমিনি এআই স্মার্ট বাংলা উত্তর তৈরি করছে...")

            # জেমিনি এআই কল
            ai_reply = call_gemini_api(
                user_message=last_text,
                sender_id=sender_name,
                sender_name=sender_name,
                platform="messenger"
            )

            print(f"🤖 [এআই উত্তর]: \"{ai_reply}\"")

            # ইনপুট বক্সে টাইপ ও সেন্ড
            input_box = self.page.locator('div[role="textbox"][aria-label*="Message" i], div[role="textbox"]').first
            if not input_box.is_visible():
                return

            input_box.click()
            time.sleep(0.5)
            input_box.fill(ai_reply)
            time.sleep(0.8)
            self.page.keyboard.press("Enter")
            time.sleep(1.2)

            print("🚀 মেসেঞ্জারে উত্তর সফলভাবে সেন্ট (Sent) হয়েছে!\n")

            # হিস্টোরিতে সংরক্ষণ যাতে রিপিট না হয়
            self.replied_history.add(history_key)

            # মোবাইলের টেলিগ্রামে অ্যালার্ট
            send_telegram_alert(sender_name, last_text, ai_reply)

        except Exception as e:
            pass

    def run_loop(self):
        """২৪/৭ অটোমেশন লুপ যা মেসেঞ্জার মনিটর করে।"""
        print("\n" + "=" * 65)
        print("🚀 JUBAYER SIR'S MESSENGER AI ASSISTANT IS LIVE & MONITORING!")
        print("📡 নতুন মেসেজ আসলেই জেমিনি এআই স্বয়ংক্রিয়ভাবে উত্তর দেবে।")
        print("📱 প্রতিটি উত্তরের রিয়েলটাইম কপি আপনার টেলিগ্রাম বটে পৌঁছে যাবে।")
        print("🛑 বন্ধ করতে চাইলে এই উইন্ডোতে Ctrl + C চাপুন।")
        print("=" * 65 + "\n")

        try:
            while True:
                self.scan_and_reply()
                time.sleep(4)  # প্রতি ৪ সেকেন্ড পরপর স্ক্যান
        except KeyboardInterrupt:
            print("\n🛑 অটোমেশন বন্ধ করা হয়েছে।")
        finally:
            self.close()

    def close(self):
        try:
            if self.browser_context:
                self.browser_context.close()
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass


if __name__ == "__main__":
    automator = MessengerAutomator()
    automator.start_browser(headless=False)
    automator.ensure_logged_in()
    automator.run_loop()
