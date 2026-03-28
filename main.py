import socket
import threading

# Lock for thread-safe printing
lock = threading.Lock()

# Function to scan a single port
def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        
        if result == 0:
            with lock:
                print(f"[OPEN] Port {port}")
        
        s.close()
    except:
        pass

# Main scanner function
def start_scan():
    target = input("Enter target (IP or domain): ")
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid target!")
        return

    print(f"\nScanning target: {target_ip}")
    print("Scanning ports...\n")

    threads = []

    for port in range(1, 1025):  # Scan ports 1–1024
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nScan completed!")

if __name__ == "__main__":
    start_scan()
