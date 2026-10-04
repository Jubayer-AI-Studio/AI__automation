from playwright.sync_api import sync_playwright
import urllib.parse, re

queries = [
    'arc reactor',
    'holographic screen',
    'futuristic armor'
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    for q in queries:
        url = f'https://pixabay.com/videos/search/{urllib.parse.quote(q)}/'
        try:
            page.goto(url, timeout=25000)
            page.wait_for_timeout(2500)
            links = page.locator('a').all()
            ids = []
            for l in links:
                href = l.get_attribute('href') or ''
                m = re.search(r'/videos/[^/]+-(\d+)/?$', href)
                if m and m.group(1) not in ids:
                    ids.append(m.group(1))
            print(f'{q}: found {len(ids)} -> {ids[:5]}')
        except Exception as e:
            print(f'{q}: error {e}')
    browser.close()
