# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import main
from thumbnail_card.thumbnail_maker import create_ai_photocard

RENDER_BASE_URL = os.getenv('RENDER_SERVER_URL', 'https://facebook-hx1b.onrender.com')
POLL_INTERVAL_SECONDS = 8

def send_telegram_msg(chat_id, text):
    if not TELEGRAM_BOT_TOKEN or not chat_id:
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={'chat_id': chat_id, 'text': text},
            timeout=10
        )
    except Exception as e:
        print(f'[Worker Telegram Error] {e}')

def process_job(job: dict):
    job_id = job.get('job_id')
    job_type = job.get('type', 'video')
    chat_id = job.get('chat_id', TELEGRAM_CHAT_ID)
    prompt = job.get('prompt', '')

    print(f"\n[{datetime.now().strftime('%I:%M:%S %p')}] ⚡ নতুন কাজ এসেছে: {job_type.upper()} (ID: {job_id})")

    if job_type == 'video':
        send_telegram_msg(
            chat_id,
            '⚙️ জুবায়ের ভাই, আপনার পিসির লোকাল ইঞ্জিনে ভিডিও রেন্ডারিং শুরু হয়েছে... (প্রায় ১-২ মিনিট লাগবে)'
        )
        try:
            main.run_pipeline()
            print(f'✅ ভিডিও জব {job_id} সফলভাবে সম্পন্ন হয়েছে!')
        except Exception as e:
            print(f'❌ ভিডিও রেন্ডারিং ব্যর্থ: {e}')
            send_telegram_msg(chat_id, f'⚠️ ভিডিও রেন্ডারিংয়ের সময় সমস্যা হয়েছে: {e}')

    elif job_type == 'post_card':
        try:
            print('🎨 ফটো কার্ড তৈরি হচ্ছে...')
            card_path = create_ai_photocard(
                title=prompt[:40] if prompt else 'এআই ও ভবিষ্যৎ প্রযুক্তি',
                points=[
                    'কৃত্রিম বুদ্ধিমত্তার নতুন দিগন্ত ও অটোমেশন',
                    'সফটওয়্যার আর্কিটেকচার ও ক্লাউড সিস্টেমস',
                    'সিলিকন ভ্যালি ২০৩০ টেকনোলজি আপডেট'
                ],
                category='Jubayer.dev AI Lab'
            )
            if card_path and card_path.exists():
                with open(card_path, 'rb') as pf:
                    requests.post(
                        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto',
                        data={'chat_id': chat_id, 'caption': '🎨 আপনার এআই ফটো কার্ড প্রস্তুত:\n\n#JubayerDev #Tech #AI'},
                        files={'photo': pf},
                        timeout=60
                    )
            print(f'✅ ফটো কার্ড জব {job_id} সফলভাবে সম্পন্ন হয়েছে!')
        except Exception as e:
            print(f'❌ ফটো কার্ড ব্যর্থ: {e}')

    try:
        requests.post(
            f'{RENDER_BASE_URL}/api/jobs/complete',
            json={'job_id': job_id},
            timeout=10
        )
    except Exception as e:
        print(f'[Worker Complete Error] {e}')

def run_worker():
    print('=================================================================')
    print("🤖 JUBAYER'S PERSONAL AI WORKER IS RUNNING (LOCAL ENGINE)")
    print(f'🌐 Connected to: {RENDER_BASE_URL}')
    print(f'📲 Telegram Target Chat ID: {TELEGRAM_CHAT_ID}')
    print('=================================================================')
    print('⏳ টেলিগ্রাম থেকে ভিডিও বা পোস্ট তৈরির নির্দেশের অপেক্ষায়...\n')

    while True:
        try:
            res = requests.get(f'{RENDER_BASE_URL}/api/jobs/pending', timeout=12)
            if res.status_code == 200:
                data = res.json()
                jobs = data.get('jobs', [])
                if jobs:
                    for job in jobs:
                        process_job(job)
            else:
                print(f'[Worker Warning] Render Server HTTP {res.status_code}')
        except requests.exceptions.RequestException:
            pass
        except Exception as e:
            print(f'[Worker Loop Error] {e}')

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == '__main__':
    run_worker()
