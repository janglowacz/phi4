import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.optimize as so

import Theory as Theory
import Utility

saveformat = '.pdf'

Tracker = Utility.Tracker()

verbose = True

Lattice = Theory.Lattice()
Lattice.load("Corr/Corr")

t_s = np.linspace(0, Lattice.Size[0]//2, Lattice.Shape[0]//2+1)
TPC = np.zeros([t_s.size, len(Lattice.History)])

runs = len(Lattice.History)*len(t_s)
Tracker.START()
for i in range(len(Lattice.History)):
    for t in range(len(t_s)):
        Tracker.FLUSH(t+(i*len(t_s)), runs)
        TPC[t, i] = Lattice.two_Point_Average(t, phi = Lattice.History[i])
Tracker.FLUSH_Final(runs, runs)

TP = TPC.mean(axis = 1)
TP = TP / TPC.mean(axis = 1)[0]
 
TPE = np.array([Utility.bootstrap(TPC[t,:], 10000) for t in range(len(t_s))])
TPE = TPE / TPC.mean(axis = 1)[0]

def func(x,a):
    return np.exp(-a * x)

plt.errorbar(t_s, TP, yerr = TPE, fmt = ".", label="two_point_correlators", color="C0")

par, cov = so.curve_fit(func, t_s, TP, [1], sigma = TPE, absolute_sigma=True)

X = np.sum(np.square((TP - func(t_s,par))/TPE))
print()
print("Chi Squared:",X)
print("n.d.f.:",t_s.size - 1)
print("Chi Squared over n.d.f.:",X / (t_s.size - 1))

lin = np.linspace(0,Lattice.Size[0]//2,1000)

plt.plot(lin, [func(x, par) for x in lin], label="test", color="C1")
plt.legend(loc="best")
plt.grid()
plt.xlabel("t")
plt.ylabel("two point corrleator")
plt.show()
plt.close()