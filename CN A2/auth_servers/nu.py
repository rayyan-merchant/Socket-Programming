import socket
import json

PORT = 6006

records = {
"A":["111.68.103.26"],
"NS":["ns1.nu.edu.pk","ns2.nu.edu.pk"],
"MX":["mail.nu.edu.pk"]
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", PORT))

print("NU Authoritative Server running")

while True:
    data, addr = sock.recvfrom(1024)
    request = json.loads(data.decode())

    response = {
        "id": request["id"],
        "type": "RESPONSE",
        "domain": "nu.edu.pk",
        "records": records
    }

    sock.sendto(json.dumps(response).encode(), addr)