import time
from packet import Packet

TIMEOUT = 2  #timeout duration for retransmission


class RDT3_Sender:
    def __init__(self, data, channel):
        self.data = data
        self.channel = channel
        self.seq = 0  # alternating sequence number(0/1)
        self.state = "WAIT_CALL"  #FSM starting state

    def start(self):
        for msg in self.data:
            self.state = "WAIT_ACK"
            pkt = Packet(self.seq, msg)  

            while True:
                print(f"[RDT3 SENDER] Sending {self.seq}")
                self.channel.data_queue.put(pkt)  # send packet

                start = time.time()

                #wait for ack or timeout
                while self.state == "WAIT_ACK":
                    if time.time() - start > TIMEOUT:
                        print("[RDT3] Timeout -> Resend")
                        break
                    time.sleep(0.01)  # keeping it real

                if self.state == "WAIT_CALL":
                    break
            
            # alternate 0/1 numbers
            self.seq = 1 - self.seq


    def input_ack(self, ack):
        if self.state == "WAIT_ACK" and ack == self.seq:
            print(f"[RDT3] ACK {ack}")
            self.state = "WAIT_CALL"



class RDT3_Receiver:
    def __init__(self, channel):
        self.channel = channel
        self.expected = 0   # what seq expecting next

    def input(self, packet):
        if not packet.is_corrupted() and packet.seq_num == self.expected:
            # success condition
            print(f"[DELIVERED] {packet.data}")
            ack = packet.seq_num
            self.expected = 1 - self.expected
        else:
            # handle duplicates
            ack = 1 - self.expected
        # send ACK back to sender
        self.channel.ack_queue.put(ack)