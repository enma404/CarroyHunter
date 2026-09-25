#!/data/data/com.termux/files/usr/bin/bash
# setup.sh
# CarrotHunter - Setup Script for Termux
# Academic Security Research Tool - Isolated Lab Only

# =============================================
# CONFIGURATION
# =============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m'

# =============================================
# BANNER
# =============================================

show_banner() {
    clear
    echo -e "${RED}"
    cat << "EOF"
   ██████╗ █████╗ ██████╗ ██████╗  ██████╗ ████████╗
  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
  ██║     ███████║██████╔╝██████╔╝██║   ██║   ██║   
  ██║     ██╔══██║██╔══██╗██╔══██╗██║   ██║   ██║   
  ╚██████╗██║  ██║██║  ██║██║  ██║╚██████╔╝   ██║   
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   
EOF
    echo -e "${NC}"
    echo -e "${YELLOW}              H U N T E R  v1.0${NC}"
    echo -e "${CYAN}    Academic Security Research Tool${NC}"
    echo -e "${GREEN}    Isolated Lab Environment Only${NC}"
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}              SETUP INSTALLER${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════${NC}"
    echo ""
}

# =============================================
# LOGGING FUNCTIONS
# =============================================

log_info()  { echo -e "${CYAN}[*]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_step()  { echo -e "\n${MAGENTA}▶ $1${NC}"; }

# =============================================
# CHECK TERMUX
# =============================================

check_termux() {
    if [ ! -d "/data/data/com.termux" ]; then
        log_error "This script must be run inside Termux"
        echo ""
        echo -e "${YELLOW}[!] Download Termux from F-Droid:${NC}"
        echo -e "    https://f-droid.org/packages/com.termux/"
        exit 1
    fi
    log_ok "Termux detected"
}

# =============================================
# STEP 1: UPDATE PACKAGES
# =============================================

update_packages() {
    log_step "STEP 1/7: Updating Package Lists"
    
    # Update package lists
    if ! pkg update -y 2>/dev/null; then
        log_warn "Package update failed, trying mirror change..."
        termux-change-repo
        pkg update -y
    fi
    
    log_ok "Package lists updated"
}

# =============================================
# STEP 2: INSTALL CORE PACKAGES
# =============================================

install_core_packages() {
    log_step "STEP 2/7: Installing Core Packages"
    
    # Core dependencies
    PACKAGES=(
        "python"
        "python-pip"
        "git"
        "curl"
        "wget"
        "openssl"
        "openssl-tool"
        "libxml2"
        "libxslt"
        "clang"
        "make"
        "nano"
        "which"
        "termux-api"
    )
    
    for pkg in "${PACKAGES[@]}"; do
        if ! pkg list-installed 2>/dev/null | grep -q "^$pkg/"; then
            log_info "Installing $pkg..."
            pkg install -y "$pkg" -o Dpkg::Options::="--force-confnew" 2>/dev/null || {
                log_warn "Failed to install $pkg (may already exist)"
            }
        else
            log_ok "$pkg already installed"
        fi
    done
    
    log_ok "Core packages installed"
}

# =============================================
# STEP 3: UPGRADE PIP
# =============================================

upgrade_pip() {
    log_step "STEP 3/7: Upgrading pip"
    
    python3 -m pip install --upgrade pip setuptools wheel 2>&1 | tail -2
    
    log_ok "pip upgraded"
}

# =============================================
# STEP 4: INSTALL PYTHON LIBRARIES
# =============================================

install_python_libs() {
    log_step "STEP 4/7: Installing Python Libraries"
    
    # Required libraries
    LIBS=(
        "requests"
        "urllib3"
        "beautifulsoup4"
        "lxml"
        "colorama"
        "dnspython"
        "python-whois"
        "pyOpenSSL"
        "cryptography"
        "tldextract"
        "chardet"
        "idna"
        "certifi"
    )
    
    for lib in "${LIBS[@]}"; do
        log_info "Installing $lib..."
        python3 -m pip install "$lib" 2>&1 | tail -1
    done
    
    log_ok "Python libraries installed"
}

# =============================================
# STEP 5: CREATE DIRECTORIES
# =============================================

create_directories() {
    log_step "STEP 5/7: Creating Project Directories"
    
    DIRS=(
        "core"
        "scanners"
        "exploits"
        "payloads"
        "payloads/output"
        "config"
        "reports"
        "reports/loot"
        "logs"
        "wordlists"
        "downloads"
    )
    
    for dir in "${DIRS[@]}"; do
        mkdir -p "$SCRIPT_DIR/$dir"
        touch "$SCRIPT_DIR/$dir/.gitkeep" 2>/dev/null
        log_ok "Created: $dir"
    done
    
    # Set permissions
    chmod +x "$SCRIPT_DIR/carrot.sh" 2>/dev/null || true
    chmod +x "$SCRIPT_DIR/setup.sh" 2>/dev/null || true
    chmod +x "$SCRIPT_DIR/metasploit.sh" 2>/dev/null || true
    
    log_ok "Directories created"
}

# =============================================
# STEP 6: CREATE CONFIG FILE
# =============================================

create_config() {
    log_step "STEP 6/7: Creating Configuration File"
    
    if [ ! -f "$SCRIPT_DIR/config/config.json" ]; then
        cat > "$SCRIPT_DIR/config/config.json" << 'EOF'
{
    "name": "CarrotHunter",
    "version": "1.0.0",
    "description": "Academic Security Research Tool - Isolated Lab Only",
    
    "scan_settings": {
        "timeout": 10,
        "threads": 10,
        "user_agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
        "max_redirects": 5,
        "verify_ssl": false,
        "follow_redirects": true
    },
    
    "modules": {
        "recon": { "enabled": true },
        "port": { "enabled": true },
        "web": { "enabled": true },
        "cms": { "enabled": true },
        "sqli": { "enabled": true, "severity": "CRITICAL" },
        "xss": { "enabled": true, "severity": "MEDIUM" },
        "lfi": { "enabled": true, "severity": "HIGH" },
        "cmdi": { "enabled": true, "severity": "CRITICAL" },
        "ssrf": { "enabled": true, "severity": "HIGH" },
        "upload": { "enabled": true, "severity": "CRITICAL" }
    },
    
    "output": {
        "report_dir": "reports",
        "log_dir": "logs",
        "save_json": true,
        "save_html": true
    },
    
    "ethical_guardrails": {
        "require_authorization": true,
        "isolated_lab_only": true
    }
}
EOF
        log_ok "Config file created"
    else
        log_ok "Config file already exists"
    fi
}

# =============================================
# STEP 7: VERIFY INSTALLATION
# =============================================

verify_installation() {
    log_step "STEP 7/7: Verifying Installation"
    
    echo ""
    echo -e "${CYAN}  Environment Check:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    
    # Python
    if command -v python3 &>/dev/null; then
        PY_VERSION=$(python3 --version 2>&1)
        log_ok "$PY_VERSION"
    else
        log_error "Python3 not found"
    fi
    
    # Pip
    if command -v pip3 &>/dev/null || python3 -m pip --version &>/dev/null; then
        log_ok "pip installed"
    else
        log_error "pip not found"
    fi
    
    # Git
    if command -v git &>/dev/null; then
        log_ok "Git installed"
    else
        log_warn "Git not found"
    fi
    
    # Curl
    if command -v curl &>/dev/null; then
        log_ok "curl installed"
    else
        log_warn "curl not found"
    fi
    
    # OpenSSL
    if command -v openssl &>/dev/null; then
        log_ok "OpenSSL installed"
    else
        log_warn "OpenSSL not found"
    fi
    
    echo ""
    echo -e "${CYAN}  Python Libraries Check:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    
    # Check Python libraries
    LIBS_CHECK=(
        "requests:requests"
        "bs4:beautifulsoup4"
        "colorama:colorama"
        "dns:dnspython"
        "OpenSSL:pyOpenSSL"
        "cryptography:cryptography"
    )
    
    for lib_check in "${LIBS_CHECK[@]}"; do
        lib_name="${lib_check%%:*}"
        lib_full="${lib_check##*:}"
        
        if python3 -c "import $lib_name" 2>/dev/null; then
            log_ok "$lib_full"
        else
            log_error "$lib_full missing"
        fi
    done
    
    echo ""
    echo -e "${CYAN}  Directory Structure:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    
    DIRS_CHECK=(
        "core"
        "scanners"
        "exploits"
        "payloads"
        "config"
        "reports"
        "logs"
    )
    
    for dir in "${DIRS_CHECK[@]}"; do
        if [ -d "$SCRIPT_DIR/$dir" ]; then
            log_ok "$dir/"
        else
            log_error "$dir/ missing"
        fi
    done
}

# =============================================
# FINAL MESSAGE
# =============================================

show_completion() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
    echo -e "${GREEN}         SETUP COMPLETED SUCCESSFULLY${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}  🥕 CarrotHunter is ready to use!${NC}"
    echo ""
    echo -e "${WHITE}  How to use:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    echo -e "  ${GREEN}./carrot.sh${NC}              ${WHITE}# Launch CarrotHunter${NC}"
    echo ""
    echo -e "${WHITE}  Optional installations:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    echo -e "  ${GREEN}./metasploit.sh${NC}          ${WHITE}# Install Metasploit${NC}"
    echo ""
    echo -e "${WHITE}  Quick commands:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    echo -e "  ${GREEN}python3 core/runner.py --help${NC}     ${WHITE}# CLI help${NC}"
    echo -e "  ${GREEN}ls reports/${NC}                     ${WHITE}# View reports${NC}"
    echo -e "  ${GREEN}ls logs/${NC}                        ${WHITE}# View logs${NC}"
    echo ""
    echo -e "${YELLOW}  [⚠] Ethical Warning:${NC}"
    echo -e "${YELLOW}  ─────────────────────────────────────${NC}"
    echo -e "${YELLOW}  This tool is for ACADEMIC use only.${NC}"
    echo -e "${YELLOW}  Use it ONLY in isolated lab environments.${NC}"
    echo -e "${YELLOW}  Never scan systems you don't own.${NC}"
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  Stay ethical. Stay safe. Happy hunting! 🥕${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════${NC}"
    echo ""
}

# =============================================
# MAIN EXECUTION
# =============================================

main() {
    # Show banner
    show_banner
    
    # Check environment
    check_termux
    echo ""
    
    # Run steps
    update_packages
    install_core_packages
    upgrade_pip
    install_python_libs
    create_directories
    create_config
    verify_installation
    
    # Show completion
    show_completion
    
    # Ask to launch
    echo -ne "${YELLOW}[?] Launch CarrotHunter now? (y/n): ${NC}"
    read -r launch
    
    if [[ "$launch" =~ ^[Yy]$ ]]; then
        exec "$SCRIPT_DIR/carrot.sh"
    fi
}

# Handle Ctrl+C
trap 'echo -e "\n${YELLOW}[!] Setup interrupted${NC}"; exit 1' INT

# Run main
main