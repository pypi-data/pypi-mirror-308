from drawzero import *

circle('red', (500, 500), 50)


print('a b c d')
for a in range(2):
    for b in range(2):
        for c in range(2):
            for d in range(2):
                if (not c) and ((not a) <= (not d) <= (not b)):
                    print(a, b, c, d)
