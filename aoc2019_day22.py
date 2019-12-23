# Advent of Code 2019
# Day 22: Slam Shuffle

from collections import deque


FACTORY = [i for i in range(10007)]
TEST = [i for i in range(10)]

def calc_deal_new(d):
    return [ d[len(d) - 1 - i] for i, _ in enumerate(d) ]

def calc_cut(d, n):
    return [ d[(i + n + len(d)) % len(d)] for i, _ in enumerate(d) ]
    
def calc_deal_increment(d, n):
    return [ d[abs((i * n) % -len(d))] for i, _ in enumerate(d) ]

def deal_new(d):
    return list(reversed(d))

def cut(d, n):
    new = deque(d)
    new.rotate(-n)
    return list(new)
    
def deal_increment(d, n):
    new = [-1] * len(d)
    for i in range(len(d)):
        new[(i * n) % len(d)] = d[i]
    return new

def test_cases():
    assert deal_new(TEST) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert cut(TEST, 3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert cut(TEST, -4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert deal_increment(TEST, 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]

    deck = TEST
    deck = deal_increment(deck, 7)
    deck = deal_new(deck)
    deck = deal_new(deck)
    assert deck == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

    deck = TEST
    deck = cut(deck, 6)
    deck = deal_increment(deck, 7)
    deck = deal_new(deck)
    assert deck == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

    deck = TEST
    deck = deal_new(deck)
    deck = cut(deck, -2)
    deck = deal_increment(deck, 7)
    deck = cut(deck, 8)
    deck = cut(deck, -4)
    deck = deal_increment(deck, 7)
    deck = cut(deck, 3)
    deck = deal_increment(deck, 9)
    deck = deal_increment(deck, 3)
    deck = cut(deck, -1)
    assert deck == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

def test_cases_calc():
    assert calc_deal_new(TEST) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert calc_cut(TEST, 3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert calc_cut(TEST, -4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert calc_deal_increment(TEST, 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]

    deck = TEST
    deck = calc_deal_increment(deck, 7)
    deck = calc_deal_new(deck)
    deck = calc_deal_new(deck)
    assert deck == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

    deck = TEST
    deck = calc_cut(deck, 6)
    deck = calc_deal_increment(deck, 7)
    deck = calc_deal_new(deck)
    assert deck == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

    deck = TEST
    deck = calc_deal_new(deck)
    deck = calc_cut(deck, -2)
    deck = calc_deal_increment(deck, 7)
    deck = calc_cut(deck, 8)
    deck = calc_cut(deck, -4)
    deck = calc_deal_increment(deck, 7)
    deck = calc_cut(deck, 3)
    deck = calc_deal_increment(deck, 9)
    deck = calc_deal_increment(deck, 3)
    deck = calc_cut(deck, -1)
    assert deck == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

test_cases()

def apply(deck, program):
    new = list(deck)
    for line in program:
        op = line.split()
        if op[0] == 'deal':
            if op[3] == 'stack':
                new = deal_new(new)
            else:
                new = deal_increment(new, int(op[3]))
        else:    
            assert op[0] == 'cut'      
            new = cut(new, int(op[1]))
    return new

# def calc_apply(deck, program):
#     new = list(deck)
#     for line in program:
#         op = line.split()
#         if op[0] == 'deal':
#             if op[3] == 'stack':
#                 new = calc_deal_new(new)
#             else:
#                 new = calc_deal_increment(new, int(op[3]))
#         else:    
#             assert op[0] == 'cut'      
#             new = calc_cut(new, int(op[1]))
#     return new

# Part 1
with open("data/day22.dat", "r") as data_file:
    program = data_file.read().splitlines()

deck = FACTORY
deck = apply(deck, program)

print("After shuffling your factory order deck of 10007 cards, what is the position of card 2019?")
print(deck.index(2019)) # 6417


# print("Calc part 1")
# deck = FACTORY
# deck = calc_apply(deck, program)
# print(deck.index(2019))


# Part 2
# Number of cards: 119315717514047
# Number of shuffles: 101741582076661