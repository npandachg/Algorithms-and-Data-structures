# from basicSort import Selection
# from basicSort import Insertion
from basicSort import MergeSort

a = []
a.append("M")
a.append("E")
a.append("R")
a.append("G")
a.append("E")
a.append("S")
a.append("O")
a.append("R")
a.append("T")
a.append("E")
a.append("X")
a.append("A")
a.append("M")
a.append("P")
a.append("L")
a.append("E")
a.append("S")

# Selection.sort(a)
MergeSort.sort(a)

for elem in a:
    print elem
