class intcode():
    opcodes = {
        1: ('_add', 3),
        2: ('_mult', 3),
        3: ('_input', 1),
        4: ('_output', 1),
        5: ('_jump_if_true', 2),
        6: ('_jump_if_false', 2),
        7: ('_lt', 3),
        8: ('_eq', 3),
        9: ('_adj_rel_base', 1),
        99: ('_halt', 0)
    }
    
    def __init__(self, mem, debug=False, take_input=lambda: 1, give_output=(lambda x: print('output: {}'.format(x))), add_mem=0):
        self.initstate = mem + [0 for i in range(add_mem)]
        self.debug = debug
        self.take_input = take_input
        self.give_output = give_output
        self.reset()
    
    def reset(self):
        self.mem = self.initstate[:]
        self.ip = 0
        self.base = 0
        
    def __getstate__(self):
        print('saving')
        return [self.initstate, self.mem, self.ip, self.base]
    
    def __setstate__(self, state):
        self.initstate, self.mem, self.ip, self.base = state
        
    def lu(self, arg):
        mode, loc = arg
        if mode == 0:
            return self.mem[loc]
        elif mode == 2:
            return self.mem[self.base + loc]
        else:
            return loc
    
    def put(self, arg, val):
        if self.debug: print(arg, val)
        mode, loc = arg
        if mode == 0:
            self.mem[loc] = val
        elif mode == 2:
            self.mem[self.base + loc] = val
        else:
            raise ValueError("illegel mode for put {}".format(mode))
    
    def run(self):
        self.running = True
        while self.running:
            opcode = self.mem[self.ip]
            op, nargs = self.opcodes[opcode % 100]
            modes = opcode // 100
            modes = [int(d) for d in ('%03d' % modes)][::-1]
            args = list(zip(modes, self.mem[(self.ip+1):(self.ip+1+nargs)]))
            if self.debug:
                print(self.ip, ': ', op, args)
                print('before ', self.mem[self.ip:self.ip+8])
            ret = getattr(self, op)(*args)
            if ret:
                return ret
            if self.debug:
                print('after ', self.mem[self.ip:self.ip+8])
                print('-----------------------------------')
            self.ip += 1+nargs
        return ret
            
    
    def _add(self, a, b, c):
        self.put(c, self.lu(a) + self.lu(b))
        
    def _mult(self, a, b, c):
        self.put(c, self.lu(a) * self.lu(b))
    
    def _input(self, a):
        try:
            val = self.take_input()
        except IndexError:
            return 1
        self.put(a, val)        
    
    def _output(self, a):
        val = self.lu(a)
        self.give_output(val)
       
    def _jump_if_true(self, a, b):
        if self.lu(a):
            self.ip = self.lu(b) - 3
    
    def _jump_if_false(self, a, b):
        if not self.lu(a):
            self.ip = self.lu(b) - 3
    
    def _lt(self, a, b, c):
        if self.lu(a) < self.lu(b):
            self.put(c, 1)
        else:
            self.put(c, 0)
    
    def _eq(self, a, b, c):
        if self.lu(a) == self.lu(b):
            self.put(c, 1)
        else:
            self.put(c, 0)
          
    def _adj_rel_base(self, a):
        self.base += self.lu(a)
    
    def _halt(self):
        self.running = False
        return 99
    
    def give_output(self, a):
        print('output: {}'.format(a))