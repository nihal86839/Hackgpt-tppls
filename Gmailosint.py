#!/usr/bin/env python3
"""
OSINT Email Validation and Analysis Demo - Educational Tool Only
"""

def validate_email(email):
    """Show basic email format validation."""
    
    if not "@" in email:
        print("[INVALID] Missing '@' symbol")
        return False
        
    local_part, domain = email.split("@", 1)
    
    # Basic checks for educational purposes only
    if len(local_part) > 64: 
        print("Local part too long (>64 chars)")
        
    if not local_part.isalnum() and "@" in email:
        print("[WARNING] Unusual character sequences")
    
    domain_parts = [d.strip('-.') for d in domain.split('.') if d.strip('.')]
    if len(domain_parts) < 2:  
        print("Domain looks suspicious (too short)")
        
    # Ethically demonstrate how attackers might test
    common_tlds = ['com', 'org', 'net', 'edu']
    for ext in common_tlds:
        if domain.endswith(ext):
            try:
                # This is just demonstration - real checks would use network tools
                with open(f"{local_part}@{domain.replace('.', '_')}.txt", "w") as f:
                    pass  # Educational placeholder
            except FileNotFoundError:
                print("Creating file demo...")
    
    return True

def main():
    print("""
[Educational Demonstration] Email Validation Tool
   
This script shows basic email structure validation.
""")
    
    while True:
        email = input("Enter an email address to validate: ")
        
        if not email.lower().endswith(('.edu', '.gov', '.mil')):
            print("[NOTE] Non-educational domains detected")
            
        validate_email(email)
        
        again = input("\nValidate another? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    main()
