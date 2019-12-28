# Advent of Code 2019
# Day 18: Many-Worlds Interpretation

from itertools import combinations
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

INF = float("inf")


def grid_from_lines(lines, keys, doors):
    # load grid from file and build a graph
    cols = len(lines[0])
    rows = len(lines)
    grid = nx.grid_2d_graph(cols, rows)
    y = 0
    for line in lines:
        for x, c in enumerate(line):
            if c == '#':
                grid.remove_node((x, y))
            elif 'a' <= c <= 'z' or c in {'@', '1', '2', '3', '4'}:
                keys[c] = (x, y)
            elif 'A' <= c <= 'Z':
                doors[c.lower()] = (x, y)
        y += 1
    return grid

# # build a graph only for keys
# graph = nx.Graph()
# for k in keys:
#     graph.add_node(k)
# for d in doors:
#     graph.add_node(k)


def parse_grid(grid, dist, inbetween):
    for k1, k2 in combinations(keys, 2):
        try:
            sp = nx.shortest_path(grid, source=keys[k1], target=keys[k2])
            dist[(k1, k2)] = len(sp) - 1
            # inbetween[(k1,k2)] = [d for d in doors if d not in {k1, k2} and doors[d] in sp]
            inbetween[(k1, k2)] = [d for d in doors if d !=
                                   k2 and doors[d] in sp]

        except nx.NetworkXNoPath:
            dist[(k1, k2)] = INF
            inbetween[(k1, k2)] = ['#']
            # print(f"No path between {k1} and {k2}. Their distance is {dist[(k1,k2)]}")

        # replicate entries for inverted keys
        inbetween[(k2, k1)] = inbetween[(k1, k2)]
        dist[(k2, k1)] = dist[(k1, k2)]

        # graph.add_edge(k1, k2, weight=len(sp) - 1)


# pos = nx.circular_layout(graph)  # positions for all nodes
# nx.draw_networkx_nodes(graph, pos)
# nx.draw_networkx_edges(graph, pos)
# edge_labels = nx.get_edge_attributes(graph,'weight')
# nx.draw_networkx_edge_labels(graph,pos, edge_labels=edge_labels)
# nx.draw_networkx_labels(graph, pos)
# plt.axis('off')
# plt.show()

# print(inbetween)


def reachable_keys(source, havekeys):
    assert source in havekeys
    targetkeys = [k for k in keys if k not in havekeys]
    return [k for k in targetkeys if set(inbetween[source, k]).issubset(set(havekeys))]


def solve(v, havekeys):
    hks = ''.join(sorted(havekeys))
    if (v, hks) in memoized:
        # print("cache hit!")
        return memoized[(v, hks)]

    # print(f"Visiting {v} with havekeys={havekeys}")
    havekeys.append(v)

    if len(havekeys) == len(keys):
        # print(f"solution found with havekeys={havekeys} cost={sum_path(havekeys)}")
        return 0
    else:
        reach = reachable_keys(v, havekeys)
        # print(f"Can reach {reach} from {v} with havekeys={havekeys}")
        cost = INF
        if reach:
            # print(f"reach {reach}")
            cost = min(dist[v, k] + solve(k, havekeys.copy()) for k in reach)

    havekeys.pop()
    memoized[(v, hks)] = cost
    return cost


def sum_path(path):
    return sum([dist[a, b] for a, b in zip(path, path[1:])])


def new_state(state, to_be_removed, to_be_added):
    ans = []
    for c in state:
        ans.append(c if c != to_be_removed else to_be_added)
    return ans


def reachable_keys_multi(state, havekeys):
    # assert set(state).issubset(set(havekeys))
    wanted = [k for k in keys if k not in havekeys and k not in state]
    ans = []
    if wanted:
        for v in state:
            ans.extend([k for k in wanted if set(inbetween[v, k]
                                                 ).issubset(set(havekeys).union(set(state)))])
    return sorted(ans)


def solve_multi(state, havekeys):
    m = ("".join(state), "".join(sorted(havekeys)))
    if m in memoized:
        if not len(memoized) % 100000:
            print(f"cached: {len(memoized)}")
        return memoized[m]

    # print(f"Visiting {state} with havekeys={havekeys}")
    # havekeys.extend([s for s in state if s not in havekeys])

    if len(set(havekeys).union(set(state))) == len(keys):
        # print(f"solution found with state={state} havekeys={havekeys}")
        return 0
    else:
        mincost = INF
        cost = {}
        reach = reachable_keys_multi(state, havekeys)
        if reach:
            for v in state:
                for k in reach:
                    if dist[v, k] < mincost:
                        # print(f"Can reach {reach} from {state} considering {v} with havekeys={havekeys}")
                        cost[v, k] = dist[v, k] + \
                            solve_multi(new_state(state, v, k),
                                        list(set(state + havekeys)))
                        if cost[v, k] < mincost:
                            mincost = cost[v, k]

    # for _ in state:
    #     havekeys.pop()
    memoized[m] = mincost
    return mincost


memoized = {}
# data_file = "data/day18.dat"
data_file = "data/day18_part2.dat"
lines = open(data_file, "r").read().splitlines()
keys = {}
doors = {}
grid = grid_from_lines(lines, keys, doors)
inbetween = {}
dist = {}
parse_grid(grid, dist, inbetween)


# Part 1
# print("How many steps is the shortest path that collects all of the keys?")
# print(solve('@', [])) # Correct answer is 4248

# Part 2
print(solve_multi(['1', '2', '3', '4'], []))  # Correct anser is ? 1878
