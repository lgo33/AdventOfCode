class VM():    
    def __init__(self, data, debug=False):
        self.data = data
        self.last = len(self.data)
        self.loc = 0
        self.acc = 0
        self.seen = set([])
        self.debug = debug
        self.halting = None
        
        
        self.ops = {
            'nop': self._nop,
            'acc': self._acc,
            'jmp': self._jmp
        }
    
    def run(self):
        while True:
            if self.loc in self.seen:
                self.halting = False
                break
            if self.loc == self.last:
                self.halting = True
                break
            self.seen.add(self.loc)
            op, param = self.data[self.loc]
            if self.debug:
                print('exe #{}: {} {}'.format(self.loc, op, param))
            self.execute(op, param)
    
    def execute(self, instruction, param):
        self.ops[instruction](param)
        if instruction not in ('jmp'):
            self.loc += 1
    
    def _nop(self, param):
        pass
    
    def _jmp(self, param):
        self.loc += param
    
    def _acc(self, param):
        self.acc += param