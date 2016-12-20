#part 1
reg = [0, 0, 0, 0]

reg[0] = 1
reg[1] = 1
#part 2
reg[2] = 1

reg[3] = 26

def memo(fn):
    cache = {}
    def helper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return helper

@memo
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

if reg[2] != 0:
    reg[2] = 7
    reg[3] += reg[2]
reg[0] = fib(reg[3]+2)
reg[2] = 19
reg[3] = 11
reg[0] += reg[3] * reg[2]


print reg
