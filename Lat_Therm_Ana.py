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

Settings = [[1,1,0],[-1,1,0],[-1,1,0.1]]

Lattice_s = []
Phi_mean_s = []

for Setting in Settings:
    Lattice_s.append(Theory.Lattice())
    Lattice_s[-1].load("therm/Mu_"+str(Setting[0])+"_Lambda_"+str(Setting[1])+"_Offset_"+str(Setting[2]))

    Phi_mean = np.array([phi.mean() for phi in Lattice_s[-1].History])
    Phi_mean_s.append(np.abs(Phi_mean))

plt.figure(figsize=(9,6))
i = -1
for Setting in Settings:
    i += 1
    plt.plot(np.linspace(0,Phi_mean_s[0].size, Phi_mean_s[i].size), Phi_mean_s[i], label = r"$\mu = $"+str(Setting[0])+r", $\lambda = $"+str(Setting[1])+", initial = "+str(Setting[2]))
plt.legend(loc = "best")
plt.grid()
plt.xlabel("Sweeps")
plt.ylabel(r"$|\langle \phi \rangle|$")
plt.savefig("Lat_2.pdf")
plt.show()
plt.close()