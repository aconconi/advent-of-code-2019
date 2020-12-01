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




def run_program(m, input_values):
    out = []
    # instruction pointer
    x = 0
    full_opcode = ""

    # get value by dereferencing pointer if needed
    def deref(mode, val):
        # '1' is immediate mode, '0' is position mode
        return val if mode == '1' else m[val]

    def deref_par(i):
        return deref(full_opcode[3-i], m[x+i])

    def read_par(i):
        return m[x+i]

    while m[x] != 99:
        full_opcode = str(m[x]).zfill(5)  # pad string with 0 so that it's always 5 digits
        opcode = int(full_opcode[3:])     # opcode is two rightmost digits
        if opcode in [1,2]:
            # Operation: sum or multiply
            a, b, c = deref_par(1), deref_par(2), read_par(3)
            m[c] = a + b if opcode == 1 else a * b
            x += 4
        elif opcode == 3:
            # Operation: input
            a = read_par(1)
            m[a] = input_values.pop(0)
            x += 2
        elif opcode == 4:
            # Operation: output
            a = deref_par(1)
            out.append(a)  
            x += 2
        elif opcode == 5:
            # Operation: jump-if-true
            a, b = deref_par(1), deref_par(2)
            x = b if a != 0 else x+3
        elif opcode == 6:
            # Operation: jump-if-false
            a, b = deref_par(1), deref_par(2)
            x = b if a == 0 else x+3
        elif opcode == 7:
            # Operation: less-than
            a, b, c = deref_par(1), deref_par(2), read_par(3)
            m[c] = 1 if a < b else 0
            x += 4
        elif opcode == 8:
            # Operation: less-than
            a, b, c = deref_par(1), deref_par(2), read_par(3)
            m[c] = 1 if a == b else 0
            x += 4           
        else:
            print("Invalid opcode found.")
            exit(1)
    return out

