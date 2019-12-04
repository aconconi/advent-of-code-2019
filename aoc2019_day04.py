# Advent of Code 2019
# Day 4: Secure Container

# I would like to write a better implementation based on a generator
# that generates the solutions skipping directly to the next number
# with digits that never decrease.
# def counter(low, high):
#     current = low
#     while current <= high:
#         yield current
#         current += 1  
# for c in counter(3, 9):
#     print(c)

def get_digit(n, i):
    return n // 10**i % 10

# At least two adjacent digits are the same
def same_adjacent_digits(n):
    l = len(str(n))
    digits = [get_digit(n, i) for i in range(l)]
    for i in range(l-1):
        if digits[i] == digits[i+1]:
            return True
    return False
    
# Going from left to right, the digits never decrease
def digits_never_decrease(n):
    l = len(str(n))
    digits = [get_digit(n, i) for i in range(l)]
    for i in range(l-1): # this is going right to left
        if digits[i] < digits[i+1]:
            return False
    return True

def solve(low, high):
    return [x for x in range(low, high) if digits_never_decrease(x) and same_adjacent_digits(x)]


def day04part1(low, high):
    return len(solve(low, high))

assert same_adjacent_digits(111111)
assert digits_never_decrease(111111)
assert not digits_never_decrease(223450)
assert not same_adjacent_digits(123789)

print("How many different passwords within the range given in your puzzle input meet these criteria?")
print(day04part1(171309,643603)) # correct answer is 1625



# print(get_digit(987654321, 0))
# 1

# get_digit(987654321, 5)
# 6

# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

# 111111 meets these criteria (double 11, never decreases).
# 223450 does not meet these criteria (decreasing pair of digits 50).
# 123789 does not meet these criteria (no double).

# *** How many different passwords within the range given in your puzzle input meet these criteria? ***

# Your puzzle input is 171309-643603.

# --- Part Two ---

# An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

# Given this additional criterion, but still ignoring the range rule, the following are now true:

#     112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
#     123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
#     111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

# How many different passwords within the range given in your puzzle input meet all of the criteria?

# Your puzzle input is still 171309-643603.