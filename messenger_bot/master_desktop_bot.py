# -*- coding: utf-8 -*-
"""
=============================================================================
🤖 JUBAYER.DEV - UNIFIED MASTER DESKTOP AI AUTOMATOR (ALL-IN-ONE)
=============================================================================
এটি জুবায়ের ভাইয়ের ফেসবুক মেসেঞ্জার ও রিলস/ভিডিও কমেন্ট—দুটোকেই একসাথে
একটিমাত্র ক্রোম ব্রাউজারে নিখুঁতভাবে ও ১০০% ঝুঁকিমুক্ত উপায়ে অটোমেট করে:

  ১. ট্যাব ১ (মেসেঞ্জার): আনরিড মেসেজ আসা মাত্রই জেমিনি এআই দিয়ে উত্তর দেয়।
  ২. ট্যাব ২ (রিলস ও পোস্ট): প্রতি ১০ মিনিট পর পর রিলস চেক করে নতুন কমেন্টে
     মানুষের মতো স্বাভাবিক গতি ও সেফটি ডিলে সহকারে উত্তর দেয়।
  ৩. সম্পূর্ণ ঝুঁকিমুক্ত: কোনো ক্রোম প্রোফাইল লক হবে না এবং ফেসবুকের
     অ্যান্টি-বট পলিসি অনুযায়ী প্রাকৃতিক বিরতি বজায় রাখবে।
  ৪. প্রতিটি মেসেজ ও কমেন্ট রিপ্লাইয়ের লাইভ কপি সাথে সাথে স্যারের মোবাইলের
     টেলিগ্রাম বটে পৌঁছে যাবে।
=============================================================================
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from pathlib import Path

# Windows console encoding fix
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
from messenger_bot.agent_brain import call_gemini_api, call_comment_ai
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

PROFILE_DIR = ROOT_DIR / "messenger_bot" / "chrome_profile"
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPLIED_COMMENTS_FILE = DATA_DIR / "replied_comments.json"

MESSENGER_URL = "https://business.facebook.com/latest/inbox/all?asset_id=1354604231069150"
JUBAYER_REELS_URL = "https://www.facebook.com/profile.php?id=61593846507081&sk=reels_tab"


# কমেন্ট চেক করার বিরতি (সেকেন্ডে): ১০ মিনিট
COMMENT_CHECK_INTERVAL = 600
# দৈনিক সর্বোচ্চ কমেন্ট লিমিট (অ্যাকাউন্ট নিরাপত্তার জন্য)
DAILY_MAX_COMMENTS = 25


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


def send_telegram_alert(sender_name: str, incoming_msg: str, ai_reply: str, event_type: str = "messenger"):
    """টেলিগ্রামে মেসেঞ্জার ও কমেন্টের নোটিফিকেশন পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    if event_type == "comment":
        header = "💬 <b>ফেসবুক রিলস/পোস্টে এআই কমেন্ট রিপ্লাই দেওয়া হয়েছে!</b>"
        label = "মন্তব্যকারী"
        msg_label = "কমেন্ট"
    else:
        header = "⚡ <b>ফেসবুক মেসেঞ্জারে এআই অটো-রিপ্লাই দিয়েছে!</b>"
        label = "ক্লায়েন্ট"
        msg_label = "মেসেজ"

    alert_text = (
        f"{header}\n\n"
        f"👤 <b>{label}:</b> {sender_name}\n"
        f"💬 <b>{msg_label}:</b> {incoming_msg}\n"
        f"🤖 <b>এআই উত্তর:</b>\n{ai_reply}\n\n"
        f"⏰ <i>সময়: {datetime.now().strftime('%I:%M %p, %d %b %Y')}</i>"
    )
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": alert_text,
            "parse_mode": "HTML"
        }, timeout=10)
    except Exception:
        pass


class MasterDesktopAutomator:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser_context = None
        self.page_messenger = None
        self.page_reels = None
        self.replied_msg_history = set()
        self.replied_comments = load_replied_comments()
        self.last_comment_check = 0
        self.today_comment_count = 0
        self.last_day = datetime.now().day

    def start(self):
        print("\n🌐 গুগল ক্রোম মাস্টার ব্রাউজার চালু হচ্ছে (All-in-One Engine)...")
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

        # ট্যাব ১: মেসেঞ্জার
        self.page_messenger = self.browser_context.pages[0] if self.browser_context.pages else self.browser_context.new_page()
        print(f"🔗 [ট্যাব ১] মেসেঞ্জারে কানেক্ট করা হচ্ছে: {MESSENGER_URL}")
        try:
            self.page_messenger.goto(MESSENGER_URL, wait_until="domcontentloaded", timeout=30000)
        except Exception:
            pass

        time.sleep(3)
        if "login" in self.page_messenger.url.lower():
            print("⚠️ মেসেঞ্জারে লগইন পাওয়া যায়নি। দয়া করে লগইন সম্পন্ন করুন।")
            while "login" in self.page_messenger.url.lower():
                time.sleep(2)
        print("✅ [ট্যাব ১] মেসেঞ্জার কানেক্টেড ও রেডি!")

        # ট্যাব ২: রিলস ও পোস্ট কমেন্ট মনিটর
        self.page_reels = self.browser_context.new_page()
        print(f"🔗 [ট্যাব ২] রিলস সেকশনে কানেক্ট করা হচ্ছে: {JUBAYER_REELS_URL}")
        try:
            self.page_reels.goto(JUBAYER_REELS_URL, wait_until="domcontentloaded", timeout=25000)
        except Exception:
            pass
        time.sleep(2)
        print("✅ [ট্যাব ২] রিলস সেকশন কানেক্টেড ও রেডি!")

    def scan_messenger(self):
        """ট্যাব ১-এ মেসেঞ্জারের আনরিড চ্যাট চেক করে রিপ্লাই দেয় (Meta Business Suite Inbox ও Standard Messenger উভয়ই সাপোর্ট করে)।"""
        try:
            curr_url = self.page_messenger.url.lower()
            if "business.facebook.com" in curr_url or "inbox" in curr_url:
                self.process_meta_inbox()
                return

            # স্ট্যান্ডার্ড ফেসবুক মেসেঞ্জার হ্যান্ডলার
            try:
                if self.page_messenger.locator('div[aria-label="Notifications"]').is_visible():
                    self.page_messenger.keyboard.press("Escape")
            except Exception:
                pass

            rows = self.page_messenger.locator('div[role="grid"] div[role="row"]').all()
            unread_target = None
            for r in rows:
                try:
                    txt = r.inner_text()
                    if "unread message:" in txt.lower() or "অপঠিত" in txt.lower():
                        unread_target = r
                        break
                except Exception:
                    pass

            if unread_target:
                unread_target.click()
                time.sleep(2.5)
                self.process_active_messenger_chat()
            else:
                self.process_active_messenger_chat()

        except Exception:
            pass

    def process_meta_inbox(self):
        """মেটা বিজনেস স্যুট ইনবক্স (Meta Business Suite Inbox) অটোমেশন হ্যান্ডলার।"""
        try:
            # ১. সেন্ডার নাম ডিটেক্ট করা
            sender_name = self.page_messenger.evaluate('''() => {
                const cards = document.querySelectorAll('div._5_n1');
                for (const card of cards) {
                    const lines = card.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
                    if (lines.length > 0 && lines[0].length < 40) return lines[0];
                }
                const viewProfile = Array.from(document.querySelectorAll('*')).find(el => (el.innerText || '').includes('View profile'));
                if (viewProfile && viewProfile.parentElement) {
                    const pText = viewProfile.parentElement.innerText || '';
                    const lines = pText.split('\\n').map(s => s.trim()).filter(Boolean);
                    if (lines.length > 0 && lines[0] !== 'View profile') return lines[0];
                }
                return "Facebook User";
            }''')

            # ২. লেটেস্ট মেসেজ বাব্ল এক্সট্র্যাক্ট করা
            last_text = self.page_messenger.evaluate('''() => {
                const nodes = document.querySelectorAll('div.x1y1aw1k, div[dir="auto"]');
                const ignored = [
                    'Inbox', 'All messages', 'Messenger', 'Instagram', 'Search', 'Manage',
                    'Unread', 'Priority', 'Ad replies', 'Follow up', 'Create messaging ad',
                    'Messaging insights', 'Message settings', 'To-dos', 'Open Dropdown',
                    'Assign this conversation', 'View profile', 'Create order', 'Mark as lead',
                    'Submit', 'More items', 'Collapse contact details'
                ];
                let latest = "";
                for (const n of nodes) {
                    const t = (n.innerText || '').trim();
                    if (!t || ignored.some(ig => t.includes(ig)) || t.includes('Reply in Messenger') || t.includes('AM') || t.includes('PM')) {
                        continue;
                    }
                    latest = t;
                }
                return latest;
            }''')

            if not last_text or len(last_text) < 1:
                return

            # যদি এটি আমাদের নিজের দেওয়া পূর্ববর্তী উত্তর হয় তাহলে স্কিপ
            if any(w in last_text for w in ["জুবায়ের ভাই", "জুবায়ের স্যার", "আসসালামু আলাইকুম", "ল্যাবে ব্যস্ত", "অ্যাসিস্ট্যান্ট"]):
                return

            history_key = (sender_name, last_text)
            if history_key in self.replied_msg_history:
                return

            print(f"\n📩 [মেটা ইনবক্স - {sender_name}]: \"{last_text}\"", flush=True)
            print("🧠 এআই মেসেঞ্জার উত্তর তৈরি করছে...", flush=True)

            ai_reply = call_gemini_api(
                user_message=last_text,
                sender_id=sender_name,
                sender_name=sender_name,
                platform="messenger"
            )
            print(f"🤖 [এআই উত্তর]: \"{ai_reply}\"", flush=True)

            reply_box = self.page_messenger.locator('div[role="textbox"]').first
            if not reply_box.is_visible():
                return

            reply_box.click()
            time.sleep(0.5)

            # টাইপ করা
            for char in ai_reply:
                self.page_messenger.keyboard.type(char, delay=random.randint(15, 35))
            time.sleep(0.8)

            # Send বাটন অথবা Enter
            send_btn = self.page_messenger.locator('div[aria-label="Send"], button[aria-label="Send"], div[role="button"][aria-label="Send"]').first
            if send_btn.is_visible():
                send_btn.click()
            else:
                self.page_messenger.keyboard.press("Enter")
            time.sleep(2)

            print("🚀 মেটা বিজনেস ইনবক্সে এআই উত্তর পাঠানো হয়েছে!\n", flush=True)
            self.replied_msg_history.add(history_key)
            send_telegram_alert(sender_name, last_text, ai_reply, event_type="messenger")

        except Exception:
            pass

    def process_active_messenger_chat(self):
        try:
            sender_name = "Facebook User"
            try:
                header_el = self.page_messenger.locator('div[role="main"] h1, h2 span, span[dir="auto"].x193iq5w.xeuugli').first
                if header_el.is_visible():
                    t = header_el.inner_text().strip()
                    if t and len(t) < 40 and not any(k in t.lower() for k in ["chats", "messages", "find friends"]):
                        sender_name = t
            except Exception:
                pass

            message_bubbles = self.page_messenger.locator('div[role="main"] div[dir="auto"], div[data-pagelet="MessagesWrapper"] div[dir="auto"]')
            count = message_bubbles.count()
            if count == 0:
                return

            last_bubble = message_bubbles.nth(count - 1)
            last_text = last_bubble.inner_text().strip()

            if not last_text or len(last_text) < 1:
                return

            if "জুবায়ের স্যার" in last_text or "আসসালামু আলাইকুম" in last_text or "automatic reply" in last_text.lower():
                return

            history_key = (sender_name, last_text)
            if history_key in self.replied_msg_history:
                return

            print(f"\n📩 [মেসেঞ্জার - {sender_name}]: \"{last_text}\"", flush=True)
            print("🧠 এআই মেসেঞ্জার উত্তর তৈরি করছে...", flush=True)

            ai_reply = call_gemini_api(
                user_message=last_text,
                sender_id=sender_name,
                sender_name=sender_name,
                platform="messenger"
            )
            print(f"🤖 [এআই উত্তর]: \"{ai_reply}\"", flush=True)

            input_box = self.page_messenger.locator('div[role="textbox"][aria-label*="Message" i], div[role="textbox"]').first
            if not input_box.is_visible():
                return

            input_box.click()
            time.sleep(0.5)
            input_box.fill(ai_reply)
            time.sleep(0.8)
            self.page_messenger.keyboard.press("Enter")
            time.sleep(1.2)

            print("🚀 মেসেঞ্জারে উত্তর পাঠানো হয়েছে!\n", flush=True)
            self.replied_msg_history.add(history_key)
            send_telegram_alert(sender_name, last_text, ai_reply, event_type="messenger")

        except Exception:
            pass

    def scan_reels_comments(self):
        """ট্যাব ২-এ রিসেন্ট রিলসের নতুন কমেন্ট স্ক্যান করে সেফটি ডিলে সহকারে উত্তর দেয়।"""
        # নতুন দিন শুরু হলে কাউন্টার রিসেট
        current_day = datetime.now().day
        if current_day != self.last_day:
            self.today_comment_count = 0
            self.last_day = current_day

        if self.today_comment_count >= DAILY_MAX_COMMENTS:
            print(f"🛡️ আজকের কমেন্ট লিমিট ({DAILY_MAX_COMMENTS}টি) পূর্ণ হয়েছে। সুরক্ষার স্বার্থে কমেন্ট স্ক্যান স্থগিত রাখা হচ্ছে।", flush=True)
            return

        print("\n🔍 [ট্যাব ২] রিলসের নতুন কমেন্ট স্ক্যান করা হচ্ছে...", flush=True)
        try:
            self.page_reels.goto(JUBAYER_REELS_URL, wait_until="domcontentloaded", timeout=20000)
            time.sleep(3)

            reel_elements = self.page_reels.locator('a[href*="/reel/"]').all()
            reel_urls = []
            for r in reel_elements:
                try:
                    href = r.get_attribute("href") or ""
                    if href and "/reel/" in href and href not in reel_urls:
                        reel_urls.append(href)
                except Exception:
                    pass

            for idx, r_url in enumerate(reel_urls[:3]):
                if self.today_comment_count >= DAILY_MAX_COMMENTS:
                    break

                full_url = r_url if r_url.startswith("http") else f"https://www.facebook.com{r_url}"
                try:
                    self.page_reels.goto(full_url, wait_until="domcontentloaded", timeout=20000)
                    time.sleep(3)

                    reel_title = ""
                    try:
                        title_el = self.page_reels.locator('div[role="main"] h1, div[role="main"] div[dir="auto"]').first
                        if title_el.is_visible():
                            reel_title = title_el.inner_text().strip()[:80]
                    except Exception:
                        pass

                    comments = self.page_reels.locator('div[role="article"]').all()
                    for article in comments:
                        if self.today_comment_count >= DAILY_MAX_COMMENTS:
                            break

                        raw_text = article.inner_text().strip()
                        if not raw_text or "author" in raw_text.lower() or "jubayer ahmad" in raw_text.lower():
                            continue

                        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
                        commenter_name = lines[0] if lines else "ফেসবুক ব্যবহারকারী"

                        clean_lines = []
                        for l in lines[1:]:
                            if l.isdigit() and len(l) < 4:
                                continue
                            if not any(btn_w in l.lower() for btn_w in ["reply", "hide", "like", "share", "author", "উত্তর দিন", "লুকান", "লাইক", "1h", "2h", "3h", "d", "w"]):
                                l_cleaned = l.lstrip("· •-  ").strip()
                                if l_cleaned and not l_cleaned.isdigit():
                                    clean_lines.append(l_cleaned)
                        comment_body = " ".join(clean_lines) if clean_lines else raw_text

                        comment_key = f"{full_url}_{commenter_name}_{comment_body[:30]}"
                        if comment_key in self.replied_comments:
                            continue

                        print(f"\n💬 [নতুন কমেন্ট - {commenter_name}]: \"{comment_body}\"", flush=True)
                        print("🧠 জেমিনি এআই কমেন্ট রিপ্লাই তৈরি করছে...", flush=True)

                        ai_reply = call_comment_ai(
                            commenter_name=commenter_name,
                            comment_text=comment_body,
                            post_context=reel_title
                        )
                        print(f"🤖 [এআই উত্তর]: \"{ai_reply}\"", flush=True)

                        reply_btn = article.locator('div[role="button"]:has-text("Reply"), span:has-text("Reply"), div[role="button"]:has-text("উত্তর দিন")').first
                        if reply_btn.is_visible():
                            reply_btn.click()
                            time.sleep(1.5)

                            textboxes = self.page_reels.locator('div[role="textbox"][contenteditable="true"]').all()
                            if textboxes:
                                reply_box = textboxes[-1]
                                reply_box.click()
                                time.sleep(0.5)

                                for char in ai_reply:
                                    self.page_reels.keyboard.type(char, delay=random.randint(20, 50))
                                time.sleep(1)

                                self.page_reels.keyboard.press("Enter")
                                time.sleep(3)
                                print("✅ রিলসে কমেন্ট রিপ্লাই সফলভাবে পোস্ট হয়েছে!", flush=True)

                                send_telegram_alert(commenter_name, comment_body, ai_reply, event_type="comment")

                                self.replied_comments[comment_key] = {
                                    "commenter": commenter_name,
                                    "comment": comment_body,
                                    "reply": ai_reply,
                                    "mode": "live",
                                    "time": datetime.now().isoformat()
                                }
                                save_replied_comments(self.replied_comments)
                                self.today_comment_count += 1

                                # অ্যান্টি-বট সেফটি ডিলে: ১ থেকে ২ মিনিট স্বাভাবিক বিরতি
                                delay = random.randint(65, 115)
                                print(f"⏳ অ্যান্টি-বট সুরক্ষার জন্য {delay} সেকেন্ড বিরতি...", flush=True)
                                time.sleep(delay)

                except Exception:
                    pass

        except Exception as e:
            print(f"⚠️ রিলস কমেন্ট স্ক্যান এরর: {e}", flush=True)

        print("👍 রিলস স্ক্যান সম্পন্ন। আবার মেসেঞ্জার মনিটরিংয়ে ফিরে যাওয়া হচ্ছে।\n", flush=True)

    def run_master_loop(self):
        print("=================================================================")
        print("🚀 JUBAYER.DEV ALL-IN-ONE DESKTOP AI AUTOMATOR IS RUNNING!")
        print("⚡ [ট্যাব ১] মেসেঞ্জার আনরিড চ্যাট সার্বক্ষণিক মনিটর হচ্ছে")
        print("💬 [ট্যাব ২] প্রতি ১০ মিনিট পর পর রিলসের নতুন কমেন্ট রিপ্লাই দেওয়া হচ্ছে")
        print("📱 প্রতিটি রিপ্লাই রিয়েলটাইমে আপনার টেলিগ্রাম বটে পৌঁছে যাবে")
        print("🛡️ শতভাগ সেফটি ডিলে ও নো-কনফ্লিক্ট সিঙ্গেল ব্রাউজার মোড সক্রিয়")
        print("=================================================================\n")

        self.start()
        self.last_comment_check = time.time()

        try:
            while True:
                # ১. মেসেঞ্জার স্ক্যান (প্রতি ৫ সেকেন্ড)
                self.scan_messenger()

                # ২. প্রতি ১০ মিনিট পর রিলস কমেন্ট স্ক্যান
                now = time.time()
                if now - self.last_comment_check >= COMMENT_CHECK_INTERVAL:
                    self.scan_reels_comments()
                    self.last_comment_check = time.time()

                time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 ব্যবহারকারী দ্বারা মাস্টার বট বন্ধ করা হয়েছে।")
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
    automator = MasterDesktopAutomator(headless=False)
    automator.run_master_loop()
