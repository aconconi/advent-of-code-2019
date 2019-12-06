# SCRATCHES

# visits all the nodes of a graph (connected component) using BFS
def bfs_graph2(graph, start):
    # keep track of all visited nodes
    explored = []

    # keep track of nodes to be checked
    queue = [start]

    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        v = queue.pop(0)
        if v not in explored:
            # add node to list of checked nodes
            explored.append(v)
            neighbours = graph[v]

            # add neighbours of node to queue
            for k in neighbours:
                queue.append(k)
    return explored

def bfs_tree(tree, start):
    # keep track of all visited nodes
    explored = []

    # keep track of nodes to be checked
    queue = [start]

    while queue:
        v = queue.pop(0)
        explored.append(v)
        queue.extend(tree[v])

    return explored
