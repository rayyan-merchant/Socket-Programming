import socket
import json

PORT = 6003

records = {
"A": ["208.80.154.224"],
"NS": ["ns0.wikimedia.org","ns1.wikimedia.org","ns2.wikimedia.org"],
"MX": ["mx1.wikimedia.org","mx2.wikimedia.org"]
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print("Wikipedia Authoritative DNS running on port", PORT)

while True:
    data, addr = sock.recvfrom(1024)
    request = json.loads(data.decode())

    response = {
        "id": request["id"],
        "type": "RESPONSE",
        "domain": "wikipedia.org",
        "records": records
    }

    sock.sendto(json.dumps(response).encode(), addr)