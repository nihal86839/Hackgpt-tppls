import random
import string
import sys
import os

# --- CONFIGURATION ---
TARGET_COUNT = 50000000  # Target: 20 Million
OUTPUT_FILE = "indian_pass_50m.txt"
RANDOM_CHARS_LENGTH = 3  # Adds 3 random characters (e.g., Axy, 129, Zk9)

# --- DATA SOURCE: INDIAN NAMES & SURNAMES ---
# I have included top common names here. 
# If you have a bigger list (20k names), put them in a file named 'names.txt'
# and the script will automatically load them.

DEFAULT_INDIAN_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Krishna", "Ishaan", "Rohan", "Rahul",
    "Amit", "Raj", "Vikram", "Sanjay", "Deepak", "Ravi", "Suresh", "Anil", "Manish", "Sunil", "Prakash",
    "Ramesh", "Mahesh", "Suresh", "Ankit", "Nikhil", "Karan", "Varun", "Yash", "Divya", "Priya",
    "Ananya", "Aadhya", "Aanya", "Diya", "Saanvi", "Pooja", "Neha", "Anjali", "Sneha", "Deepika",
    "Kavita", "Sunita", "Geeta", "Seema", "Ritu", "Nisha", "Megha", "Ishita", "Roshni", "Kiran",
    "Riya", "Sara", "Myra", "Avni", "Ira", "Aditi", "Naira", "Arya", "Prisha", "Kavya",
    "Gaurav", "Siddharth", "Akash", "Harsh", "Rishabh", "Tanmay", "Saurabh", "Abhishek", "Shubham", "Pranav",
    "Mohammed", "Ali", "Khan", "Ahmed", "Imran", "Salman", "Farhan", "Zaid", "Ayaan", "Hamza",
    "Siddique", "Iqbal", "Hussain", "Omar", "Usman", "Asad", "Bilal", "Faisal", "Khalid", "Nasir",
    "David", "John", "Michael", "Robert", "William", "Richard", "Thomas", "Daniel", "Matthew", "Anthony"
    # Note: To reach 20k names, please use an external file as described below.
]

DEFAULT_INDIAN_SURNAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Joshi", "Patel", "Reddy", "Rao", "Nair",
    "Iyer", "Iyengar", "Choudhury", "Banerjee", "Mukherjee", "Ghosh", "Das", "Seth", "Agarwal", "Malhotra",
    "Kapoor", "Khanna", "Mehta", "Shah", "Desai", "Trivedi", "Bhatt", "Chopra", "Kulkarni", "Joshi",
    "Pillai", "Menon", "Nambiar", "Varma", "Thakur", "Rajput", "Chauhan", "Solanki", "Pandey", "Mishra",
    "Shukla", "Tiwari", "Dubey", "Chaturvedi", "Bajpai", "Srivastava", "Awasthi", "Yadav", "Jha", "Thakur",
    "Khan", "Sheikh", "Hussain", "Ahmed", "Syed", "Beg", "Mirza", "Qureshi", "Ansari", "Hashmi",
    "Oberoi", "Khosla", "Wadhwa", "Sachdev", "Bhasin", "Chadha", "Kohli", "Gill", "Saggi", "Vohra",
    "Dhillon", "Sandhu", "Sidhu", "Bains", "Basra", "Bhullar", "Cheema", "Grewal", "Maan", "Pannu"
]

def load_external_list(filename):
    """Loads names from a file if it exists."""
    if os.path.exists(filename):
        print(f"[*] Found '{filename}'. Loading {filename}...")
        with open(filename, "r", encoding='utf-8', errors='ignore') as f:
            # Read lines, strip whitespace, remove empty lines
            return [line.strip() for line in f if line.strip()]
    return None

def main():
    print("##############################################")
    print("#    INDIAN PASSWORD LIST GENERATOR          #")
    print("#    Target: 20 Million Passwords            #")
    print("##############################################")

    # 1. Load Names
    # Checks if user provided a file named 'names.txt'
    names_list = load_external_list("names.txt")
    if not names_list:
        names_list = DEFAULT_INDIAN_NAMES
        print("[*] Using built-in Indian names list (approx 100).")
        print("[*] TIP: Create a file named 'names.txt' with 20,000 names for better results!")
    else:
        print(f"[+] Loaded {len(names_list)} names from file.")

    # 2. Load Surnames
    # Checks if user provided a file named 'surnames.txt'
    surnames_list = load_external_list("surnames.txt")
    if not surnames_list:
        surnames_list = DEFAULT_INDIAN_SURNAMES
        print("[*] Using built-in Indian surnames list.")
    else:
        print(f"[+] Loaded {len(surnames_list)} surnames from file.")

    # Character set: a-z, A-Z, 0-9
    char_set = string.ascii_letters + string.digits

    print(f"[*] Generating {TARGET_COUNT:,} passwords...")
    print(f"[*] Pattern: NameSurname + {RANDOM_CHARS_LENGTH} Random Chars (e.g., RahulSharmaA9x)")
    print(f"[*] Writing to: {OUTPUT_FILE}")

    count = 0
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            while count < TARGET_COUNT:
                # Pick random name and surname
                name = random.choice(names_list)
                surname = random.choice(surnames_list)

                # Generate random suffix (a-z, A-Z, 0-9)
                # 62 characters ^ 3 = 238,328 variations per name combo
                suffix = "".join(random.choices(char_set, k=RANDOM_CHARS_LENGTH))

                # Combine
                password = f"{name}{surname}{suffix}"

                f.write(password + "\n")
                count += 1

                if count % 1000000 == 0:
                    print(f"[+] Generated {count:,} passwords...")

        print(f"\n[+] SUCCESS! Generated {count:,} passwords.")
        print(f"[+] File saved as: {OUTPUT_FILE}")

    except KeyboardInterrupt:
        print(f"\n[!] Stopped by user. Generated {count:,} passwords.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
