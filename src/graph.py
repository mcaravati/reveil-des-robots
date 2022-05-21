from turtle import width
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import random

class Node:
    """
        A node in the graph.
    """
    type = None

    def __init__(self, id: Tuple[int, int], x: int, y: int):
        self.id: Tuple[int, int] = id
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return "Node {}: ({}, {})".format(self.id, self.x, self.y)
    
    def __repr__(self) -> str:
        return self.__str__()


# Create a grid graph of size N * N
# Create a graph with the following structure:
#   - Each node is a position
#   - Each edge is a tuple of two positions
class Graph:
    def __init__(self, N: int):
        # Here we store the graph size for if needed
        # for further purpose
        self.N: int = N

        self.R = None

        # Graph store the position the neighbors of each vertex
        # ex: (0, 0): [(0, 1), (1, 0)]
        self.graph: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}

        # Nodes store the Node object of each vertex
        # ex: (0, 0): Node<(0, 0)>
        self.nodes: Dict[Tuple[int, int], Node] = {}

        self.constraints = []

        # Create the nodes
        for i in range(N):
            for j in range(N):
                self.graph[(i, j)] = []
                self.nodes[(i, j)] = Node((i, j), i, j)

        # Initialize the children of each node
        for i in range(N):
            for j in range(N):
                # Do not add the neighbor to the right
                # if we are on the last column
                if i + 1 < N:
                    self.graph[(i, j)].append((i + 1, j))
                
                # Do not add the neighbor to the left
                # if we are on the first column
                if i - 1 >= 0:
                    self.graph[(i, j)].append((i - 1, j))

                # Do not add the neighbor to the bottom
                # if we are on the last row
                if j + 1 < N:
                    self.graph[(i, j)].append((i, j + 1))

                # Do not add the neighbor to the top
                # if we are on the first row
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

    def __str__(self) -> str:
        return "Graph: {}\nNodes: {}\nConstraints: {}".format(self.graph, self.nodes, self.constraints)

    def __repr__(self) -> str:
        return self.__str__()

    def generate_random_obstacles(self, number: int) -> None:
        for i in range(number):
            # Generate a random position for the lower left corner of the obstacle
            x = random.randint(0, self.N - 1)
            y = random.randint(0, self.N - 1)

            # Generate a random size for the obstacle
            width = random.randint(1, self.N - x)
            height = random.randint(1, self.N - y)

            def check_for_robots():
                # Check if the obstacle covers a robot
                for i in range(x, x + width):
                    for j in range(y, y + height):
                        if self.nodes[(i, j)].type == "R":
                            return True
                
                return False

            while check_for_robots():
                x = random.randint(0, self.N - 1)
                y = random.randint(0, self.N - 1)

                width = random.randint(1, self.N - x)
                height = random.randint(1, self.N - y)


            # Set the obstacle in the graph
            for i in range(width):
                for j in range(height):
                    self.set_node_type((x + i, y + j), "X")

    def print_path(self, path: List[Tuple[int, int]]) -> None:
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

        # We print the path
        if (type(path) == list) :
            for i in range(len(path) - 1):
                plt.plot([path[i][0], path[i + 1][0]], [path[i][1], path[i + 1][1]], "r-")
        else :  
            colors = ["r-", "yo-", "go-", "k-"]
            j = 0
            for keys in path.keys() :
                first = keys
                for i in range(len(path[keys])):
                    plt.plot([first[0], path[keys][i][0]], [first[1], path[keys][i][1]], colors[j])
                    first = path[keys][i]
                j+=1   
        plt.show()
