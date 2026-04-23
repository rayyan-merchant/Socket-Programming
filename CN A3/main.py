import threading
from channel import Channel

from rdt3 import RDT3_Sender, RDT3_Receiver
from gbn import GBN_Sender, GBN_Receiver
from sr import SR_Sender, SR_Receiver


def main():
    protocol = input("Enter protocol (rdt3, gbn, sr): ").strip().lower()
    while protocol not in ["rdt3", "gbn", "sr"]:
        protocol = input("Invalid protocol. Enter protocol (rdt3, gbn, sr): ").strip().lower()

    if protocol in ["gbn", "sr"]:
        window = int(input("Enter window size: ").strip() or 4)
    else:
        window = 4

    count = int(input("Enter number of packets: ").strip() or 5)
    size = int(input("Enter packet size: ").strip() or 10)

    import random
    import string
    data = [''.join(random.choices(string.ascii_letters, k=size)) for _ in range(count)]

    channel = Channel()

    if protocol == "rdt3":
        sender = RDT3_Sender(data, channel)
        receiver = RDT3_Receiver(channel)

    elif protocol == "gbn":
        sender = GBN_Sender(data, channel, window)
        receiver = GBN_Receiver(channel)

    elif protocol == "sr":
        sender = SR_Sender(data, channel, window)
        receiver = SR_Receiver(channel, window)

    channel.start(sender, receiver)

    sender_thread = threading.Thread(target=sender.start)
    sender_thread.start()

    sender_thread.join()


if __name__ == "__main__":
    main()