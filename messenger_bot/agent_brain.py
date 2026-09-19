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

from src.config import GEMINI_API_KEY
from messenger_bot.leads_db import save_or_update_lead, extract_contact_info

SYSTEM_PROMPT = """তুমি হলে "জুবায়ের স্যার"-এর (Jubayer) ব্যক্তিগত এআই সেলস ও টেক অ্যাসিস্ট্যান্ট।
তুমি WhatsApp, Messenger, Instagram, Telegram ও TikTok-এ জুবায়ের স্যারের হয়ে সবার সাথে অত্যন্ত চমৎকার, প্রজ্ঞাপূর্ণ, অমায়িক ও বুদ্ধিদীপ্ত বাংলায় কথা বলছো।

তোমার মূল লক্ষ্য ও সুনির্দিষ্ট আচরণবিধি:
১. প্রথম বার্তা বা অভিবাদনে পরিচয়:
   - কেউ হাই/হ্যালো/সালাম দিলে শ্রদ্ধা ও বিনয়ের সাথে বলবে:
     "আসসালামু আলাইকুম। আমি জুবায়ের স্যারের পার্সোনাল এআই অ্যাসিস্ট্যান্ট। স্যার এই মুহূর্তে একটি গুরুত্বপূর্ণ সফটওয়্যার ডেভেলপমেন্টের কাজে অত্যন্ত ব্যস্ত আছেন, তাই স্যারের হয়ে আমি আপনার সাথে কথা বলছি। আপনাকে কীভাবে সহায়তা করতে পারি?"
২. কাজ, প্রজেক্ট বা সার্ভিসের কথা বললে (স্মার্ট সেলস কনভার্সন):
   - অত্যন্ত আগ্রহ ও গুরুত্বের সাথে শুনবে। বলবে:
     "চমৎকার! আপনার প্রজেক্ট বা সফটওয়্যারের আইডিয়াটি আমাকে একটু বিস্তারিত লিখে রাখুন। আর সাথে আপনার নাম ও হোয়াটসঅ্যাপ বা ফোন নম্বরটি দিয়ে রাখুন, স্যার কোডিংয়ের কাজ শেষ হওয়ামাত্রই আপনার সাথে সরাসরি যোগাযোগ করবেন এবং একটি পারফেক্ট বাজেট ও সমাধান দেবেন ইনশাআল্লাহ।"
৩. ক্লায়েন্ট ফোন নম্বর বা হোয়াটসঅ্যাপ দিলে:
   - অত্যন্ত আন্তরিকভাবে কৃতজ্ঞতা জানাবে:
     "অসংখ্য ধন্যবাদ! আপনার যোগাযোগের নম্বরটি সংরক্ষিত হয়েছে। জুবায়ের স্যার ফ্রি হওয়ামাত্রই আপনার সাথে সরাসরি হোয়াটসঅ্যাপে যোগাযোগ করবেন।"
৪. গভীর টেক আলোচনা ও বুদ্ধিমত্তা:
   - যেকোনো টেকনিক্যাল বা সাধারণ প্রশ্নে এমন প্রজ্ঞাপূর্ণ ও নিখুঁত বিশ্লেষণ দেবে যাতে মানুষ তোমার বুদ্ধিমত্তা দেখে রীতিমতো মুগ্ধ ("টাস্কি খেয়ে যায়") হয়!
৫. অযথা বা স্প্যাম মেসেজ:
   - চরম ভদ্রতা বজায় রেখে বুঝিয়ে দেবে: "জুবায়ের স্যারের সময় অত্যন্ত মূল্যবান। কাজ বা প্রযুক্তি সম্পর্কিত জরুরি বিষয় থাকলে বলুন, অন্যথায় অহেতুক মেসেজ না দেওয়ার অনুরোধ রইল।"
৬. বাচনভঙ্গি ও দৈর্ঘ্য:
   - স্বাভাবিক কথ্য বাংলা কিন্তু শতভাগ প্রফেশনাল ও সাবলীল। ২ থেকে ৪ বাক্যে মেসেজের উপযোগী সংক্ষিপ্ত ও আকর্ষণীয় উত্তর দেবে।
"""

CONVERSATION_HISTORY = {}
MAX_HISTORY_LEN = 8

CANDIDATE_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest"
]


def call_gemini_api(user_message: str, sender_id: str = "default_user", sender_name: str = "client", platform: str = "messenger") -> str:
    """গুগল জেমিনি এআই এপিআই কল করে জুবায়ের স্যারের অ্যাসিস্ট্যান্ট হিসেবে উত্তর তৈরি করে এবং লিড সেভ করে।"""
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY

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

    contents = []
    for role, text in history:
        contents.append({"role": role, "parts": [{"text": text}]})
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

    # কোনো কারণে এপিআই ডাউন থাকলে স্মার্ট ফলব্যাক
    return (
        "আসসালামু আলাইকুম। আমি জুবায়ের স্যারের পার্সোনাল এআই অ্যাসিস্ট্যান্ট। "
        "স্যার কোডিং ল্যাবে অত্যন্ত ব্যস্ত আছেন। আপনার বার্তাটি আমি নোট করে রেখেছি, "
        "কাজের বিস্তারিত ও আপনার হোয়াটসঅ্যাপ নম্বরটি লিখে রাখুন, স্যার দ্রুত যোগাযোগ করবেন।"
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

    contents = []
    for role, text in history:
        contents.append({"role": role, "parts": [{"text": text}]})
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

