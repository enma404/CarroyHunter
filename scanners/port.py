# scanners/port.py
# CarrotHunter - Port Scanner
# Fast, multi-threaded port scanning with service detection

import socket
import threading
import time
import concurrent.futures
from queue import Queue
from colorama import Fore, Style

import warnings
warnings.filterwarnings("ignore")


class PortScanner:
    """
    Port Scanner Module
    - Multi-threaded TCP port scanning
    - Common ports + custom ranges
    - Service identification
    - Banner grabbing
    - UDP scanning (optional)
    - Fast mode (top 100 ports) & Full mode (1-65535)
    """

    # =============================================
    # TOP 100 PORTS (Most common)
    # =============================================

    TOP_100_PORTS = [
        21, 22, 23, 25, 53, 80, 81, 110, 111, 113,
        135, 139, 143, 161, 162, 179, 199, 389, 443, 445,
        465, 514, 515, 548, 554, 587, 631, 636, 646, 873,
        990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1080, 1110,
        1194, 1433, 1434, 1521, 1701, 1720, 1723, 1755, 1812, 1900,
        2000, 2001, 2049, 2082, 2083, 2086, 2087, 2095, 2096, 2222,
        2323, 2375, 2376, 3000, 3128, 3260, 3306, 3389, 3690, 4000,
        4333, 4443, 4444, 4505, 4506, 5000, 5001, 5005, 5432, 5433,
        5672, 5900, 5901, 5984, 5985, 5986, 6000, 6379, 6443, 6666,
        7000, 7070, 8000, 8001, 8008, 8080, 8081, 8086, 8088, 8090,
        8443, 8888, 9000, 9090, 9200, 9300, 9443, 9999, 10000, 11211,
        15672, 27017, 27018, 50000, 50070, 50075, 50090,
    ]

    # =============================================
    # SERVICE IDENTIFICATION
    # =============================================

    SERVICES = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        69: "TFTP",
        80: "HTTP",
        81: "HTTP-Alt",
        110: "POP3",
        111: "RPCbind",
        113: "Ident",
        123: "NTP",
        135: "MSRPC",
        137: "NetBIOS-NS",
        138: "NetBIOS-DGM",
        139: "NetBIOS-SSN",
        143: "IMAP",
        161: "SNMP",
        162: "SNMPTrap",
        179: "BGP",
        199: "SNMP-SSL",
        389: "LDAP",
        443: "HTTPS",
        445: "SMB",
        465: "SMTPS",
        514: "Syslog",
        515: "LPD",
        548: "AFP",
        554: "RTSP",
        587: "SMTP-Submit",
        631: "IPP",
        636: "LDAPS",
        646: "LDP",
        873: "Rsync",
        990: "FTP-SSL",
        993: "IMAPS",
        995: "POP3S",
        1025: "NFS",
        1026: "NFS-Alt",
        1027: "NFS-Alt",
        1028: "NFS-Alt",
        1029: "NFS-Alt",
        1080: "SOCKS",
        1110: "NFS-Alt",
        1194: "OpenVPN",
        1433: "MSSQL",
        1434: "MSSQL-Browser",
        1521: "Oracle",
        1701: "L2TP",
        1720: "H.323",
        1723: "PPTP",
        1755: "MMS",
        1812: "RADIUS",
        1900: "SSDP",
        2000: "Cisco-SCCP",
        2001: "Cisco-SCCP",
        2049: "NFS",
        2082: "cPanel",
        2083: "cPanel-SSL",
        2086: "WHM",
        2087: "WHM-SSL",
        2095: "Webmail",
        2096: "Webmail-SSL",
        2222: "SSH-Alt",
        2323: "Telnet-Alt",
        2375: "Docker",
        2376: "Docker-SSL",
        3000: "Node.js",
        3128: "Squid-Proxy",
        3260: "iSCSI",
        3306: "MySQL",
        3389: "RDP",
        3690: "SVN",
        4000: "HTTP-Alt",
        4333: "mSQL",
        4443: "HTTPS-Alt",
        4444: "Metasploit",
        4505: "SaltStack",
        4506: "SaltStack",
        5000: "UPnP",
        5001: "HTTP-Alt",
        5005: "Java-RMI",
        5432: "PostgreSQL",
        5433: "PostgreSQL-Alt",
        5672: "AMQP",
        5900: "VNC",
        5901: "VNC-Alt",
        5984: "CouchDB",
        5985: "WinRM-HTTP",
        5986: "WinRM-HTTPS",
        6000: "X11",
        6379: "Redis",
        6443: "Kubernetes-API",
        6666: "IRC-Alt",
        7000: "Cassandra",
        7070: "HTTP-Alt",
        8000: "HTTP-Alt",
        8001: "HTTP-Alt",
        8008: "HTTP-Alt",
        8080: "HTTP-Proxy",
        8081: "HTTP-Alt",
        8086: "InfluxDB",
        8088: "HTTP-Alt",
        8090: "HTTP-Alt",
        8443: "HTTPS-Alt",
        8888: "HTTP-Alt",
        9000: "HTTP-Alt",
        9090: "HTTP-Alt",
        9200: "Elasticsearch",
        9300: "Elasticsearch",
        9443: "HTTPS-Alt",
        9999: "HTTP-Alt",
        10000: "Webmin",
        11211: "Memcached",
        15672: "RabbitMQ",
        27017: "MongoDB",
        27018: "MongoDB-Alt",
        50000: "SAP",
        50070: "Hadoop",
        50075: "Hadoop",
        50090: "Hadoop",
    }

    # =============================================
    # INITIALIZATION
    # =============================================

    def __init__(self, target, timeout=2, threads=100, ports=None):
        """
        Initialize port scanner

        Args:
            target: Target URL or hostname
            timeout: Connection timeout per port
            threads: Number of concurrent threads
            ports: Custom list of ports (or None for default)
        """
        # Parse target
        if '://' in target:
            from urllib.parse import urlparse
            parsed = urlparse(target)
            self.host = parsed.hostname
        else:
            self.host = target.split(':')[0].split('/')[0]

        self.target = target
        self.timeout = timeout
        self.threads = threads
        self.ports = ports or self.TOP_100_PORTS

        self.results = {
            'host': self.host,
            'ip': '',
            'open_ports': [],
            'closed_ports': 0,
            'filtered_ports': 0,
            'scan_time': 0,
            'total_scanned': 0,
        }

        self._lock = threading.Lock()
        self._start_time = None

    # =============================================
    # MAIN RUN
    # =============================================

    def run(self):
        """Execute port scan"""
        print(f"{Fore.CYAN}[*] Port Scanner started")
        print(f"{Fore.CYAN}[*] Target: {self.host}")
        print(f"{Fore.CYAN}[*] Ports to scan: {len(self.ports)}")
        print(f"{Fore.CYAN}[*] Threads: {self.threads}")
        print()

        # Resolve IP
        try:
            self.results['ip'] = socket.gethostbyname(self.host)
            print(f"{Fore.GREEN}[+] Resolved: {self.results['ip']}")
        except socket.gaierror:
            print(f"{Fore.RED}[-] Failed to resolve {self.host}")
            return self.results

        # Start scan
        self._start_time = time.time()

        print(f"{Fore.YELLOW}[*] Scanning...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._scan_port, port): port for port in self.ports}

            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                try:
                    result = future.result()
                    self.results['total_scanned'] += 1
                except Exception:
                    pass

        self.results['scan_time'] = time.time() - self._start_time

        # Print results
        self._print_results()

        return self.results

    # =============================================
    # SCAN SINGLE PORT
    # =============================================

    def _scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)

            result = sock.connect_ex((self.host, port))

            if result == 0:
                # Port is open
                service = self.SERVICES.get(port, 'Unknown')
                banner = self._grab_banner(sock, port)

                with self._lock:
                    self.results['open_ports'].append({
                        'port': port,
                        'service': service,
                        'banner': banner,
                        'state': 'open'
                    })

            sock.close()
        except socket.timeout:
            with self._lock:
                self.results['filtered_ports'] += 1
        except:
            with self._lock:
                self.results['closed_ports'] += 1

    # =============================================
    # BANNER GRABBING
    # =============================================

    def _grab_banner(self, sock, port, max_bytes=1024):
        """Grab service banner"""
        try:
            sock.settimeout(1.5)

            # Some services need us to send data first
            if port in [80, 8080, 8000, 8443, 443, 8081, 8888]:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            elif port == 21:
                pass  # FTP sends banner automatically
            elif port == 22:
                pass  # SSH sends banner automatically
            elif port == 25:
                pass  # SMTP sends banner automatically
            elif port == 110:
                pass  # POP3 sends banner automatically
            elif port == 143:
                pass  # IMAP sends banner automatically
            elif port == 3306:
                pass  # MySQL sends banner automatically
            elif port == 6379:
                sock.send(b"PING\r\n")

            banner = sock.recv(max_bytes)
            banner_str = banner.decode('utf-8', errors='ignore').strip()
            banner_str = banner_str.split('\n')[0][:100]

            return banner_str if banner_str else None
        except:
            return None

    # =============================================
    # PRINT RESULTS
    # =============================================

    def _print_results(self):
        """Print scan results"""
        open_ports = self.results['open_ports']

        if not open_ports:
            print(f"\n{Fore.YELLOW}[!] No open ports found")
            return

        print(f"\n{Fore.GREEN}[+] Found {len(open_ports)} open ports:")
        print()

        # Sort by port number
        open_ports.sort(key=lambda x: x['port'])

        for port_info in open_ports:
            port = port_info['port']
            service = port_info['service']
            banner = port_info['banner']

            # Color based on risk
            if port in [22, 23, 3389, 5900]:
                color = Fore.YELLOW
            elif port in [21, 445, 1433, 3306, 5432, 6379, 27017, 11211]:
                color = Fore.RED
            else:
                color = Fore.GREEN

            print(f"{color}    [+] {port:<6} {service:<18}{Style.RESET_ALL}", end="")

            if banner:
                print(f" {Fore.CYAN}{banner[:50]}{Style.RESET_ALL}")
            else:
                print()

    # =============================================
    # QUICK SCAN
    # =============================================

    def quick_scan(self):
        """Quick scan of top 20 ports"""
        self.ports = self.TOP_100_PORTS[:20]
        return self.run()

    def full_scan(self):
        """Full scan of all ports (1-65535)"""
        self.ports = list(range(1, 65536))
        return self.run()

    def scan_range(self, start, end):
        """Scan a range of ports"""
        self.ports = list(range(start, end + 1))
        return self.run()

    # =============================================
    # UDP SCAN
    # =============================================

    def scan_udp(self, ports=None):
        """Scan UDP ports (limited)"""
        udp_ports = ports or [53, 67, 68, 69, 123, 135, 137, 138, 139, 161, 162, 500, 514, 520, 1900, 4500]

        print(f"{Fore.CYAN}[*] UDP scanning {len(udp_ports)} ports...")

        for port in udp_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(self.timeout)

                # Send dummy data
                sock.sendto(b'\x00' * 10, (self.host, port))

                try:
                    data, _ = sock.recvfrom(1024)
                    service = self.SERVICES.get(port, 'Unknown')

                    self.results['open_ports'].append({
                        'port': port,
                        'service': f"UDP/{service}",
                        'banner': data[:50].decode('utf-8', errors='ignore'),
                        'state': 'open',
                        'protocol': 'udp'
                    })
                    print(f"{Fore.GREEN}    [+] UDP/{port} {service}")
                except socket.timeout:
                    pass

                sock.close()
            except:
                pass

        return self.results

    # =============================================
    # SUMMARY
    # =============================================

    def summary(self):
        """Print summary"""
        r = self.results

        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}  PORT SCAN SUMMARY")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Host:     {r['host']}")
        print(f"{Fore.GREEN}[+] IP:       {r['ip']}")
        print(f"{Fore.GREEN}[+] Open:     {len(r['open_ports'])}")
        print(f"{Fore.GREEN}[+] Closed:   {r['closed_ports']}")
        print(f"{Fore.GREEN}[+] Filtered: {r['filtered_ports']}")
        print(f"{Fore.GREEN}[+] Time:     {r['scan_time']:.2f}s")

        if r['open_ports']:
            print(f"\n{Fore.YELLOW}[!] Open Ports:")
            for p in r['open_ports']:
                print(f"{Fore.YELLOW}    - {p['port']}/{p.get('protocol', 'tcp')} ({p['service']})")

        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


# =============================================
# EXPORTS
# =============================================

__all__ = ["PortScanner"]