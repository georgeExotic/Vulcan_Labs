from time import time
d_motion1 = 5 #seconds

start = time() # returns the current time
t = time() - start

while t < d_motion1:

    t = time() - start 
    print("do this")
print("done")