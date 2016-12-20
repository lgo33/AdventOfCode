
# coding: utf-8

# In[1]:

input = []
with open("data/input_12.txt", "r") as f:
    for line in f:
        input.append(line.strip())


# In[2]:

input


# In[3]:
# part 1
reg = [0, 0, 0, 0]
# part 2
reg = [0, 0, 1, 0]
loc = 0

def getReg(x):
    return ord(x) - ord('a')

def getValue(x):
    try:
        return int(x)
    except ValueError:
        return reg[getReg(x)]

def abCopy(x, y):
    global reg
    reg[getReg(y)] = getValue(x)

def abInc(x):
    global reg
    reg[getReg(x)] += 1

def abDec(x):
    global reg
    reg[getReg(x)] -= 1

def abJnz(x, y):
    global loc
    if getValue(x) != 0:
        loc += getValue(y)
        loc -= 1

def parse(line):
    cmd = line.split(" ")
    if cmd[0] == 'cpy':
        abCopy(cmd[1], cmd[2])
    elif cmd[0] == 'inc':
        abInc(cmd[1])
    elif cmd[0] == 'dec':
        abDec(cmd[1])
    elif cmd[0] == 'jnz':
        abJnz(cmd[1], cmd[2])



# In[4]:

loc = 0
while loc < len(input):
    print loc, reg, input[loc]
    parse(input[loc])
    loc += 1

print reg


# In[ ]:
