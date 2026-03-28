import socket
import threading

# Set default timeout
socket.setdefaulttimeout(1)

# Thread lock for clean output
lock = threading.Lock()

# Common ports (faster + realistic scanning)
common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]


# Resolve domain to IP
def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Could not resolve {target}")
        return None


# Scan a single port
def scan_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            with lock:
                print(f"[OPEN] Port {port} ({service})")

        s.close()
    except:
        pass


# Main function
def start_scan():
    target = input("Enter target (IP or domain): ")
    target_ip = resolve_target(target)

    if not target_ip:
        return

    print(f"\n[+] Target resolved: {target_ip}")
    print("[*] Scanning common ports...\n")

    threads = []

    for port in common_ports:
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n[✓] Scan completed!")


# Run program
if __name__ == "__main__":
    start_scan()
