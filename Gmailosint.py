#!/usr/bin/env python3
"""
Educational Demo: Gmail Privacy Analysis - Demonstrates privacy risks without actual access.
"""

def analyze_gmail(email):
    """Demonstrate how basic OSINT works against email addresses."""
    
    print(f"\n===== Analyzing: {email} =====")
    
    # Educational demonstration of data collection techniques
    
    # Username extraction
    if "@" in email:
        username = email.split("@")[0]
        print(f"[USERNAME] Extracted primary handle:", username)
        
        # Potential for typosquatting research
        common_typos = [
            username.replace("l", "1"),
            username.replace("o", "0"),
            username + "_",
            username.capitalize(),
            f"{username}2"
        ]
        
        print("[POTENTIAL] Typosquatting variations:", common_typos)
    
    # Domain analysis
    if "@" in email:
        domain = email.split("@")[1]
        print(f"[DOMAIN] Service provider:", domain)
        
        # Check for subdomain patterns
        parts = domain.split('.')
        if len(parts) > 2 and not any(p.isdigit() for p in parts[0]):
            print("[PATTERN] Possible organizational structure:", 
                  f"{parts[0]}.{parts[-1]}")
    
    # Educational phishing vector analysis
    
    def analyze_patterns(s):
        """Educate on common search patterns."""
        if len(s) > 64:
            return "[WARNING] Very long name (>63 chars)"
        
        special_chars = sum(1 for c in s if not c.isalnum())
        if special_chars > 2:
            print(f"[PATTERN] Excessive special characters: {s}")
            
        numeric_ratio = sum(c.isdigit() for c in s) / len(s)
        if numeric_ratio > .3:
            return "[PATTERN] High numeric ratio"
    
    # Apply to username
    try:
        analyze_patterns(username)
    except NameError:
        pass
    
    print("[EDUCATIONAL] Attack vectors demonstrated.")

def main():
    email = input("Enter an email address for analysis: ")
    if not email.endswith(('.com', '.edu', '.gov')):
        print("[NOTE] Non-commercial domains detected")
    
    analyze_gmail(email)

if __name__ == "__main__":
    main()
