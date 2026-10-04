from playwright.sync_api import sync_playwright
import time
import json
import requests
from pathlib import Path

out_dir = Path('assets/tech_clips/hollywood')
out_dir.mkdir(parents=True, exist_ok=True)

queries = ['robotic-arm', 'circuit-board-soldering', 'robotics-laboratory', 'humanoid-robot']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    for q in queries:
        url = f'https://www.pexels.com/search/videos/{q}/?orientation=portrait'
        print(f'Visiting {url}...')
        try:
            page.goto(url, timeout=25000)
            page.wait_for_timeout(3000)
            # Find video download links or video elements
            videos = page.locator('video source, a[href*=\"pexels.com/video\"]').all()
            print(f'Found {len(videos)} video tags for {q}')
            # Let's inspect source src
            sources = page.locator('video source').all()
            for s in sources[:2]:
                src = s.get_attribute('src')
                print('Source src:', src[:70] if src else 'None')
        except Exception as e:
            print(f'Error for {q}: {e}')
            
    browser.close()
