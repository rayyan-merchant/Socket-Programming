import socket
import json

PORT = 6002

records = {
"A": ["176.32.103.205","205.251.242.103"],
"NS": ["ns1.amazon.com","ns2.amazon.com","ns3.amazon.com"],
"MX": ["smtp1.amazon.com","smtp2.amazon.com"]
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print("Amazon Authoritative DNS running on port", PORT)

while True:
    data, addr = sock.recvfrom(1024)
    request = json.loads(data.decode())

    response = {
        "id": request["id"],
        "type": "RESPONSE",
        "domain": "amazon.com",
        "records": records
    }

    sock.sendto(json.dumps(response).encode(), addr)