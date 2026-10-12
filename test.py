import time, random

start = time.perf_counter()

tmp = []

pminu = 250000
phour = pminu*60
pdate = phour*24
pmont = pdate*30
ptotl = pmont*9

print(f"{ptotl/1000000000}GB")

for _ in range (pminu):
    tmp.append(random.randint(-1000, 1000))
    
end = time.perf_counter()

print(end-start)

print((end-start)*60*24*30*9)