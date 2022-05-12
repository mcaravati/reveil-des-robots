import matplotlib.pyplot as plt

class Node:
    """
        A node in the graph.
    """
    type = None

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


# Create a grid graph of size N * N
# Create a graph with the following structure:
#   - Each node is a position
#   - Each edge is a tuple of two positions
class Graph:
    def __init__(self, N):
        self.N = N
        self.graph = {}
        self.nodes = {}
        self.constraints = []

        # Create the nodes
        for i in range(N):
            for j in range(N):
                self.graph[(i, j)] = []
                self.nodes[(i, j)] = Node((i, j), i, j)

        # Initialize the children of each node
        for i in range(N):
            for j in range(N):
                if i + 1 < N:
                    self.graph[(i, j)].append((i + 1, j))
                if i - 1 >= 0:
                    self.graph[(i, j)].append((i - 1, j))
                if j + 1 < N:
                    self.graph[(i, j)].append((i, j + 1))
                if j - 1 >= 0:
                    self.graph[(i, j)].append((i, j - 1))

    def get_neighbors(self, node):
        return self.graph[node]

    def set_node_type(self, node, type):
        self.nodes[node].type = type

    def print(self):
        # We print the node a different color for each type
        for node in self.nodes:
            # If the node is a robot, we print it in red
            if self.nodes[node].type == "R":
                plt.plot(node[0], node[1], "ro")
            # If the node is an obstacle, we print it in blue
            elif self.nodes[node].type == "X":
                plt.plot(node[0], node[1], "bo")
            # If the node is a constraint, we print it in green
            elif self.nodes[node].type == "E":
                plt.plot(node[0], node[1], "go")
            # If the node is another robot, we print it in black
            elif self.nodes[node].type and self.nodes[node].type.isnumeric():
                plt.plot(node[0], node[1], "yo")

        # We print the edges
        for edge in self.graph:
            for neighbor in self.graph[edge]:
                plt.plot([edge[0], neighbor[0]], [edge[1], neighbor[1]], "k-")

        plt.show()

    def add_constraint(self, constraint):
        self.constraints.append(constraint)