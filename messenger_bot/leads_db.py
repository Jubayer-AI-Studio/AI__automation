# -*- coding: utf-8 -*-
"""
=============================================================================
🗄️ JUBAYER.DEV CENTRAL LEAD DATABASE & TELEGRAM DISPATCHER
=============================================================================
সব সোশ্যাল মিডিয়া (WhatsApp, Messenger, Instagram, Telegram, TikTok) থেকে আসা
সম্ভাব্য ক্লায়েন্ট ও ফোন নম্বরগুলো স্বয়ংক্রিয়ভাবে এই ডাটাবেজে সংরক্ষিত হয়
এবং তাৎক্ষণিকভাবে জুবায়ের স্যারের ব্যক্তিগত টেলিগ্রামে অ্যালার্ট পাঠিয়ে দেয়।
=============================================================================
"""

import re
import sqlite3
import requests
from datetime import datetime
from pathlib import Path
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "leads.db"


def init_db():
    """ডাটাবেজ ও টেবিল তৈরি নিশ্চিত করে।"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            sender_name TEXT,
            sender_id TEXT,
            phone TEXT,
            email TEXT,
            project_details TEXT,
            last_message TEXT,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def extract_contact_info(text: str) -> tuple:
    """মেসেজের ভেতর থেকে মোবাইল/হোয়াটসঅ্যাপ নম্বর এবং ইমেইল খুঁজে বের করে।"""
    if not text:
        return None, None

    # ১. মোবাইল ও হোয়াটসঅ্যাপ নম্বর (বাংলাদেশী ০১... অথবা +৮৮০... অথবা আন্তর্জাতিক)
    phone_pattern = r'(?:(?:\+|00)880|0)?1[3-9]\d{8}|(?:\+\d{1,3}[- ]?)?\d{10,12}'
    phones = re.findall(phone_pattern, text.replace('-', '').replace(' ', ''))
    phone = phones[0] if phones else None

    # ২. ইমেইল ঠিকানা
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else None

    return phone, email


def send_telegram_lead_alert(lead: dict):
    """নতুন ক্লায়েন্ট বা ফোন নম্বর পাওয়ামাত্রই জুবায়ের স্যারের টেলিগ্রামে অ্যালার্ট পাঠায়।"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Lead Alert] Telegram token/chat_id missing!")
        return False

    platform_icons = {
        "whatsapp": "🟢 WhatsApp",
        "messenger": "🔵 Messenger",
        "instagram": "🟣 Instagram",
        "telegram": "✈️ Telegram",
        "tiktok": "🎵 TikTok",
        "linkedin": "💼 LinkedIn"
    }

    icon_platform = platform_icons.get(lead.get("platform", "").lower(), f"🌐 {lead.get('platform')}")

    msg = (
        f"🔔 <b>নতুন ক্লায়েন্ট লিড অ্যালার্ট!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 <b>প্ল্যাটফর্ম:</b> {icon_platform}\n"
        f"👤 <b>নাম:</b> {lead.get('sender_name', 'অজ্ঞাত')}\n"
        f"📞 <b>ফোন/হোয়াটসঅ্যাপ:</b> {lead.get('phone', 'পাওয়া যায়নি')}\n"
        f"📧 <b>ইমেইল:</b> {lead.get('email', 'পাওয়া যায়নি')}\n"
        f"💬 <b>শেষ বার্তা:</b>\n<i>\"{lead.get('last_message', '')}\"</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>জুবায়ের স্যার, এখনই ক্লায়েন্টের সাথে যোগাযোগ করে ডিল ফাইনাল করুন!</i>"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.status_code == 200
    except Exception as e:
        print(f"[Lead Alert Error] {e}")
        return False


def save_or_update_lead(platform: str, sender_name: str, sender_id: str, message: str, project_details: str = None) -> dict:
    """নতুন লিড সেভ করে অথবা পূর্বের লিড আপডেট করে এবং প্রয়োজনমতো অ্যালার্ট পাঠায়।"""
    init_db()
    phone, email = extract_contact_info(message)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # পূর্বের রেকর্ড চেক
    cursor.execute("SELECT id, phone, email, project_details FROM leads WHERE sender_id = ? AND platform = ?", (sender_id, platform))
    row = cursor.fetchone()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_new_contact_info = False

    if row:
        lead_id, old_phone, old_email, old_proj = row
        new_phone = phone or old_phone
        new_email = email or old_email
        new_proj = project_details or old_proj

        if (phone and not old_phone) or (email and not old_email):
            is_new_contact_info = True

        cursor.execute("""
            UPDATE leads
            SET sender_name = ?, phone = ?, email = ?, project_details = ?, last_message = ?, updated_at = ?
            WHERE id = ?
        """, (sender_name, new_phone, new_email, new_proj, message, now, lead_id))
    else:
        cursor.execute("""
            INSERT INTO leads (platform, sender_name, sender_id, phone, email, project_details, last_message, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (platform, sender_name, sender_id, phone, email, project_details, message, now, now))
        lead_id = cursor.lastrowid
        new_phone = phone
        new_email = email
        if phone or email:
            is_new_contact_info = True

    conn.commit()
    conn.close()

    lead_data = {
        "id": lead_id,
        "platform": platform,
        "sender_name": sender_name,
        "sender_id": sender_id,
        "phone": new_phone,
        "email": new_email,
        "last_message": message
    }

    # যদি নতুন কোনো ফোন বা ইমেইল পাওয়া যায়, তৎক্ষণাৎ টেলিগ্রাম অ্যালার্ট ট্রিগার হবে
    if is_new_contact_info:
        print(f"[Lead Manager] 🎯 New contact info detected! Dispatching Telegram alert for {sender_name}...")
        send_telegram_lead_alert(lead_data)

    return lead_data


def get_all_leads(limit: int = 50):
    """সব সংরক্ষিত লিডের তালিকা দেয়।"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY updated_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print("✅ Leads database initialized successfully at:", DB_PATH)

    # টেস্ট ইনসার্ট
    sample_lead = save_or_update_lead(
        platform="whatsapp",
        sender_name="রাকিবুল হাসান",
        sender_id="8801711223344",
        message="ভাই একটা এআই সফটওয়্যার বানাবো, আমার নম্বর 01711223344"
    )
    print("Test lead saved:", sample_lead)
