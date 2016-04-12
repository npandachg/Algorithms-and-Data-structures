from AlgoDS.graphs import DirectedGraph
from AlgoDS.graphs import Degrees
from AlgoDS.graphs import DetectCycle
from AlgoDS.graphs import ShortestAncestralPath
from AlgoDS.graphs import GraphReadError
from AlgoDS.basicDS import Stack
from collections import defaultdict
import csv
import numpy as np
from nose.tools import *


class WordNet(object):
    """WordNet class : words are grouped as synonyms and looks
    at the semantic relationships between them.

    API :
    # constructor that takes two file names
    WordNet(syn_file, hyper_file)
    # returns all WordNet Nouns
    get_nouns()
    # is the word a WordNet noun
    is_noun(word)
    # distance between noun_a, noun_b
    distance(noun_a, noun_b)
    # shortest ancestral path between noun_a, noun_b
    sap(noun_a, noun_b)
    """

    def __init__(self, syn_file, hyper_file):
        self.nouns = defaultdict(Stack)  # multimap word -> synset ids
        self.root = None

        # read the synsets file and populate the dict of nouns
        with open(syn_file, 'r') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',')
            num_vert = 0
            for row in file_reader:
                num_vert += 1
                for key in row[1].split():
                    self.nouns[key].push(int(row[0]))

        # id : synset id -> words
        self.id = np.empty([num_vert], dtype=object)
        for i in range(num_vert):
            self.id[i] = Stack()

        for key in self.nouns.keys():
            indx_arr = self.nouns[key]
            for indx in indx_arr:
                self.id[indx].push(key)

        # construct the graph. Read edges from hyper_file
        self.G = DirectedGraph(num_vert)

        with open(hyper_file, 'r') as csvfile2:
            file_reader = csv.reader(csvfile2, delimiter=',')
            for row in file_reader:
                v = int(row[0])
                for vertex in row[1:]:
                    w = int(vertex)
                    self.G.add_edge(v, w)

        # check if Graph is Acyclic
        dag = DetectCycle(self.G)
        if dag.has_cycle():
            raise GraphReadError("Graph is not a DAG")
        else:
            deg = Degrees(self.G)
            sinks = deg.get_sinks()

            if sinks.size() > 1:
                raise GraphReadError("DAG has more than one root")
            else:
                self.root = sinks.pop()

        # construct the SAP
        self.sap_obj = ShortestAncestralPath(self.G)

    def get_nouns(self):
        return self.nouns.keys()

    def is_noun(self, word):
        return word in self.nouns

    def distance(self, noun_a, noun_b):
        if (noun_a not in self.nouns) or (noun_b not in self.nouns):
            raise GraphReadError("nouns are not in WordNet")

        return self.sap_obj.length(self.nouns[noun_a],
                                   self.nouns[noun_b])

    def sap(self, noun_a, noun_b):
        if (noun_a not in self.nouns) or (noun_b not in self.nouns):
            raise GraphReadError("nouns are not in WordNet")

        return self.sap_obj.ancestor(self.nouns[noun_a],
                                     self.nouns[noun_b])


class Outcast(object):
    """outcast class: which word is least related to a given
    set of words in a wordNet
    """

    def __init__(self, word_net):
        self.word_net = word_net

    def outcast(self, nouns):
        """ given a list of nouns, find the outcast """
        max_length = -1

        for i in range(len(nouns)):
            d = self._get_dist(nouns, i)
            if d > max_length:
                max_length = d
                max_indx = i

        return nouns[max_indx]

    def _get_dist(self, nouns, i):
        temp_dist = 0
        for noun in nouns:
            if noun == nouns[i]:
                d = 0
            else:
                d = self.word_net.distance(noun, nouns[i])
            temp_dist += d

        return temp_dist

synsets_file = "/Users/nishpan/PyProjects/AlgoDS/examples/\
graphs/wordnet/synsets.txt"
hypernyms_file = "/Users/nishpan/PyProjects/AlgoDS/examples/\
graphs/wordnet/hypernyms.txt"

test = WordNet(synsets_file, hypernyms_file)
outcast1 = Outcast(test)
print "Here"
print "verticies :", test.G.get_v()
print "edges :", test.G.get_e()
print "num nouns:", len(test.nouns.keys())
print "root is :", test.root, test.id[test.root].pop()
print "worm in synset", test.is_noun("worm")
print "all synsets of word", test.nouns["word"]
print "all synsets of worm", test.nouns["worm"]


for syn_id in test.nouns["worm"]:
    print syn_id,
    for word in test.id[syn_id]:
        print word,
    print "\n"

print "distance from worm and bird", test.distance("worm", "bird")
for word in test.id[test.sap("worm", "bird")]:
    print word,

print "\n"
nouns_1 = ["horse", "zebra", "cat", "bear", "table"]
print outcast1.outcast(nouns_1)
print "\n"
nouns_2 = ["water", "soda", "bed", "orange", "juice", "milk",
           "apple_juice", "tea", "coffee"]
print outcast1.outcast(nouns_2)
print "\n"
nouns_3 = ["apple", "pear", "peach", "banana", "lime", "lemon",
           "blueberry", "strawberry", "mango", "watermelon",
           "potato"]
print outcast1.outcast(nouns_3)
