import hashlib
import os
import sys

def print_banner():
    print("""
##############################################
#       UNIVERSAL HASH CRACKER TOOL          #
#       Supports: MD5, SHA-1, SHA-256...     #
##############################################
    """)

def detect_hash_type(h):
    length = len(h)
    if length == 32:
        return 'md5'
    elif length == 40:
        return 'sha1'
    elif length == 56:
        return 'sha224'
    elif length == 64:
        return 'sha256'
    elif length == 96:
        return 'sha384'
    elif length == 128:
        return 'sha512'
    else:
        return None

def main():
    print_banner()
    
    # 1. Ask for the hash
    target_hash = input("Enter hash: ").strip()
    
    # 2. Check hash type
    print("\nChecking hash...")
    hash_type = detect_hash_type(target_hash)
    
    if hash_type:
        print(f"Successfully identified hash type: {hash_type.upper()}")
    else:
        print("[-] Error: Could not identify hash type or unsupported hash.")
        sys.exit(1)

    # 3. Ask for wordlist path
    # This handles paths like ~/ex.txt or relative paths automatically
    raw_path = input("Enter wordlist path: ").strip()
    wordlist_path = os.path.expanduser(raw_path)

    # Check if file exists
    if not os.path.exists(wordlist_path):
        print(f"\n[-] Error: File not found at '{wordlist_path}'")
        print("[-] Please check the path and try again.")
        sys.exit(1)

    print(f"\n[*] Cracking {hash_type.upper()} hash using: {wordlist_path}")
    print("[*] Please wait...")

    # 4. Crack the hash
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                word = line.strip()
                
                # Hash the current word in the detected algorithm
                hashed_word = hashlib.new(hash_type, word.encode('utf-8')).hexdigest()

                # Compare
                if hashed_word == target_hash.lower():
                    print(f"\n[+] SUCCESS! Password found: {word}")
                    return

            print("\n[-] Password not found in the wordlist.")
            
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")

if __name__ == "__main__":
    main()
