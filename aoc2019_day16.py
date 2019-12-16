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
    return new

def apply(pattern, signal):
    # print(f"Pattern: {pattern}, signal: {signal}")
    return abs(sum( s * p for s, p in zip(signal, cycle(rotate_left(pattern))))) % 10

def phase(signal):
    r = []
    for i in range(len(signal)):
        pattern = expand(BASE_PATTERN, i+1, len(signal))
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

def day16part2(signal_str, phases):
    length = len(signal_str)
    offset = int(signal_str[:7])
    times  = 10000
    # print(f"Offset: {offset}")
    signal = [int(c) for c in signal_str] * times
    # print(f"Starting phases with signal {signal}, len {length}")
    for i in range(phases):
        # print(f"Phase {i}...")
        signal = phase(signal)
        
    result = list_to_string(signal[offset:offset+8])
    return result
    


# Test cases for part 1
test_data1 = '12345678' # becomes 01029498 after 4 phases 
test_data2 = '80871224585914546619083218645595' # becomes 24176176 after 100 phases
test_data3 = '19617804207202209144916044189917' # becomes 73745418 after 100 phases
test_data4 = '69317163492948606335995924319873' # becomes 52432133 after 100 phases
assert day16part1(test_data1, 4) == '01029498'
assert day16part1(test_data2, 100) == '24176176'
assert day16part1(test_data3, 100) == '73745418'
assert day16part1(test_data4, 100) == '52432133'

with open("data/day16.dat", "r") as data_file:
        data = data_file.readline().strip()

# Part 1
# print("After 100 phases of FFT, what are the first eight digits in the final output list?")
# print(day16part1(data, 100))

# Part 2
# print("Part 2")
# test_data5 = '03036732577212944063491565474664'
# print(day16part2(test_data5, 1))  # Correct answer is 73127523

# print(expand(BASE_PATTERN, 8))