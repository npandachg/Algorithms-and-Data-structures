import fileinput

lines = fileinput.input()
# print lines
a = int(lines[0])
b = int(lines[1])
for line in lines:
    edges = line.split()
    print int(edges[0]), int(edges[1])
