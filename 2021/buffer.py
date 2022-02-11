class Buffer():
    def __init__(self, data):
        self.data = data
        self.buffer = self.generator()
        self.cnt = 0
        self.tot_version = 0

    def generator(self):
        for char in self.data:
            bits = bin(int(char, 16))[2:]
            for bit in bits.zfill(4):
                yield int(bit)
    
    def read(self, n=1, convert=False):
        res = []
        for i in range(n):
            res.append(next(self.buffer))
            self.cnt += 1
        if convert:
            return self.convert(res)
        return res
    
    @staticmethod
    def convert(bitarray):
        return int("".join(map(str, bitarray)), 2)
    
    def read_literal(self):
        res = []
        while True:
            pkg = self.read(5)
            res.extend(pkg[1:])
            if pkg[0] == 0:
                break
        return self.convert(res)
    
    def read_operator(self, op):
        ltid = self.read().pop()
        sub_pkts = []
        if ltid == 0:
            total_length = self.read(15, convert=True)
            loc = self.cnt
            while self.cnt < loc + total_length:
                sub_pkts.append(self.read_packet())
        else:
            num_packets = self.read(11, convert=True)
            for i in range(num_packets):
                sub_pkts.append(self.read_packet())
                
        if op == 0:
            return sum(sub_pkts)
        elif op == 1:
            res = 1
            for sp in sub_pkts:
                res *= sp
            return res
        elif op == 2:
            return min(sub_pkts)
        elif op == 3:
            return max(sub_pkts)
        elif op == 5:
            if sub_pkts[0] > sub_pkts[1]:
                return 1
            else:
                return 0
        elif op == 6:
            if sub_pkts[0] < sub_pkts[1]:
                return 1
            else:
                return 0
        elif op == 7:
            if sub_pkts[0] == sub_pkts[1]:
                return 1
            else:
                return 0
        
    
    def read_packet(self):
        version = self.read(3, convert=True)
        self.tot_version += version
        tid = self.read(3, convert=True)
        if tid == 4:
            return self.read_literal()
        else:
            return self.read_operator(tid)
        return version, tid
    
    def parse(self):
        try:
            while True:
                _ = self.read_packet()
        except StopIteration:
            return _
            