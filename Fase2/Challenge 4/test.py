import numpy as np

with open("input4.txt", 'r') as f:
  lines = f.readlines()

lines = np.array([[ int(x.replace('x', '-1')) for x in line.replace('\n', '').split(' ') ] for line in lines])
x = 2300
y = 2300
s = 10
quad = lines[y:y+s, x:x+s] + 1

print(quad)
'''
[0 0 0 0 0 0 2 0 0 0]
[0 1 0 0 0 1 2 0 0 2]
[0 0 0 2 0 0 0 0 1 0]
[0 2 2 0 0 2 0 2 0 0]
[2 0 0 0 0 1 0 0 2 0]
[0 0 0 2 0 0 0 2 1 0]
[0 2 0 0 0 0 2 2 0 0]
[2 0 0 0 0 0 0 0 2 0]
[0 0 2 0 0 2 0 2 2 0]
[0 2 0 0 2 0 0 0 0 0]
'''