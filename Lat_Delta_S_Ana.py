import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.optimize as so

import Theory as Theory
import Utility

Tracker = Utility.Tracker()

Lattice1 = Theory.Lattice()
Lattice2 = Theory.Lattice()
Lattice3 = Theory.Lattice()

Lattice1.load("Comparison/Type1")
Lattice2.load("Comparison/Type2")
Lattice3.load("Comparison/Type3")

Lattice2.calc_crazy_stuff()
Lattice3.calc_other_stuff()

t_s = np.linspace(0, Lattice1.Size[0]//2, Lattice1.Shape[0]//2+1)

TPC1 = np.zeros([t_s.size, len(Lattice1.History)])
TPC2 = np.zeros([t_s.size, len(Lattice1.History)])
TPC3 = np.zeros([t_s.size, len(Lattice1.History)])

runs = len(Lattice1.History)*len(t_s)
Tracker.START()
for i in range(len(Lattice1.History)):
    for t in range(len(t_s)):
        Tracker.FLUSH(t+(i*len(t_s)), runs)
        TPC1[t, i] = Lattice1.two_Point_Average(t, phi = Lattice1.History[i])
        TPC2[t, i] = Lattice2.two_Point_Average(t, phi = Lattice2.History[i])
        TPC3[t, i] = Lattice3.two_Point_Average(t, phi = Lattice3.History[i])

TP1 = TPC1.mean(axis = 1)
TP1 = TP1 / TPC1.mean(axis = 1)[0]
 
TPE1 = np.array([Utility.bootstrap(TPC1[t,:], 10000) for t in range(len(t_s))])
TPE1 = TPE1 / TPC1.mean(axis = 1)[0]

TP2 = TPC2.mean(axis = 1)
TP2 = TP2 / TPC2.mean(axis = 1)[0]
 
TPE2 = np.array([Utility.bootstrap(TPC2[t,:], 10000) for t in range(len(t_s))])
TPE2 = TPE2 / TPC2.mean(axis = 1)[0]

TP3 = TPC3.mean(axis = 1)
TP3 = TP3 / TPC3.mean(axis = 1)[0]
 
TPE3 = np.array([Utility.bootstrap(TPC3[t,:], 10000) for t in range(len(t_s))])
TPE3 = TPE3 / TPC3.mean(axis = 1)[0]


plt.figure(figsize=(9,6))

plt.errorbar(t_s, TP1, yerr = TPE1, fmt = "x", label="Method 1", capsize=3)
plt.errorbar(t_s, TP2, yerr = TPE2, fmt = "x", label="Method 2", capsize=3)
plt.errorbar(t_s, TP3, yerr = TPE3, fmt = "x", label="Method 3", capsize=3)

plt.legend(loc="best")
plt.grid()
plt.xlabel("t")
plt.ylabel("two point corrleator")
plt.show()
plt.close()