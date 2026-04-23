import time
from packet import Packet

TIMEOUT = 2


class RDT3_Sender:
    def __init__(self, data, channel):
        self.data = data
        self.channel = channel
        self.seq = 0
        self.state = "WAIT_CALL"

    def start(self):
        for msg in self.data:
            self.state = "WAIT_ACK"
            pkt = Packet(self.seq, msg)

            while True:
                print(f"[RDT3 SENDER] Sending {self.seq}")
                self.channel.data_queue.put(pkt)

                start = time.time()

                while self.state == "WAIT_ACK":
                    if time.time() - start > TIMEOUT:
                        print("[RDT3] Timeout -> Resend")
                        break
                    time.sleep(0.01)

                if self.state == "WAIT_CALL":
                    break

            self.seq = 1 - self.seq


    def input_ack(self, ack):
        if self.state == "WAIT_ACK" and ack == self.seq:
            print(f"[RDT3] ACK {ack}")
            self.state = "WAIT_CALL"


class RDT3_Receiver:
    def __init__(self, channel):
        self.channel = channel
        self.expected = 0

    def input(self, packet):
        if not packet.is_corrupted() and packet.seq_num == self.expected:
            print(f"[DELIVERED] {packet.data}")
            ack = packet.seq_num
            self.expected = 1 - self.expected
        else:
            ack = 1 - self.expected

        self.channel.ack_queue.put(ack)