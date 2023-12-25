from typing import Union
from util.util import ProcessInput, run_day
import networkx as nx
import matplotlib.pyplot as plt


debug = True


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2023).data

    # Process to node mapping
    edge_list = []
    node_mapping = {}
    for row in data:
        r_from, r_to = row.split(': ')
        r_to = r_to.split(' ')
        for x in r_to:
            edge_list.append([r_from, x])
            if r_from not in node_mapping:
                node_mapping[r_from] = []
            node_mapping[r_from].append(x)

            if x not in node_mapping:
                node_mapping[x] = []
            node_mapping[x].append(r_from)
    if debug:  # Plot to find the three edges that keep the two parts together
        G = nx.Graph()
        G.add_edges_from(edge_list)
        nx.draw_networkx(G)
        plt.show()

    # Remove these links based on above visual inspection
    remove = [('gpj', 'tmb'), ('rhh', 'mtc'), ('njn', 'xtx')] if not example_run else [('hfx', 'pzl'), ('bvb', 'cmg'), ('jqt', 'nvd')]

    # Identify all in one part by starting with all on that side and increasing the group without linking to the other
    # part of the linking nodes
    total_node = len(node_mapping)
    node_A = {remove[i][0] for i in range(3)}
    node_B = {remove[i][1] for i in range(3)}
    stop = False
    while not stop:
        new_node_A = node_A.copy()
        for node in node_A:
            for x in node_mapping[node]:
                if x not in node_B:
                    new_node_A.add(x)
        if new_node_A == node_A:
            stop = True
        else:
            node_A = new_node_A

    result_part1 = len(node_A) * (total_node - len(node_A))  # > 2986
    result_part2 = "Merry Christmas :)"

    extra_out = {'Number of rows in input': len(data),
                 'Number of edges': int(sum(len(x) for x in node_mapping.values()) / 2),
                 'Number of nodes': total_node,
                 'Group sizes': (len(node_A), total_node - len(node_A))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
