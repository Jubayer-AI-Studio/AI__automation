from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    url = 'https://www.pexels.com/search/videos/robotic%20arm/?orientation=portrait'
    page.goto(url, timeout=30000)
    page.wait_for_timeout(4000)
    
    links = page.locator('a[href*="/video/"]').all()
    print(f'Found {len(links)} video page links')
    found_urls = set()
    for l in links[:10]:
        href = l.get_attribute('href')
        if href and '/video/' in href:
            found_urls.add(href)
            
    for u in list(found_urls)[:5]:
        print('Video URL:', u)
        
    browser.close()
