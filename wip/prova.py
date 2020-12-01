# Advent of Code 2019
# Day 14: Space Stoichiometry

from math import ceil
from collections import namedtuple

testdata1 = ['10 ORE => 10 A', 
'1 ORE => 1 B',
'7 A, 1 B => 1 C',
'7 A, 1 C => 1 D',
'7 A, 1 D => 1 E',
'7 A, 1 E => 1 FUEL']

testdata2 = ['9 ORE => 2 A',
'8 ORE => 3 B',
'7 ORE => 5 C',
'3 A, 4 B => 1 AB',
'5 B, 7 C => 1 BC',
'4 C, 1 A => 1 CA',
'2 AB, 3 BC, 4 CA => 1 FUEL']


Reaction = namedtuple('Reaction', 'q e r')


reactions = {}
from_ore = []
for line in testdata1:
    line = ''.join([c for c in line if c not in '>']).split("=")

    rhs_quant = int(line[1].strip().split()[0]) # e.g. 1
    rhs_elem  = line[1].strip().split()[1] # e.g. FUEL

    lhs =  line[0].strip().split(',')  # e.g. ['2 AB', '3 BC', '4 CA']
    
    # print(f"{rhs_quant} of {rhs_elem} from {lhs}")
    
    reactions[rhs_elem] = (rhs_quant, [])
    for k in lhs:
        q = int(k.split()[0])
        e = k.split()[1]
        reactions[rhs_elem][1].extend([(q, e)])
        if e == 'ORE':
            from_ore.append(rhs_elem)


print("List of reactions")
for r in reactions:
    print(f"{r} = {reactions[r]}")
    
print("Ore elements: ",from_ore)
print("-------")


def expand(quant, elem):
    m = ceil(quant / reactions[elem][0])
    return [(m * q, e) for (q, e) in reactions[elem][1]]
    
# expr = reactions['FUEL'][1]
# quant = reactions['FUEL'][0]
# print("current", expr)
# while expr:
#     r = []
#     for (q, e) in expr:
#         if e not in from_ore:
#             r.extend( [(q * reactions[elem][0], e) for (q, e) in reactions[elem][1]] )
#     expr = r
#     print(expr, total)


# # print("expr", expr)
# # print(total)

print(expand(5, 'E'))


expr = reactions['FUEL'][1]
quant = reactions['FUEL'][0]
need = defaultdict(0)

def process(q, e):
    print(f"asked to produce {q} of {e}")
    # print("need_ore:", need_ore)
    if e in need_ore:
        need_ore[e] += q
    else:
        print("leftover:", have)
        for (sub_q, sub_e) in reactions[e][1]:
            process( ceil(q / reactions[e][0]) * sub_q, sub_e)