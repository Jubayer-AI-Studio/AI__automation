from playwright.sync_api import sync_playwright
import urllib.request
import re
from pathlib import Path

out_dir = Path('assets/tech_clips/hollywood')
out_dir.mkdir(parents=True, exist_ok=True)

queries = [
    ('soldering', 'https://www.pexels.com/search/videos/soldering%20circuit%20board/?orientation=portrait'),
    ('robotic_arm', 'https://www.pexels.com/search/videos/robotic%20arm%20industrial/?orientation=portrait'),
    ('cyber_lab', 'https://www.pexels.com/search/videos/futuristic%20laboratory/?orientation=portrait'),
    ('microchip', 'https://www.pexels.com/search/videos/microprocessor%20technology/?orientation=portrait')
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    for tag, url in queries:
        try:
            print(f'Fetching {tag}...')
            page.goto(url, timeout=30000)
            page.wait_for_timeout(3000)
            
            # Find download links: a[href*=\"/download/video/\"]
            dl_links = page.locator('a[href*=\"/download/video/\"]').all()
            if not dl_links:
                # Also check links like a[href*=\"/video/\"]
                v_links = page.locator('a[href*=\"/video/\"]').all()
                vid_ids = []
                for vl in v_links:
                    href = vl.get_attribute('href') or ''
                    m = re.search(r'-(\d+)/?$', href)
                    if m:
                        vid_ids.append(m.group(1))
                if vid_ids:
                    target_id = vid_ids[0]
                    target_url = f'https://www.pexels.com/download/video/{target_id}/'
                else:
                    target_url = None
            else:
                target_url = dl_links[0].get_attribute('href')
                
            print(f'-> Found target URL for {tag}: {target_url}')
            if target_url:
                out_file = out_dir / f"{tag}.mp4"
                req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req) as resp, open(out_file, 'wb') as f:
                    f.write(resp.read())
                print(f'✅ Successfully downloaded {out_file.name} ({out_file.stat().st_size} bytes)')
        except Exception as e:
            print(f'Error for {tag}: {e}')
            
    browser.close()
