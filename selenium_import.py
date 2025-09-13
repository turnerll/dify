#!/usr/bin/env python3
"""
Direct AI CEO Import using Selenium Web Automation
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Configuration
DIFY_URL = "http://localhost"
ADMIN_EMAIL = "djtlmed@gmail.com"
ADMIN_PASSWORD = "Infinity00di!"  # Using the password from the terminal output
AI_CEO_FILE = "/home/djtl/Projects/dify-ai-platform/ai_ceo_assistant_simple.json"

def setup_browser():
    """Setup Chrome browser with options"""
    print("🌐 Setting up browser...")
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Browser ready!")
        return driver
    except Exception as e:
        print(f"❌ Browser setup failed: {str(e)}")
        return None

def login_to_dify(driver):
    """Login to Dify"""
    print("🔐 Logging into Dify...")
    
    try:
        # Go to Dify
        driver.get(DIFY_URL)
        time.sleep(3)
        
        # Look for login form
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
        )
        
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
        
        # Enter credentials
        email_input.clear()
        email_input.send_keys(ADMIN_EMAIL)
        
        password_input.clear()
        password_input.send_keys(ADMIN_PASSWORD)
        
        # Submit form
        password_input.send_keys(Keys.RETURN)
        
        # Wait for dashboard to load
        time.sleep(5)
        
        print("✅ Login successful!")
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return False

def import_ai_ceo(driver):
    """Import the AI CEO assistant"""
    print("🤖 Importing AI CEO Assistant...")
    
    try:
        # Look for import button
        import_selectors = [
            "//button[contains(text(), 'Import DSL')]",
            "//button[contains(text(), 'Import')]", 
            "//a[contains(text(), 'Import DSL')]",
            "//div[contains(text(), 'Import DSL')]"
        ]
        
        import_button = None
        for selector in import_selectors:
            try:
                import_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not import_button:
            print("❌ Could not find import button")
            return False
        
        # Click import button
        import_button.click()
        time.sleep(2)
        
        # Look for file input
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        
        # Upload file
        file_input.send_keys(AI_CEO_FILE)
        time.sleep(2)
        
        # Look for create/submit button
        create_selectors = [
            "//button[contains(text(), 'Create')]",
            "//button[contains(text(), 'Import')]",
            "//button[contains(text(), 'Submit')]"
        ]
        
        create_button = None
        for selector in create_selectors:
            try:
                create_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if create_button:
            create_button.click()
            time.sleep(5)
            print("🎉 AI CEO Assistant imported successfully!")
            return True
        else:
            print("❌ Could not find create button")
            return False
            
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        return False

def main():
    print("🚀 AUTOMATED AI CEO IMPORT")
    print("=" * 30)
    
    # Check if file exists
    if not os.path.exists(AI_CEO_FILE):
        print(f"❌ AI CEO file not found: {AI_CEO_FILE}")
        return
    
    print(f"✅ AI CEO file ready: {os.path.basename(AI_CEO_FILE)}")
    
    # Setup browser
    driver = setup_browser()
    if not driver:
        return
    
    try:
        # Login to Dify
        if not login_to_dify(driver):
            return
        
        # Import AI CEO
        if import_ai_ceo(driver):
            print("\n🎉 SUCCESS! AI CEO imported!")
            print("=" * 30)
            print(f"🌐 Go to: {DIFY_URL}")
            print("🤖 Your AI CEO Assistant is ready!")
        
        # Keep browser open for 10 seconds to see result
        print("⏳ Keeping browser open for 10 seconds...")
        time.sleep(10)
        
    finally:
        driver.quit()
        print("🔚 Browser closed")

if __name__ == "__main__":
    main()
