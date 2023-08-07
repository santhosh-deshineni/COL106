import pickle
import random
l = []
for _ in range(3):
    t = 10**5
    x = [i for i in range(-t, t+1)]
    y = [i for i in range(2*t+1)]
    z = []
    print("Step 1")
    for i in range(-t, t+1):
        m = len(x)
        a, b = random.randint(0, m-1), random.randint(0, m-1)
        z.append((x[a], y[b]))
        x[a] = x[-1]
        y[b] = y[-1]
        x.pop()
        y.pop()

    print("Step 2")
    q = []
    for i in range(10**5):
        a, b = random.randint(-t-5000, t+5000), random.randint(-t-5000, t+5000)
        d = random.randint(0, 500)
        q.append([(a, b), d])
    for i in range(10**3):
        a, b = random.randint(-t-5000, t+5000), random.randint(-t-50000, 50000)
        d = random.randint(500, 50000)
        q.append([(a, b), d])
    for i in range(10**5):
        a = random.randint(0, len(z)-1)
        d = random.randint(0, 500)
        q.append([z[a], d])

    l.append([z, q])

for _ in range(1):
    t = 10**6
    x = [i for i in range(-t, t+1)]
    y = [i for i in range(-t, t+1)]
    z = []
    print("Step 1")
    for i in range(-t, t+1):
        m = len(x)
        a, b = random.randint(0, m-1), random.randint(0, m-1)
        z.append((x[a], y[b]))
        x[a] = x[-1]
        y[b] = y[-1]
        x.pop()
        y.pop()

    print("Step 2")
    q = []
    for i in range(5*10**5):
        a, b = random.randint(-t-5000, t+5000), random.randint(-t-5000, t+5000)
        d = random.randint(0, 5000)
        q.append([(a, b), d])
    for i in range(5*10**3):
        a, b = random.randint(-t-5000, t+5000), random.randint(-t-50000, 50000)
        d = random.randint(5000, 50000)
        q.append([(a, b), d])
    for i in range(5*10**5):
        a = random.randint(0, len(z)-1)
        d = random.randint(0, 5000)
        q.append([z[a], d])
    l.append([z, q])

f = open("testcase1.bin", "wb")
pickle.dump(l, f)
