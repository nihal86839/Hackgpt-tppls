#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ███████╗ █████╗ ██╗     ██╗      ██████╗ ██╗   ██╗ ██████╗ ██████╗ ███████╗║
║     ██╔════╝██╔══██╗██║     ██║     ██╔════╝ ██║   ██║██╔═══██╗██╔══██╗██╔════╝║
║     █████╗  ███████║██║     ██║     ██║  ███╗██║   ██║██║   ██║██║  ██║█████╗  ║
║     ██╔══╝  ██╔══██║██║     ██║     ██║   ██║██║   ██║██║   ██║██║  ██║██╔══╝  ║
║     ██║     ██║  ██║███████╗███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║  ██║███████╗║
║     ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝║
║                                                                              ║
║                    🛡️ ALL-IN-ONE HACKER CAPTURE TOOL 🛡️                     ║
║                                                                              ║
║                         Defensive Security Toolkit                           ║
║                         Created by: Sa & Nihal                               ║
║                                                                              ║
║    ⚠️  LEGAL USE ONLY - For protecting your system from attackers ⚠️        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import socket
import platform
import subprocess
import threading
from datetime import datetime
from collections import defaultdict

# ============== INSTALLATION CHECK ==============
MISSING_MODULES = []

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    MISSING_MODULES.append("opencv-python")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    MISSING_MODULES.append("requests")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    MISSING_MODULES.append("psutil")

# ============== CONFIGURATION ==============
CONFIG = {
    "evidence_folder": "evidence",
    "log_file": "hacker_logs.json",
    "config_file": "config.json",
    "max_logs": 1000,
    "photo_cooldown": 5,
    "alert_sound": True
}

# ============== GLOBAL VARIABLES ==============
ATTACK_LOGS = []
MONITORING_ACTIVE = False
LAST_PHOTO_TIME = 0

# ============== SETUP ==============
def setup_directories():
    """Create necessary directories"""
    folders = [CONFIG["evidence_folder"], "reports", "captures"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def load_logs():
    """Load existing logs"""
    global ATTACK_LOGS
    if os.path.exists(CONFIG["log_file"]):
        try:
            with open(CONFIG["log_file"], 'r') as f:
                ATTACK_LOGS = json.load(f)
        except:
            ATTACK_LOGS = []

def save_logs():
    """Save logs to file"""
    with open(CONFIG["log_file"], 'w') as f:
        json.dump(ATTACK_LOGS[-CONFIG["max_logs"]:], f, indent=2)

# ============== 1. IP TRACKER ==============
class IPTracker:
    """Track IP address and get location information"""
    
    @staticmethod
    def get_local_ip():
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "Unknown"
    
    @staticmethod
    def get_public_ip():
        """Get public IP address"""
        if not REQUESTS_AVAILABLE:
            return {"error": "Requests module not installed"}
        
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            return response.json()
        except:
            try:
                response = requests.get('https://api64.ipify.org?format=json', timeout=5)
                return response.json()
            except:
                return {"error": "Could not fetch public IP"}
    
    @staticmethod
    def get_ip_info(ip_address=None):
        """Get detailed information about an IP address"""
        if not REQUESTS_AVAILABLE:
            return {"error": "Requests module not installed"}
        
        try:
            if ip_address is None:
                ip_data = IPTracker.get_public_ip()
                if "ip" in ip_data:
                    ip_address = ip_data["ip"]
                else:
                    return {"error": "Could not get IP"}
            
            response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=10)
            data = response.json()
            
            if data['status'] == 'success':
                return {
                    "ip": data.get('query', 'Unknown'),
                    "city": data.get('city', 'Unknown'),
                    "region": data.get('regionName', 'Unknown'),
                    "country": data.get('country', 'Unknown'),
                    "country_code": data.get('countryCode', 'Unknown'),
                    "isp": data.get('isp', 'Unknown'),
                    "org": data.get('org', 'Unknown'),
                    "as": data.get('as', 'Unknown'),
                    "lat": data.get('lat', 0),
                    "lon": data.get('lon', 0),
                    "timezone": data.get('timezone', 'Unknown'),
                    "zip": data.get('zip', 'Unknown')
                }
            else:
                return {"error": "Could not fetch IP info"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_google_maps_link(lat, lon):
        """Generate Google Maps link"""
        return f"https://www.google.com/maps?q={lat},{lon}"

# ============== 2. CAMERA CAPTURE ==============
class CameraCapture:
    """Capture photos from webcam for evidence"""
    
    @staticmethod
    def list_cameras():
        """List available cameras"""
        cameras = []
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
        return cameras
    
    @staticmethod
    def capture_photo(save_path=None):
        """Capture a single photo from webcam"""
        if not CV2_AVAILABLE:
            return None, "OpenCV not installed. Run: pip install opencv-python"
        
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                for i in range(1, 5):
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        break
            
            if not cap.isOpened():
                return None, "No camera available"
            
            time.sleep(0.3)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None, "Could not capture frame"
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if save_path is None:
                save_path = f"{CONFIG['evidence_folder']}/hacker_{timestamp}.jpg"
            
            cv2.putText(frame, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "EVIDENCE - HACKER CAPTURE", 
                       (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            cv2.imwrite(save_path, frame)
            return save_path, "Success"
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def capture_multiple(count=3, interval=0.5):
        """Capture multiple photos"""
        photos = []
        for i in range(count):
            path, msg = CameraCapture.capture_photo()
            if path:
                photos.append(path)
            time.sleep(interval)
        return photos

# ============== 3. MICROPHONE RECORDER ==============
class AudioCapture:
    """Capture audio for evidence"""
    
    @staticmethod
    def check_audio_available():
        """Check if audio recording is available"""
        try:
            import pyaudio
            return True
        except ImportError:
            return False
    
    @staticmethod
    def record_audio(duration=5, save_path=None):
        """Record audio for specified duration"""
        try:
            import pyaudio
            import wave
            
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            
            if save_path is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                save_path = f"{CONFIG['evidence_folder']}/audio_{timestamp}.wav"
            
            p = pyaudio.PyAudio()
            
            stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK)
            
            print(f"🎤 Recording for {duration} seconds...")
            frames = []
            
            for _ in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            wf = wave.open(save_path, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return save_path, "Success"
            
        except ImportError:
            return None, "PyAudio not installed. Run: pip install pyaudio"
        except Exception as e:
            return None, str(e)

# ============== 4. SYSTEM MONITOR ==============
class SystemMonitor:
    """Monitor system for suspicious activities"""
    
    @staticmethod
    def get_network_connections():
        """Get active network connections"""
        if not PSUTIL_AVAILABLE:
            return []
        
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        "local_ip": conn.laddr.ip if conn.laddr else "N/A",
                        "local_port": conn.laddr.port if conn.laddr else "N/A",
                        "remote_ip": conn.raddr.ip if conn.raddr else "N/A",
                        "remote_port": conn.raddr.port if conn.raddr else "N/A",
                        "status": conn.status,
                        "pid": conn.pid
                    })
        except:
            pass
        return connections
    
    @staticmethod
    def get_suspicious_connections():
        """Find suspicious network connections"""
        connections = SystemMonitor.get_network_connections()
        suspicious = []
        
        known_safe_ports = [80, 443, 53, 22, 21, 25, 110, 143, 993, 995, 3306, 5432, 27017]
        
        for conn in connections:
            remote_port = conn.get("remote_port", "N/A")
            if remote_port != "N/A" and remote_port not in known_safe_ports:
                suspicious.append(conn)
        
        return suspicious
    
    @staticmethod
    def get_running_processes():
        """Get list of running processes"""
        if not PSUTIL_AVAILABLE:
            return []
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "user": proc.info['username'],
                    "cpu": proc.info['cpu_percent']
                })
            except:
                pass
        return processes
    
    @staticmethod
    def get_system_info():
        """Get system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "hostname": socket.gethostname(),
            "username": os.getlogin() if hasattr(os, 'getlogin') else "Unknown",
            "machine": platform.machine(),
            "processor": platform.processor(),
            "local_ip": IPTracker.get_local_ip()
        }

# ============== 5. ATTACK LOGGER ==============
class AttackLogger:
    """Log all attack information"""
    
    @staticmethod
    def log_attack(attack_type, details, ip_info=None, photo_path=None, audio_path=None):
        """Log an attack event"""
        global ATTACK_LOGS
        
        attack_record = {
            "id": len(ATTACK_LOGS) + 1,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "unix_timestamp": time.time(),
            "attack_type": attack_type,
            "details": details,
            "ip_info": ip_info,
            "photo_evidence": photo_path,
            "audio_evidence": audio_path,
            "system_info": SystemMonitor.get_system_info()
        }
        
        ATTACK_LOGS.append(attack_record)
        save_logs()
        
        return attack_record
    
    @staticmethod
    def get_all_logs():
        """Get all attack logs"""
        return ATTACK_LOGS
    
    @staticmethod
    def get_log_by_id(log_id):
        """Get specific log by ID"""
        for log in ATTACK_LOGS:
            if log["id"] == log_id:
                return log
        return None
    
    @staticmethod
    def clear_logs():
        """Clear all logs"""
        global ATTACK_LOGS
        ATTACK_LOGS = []
        if os.path.exists(CONFIG["log_file"]):
            os.remove(CONFIG["log_file"])

# ============== 6. REPORT GENERATOR ==============
class ReportGenerator:
    """Generate reports for authorities"""
    
    @staticmethod
    def generate_text_report(log_id=None):
        """Generate a text report"""
        if log_id:
            logs = [AttackLogger.get_log_by_id(log_id)]
            if not logs[0]:
                return None
        else:
            logs = ATTACK_LOGS
        
        if not logs:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"reports/hacker_report_{timestamp}.txt"
        
        report_lines = [
            "=" * 70,
            "CYBER ATTACK INCIDENT REPORT",
            "=" * 70,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Incidents: {len(logs)}",
            "=" * 70,
            ""
        ]
        
        for log in logs:
            report_lines.extend([
                f"INCIDENT #{log.get('id', 'N/A')}",
                "-" * 40,
                f"Timestamp: {log.get('timestamp', 'N/A')}",
                f"Attack Type: {log.get('attack_type', 'N/A')}",
                f"Details: {log.get('details', 'N/A')}",
                ""
            ])
            
            if log.get('ip_info'):
                ip_info = log['ip_info']
                if 'ip' in ip_info:
                    report_lines.extend([
                        "ATTACKER INFORMATION:",
                        f"  IP Address: {ip_info.get('ip', 'N/A')}",
                        f"  Location: {ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}",
                        f"  Country: {ip_info.get('country', 'N/A')} ({ip_info.get('country_code', 'N/A')})",
                        f"  ISP: {ip_info.get('isp', 'N/A')}",
                        f"  Organization: {ip_info.get('org', 'N/A')}",
                        f"  Coordinates: {ip_info.get('lat', 'N/A')}, {ip_info.get('lon', 'N/A')}",
                        f"  Google Maps: {IPTracker.get_google_maps_link(ip_info.get('lat', 0), ip_info.get('lon', 0))}",
                        ""
                    ])
            
            if log.get('photo_evidence'):
                report_lines.append(f"Photo Evidence: {log['photo_evidence']}")
            
            if log.get('audio_evidence'):
                report_lines.append(f"Audio Evidence: {log['audio_evidence']}")
            
            report_lines.append("")
        
        report_lines.extend([
            "=" * 70,
            "IMPORTANT: Submit this report to your local cyber crime cell",
            "India Cyber Crime Helpline: 1930",
            "Website: https://cybercrime.gov.in",
            "=" * 70
        ])
        
        report_content = "\n".join(report_lines)
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        return report_path
    
    @staticmethod
    def generate_json_report(log_id=None):
        """Generate a JSON report"""
        if log_id:
            logs = [AttackLogger.get_log_by_id(log_id)]
        else:
            logs = ATTACK_LOGS
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"reports/hacker_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump({
                "generated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total_incidents": len(logs),
                "incidents": logs
            }, f, indent=2)
        
        return report_path

# ============== 7. REAL-TIME MONITOR ==============
class RealTimeMonitor:
    """Real-time monitoring for attacks"""
    
    @staticmethod
    def start_monitoring(callback=None):
        """Start real-time monitoring"""
        global MONITORING_ACTIVE
        MONITORING_ACTIVE = True
        
        print("\n🔍 Starting real-time monitoring...")
        print("Press Ctrl+C to stop\n")
        
        last_connections = set()
        
        try:
            while MONITORING_ACTIVE:
                current_connections = SystemMonitor.get_suspicious_connections()
                
                for conn in current_connections:
                    conn_id = f"{conn['remote_ip']}:{conn['remote_port']}"
                    
                    if conn_id not in last_connections:
                        print(f"⚠️  New suspicious connection: {conn['remote_ip']}:{conn['remote_port']}")
                        
                        ip_info = IPTracker.get_ip_info(conn['remote_ip'])
                        photo_path, _ = CameraCapture.capture_photo()
                        
                        AttackLogger.log_attack(
                            attack_type="Suspicious Connection",
                            details=f"New connection from {conn['remote_ip']}:{conn['remote_port']}",
                            ip_info=ip_info,
                            photo_path=photo_path
                        )
                        
                        print(f"📸 Evidence captured!")
                        print(f"📍 Location: {ip_info.get('city', 'Unknown')}, {ip_info.get('country', 'Unknown')}")
                        
                        if callback:
                            callback(conn, ip_info, photo_path)
                        
                        last_connections.add(conn_id)
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped.")
            MONITORING_ACTIVE = False
    
    @staticmethod
    def stop_monitoring():
        """Stop monitoring"""
        global MONITORING_ACTIVE
        MONITORING_ACTIVE = False

# ============== MAIN MENU ==============
def show_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                  
