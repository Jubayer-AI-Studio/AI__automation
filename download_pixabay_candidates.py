from playwright.sync_api import sync_playwright
import urllib.request
import re
from pathlib import Path

targets = [
    ('robot_arm_159021', 'https://pixabay.com/videos/id-159021/'),
    ('iron_man_hud_192779', 'https://pixabay.com/videos/id-192779/'),
    ('sci_fi_lab_6797', 'https://pixabay.com/videos/id-6797/'),
    ('cyborg_199827', 'https://pixabay.com/videos/id-199827/'),
    ('robot_arm_225826', 'https://pixabay.com/videos/id-225826/'),
    ('iron_man_hud_122366', 'https://pixabay.com/videos/id-122366/')
]

out_dir = Path('temp/pixabay')
out_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    for name, url in targets:
        try:
            print(f'Visiting {name}: {url}...')
            page.goto(url, timeout=30000)
            page.wait_for_timeout(2500)
            
            # Find video src
            video_el = page.locator('video').first
            src = ''
            if video_el.count() > 0:
                src = video_el.get_attribute('src') or ''
                if not src:
                    source_el = video_el.locator('source').first
                    if source_el.count() > 0:
                        src = source_el.get_attribute('src') or ''
            
            print(f'{name} video src: {src}')
            if src:
                out_file = out_dir / f"{name}.mp4"
                req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req) as resp, open(out_file, 'wb') as f:
                    f.write(resp.read())
                print(f'-> Successfully downloaded {name}: {out_file.stat().st_size} bytes')
        except Exception as e:
            print(f'Error on {name}: {e}')
            
    browser.close()
