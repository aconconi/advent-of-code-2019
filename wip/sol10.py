import math

def countInLOS(station, asteroids, size):
    detected = set()
    for asteroid in asteroids:
        if asteroid != station:
                dx, dy = asteroid[0]-station[0], asteroid[1]-station[1]
                g = abs(math.gcd(dx, dy))
                reduced = (dx//g, dy//g)
                detected.add(reduced)
    return detected

with open("data/day10.dat") as f: content = f.readlines()
rawAsteroids = [s.strip() for s in content]
size = (len(rawAsteroids), len(rawAsteroids[0]))
asteroids = set()
for x in range(size[0]):
    for y in range(size[1]):
        if rawAsteroids[x][y] == "#":
                asteroids.add((x, y))

stationCounts = []
for station in asteroids:
    inLOS = countInLOS(station, asteroids, size)
    stationCounts.append((len(inLOS), station, inLOS))
    stationCounts.sort(reverse=True)
    amtInLOS, station, inLOS = stationCounts[0]
print("Part 1: {}".format(amtInLOS))

destroyed = [(math.atan2(dy, dx), (dx, dy)) for dx, dy in inLOS]
destroyed.sort(reverse=True)
dx, dy = destroyed[200-1][1]

x, y = station[0]+dx, station[1]+dy
while (x, y) not in asteroids:
    x, y = x+dx, y+dy

print("Part 2: {}".format(y*100 + x))