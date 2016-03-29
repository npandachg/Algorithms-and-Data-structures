from nose.tools import *
from AlgoDS.graphs import Graph
import fileinput


def test_graphs_Graph():
    """ test the constructor """
    G = Graph(fileinput.input("tinyG.txt"))
    print G
