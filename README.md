# 🚗 Vehicle OSINT Scanner - Enhanced Edition

![Version](https://img.shields.io/badge/Version-3.0%20ELITE-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Educational-yellow)

### 🔥 Enhanced by **HACK WITH_NIHAL**  
### 🎯 A Professional OSINT Tool To Fetch Indian Vehicle Registration Information

---

## ★ STAY ETHICAL ★

---

## 📌 About  
Vehicle OSINT Scanner is a professional-grade Open Source Intelligence (OSINT) tool designed for educational and cybersecurity research purposes. Using a publicly available API, the tool fetches detailed information about an Indian vehicle using its registration number and displays the output in a beautiful RGB animated interface.

This enhanced version includes:
- 🌈 **RGB Animated Banner** - Beautiful rainbow-colored ASCII art banner
- 📊 **Interactive Menu System** - Easy-to-use numbered menu options
- 💾 **Smart Caching** - Automatic local caching for faster repeated lookups
- 📋 **Query History** - Track all your previous searches
- 📄 **Multiple Export Formats** - JSON and detailed text reports
- 🎨 **Rich UI** - Beautiful colored output using Rich library

---

## ⚙️ Features  

### Core Features
✔ Beautiful RGB animated banner with "HACK WITH_NIHAL" branding  
✔ Interactive menu system with 6 options  
✔ Real-time API lookup for vehicle information  
✔ Smart caching system for faster repeated queries  
✔ Query history tracking and viewing  
✔ Cache management (view and clear options)  
✔ Multiple export formats (JSON + Text reports)  

### Technical Features
✔ Auto screen clear on run  
✔ Professional disclaimer panel  
✔ Error handling with user-friendly messages  
✔ Internet connection check  
✔ System information display  
✔ Works on Windows, Termux & Linux  
✔ Beginner-friendly clean source code  

---

## 🖥️ Screenshots

### RGB Banner
```
██╗  ██╗ █████╗  ██████╗██╗  ██╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝
███████║███████║██║     █████╔╝ 
██╔══██║██╔══██║██║     ██╔═██╗ 
██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

██╗    ██╗██╗███╗   ██╗
██║    ██║██║████╗  ██║
██║ █╗ ██║██║██╔██╗ ██║
██║███╗██║██║██║╚██╗██║
╚███╔███╔╝██║██║ ╚████║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝

███╗   ██╗██╗   ██╗██╗  ██╗
████╗  ██║██║   ██║██║ ██╔╝
██╔██╗ ██║██║   ██║█████╔╝ 
██║╚██╗██║██║   ██║██╔═██╗ 
██║ ╚████║╚██████╔╝██║  ██╗
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝

★ STAY ETHICAL ★
```

---

## ⚠️ Legal Disclaimer  
This tool is strictly for:

- ✅ Ethical research  
- ✅ Cyber awareness  
- ✅ OSINT investigations  
- ✅ Educational demonstrations  

❌ Unauthorized use, privacy violation, cybercrime, or misuse of this tool is completely illegal.  
The user is solely responsible for their actions.

**★ STAY ETHICAL ★**

---

## 📥 Installation

### Supported Platforms
- **Termux** 📱
- **Windows** 💻
- **Kali Linux** 🐧
- **Ubuntu/Debian** 🌱
- **Parrot OS** 🕵️‍♂️
- **Arch Linux** 🐧

---

## Windows 10/11 Installation (PowerShell)  

### Step 1: Install Python  
1. Go to: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
2. Click **"Download Python 3.12"** (or latest)  
3. Run the installer  
4. **CHECK THIS BOX**: `Add Python to PATH`  
5. Click **"Install Now"**  

> Verify: Open **PowerShell** → Type:  
> `python --version`

### Step 2: Install Git  
1. Go to: [https://git-scm.com/download/win](https://git-scm.com/download/win)  
2. Download and install Git

### Step 3: Clone and Run
```bash
git clone https://github.com/thakur2309/vehicle-osint-scanner.git
cd vehicle-osint-scanner

# Install requirements (only needed once)
pip install -r requirements.txt

# Run the tool
python vehicle_lookup.py
```

---

## 🐧 Linux & Termux Setup

### Kali Linux / Ubuntu / Debian / Parrot OS
```bash
sudo apt update
git clone https://github.com/thakur2309/vehicle-osint-scanner.git
cd vehicle-osint-scanner

# Install requirements (only needed once)
pip install -r requirements.txt

# Run the tool
python vehicle_lookup.py
```

### Termux (Android)
```bash
pkg update
pkg install python git

git clone https://github.com/thakur2309/vehicle-osint-scanner.git
cd vehicle-osint-scanner

# Install requirements (only needed once)
pip install -r requirements.txt

# Run the tool
python vehicle_lookup.py
```

---

## 📋 Menu Options

| Option | Description |
|--------|-------------|
| 1 | 🔍 Look up vehicle by RC number |
| 2 | 📂 View cached results |
| 3 | 📋 View query history |
| 4 | 🗑️ Clear cache |
| 5 | ℹ️ About / Help |
| 6 | 🚪 Exit |

---

## 📁 Output Directories

| Directory | Purpose |
|-----------|---------|
| `results/` | JSON files with vehicle data |
| `reports/` | Detailed text reports |
| `logs/` | Query history logs |
| `cache/` | Cached API responses |

---

## 🎯 Intended Uses

- ✅ Ethical OSINT training  
- ✅ Cybersecurity workshops  
- ✅ Personal number verification  
- ✅ Red team research (with permission)  

---

## ❌ Prohibited Uses

- ❌ Unauthorized data access  
- ❌ Privacy invasion or doxxing  
- ❌ Illegal surveillance  
- ❌ Commercial redistribution  
- ❌ Cracking or bypassing license  

---

## 📜 License

This tool is for **educational purposes only**. Use responsibly.

---

## 👨‍💻 Credits

- **Enhanced by:** HACK WITH_NIHAL
- **Original Creator:** thakur2309 (Firewall Breaker)
- **Original Repository:** [vehicle-osint-scanner](https://github.com/thakur2309/vehicle-osint-scanner)

---

## ⚠️ Disclaimer
This tool is intended **only for educational and lawful use** on devices **you own** or have **explicit permission** to manage. The creator and contributors are **not responsible** for any misuse.  

**★ STAY ETHICAL ★**  
**★ HACK WITH_NIHAL ★**

---

**Made with ❤️ by HACK WITH_NIHAL**
