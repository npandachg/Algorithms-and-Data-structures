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
from AlgoDS.basicDS import Stack
from AlgoDS.basicDS import Queue
import numpy as np


class GraphReadError(Exception):
    pass


class Graph(object):
    """Undirected Graph API """

    def __init__(self, vertices):
        self.V = vertices
        self.E = 0
        self.adj = np.empty([self.V], dtype=object)
        for j in range(len(self.adj)):
            self.adj[j] = Bag()

    @classmethod
    def read_from_file(cls, in_stream):
        """ Reads a Graph from input_stream """
        lines = in_stream
        G = cls(int(lines[0]))

        edges = int(lines[1])

        for line in lines:
            G.add_edge(int(line.split()[0]), int(line.split()[1]))

        if edges != G.E:
            raise GraphReadError("Read Error in Graph")

        return G

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


class DirectedGraph(Graph):
    """A DirectedGraph is a set of vertices and a collection of
    directed edges. Each directed edge connects an ordered pair of
    vertices.
    """
    def __init__(self, vertices):
        super(DirectedGraph, self).__init__(vertices)

    def add_edge(self, v, w):
        self.adj[v].add(w)
        self.E += 1

    def reverse(self):
        R = DirectedGraph(self.get_v())
        for vertex in range(self.get_v()):
            for w in self.adjacent_to(vertex):
                R.add_edge(w, vertex)
        return R


class Search(object):
    """Template Search API for Graphs. All search objects will inherit
    from this class.
    """
    def __init__(self, G, source):
        """ Create an array marked, of length equal to number of
        vertices in the Graph, of boolean False. marked[v] is true if
        for a given source vertex s, s is connected to v.
        The source s will be provided by the client.
        edge_to[w] = v means that we came through
        the vertex w via the vertex v.
        """
        self.marked = np.zeros([G.get_v()], dtype=bool)
        self.edge_to = np.zeros([G.get_v()], dtype=int)
        self.source = source
        self.V = G.get_v()

    def is_marked(self, v):
        """ v is marked if marked[v] is True. If true, this
        means that v is connected to one of the source vertex.
        """
        return self.marked[v]

    def path_to(self, v):
        """ find path from v to source s """
        if not self.is_marked(v):
            return None

        stack_of_path = Stack()
        current = v
        while current not in self.source:
            stack_of_path.push(current)
            current = self.edge_to[current]

        stack_of_path.push(current)
        return stack_of_path

    def reachable_from(self, s):
        """ Returns all vertices reachable from s """
        if s not in self.source:
            raise GraphReadError("s not in Source")

        stack_of_vertices = Stack()

        for v in range(self.V):
            if self.marked[v]:
                stack_of_vertices.push(v)

        return stack_of_vertices


class ConnectedComponents(object):
    """ Gives the connected components of a undirected graph.
    """
    def __init__(self, G, search_type="DFS"):
        self.id = np.zeros([G.get_v()], dtype=int)
        if search_type == "BFS":
            search_obj = BFS(G, range(G.get_v()), self.id)
        else:
            search_obj = DFS(G, range(G.get_v()), self.id)
        self.count = search_obj.get_count()

    def are_connected(self, v, w):
        """ Are v and w connected """
        return self.id[v] == self.id[w]

    def get_count(self):
        """ Number of connected components """
        return self.count

    def id(self, v):
        """ return the component id of vertex v """
        return self.id[v]


class DFS(Search):
    """DFS search class for a Graph object. Given a list of
    source verticies, what verticies are connected to each
    source vertex? Is there a path from a given vertex v to any
    one of the source vertex? Use Depth first search to
    answer this.
    """
    def __init__(self, G, source, id=None, order="reverse"):
        """ create a DFS object by inheriting from Search class
        count variable is the number of distinct components connected
        to source.
        """
        self.count = 0
        super(DFS, self).__init__(G, source)
        self.order_type = order
        if order == "pre" or order == "post":
            self.order = Queue()
        if order == "reverse":
            self.order = Stack()

        for s in source:
            if (not self.is_marked(s)):
                self.dfs(G, s, id)
                self.count += 1

    def dfs(self, G, s, id):
        """ Depth first search. Mark s as visited, then
        recursively visit the verticies adjacent to s, ignoring
        the vertex which has been marked before
        """
        if self.order_type == "pre":
            self.order.enqueue(s)

        self.marked[s] = True
        if not (id is None):
            id[s] = self.count
        for w in G.adjacent_to(s):
            if not self.is_marked(w):
                self.edge_to[w] = s
                self.dfs(G, w, id)

        if self.order_type == "post":
            self.order.enqueue(s)
        if self.order_type == "reverse":
            self.order.push(s)

    def get_count(self):
        return self.count

    def _get_order(self):
        return self.order


class BFS(Search):
    """BFS search class for a Graph object. BFS returns
    the shortest path to the source.
    """
    def __init__(self, G, source, id=None):
        super(BFS, self).__init__(G, source)
        self.count = 0
        for s in source:
            if not self.is_marked(s):
                self.marked[s] = True
                self.bfs(G, s, id)
                self.count += 1

    def bfs(self, G, s, id):
        dist_from_src = Queue()
        dist_from_src.enqueue(s)

        """ Start BFS search. In BFS, the queue contains
        vertices at 0 distance from the source, then vertices
        adjacent to the source, then vertices adjacent to the adjacent
        adjacent vertices and so on.
        """
        while not dist_from_src.is_empty():
            # take out item from the queue
            v = dist_from_src.pop()
            if not (id is None):
                id[v] = self.count
            for w in G.adjacent_to(v):
                if not self.is_marked(w):
                    self.marked[w] = True
                    self.edge_to[w] = v
                    dist_from_src.enqueue(w)

    def get_count(self):
        return self.count


class DetectCycle(object):
    """Detect cycle in directed graph"""
    def __init__(self, G):
        self.marked = np.zeros([G.get_v()], dtype=bool)
        self.edge_to = np.zeros([G.get_v()], dtype=int)
        self.on_stack = np.zeros([G.get_v()], dtype=bool)
        self.cycle = None
        # Loop over vertices and do depth first search until
        # cycle is detected
        for v in range(G.get_v()):
            if (not self.marked[v]) and (self.cycle is None):
                self.depth_search(G, v)
            else:
                break

    def depth_search(self, G, v):
        # Mark v and put it on stack
        self.on_stack[v] = True
        self.marked[v] = True
        for w in G.adjacent_to(v):
            if self.cycle is not None:
                return
            # if not marked do depth search
            # else check if we have a cycle
            if not self.marked[w]:
                self.edge_to[w] = v
                self.depth_search(G, w)
            elif self.on_stack[w]:
                self.cycle = Stack()
                current = v
                while not current == w:
                    self.cycle.push(current)
                    current = self.edge_to[current]
                self.cycle.push(w)
                self.cycle.push(v)
        # returning from function, make on stack false
        self.on_stack[v] = False

    def get_cycle(self):
        return self.cycle


class TopologicalOrder(object):
    """Topological sort of a DAG"""
    def __init__(self, G, ord_type):
        order_types = ["pre", "post", "reverse"]
        self.order = None
        if ord_type not in order_types:
            raise GraphReadError("order should be : pre, post\
             or reverse")
        check_cycle = DetectCycle(G)
        if check_cycle.get_cycle() is not None:
            raise GraphReadError("Graph is not DAG")
        dfs = DFS(G, range(G.get_v()), order=ord_type)
        self.order = dfs._get_order()

    def get_order(self):
        return self.order


















