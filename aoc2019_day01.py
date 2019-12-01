# Advent of Code 2019
# Day 1: The Tyranny of the Rocket Equation

from math import floor

# read input file into lines
with open("data/day01.dat", "r") as data_file:
    lines = data_file.readlines()

# load data into array of integers
data = []
for line in lines:
    data.append(int(line))

# to find the fuel required for a module,
# take its mass, divide by three, round down, and subtract 2.
def fuel(m):
    return floor(m / 3) - 2

# Fuel itself requires fuel just like a module
def secondary_fuel(m):
    r = fuel(m)
    if r > 0:
        return r + secondary_fuel(r)
    else:
        return 0

def day01part1(data):
    return sum(fuel(m) for m in data)

def day01part2(data):
    return sum(secondary_fuel(m) for m in data)


print("What is the sum of the fuel requirements for all of the modules\
on your spacecraft?")
print(day01part1(data)) # Correct answer is 3394689

print("What is the sum of the fuel requirements for all of the modules on\
your spacecraft when also taking into account the mass of the added fuel? ")
print(day01part2(data)) # Correct answer is 5089160



