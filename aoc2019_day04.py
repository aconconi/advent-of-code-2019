# Advent of Code 2019
# Day 4: Secure Container

def get_digit(n, i):
    return n // 10**i % 10

# initially implemented this to generate list of digits from number
# however generating a string instead works just fine
def number_to_digits(n):
    return str(n)
    # return [ get_digit(n, i) for i in range(len(str(n))) ]

# At least two adjacent digits are the same
def same_adjacent_digits(n):
    digits = number_to_digits(n)  
    return True if [d for i, d in enumerate(digits[:-1]) if digits[i] == digits[i+1] ] else False

# At least two adjacent digits are the same
# alternative implementation 2, same speed
def same_adjacent_digits2(n):
    digits = number_to_digits(n)
    for i in range(len(digits) - 1):
        if digits[i] == digits[i+1]:
            return True
    return False

# At least two adjacent digits are the same
# alternative implementation 3, same speed
def same_adjacent_digits3(n):
    digits = number_to_digits(n)
    d1,d2,d3,d4,d5,d6 = digits[0], digits[1], digits[2], digits[3], digits[4], digits[5]
    return d1 == d2 or d2 == d3 or d3 == d4 or d4 == d5 or d5 == d6

# check that going from left to right the digits never decrease
def digits_never_decrease(n):
    digits = number_to_digits(n)
    for i in range(len(digits) - 1):
        if digits[i+1] < digits[i]:
            return False
    return True

# check that going from left to right the digits never decrease
# alternative implementation 2, functional syle, slower
def digits_never_decrease2(n):
    digits = number_to_digits(n)  
    return False if [d for i, d in enumerate(digits[:-1]) if digits[i+1] < digits[i] ] else True


# check that adjacent matching digits are not part of a larger group of matching digits
def includes_perfect_pair(n):
    digits = number_to_digits(n)
    d1,d2,d3,d4,d5,d6 = digits[0], digits[1], digits[2], digits[3], digits[4], digits[5]
    if d1 == d2 and d2 != d3:
        return True
    elif d1 != d2 and d2 == d3 and d3 != d4:
        return True
    elif d2 != d3 and d3 == d4 and d4 != d5:
        return True
    elif d3 != d4 and d4 == d5 and d5 != d6:
        return True
    elif d4 != d5 and d5 == d6:
        return True
    else:
        return False

# Some test cases for Part 1
assert same_adjacent_digits(111111)
assert digits_never_decrease(111111)
assert not digits_never_decrease(223450)
assert not same_adjacent_digits(123789)

def day04part1(low, high):
    return len( [x for x in range(low, high) if digits_never_decrease(x) and same_adjacent_digits(x)] )

# Some test cases for Part 2
assert includes_perfect_pair(177999)
assert includes_perfect_pair(112233) 
assert not includes_perfect_pair(123444)
assert includes_perfect_pair(111122)

def day04part2(low, high):
    return len( [x for x in range(low, high) if digits_never_decrease(x) and includes_perfect_pair(x)] )

# Part 1
print("How many different passwords within the range given in your puzzle input meet these criteria?")
print(day04part1(171309,643603)) # correct answer is 1625

# Part 2
print("How many different passwords within the range given in your puzzle input meet all of the criteria?")
print(day04part2(171309,643603)) # correct answer is 1111
