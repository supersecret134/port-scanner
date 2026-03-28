import socket
import threading

# Increase timeout (IMPORTANT FIX)
socket.setdefaulttimeout(2)

lock = threading.Lock()

# Use only key ports for reliability
common_ports = [22, 80, 443]


def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Could not resolve {target}")
        return None


def scan_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((target_ip, port))

        if result == 0:
            with lock:
                print(f"[OPEN] Port {port}")

        s.close()
    except Exception as e:
        pass


def start_scan():
    target = input("Enter target (IP or domain): ")
    target_ip = resolve_target(target)

    if not target_ip:
        return

    print(f"\n[+] Target: {target_ip}")
    print("[*] Scanning...\n")

    threads = []

    for port in common_ports:
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n[✓] Scan completed!")


if __name__ == "__main__":
    start_scan()
