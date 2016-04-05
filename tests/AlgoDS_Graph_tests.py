from nose.tools import *
from AlgoDS.graphs import Graph
from AlgoDS.graphs import DFS
from AlgoDS.graphs import BFS
from AlgoDS.graphs import ConnectedComponents
from AlgoDS.graphs import DirectedGraph
from AlgoDS.graphs import DetectCycle
from AlgoDS.graphs import TopologicalOrder
import fileinput


def test_graphs_Graph():
    """ test the constructor """
    G = Graph.read_from_file(fileinput.input("tinyG.txt"))
    print G


def test_graphs_DFS():
    """ test the DFS class """
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
    G = Graph.read_from_file(fileinput.input("tinyG.txt"))
    cc = ConnectedComponents(G)

    print cc.get_count()
    print cc.are_connected(0, 9)

    cc2 = ConnectedComponents(G, "BFS")
    print cc2.get_count()
    print cc2.are_connected(0, 9)


def test_graphs_DirectedGraph():
    """ test the constructor for DiG"""
    G = DirectedGraph.read_from_file(fileinput.input("tinyDG.txt"))
    # G = Graph(fileinput.input("tinyG.txt"))
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
    G = DirectedGraph.read_from_file(fileinput.input("tinyDG.txt"))
    dcycle = DetectCycle(G)

    if dcycle.get_cycle() is not None:
        for v in dcycle.get_cycle():
            print v


def test_graphs_TopologicalOrder():
    """ test Topological order in DAG """

    G = DirectedGraph.read_from_file(fileinput.input("tinyDAG.txt"))
    t_sort = TopologicalOrder(G, "post")
    for v in t_sort.get_order():
        print v













