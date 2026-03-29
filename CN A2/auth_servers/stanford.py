import socket
import json

PORT = 6005

records = {
"A": ["171.67.215.200"],
"NS": ["ns1.stanford.edu","ns2.stanford.edu"],
"MX": ["mail.stanford.edu"]
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print("Stanford Authoritative DNS running on port", PORT)

while True:
    data, addr = sock.recvfrom(1024)
    request = json.loads(data.decode())

    response = {
        "id": request["id"],
        "type": "RESPONSE",
        "domain": "stanford.edu",
        "records": records
    }

    sock.sendto(json.dumps(response).encode(), addr)