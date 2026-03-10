import socket
from concurrent.futures import ThreadPoolExecutor

open_ports = []

# Resolve domain to IP
def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        print(f"\nTarget IP: {ip}")
        return ip
    except:
        print("Could not resolve target.")
        exit()

# Scan single port
def scan_port(ip, port):
    print(f"Scanning port {port}...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((ip, port))

        if result == 0:
            open_ports.append(port)

        s.close()

    except:
        pass


# -------- INPUT --------
target = input("Enter target (IP or domain): ")
port_range = input("Enter port range (example 0-1000): ")
threads = int(input("Enter thread count: "))

start_port, end_port = map(int, port_range.split("-"))

ip = resolve_target(target)

print("\nStarting scan...\n")

# -------- THREAD SCAN --------
with ThreadPoolExecutor(max_workers=threads) as executor:
    for port in range(start_port, end_port + 1):
        executor.submit(scan_port, ip, port)

print("\nScan completed.\n")

# -------- RESULT --------
if open_ports:
    print("Open Ports Found:")
    for port in open_ports:
        print(port)
else:
    print("No open ports found.")
