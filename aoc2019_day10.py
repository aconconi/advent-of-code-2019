# Advent of Code 2019
# Day 10: Monitoring Station

from collections import namedtuple
import math
from itertools import chain

Point = namedtuple('Point', 'x y')

asteroids = set()

# read input file and generate asteroids
with open("data/day10.dat", "r") as data_file:
    for y,line in enumerate(data_file):
        for x,c in enumerate(line.strip()):
            if c == '#' or c == 'X':
                asteroids.add(Point(x,y))

def normalize(x, y):
    return (x // math.gcd(x,y), y // math.gcd(x,y))

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


# this is not needed, stashed for future use :-)
# def between_with_end(p1, p2):
#     return chain(between(p1,p2), [p2])
#
# def sweep(p, width, height):
#     iter1 = ( Point(x, 0) for x in range(p.x, width) )
#     iter2 = ( Point(width-1, y) for y in range(1, height) )
#     iter3 = ( Point(x, height-1) for x in reversed(range(0, width-1)) )
#     iter4 = ( Point(0, y) for y in reversed(range(0, height-1)) )
#     iter5 = ( Point(x,0) for x in range(1,p.x) )
#     return chain(iter1, iter2, iter3, iter4, iter5)
    
    
def angle_between(p1, p2):
    # I learnt how to get this right thanks to this snippet in Haskell by sigwinch28
    # def angleBetween (x1,y1) (x2,y2) = if angle < 0 then (2*pi) + angle else angle
    #   where (dx,dy) = (x2-x1, y1-y2) -- note that y is inverted (i.e. going *down*)
    #         angle = atan2 (fromIntegral dx) (fromIntegral dy)
    dx = p2.x - p1.x
    dy = p1.y - p2.y # note that y is inverted (i.e. going *down*)
    angle = math.atan2(dx, dy)
    return (2 * math.pi) + angle if angle < 0 else angle

def day10part2():
    station = find_station()
    visible = sorted(visibile_from(station), key=lambda z: angle_between(station, z))
    sol = visible[200-1]
    return sol.x * 100 + sol.y

print("How many other asteroids can be detected from that location?")
print(day10part1())  # Correct answer is 280

print("What is x*100+y for the 200th asteroid to be vaporized?") 
print(day10part2())  # Correct answer is 706