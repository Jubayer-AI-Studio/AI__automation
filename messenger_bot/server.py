# -*- coding: utf-8 -*-
"""
=============================================================================
🌐 JUBAYER.DEV OMNICHANNEL AI WEBHOOK SERVER (PHASE 1 PRODUCTION)
=============================================================================
এই সার্ভারটি একটি সার্বজনীন এআই হাব (Universal AI Hub) হিসেবে কাজ করে:
  ১. WhatsApp, Facebook Messenger, Instagram, TikTok ও Telegram সাপোর্ট
  ২. ইনকামিং মেসেজের উৎস (Platform) স্বয়ংক্রিয়ভাবে শনাক্তকরণ
  ৩. সেন্ট্রাল লিড ডাটাবেজ ইন্টিগ্রেশন ও সরাসরি টেলিগ্রাম লিড অ্যালার্ট
  ৪. নেটিভ টেলিগ্রাম বট ওয়েবহুক হ্যান্ডলার (`/telegram-webhook`)
  ৫. সংরক্ষিত সব ক্লায়েন্ট লিড দেখার জন্য এপিআই (`/api/leads`)
=============================================================================
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import os
import requests
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flask import Flask, request, jsonify, Response
from messenger_bot.agent_brain import call_gemini_api, call_jubayer_personal_ai
from messenger_bot.leads_db import get_all_leads
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "jubayer_dev_webhook_2026")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN", "")

app = Flask(__name__)

# জুবায়ের ভাই যখন ভিডিও বা পোস্ট রেন্ডার করতে বলবেন, পিসির জন্য জব কিউ
PENDING_JOBS = []


def send_telegram_alert(sender_name: str, incoming_msg: str, ai_reply: str):
    """টেলিগ্রামে ক্লাউড মেসেঞ্জার অ্যালার্ট পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    alert_text = (
        f"⚡ <b>ফেসবুক মেসেঞ্জারে ক্লাউড এআই অটো-রিপ্লাই দিয়েছে!</b>\n\n"
        f"👤 <b>ক্লায়েন্ট:</b> {sender_name}\n"
        f"💬 <b>মেসেজ:</b> {incoming_msg}\n"
        f"🤖 <b>এআই উত্তর:</b>\n{ai_reply}\n\n"
        f"⏰ <i>সময়: {datetime.now().strftime('%I:%M %p, %d %b %Y')}</i>"
    )
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": alert_text, "parse_mode": "HTML"},
            timeout=8
        )
    except Exception:
        pass


def send_meta_messenger_reply(recipient_id: str, message_text: str):
    """মেটার অফিসিয়াল গ্রাফ এপিআই দিয়ে মেসেঞ্জারে সরাসরি রিপ্লাই সেন্ড করে।"""
    token = os.getenv("FB_PAGE_ACCESS_TOKEN", "").strip() or FB_PAGE_ACCESS_TOKEN
    if not token:
        print("[Meta Send] Warning: FB_PAGE_ACCESS_TOKEN সেট করা নেই।")
        return False
    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={token}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        print(f"[Meta Send Response] {res.status_code}")
        return res.status_code == 200
    except Exception as e:
        print(f"[Meta Send Exception] {e}")
        return False



def detect_platform(data: dict, args: dict) -> str:
    """ইনকামিং রিকোয়েস্ট থেকে প্ল্যাটফর্ম (WhatsApp, Messenger, Instagram, TikTok) শনাক্ত করে।"""
    # ১. URL কুয়েরি প্যারামিটার চেক
    if "platform" in args:
        return args.get("platform", "general").lower()

    # ২. AutoResponder অ্যাপের প্যাকেজ নাম চেক
    pkg = (data.get("appPackageName") or data.get("messengerPackageName") or "").lower()

    if any(k in pkg for k in ["wa", "whatsapp"]):
        return "whatsapp"
    elif any(k in pkg for k in ["ig", "instagram"]):
        return "instagram"
    elif any(k in pkg for k in ["fb", "orca", "messenger"]):
        return "messenger"
    elif any(k in pkg for k in ["tiktok", "musically"]):
        return "tiktok"
    elif any(k in pkg for k in ["telegram", "chatapp"]):
        return "telegram"

    return "messenger"


@app.route("/", methods=["GET", "POST"])
@app.route("/webhook", methods=["GET", "POST"])
def unified_webhook():
    """
    Universal Omnichannel Webhook (WhatsApp, Messenger, Instagram, TikTok)
    GET ও POST উভয় মেথড সমর্থন করে এবং গ্যারান্টি সহকারে replies প্রদান করে।
    """
    sender_name = "someone"
    sender_id = "user_default"
    incoming_msg = ""

    data = request.get_json(silent=True) or {}
    args = request.args.to_dict()

    platform = detect_platform(data, args)

    # -------------------------------------------------------------
    # 🌟 ১. মেটার অফিশিয়াল ওয়েবভেরিফিকেশন হ্যান্ডলার (GET hub.challenge)
    # -------------------------------------------------------------
    if request.method == "GET":
        mode = args.get("hub.mode")
        token = args.get("hub.verify_token")
        challenge = args.get("hub.challenge")
        if mode and token:
            if mode == "subscribe" and token == FB_VERIFY_TOKEN:
                print("✅ [Meta Webhook] ভেরিফিকেশন সফলভাবে সম্পন্ন হয়েছে!")
                return Response(challenge, mimetype='text/plain', status=200)
            else:
                return "Forbidden", 403

    # -------------------------------------------------------------
    # 🌟 ২. মেটার অফিশিয়াল ফেসবুক পেজ মেসেঞ্জার হ্যান্ডলার (POST object == 'page')
    # -------------------------------------------------------------
    if isinstance(data, dict) and data.get("object") == "page":
        try:
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    sender_id = messaging_event.get("sender", {}).get("id")
                    if "message" in messaging_event and not messaging_event.get("message", {}).get("is_echo"):
                        user_text = messaging_event["message"].get("text", "")
                        if user_text:
                            print(f"\n[Meta Messenger In] ক্লায়েন্ট ({sender_id}): {user_text}")
                            ai_reply = call_gemini_api(
                                user_message=user_text,
                                sender_id=str(sender_id),
                                sender_name=f"Client_{sender_id[:6]}",
                                platform="messenger"
                            )
                            print(f"[Meta Messenger Out] AI Reply: {ai_reply}")
                            send_meta_messenger_reply(sender_id, ai_reply)
                            send_telegram_alert(f"Meta Client ({sender_id[:6]})", user_text, ai_reply)
            return "EVENT_RECEIVED", 200
        except Exception as ex:
            print(f"[Meta Webhook Event Error] {ex}")
            return "EVENT_RECEIVED", 200

    try:
        # ১. JSON বডি পার্সিং (AutoResponder ফরম্যাট)
        if "query" in data and isinstance(data["query"], dict):
            q = data["query"]
            sender_name = q.get("sender", "someone")
            sender_id = str(q.get("sender", sender_name))
            incoming_msg = q.get("message", "")
        else:
            sender_name = data.get("sender", "someone")
            sender_id = str(data.get("sender_id", sender_name))
            incoming_msg = data.get("message", "")

        if not incoming_msg and "text" in data:
            incoming_msg = data.get("text", "")

        # ২. URL কুয়েরি পার্সিং (GET টেস্ট ও প্যারামিটার)
        if not incoming_msg:
            incoming_msg = args.get("message") or args.get("text") or args.get("query") or ""
            if "sender" in args:
                sender_name = args.get("sender")
                sender_id = sender_name

        print(f"[{platform.upper()} In] {sender_name}: {incoming_msg}")

        # টেস্ট বা পিং রিকোয়েস্টের জন্য ডিফল্ট সালাম
        if not incoming_msg or not incoming_msg.strip():
            return jsonify({
                "status": "online",
                "service": "Jubayer Sir's Omnichannel AI Assistant",
                "platform": platform,
                "replies": [
                    {
                        "message": "আসসালামু আলাইকুম। আমি জুবায়ের স্যারের পার্সোনাল এআই অ্যাসিস্ট্যান্ট।"
                    }
                ]
            })

        # এআই ব্রেইন থেকে উত্তর ও লিড সেভ
        ai_reply = call_gemini_api(
            user_message=incoming_msg,
            sender_id=sender_id,
            sender_name=sender_name,
            platform=platform
        )
        print(f"[{platform.upper()} Out] AI Reply: {ai_reply}\n")

        return jsonify({
            "replies": [
                {
                    "message": ai_reply
                }
            ]
        })
    except Exception as e:
        print(f"[Webhook Error] {e}")
        return jsonify({
            "replies": [
                {
                    "message": "আসসালামু আলাইকুম। আমি জুবায়ের স্যারের পার্সোনাল এআই অ্যাসিস্ট্যান্ট। আপনার বার্তাটি আমি নোট করে নিয়েছি।"
                }
            ]
        })


@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    """
    টেলিগ্রাম বট হ্যান্ডলার:
    - জুবায়ের ভাই মেসেজ দিলে পার্সোনাল এআই অ্যাসিস্ট্যান্ট হিসেবে উত্তর দেয় এবং ভিডিও/পোস্ট রেন্ডার কিউতে যোগ করে।
    - বহিরাগত কোনো ভিজিটর মেসেজ দিলে জুবায়ের স্যারের রিপ্রেজেন্টেটিভ হিসেবে উত্তর দেয়।
    """
    update = request.get_json(silent=True) or {}
    message = update.get("message", {})
    text = message.get("text", "").strip()
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    user_name = chat.get("first_name", "User")

    if not text or not chat_id:
        return jsonify({"ok": True})

    # ১. ইউজার কি জুবায়ের ভাই নিজে? (Boss / Creator)
    is_jubayer = str(chat_id) == str(TELEGRAM_CHAT_ID) or str(chat_id) == "8273323826"

    if is_jubayer:
        text_lower = text.lower()
        # ক. ভিডিও বানানোর নির্দেশ
        if any(kw in text_lower for kw in ["ভিডিও", "রিল", "রিলস", "video", "reel", "/video"]):
            job_id = f"job_vid_{int(datetime.now().timestamp())}"
            PENDING_JOBS.append({
                "job_id": job_id,
                "type": "video",
                "prompt": text,
                "chat_id": chat_id,
                "created_at": datetime.now().strftime("%I:%M %p, %d %b %Y")
            })
            ai_reply = (
                "🚀 জুবায়ের ভাই, আপনার ভিডিও তৈরির কম্যান্ড পেয়েছি!\n\n"
                "💻 আপনার পিসির এআই ভিডিও রেন্ডারিং পাইপলাইন স্বয়ংক্রিয়ভাবে ব্যাকগ্রাউন্ডে শুরু হচ্ছে...\n"
                "⏱️ অডিও সিন্থেসিস, বাংলা সাবটাইটেল ও মোশন রেন্ডার সম্পন্ন হলেই সরাসরি এই চ্যাটে ফুল ক্রিয়েটর কিট (ভিডিও + ফটো কার্ড + ক্যাপশন) পৌঁছে যাবে!"
            )
        # খ. পোস্ট বা ফটো কার্ড বানানোর নির্দেশ
        elif any(kw in text_lower for kw in ["পোস্ট", "ফটো কার্ড", "ক্যাপশন", "/post", "post"]):
            post_caption = call_jubayer_personal_ai(
                f"জুবায়ের ভাই একটি নতুন সোশ্যাল মিডিয়া পোস্ট বা স্ট্যাটাস চেয়েছেন। তার নির্দেশ: {text}। "
                "একটি আকর্ষণীয়, প্রফেশনাল এবং এঙ্গেজিং পোস্ট লিখে দিন সাথে পাওয়ারফুল হুক ও ট্রেন্ডিং হ্যাশট্যাগ।"
            )
            job_id = f"job_post_{int(datetime.now().timestamp())}"
            PENDING_JOBS.append({
                "job_id": job_id,
                "type": "post_card",
                "prompt": text,
                "caption": post_caption,
                "chat_id": chat_id,
                "created_at": datetime.now().strftime("%I:%M %p, %d %b %Y")
            })
            ai_reply = (
                f"📝 জুবায়ের ভাই, আপনার সোশ্যাল মিডিয়া পোস্ট প্রস্তুত:\n\n"
                f"{post_caption}\n\n"
                f"🎨 (আপনার পিসির এআই ফটো কার্ড জেনারেটর ব্যাকগ্রাউন্ডে কার্ড তৈরি করে টেলিগ্রামে পাঠিয়ে দেবে।)"
            )
        # গ. সাধারণ কথোপকথন, কোডিং হেল্প, টেকনিক্যাল সমস্যা সমাধান বা যে কোনো প্রশ্ন
        else:
            ai_reply = call_jubayer_personal_ai(text)
    else:
        # বহিরাগত ক্লায়েন্ট বা ভিজিটরদের জন্য বিজনেস অ্যাসিস্ট্যান্ট
        ai_reply = call_gemini_api(
            user_message=text,
            sender_id=str(chat_id),
            sender_name=user_name,
            platform="telegram"
        )

    # টেলিগ্রামে উত্তর পাঠানো
    if TELEGRAM_BOT_TOKEN:
        send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        try:
            requests.post(send_url, json={"chat_id": chat_id, "text": ai_reply}, timeout=10)
        except Exception as ex:
            print(f"[Telegram Send Error] {ex}")

    return jsonify({"ok": True})


@app.route("/api/jobs/pending", methods=["GET"])
def get_pending_jobs():
    """পিসির লোকাল ওয়ার্কারের জন্য কিউতে থাকা পেন্ডিং জবগুলোর তালিকা।"""
    return jsonify({
        "count": len(PENDING_JOBS),
        "jobs": PENDING_JOBS
    })


@app.route("/api/jobs/complete", methods=["POST"])
def complete_job():
    """পিসিতে জব সম্পন্ন হলে কিউ থেকে তা সরিয়ে ফেলার এপিআই।"""
    global PENDING_JOBS
    data = request.get_json(silent=True) or {}
    job_id = data.get("job_id")
    if job_id:
        PENDING_JOBS = [j for j in PENDING_JOBS if j.get("job_id") != job_id]
    elif PENDING_JOBS:
        PENDING_JOBS.pop(0)
    return jsonify({"ok": True, "remaining": len(PENDING_JOBS)})


@app.route("/api/leads", methods=["GET"])
def list_leads():
    """সব সংরক্ষিত লিডের তালিকা প্রদর্শনের এপিআই।"""
    leads = get_all_leads(limit=100)
    return jsonify({
        "total": len(leads),
        "leads": leads
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Jubayer Sir's Omnichannel AI Webhook Server starting on port {port}...")
    app.run(host="0.0.0.0", port=port)
