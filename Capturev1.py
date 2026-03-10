#!/usr/bin/env python3
"""
HACKER CAPTURE TOOL - Error Fixed Version
Created by: Sa & Nihal
"""

import os
import sys
import json
import time
import socket
import platform
from datetime import datetime

# Create folders first
for folder in ["evidence", "reports"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Try to import modules with error handling
CV2_AVAILABLE = False
REQUESTS_AVAILABLE = False
PSUTIL_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except:
    pass

try:
    import requests
    REQUESTS_AVAILABLE = True
except:
    pass

try:
    import psutil
    PSUTIL_AVAILABLE = True
except:
    pass

# Global variables
LOG_FILE = "hacker_logs.json"
ATTACK_LOGS = []

def load_logs():
    global ATTACK_LOGS
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                ATTACK_LOGS = json.load(f)
    except:
        ATTACK_LOGS = []

def save_logs():
    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(ATTACK_LOGS, f, indent=2)
    except:
        pass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unknown"

def get_ip_info(ip=None):
    if not REQUESTS_AVAILABLE:
        return {"error": "Install: pip install requests"}
    
    try:
        if ip is None:
            r = requests.get('https://api.ipify.org?format=json', timeout=5)
            ip = r.json().get("ip", "")
        
        r = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
        data = r.json()
        
        if data.get('status') == 'success':
            return {
                "ip": data.get('query', 'Unknown'),
                "city": data.get('city', 'Unknown'),
                "region": data.get('regionName', 'Unknown'),
                "country": data.get('country', 'Unknown'),
                "isp": data.get('isp', 'Unknown'),
                "lat": data.get('lat', 0),
                "lon": data.get('lon', 0)
            }
        return {"error": "Could not get info"}
    except Exception as e:
        return {"error": str(e)}

def capture_photo():
    if not CV2_AVAILABLE:
        return None, "Install: pip install opencv-python"
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None, "Camera not available"
        
        time.sleep(0.3)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return None, "Capture failed"
        
        filename = f"evidence/hacker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        # Add timestamp
        cv2.putText(frame, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imwrite(filename, frame)
        return filename, "OK"
    except Exception as e:
        return None, str(e)

def get_connections():
    if not PSUTIL_AVAILABLE:
        return []
    
    connections = []
    try:
        for c in psutil.net_connections(kind='inet'):
            if c.status == 'ESTABLISHED' and c.raddr:
                connections.append({
                    "local": f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A",
                    "remote": f"{c.raddr.ip}:{c.raddr.port}",
                    "pid": c.pid
                })
    except:
        pass
    return connections

def log_attack(attack_type, details, ip_info=None, photo=None):
    global ATTACK_LOGS
    
    record = {
        "id": len(ATTACK_LOGS) + 1,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "type": attack_type,
        "details": details,
        "ip_info": ip_info,
        "photo": photo
    }
    
    ATTACK_LOGS.append(record)
    save_logs()
    return record

def generate_report():
    if not ATTACK_LOGS:
        return None
    
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    lines = [
        "=" * 50,
        "CYBER ATTACK REPORT",
        "=" * 50,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Incidents: {len(ATTACK_LOGS)}",
        ""
    ]
    
    for log in ATTACK_LOGS:
        lines.extend([
            f"ID: {log['id']}",
            f"Time: {log['time']}",
            f"Type: {log['type']}",
            f"Details: {log['details']}"
        ])
        
        if log.get('ip_info') and 'ip' in log['ip_info']:
            lines.extend([
                f"IP: {log['ip_info'].get('ip')}",
                f"Location: {log['ip_info'].get('city')}, {log['ip_info'].get('country')}"
            ])
        
        if log.get('photo'):
            lines.append(f"Photo: {log['photo']}")
        
        lines.append("-" * 40)
    
    lines.extend([
        "",
        "=" * 50,
        "Report to Cyber Crime: 1930",
        "Website: https://cybercrime.gov.in",
        "=" * 50
    ])
    
    with open(filename, 'w') as f:
        f.write("\n".join(lines))
    
    return filename

def show_banner():
    print("""
    ╔════════════════════════════════════════════╗
    ║   🛡️ HACKER CAPTURE TOOL 🛡️               ║
    ║   Error Fixed Version                      ║
    ║   Created by: Sa & Nihal                   ║
    ╚════════════════════════════════════════════╝
    """)

def show_status():
    print("\n📊 STATUS:")
    print(f"  📷 Camera: {'✅' if CV2_AVAILABLE else '❌'}")
    print(f"  🌐 Network: {'✅' if REQUESTS_AVAILABLE else '❌'}")
    print(f"  📊 Monitor: {'✅' if PSUTIL_AVAILABLE else '❌'}")
    print(f"  🌐 Your IP: {get_local_ip()}")
    print(f"  📝 Logs: {len(ATTACK_LOGS)}")

def main():
    load_logs()
    show_banner()
    show_status()
    
    while True:
        print("\n" + "=" * 45)
        print("📋 MENU")
        print("=" * 45)
        print("[1] 📷 Capture Photo")
        print("[2] 🌐 IP Tracker")
        print("[3] 🔍 Network Connections")
        print("[4] 💻 System Info")
        print("[5] ⚠️  Simulate Attack")
        print("[6] 📝 View Logs")
        print("[7] 📄 Generate Report")
        print("[8] 🗑️  Clear Logs")
        print("[0] 🚪 Exit")
        print("=" * 45)
        
        try:
            choice = input("\n👉 Choice: ").strip()
        except:
            break
        
        if choice == '1':
            print("\n📷 Capturing...")
            path, msg = capture_photo()
            if path:
                print(f"✅ Saved: {path}")
            else:
                print(f"❌ {msg}")
        
        elif choice == '2':
            print("\n🌐 IP TRACKER")
            try:
                ip = input("Enter IP (blank = your IP): ").strip()
            except:
                ip = ""
            
            info = get_ip_info(ip if ip else None)
            
            if 'error' in info:
                print(f"❌ {info['error']}")
            else:
                print(f"\n📍 IP: {info.get('ip')}")
                print(f"🏙️ City: {info.get('city')}")
                print(f"🌍 Country: {info.get('country')}")
                print(f"🏢 ISP: {info.get('isp')}")
                lat = info.get('lat', 0)
                lon = info.get('lon', 0)
                print(f"🗺️ Maps: https://www.google.com/maps?q={lat},{lon}")
        
        elif choice == '3':
            print("\n🔍 Scanning...")
            conns = get_connections()
            print(f"📊 Active Connections: {len(conns)}")
            for c in conns[:10]:
                print(f"  {c['remote']}")
        
        elif choice == '4':
            print("\n💻 SYSTEM:")
            print(f"  OS: {platform.system()} {platform.release()}")
            print(f"  Hostname: {socket.gethostname()}")
            print(f"  IP: {get_local_ip()}")
        
        elif choice == '5':
            print("\n🔴 ATTACK DETECTED!")
            ip_info = get_ip_info()
            photo, _ = capture_photo()
            log = log_attack("Simulated", "Test attack", ip_info, photo)
            print(f"✅ Logged! ID: {log['id']}")
            if photo:
                print(f"📸 Photo: {photo}")
        
        elif choice == '6':
            print("\n📝 LOGS:")
            if not ATTACK_LOGS:
                print("📭 No logs")
            for log in ATTACK_LOGS[-5:]:
                print(f"  #{log['id']} - {log['time']} - {log['type']}")
        
        elif choice == '7':
            path = generate_report()
            if path:
                print(f"✅ Report: {path}")
                print("📧 Submit to Cyber Crime: 1930")
            else:
                print("❌ No logs to report")
        
        elif choice == '8':
            global ATTACK_LOGS
            ATTACK_LOGS = []
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
            print("✅ Cleared!")
        
        elif choice == '0':
            print("\n👋 Bye! Stay Safe!")
            break
        
        else:
            print("❌ Invalid choice")
        
        try:
            input("\nPress Enter...")
        except:
            pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
