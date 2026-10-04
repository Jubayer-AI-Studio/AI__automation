import urllib.parse
from playwright.sync_api import sync_playwright
import re, urllib.request
from pathlib import Path

queries = [
    ('welding_robot', 'robotic arm welding sparks'),
    ('cyber_robotics', 'futuristic robotics laboratory'),
    ('pcb_macro', 'printed circuit board electronic components macro')
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    for tag, query in queries:
        url = f'https://www.pexels.com/search/videos/{urllib.parse.quote(query)}/?orientation=portrait'
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(3000)
            links = page.locator('a').all()
            ids = []
            for l in links:
                href = l.get_attribute('href') or ''
                m = re.search(r'/video/[^/]+-(\d+)/?$', href)
                if m:
                    vid_id = m.group(1)
                    if vid_id not in ids:
                        ids.append(vid_id)
            print(tag, ids[:5])
        except Exception as e:
            print(tag, "Error:", e)
    browser.close()
