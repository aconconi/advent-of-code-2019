# Advent of Code 2019
# Day 14: Space Stoichiometry

import math

with open('data/day14.dat') as file:
    input = file.read()

reacts = {}
for line in input.split('\n'):
    print(line)
    lhs, rhs = line.split(' => ')
    rq,rn = rhs.split(' ')
    ls = {}
    for lv in lhs.split(', '):
        lvq,lvn = lv.split(' ')
        ls[lvn] = int(lvq)
    reacts[rn] = (int(rq),ls)

def getore(fuel):
    have = {k:0 for k in reacts}
    need = {k:0 for k in reacts}
    have['ORE'] = need['ORE'] = 0
    need['FUEL'] = fuel
    
    needed_quant = fuel
    while needed_quant > 0:
        for c in need:
            if c == 'ORE' or need[c] == 0:
                continue
            add = need[c] - have[c]
            if add > 0:
                repeat = math.ceil(add / reacts[c][0])
                have[c] += reacts[c][0] * repeat
                for c2, need2 in reacts[c][1].items():
                    need[c2] += need2 * repeat
                    if c2 != 'ORE':
                        needed_quant += need2 * repeat
            have[c] -= need[c]
            needed_quant -= need[c]
            need[c] = 0

    for k,v in need.items():
        if k!='ORE' and v!=0:
            print('something wrong:', k, v)

    return need['ORE']


x = 3756878
a = getore(x)
print(f"getore({x}) = {a}")


if a >= 1000000000000:
    print("1000000000000 ok")


# Part 1 correct answer: 365768
# Part 2 correct answer: 3756878
