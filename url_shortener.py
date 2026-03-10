
#!/usr/bin/env python3
"""
🔗 URL SHORTENER TOOL
Created by: Sa
"""

import hashlib
import json
import os
from datetime import datetime

DB_FILE = "url_database.json"

def load_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_database(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_short_code(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:6]

def shorten_url(long_url):
    if not long_url.startswith('http://') and not long_url.startswith('https://'):
        long_url = 'https://' + long_url
    
    short_code = generate_short_code(long_url)
    short_url = f"https://sa.url/{short_code}"
    
    db = load_database()
    db[short_code] = {
        'original_url': long_url,
        'short_url': short_url,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_database(db)
    
    return short_url, short_code

def banner():
    print("""
    ╔════════════════════════════════════════════════╗
    ║     🔗 URL SHORTENER TOOL 🔗                  ║
    ║     Created by: Sa                             ║
    ╚════════════════════════════════════════════════╝
    """)

def main():
    banner()
    
    while True:
        print("\n📌 MENU:")
        print("  [1] Shorten URL")
        print("  [2] List All URLs")
        print("  [3] Clear All")
        print("  [4] Exit")
        
        choice = input("\n👉 Choice (1-4): ").strip()
        
        if choice == '1':
            print("\n📝 Enter Long URL:")
            long_url = input(">>> ").strip()
            
            if not long_url:
                print("❌ Empty!")
                continue
            
            short_url, code = shorten_url(long_url)
            
            print(f"\n✅ SUCCESS!")
            print(f"📎 Original: {long_url[:50]}...")
            print(f"🔗 Short: {short_url}")
            print(f"🔑 Code: {code}")
        
        elif choice == '2':
            db = load_database()
            if not db:
                print("\n📭 No URLs!")
            else:
                print(f"\n📋 ALL URLs:")
                for code, data in db.items():
                    print(f"  {data['short_url']} → {data['original_url'][:40]}...")
        
        elif choice == '3':
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
            print("\n🗑️ Cleared!")
        
        elif choice == '4':
            print("\n👋 Bye!")
            break

if __name__ == "__main__":
    main()
