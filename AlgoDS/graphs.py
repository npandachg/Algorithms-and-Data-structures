"""Graph module for Graph Data structure : UndirectedGraphs,
DirectedGraphs, etc and Graph processing classes: Search,
ConnectedComponents etc.

The verticies are assumed to be integers. Use symbol table
to map integers to a given vertex description.

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

Cycle: A closed path whose first and last vertex
are same.

Length: Number of edges in a cycle or path.
"""
from AlgoDS.basicDS import Bag
from AlgoDS.basicDS import Stack
from AlgoDS.basicDS import Queue
from AlgoDS.basicDS import MinPQ
from AlgoDS.basicDS import UnionFind

import collections
from sets import Set
import numpy as np


class GraphReadError(Exception):
    pass


# Edge class for edge weighted graph type
class Edge(object):
    """Edge class where each edge has a weight associated
    with it.
    """
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def either(self):
        """ returns one of the end points
        """
        return self.v

    def other(self, v):
        """ returns the other end point """
        if v == self.v:
            return self.w
        if v == self.w:
            return self.v

    def get_weight(self):
        return self.weight


# Graph data structures
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


class EdgeWeightedGraph(Graph):
    """Edge Weighted Graph"""
    def __init__(self, vertices):
        super(EdgeWeightedGraph, self).__init__(vertices)

    @classmethod
    def read_from_file(cls, in_stream):
        """ Reads a Graph from input_stream """
        lines = in_stream
        G = cls(int(lines[0]))

        edges = int(lines[1])

        for line in lines:
            v = int(line.split()[0])
            w = int(line.split()[1])
            weight = float(line.split()[2])

            tmp_edge = Edge(v, w, weight)
            G.add_edge(tmp_edge)

        if edges != G.E:
            raise GraphReadError("Read Error in Graph")

        return G

    def add_edge(self, e):
        v = e.either()
        w = e.other(v)
        self.adj[v].add(e)
        self.adj[w].add(e)
        self.E += 1

    def edges(self):
        """ return the edges """
        ed = Bag()
        for v in range(self.V):
            for e in self.adj[v]:
                if e.other(v) > v:
                    ed.add(e)
        return ed

    def __str__(self):
        s = str(self.V) + " vertices " + str(self.E) + " Edges\n"
        for v in range(self.V):
            s += str(v) + " : "
            for e in self.adj[v]:
                s += str(e.other(v)) + " " + str(e.get_weight()) + " "
            s += "\n"
        return s


# Graph processing classes
class Degrees(object):
    """docstring for Degrees"""

    def __init__(self, G):
        self.in_degree = np.zeros([G.get_v()], dtype=int)
        self.out_degree = np.zeros([G.get_v()], dtype=int)
        self.sources = Stack()
        self.sinks = Stack()
        for vertex in range(G.get_v()):
            adjacency = G.adjacent_to(vertex)
            self.out_degree[vertex] = adjacency.size()
            for w in adjacency:
                self.in_degree[w] += 1

        for vertex in range(G.get_v()):
            if self.in_degree[vertex] == 0:
                self.sources.push(vertex)
            if self.out_degree[vertex] == 0:
                self.sinks.push(vertex)

    def get_sinks(self):
        return self.sinks

    def get_sources(self):
        return self.sources

    def get_outdegree(self, v):
        return self.out_degree[v]

    def get_indegree(self, v):
        return self.in_degree[v]


class Search(object):
    """Template Search API for Graphs. All search objects will inherit
    from this class.
    Given a list of source verticies, what verticies are
    connected to each source vertex? Is there a path from a
    given vertex v to any one of the source vertex?
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
    """ Gives the connected components of an undirected graph.
    Use DFS to find connected components.
    """

    def __init__(self, G, order=None):
        self.id = np.zeros([G.get_v()], dtype=int)
        self.order = order
        if order is None:
            self.order = range(G.get_v())
        search_obj = DFS(G, self.order, self.id)
        self.count = search_obj.get_count()

    def are_connected(self, v, w):
        """ Are v and w connected/strongly connected"""
        return self.id[v] == self.id[w]

    def get_count(self):
        """ Number of connected components """
        return self.count

    def get_id(self, v):
        """ return the component id of vertex v """
        return self.id[v]


class DFS(Search):
    """D(epth)F(irst)S(earch) search class for a Graph object.
    """

    def __init__(self, G, source, id=None, order="reverse"):
        """ create a DFS object by inheriting from Search class.
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
        the vertex which has been marked before.
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
    """B(readth)F(irst)S(earch) search class for a Graph object.
    BFS returns the shortest path to the source.
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
        adjacent vertices and so on. Thus BFS gives us the
        shortest path.
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
            # if we found cycle, no need to continue
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

    def has_cycle(self):
        return self.cycle is not None


class TopologicalOrder(object):
    """Topological order of a Digraph: pre, post or reverse post"""

    def __init__(self, G, ord_type="reverse"):
        order_types = ["pre", "post", "reverse"]

        if ord_type not in order_types:
            raise GraphReadError("order should be : pre, post\
             or reverse")
        dfs = DFS(G, range(G.get_v()), order=ord_type)

        self.order = dfs._get_order()

    def get_order(self):
        return self.order


class TopologicalSort(object):
    """sort DAG based on topological order i.e
    given a digraph, put the vertices in an order such that
    all its directed edges point from a vertex earlier in the
    order to a vertex later in the order.
    """

    def __init__(self, G):
        check_cycle = DetectCycle(G)
        self.sortable = False
        if check_cycle.get_cycle() is None:
            self.sortable = True
            self.top_order = TopologicalOrder(G)

    def sort(self):
        if self.sortable:
            return self.top_order.get_order()
        else:
            return None

    def is_DAG(self):
        return self.sortable


class StrongCC(ConnectedComponents):
    """strongly connected components of a directed Graph.
    Two vertices v, w are strongly connected if there is a
    directed path from v to w and from w to v. Strong connectivity
    partitions the graph into equivalance class given by the
    relation : connected to. The following algorithm is
    due to Kosaraju and Sharir.

    """

    def __init__(self, G):
        top_order = TopologicalOrder(G.reverse())
        super(StrongCC, self).__init__(G, order=top_order.get_order())


class ShortestAncestralPath(object):
    """finds the shortest distance to a common ancestor in a
    directed graph.
    """

    def __init__(self, G):
        self.marked = np.zeros([G.get_v()], dtype=bool)
        self.edge_to = np.zeros([G.get_v()], dtype=int)
        self.first_source = dict()
        self.cache = Set()
        self.cache_col = Set()
        self.G = G

    def length(self, v, w):
        if (type(v) == int) and (type(w) == int):
            if (v in self.cache) and (w in self.cache):
                return self.min_length
            else:
                self._sap_dfs(self.G, v, w)
                return self.min_length
        elif (isinstance(v, collections.Iterable)) and \
                (isinstance(w, collections.Iterable)):
            self._sap_dfs_collections(self.G, v, w)
            return self.min_length_col

    def ancestor(self, v, w):
        if (type(v) == int) and (type(w) == int):
            if (v in self.cache) and (w in self.cache):
                return self.common_ancestor
            else:
                self._sap_dfs(self.G, v, w)
                return self.common_ancestor
        elif (isinstance(v, collections.Iterable)) and \
                (isinstance(w, collections.Iterable)):
            self._sap_dfs_collections(self.G, v, w)
            return self.common_ancestor_col

    def _sap_dfs(self, G, v, w):
        """ find the common ancestor of v and w that participates
        in shortest path. Here v, w are int type.
        Each vertex is an ancestor of itself and hence is 0 distance
        from itself. Use BFS to find ancestors with minimum length.
        """

        # create queue to put v as source
        dist_from_src = Queue()
        # add v to the queue
        dist_from_src.enqueue(v)
        # mark v as visited
        self.marked[v] = True

        # set up cache data structure
        self.cache = Set()
        self.cache.add(v)
        self.cache.add(w)

        if v == w:
            self.common_ancestor = v
            self.min_length = 0
            return

        """empty dictionary :
        key : ancestors of v
        value : length from v
        """
        self.first_source = dict()

        # v is an ancestor of itself with length 0
        self.first_source[v] = 0

        # Start BFS from v
        while not dist_from_src.is_empty():
            # take out item from the queue
            v1 = dist_from_src.pop()
            # check for vertices adjacent to v1
            for w1 in G.adjacent_to(v1):
                # if not marked add them to queue
                if not self.marked[w1]:
                    # w1 is ancestor of v!
                    self.marked[w1] = True
                    self.edge_to[w1] = v1
                    # add it to queue
                    dist_from_src.enqueue(w1)
                    # find the length frow v to w1
                    current = w1
                    length = 0
                    while not (current == v):
                        length += 1
                        current = self.edge_to[current]
                    # add w1, length as the ancestor of v
                    self.first_source[w1] = length

        # BFS from w.
        # First change back self.marked and self.edge_to
        for v in self.first_source.keys():
            self.marked[v] = False
            self.edge_to[v] = 0

        # make common_ancestor none and min_length large
        common_ancestor = -1
        min_length = float("inf")

        # add w to queue
        dist_from_src.enqueue(w)
        # mark w as True
        self.marked[w] = True
        # all ancestors of w are in the stack indx
        indx = Stack()
        # w is an ancestor of itself
        indx.push(w)
        while not dist_from_src.is_empty():
            # take out item from the queue
            v1 = dist_from_src.pop()

            # check if v1 is an ancestor of v
            if v1 in self.first_source:
                # v1 is a common ancestor!
                length = 0
                # find the length frow w to v1
                current = v1
                while not (current == w):
                    length += 1
                    current = self.edge_to[current]
                # check if the total length is smallest
                tot_length = length + self.first_source[v1]
                if tot_length < min_length:
                    common_ancestor = v1
                    min_length = tot_length

            # check for vertices adjacent to v1
            for w1 in G.adjacent_to(v1):
                # if not marked add them to queue
                if not self.marked[w1]:
                    self.marked[w1] = True
                    self.edge_to[w1] = v1
                    # add it to queue
                    dist_from_src.enqueue(w1)
                    indx.push(w1)

        # Change back self.marked and self.edge_to
        for w in indx:
            self.marked[w] = False
            self.edge_to[w] = 0

        # Put common ancestor and min length in instance var for caching!
        self.common_ancestor = common_ancestor
        if min_length == float("inf"):
            self.min_length = -1
        else:
            self.min_length = min_length

    def _sap_dfs_collections(self, G, v, w):
        """ Here v and w are iterable. Allowed data types for
        v and w are Bag, Queues and Stack.
        See _sap_dfs. """
        if not isinstance(v, collections.Iterable):
            raise GraphReadError("v is not iterable: make it \
                Bag, Queue or Stack")

        if not isinstance(w, collections.Iterable):
            raise GraphReadError("w is not iterable: make it \
                Bag, Queue or Stack")

        # check if v and w are in cache_col
        if (v in self.cache_col) and (w in self.cache_col):
            return
        # set up cache data structure
        else:
            self.cache_col = Set()
            self.cache.add(v)
            self.cache.add(w)

        """empty dictionary :
        key : ancestors of v
        value : length from v
        """
        self.first_source = dict()

        # better to use dict if v is large
        v_set = Set()

        # create queue to put v as source
        dist_from_src = Queue()
        for vertex in v:
            v_set.add(vertex)
            # add vertex to queue
            dist_from_src.enqueue(vertex)
            # mark vertex as visited
            self.marked[vertex] = True
            # source vertex are ancestors of themselves and 0 dist
            self.first_source[vertex] = 0

        # start BFS from v
        while not dist_from_src.is_empty():
            # take out item from the queue
            v1 = dist_from_src.pop()
            # check for vertices adjacent to v1
            for w1 in G.adjacent_to(v1):
                # if not marked add them to queue
                if not self.marked[w1]:
                    self.marked[w1] = True
                    self.edge_to[w1] = v1
                    # add it to queue
                    dist_from_src.enqueue(w1)
                    # find the length frow v to w1
                    current = w1
                    length = 0
                    while current not in v_set:
                        length += 1
                        current = self.edge_to[current]
                    # add w1, length as the ancestor of v
                    self.first_source[w1] = length

        # BFS from w.
        # Change back self.marked and self.edge_to arrays
        for v in self.first_source.keys():
            self.marked[v] = False
            self.edge_to[v] = 0

        # make common_ancestor none and min_length large
        common_ancestor = -1
        min_length = float("inf")

        # better to use dict if w is large
        w_set = Set()
        # create queue to put w as source
        dist_from_src = Queue()
        # all ancestors of w
        indx = Stack()

        common_vert = False
        for vertex in w:
            w_set.add(vertex)
            # add vertex to queue
            dist_from_src.enqueue(vertex)
            # mark vertex as visited
            self.marked[vertex] = True
            indx.push(vertex)
            if vertex in v_set:
                common_vert = True
                break

        """if v and w share a common vertex
        then that vertex is the common ancestor
        with length 0
        """
        if common_vert:
            for vertex in w:
                self.marked[vertex] = False
            self.common_ancestor_col = indx.pop()
            self.min_length_col = 0
            return

        while not dist_from_src.is_empty():
            # take out item from the queue
            v1 = dist_from_src.pop()

            # check if v1 is an ancestor of v
            if v1 in self.first_source:
                length = 0
                # find the length frow w to w1
                current = v1
                while current not in w_set:
                    length += 1
                    current = self.edge_to[current]
                # check if the total length is smallest
                tot_length = length + self.first_source[v1]
                if tot_length < min_length:
                    common_ancestor = v1
                    min_length = tot_length

            # check for vertices adjacent to v1
            for w1 in G.adjacent_to(v1):
                # if not marked add them to queue
                if not self.marked[w1]:
                    self.marked[w1] = True
                    self.edge_to[w1] = v1
                    # add it to queue
                    dist_from_src.enqueue(w1)
                    indx.push(w1)

        # Edit again self.marked and self.edge_to
        for w in indx:
            self.marked[w] = False
            self.edge_to[w] = 0

        self.common_ancestor_col = common_ancestor
        if min_length == float("inf"):
            self.min_length_col = -1
        else:
            self.min_length_col = min_length


class KruskalMST(object):
    """Minimum Spanning Tree using Kruskal's
    Algorithm.
    """
    def __init__(self, G):
        """ Put edges in ascending order in a min PQ
        (acc. to weight). Delete the min edge, if its verticies
        are connected, ignore if not add edge to MST and
        union its verticies.
        """

        self.mst = Queue()
        self.pq = MinPQ()
        self.uf = UnionFind(G.get_v())

        # add all edges to PQ
        for edge in G.edges():
            self.pq.insert(edge)

        while (not self.pq.is_empty()) \
                and (self.mst.size() < G.get_v() - 1):

            e = self.pq.delete_min()
            v = e.either()
            w = e.other(v)

            if self.uf.are_connected(v, w):
                continue

            self.uf.union(v, w)
            self.mst.enqueue(e)

    def get_mst(self):
        return self.mst


