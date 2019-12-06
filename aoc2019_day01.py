# Advent of Code 2019
# Day 1: The Tyranny of the Rocket Equation

from math import floor

# read input file and load data into array of integers
# expecting one integer per line
with open("data/day01.dat", "r") as data_file:
        data = [line.strip() for line in data_file]

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

# Test cases
assert fuel(12) == 2
assert fuel(14) == 2
assert fuel(1969) == 654
assert fuel(100756) == 33583
assert secondary_fuel(14) == 2
assert secondary_fuel(1969) == 966
assert secondary_fuel(100756) == 50346

# Part 1
print("What is the sum of the fuel requirements for all of the modules on\
on your spacecraft?")
print(day01part1(data)) # Correct answer is 3394689

# Part 2
print("What is the sum of the fuel requirements for all of the modules on\
your spacecraft when also taking into account the mass of the added fuel? ")
print(day01part2(data)) # Correct answer is 5089160



