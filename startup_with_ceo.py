#!/usr/bin/env python3
import os
import time
import shutil

def main():
    print("🤖 Starting Dify with AI CEO pre-loaded...")
    
    # Copy AI CEO files to a web-accessible location
    web_dir = "/tmp/dify_import"
    os.makedirs(web_dir, exist_ok=True)
    
    # Copy both formats
    shutil.copy("ai_ceo_assistant_simple.json", f"{web_dir}/ai_ceo_assistant.json") 
    shutil.copy("ai_ceo_assistant.yml", f"{web_dir}/ai_ceo_assistant.yml")
    
    print("✅ AI CEO files ready for import:")
    print(f"   📁 JSON: {web_dir}/ai_ceo_assistant.json")
    print(f"   📁 YML:  {web_dir}/ai_ceo_assistant.yml")
    print()
    print("🌐 Go to: http://localhost")
    print("🔑 Login: djtlmed@gmail.com")
    print("📥 Import either file using 'Import DSL file' button")
    print()
    print("💡 Both formats available - try the YML if JSON fails!")

if __name__ == "__main__":
    main()
