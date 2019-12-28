# Advent of Code 2019
# Day 6: Universal Orbit Map

# read input file into a list of integers
# expecting just one line of comma separated integers
with open("data/day06.dat", "r") as data_file:
    data = [line.strip() for line in data_file]


def add_parent_child(tree, a, b):
    if a not in tree:
        tree[a] = [b]
    else:
        tree[a].append(b)
    if b not in tree:
        tree[b] = []


def build_tree_from_data(data):
    tree = {}
    for line in data:
        add_parent_child(tree, line.split(')')[0], line.split(')')[1])
    return tree


def bfs_graph(graph, start):
    queue = [start]
    depth = {start: 0}
    while queue:
        v = queue.pop(0)
        for k in graph[v]:
            if k not in depth:
                queue.append(k)
                depth[k] = depth[v] + 1
    return depth


def parent(tree, node):
    result = [v for v in tree if node in tree[v]]
    return result[0] if result else None


def ancestors(tree, node):
    result = []
    v = parent(tree, node)
    while v:
        result += [v]
        v = parent(tree, v)
    return result


def day01part1(data):
    tree = build_tree_from_data(data)
    return sum(bfs_graph(tree, 'COM').values())


def day01part2(data, a, b):
    tree = build_tree_from_data(data)
    depth = bfs_graph(tree, 'COM')
    common = [v for v in ancestors(tree, a) if v in ancestors(tree, b)]
    # nearest ancestor is ancestor with highest depth
    nearest = max(common, key=lambda x: depth[x])
    return depth[a] + depth[b] - 2 * depth[nearest] - 2


# Some tests
test_data1 = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F',
              'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
assert day01part1(test_data1) == 42
test_data2 = test_data1 + ['K)YOU', 'I)SAN']
assert day01part2(test_data2, 'YOU', 'SAN') == 4

# Part 1
print("What is the total number of direct and indirect orbits in your map data?")
print(day01part1(data))  # Correct answer is 130681

# Part 2
print("What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting?")
print(day01part2(data, 'YOU', 'SAN'))  # Correct answer is 313
