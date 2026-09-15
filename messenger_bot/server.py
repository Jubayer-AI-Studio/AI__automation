# -*- coding: utf-8 -*-
"""
=============================================================================
🌐 FACEBOOK MESSENGER AI WEBHOOK SERVER
=============================================================================
এটি একটি ফ্লাস্ক (Flask) লাইটওয়েট ওয়েব সার্ভার।
মোবাইলের 'AutoResponder for FB Messenger' অ্যাপ থেকে ওয়েবহুকে মেসেজ আসবে
এবং এআই ব্রেইন কয়েক সেকেন্ডে মানুষের মতো প্রফেশনাল উত্তর ব্যাক পাঠাবে।
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

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "Jubayer Sir's Facebook Messenger AI Assistant",
        "author": "Jubayer.dev",
        "message": "AI Webhook Server is running smoothly 24/7!"
    })


@app.route("/webhook", methods=["POST", "GET"])
def messenger_webhook():
    """
    AutoResponder for FB Messenger Webhook Handler
    App Payload ফরম্যাট:
      {"query": {"sender": "Rahim", "message": "Hi"}}
      অথবা
      {"sender": "...", "message": "..."}
    App Expected Response ফরম্যাট:
      {"replies": [{"message": "AI reply text"}]}
    """
    if request.method == "GET":
        return jsonify({"status": "Webhook endpoint is active. Use POST."})

    try:
        data = request.get_json(silent=True) or {}
        sender = "someone"
        incoming_msg = ""

        # AutoResponder for FB Messenger এর বিভিন্ন পেলোড পার্সিং
        if "query" in data and isinstance(data["query"], dict):
            sender = data["query"].get("sender", "someone")
            incoming_msg = data["query"].get("message", "")
        else:
            sender = data.get("sender", "someone")
            incoming_msg = data.get("message", "")

        if not incoming_msg and "text" in data:
            incoming_msg = data.get("text", "")

        print(f"[Messenger In] Sender: {sender} | Message: {incoming_msg}")

        if not incoming_msg.strip():
            return jsonify({"replies": []})

        # এআই ব্রেইন থেকে উত্তর নেওয়া
        ai_reply = call_gemini_api(user_message=incoming_msg, sender_id=str(sender))
        print(f"[Messenger Out] AI Reply: {ai_reply}\n")

        # AutoResponder অ্যাপ যে ফরম্যাট পছন্দ করে
        return jsonify({
            "replies": [
                {
                    "message": ai_reply
                }
            ]
        })
    except Exception as e:
        print(f"[Server Error] {e}")
        return jsonify({"replies": [{"message": "ধন্যবাদ। বার্তাটি পৌঁছেছে।"}]})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Jubayer Sir's Messenger AI Webhook Server starting on port {port}...")
    app.run(host="0.0.0.0", port=port)
