# core/banner.py
# CarrotHunter - Banner Module
# ASCII art banners and visual elements

import os
import sys
import time
import random

# =============================================
# COLORS
# =============================================

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


C = Colors

# =============================================
# BANNER TEXT
# =============================================

CARROT_BANNER = f"""
{C.RED}   ██████╗ █████╗ ██████╗ ██████╗  ██████╗ ████████╗
{C.RED}  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
{C.RED}  ██║     ███████║██████╔╝██████╔╝██║   ██║   ██║   
{C.RED}  ██║     ██╔══██║██╔══██╗██╔══██╗██║   ██║   ██║   
{C.RED}  ╚██████╗██║  ██║██║  ██║██║  ██║╚██████╔╝   ██║   
{C.RED}   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   
{C.RESET}
{C.YELLOW}               H U N T E R  v1.0
{C.CYAN}      Academic Security Research Tool
{C.GREEN}      Isolated Lab Environment Only
{C.RESET}
"""

SMALL_BANNER = f"""
{C.RED}╔═══════════════════════════════════════════════╗
{C.RED}║{C.YELLOW}          🥕  C A R R O T H U N T E R  🥕       {C.RED}║
{C.RED}║{C.CYAN}         Web Security Assessment Tool         {C.RED}║
{C.RED}║{C.GREEN}              v1.0.0  |  Termux               {C.RED}║
{C.RED}╚═══════════════════════════════════════════════╝{C.RESET}
"""

MINI_BANNER = f"{C.RED}[🥕 CarrotHunter]{C.RESET}"


# =============================================
# FUNCTIONS
# =============================================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_width():
    """Get terminal width"""
    try:
        return os.get_terminal_size().columns
    except:
        return 80


def center_text(text, width=None):
    """Center text in terminal"""
    if width is None:
        width = get_terminal_width()
    
    # Remove ANSI color codes for length calculation
    import re
    clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
    padding = max(0, (width - len(clean_text)) // 2)
    
    return ' ' * padding + text


def show_banner(clear=True):
    """Show main banner"""
    if clear:
        clear_screen()
    print(CARROT_BANNER)


def show_small_banner():
    """Show small banner"""
    print(SMALL_BANNER)


def show_mini_banner():
    """Show mini banner"""
    print(MINI_BANNER)


def show_completion_banner():
    """Show completion banner"""
    print(f"""
{C.GREEN}╔═══════════════════════════════════════════════╗
{C.GREEN}║{C.WHITE}          ✓ SCAN COMPLETED SUCCESSFULLY        {C.GREEN}║
{C.GREEN}╚═══════════════════════════════════════════════╝{C.RESET}
""")


def show_loading_banner(message="Loading"):
    """Show loading message with spinner"""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    for i in range(20):
        sys.stdout.write(f'\r{C.CYAN}{spinner[i % len(spinner)]}{C.RESET} {message}...')
        sys.stdout.flush()
        time.sleep(0.1)
    
    sys.stdout.write(f'\r{C.GREEN}✓{C.RESET} {message}... Done!{" " * 20}\n')
    sys.stdout.flush()


def show_progress_bar(current, total, prefix="Progress", length=40):
    """Show progress bar"""
    percent = current / total if total > 0 else 0
    filled = int(length * percent)
    bar = '█' * filled + '░' * (length - filled)
    
    sys.stdout.write(f'\r{C.CYAN}{prefix}:{C.RESET} |{C.GREEN}{bar}{C.RESET}| {percent*100:.1f}%')
    sys.stdout.flush()
    
    if current == total:
        sys.stdout.write('\n')


def show_phase_header(phase_num, phase_name, total_phases=6):
    """Show phase header"""
    print(f"""
{C.MAGENTA}═══════════════════════════════════════════════
{C.WHITE}  PHASE {phase_num}/{total_phases}: {phase_name.upper()}
{C.MAGENTA}═══════════════════════════════════════════════{C.RESET}
""")


def show_section_header(title):
    """Show section header"""
    width = 60
    print(f"\n{C.CYAN}{'─' * width}{C.RESET}")
    print(f"{C.WHITE}  {title}{C.RESET}")
    print(f"{C.CYAN}{'─' * width}{C.RESET}\n")


def show_vuln_alert(vuln_type, severity, url):
    """Show vulnerability alert"""
    severity_colors = {
        'CRITICAL': C.RED,
        'HIGH': C.YELLOW,
        'MEDIUM': C.CYAN,
        'LOW': C.GREEN,
    }
    
    color = severity_colors.get(severity.upper(), C.WHITE)
    
    print(f"""
{color}  ┌─────────────────────────────────────────────┐
{color}  │ {C.WHITE}[!] VULNERABILITY DETECTED{C.RESET}
{color}  ├─────────────────────────────────────────────┤
{color}  │ {C.WHITE}Type:{C.RESET}     {vuln_type}
{color}  │ {C.WHITE}Severity:{C.RESET} {color}{severity}{C.RESET}
{color}  │ {C.WHITE}URL:{C.RESET}      {url[:45]}
{color}  └─────────────────────────────────────────────┘{C.RESET}
""")


def show_success(message):
    """Show success message"""
    print(f"{C.GREEN}  [✓] {message}{C.RESET}")


def show_error(message):
    """Show error message"""
    print(f"{C.RED}  [✗] {message}{C.RESET}")


def show_warning(message):
    """Show warning message"""
    print(f"{C.YELLOW}  [!] {message}{C.RESET}")


def show_info(message):
    """Show info message"""
    print(f"{C.CYAN}  [*] {message}{C.RESET}")


def show_scan_summary(target, duration, vulns_count, report_path):
    """Show scan summary"""
    print(f"""
{C.CYAN}╔═══════════════════════════════════════════════╗
{C.CYAN}║{C.WHITE}              SCAN SUMMARY                    {C.CYAN}║
{C.CYAN}╠═══════════════════════════════════════════════╣
{C.CYAN}║{C.GREEN}  Target:       {C.WHITE}{target[:30]:<30}{C.CYAN}║
{C.CYAN}║{C.GREEN}  Duration:     {C.WHITE}{duration:<30}{C.CYAN}║
{C.CYAN}║{C.GREEN}  Vulnerabilities: {C.RED}{vulns_count:<26}{C.CYAN}║
{C.CYAN}║{C.GREEN}  Report:       {C.WHITE}{report_path[:30]:<30}{C.CYAN}║
{C.CYAN}╚═══════════════════════════════════════════════╝{C.RESET}
""")


def animate_text(text, delay=0.03, color=C.GREEN):
    """Animate text typing"""
    for char in text:
        sys.stdout.write(f'{color}{char}{C.RESET}')
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_matrix_effect(duration=2):
    """Show matrix effect (short)"""
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"
    width = get_terminal_width()
    
    start = time.time()
    while time.time() - start < duration:
        line = ''.join(random.choice(chars) for _ in range(width))
        print(f"{C.GREEN}{line}{C.RESET}")
        time.sleep(0.05)


def show_skull():
    """Show ASCII skull"""
    print(f"""
{C.RED}        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
{C.RED}      ████████████████████████████████████
{C.RED}    ████████████████████████████████████████
{C.RED}   ██████████████████████████████████████████
{C.RED}   ████████████▀▀████████████▀▀████████████
{C.RED}   ████████████  ████████████  ████████████
{C.RED}   ████████████▄▄████████████▄▄████████████
{C.RED}   ██████████████████████████████████████████
{C.RED}   ██████████████████████████████████████████
{C.RED}    ████████████████████████████████████████
{C.RED}      ████████████████████████████████████
{C.RED}        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
{C.RESET}""")


def show_carrot():
    """Show ASCII carrot"""
    print(f"""
{C.YELLOW}         ▄
{C.YELLOW}        ███
{C.GREEN}       █████
{C.GREEN}      ███████
{C.GREEN}     █████████
{C.GREEN}    ███████████
{C.GREEN}   █████████████
{C.GREEN}  ███████████████
{C.GREEN}   █████████████
{C.GREEN}    ███████████
{C.GREEN}     █████████
{C.GREEN}      ███████
{C.GREEN}       █████
{C.GREEN}        ███
{C.GREEN}         █
{C.RESET}""")


# =============================================
# EXPORTS
# =============================================

__all__ = [
    "Colors",
    "C",
    "CARROT_BANNER",
    "SMALL_BANNER",
    "MINI_BANNER",
    "clear_screen",
    "get_terminal_width",
    "center_text",
    "show_banner",
    "show_small_banner",
    "show_mini_banner",
    "show_completion_banner",
    "show_loading_banner",
    "show_progress_bar",
    "show_phase_header",
    "show_section_header",
    "show_vuln_alert",
    "show_success",
    "show_error",
    "show_warning",
    "show_info",
    "show_scan_summary",
    "animate_text",
    "show_matrix_effect",
    "show_skull",
    "show_carrot",
]