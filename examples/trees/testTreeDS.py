# from AlgoDS.treeDS import UnOrderedSeqST
from AlgoDS.treeDS import BinarySearchST

# st = UnOrderedSeqST()
st = BinarySearchST()
st['S'] = 0
st['E'] = 1
st['A'] = 2
st['R'] = 3
st['C'] = 4
st['H'] = 5
st['E'] = 6
st['X'] = 7
st['A'] = 8
st['M'] = 9
st['P'] = 10
st['L'] = 11
st['E'] = 12

# print "here"
print 's' in st
print st.size()

print st['E']

for key in st.keys():
    print key, st[key]
