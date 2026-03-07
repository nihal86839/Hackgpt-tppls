#!/usr/bin/env python3
# Vehicle OSINT Scanner - Enhanced Edition
# Modified by: HACK WITH_NIHAL
# Original Creator: thakur2309

"""
DISCLAIMER:
This tool is for EDUCATIONAL and ETHICAL USE ONLY.
Unauthorized tracking, surveillance or background searches
without permission may be ILLEGAL. Use responsibly.
STAY ETHICAL - HACK WITH_NIHAL
"""

import sys
import os
import json
import time
import hashlib
import requests
import platform
import subprocess
from urllib.parse import urlencode
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.align import Align
from rich.text import Text
from rich.style import Style
from datetime import datetime
from threading import Thread

API_BASE = "https://vehicleinfobyterabaap.vercel.app/lookup"
VERSION = "3.0 ELITE"
console = Console()

# ==================== RGB BANNER SYSTEM ====================
class RGBBanner:
    """Creates animated RGB banner effect"""
    
    def __init__(self):
        self.colors = [
            "bright_red", "bright_green", "bright_yellow", 
            "bright_blue", "bright_magenta", "bright_cyan",
            "red", "green", "yellow", "blue", "magenta", "cyan"
        ]
        self.rainbow_colors = [
            "#FF0000", "#FF7F00", "#FFFF00", "#00FF00", 
            "#0000FF", "#4B0082", "#9400D3",
            "#FF1493", "#00FF7F", "#1E90FF", "#FFD700", "#FF4500"
        ]
    
    def create_rgb_text(self, text, style="bold"):
        """Create text with RGB gradient effect"""
        result = Text()
        for i, char in enumerate(text):
            color = self.rainbow_colors[i % len(self.rainbow_colors)]
            result.append(char, style=Style(color=color, bold=True))
        return result
    
    def animate_banner(self, iterations=3):
        """Display animated RGB banner"""
        banner_lines = [
            "██╗  ██╗ █████╗  ██████╗██╗  ██╗    ███╗   ██╗ ██████╗ ██████╗ ███████╗",
            "██║  ██║██╔══██╗██╔════╝██║ ██╔╝    ████╗  ██║██╔═══██╗██╔══██╗██╔════╝",
            "███████║███████║██║     █████╔╝     ██╔██╗ ██║██║   ██║██║  ██║█████╗  ",
            "██╔══██║██╔══██║██║     ██╔═██╗     ██║╚██╗██║██║   ██║██║  ██║██╔══╝  ",
            "██║  ██║██║  ██║╚██████╗██║  ██╗    ██║ ╚████║╚██████╔╝██████╔╝███████╗",
            "╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝"
        ]
        
        subtitle = "██╗    ██╗██╗███╗   ██╗    ██╗   ██╗██████╗ ███████╗██████╗ "
        subtitle2 = "██║    ██║██║████╗  ██║    ██║   ██║██╔══██╗██╔════╝██╔══██╗"
        subtitle3 = "██║ █╗ ██║██║██╔██╗ ██║    ██║   ██║██████╔╝█████╗  ██████╔╝"
        subtitle4 = "██║███╗██║██║██║╚██╗██║    ██║   ██║██╔══██╗██╔══╝  ██╔══██╗"
        subtitle5 = "╚███╔███╔╝██║██║ ╚████║    ╚██████╔╝██║  ██║███████╗██║  ██║"
        subtitle6 = " ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"
        
        with_lines = [
            "██╗    ██╗██╗███╗   ██╗███████╗██████╗ ",
            "██║    ██║██║████╗  ██║██╔════╝██╔══██╗",
            "██║ █╗ ██║██║██╔██╗ ██║█████╗  ██████╔╝",
            "██║███╗██║██║██║╚██╗██║██╔══╝  ██╔══██╗",
            "╚███╔███╔╝██║██║ ╚████║███████╗██║  ██║",
            " ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
        ]
        
        nihal_lines = [
            "███╗   ██╗██╗   ██╗██╗  ██╗███████╗",
            "████╗  ██║██║   ██║██║ ██╔╝██╔════╝",
            "██╔██╗ ██║██║   ██║█████╔╝ █████╗  ",
            "██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ",
            "██║ ╚████║╚██████╔╝██║  ██╗███████╗",
            "╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
        ]
        
        for _ in range(iterations):
            console.clear()
            # Main HACK banner
            for i, line in enumerate(banner_lines):
                color = self.rainbow_colors[(i + _) % len(self.rainbow_colors)]
                console.print(Align.center(f"[bold {color}]{line}[/bold {color}]"))
                time.sleep(0.02)
            
            console.print()
            
            # WITH banner
            for i, line in enumerate(with_lines):
                color = self.rainbow_colors[(i + _ + 6) % len(self.rainbow_colors)]
                console.print(Align.center(f"[bold {color}]{line}[/bold {color}]"))
                time.sleep(0.02)
            
            console.print()
            
            # NIHAL banner
            for i, line in enumerate(nihal_lines):
                color = self.rainbow_colors[(i + _ + 12) % len(self.rainbow_colors)]
                console.print(Align.center(f"[bold {color}]{line}[/bold {color}]"))
                time.sleep(0.02)
            
            time.sleep(0.15)
        
        console.print()
        console.print(Align.center("[bold bright_white]═══════════════════════════════════════════════════════════[/bold bright_white]"))
        console.print()
        
        # Animated STAY ETHICAL text
        stay_ethical = "★ STAY ETHICAL ★"
        for i, char in enumerate(stay_ethical):
            color = self.rainbow_colors[i % len(self.rainbow_colors)]
            console.print(Align.center(f"[bold {color}]{char}[/bold {color}]"), end="")
            time.sleep(0.03)
        console.print()
        
        console.print()
        console.print(Align.center("[bold bright_white]═══════════════════════════════════════════════════════════[/bold bright_white]"))
        console.print()
        
    def simple_banner(self):
        """Display simple static RGB banner"""
        console.clear()
        
        # HACK banner
        hack_art = [
            "██╗  ██╗ █████╗  ██████╗██╗  ██╗",
            "██║  ██║██╔══██╗██╔════╝██║ ██╔╝",
            "███████║███████║██║     █████╔╝ ",
            "██╔══██║██╔══██║██║     ██╔═██╗ ",
            "██║  ██║██║  ██║╚██████╗██║  ██╗",
            "╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝"
        ]
        
        with_art = [
            "██╗    ██╗██╗███╗   ██╗",
            "██║    ██║██║████╗  ██║",
            "██║ █╗ ██║██║██╔██╗ ██║",
            "██║███╗██║██║██║╚██╗██║",
            "╚███╔███╔╝██║██║ ╚████║",
            " ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝"
        ]
        
        nihal_art = [
            "███╗   ██╗██╗   ██╗██╗  ██╗",
            "████╗  ██║██║   ██║██║ ██╔╝",
            "██╔██╗ ██║██║   ██║█████╔╝ ",
            "██║╚██╗██║██║   ██║██╔═██╗ ",
            "██║ ╚████║╚██████╔╝██║  ██╗",
            "╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝"
        ]
        
        # Print with rainbow colors
        for i, line in enumerate(hack_art):
            color = self.rainbow_colors[i % len(self.rainbow_colors)]
            console.print(Align.center(f"[bold {color}]{line}[/bold {color}]"))
        
        console.print()
        
        for i, line in enumerate(with_art):
            color = self.rainbow_colors[(i + 6) % len(self.rainbow_colors)]
            console.print(Align.center(f"[bold {color}]{line}[/bold {color}]"))
        
        console.print()
        
        for i, line in enumerate(nihal_art):
            color = self.rainbow_colors[(i + 12) % len(self.rainbow_colors)]
            console.print(Align.center(f"[bold {color}]{line}[/bold {color}]"))
        
        console.print()
        console.print(Align.center("[bold bright_white]═══════════════════════════════════════════════════════════[/bold bright_white]"))
        console.print()
        console.print(Align.center("[bold bright_red]★[/bold bright_red] [bold bright_green]STAY[/bold bright_green] [bold bright_yellow]ETHICAL[/bold bright_yellow] [bold bright_red]★[/bold bright_red]"))
        console.print()
        console.print(Align.center("[bold bright_white]═══════════════════════════════════════════════════════════[/bold bright_white]"))
        console.print()


# ==================== UTILITIES ====================
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def ensure_dirs():
    os.makedirs("results", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("cache", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

def log(msg):
    with open("logs/vehicle_osint.log", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def cache_path(rc):
    return f"cache/{hashlib.md5(rc.encode()).hexdigest()}.json"

def save_cache(rc, data):
    with open(cache_path(rc), "w") as f:
        json.dump(data, f, indent=4)

def load_cache(rc):
    path = cache_path(rc)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def get_system_info():
    """Get system information for logging"""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "machine": platform.machine(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def check_internet_connection():
    """Check if internet connection is available"""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False


# ==================== UI / BANNER ====================
def loading_animation():
    console.print("\n[bold green]Initializing Vehicle OSINT Scanner...[/bold green]\n")
    steps = [
        "Loading core modules",
        "Checking network connectivity",
        "Initializing API handlers",
        "Setting up caching system",
        "Loading UI components",
        "Preparing report generator",
        "Starting scan engine"
    ]
    for step in steps:
        console.print(f"[bold cyan]>> {step}...[/bold cyan]")
        time.sleep(0.25)
    time.sleep(0.3)

def banner():
    rgb = RGBBanner()
    rgb.animate_banner(iterations=2)
    
    # Disclaimer
    console.print(
        Panel(
            "[bold white on red] DISCLAIMER [/bold white on red]\n"
            "This tool is for lawful, educational use only.\n"
            "Unauthorized use may be ILLEGAL.\n\n"
            "[bold yellow]★ STAY ETHICAL ★ HACK WITH_NIHAL ★[/bold yellow]",
            style="red",
            expand=False,
        )
    )
    console.print()
    
    # Version info
    version_panel = Panel(
        f"[bold cyan]Version:[/bold cyan] {VERSION}\n"
        f"[bold cyan]Platform:[/bold cyan] {platform.system()} {platform.release()}\n"
        f"[bold cyan]Python:[/bold cyan] {platform.python_version()}",
        title="[bold green]System Info[/bold green]",
        style="green",
        expand=False
    )
    console.print(version_panel)
    console.rule()


# ==================== CORE LOGIC ====================
def get_rc_input():
    console.print("\n[bold cyan]Enter Vehicle RC number:[/bold cyan] ", end="")
    return input().strip().upper()

def validate_rc(rc):
    """Validate RC number format"""
    if not rc:
        return False, "RC number cannot be empty"
    if len(rc) < 4:
        return False, "RC number too short"
    if len(rc) > 15:
        return False, "RC number too long"
    return True, "Valid"

def fetch_vehicle_data(rc):
    cached = load_cache(rc)
    if cached:
        return cached, True

    params = {"rc": rc}
    url = f"{API_BASE}?{urlencode(params)}"

    start = time.time()
    try:
        resp = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "VehicleOSINT/3.0 (by HACK_WITH_NIHAL)"},
        )
    except requests.exceptions.Timeout:
        return {"error": "Request timeout - server took too long to respond"}, False
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error - check your internet connection"}, False
    except Exception as e:
        return {"error": str(e)}, False

    duration = round((time.time() - start) * 1000, 2)

    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code} – {resp.text}"}, False

    try:
        data = resp.json()
    except:
        return {"error": "Invalid JSON returned by API."}, False

    data["_api_time"] = duration
    data["_query_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["_queried_by"] = "HACK WITH_NIHAL Vehicle OSINT Scanner"
    save_cache(rc, data)
    return data, False

def export_json(rc, data):
    path = f"results/{rc}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    return path

def export_text_report(rc, data):
    """Export detailed text report"""
    path = f"reports/{rc}_report.txt"
    with open(path, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("       VEHICLE OSINT SCANNER - DETAILED REPORT\n")
        f.write("            By HACK WITH_NIHAL\n")
        f.write("            ★ STAY ETHICAL ★\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Query Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"RC Number: {rc}\n\n")
        f.write("-" * 60 + "\n")
        f.write("VEHICLE INFORMATION\n")
        f.write("-" * 60 + "\n\n")
        
        for key, value in data.items():
            if not key.startswith("_"):
                formatted_key = key.replace("_", " ").title()
                f.write(f"{formatted_key}: {value}\n")
        
        f.write("\n" + "-" * 60 + "\n")
        f.write("SYSTEM INFORMATION\n")
        f.write("-" * 60 + "\n\n")
        sys_info = get_system_info()
        for key, value in sys_info.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("DISCLAIMER: This tool is for educational purposes only.\n")
        f.write("Unauthorized use may be illegal. STAY ETHICAL!\n")
        f.write("=" * 60 + "\n")
    
    return path

def print_results(rc, data, from_cache):
    tool_info = f"[bold magenta]Vehicle OSINT Scanner[/bold magenta]  •  [bold magenta]v{VERSION}[/bold magenta]\n[bold cyan]★ HACK WITH_NIHAL ★ STAY ETHICAL ★[/bold cyan]"
    console.print(Panel(tool_info, style="magenta", expand=False))

    if "error" in data:
        console.print(Panel(f"[bold red]Error:[/bold red] {data['error']}", style="red"))
        return False

    api_time = data.get("_api_time", None)
    query_time = data.get("_query_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    status = Panel(
        f"[bold green]API Status: OK[/bold green]\n"
        f"Cache: {'[bold yellow]YES[/bold yellow]' if from_cache else '[bold red]NO[/bold red]'}\n"
        f"Response Time: [bold cyan]{api_time} ms[/bold cyan]\n"
        f"Query Time: [bold cyan]{query_time}[/bold cyan]",
        title="[bold green]Status[/bold green]",
        style="green",
        expand=False,
    )
    console.print(status)

    # Store metadata for removal
    metadata_keys = ["_api_time", "_query_time", "_queried_by"]
    display_data = {k: v for k, v in data.items() if k not in metadata_keys}

    # Main vehicle info table
    table = Table(
        title=f"🚗 Vehicle Information — {rc}",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")

    for k, v in display_data.items():
        if v is None or v == "":
            v = "N/A"
        table.add_row(k.replace("_", " ").title(), str(v))

    console.print(table)
    
    # Additional information panel
    additional_info = Panel(
        "[bold green]📁 Results saved to 'results/' folder[/bold green]\n"
        "[bold blue]📋 Logs saved in 'logs/' folder[/bold blue]\n"
        "[bold yellow]📄 Detailed report in 'reports/' folder[/bold yellow]\n\n"
        "[bold white]★ STAY ETHICAL ★ HACK WITH_NIHAL ★[/bold white]",
        title="[bold magenta]Output Files[/bold magenta]",
        style="blue",
        expand=False
    )
    console.print(additional_info)

    console.print(
        Panel(
            Align.center(
                "[bold cyan]Made with ♥ by HACK WITH_NIHAL[/bold cyan]\n"
                "[bold yellow]★ STAY ETHICAL ★[/bold yellow]",
                vertical="middle",
            ),
            style="blue",
        )
    )
    
    return True


# ==================== MENU SYSTEM ====================
def show_menu():
    """Display interactive menu"""
    menu_table = Table(
        title="[bold cyan]VEHICLE OSINT SCANNER MENU[/bold cyan]",
        box=box.ROUNDED,
        show_lines=True,
    )
    menu_table.add_column("Option", style="bold yellow", no_wrap=True)
    menu_table.add_column("Description", style="white")
    
    menu_table.add_row("1", "🔍 Look up vehicle by RC number")
    menu_table.add_row("2", "📂 View cached results")
    menu_table.add_row("3", "📋 View query history")
    menu_table.add_row("4", "🗑️ Clear cache")
    menu_table.add_row("5", "ℹ️  About / Help")
    menu_table.add_row("6", "🚪 Exit")
    
    console.print(menu_table)
    return menu_table

def view_cached_results():
    """View all cached results"""
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        console.print("[bold red]No cache directory found.[/bold red]")
        return
    
    cache_files = [f for f in os.listdir(cache_dir) if f.endswith(".json")]
    if not cache_files:
        console.print("[bold yellow]No cached results found.[/bold yellow]")
        return
    
    console.print(f"\n[bold green]Found {len(cache_files)} cached results:[/bold green]\n")
    
    for i, cache_file in enumerate(cache_files, 1):
        with open(os.path.join(cache_dir, cache_file), "r") as f:
            data = json.load(f)
        
        # Extract key info
        rc_number = "Unknown"
        for key in data:
            if "rc" in key.lower() or "registration" in key.lower():
                rc_number = data[key]
                break
        
        console.print(f"  [bold cyan]{i}.[/bold cyan] Cache file: {cache_file}")
        if rc_number != "Unknown":
            console.print(f"     [dim]RC: {rc_number}[/dim]")
    
    console.print()

def view_query_history():
    """View query history from logs"""
    log_file = "logs/vehicle_osint.log"
    if not os.path.exists(log_file):
        console.print("[bold red]No query history found.[/bold red]")
        return
    
    with open(log_file, "r") as f:
        lines = f.readlines()[-20:]  # Last 20 queries
    
    console.print("\n[bold green]Recent Query History (last 20):[/bold green]\n")
    for line in lines:
        console.print(f"  [dim]{line.strip()}[/dim]")
    console.print()

def clear_cache():
    """Clear all cached results"""
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        console.print("[bold red]No cache directory found.[/bold red]")
        return
    
    cache_files = [f for f in os.listdir(cache_dir) if f.endswith(".json")]
    if not cache_files:
        console.print("[bold yellow]Cache is already empty.[/bold yellow]")
        return
    
    for f in cache_files:
        os.remove(os.path.join(cache_dir, f))
    
    console.print(f"[bold green]Cleared {len(cache_files)} cached results.[/bold green]")

def show_about():
    """Show about information"""
    about_panel = Panel(
        "[bold cyan]Vehicle OSINT Scanner[/bold cyan]\n"
        f"[bold green]Version: {VERSION}[/bold green]\n\n"
        "[bold yellow]★ HACK WITH_NIHAL ★[/bold yellow]\n\n"
        "[white]A professional OSINT tool for fetching\n"
        "Indian vehicle registration information.\n\n"
        "Features:\n"
        "• Real-time API lookup\n"
        "• Local caching system\n"
        "• JSON & Text report export\n"
        "• Query history tracking\n"
        "• Beautiful RGB interface\n\n"
        "[bold red]DISCLAIMER:[/bold red]\n"
        "This tool is for educational purposes only.\n"
        "Unauthorized use may be illegal.\n\n"
        "[bold yellow]★ STAY ETHICAL ★[/bold yellow][/white]",
        title="[bold magenta]About[/bold magenta]",
        style="blue",
        expand=False
    )
    console.print(about_panel)


# ==================== ENTRY ====================
def main():
    ensure_dirs()
    clear_screen()
    loading_animation()
    banner()
    
    # Check internet connection
    if not check_internet_connection():
        console.print("[bold red]Warning: No internet connection detected![/bold red]")
        console.print("[bold yellow]Cached results will still be available.[/bold yellow]\n")
    
    # Interactive menu
    while True:
        console.print()
        show_menu()
        console.print()
        console.print("[bold cyan]Enter your choice (1-6):[/bold cyan] ", end="")
        choice = input().strip()
        
        if choice == "1":
            # Look up vehicle
            rc = get_rc_input()
            if not rc:
                console.print("[bold red]No RC entered.[/bold red]")
                continue
            
            # Validate RC
            is_valid, msg = validate_rc(rc)
            if not is_valid:
                console.print(f"[bold red]Invalid RC: {msg}[/bold red]")
                continue
            
            log(f"Query started for RC: {rc}")
            console.print(f"\n[bold yellow]Looking up vehicle information for: {rc}[/bold yellow]")
            
            data, from_cache = fetch_vehicle_data(rc)
            success = print_results(rc, data, from_cache)
            
            if success:
                export_json(rc, data)
                export_text_report(rc, data)
                log(f"Result exported for RC: {rc}")
            
            console.print("\n[bold green]Done. Press Enter to continue...[/bold green]")
            input()
            clear_screen()
            banner()
            
        elif choice == "2":
            view_cached_results()
            console.print("\n[bold green]Press Enter to continue...[/bold green]")
            input()
            clear_screen()
            banner()
            
        elif choice == "3":
            view_query_history()
            console.print("\n[bold green]Press Enter to continue...[/bold green]")
            input()
            clear_screen()
            banner()
            
        elif choice == "4":
            clear_cache()
            console.print("\n[bold green]Press Enter to continue...[/bold green]")
            input()
            clear_screen()
            banner()
            
        elif choice == "5":
            show_about()
            console.print("\n[bold green]Press Enter to continue...[/bold green]")
            input()
            clear_screen()
            banner()
            
        elif choice == "6":
            console.print("\n[bold cyan]Thank you for using Vehicle OSINT Scanner![/bold cyan]")
            console.print("[bold yellow]★ STAY ETHICAL ★ HACK WITH_NIHAL ★[/bold yellow]")
            console.print("[bold green]Goodbye![/bold green]\n")
            break
            
        else:
            console.print("[bold red]Invalid choice. Please enter 1-6.[/bold red]")
    
    console.print("\n[bold green]Session ended.[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user – exiting.[/bold red]")
        console.print("[bold yellow]★ STAY ETHICAL ★ HACK WITH_NIHAL ★[/bold yellow]")
        sys.exit(0)
