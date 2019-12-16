# Advent of Code 2019
# Day 16: Flawed Frequency Transmission


from collections import deque
from itertools import chain, repeat, cycle
from math import gcd


BASE_PATTERN = [0, 1, 0, -1]
      
def mcm(a,b):
    return a * b // gcd(a,b)

def list_to_string(l):
    s = "" 
    for x in l: 
        s += str(x)  
    return s 

def rotate_left(a):
    d = deque(a)
    d.rotate(-1)
    return list(d)

def expand(pattern, n, max_len):
    new = list(chain.from_iterable(zip(*repeat(pattern, n))))
    return new[:max_len+1]

def apply(pattern, signal):
    # print(f"Pattern: {pattern}, signal: {signal}")
    return abs(sum( s * p for s, p in zip(signal, cycle(rotate_left(pattern))))) % 10


def phase(signal):
    r = []
    for i in range(len(signal)):
        pattern = expand(BASE_PATTERN, i+1, len(signal))
        # pattern = deque([p for p in [0, 1, 0, -1] for _ in range(i+1)])
        r.append(apply(pattern, signal))
    return r

def iterate_phases(signal, n):
    s = signal
    for i in range(n):
        # print(f"Phase {i}...")
        s = phase(s)
    return s

def day16part1(signal_str, phases):
    signal = [int(c) for c in signal_str]
    return list_to_string(iterate_phases(signal, phases))[:8]

    # new = []
    # print(f"pattern={pattern} len={len(pattern)} n={n}")
    # for i, x in enumerate(pattern):
    #     new.extend([z for z in repeat(x, n)])
    #     print(f"step={i}  digit={x}  new={new}")
    #     if len(new) > max_len:
    #         new = new[:max_len]
    #         break

def mul(k, n):
    return BASE_PATTERN[ (k % (n*4)) // n ]

def day16part2(signal_str):
    offset = int(signal_str[:7])
    # print(f"Offset: {offset}")
    signal = [int(c) for c in signal_str] * 10000
    signal = signal[offset:]
    for f in range(100):
        # print(f"Starting phase {f+1} with signal len {len(signal)}")
        for i in range(-2, -len(signal)-1, -1):
            signal[i] = (signal[i] + signal[i+1]) % 10

    return "".join([str(x) for x in signal[:8]])

    


# Test cases for part 1
assert day16part1('12345678', 4) == '01029498'
assert day16part1('80871224585914546619083218645595', 100) == '24176176'
assert day16part1('19617804207202209144916044189917', 100) == '73745418'
assert day16part1('69317163492948606335995924319873', 100) == '52432133'

with open("data/day16.dat", "r") as data_file:
        data = data_file.readline().strip()

# Part 1
print("After 100 phases of FFT, what are the first eight digits in the final output list?")
print(day16part1(data, 100)) # Correct answer is 73127523


# Test cases for part 2
assert day16part2('03036732577212944063491565474664') == '84462026'
assert day16part2('02935109699940807407585447034323') == '78725270'
assert day16part2('03081770884921959731165446850517') == '53553731'

# Part 2
print("What is the eight-digit message embedded in the final output list?")
test_data5 = '03036732577212944063491565474664'
print(day16part2(data))  # Correct answer is ?
