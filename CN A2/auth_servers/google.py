import socket
import json

PORT = 6001

records = {
"A":["64.233.187.99","72.14.207.99","64.233.167.99"],
"NS":["ns1.google.com","ns2.google.com","ns3.google.com","ns4.google.com"],
"MX":["smtp1.google.com","smtp2.google.com","smtp3.google.com","smtp4.google.com"]
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print("Google Authoritative Server running")

while True:
    data, addr = sock.recvfrom(1024)
    request = json.loads(data.decode())

    response = {
        "id": request["id"],
        "type": "RESPONSE",
        "domain": "google.com",
        "records": records
    }

    sock.sendto(json.dumps(response).encode(), addr)