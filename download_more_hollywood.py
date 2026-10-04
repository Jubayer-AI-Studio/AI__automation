from playwright.sync_api import sync_playwright
import urllib.request
import re
from pathlib import Path

out_dir = Path('assets/tech_clips/hollywood')
out_dir.mkdir(parents=True, exist_ok=True)

targets = [
    ('robotic_assembly', 'https://www.pexels.com/search/videos/robotic%20arm%20factory/?orientation=portrait'),
    ('cyber_mechanics', 'https://www.pexels.com/search/videos/robot%20hand/?orientation=portrait'),
    ('tech_lab', 'https://www.pexels.com/search/videos/electronics%20laboratory/?orientation=portrait'),
    ('microchip_core', 'https://www.pexels.com/search/videos/microchip%20circuit/?orientation=portrait')
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    for tag, url in targets:
        try:
            print(f'Visiting {tag}...')
            page.goto(url, timeout=30000)
            page.wait_for_timeout(3500)
            
            # Find all video links
            links = page.locator('a').all()
            found_ids = []
            for l in links:
                href = l.get_attribute('href') or ''
                # check /download/video/(\d+) or /video/.*-(\d+)/
                m1 = re.search(r'/download/video/(\d+)', href)
                m2 = re.search(r'/video/[^/]+-(\d+)/?$', href)
                if m1:
                    found_ids.append(m1.group(1))
                elif m2:
                    found_ids.append(m2.group(1))
                    
            print(f'-> Found {len(found_ids)} candidate IDs for {tag}: {found_ids[:5]}')
            
            if found_ids:
                # pick the first unique valid ID
                chosen_id = found_ids[0]
                dl_url = f'https://www.pexels.com/download/video/{chosen_id}/'
                out_file = out_dir / f"{tag}.mp4"
                print(f'-> Downloading from {dl_url}...')
                req = urllib.request.Request(dl_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req) as resp, open(out_file, 'wb') as f:
                    f.write(resp.read())
                print(f'Done downloading {tag}. Size: {out_file.stat().st_size} bytes')
        except Exception as e:
            print(f'Error for {tag}: {e}')
            
    browser.close()
