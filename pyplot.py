import matplotlib.pyplot as plt

def getAlldata(entries):
    res = []
    for i in range(len(entries[0])):
        res.append([])
    for entry in entries:
        for i in range(len(res)):
            res[i].append(entry[i])
    return res

def getDifference(a, b):
    res = []
    for i in range(len(a)):
        res.append(int(a[i]) - int(b[i]))
    return res


file = open("testfile.txt", "r")

all_rows = file.read().splitlines()

all_entries = []

for row in all_rows:
    entry = row.split()
    all_entries.append(entry)

all_data = getAlldata(all_entries)

t = all_data[0]
ra0 = all_data[1]
a0 = all_data[2]
ra1 = all_data[3]
a1 = all_data[4]

plt.figure(1)
plt.subplot(211)
plt.plot(t, a0)
plt.plot(t, ra0)
plt.legend(['angle', 'reference_angle'], loc='upper left')
plt.ylabel('motor 0')
plt.xlabel('time')


plt.subplot(212)
plt.plot(t, a1)
plt.plot(t, ra1)
plt.legend(['angle', 'reference_angle'], loc='upper left')
plt.ylabel('motor 1')
plt.xlabel('time')

plt.figure(2)
plt.plot(t, getDifference(ra0, a0))
plt.plot(t, getDifference(ra1, a1))
plt.legend(['motor 0', 'motor 1'], loc='upper left')
plt.xlabel('time')



plt.show()
