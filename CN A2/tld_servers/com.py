import socket
import json

PORT = 5001

domains = {
    "google.com": ("127.0.0.1", 6001),
    "amazon.com": ("127.0.0.1", 6002)
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print(".COM TLD running")

while True:
    data, addr = sock.recvfrom(1024)
    request = json.loads(data.decode())

    domain = request["domain"]

    if domain in domains:
        request = json.loads(data.decode())
        response = {
            "id": request["id"],
            "type": "RESPONSE",
            "server": domains[domain]
        }
        
    else:
        response = {"error": "Domain not found"}

    sock.sendto(json.dumps(response).encode(), addr)