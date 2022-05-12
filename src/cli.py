import argparse
from graph import Graph

def read_file(file_path, N):
    """
        Reads the file and builds a graph from it.
    """
    def unwrap_tuple(tuple_string):
        """
            Unwraps a tuple string into a tuple.
        """
        return list(map(str.strip, tuple_string[1:-1].split(',')))

    def parse_tuple(tuple):
        """
            Parses a tuple's elements if they are integers.
        """
        first_element = tuple[0]
        if first_element.isnumeric():
            first_element = int(first_element)

        second_element = tuple[1]
        if second_element.isnumeric():
            second_element = int(second_element)

        return (first_element, second_element)

    graph = Graph(N)

    with open(file_path, 'r') as f:
        lines = f.readlines()

        for line in lines:
            # Return the line following this format [<type>: str, <tuples>: str]
            line = list(map(str.strip, line.split(':')))

            element = line[0]

            # Return the tuples following this format [[<first_element>: str, <second_element>: str]]
            tuples = list(map(unwrap_tuple, list(
                map(str.strip, line[1].split(';')))))
            tuples = list(map(parse_tuple, tuples))

            if element == 'E':
                #  Store the constraints in the graph
                for constraint in tuples:
                    graph.add_constraint(constraint)
            elif element == 'X':
                # The first tuple is the bottom left corner and the second tuple is the upper right corner
                # We mark every position between the two corners as an obstacle
                x1, y1 = tuples[0]
                x2, y2 = tuples[1]
                for i in range(x1, x2 + 1):
                    for j in range(y1, y2 + 1):
                        graph.set_node_type((i, j), 'X')
            else:
                # Add the element to the graph
                for position in tuples:
                    if graph.nodes[position].type != 'R':
                        graph.set_node_type(position, element)

    return graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str,
                        help='The path to the file to read.')
    parser.add_argument('N', type=int, help='The size of the grid.')
    args = parser.parse_args()

    graph = read_file(args.file_path, args.N)
    graph.print()
