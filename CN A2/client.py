import socket
import json
from cache import DNSCache
import random

ROOT_SERVER = ("127.0.0.1",5000)

cache = DNSCache()

msg_id = random.randint(0,65535)  #16 bits

def query(server, domain):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = {
        "id": random.randint(0,65535),
        "type": "QUERY",
        "domain": domain
    }

    sock.sendto(json.dumps(message).encode(), server)
    data,_ = sock.recvfrom(1024)
    response = json.loads(data.decode())

    return response


def resolve(domain):

    cached = cache.get(domain)

    if cached:
        print("\n[CACHE HIT]")
        return cached

    print("Contacting ROOT DNS")

    root_reply = query(ROOT_SERVER, domain)
    tld_server = tuple(root_reply["server"])

    print("Contacting TLD server")

    tld_reply = query(tld_server, domain)
    auth_server = tuple(tld_reply["server"])

    print("Contacting Authoritative server")

    final_reply = query(auth_server, domain)
    cache.add(domain, final_reply)

    return final_reply


while True:
    domain = input("\nEnter domain (or 'quit' to exit): ")
    if domain.lower() == 'quit':
        break

    result = resolve(domain)

    if "records" not in result:
        print("DNS lookup failed.")
        continue

    print(f"\n{domain}/{result['records']['A'][-1]}")
    print("\n-- DNS INFORMATION --")

    for record_type, values in result["records"].items():

        formatted = ", ".join(values)
        print(f"{record_type}: {formatted}")