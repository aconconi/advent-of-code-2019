# Advent of Code 2019
# Day 22: Slam Shuffle

from collections import deque

FACTORY = [i for i in range(10007)]
TEST = [i for i in range(10)]

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


def inv(x, m):
    return pow(x, m - 2, m)


def apply_repeated(cards, program, shuffles):
    a = 1
    b = 0
    for line in program:
        op = line.split()
        if op[0] == 'deal':
            if op[3] == 'stack':
                # deal new
                a *= -1
                b += a
            else:
                # deal with increment
                a *= inv(int(op[3]), cards)
        else:    
            # cut     
            b += a * int(op[1])
        a %= cards  
        b %= cards
    
    increment = pow(a, shuffles, cards)
    offset = b * (1 - increment) * inv((1 - a) % cards, cards)
    offset %= cards
    return (2020 * increment + offset) % cards


with open("data/day22.dat", "r") as data_file:
    program = data_file.read().splitlines()

# Part 1
deck = apply(FACTORY, program)
print("After shuffling your factory order deck of 10007 cards, what is the position of card 2019?")
print(deck.index(2019)) # Correct answer is 6417

# Part 2
cards = 119315717514047
shuffles = 101741582076661
print("After shuffling your new, giant, factory order deck that many times, what number is on the card that ends up in position 2020?")
print(apply_repeated(cards, program, shuffles))
# Correct answer is 98461321956136