# core/menu.py
# CarrotHunter - Interactive Menu System
# Academic Security Research Tool - Isolated Lab Only

import os
import sys
import time

# Import banner and colors
try:
    from .banner import (
        Colors as C,
        show_banner,
        show_small_banner,
        show_section_header,
        clear_screen,
    )
except ImportError:
    from banner import (
        Colors as C,
        show_banner,
        show_small_banner,
        show_section_header,
        clear_screen,
    )


# =============================================
# MAIN MENU
# =============================================

def show_main_menu():
    """Display the main menu"""
    clear_screen()
    show_banner(clear=False)
    
    print(f"""
{C.CYAN}  ╔═══════════════════════════════════════════════╗
{C.CYAN}  ║{C.WHITE}            SCANNING MODULES                    {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[1]{C.RESET}  Reconnaissance                        {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[2]{C.RESET}  Port Scanning                         {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[3]{C.RESET}  Web Scanning                          {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[4]{C.RESET}  CMS Detection                         {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.WHITE}           EXPLOITATION MODULES                 {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[5]{C.RESET}  SQL Injection                         {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[6]{C.RESET}  XSS (Cross-Site Scripting)            {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[7]{C.RESET}  LFI (Local File Inclusion)            {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[8]{C.RESET}  Command Injection                     {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[9]{C.RESET}  SSRF (Server-Side Request Forgery)    {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[10]{C.RESET} File Upload                           {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.WHITE}              AUTOMATION                       {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[11]{C.RESET} Full Scan (All Modules)               {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[12]{C.RESET} Generate Report                       {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.WHITE}               TOOLS                         {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[13]{C.RESET} Metasploit Launcher                   {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[14]{C.RESET} Settings                              {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[15]{C.RESET} Help                                  {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.RED}[0]{C.RESET}  Exit                                  {C.CYAN}║
{C.CYAN}  ╚═══════════════════════════════════════════════╝{C.RESET}
""")


# =============================================
# SETTINGS MENU
# =============================================

def show_settings_menu():
    """Display settings menu"""
    clear_screen()
    show_small_banner()
    
    print(f"""
{C.CYAN}  ╔═══════════════════════════════════════════════╗
{C.CYAN}  ║{C.WHITE}              SETTINGS                          {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[1]{C.RESET}  View Configuration                    {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[2]{C.RESET}  Edit Configuration                    {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[3]{C.RESET}  Reset to Defaults                     {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[4]{C.RESET}  View Logs                             {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[5]{C.RESET}  Clear Logs                            {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[6]{C.RESET}  View Reports                          {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[7]{C.RESET}  Clear Reports                         {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[8]{C.RESET}  Update CarrotHunter                   {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[9]{C.RESET}  Check Dependencies                    {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[0]{C.RESET}  Back to Main Menu                     {C.CYAN}║
{C.CYAN}  ╚═══════════════════════════════════════════════╝{C.RESET}
""")


# =============================================
# METASPLOIT MENU
# =============================================

def show_metasploit_menu():
    """Display Metasploit menu"""
    clear_screen()
    show_small_banner()
    
    print(f"""
{C.CYAN}  ╔═══════════════════════════════════════════════╗
{C.CYAN}  ║{C.WHITE}          METASPLOIT LAUNCHER                   {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[1]{C.RESET}  Launch msfconsole                     {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[2]{C.RESET}  Generate Android Payload (APK)        {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[3]{C.RESET}  Generate Windows Payload (EXE)        {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[4]{C.RESET}  Generate Linux Payload (ELF)          {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[5]{C.RESET}  Start Listener (Multi/Handler)        {C.CYAN}║
{C.CYAN}  ║{C.RESET}  {C.GREEN}[6]{C.RESET}  Setup Database                        {C.CYAN}║
{C.CYAN}  ╠═══════════════════════════════════════════════╣
{C.CYAN}  ║{C.RESET}  {C.GREEN}[0]{C.RESET}  Back to Main Menu                     {C.CYAN}║
{C.CYAN}  ╚═══════════════════════════════════════════════╝{C.RESET}
""")


# =============================================
# HELP MENU
# =============================================

def show_help():
    """Display help information"""
    clear_screen()
    show_small_banner()
    
    print(f"""
{C.CYAN}  ╔═══════════════════════════════════════════════╗
{C.CYAN}  ║{C.WHITE}                 HELP                           {C.CYAN}║
{C.CYAN}  ╚═══════════════════════════════════════════════╝{C.RESET}

{C.YELLOW}  About:{C.RESET}
  CarrotHunter is an academic security research tool for
  web application vulnerability assessment in isolated
  lab environments.

{C.YELLOW}  Scanning Modules:{C.RESET}
  {C.GREEN}[1]{C.RESET} Reconnaissance    - DNS, WHOIS, Headers, Technologies
  {C.GREEN}[2]{C.RESET} Port Scanning     - Open ports detection
  {C.GREEN}[3]{C.RESET} Web Scanning      - Directories, Files, Methods
  {C.GREEN}[4]{C.RESET} CMS Detection     - WordPress, Joomla, Craft

{C.YELLOW}  Exploitation Modules:{C.RESET}
  {C.GREEN}[5]{C.RESET} SQL Injection     - Error, Union, Boolean, Time-based
  {C.GREEN}[6]{C.RESET} XSS               - Reflected, Stored, DOM-based
  {C.GREEN}[7]{C.RESET} LFI               - Local File Inclusion, Traversal
  {C.GREEN}[8]{C.RESET} Command Injection - OS Command Injection
  {C.GREEN}[9]{C.RESET} SSRF              - Server-Side Request Forgery
  {C.GREEN}[10]{C.RESET} File Upload      - Unrestricted Upload, Bypass

{C.YELLOW}  Example Usage:{C.RESET}
  {C.CYAN}1.{C.RESET} Choose {C.GREEN}[11]{C.RESET} for Full Scan
  {C.CYAN}2.{C.RESET} Enter target: {C.GREEN}http://testphp.vulnweb.com{C.RESET}
  {C.CYAN}3.{C.RESET} Wait for scan to complete
  {C.CYAN}4.{C.RESET} View report in {C.GREEN}reports/{C.RESET} directory

{C.YELLOW}  Output:{C.RESET}
  - JSON report: {C.GREEN}reports/report_*.json{C.RESET}
  - HTML report: {C.GREEN}reports/report_*.html{C.RESET}
  - Logs:        {C.GREEN}logs/scan_*.log{C.RESET}
  - Loot:        {C.GREEN}reports/loot/{C.RESET}

{C.YELLOW}  Important Notes:{C.RESET}
  {C.RED}⚠{C.RESET} Use ONLY in isolated lab environment
  {C.RED}⚠{C.RESET} Never target systems you don't own
  {C.RED}⚠{C.RESET} Get written authorization before testing

{C.YELLOW}  Troubleshooting:{C.RESET}
  - Permission denied: {C.GREEN}chmod +x *.sh{C.RESET}
  - Missing modules:   {C.GREEN}./setup.sh{C.RESET}
  - SSL errors:        {C.GREEN}pkg install ca-certificates{C.RESET}
  - Storage access:    {C.GREEN}termux-setup-storage{C.RESET}

{C.YELLOW}  Links:{C.RESET}
  - Documentation: README.md
  - Report bugs:   GitHub Issues

{C.MAGENTA}═══════════════════════════════════════════════{C.RESET}
""")


# =============================================
# INPUT HANDLERS
# =============================================

def get_menu_choice(prompt="Choose option"):
    """Get user menu choice"""
    try:
        choice = input(f"{C.YELLOW}  [?] {prompt}: {C.RESET}").strip()
        return choice
    except (KeyboardInterrupt, EOFError):
        print()
        return "0"


def get_target_input():
    """Get target URL from user"""
    try:
        target = input(f"{C.YELLOW}  [?] Enter target URL: {C.RESET}").strip()
        
        if not target:
            return None
        
        # Add http:// if missing
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        return target
    except (KeyboardInterrupt, EOFError):
        print()
        return None


def get_yes_no(prompt="Continue"):
    """Get yes/no confirmation"""
    try:
        response = input(f"{C.YELLOW}  [?] {prompt} (y/n): {C.RESET}").strip().lower()
        return response in ['y', 'yes']
    except (KeyboardInterrupt, EOFError):
        print()
        return False


def wait_for_enter():
    """Wait for user to press Enter"""
    try:
        input(f"\n{C.DIM}  Press Enter to continue...{C.RESET}")
    except (KeyboardInterrupt, EOFError):
        print()


# =============================================
# MENU HANDLERS
# =============================================

def handle_main_menu_choice(choice):
    """Handle main menu choice - returns action string"""
    
    menu_actions = {
        # Scanning
        "1": "recon",
        "2": "port",
        "3": "web",
        "4": "cms",
        
        # Exploitation
        "5": "sqli",
        "6": "xss",
        "7": "lfi",
        "8": "cmdi",
        "9": "ssrf",
        "10": "upload",
        
        # Automation
        "11": "full",
        "12": "report",
        
        # Tools
        "13": "metasploit",
        "14": "settings",
        "15": "help",
        
        # Exit
        "0": "exit",
        "q": "exit",
        "quit": "exit",
    }
    
    return menu_actions.get(choice, "invalid")


def handle_settings_choice(choice):
    """Handle settings menu choice"""
    
    settings_actions = {
        "1": "view_config",
        "2": "edit_config",
        "3": "reset_config",
        "4": "view_logs",
        "5": "clear_logs",
        "6": "view_reports",
        "7": "clear_reports",
        "8": "update_tool",
        "9": "check_deps",
        "0": "back",
    }
    
    return settings_actions.get(choice, "invalid")


def handle_metasploit_choice(choice):
    """Handle metasploit menu choice"""
    
    msf_actions = {
        "1": "launch_msf",
        "2": "android_payload",
        "3": "windows_payload",
        "4": "linux_payload",
        "5": "start_listener",
        "6": "setup_db",
        "0": "back",
    }
    
    return msf_actions.get(choice, "invalid")


# =============================================
# ALIASES
# =============================================

# For backward compatibility
handle_menu_choice = handle_main_menu_choice


# =============================================
# EXPORTS
# =============================================

__all__ = [
    "show_main_menu",
    "show_settings_menu",
    "show_metasploit_menu",
    "show_help",
    "get_menu_choice",
    "get_target_input",
    "get_yes_no",
    "wait_for_enter",
    "handle_main_menu_choice",
    "handle_menu_choice",
    "handle_settings_choice",
    "handle_metasploit_choice",
]