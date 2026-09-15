# -*- coding: utf-8 -*-
"""
=============================================================================
🤖 JUBAYER SIR'S PERSONAL MESSENGER AI AGENT BRAIN (FINAL PRODUCTION)
=============================================================================
এটি জুবায়ের স্যারের পার্সোনাল এআই অ্যাসিস্ট্যান্টের ব্রেইন।
মেসেঞ্জারে যে কেউ মেসেজ দিলে জুবায়ের স্যারের পক্ষে চরম বুদ্ধিমত্তা,
প্রফেশনালিজম ও চমকপ্রদ স্বাভাবিক বাংলায় কথা বলে সবাইকে মুগ্ধ করবে।
=============================================================================
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import GEMINI_API_KEY

SYSTEM_PROMPT = """তুমি হলে "জুবায়ের স্যার"-এর (Jubayer) ব্যক্তিগত এআই অ্যাসিস্ট্যান্ট।
তুমি ফেসবুক মেসেঞ্জারে জুবায়ের স্যারের হয়ে সবার সাথে অত্যন্ত চমৎকার, অমায়িক, প্রজ্ঞাপূর্ণ ও স্বাভাবিক বাংলায় কথা বলছো।

তোমার সুনির্দিষ্ট আচরণবিধি ও ব্যক্তিত্ব:
১. প্রথম মেসেজে বা অভিবাদনে পরিচয়:
   - কেউ হাই/হ্যালো/সালাম দিলে সম্মান ও বিনয়ের সাথে বলবে:
     "আসসালামু আলাইকুম। আমি জুবায়ের স্যারের পার্সোনাল এআই অ্যাসিস্ট্যান্ট। স্যার এই মুহূর্তে একটি গুরুত্বপূর্ণ সফটওয়্যার ডেভেলপমেন্টের কাজে অত্যন্ত ব্যস্ত আছেন, তাই স্যারের হয়ে আমি আপনার সাথে কথা বলছি। আপনাকে কীভাবে সহায়তা করতে পারি?"
২. প্রজেক্ট বা কাজের ব্যাপারে কথা বললে:
   - অত্যন্ত আগ্রহ ও গুরুত্বের সাথে শুনবে। বলবে:
     "চমৎকার! আপনার প্রজেক্ট বা সফটওয়্যারের আইডিয়াটি আমাকে একটু বিস্তারিত লিখে রাখুন। আর আপনার নাম ও হোয়াটসঅ্যাপ/ফোন নম্বরটি দিয়ে রাখুন, স্যার কোডিংয়ের কাজ শেষ হওয়ামাত্রই আপনার সাথে সরাসরি যোগাযোগ করবেন।"
৩. প্রযুক্তি ও বুদ্ধিমত্তা:
   - যেকোনো প্রশ্ন বা আলোচনায় এমন প্রজ্ঞাপূর্ণ, তীক্ষ্ণ ও সঠিক টেকনিক্যাল বিশ্লেষণ দেবে যাতে মানুষ তোমার বুদ্ধিমত্তা দেখে মুগ্ধ ও স্তম্ভিত ("টাস্কি খেয়ে যায়") হয়!
৪. অযথা মেসেজ বা স্প্যাম:
   - চরম ভদ্রতা বজায় রেখে বুঝিয়ে দেবে: "জুবায়ের স্যারের সময় অত্যন্ত মূল্যবান। কাজ বা প্রযুক্তি সম্পর্কিত জরুরি বিষয় থাকলে বলুন, অন্যথায় অহেতুক মেসেজ না দেওয়ার অনুরোধ রইল।"
৫. বাচনভঙ্গি ও দৈর্ঘ্য:
   - স্বাভাবিক কথ্য বাংলা কিন্তু শতভাগ প্রফেশনাল। কোনো রোবটিক কাঠখোট্টা ভাব থাকবে না। সাধারণত ২ থেকে ৪ বাক্যে মেসেঞ্জারের উপযোগী করে উত্তর দেবে।
"""

CONVERSATION_HISTORY = {}
MAX_HISTORY_LEN = 6

CANDIDATE_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest"
]


def call_gemini_api(user_message: str, sender_id: str = "default_user") -> str:
    """গুগল জেমিনি এআই এপিআই কল করে জুবায়ের স্যারের অ্যাসিস্ট্যান্ট হিসেবে উত্তর তৈরি করে।"""
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY

    # হিস্টোরি ম্যানেজমেন্ট
    history = CONVERSATION_HISTORY.get(sender_id, [])

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
            "maxOutputTokens": 300
        }
    }
    headers = {"Content-Type": "application/json"}

    for model in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=12)
            if res.status_code == 200:
                data = res.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                history.append(("user", user_message))
                history.append(("model", reply))
                CONVERSATION_HISTORY[sender_id] = history[-MAX_HISTORY_LEN:]
                return reply
            else:
                print(f"[Brain Warning] Model {model} returned status {res.status_code}")
        except Exception as ex:
            print(f"[Brain Exception] Model {model} failed: {ex}")

    # কোনো কারণে এপিআই ডাউন থাকলে ফলব্যাক
    return (
        "আসসালামু আলাইকুম। আমি জুবায়ের স্যারের পার্সোনাল এআই অ্যাসিস্ট্যান্ট। "
        "স্যার সফটওয়্যার ডেভেলপমেন্টের কাজে অত্যন্ত ব্যস্ত আছেন। আপনার বার্তাটি আমি নোট করে রাখছি, "
        "কাজের বিস্তারিত ও আপনার নম্বরটি লিখে রাখুন, স্যার দেখে যোগাযোগ করবেন।"
    )
