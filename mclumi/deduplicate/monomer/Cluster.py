__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import os
import sys
sys.path.insert(0, os.path.abspath('../../..'))
import networkx as nx
from mclumi.network.CC import cc as gbfscc


class cluster(object):

    def __init__(self, ):
        pass

    def cc(self, graph_adj):
        """

        Parameters
        ----------
        graph_adj

        Returns
        -------

        """
        connected_components = list(gbfscc().deque(graph_adj))
        return {i: cc for i, cc in enumerate(connected_components)}

    def ccnx(self, edge_list):
        """

        Parameters
        ----------
        edge_list

        Returns
        -------

        """
        G = nx.Graph()
        for edge in edge_list:
            G.add_edge(edge[0], edge[1])
        return {i: G.subgraph(cc).nodes() for i, cc in enumerate(nx.connected_components(G))}


if __name__ == "__main__":
    p = cluster()
    print(p.cc({0: [1,], 1: [0, 2], 2: [1]}))
    print(p.cc({0: []}))