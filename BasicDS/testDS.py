from basicDS import Stack
from basicDS import Queue


s = Stack()


s.push("Hello")
s.push("World")

for item in s:
    print item

q = Queue()
q.enqueue("Hello")
q.enqueue("World")

for item in q:
    print item
