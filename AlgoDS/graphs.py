"""Graph module for UndirectedGraphs, DirectedGraphs, etc. The vertex
are assumed to be integers. Use symbol table to map integers to
a given vertex description.

Graph : A set of vertices and a collection of edges that each
connect a pair of vertices. We allow self loops (edge that con
nect the same vertex) and parallel edges (multiple edges)
connecting the same pair of vertices.

Nomenclature and Definitions:
Adjacent: Two vertices are adjacent if there is an edge connecting
the two.

Incident: If an edge connects two vertices, we say that
the edge is Incident to both.

Degree: Number of incident egdes to a vertex.

Subgraph: Subset of a graph's edges and the associated vertices
that constitutes a graph on its own.

Path: A sequence of vertices connected by edges.

Simple Path: A path with no repeated vertices.

Cycle: A closed path with whose first and last vertices
are same.

Length: Number of edges in a cycle or path.
"""
from AlgoDS.basicDS import Bag
import numpy as np


class GraphReadError(Exception):
    pass


class Graph(object):
    """Undirected Graph API """

    def __init__(self, in_stream):
        """ Reads a Graph from input_stream """

        lines = in_stream
        self.V = int(lines[0])
        self.E = 0
        edges = int(lines[1])
        self.adj = np.empty([self.V], dtype=object)
        for j in range(len(self.adj)):
            self.adj[j] = Bag()

        for line in lines:
            self.add_edge(int(line.split()[0]), int(line.split()[1]))

        if edges != self.E:
            raise GraphReadError("Read Error in Graph")

    def add_edge(self, v, w):
        """ add an edge from v to w and from w to v"""
        self.adj[v].add(w)
        self.adj[w].add(v)
        self.E += 1

    def adjacent_to(self, v):
        """ returns the vertices adjacent to v """
        return self.adj[v]

    def get_v(self):
        return self.V

    def get_e(self):
        return self.E

    def __str__(self):
        s = str(self.V) + " vertices " + str(self.E) + " Edges\n"
        for v in range(self.V):
            s += str(v) + " : "
            for w in self.adj[v]:
                s += str(w) + " "
            s += "\n"
        return s


class Search(object):
    """Search API for Graphs"""
    def __init__(self, arg):
        super(Search, self).__init__()
        self.arg = arg







