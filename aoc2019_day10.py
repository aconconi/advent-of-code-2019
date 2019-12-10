# Advent of Code 2019
# Day 10: Monitoring Station

from collections import namedtuple
from math import gcd
from itertools import chain

Point = namedtuple('Point', 'x y')

size =0
asteroids = set()
# read input file and generate asteroids
with open("data/day10_test6.dat", "r") as data_file:
    for y,line in enumerate(data_file):
        size = len(line)
        for x,c in enumerate(line.strip()):
            if c == '#' or c == 'X':
                asteroids.add(Point(x,y))

def normalize(x, y):
    return (x // gcd(x,y), y // gcd(x,y))

def between (p1, p2):
    if p1 == p2:
        return []

    x1,y1,x2,y2 = p1.x, p1.y, p2.x, p2.y
    dx = x2 - x1
    dy = y2 - y1
    (sx, sy) = normalize(dx,dy) 
    
    if sx and sy:
        return ( Point(x,y) for x,y in zip(range(x1+sx, x2, sx), range(y1+sy, y2, sy)) )
    elif sx:
        return ( Point(x,y1) for x in range(x1+sx, x2, sx) )
    else:
        return ( Point(x1,y) for y in range(y1+sy, y2, sy) )

def between_with_end(p1, p2):
    if p1 == p2:
        return []

    x1,y1,x2,y2 = p1.x, p1.y, p2.x, p2.y
    dx = x2 - x1
    dy = y2 - y1
    (sx, sy) = normalize(dx,dy) 
    
    if sx and sy:
        return ( Point(x,y) for x,y in zip(range(x1+sx, x2, sx), range(y1+sy, y2, sy)) )
    elif sx:
        return ( Point(x,y1) for x in range(x1, x2+sx, sx) )
    else:
        return ( Point(x1,y) for y in range(y1, y2+sx, sy) )

    
def see_each_other(p1, p2):
    if p1 == p2 or {b for b in between(p1, p2)} & asteroids:
        return False
    else:
        return True

def visibile_from(p):
    return [ a for a in asteroids if see_each_other(p, a) ]

def can_see_how_many(p):
    return len(visibile_from(p))

def find_station():
    return max(asteroids, key=lambda a: can_see_how_many(a))

def day10part1():
    return max(can_see_how_many(a) for a in asteroids)

# print(max(asteroids, key=lambda x: can_see_how_many(x)))
# print(asteroids)
# p1 = Point(1,0)
# p2 = Point(3,4)
# print(p1)
# print("between:", between(p1, p2))
# print("see_each_other:", see_each_other(p1,p2))
# print("visible_from:",visibile_from(p1))
# print("can_see_how_many:",can_see_how_many(p1))
# print([can_see_how_many(p) for p in asteroids])

print("How many other asteroids can be detected from that location?")
print(day10part1())  # Correct answer is 280

# print("Part 2")
# print("asteroids:", asteroids)
# print([b for b in between(find_station(),Point(8,0))])


def sweep(p, width, height):
    iter1 = ( Point(x, 0) for x in range(p.x, width) )
    iter2 = ( Point(width-1, y) for y in range(1, height) )
    iter3 = ( Point(x, height-1) for x in reversed(range(0, width-1)) )
    iter4 = ( Point(0, y) for y in reversed(range(0, height-1)) )
    iter5 = ( Point(x,0) for x in range(1,p.x) )
    return chain(iter1, iter2, iter3, iter4, iter5)
    
    

width =  max(p.x for p in asteroids) 
height = max(p.y for p in asteroids) 
print("width", width, "height", height)

# print([x for x in sweep(find_station(), width, height)])
station = find_station()
print(station)
print([x for x in between_with_end(station, Point(8,0))])
exit(0)
i = 0
for e in sweep(station, width, height):
    print("edge", e)
    for a in between_with_end(station, e):
        if a in asteroids:
            i += 1
            print("     ast", a)