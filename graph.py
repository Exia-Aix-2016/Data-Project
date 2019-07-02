import json
import networkx as nx
import sys
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

node_size_min = 300
node_size_max = 800

def main(argv):
    with open("results/{}.json".format(argv[0]), 'r') as json_file:
        data = json.load(json_file)

    graph = nx.DiGraph()

    colors = list(mcolors.CSS4_COLORS.values())
    showDepotEdges = bool(int(argv[1]))

    paths = []

    for y, vehicle in enumerate(data["vehicles"]):
        paths.append({
            "color": colors[y % len(colors)],
            "nodelist": [],
            "node_sizes": [],
            "edgelist": []
        })


        for i, city in enumerate(vehicle["route"]):
            graph.add_node(city["id"], pos=(city["location"][0], city["location"][1]))
            paths[y]["nodelist"].append(city["id"])
            paths[y]["node_sizes"].append((city["load"] * 0.5) * 300 )
            if i > 1 or showDepotEdges:
                graph.add_edge(vehicle["route"][i - 1]["id"], city["id"], distance=city["distance"])
                paths[y]["edgelist"].append((vehicle["route"][i - 1]["id"], city["id"]))

    pos = nx.get_node_attributes(graph, 'pos')

    for path in paths:
        nx.draw_networkx_nodes(graph, pos,
                                nodelist=path["nodelist"],
                                node_size=path["node_sizes"],
                                node_color=path["color"])

        nx.draw_networkx_edges(graph, pos,
                                edgelist=path["edgelist"],
                                edge_color=path["color"],
                                connectionstyle="arc3,rad=0.1",
                                width=2)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
