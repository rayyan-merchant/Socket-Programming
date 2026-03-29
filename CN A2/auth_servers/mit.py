import socket
import json

PORT = 6004

records = {
"A": ["23.5.92.142"],
"NS": ["ns1.mit.edu","ns2.mit.edu"],
"MX": ["mail.mit.edu"]
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print("MIT Authoritative DNS running on port", PORT)

while True:
    data, addr = sock.recvfrom(1024)
    request = json.loads(data.decode())

    response = {
        "id": request["id"],
        "type": "RESPONSE",
        "domain": "mit.edu",
        "records": records
    }

    sock.sendto(json.dumps(response).encode(), addr)