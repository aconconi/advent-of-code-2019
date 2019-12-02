# Advent of Code 2019
# Day 2: 1202 Program Alarm

# read input file and load data into array of integers
# expecting just 1 line of comma separated integers
with open("data/day02.dat", "r") as data_file:
    data = [int(x) for x in data_file.read().split(",")]

def run_program(p):
    x = 0
    while(p[x] != 99):
        # print("x:", x, "p:", p, "p[x]:", p[x])
        if p[x] == 1:
            p[ p[x+3] ] = p[ p[x+1] ] + p[ p[x+2] ]
        elif p[x] == 2:
            p[ p[x+3] ] = p[ p[x+1] ] * p[ p[x+2] ]
        else:
            print("Invalid opcode found.")
            exit(1)
        x += 4
    return p

# Some test cases
def test_run_program():
    assert run_program([99]) == [99]
    assert run_program([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
    assert run_program([1,0,0,0,99]) == [2,0,0,0,99]
    assert run_program([2,3,0,3,99]) == [2,3,0,6,99]
    assert run_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

def day02part1(data, noun, verb):
    memory = data.copy()
    memory[1] = noun
    memory[2] = verb
    run_program(memory)
    return memory[0]
 
def day02part2(data, target):
    for noun in range(100):
        for verb in range(100):
            r = day02part1(data, noun, verb)
            if r == target:
                return r
    print("day02part2: could not find solution.")
    exit(1)    


test_run_program()

# Part 1
print("What value is left at position 0 after the program halts?")
print(day02part1(data, 12, 2))  # Correct answer is 4330636

# Part 2
print("What is 100 * noun + verb?")
print(day02part2(data, 19690720))  # Correct answer is 6086
