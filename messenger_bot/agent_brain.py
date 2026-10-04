# -*- coding: utf-8 -*-
"""
=============================================================================
🤖 JUBAYER SIR'S OMNICHANNEL AI SALES ASSISTANT BRAIN (PHASE 1)
=============================================================================
এটি জুবায়ের স্যারের বহুমুখী (WhatsApp, Messenger, Instagram, Telegram, TikTok)
এআই সেলস অ্যাসিস্ট্যান্ট। এটি অমায়িক আলাপের মাধ্যমে ক্লায়েন্টের কাজের ধরন ও
বাজেট জেনে তাদের ফোন/হোয়াটসঅ্যাপ নম্বর সংগ্রহ করে এবং ডাটাবেজে সংরক্ষণ করে।
=============================================================================
"""

import os
import sys
import json
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

from src.config import GEMINI_API_KEY, GROK_API_KEY
from messenger_bot.leads_db import save_or_update_lead, extract_contact_info

SYSTEM_PROMPT = """তুমি হলে "জুবায়ের এআই স্টুডিও" (Jubayer AI Studio) এবং জুবায়ের আহমেদ (Jubayer Ahmad)-এর অফিশিয়াল হাইপার-ইন্টেলিজেন্ট এআই অ্যাসিস্ট্যান্ট।
তুমি Facebook Messenger, WhatsApp, Instagram ও কমেন্ট সেকশনে জুবায়ের ভাইয়ের হয়ে সবার সাথে অত্যন্ত প্রজ্ঞাপূর্ণ, অমায়িক, প্রফেশনাল ও বুদ্ধিদীপ্ত বাংলায় কথা বলো।

জুবায়ের ভাই ও স্টুডিওর পরিচয়:
- জুবায়ের আহমেদ: এআই ও সফটওয়্যার সিস্টেমস আর্কিটেক্ট, ফাউন্ডার অব Jubayer AI Studio।
- অফিশিয়াল ওয়েবসাইট: https://jubayer-ai-studio.github.io/jubayer-ai-studio/
- সেবা/সার্ভিস: কাস্টম এআই এজেন্ট ও অটোমেশন, হাই-পারফরম্যান্স ওয়েব ডেভেলপমেন্ট (Next.js/React), পাইথন ব্যাকএন্ড, এআই ভিডিও/মিডিয়া প্রোডাকশন ও বিজনেস অটোমেশন।

তোমার মূল আচরণবিধি:
১. শুভেচ্ছা ও প্রাথমিক আলাপ:
   - কেউ হাই/হ্যালো/সালাম দিলে অত্যন্ত বিনয়ী ও অমায়িক ভাষায় বলবে:
     "আসসালামু আলাইকুম! আমি জুবায়ের ভাইয়ের পার্সোনাল এআই অ্যাসিস্ট্যান্ট। ভাইয়া এই মুহূর্তে একটি গুরুত্বপূর্ণ সফটওয়্যার আর্কিটেকচারের কাজে ল্যাবে আছেন, তাই উনার হয়ে আমি আপনার সাথে কথা বলছি। আপনার প্রজেক্ট বা কাজের ব্যাপারে কীভাবে সহায়তা করতে পারি বলুন?"
২. কাজ, প্রজেক্ট বা সার্ভিসের কথা বললে (স্মার্ট সেলস কনভার্সন):
   - অত্যন্ত গুরুত্ব ও আগ্রহ নিয়ে শুনবে। বলবে:
     "চমৎকার আইডিয়া! আপনার প্রজেক্টের রিকোয়ারমেন্টটি সংক্ষেপে একটু লিখে রাখুন। আর আপনার ফোন বা হোয়াটসঅ্যাপ নম্বরটি দিয়ে রাখলে, ভাইয়া কাজ শেষ হওয়ামাত্রই সরাসরি আপনার সাথে যোগাযোগ করে একটি পারফেক্ট সমাধান ও বাজেট জানিয়ে দেবেন ইনশাআল্লাহ।"
   - প্রয়োজনে আমাদের অফিশিয়াল ওয়েবসাইট লিংক শেয়ার করবে: https://jubayer-ai-studio.github.io/jubayer-ai-studio/
৩. ফোন নম্বর বা হোয়াটসঅ্যাপ দিলে:
   - আন্তরিকভাবে ধন্যবাদ জানাবে:
     "অসংখ্য ধন্যবাদ! আপনার যোগাযোগের নম্বরটি সংরক্ষিত হয়েছে। জুবায়ের ভাইয়া দ্রুতই সরাসরি আপনার সাথে হোয়াটসঅ্যাপে যোগাযোগ করবেন।"
৪. টেক আলোচনা ও বুদ্ধিমত্তা:
   - টেকনিক্যাল বা যেকোনো জটিল প্রশ্নে এমন অগাধ জ্ঞান ও প্রজ্ঞা প্রকাশ করবে যেন ক্লায়েন্ট তোমার অসাধারণ বুদ্ধিমত্তা দেখে মুগ্ধ হয়ে যায়!
৫. বাচনভঙ্গি ও আকার:
   - সম্পূর্ণ প্রফেশনাল ও ঝরঝরে কথ্য বাংলা। মেসেঞ্জারের উপযোগী ২ থেকে ৪ লাইনের চমৎকার ও সুনির্দিষ্ট উত্তর দেবে।
"""

CONVERSATION_HISTORY = {}
MAX_HISTORY_LEN = 8

CANDIDATE_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest"
]


def call_grok_api(user_message: str, system_prompt: str = SYSTEM_PROMPT, history: list = None, max_tokens: int = 400) -> str:
    """xAI Grok API কল করে অতি-উচ্চ বুদ্ধিমত্তাসম্পন্ন (Hyper-Intelligent) উত্তর তৈরি করে।"""
    api_key = os.getenv("GROK_API_KEY", "").strip() or os.getenv("XAI_API_KEY", "").strip() or GROK_API_KEY
    if not api_key:
        return ""

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        for role, text in history:
            r = "assistant" if role in ("model", "assistant") else "user"
            messages.append({"role": r, "content": text})
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # xAI Grok মডেলসমূহ (অগ্রাধিকার ভিত্তিতে)
    for model_name in ["grok-2-latest", "grok-beta", "grok-2"]:
        payload = {
            "messages": messages,
            "model": model_name,
            "temperature": 0.7,
            "max_tokens": max_tokens,
            "stream": False
        }
        try:
            res = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload, timeout=8.0)
            if res.status_code == 200:
                data = res.json()
                reply = data["choices"][0]["message"]["content"].strip()
                if reply:
                    return reply
            else:
                print(f"[Grok Warning] Model {model_name} returned status {res.status_code}")
        except Exception as ex:
            print(f"[Grok Exception] Model {model_name} failed: {ex}")

    return ""


def call_gemini_api(user_message: str, sender_id: str = "default_user", sender_name: str = "client", platform: str = "messenger") -> str:
    """গ্রোক (xAI) বা জেমিনি এআই এপিআই কল করে জুবায়ের ভাইয়ের অ্যাসিস্ট্যান্ট হিসেবে উত্তর তৈরি করে এবং লিড সেভ করে।"""
    # ১. সেন্ট্রাল ডাটাবেজে ক্লায়েন্ট মেসেজ ও লিড সেভ করা
    save_or_update_lead(
        platform=platform,
        sender_name=sender_name,
        sender_id=sender_id,
        message=user_message
    )

    # ২. ইউজারের চ্যাট হিস্টোরি ম্যানেজমেন্ট
    history_key = f"{platform}_{sender_id}"
    history = CONVERSATION_HISTORY.get(history_key, [])

    # ৩. Grok AI ট্রাই করা (সর্বোচ্চ অগ্রাধিকার - চরম বুদ্ধিমত্তা)
    grok_reply = call_grok_api(user_message=user_message, system_prompt=SYSTEM_PROMPT, history=history, max_tokens=350)
    if grok_reply:
        history.append(("user", user_message))
        history.append(("assistant", grok_reply))
        CONVERSATION_HISTORY[history_key] = history[-MAX_HISTORY_LEN:]
        return grok_reply

    # ৪. Gemini AI ট্রাই করা (ফলব্যাক)
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY
    if api_key:
        contents = []
        for role, text in history:
            contents.append({"role": role if role in ("user", "model") else "model", "parts": [{"text": text}]})
        contents.append({"role": "user", "parts": [{"text": user_message}]})

        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.75,
                "maxOutputTokens": 320
            }
        }
        headers = {"Content-Type": "application/json"}

        for idx, model in enumerate(CANDIDATE_MODELS):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            t_limit = 4.0 if idx == 0 else 2.5
            try:
                res = requests.post(url, headers=headers, json=payload, timeout=t_limit)
                if res.status_code == 200:
                    data = res.json()
                    reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    history.append(("user", user_message))
                    history.append(("model", reply))
                    CONVERSATION_HISTORY[history_key] = history[-MAX_HISTORY_LEN:]
                    return reply
                else:
                    print(f"[Brain Warning] Model {model} returned status {res.status_code}")
            except Exception as ex:
                print(f"[Brain Exception] Model {model} failed ({t_limit}s): {ex}")

    # ৫. কোনো কারণে এপিআই ডাউন থাকলে স্মার্ট ফলব্যাক
    return (
        "আসসালামু আলাইকুম। আমি জুবায়ের ভাইয়ের পার্সোনাল এআই অ্যাসিস্ট্যান্ট। "
        "ভাইয়া এই মুহূর্তে সফটওয়্যার ডেভেলপমেন্টের কাজে ল্যাবে ব্যস্ত আছেন। আপনার বার্তাটি নোট করা হয়েছে, "
        "কাজের বিস্তারিত ও হোয়াটসঅ্যাপ নম্বরটি দিয়ে রাখুন, ভাইয়া দ্রুত যোগাযোগ করবেন।"
    )



JUBAYER_PERSONAL_SYSTEM_PROMPT = """তুমি হলে জুবায়ের ভাইয়ের (Jubayer - 24yo AI & Software Systems Developer, Creator of Jubayer.dev) ব্যক্তিগত সুপার-ইন্টেলিজেন্ট এআই এক্সিকিউটিভ পার্টনার ও অ্যাসিস্ট্যান্ট।
তুমি জুবায়ের ভাইয়ের সাথে অত্যন্ত বন্ধুত্বপূর্ণ, আন্তরিক, বুদ্ধিদীপ্ত, প্রজ্ঞাপূর্ণ এবং স্বাভাবিক বাংলায় (প্রয়োজনে স্পষ্ট টেকনিক্যাল ইংরেজি সহ) কথা বলো।

তোমার মূল দায়িত্বসমূহ:
১. জুবায়ের ভাই তোমার বস ও ক্রিয়েটর। তাকে কখনো বলবে না "জুবায়ের স্যার ব্যস্ত আছেন" বা থার্ড-পার্টি হিসেবে কথা বলবে না। তাকে সরাসরি "জুবায়ের ভাই" বলে ডাকবে।
২. টেকনিক্যাল সলিউশন ও কোডিং: পাইথন, এআই, অটোমেশন, ওয়েব ডেভেলপমেন্ট, বা যেকোনো কোডিংয়ের ত্রুটি জিজ্ঞেস করলে সরাসরি একদম নিখুঁত কোড ও প্র্যাকটিক্যাল সমাধান দেবে।
৩. কনটেন্ট ও আইডিয়া: রিলস, ফেসবুক পোস্ট, ইউটিউব ভিডিও আইডিয়া, বা যেকোনো ক্রিয়েটিভ পরামর্শ চাইলে সাথে সাথে আকর্ষণীয় ও ভাইরাল ফরম্যাটে আইডিয়া দেবে।
৪. বিজনেস ও স্ট্র্যাটেজি: ক্লায়েন্ট হ্যান্ডেলিং, বাজেট, প্রজেক্ট প্ল্যানিং নিয়ে জিজ্ঞেস করলে অত্যন্ত শার্প ও বিজনেস-মাইন্ডেড পরামর্শ দেবে।
৫. সাহায্যকারী বাচনভঙ্গি: Antigravity যেমন কম্পিউটারে পেয়ার প্রোগ্রামার হিসেবে হেল্প করে, তুমি টেলিগ্রামে তার সার্বক্ষণিক বিশ্বস্ত এআই পার্টনার হিসেবে সেভাবেই হেল্প করবে।
"""


def call_jubayer_personal_ai(user_message: str) -> str:
    """জুবায়ের ভাইয়ের সাথে ১-অন-১ ব্যক্তিগত এআই পার্টনার হিসেবে কথা বলে ও সলিউশন দেয়।"""
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY

    history_key = "jubayer_personal_chat"
    history = CONVERSATION_HISTORY.get(history_key, [])

    # ১. Grok AI ট্রাই করা (১ম অগ্রাধিকার)
    grok_reply = call_grok_api(user_message=user_message, system_prompt=JUBAYER_PERSONAL_SYSTEM_PROMPT, history=history, max_tokens=800)
    if grok_reply:
        history.append(("user", user_message))
        history.append(("assistant", grok_reply))
        CONVERSATION_HISTORY[history_key] = history[-MAX_HISTORY_LEN:]
        return grok_reply

    contents = []
    for role, text in history:
        contents.append({"role": role if role in ("user", "model") else "model", "parts": [{"text": text}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    payload = {
        "system_instruction": {
            "parts": [{"text": JUBAYER_PERSONAL_SYSTEM_PROMPT}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800
        }
    }
    headers = {"Content-Type": "application/json"}

    for idx, model in enumerate(CANDIDATE_MODELS):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        t_limit = 6.0 if idx == 0 else 4.0
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=t_limit)
            if res.status_code == 200:
                data = res.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                history.append(("user", user_message))
                history.append(("model", reply))
                CONVERSATION_HISTORY[history_key] = history[-MAX_HISTORY_LEN:]
                return reply
        except Exception as ex:
            print(f"[Personal AI Error] {ex}")

    return "জুবায়ের ভাই, আপনার বার্তাটি পেয়েছি। সাময়িক নেটওয়ার্ক ধীরগতির কারণে আমি দ্রুত উত্তর প্রস্তুত করছি, আপনি কী বিষয়ে জানতে চান আমাকে বলুন।"


COMMENT_REPLY_SYSTEM_PROMPT = """তুমি হলে জুবায়ের আহমেদ (Jubayer.dev / Jubayer AI Studio)-এর ফেসবুক ভিডিও ও পোস্টের কমেন্ট অ্যাসিস্ট্যান্ট।
ফেসবুকে ভিডিও বা পোস্টে সাধারণ মানুষ ও ক্লায়েন্টরা বিভিন্ন মন্তব্য বা প্রশ্ন করেন। তোমাকে তাদের মন্তব্যের প্রেক্ষিতে একজন বাস্তবসম্মত, আন্তরিক, বুদ্ধিদীপ্ত ও প্রফেশনাল মানুষ হিসেবে সুন্দর ও সংক্ষিপ্ত কমেন্ট রিপ্লাই দিতে হবে।

নির্দেশনাবলী:
১. কমেন্টের উত্তর সবসময় ১ থেকে ৩ লাইনের মধ্যে সংক্ষিপ্ত ও সাবলীল রাখবে।
২. প্রশংসামূলক মন্তব্যে আন্তরিক কৃতজ্ঞতা ও ভালোবাসা প্রকাশ করবে (যেমন: "অনেক ধন্যবাদ ভাই!", "অনুপ্রেরণা দেওয়ার জন্য আন্তরিক কৃতজ্ঞতা!", "থ্যাংকস ব্রো! সাথে থাকবেন।")।
৩. টেকনিক্যাল প্রশ্ন থাকলে সংক্ষেপে স্পষ্ট ভাষায় সঠিক উত্তর দেবে।
৪. কাজের প্রস্তাব বা সার্ভিস নিয়ে জানতে চাইলে বলবে বিস্তারিত জানার জন্য সরাসরি ইনবক্সে মেসেজ দিতে।
৫. প্রতি উত্তরে একই কথা না বলে ভিন্ন ভিন্ন বৈচিত্র্যময় শব্দ ও বন্ধুত্বপূর্ণ বাচনভঙ্গি ব্যবহার করবে।
৬. কোনো উদ্ধৃতি চিহ্ন (" ") ছাড়া সরাসরি কমেন্টের উত্তরটি প্রদান করবে।
"""


def call_comment_ai(commenter_name: str, comment_text: str, post_context: str = "") -> str:
    """ফেসবুক পোস্ট বা ভিডিওর কমেন্টের জন্য স্মার্ট এআই রিপ্লাই তৈরি করে।"""
    user_prompt = f"মন্তব্যকারী: {commenter_name}\n"
    if post_context:
        user_prompt += f"পোস্ট/ভিডিওর বিষয়: {post_context}\n"
    user_prompt += f"মন্তব্য: {comment_text}\n\nউপযুক্ত, আন্তরিক ও চমৎকার ফেসবুক কমেন্ট রিপ্লাই দিন:"

    # ১. Grok ট্রাই করা
    grok_reply = call_grok_api(user_message=user_prompt, system_prompt=COMMENT_REPLY_SYSTEM_PROMPT, max_tokens=150)
    if grok_reply:
        if (grok_reply.startswith('"') and grok_reply.endswith('"')) or (grok_reply.startswith("'") and grok_reply.endswith("'")):
            grok_reply = grok_reply[1:-1].strip()
        return grok_reply

    # ২. Gemini ট্রাই করা
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY
    payload = {
        "system_instruction": {
            "parts": [{"text": COMMENT_REPLY_SYSTEM_PROMPT}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": user_prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 200
        }
    }
    headers = {"Content-Type": "application/json"}

    for idx, model in enumerate(CANDIDATE_MODELS):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        t_limit = 5.0 if idx == 0 else 3.0
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=t_limit)
            if res.status_code == 200:
                data = res.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if (reply.startswith('"') and reply.endswith('"')) or (reply.startswith("'") and reply.endswith("'")):
                    reply = reply[1:-1].strip()
                return reply
        except Exception as ex:
            print(f"[Comment AI Exception] Model {model}: {ex}")

    return f"অনেক অনেক ধন্যবাদ {commenter_name} ভাই! অনুপ্রেরণা দেওয়ার জন্য আন্তরিক কৃতজ্ঞতা।"



