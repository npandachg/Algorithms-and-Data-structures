from nose.tools import *
from AlgoDS.graphs import Graph
from AlgoDS.graphs import DFS
from AlgoDS.graphs import BFS
from AlgoDS.graphs import ConnectedComponents
from AlgoDS.graphs import DirectedGraph
from AlgoDS.graphs import DetectCycle
from AlgoDS.graphs import TopologicalOrder
from AlgoDS.graphs import Degrees
from AlgoDS.graphs import ShortestAncestralPath
from AlgoDS.graphs import StrongCC
from AlgoDS.basicDS import Queue
from AlgoDS.basicDS import Bag
from AlgoDS.basicDS import Stack
import numpy as np
import fileinput


def test_graphs_Graph():
    """ test the constructor """
    print "test constructor for undirected Graph\n"
    G = Graph.read_from_file(fileinput.input("tinyG.txt"))
    print G


def test_graphs_DFS():
    """ test the DFS class """
    print "test DFS\n"
    G = Graph.read_from_file(fileinput.input("tinyG.txt"))
    source = []
    source.append(0)
    source.append(9)
    df = DFS(G, source)
    # print df.marked
    paths = df.path_to(3)
    if paths is None:
        print "No path to source"
    else:
        print "Path from source: "
        for v in paths:
            print str(v) + " - ",


def test_graphs_BFS():
    """ test the BFS class """
    print "test BFS\n"
    G = Graph.read_from_file(fileinput.input("tinyG.txt"))
    source = []
    source.append(0)
    source.append(1)
    bf = BFS(G, source)
    # print bf.marked
    paths = bf.path_to(3)
    if paths is None:
        print "No path to source"
    else:
        print "Path from source: "
        for v in paths:
            print str(v) + " - ",

    print "\n"


def test_graphs_CC():
    """ test the Connected Components Class """
    print "test ConnectedComponents\n"
    G = Graph.read_from_file(fileinput.input("tinyG.txt"))
    cc = ConnectedComponents(G)

    print cc.get_count()
    print cc.are_connected(0, 9)


def test_graphs_DirectedGraph():
    """ test the constructor for DiG"""
    print " test DirectedGraph\n"
    G = DirectedGraph.read_from_file(fileinput.input("tinyDG.txt"))
    print G
    R = G.reverse()
    print R
    s = []
    s.append(0)
    ddfs = DFS(G, s)
    for v in ddfs.reachable_from(s[0]):
        print v


def test_graphs_DetectCycle():
    """ test detect cycle method """

    print " DetectCycle\n"
    G = DirectedGraph.read_from_file(fileinput.input("tinyDG.txt"))
    dcycle = DetectCycle(G)

    if dcycle.get_cycle() is not None:
        for v in dcycle.get_cycle():
            print v


def test_graphs_TopologicalOrder():
    """ test Topological order in DAG """

    print " TopologicalOrder\n"
    G = DirectedGraph.read_from_file(fileinput.input("digraph2.txt"))
    top_order = TopologicalOrder(G)
    for v in top_order.get_order():
        print v


def test_graphs_SCC():
    """ test StrongCC """
    print "StrongCC\n"

    G = DirectedGraph.read_from_file(fileinput.input("tinyDG.txt"))
    scc = StrongCC(G)
    print scc.get_count()
    components = np.empty([scc.get_count()], dtype=object)

    for index in range(scc.get_count()):
        components[index] = Queue()

    for v in range(G.get_v()):
        id_v = scc.get_id(v)
        components[id_v].enqueue(v)

    for index in range(scc.get_count()):
        print "\n"
        for v in components[index]:
            print v,


def test_graphs_Degrees():
    """ test the Degrees class """
    print "Degrees\n"
    G = DirectedGraph.read_from_file(fileinput.input("tinyDAG.txt"))

    deg = Degrees(G)

    for v in range(G.get_v()):
        print v, deg.get_indegree(v), deg.get_outdegree(v)


def test_graphs_SAP():
    """ test the ShortestAncestralPath class """
    print "SAP\n"
    G = DirectedGraph.read_from_file(fileinput.input("digraph1.txt"))
    sap = ShortestAncestralPath(G)
    print "3 ", "1 ", "length = ", sap.length(3, 1)
    print "3 ", "1 ", "ancestor = ", sap.ancestor(3, 1)
    print "3 ", "11 ", "length = ", sap.length(3, 11)
    print "3 ", "11 ", "ancestor = ", sap.ancestor(3, 11)
    print "9 ", "12 ", "length = ", sap.length(9, 12)
    print "9 ", "12 ", "ancestor = ", sap.ancestor(9, 12)
    print "7 ", "2 ", "length = ", sap.length(7, 2)
    print "7 ", "2 ", "ancestor = ", sap.ancestor(7, 2)
    print "1 ", "6 ", "length = ", sap.length(1, 6)
    print "1 ", "6 ", "ancestor = ", sap.ancestor(1, 6)
    v1 = Stack()
    v1.push(3)
    v1.push(7)
    v1.push(8)
    v2 = Stack()
    v2.push(10)
    v2.push(9)
    v2.push(11)
    v2.push(12)
    v3 = Bag()
    v3.add(4)
    v3.add(1)
    print "v1 :3,7,8 ", "v2 : 10,9,11,12 ", "length = ", sap.length(v1, v2)
    print "v1 :3,7,8 ", "v2 : 10,9,11,12 ", "ancestor = ", sap.ancestor(v1, v2)
    print "v1 :3,7,8 ", "v3 : 4, 1 ", "length = ", sap.length(v1, v3)
    print "v1 :3,7,8 ", "v2 : 4, 1 ", "ancestor = ", sap.ancestor(v1, v3)
    G_2 = DirectedGraph.read_from_file(fileinput.input("digraph2.txt"))
    sap2 = ShortestAncestralPath(G_2)
    print "1 ", "5 ", "length = ", sap2.length(2, 1)
    print "1 ", "5 ", "ancestor = ", sap2.ancestor(2, 1)



















