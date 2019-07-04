import json
import networkx as nx
import sys
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from threading import Thread

node_size_min = 300
node_size_max = 800


class Graph:
    def __init__(self, solution, showDepotEdges=False):
        Thread.__init__(self)
        self.solution = solution
        self.showDepotEdges = showDepotEdges

    def show(self):
        graph = nx.DiGraph()

        colors = list(mcolors.CSS4_COLORS.values())

        paths = []

        for y, vehicle in enumerate(self.solution["vehicles"]):
            paths.append({
                "color": colors[y % len(colors)],
                "nodelist": [],
                "node_sizes": [],
                "edgelist": []
            })

            for i, city in enumerate(vehicle["route"]):
                graph.add_node(city["id"], pos=(
                    city["location"][0], city["location"][1]))
                paths[y]["nodelist"].append(city["id"])
                paths[y]["node_sizes"].append((city["load"] * 0.5) * 300)
                if i > 1 or self.showDepotEdges:
                    graph.add_edge(vehicle["route"][i - 1]["id"],
                                   city["id"], distance=city["distance"])
                    paths[y]["edgelist"].append(
                        (vehicle["route"][i - 1]["id"], city["id"]))

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
