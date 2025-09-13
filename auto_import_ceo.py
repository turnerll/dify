#!/usr/bin/env python3
"""
Auto Import AI CEO Assistant to Dify
Automatically sets up admin account and imports the AI CEO assistant
"""

import requests
import json
import time
import sys

# Configuration
DIFY_BASE_URL = "http://localhost"
ADMIN_EMAIL = "djtlmed@gmail.com"
ADMIN_PASSWORD = input("🔑 Enter your Dify admin password: ")
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
        except:
            pass
        time.sleep(2)
        print(f"⏳ Still waiting... ({i+1}/30)")
    return False

def setup_admin():
    """Set up the admin account"""
    print("🔧 Setting up admin account...")
    
    setup_data = {
        "account": {
            "name": "AI CEO Admin",
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        },
        "workspace": {
            "name": WORKSPACE_NAME
        }
    }
    
    try:
        response = requests.post(
            f"{DIFY_BASE_URL}/api/setup",
            json=setup_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Admin account created successfully!")
            return True
        else:
            print(f"❌ Setup failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Setup error: {str(e)}")
        return False

def login():
    """Login to get auth token"""
    print("🔐 Logging in...")
    
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(
            f"{DIFY_BASE_URL}/console/api/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
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
        
        response = requests.post(
            f"{DIFY_BASE_URL}/console/api/apps/import",
            json=app_data,
            headers=headers
        )
        
        if response.status_code == 201:
            print("🎉 AI CEO Assistant imported successfully!")
            data = response.json()
            app_id = data.get('id', 'unknown')
            print(f"✅ App ID: {app_id}")
            print(f"🌟 Your AI CEO is now available at: {DIFY_BASE_URL}/app/{app_id}")
            return True
        else:
            print(f"❌ Import failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def main():
    print("🚀 IMPORTING AI CEO TO YOUR EXISTING ACCOUNT")
    print("=" * 45)
    
    # Wait for Dify to be ready
    if not wait_for_dify():
        print("❌ Dify failed to start properly")
        sys.exit(1)
    
    # Skip setup since account exists, go directly to login
    print("ℹ️  Skipping setup - using existing account")
    
    # Login to get token
    token = login()
    if not token:
        print("❌ Failed to login - check your password")
        sys.exit(1)
    
    # Import AI CEO assistant
    if not import_ai_ceo(token):
        print("❌ Failed to import AI CEO assistant")
        sys.exit(1)
    
    print("\n🎉 SUCCESS! Your AI CEO Command Center is ready!")
    print("=" * 50)
    print(f"📧 Admin Email: {ADMIN_EMAIL}")
    print(f"🌐 Dashboard: {DIFY_BASE_URL}")
    print("💡 Your AI CEO assistant is now available!")
    print("🚀 Go to Dify and start using your AI CEO!")

if __name__ == "__main__":
    main()
