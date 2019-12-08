# Advent of Code 2019
# Day 8: Space Image Format

# read first line of input file as string
with open("data/day08.dat", "r") as data_file:
        data = data_file.readline().strip()
        
test_data1 = "123456789012"      # image size 3x2
test_data2 = "0222112222120000"  # image size 2x2


def chunker(seq, size):
    # returns a generator object
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def iter_layers(s, w, h):
    layer_size = w * h
    num_layers = len(s) // layer_size
    for i in range(num_layers):
        a = layer_size * i 
        b = layer_size * (i+1)
        yield s[a:b]

def print_image(image, w, h):
    s = image.replace('1', '#').replace('0', ' ').replace('2', ' ') 
    for line in range(h):
        print(s[line*w:line*w+w])
        
def overlay_pixel(p,c):
    # 0 is black, 1 is white, and 2 is transparent.
    return c if p == '2' else p

def day08part1(data, w, h):
    fewest = min(chunker(data, w*h), key=lambda x: x.count('0'))
    return fewest.count('1') * fewest.count('2')

def day08part2(data, w, h):
    canvas = '2' * w *  h
    layers = [x for x in chunker(data, w*h)]
    for layer in reversed(layers):
        canvas = ''.join([overlay_pixel(p, c) for p, c in zip(layer, canvas)])
    print_image(canvas, w, h)


# Part 1
print("In the layer that contains the fewest 0 digits, what is \
the number of 1 digits multiplied by the number of 2 digits?")
print(day01part1(data, 25,  6))

# Part 2
print("What message is produced after decoding your image?")
day01part2(data, 25, 6) # prints LGYHB
