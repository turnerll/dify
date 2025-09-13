#!/usr/bin/env python3
"""
Create Fresh Admin Account and Import AI CEO Assistant
"""

import requests
import json
import time
import sys

# Configuration
DIFY_BASE_URL = "http://localhost"
NEW_ADMIN_EMAIL = "aiceo@djtl.local"
NEW_ADMIN_PASSWORD = "AICEO2025secure!"
WORKSPACE_NAME = "AI CEO Command Center"
AI_CEO_FILE = "/home/djtl/Projects/dify-ai-platform/ai_ceo_assistant_simple.json"

def wait_for_dify():
    """Wait for Dify to be ready"""
    print("🔄 Waiting for Dify to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{DIFY_BASE_URL}/install", timeout=5)
            if response.status_code == 200:
                print("✅ Dify is ready!")
                return True
        except Exception:
            pass
        time.sleep(2)
        if i % 5 == 0:
            print(f"⏳ Still waiting... ({i+1}/30)")
    return False

def create_fresh_admin():
    """Create a completely fresh admin account"""
    print("👤 Creating fresh admin account...")
    
    setup_data = {
        "account": {
            "name": "AI CEO Admin",
            "email": NEW_ADMIN_EMAIL,
            "password": NEW_ADMIN_PASSWORD
        },
        "workspace": {
            "name": WORKSPACE_NAME
        }
    }
    
    try:
        response = requests.post(
            f"{DIFY_BASE_URL}/api/setup",
            json=setup_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Fresh admin account created!")
            return True
        else:
            print(f"❌ Setup failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Setup error: {str(e)}")
        return False

def login_new_admin():
    """Login with the new admin account"""
    print("🔐 Logging in with new account...")
    
    login_data = {
        "email": NEW_ADMIN_EMAIL,
        "password": NEW_ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(
            f"{DIFY_BASE_URL}/console/api/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def import_ai_ceo(token):
    """Import the AI CEO assistant"""
    print("🤖 Importing AI CEO Assistant...")
    
    try:
        with open(AI_CEO_FILE, 'r') as f:
            app_data = json.load(f)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Try different possible import endpoints
        import_urls = [
            f"{DIFY_BASE_URL}/console/api/apps/import",
            f"{DIFY_BASE_URL}/api/v1/apps/import",
            f"{DIFY_BASE_URL}/api/apps/import"
        ]
        
        for url in import_urls:
            try:
                response = requests.post(url, json=app_data, headers=headers, timeout=15)
                
                if response.status_code in [200, 201]:
                    print("🎉 AI CEO Assistant imported successfully!")
                    data = response.json()
                    app_id = data.get('id', 'unknown')
                    print(f"✅ App ID: {app_id}")
                    return True
                elif response.status_code == 404:
                    continue  # Try next URL
                else:
                    print(f"❌ Import failed with {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"❌ Import error with {url}: {str(e)}")
                continue
        
        print("❌ All import endpoints failed")
        return False
            
    except Exception as e:
        print(f"❌ File error: {str(e)}")
        return False

def main():
    print("🚀 CREATING FRESH ADMIN & IMPORTING AI CEO")
    print("=" * 45)
    
    # Wait for Dify
    if not wait_for_dify():
        print("❌ Dify not ready")
        return
    
    # Create fresh admin
    if not create_fresh_admin():
        print("❌ Failed to create admin")
        return
    
    # Small delay
    time.sleep(3)
    
    # Login
    token = login_new_admin()
    if not token:
        print("❌ Failed to login")
        return
    
    # Import AI CEO
    success = import_ai_ceo(token)
    
    # Show results
    print("\n" + "=" * 50)
    if success:
        print("🎉 COMPLETE SUCCESS!")
        print("=" * 20)
        print("✅ Fresh admin account created")
        print("✅ AI CEO Assistant imported")
    else:
        print("⚠️  PARTIAL SUCCESS!")
        print("=" * 20)
        print("✅ Fresh admin account created")
        print("❌ AI CEO import failed (can import manually)")
    
    print(f"\n📧 LOGIN DETAILS:")
    print(f"   Email: {NEW_ADMIN_EMAIL}")
    print(f"   Password: {NEW_ADMIN_PASSWORD}")
    print(f"   URL: {DIFY_BASE_URL}")
    
    print(f"\n📁 AI CEO File: {AI_CEO_FILE}")
    print("💡 If import failed, use 'Import DSL file' in Dify!")

if __name__ == "__main__":
    main()
