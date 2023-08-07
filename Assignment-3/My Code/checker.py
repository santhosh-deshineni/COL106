import a3 as a3
import pickle
import time
print("Starting Checker")
f = open("testcase.bin", "rb")
test1 = pickle.load(f)
f = open("testcase1.bin", "rb")
test2 = pickle.load(f)
out1 = pickle.load(open("check.bin", "rb"))
out2 = pickle.load(open("check1.bin", "rb"))
t, t1, p = 0, 0, 0
print("Testing Easy Cases")
for i in test1:
    z, q = i[0], i[1]
    st = time.time()
    a = a3.PointDatabase(z)
    t += time.time()-st
    # print(t, t1)
    for i in q:
        st = time.time()
        m = a.searchNearby(i[0], i[1])
        t1 += time.time()-st
        m.sort()
        if not out1[p] == m:
            print(p, len(out1[p]), len(m), i[0], i[1])
        p += 1

print("Preprocessing Time (__init__): ", t, "Query RunTime:", t1)
t, t1, p = 0, 0, 0

print("Testing Hard Cases")
for i in test2:
    z, q = i[0], i[1]
    st = time.time()
    a = a3.PointDatabase(z)
    t += time.time()-st
    # print(t, t1)
    for i in q:
        st = time.time()
        m = a.searchNearby(i[0], i[1])
        t1 += time.time()-st
        m.sort()
        if not out2[p] == m:
            print(p, len(out2[p]), len(m), i[0], i[1], m)
        p += 1
print("Preprocessing Time (__init__): ", t, "Query RunTime:", t1)
