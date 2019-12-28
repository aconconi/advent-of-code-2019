# Advent of Code 2019
# Day 8: Space Image Format

# read first line of input file as string
with open("data/day08.dat", "r") as data_file:
    data = data_file.readline().strip()


def chunker(seq, size):
    # returns a generator object
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def generate_image(data, w, h):
    # 0 is black, 1 is white, and 2 is transparent.
    canvas = '2' * w * h
    layers = [x for x in chunker(data, w*h)]
    for layer in reversed(layers):
        canvas = ''.join([c if p == '2' else p for p, c in zip(layer, canvas)])
    return canvas


def day08part1(data, w, h):
    fewest = min(chunker(data, w*h), key=lambda x: x.count('0'))
    return fewest.count('1') * fewest.count('2')


def day08part2(data, w, h):
    image = generate_image(data, w, h)
    # Print image
    s = image.replace('1', '#').replace('0', ' ').replace('2', ' ')
    for line in range(h):
        print(s[line*w:line*w+w])


# Part 1
print("In the layer that contains the fewest 0 digits, what is \
the number of 1 digits multiplied by the number of 2 digits?")
print(day08part1(data, 25,  6))  # Correct answer is 1088

# Part 2
print("What message is produced after decoding your image?")
day08part2(data, 25, 6)  # Correct answer is LGYHB
