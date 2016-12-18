from itertools import combinations, chain
from collections import defaultdict

nfloors = 4
ntypes = 5
def distance(node):
    pos, chips, gens = node
    sumpath = 0
    elements = sorted(chips+gens)
    for e in elements[2:]:
        sumpath += 2 * (nfloors - 1 - e)
    sumpath += (nfloors - 1 - elements[0])
    return sumpath

def checknode(node):
    pos, chips, gens = node
    for i in range(ntypes):
        if chips[i] == gens[i]:
            continue
        if chips[i] in gens:
            return False
    return True

def neighbors(node):
    pos, chips, gens = node
    cand = []
    nb = []
    for i in range(2*ntypes):
        _all = chips+gens
        if _all[i] == pos:
             cand.append(i)
    for c in chain(combinations(cand, 2), combinations(cand,1)):
        if pos > 0:
            tmp = list(_all[:])
            for i in c:
                tmp[i] -= 1
            pos_nb = (pos-1, tuple(tmp[:ntypes]), tuple(tmp[ntypes:]))
            if checknode(pos_nb):
                nb.append(pos_nb)
        if pos < nfloors - 1:
            tmp = list(_all[:])
            for i in c:
                tmp[i] += 1
            pos_nb = (pos+1, tuple(tmp[:ntypes]), tuple(tmp[ntypes:]))
            if checknode(pos_nb):
                nb.append(pos_nb)
    return nb

# part 1
ntypes = 5
startnode = (0, (0, 2, 2, 2, 2), (0, 1, 1, 1, 1))
# part 2
#ntypes = 7
#startnode = (0, (0, 2, 2, 2, 2, 0, 0), (0, 1, 1, 1, 1, 0, 0))

#ntypes = 2
#startnode = (0, (0, 0), (1,2))
inf = 9999

gScore = defaultdict(int)
fScore = defaultdict(int)

gScore[startnode] = 0
fScore[startnode] = distance(startnode)

openSet = [startnode]
done = []

while len(openSet):
    current = openSet[0]
    minfScore = fScore[current]
    for node in openSet:
        if fScore[node] < minfScore:
            current = node
            minfScore = fScore[node]

    openSet.remove(current)
    done.append(current)
    if distance(current) == 0:
        print gScore[current]
        break
    for nb in neighbors(current):
        if nb in done:
            continue
        done.append(nb)
        tmpgScore = gScore[current] + 1
        openSet.append(nb)
        if tmpgScore < gScore[nb] or gScore[nb] == 0:
            gScore[nb] = tmpgScore
            fScore[nb] = tmpgScore + distance(nb)
    print current, fScore[current], gScore[current]
