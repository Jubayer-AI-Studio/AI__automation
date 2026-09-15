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

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flask import Flask, request, jsonify
from messenger_bot.agent_brain import call_gemini_api
from messenger_bot.leads_db import get_all_leads
from src.config import TELEGRAM_BOT_TOKEN

app = Flask(__name__)


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
    """সরাসরি টেলিগ্রাম বটের সাথে লাইভ টু-ওয়ে চ্যাটিং হ্যান্ডলার।"""
    update = request.get_json(silent=True) or {}
    message = update.get("message", {})
    text = message.get("text", "")
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    user_name = chat.get("first_name", "Telegram User")

    if not text or not chat_id:
        return jsonify({"ok": True})

    # এআই উত্তর তৈরি
    ai_reply = call_gemini_api(
        user_message=text,
        sender_id=str(chat_id),
        sender_name=user_name,
        platform="telegram"
    )

    # টেলিগ্রামে উত্তর পাঠানো
    if TELEGRAM_BOT_TOKEN:
        import requests
        send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(send_url, json={"chat_id": chat_id, "text": ai_reply}, timeout=8)

    return jsonify({"ok": True})


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
