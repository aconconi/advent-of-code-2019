# Advent of Code 2019
# Day 16: Flawed Frequency Transmission

from collections import deque
from itertools import chain, repeat, cycle

with open("data/day16.dat", "r") as data_file:
    data = data_file.readline().strip()

BASE_PATTERN = [0, 1, 0, -1]


def list_to_string(l):
    return "".join([str(x) for x in l])


def rotate_left(a):
    d = deque(a)
    d.rotate(-1)
    return list(d)


def expand(pattern, n):
    return list(chain.from_iterable(zip(*repeat(pattern, n))))


def apply(pattern, signal):
    return abs(sum(s * p for s, p in zip(signal, cycle(rotate_left(pattern))) if p)) % 10


def phase(signal):
    r = []
    for i in range(len(signal)):
        pattern = expand(BASE_PATTERN, i+1)
        # pattern = deque([p for p in [0, 1, 0, -1] for _ in range(i+1)])
        r.append(apply(pattern, signal))
    return r


def day16part1(signal_str, phases):
    signal = [int(c) for c in signal_str]
    for _ in range(phases):
        signal = phase(signal)
    return list_to_string(signal)[:8]

# def mul(k, n):
#     return BASE_PATTERN[ (k % (n*4)) // n ]


# We just need to add up all the digits from the current one to the end
# for the digits from the message offset to the end 100 times.
# This can be done a lot more efficiently going in reverse, since that
# way we only need to add the next digit instead of all the digits after
# the current one.
def day16part2(signal_str):
    offset = int(signal_str[:7])
    signal = [int(c) for c in signal_str] * 10000
    signal = signal[offset:]
    for _ in range(100):
        for i in range(-2, -len(signal)-1, -1):
            signal[i] = (signal[i] + signal[i+1]) % 10

    return list_to_string(signal[:8])


# Test cases for part 1
assert day16part1('12345678', 4) == '01029498'
assert day16part1('80871224585914546619083218645595', 100) == '24176176'
assert day16part1('19617804207202209144916044189917', 100) == '73745418'
assert day16part1('69317163492948606335995924319873', 100) == '52432133'

# Part 1
print("After 100 phases of FFT, what are the first eight digits in the final output list?")
print(day16part1(data, 100))  # Correct answer is 73127523


# Test cases for part 2
assert day16part2('03036732577212944063491565474664') == '84462026'
assert day16part2('02935109699940807407585447034323') == '78725270'
assert day16part2('03081770884921959731165446850517') == '53553731'

# Part 2
print("What is the eight-digit message embedded in the final output list?")
print(day16part2(data))  # Correct answer is 80284420
