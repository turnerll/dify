#!/usr/bin/env python3
"""
Reset Dify password and import AI CEO Assistant
"""

import requests
import json
import time
import sys
import sqlite3
import hashlib
import os

# Configuration
DIFY_BASE_URL = "http://localhost"
ADMIN_EMAIL = "djtlmed@gmail.com"
NEW_TEMP_PASSWORD = "TempAICEO2025!"
AI_CEO_FILE = "/home/djtl/Projects/dify-ai-platform/ai_ceo_assistant_simple.json"

def reset_password_in_db():
    """Reset password directly in the database"""
    print("🔑 Resetting password in database...")
    
    try:
        # Find the database file
        db_paths = [
            "/home/djtl/Projects/dify-ai-platform/docker/volumes/app_db/_data/dify.db",
            "/var/lib/docker/volumes/docker_app_db/_data/dify.db",
            "./docker/volumes/app_db/_data/dify.db"
        ]
        
        db_path = None
        for path in db_paths:
            if os.path.exists(path):
                db_path = path
                break
        
        if not db_path:
            print("❌ Could not find Dify database file")
            return False
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Hash the new password (using werkzeug's method)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          NEW_TEMP_PASSWORD.encode('utf-8'), 
                                          b'salt', 
                                          100000)
        password_hash_str = password_hash.hex()
        
        # Update password
        cursor.execute("""
            UPDATE accounts 
            SET password_hash = ?, password_salt = 'salt' 
            WHERE email = ?
        """, (password_hash_str, ADMIN_EMAIL))
        
        conn.commit()
        conn.close()
        
        print("✅ Password reset successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database reset failed: {str(e)}")
        return False

def restart_dify():
    """Restart Dify containers to reload changes"""
    print("🔄 Restarting Dify to apply changes...")
    
    try:
        os.system("cd /home/djtl/Projects/dify-ai-platform/docker && docker compose restart")
        time.sleep(10)
        print("✅ Dify restarted!")
        return True
    except Exception as e:
        print(f"❌ Restart failed: {str(e)}")
        return False

def login():
    """Login with new password"""
    print("🔐 Logging in with new password...")
    
    login_data = {
        "email": ADMIN_EMAIL,
        "password": NEW_TEMP_PASSWORD
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
        
        response = requests.post(
            f"{DIFY_BASE_URL}/console/api/apps/import",
            json=app_data,
            headers=headers
        )
        
        if response.status_code == 201:
            print("🎉 AI CEO Assistant imported successfully!")
            return True
        else:
            print(f"❌ Import failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def main():
    print("🚀 RESETTING PASSWORD & IMPORTING AI CEO")
    print("=" * 42)
    print(f"📧 Email: {ADMIN_EMAIL}")
    print(f"🔑 New temporary password: {NEW_TEMP_PASSWORD}")
    print("⚠️  Please change this password after login!")
    print()
    
    # Method 1: Try database reset
    if reset_password_in_db():
        restart_dify()
        time.sleep(5)
        
        token = login()
        if token and import_ai_ceo(token):
            print("\n🎉 SUCCESS! Everything is ready!")
            print("=" * 35)
            print(f"📧 Login: {ADMIN_EMAIL}")
            print(f"🔑 Password: {NEW_TEMP_PASSWORD}")
            print(f"🌐 URL: {DIFY_BASE_URL}")
            print("⚠️  IMPORTANT: Change password after login!")
            return
    
    # Method 2: Manual instructions
    print("\n📋 MANUAL IMPORT INSTRUCTIONS:")
    print("=" * 32)
    print("1. Go to: http://localhost")
    print(f"2. Login: {ADMIN_EMAIL}")
    print(f"3. Password: {NEW_TEMP_PASSWORD}")
    print("4. Click 'Import DSL file'")
    print(f"5. Select: {AI_CEO_FILE}")
    print("6. Click 'Create'")
    print("7. Change your password in settings!")

if __name__ == "__main__":
    main()
