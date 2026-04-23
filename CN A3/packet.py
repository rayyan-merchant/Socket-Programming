import hashlib

# packet(sequence number, data, checksum)
class Packet:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data
        self.checksum = self.compute_checksum()

    def compute_checksum(self):
        s = str(self.seq_num) + self.data
        return hashlib.md5(s.encode()).hexdigest()

    def is_corrupted(self):
        # Recompute checksum and compare with original
        # If mismatch -> packet is corrupted
        return self.checksum != self.compute_checksum()