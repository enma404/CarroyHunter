# 🥕 CarrotHunter

**Academic Security Research Tool - Isolated Lab Environment Only**

![Version](https://img.shields.io/badge/version-1.0.0-red)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Termux-green)
![License](https://img.shields.io/badge/license-Academic-orange)

---

## 📖 Overview

**CarrotHunter** is a comprehensive, lightweight, and powerful web security assessment tool designed specifically for **Termux (Android)**. It performs automated reconnaissance, vulnerability detection, and optional exploitation against web applications in **isolated lab environments**.

Built for academic cybersecurity research and graduation projects.

---

## ✨ Features

### 🔍 Reconnaissance
- DNS resolution (A, AAAA, MX, NS, TXT, CNAME, SOA)
- HTTP headers analysis
- Security headers check (HSTS, CSP, X-Frame-Options)
- Technology detection (CMS, JS frameworks, CDN)
- WHOIS lookup
- robots.txt & sitemap.xml parsing
- SSL/TLS certificate analysis

### 🛰️ Scanning
- Port scanning (40+ common ports)
- Directory & file bruteforce
- HTTP methods testing
- Parameter discovery
- Backup files detection

### 🛡️ Vulnerability Detection

| Module | Detects | Severity |
|--------|---------|----------|
| **SQLi** | Error, Union, Boolean, Time-based | CRITICAL |
| **XSS** | Reflected, Stored, DOM-based | MEDIUM |
| **LFI** | Local File Inclusion, Traversal, PHP Wrappers | HIGH |
| **CMDi** | OS Command Injection (Linux/Windows) | CRITICAL |
| **SSRF** | Basic, Blind, Cloud Metadata | HIGH |
| **Upload** | Unrestricted Upload, Bypass Techniques | CRITICAL |

### 🎯 CMS-Specific Scanners
- **WordPress**: Version, users, plugins, themes, XML-RPC, CVEs
- **Joomla**: Version, components, config exposure, CVEs
- **Craft CMS**: Version, plugins, GraphQL, CVEs

### 🚀 Exploitation (Isolated Lab Only)
- SQLi data extraction
- LFI file reading
- Command injection execution
- XSS payload delivery
- SSRF internal access
- File upload web shells

### 📊 Reporting
- JSON report
- HTML report (dark theme)
- Log files
- Loot directory (exploitation results)

---

## 🛠️ Installation

### Termux (Android)

```bash
# Clone or download CarrotHunter
cd ~/storage/downloads
git clone https://github.com/your-repo/CarrotHunter.git
cd CarrotHunter

# Make scripts executable
chmod +x setup.sh carrot.sh metasploit.sh

# Run setup (installs all dependencies)
./setup.sh