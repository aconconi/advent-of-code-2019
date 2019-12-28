# Advent of Code 2019
# Day 14: Space Stoichiometry

from math import ceil

reactions = {}
with open("data/day14_test4.dat", "r") as data_file:
    for line in data_file.read().splitlines():
        lhs, rhs = line.split(' => ')
        rq, rn = rhs.split(' ')
        ls = {}
        for lv in lhs.split(', '):
            lvq, lvn = lv.split(' ')
            ls[lvn] = int(lvq)
        reactions[rn] = (int(rq), ls)

need = {k: 0 for k in reactions.keys()}
have = {k: 0 for k in reactions.keys()}

print("---")
print("List of reactions")
for r in reactions:
    print(f"{r} = {reactions[r]}")

def process(q, e):
    print(f"asked to produce {q} of {e}")
    # print("need_ore:", need_ore)
    if e in need_ore:
        need_ore[e] += q
    else:
        print("leftover:", have)
        for (sub_q, sub_e) in reactions[e][1]:
            process(ceil(q / reactions[e][0]) * sub_q, sub_e)


process(1, 'FUEL')


print("need_ore:", need_ore)
print("leftover:", leftover)


ore = 0
for e in need_ore.keys():
    ore += ceil(need_ore[e] / reactions[e][0]) * reactions[e][1][0][0]

print("total ORE", ore)
