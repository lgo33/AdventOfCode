reg = [0, 0, 1, 0]

reg[0] = 1
reg[1] = 1
reg[3] = 26

if reg[2] != 0:
    reg[2] = 7
    reg[3] += reg[2]
while reg[3] != 0:
    reg[2] = reg[0]
    reg[0] += reg[1]
    reg[1] = reg[2]
    reg[3] -= 1
reg[2] = 19
while reg[2] != 0:
    reg[3] = 11
    while reg[3] != 0:
        reg[0] += 1
        reg[3] -= 1
    reg[2] -= 1

print reg
