# core/__init__.py
# CarrotHunter - Core Package
# Academic Security Research Tool - Isolated Lab Only

# =============================================
# PACKAGE INFO
# =============================================

__version__ = "1.0.0"
__author__ = "Academic Security Research Lab"
__description__ = "CarrotHunter - Web Security Assessment Tool"
__license__ = "Academic Use Only"

# =============================================
# CORE MODULES
# =============================================

from .banner import show_banner, show_small_banner, show_completion_banner
from .utils import (
    Colors,
    log_info,
    log_ok,
    log_warn,
    log_error,
    log_step,
    print_table,
    print_separator,
    get_target,
    validate_target,
    confirm_action,
    format_size,
    format_time,
    timestamp,
    safe_filename,
)
from .config import Config, load_config, save_config
from .menu import show_main_menu, show_settings_menu, handle_menu_choice
from .runner import Runner, run_scan, run_module

# =============================================
# EXPORTS
# =============================================

__all__ = [
    # Banner
    "show_banner",
    "show_small_banner",
    "show_completion_banner",
    
    # Utils
    "Colors",
    "log_info",
    "log_ok",
    "log_warn",
    "log_error",
    "log_step",
    "print_table",
    "print_separator",
    "get_target",
    "validate_target",
    "confirm_action",
    "format_size",
    "format_time",
    "timestamp",
    "safe_filename",
    
    # Config
    "Config",
    "load_config",
    "save_config",
    
    # Menu
    "show_main_menu",
    "show_settings_menu",
    "handle_menu_choice",
    
    # Runner
    "Runner",
    "run_scan",
    "run_module",
]

# =============================================
# CONSTANTS
# =============================================

VERSION = __version__
TOOL_NAME = "CarrotHunter"
AUTHOR = __author__

# Module categories
SCANNING_MODULES = [
    "recon",
    "port",
    "web",
    "cms",
]

EXPLOITATION_MODULES = [
    "sqli",
    "xss",
    "lfi",
    "cmdi",
    "ssrf",
    "upload",
]

ALL_MODULES = SCANNING_MODULES + EXPLOITATION_MODULES

# Severity levels
SEVERITY_LEVELS = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "INFO": 0,
}

# =============================================
# HELPER FUNCTIONS
# =============================================

def get_version():
    """Return current version"""
    return __version__


def get_module_list(category=None):
    """Return list of available modules"""
    if category == "scanning":
        return SCANNING_MODULES
    elif category == "exploitation":
        return EXPLOITATION_MODULES
    else:
        return ALL_MODULES


def get_severity_score(severity):
    """Return numeric score for severity"""
    return SEVERITY_LEVELS.get(severity.upper(), 0)