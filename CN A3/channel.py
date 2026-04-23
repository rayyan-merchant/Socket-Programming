import random
import time
import threading
from queue import Queue

loss_prob = 0.2
corrupt_prob = 0.2
max_delay = 1


class Channel:
    def __init__(self):
        self.data_queue = Queue()
        self.ack_queue = Queue()

    def start(self, sender, receiver):
        threading.Thread(target=self.forward_data, args=(receiver,), daemon=True).start()
        threading.Thread(target=self.forward_ack, args=(sender,), daemon=True).start()

    def forward_data(self, receiver):
        while True:
            packet = self.data_queue.get()

            if random.random() < loss_prob:
                print(f"[CHANNEL] Packet {packet.seq_num} LOST")
                continue

            time.sleep(random.uniform(0, max_delay))

            if random.random() < corrupt_prob:
                print(f"[CHANNEL] Packet {packet.seq_num} CORRUPTED")
                import copy
                packet = copy.deepcopy(packet)
                packet.data = "CORRUPTED"

            receiver.input(packet)

    def forward_ack(self, sender):
        while True:
            ack = self.ack_queue.get()

            if random.random() < loss_prob:
                print(f"[CHANNEL] ACK {ack} LOST")
                continue

            time.sleep(random.uniform(0, max_delay))
            sender.input_ack(ack)