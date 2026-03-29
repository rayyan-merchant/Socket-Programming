import socket
import json

PORT = 5003

domains = {
    "mit.edu": ("127.0.0.1", 6004),
    "stanford.edu": ("127.0.0.1", 6005)
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print(".EDU TLD running")

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