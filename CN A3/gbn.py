import time
import threading
from packet import Packet

TIMEOUT = 2


class GBN_Sender:
    def __init__(self, data, channel, window_size=4):
        self.data = data
        self.channel = channel
        self.base = 0  #oldest unAcked pakcet
        self.next_seq = 0  #next packet to send
        self.window_size = window_size
        self.timer = None  # only timer that is for base
        self.packets = [Packet(i, d) for i, d in enumerate(data)]
        self.lock = threading.Lock()


    def start(self):
        while True:
            with self.lock:
                if self.base >= len(self.data):
                    break

                # send packets within window
                while self.next_seq < self.base + self.window_size and self.next_seq < len(self.data):
                    print(f"[GBN SENDER] Sending {self.next_seq}")
                    self.channel.data_queue.put(self.packets[self.next_seq])

                    if self.base == self.next_seq:
                        self.timer = time.time()

                    self.next_seq += 1

                # timeout -> resend entire window
                if self.timer and time.time() - self.timer > TIMEOUT:
                    print("[GBN] Timeout -> Resend Window")
                    self.timer = time.time()

                    for i in range(self.base, self.next_seq):
                        print(f"[GBN SENDER] Resend {i}")
                        self.channel.data_queue.put(self.packets[i])
            time.sleep(0.01)


    def input_ack(self, ack):
        with self.lock:
            print(f"[GBN] ACK {ack}")
            self.base = ack + 1



class GBN_Receiver:
    def __init__(self, channel):
        self.channel = channel
        self.expected = 0

    def input(self, packet):
        # accept only in order packet
        if not packet.is_corrupted() and packet.seq_num == self.expected:
            print(f"[DELIVERED] {packet.data}")
            self.expected += 1
        else:
            # discard out of order packet
            print(f"[GBN RECEIVER] Discard {packet.seq_num}")

        # send cumulative ack
        self.channel.ack_queue.put(self.expected - 1)