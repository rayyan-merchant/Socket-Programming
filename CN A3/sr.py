import time
import threading
from packet import Packet

TIMEOUT = 2


class SR_Sender:
    def __init__(self, data, channel, window_size=4):
        self.data = data
        self.channel = channel
        self.base = 0
        self.next_seq = 0
        self.window_size = window_size
        self.packets = [Packet(i, d) for i, d in enumerate(data)]
        self.acked = [False] * len(data)
        self.timers = {}
        self.lock = threading.Lock()

    def start(self):
        while True:
            with self.lock:
                if self.base >= len(self.data):
                    break

                while self.next_seq < self.base + self.window_size and self.next_seq < len(self.data):
                    print(f"[SR SENDER] Sending {self.next_seq}")
                    self.channel.data_queue.put(self.packets[self.next_seq])
                    self.timers[self.next_seq] = time.time()
                    self.next_seq += 1

                for i in range(self.base, self.next_seq):
                    if not self.acked[i] and time.time() - self.timers[i] > TIMEOUT:
                        print(f"[SR] Timeout → Resend {i}")
                        self.channel.data_queue.put(self.packets[i])
                        self.timers[i] = time.time()
            time.sleep(0.01)

    def input_ack(self, ack):
        with self.lock:
            print(f"[SR] ACK {ack}")
            self.acked[ack] = True

            while self.base < len(self.data) and self.acked[self.base]:
                self.base += 1


class SR_Receiver:
    def __init__(self, channel, window_size=4):
        self.channel = channel
        self.base = 0
        self.window_size = window_size
        self.buffer = {}

    def input(self, packet):
        if packet.is_corrupted():
            return

        if self.base <= packet.seq_num < self.base + self.window_size:
            print(f"[SR RECEIVER] Accept {packet.seq_num}")
            self.buffer[packet.seq_num] = packet
            self.channel.ack_queue.put(packet.seq_num)

            while self.base in self.buffer:
                print(f"[DELIVERED] {self.buffer[self.base].data}")
                del self.buffer[self.base]
                self.base += 1