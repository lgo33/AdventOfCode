import curses
from copy import deepcopy

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

elevator = 0
ntypes = 5
nfloors = 4
chips = []
generators = []
for i in range(nfloors):
    chips.append([])
    generators.append([])

chips[0] = [0]
chips[2] = [1, 2, 3, 4]
generators[0] = [0]
generators[1] = [1, 2, 3, 4]

# example:
#ntypes = 5
#chips[0] = [0, 1]
#generators[1] = [0]
#generators[2] = [1]

selected = []

history = []
turn = 0
cursor = 0
quit = False
msg = ''
saved = []

checksum = 0
for i in chips:
        checksum += sum(i)

def getElement(n):
    t = 'M'
    if n % 2:
        t = 'G'
    return (t, n/2)

def exists():
    t, n = getElement(cursor)
    if t == 'G':
        if n in generators[elevator]:
            return True
    elif t == 'M':
        if n in chips[elevator]:
            return True
    return False

def move_cursor():
    global cursor
    while exists() == False:
        cursor = (cursor + 1) % (ntypes*2)

def select():
    global selected
    if cursor in selected:
        selected.remove(cursor)
        return
    if len(selected) == 2:
        selected.pop(0)
    selected.append(cursor)

def move(x):
    global generators, chips, elevator, msg, turn
    if elevator + x < 0 or elevator + x >= nfloors:
        return
    for sel in selected:
        t, n = getElement(sel)
        if t == 'G':
            generators[elevator].remove(n)
            generators[elevator+x].append(n)
        elif t == 'M':
            chips[elevator].remove(n)
            chips[elevator+x].append(n)
    history.append((selected[:], x))
    #msg = repr(history)
    elevator += x
    turn += 1

def revert():
    global generators, chips, elevator, msg, turn , selected
    if len(history) == 0:
        return
    hselected, x = history.pop()
    #msg = repr(hselected)
    turn -= 1
    for sel in hselected:
        t, n = getElement(sel)
        if t == 'G':
            generators[elevator].remove(n)
            generators[elevator-x].append(n)
        elif t == 'M':
            chips[elevator].remove(n)
            chips[elevator-x].append(n)
    selected = hselected
    elevator -= x

def save():
    global saved, msg
    saved = (deepcopy(generators), deepcopy(chips), elevator, turn, selected[:], deepcopy(history))
    msg = 'saved'

def restore():
    global generators, chips, elevator, turn, selected, history, msg, saved
    if not len(saved):
        return
    tmp = (deepcopy(generators), deepcopy(chips), elevator, turn, selected[:], deepcopy(history))
    generators, chips, elevator, turn, selected[:], history[:] = saved
    msg = 'restored'
    saved = tmp
    #msg = 'restored #%d' % len(saved)

def handle_input(x):
    global cursor, elevator, quit
    if x == curses.KEY_LEFT:
        cursor -= 1
        cursor %= (ntypes*2)
        while exists() == False:
            cursor -= 1
            cursor %= (ntypes*2)
    elif x == curses.KEY_RIGHT:
        cursor += 1
    if x == curses.KEY_DOWN:
        if len(selected) == 0:
            return
        move(-1)
    elif x == curses.KEY_UP:
        if len(selected) == 0:
            return
        move(1)
    elif x == 127 or x == ord('w'):
        revert()
        msg = 'BACK'
    elif x == 32:
        select()
    elif x == ord('s'):
        save()
    elif x == ord('r'):
        restore()
        #print generators, chips, elevator, turn, selected, history
    elif x == ord('q'):
        quit = True

def draw():
    xoff = 2+8
    yoff = 2 + nfloors * 2
    spacing = 6
    screen.clear()
    screen.border(0)
    screen.addstr(1, 42, 'Turn : %d' % turn)
    for i in range(nfloors):
        screen.addstr(yoff-2*i, 2, 'Fl #%d' %i)
        for j in range(ntypes):
            if j in chips[i]:
                screen.addstr(yoff-2*i, xoff + j * spacing, 'M')
            if j in generators[i]:
                screen.addstr(yoff-2*i, xoff + j * spacing +1, 'G')
    screen.addstr(yoff - elevator * 2 + 1, (cursor/2 * spacing) + (cursor % 2) + xoff, '^')
    screen.addstr(12,2, '')
    for sel in selected:
        screen.addstr(yoff - elevator * 2 - 1, (sel/2 * spacing) + (sel % 2) + xoff, '_')
    #screen.addstr(13, 2, repr(selected) + " " + str(getElement(cursor)) + " " + str(exists()))
    screen.addstr(14, 2, msg)
    #screen.addstr(15, 2, repr(saved))
    screen.refresh()
    #screen.addstr()

def check():
    global msg
    cs = 0
    for i in chips:
        cs += sum(i)
    if cs != checksum:
        raise Exception('invalid chips')
    cs = 0
    for i in generators:
        cs += sum(i)
    if cs != checksum:
        raise Exception('invalid generators')

    for i in range(nfloors):
        if len(generators[i]):
            for chip in chips[i]:
                if chip not in generators[i]:
                    msg = 'chip %s fried!' % chip
                    return False
    return True

x = 0

while x != ord('4') and quit != True:
    while not check():
        revert()
    move_cursor()
    draw()
    x = screen.getch()
    handle_input(x)



curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()
