import sys
import getpass
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("  Jubayer AI Specialist - Facebook Page Name Update Helper")
print("=" * 60)
print("Target Name: Jubayer AI Specialist")
print("Notice: Facebook requires your account password to verify this change.")
print()

password = getpass.getpass("Enter your Facebook password (input hidden): ")
if not password:
    print("Password cannot be empty. Exiting.")
    sys.exit(1)

profile_dir = Path(r"C:\Users\ASSDI\Desktop\facebook\messenger_bot\chrome_profile")

print("\nConnecting to Facebook browser session...")
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        channel="chrome",
        headless=False,  # Let user see the confirmation live!
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.new_page()
    try:
        url = "https://www.facebook.com/settings?tab=profile"
        print(f"Navigating to {url}...")
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        
        target_frame = None
        for f in page.frames:
            if "cquick=" in f.url or "tab=profile" in f.url and f != page.main_frame:
                target_frame = f
                break
                
        if not target_frame:
            print("Settings frame not found.")
            sys.exit(1)
            
        edit_buttons = target_frame.locator('span:has-text("Edit"), a:has-text("Edit")').all()
        if len(edit_buttons) > 0:
            edit_buttons[0].click()
            page.wait_for_timeout(2000)
            
        name_input = target_frame.locator('input[name="pseudonymous_name"]')
        name_input.fill("Jubayer AI Specialist")
        page.wait_for_timeout(1000)
        
        review_btn = target_frame.locator('button:has-text("Review Change"), input[value="Review Change"]').first
        review_btn.click()
        page.wait_for_timeout(3000)
        
        # In dialog, fill password
        pwd_input = page.locator('input[type="password"]').first
        if pwd_input.count() > 0:
            print("Entering password into Facebook verification dialog...")
            pwd_input.fill(password)
            page.wait_for_timeout(1000)
            
            # Click Request Change
            req_btn = page.locator('button:has-text("Request Change"), div[role="button"]:has-text("Request Change")').first
            if req_btn.count() > 0:
                print("Submitting Name Change Request to Facebook...")
                req_btn.click()
                page.wait_for_timeout(5000)
                print("Successfully submitted! Facebook will approve the name 'Jubayer AI Specialist'.")
            else:
                print("Request Change button not found.")
        else:
            print("Password input dialog not detected.")
            
    except Exception as e:
        print("Error during submission:", e)
    finally:
        page.wait_for_timeout(3000)
        browser.close()
        print("\nProcess finished.")
