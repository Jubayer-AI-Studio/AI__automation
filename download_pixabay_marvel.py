from playwright.sync_api import sync_playwright
import urllib.request
from pathlib import Path

targets = [
    ('arc_reactor_4872', 'https://pixabay.com/videos/id-4872/'),
    ('arc_reactor_127602', 'https://pixabay.com/videos/id-127602/'),
    ('arc_reactor_137271', 'https://pixabay.com/videos/id-137271/'),
    ('armor_31210', 'https://pixabay.com/videos/id-31210/'),
    ('armor_99615', 'https://pixabay.com/videos/id-99615/'),
    ('holo_screen_254658', 'https://pixabay.com/videos/id-254658/')
]

out_dir = Path('temp/pixabay_marvel')
out_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    for name, url in targets:
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(2000)
            v = page.locator('video').first
            src = v.get_attribute('src') or ''
            if not src:
                s = v.locator('source').first
                src = s.get_attribute('src') or ''
            if src:
                out_file = out_dir / f"{name}.mp4"
                req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req) as resp, open(out_file, 'wb') as f:
                    f.write(resp.read())
                print(f'{name}: saved {out_file.stat().st_size} bytes')
        except Exception as e:
            print(f'{name}: error {e}')
    browser.close()
