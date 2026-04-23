import random
import time
import threading
from queue import Queue

# randomly assigning prob for simulating unreliable network
loss_prob = 0.2  # prob of pckt being lost
corrupt_prob = 0.2 # prob of pckt being corrupted
max_delay = 1  # delay


class Channel:
    def __init__(self):
        # queues for data and acks messages
        self.data_queue = Queue()
        self.ack_queue = Queue()

    def start(self, sender, receiver):
        # Start separate threads for data and ACK transmission
        threading.Thread(target=self.forward_data, args=(receiver,), daemon=True).start()
        threading.Thread(target=self.forward_ack, args=(sender,), daemon=True).start()

    def forward_data(self, receiver):
        while True:
            
            # get packet from sender
            packet = self.data_queue.get()

            # packet loss
            if random.random() < loss_prob:
                print(f"[CHANNEL] Packet {packet.seq_num} LOST")
                continue
            # delay
            time.sleep(random.uniform(0, max_delay))
            # corrupt pakets
            if random.random() < corrupt_prob:
                print(f"[CHANNEL] Packet {packet.seq_num} CORRUPTED")
                import copy
                packet = copy.deepcopy(packet)
                packet.data = "CORRUPTED"
            
            # Deliver packet to receiver if relaibly recieved
            receiver.input(packet)


    def forward_ack(self, sender):
        while True:
            # get ack from reciever
            ack = self.ack_queue.get()

            # there is a chance for ack loss
            if random.random() < loss_prob:
                print(f"[CHANNEL] ACK {ack} LOST")
                continue

            # add delay
            time.sleep(random.uniform(0, max_delay))
            # deliver ack to sender
            sender.input_ack(ack)