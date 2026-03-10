#!/usr/bin/env python3
"""
ALL-IN-ONE HACKER CAPTURE TOOL
Defensive Security Toolkit
Created by: Sa & Nihal
"""

import os
import sys
import json
import time
import socket
import platform
from datetime import datetime

# Check for required modules
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Configuration
CONFIG = {
    "evidence_folder": "evidence",
    "log_file": "hacker_logs.json",
    "max_logs": 1000
}

# Global variables
ATTACK_LOGS = []
MONITORING_ACTIVE = False

# Setup
def setup_directories():
    folders = [CONFIG["evidence_folder"], "reports"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def load_logs():
    global ATTACK_LOGS
    if os.path.exists(CONFIG["log_file"]):
        try:
            with open(CONFIG["log_file"], 'r') as f:
                ATTACK_LOGS = json.load(f)
        except:
            ATTACK_LOGS = []

def save_logs():
    with open(CONFIG["log_file"], 'w') as f:
        json.dump(ATTACK_LOGS[-CONFIG["max_logs"]:], f, indent=2)

# IP Tracker
class IPTracker:
    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"
    
    @staticmethod
    def get_ip_info(ip_address=None):
        if not REQUESTS_AVAILABLE:
            return {"error": "Install requests: pip install requests"}
        
        try:
            if ip_address is None:
                response = requests.get('https://api.ipify.org?format=json', timeout=5)
                ip_address = response.json().get("ip")
            
            response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=10)
            data = response.json()
            
            if data['status'] == 'success':
                return {
                    "ip": data.get('query', 'Unknown'),
                    "city": data.get('city', 'Unknown'),
                    "region": data.get('regionName', 'Unknown'),
                    "country": data.get('country', 'Unknown'),
                    "isp": data.get('isp', 'Unknown'),
                    "lat": data.get('lat', 0),
                    "lon": data.get('lon', 0)
                }
            return {"error": "Could not fetch IP info"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_maps_link(lat, lon):
        return f"https://www.google.com/maps?q={lat},{lon}"

# Camera Capture
class CameraCapture:
    @staticmethod
    def capture_photo():
        if not CV2_AVAILABLE:
            return None, "Install opencv: pip install opencv-python"
        
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None, "No camera available"
            
            time.sleep(0.3)
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None, "Could not capture"
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = f"{CONFIG['evidence_folder']}/hacker_{timestamp}.jpg"
            
            cv2.putText(frame, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imwrite(save_path, frame)
            return save_path, "Success"
        except Exception as e:
            return None, str(e)

# System Monitor
class SystemMonitor:
    @staticmethod
    def get_connections():
        if not PSUTIL_AVAILABLE:
            return []
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    connections.append({
                        "local_ip": conn.laddr.ip if conn.laddr else "N/A",
                        "local_port": conn.laddr.port if conn.laddr else "N/A",
                        "remote_ip": conn.raddr.ip,
                        "remote_port": conn.raddr.port,
                        "pid": conn.pid
                    })
        except:
            pass
        return connections
    
    @staticmethod
    def get_suspicious_connections():
        connections = SystemMonitor.get_connections()
        safe_ports = [80, 443, 53, 22, 21, 25, 110, 143]
        suspicious = []
        for conn in connections:
            if conn["remote_port"] not in safe_ports:
                suspicious.append(conn)
        return suspicious
    
    @staticmethod
    def get_system_info():
        return {
            "os": platform.system(),
            "hostname": socket.gethostname(),
            "local_ip": IPTracker.get_local_ip()
        }

# Attack Logger
class AttackLogger:
    @staticmethod
    def log_attack(attack_type, details, ip_info=None, photo=None):
        global ATTACK_LOGS
        record = {
            "id": len(ATTACK_LOGS) + 1,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "attack_type": attack_type,
            "details": details,
            "ip_info": ip_info,
            "photo": photo
        }
        ATTACK_LOGS.append(record)
        save_logs()
        return record

# Report Generator
class ReportGenerator:
    @staticmethod
    def generate_report():
        if not ATTACK_LOGS:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = f"reports/report_{timestamp}.txt"
        
        lines = ["="*60, "CYBER ATTACK REPORT", "="*60, ""]
        
        for log in ATTACK_LOGS:
            lines.append(f"ID: {log['id']}")
            lines.append(f"Time: {log['timestamp']}")
            lines.append(f"Type: {log['attack_type']}")
            if log.get('ip_info') and 'ip' in log['ip_info']:
                lines.append(f"IP: {log['ip_info']['ip']}")
                lines.append(f"Location: {log['ip_info']['city']}, {log['ip_info']['country']}")
            if log.get('photo'):
                lines.append(f"Photo: {log['photo']}")
            lines.append("-"*40)
        
        lines.extend(["", "="*60, "Report to Cyber Crime: 1930", "="*60])
        
        with open(path, 'w') as f:
            f.write("\n".join(lines))
        
        return path

# Banner
def show_banner():
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   🛡️ HACKER CAPTURE TOOL - All-in-One 🛡️        ║
    ║   Created by: Sa & Nihal                         ║
    ║   LEGAL USE ONLY - Protect Your System           ║
    ╚══════════════════════════════════════════════════╝
    """)

# Main Menu
def main():
    setup_directories()
    load_logs()
    show_banner()
    
    while True:
        print("\n" + "="*50)
        print("📋 MAIN MENU")
        print("="*50)
        print("[1] 📷 Capture Photo")
        print("[2] 🌐 IP Tracker")
        print("[3] 🔍 Network Scanner")
        print("[4] 💻 System Info")
        print("[5] ⚠️  Simulate Attack")
        print("[6] 📝 View Logs")
        print("[7] 📄 Generate Report")
        print("[8] 🗑️  Clear Logs")
        print("[0] 🚪 Exit")
        print("="*50)
        
        choice = input("\n👉 Choice: ").strip()
        
        if choice == '1':
            print("\n📷 Capturing...")
            path, msg = CameraCapture.capture_photo()
            if path:
                print(f"✅ Saved: {path}")
            else:
                print(f"❌ Error: {msg}")
        
        elif choice == '2':
            print("\n🌐 IP TRACKER")
            ip = input("Enter IP (blank for yours): ").strip()
            info = IPTracker.get_ip_info(ip if ip else None)
            
            if 'error' in info:
                print(f"❌ {info['error']}")
            else:
                print(f"\n📍 IP: {info.get('ip')}")
                print(f"🏙️ City: {info.get('city')}")
                print(f"🌍 Country: {info.get('country')}")
                print(f"🏢 ISP: {info.get('isp')}")
                print(f"🗺️ Maps: {IPTracker.get_maps_link(info.get('lat',0), info.get('lon',0))}")
        
        elif choice == '3':
            print("\n🔍 Scanning...")
            suspicious = SystemMonitor.get_suspicious_connections()
            print(f"⚠️ Suspicious: {len(suspicious)}")
            for conn in suspicious:
                print(f"  {conn['remote_ip']}:{conn['remote_port']}")
        
        elif choice == '4':
            info = SystemMonitor.get_system_info()
            print(f"\n💻 OS: {info['os']}")
            print(f"🌐 IP: {info['local_ip']}")
            print(f"🖥️ Hostname: {info['hostname']}")
        
        elif choice == '5':
            print("\n🔴 ATTACK DETECTED!")
            ip_info = IPTracker.get_ip_info()
            photo, _ = CameraCapture.capture_photo()
            log = AttackLogger.log_attack("Simulated", "Test attack", ip_info, photo)
            print(f"✅ Logged! ID: {log['id']}")
            if photo:
                print(f"📸 Photo: {photo}")
        
        elif choice == '6':
            print("\n📝 LOGS:")
            for log in ATTACK_LOGS[-5:]:
                print(f"  #{log['id']} - {log['timestamp']} - {log['attack_type']}")
        
        elif choice == '7':
            path = ReportGenerator.generate_report()
            if path:
                print(f"✅ Report: {path}")
            else:
                print("❌ No logs")
        
        elif choice == '8':
            global ATTACK_LOGS
            ATTACK_LOGS = []
            if os.path.exists(CONFIG["log_file"]):
                os.remove(CONFIG["log_file"])
            print("✅ Cleared!")
        
        elif choice == '0':
            print("\n👋 Goodbye! Stay Safe!")
            break
        
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bye!")
