import socket
import threading

def receive():
    while True:
        try:
            print(s.recv(1024).decode())
        except:
            break

s = socket.socket()
s.connect(('localhost', 9999))

name = input("Enter name: ")
s.send(name.encode())

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input()

    if msg.lower() == "exit":
        s.send("exit".encode())
        print("Disconnected")
        s.close()
        break

    s.send(f"{name}: {msg}".encode())
