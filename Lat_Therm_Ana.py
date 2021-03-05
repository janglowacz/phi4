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

Settings1 = [[1,1,0.1],[0,1,0.1],[-1,1,0.1],[-2,1,0.1]]
Settings2 = [[-1,-1,0.1],[-1,1,0.1],[-1,1,0.1],[-1,2,0.1]]
Settings3 = [[1,-1,0.1],[1,0,0.1],[1,1,0.1],[1,2,0.1]]
Settings4 = [[-1,1,0],[-1,1,0.1],[-1,1,0.5],[-1,1,1]]
Settings5 = [[-1,0,0.1],[-1,5,0.1],[-1,25,0.1],[-1,125,0.1]]

Settings = [Settings1,Settings2,Settings3,Settings4,Settings5]

for j in range(len(Settings)):
    Lattice_s = []
    Phi_mean_s = []

    for Setting in Settings[j]:
        Lattice_s.append(Theory.Lattice())
        Lattice_s[-1].load("therm/Mu_"+str(Setting[0])+"_Lambda_"+str(Setting[1])+"_Offset_"+str(Setting[2]))

        Phi_mean = np.array([phi.mean() for phi in Lattice_s[-1].History])
        Phi_mean_s.append(np.abs(Phi_mean))

    plt.figure(figsize=(6,4))
    i = -1
    for Setting in Settings[j]:
        i += 1
        if j == 0:
            plt.plot(np.linspace(0,300,301), Phi_mean_s[i][:301], label = r"$\mu^2 = $"+str(Setting[0]))
        elif j == 1:
            plt.plot(np.linspace(0,300,301), Phi_mean_s[i][:301], label = r"$\lambda = $"+str(Setting[1]))
            plt.ylim(top=3.6, bottom=-0.1)
        elif j == 2:
            plt.plot(np.linspace(0,300,301), Phi_mean_s[i][:301], label = r"$\lambda = $"+str(Setting[1]))
        elif j == 3:
            plt.plot(np.linspace(0,300,301), Phi_mean_s[i][:301], label = r"$\phi_\mathrm{ini} = $"+str(Setting[2]))
        elif j == 4:
            plt.plot(np.linspace(0,300,301), Phi_mean_s[i][:301], label = r"$\lambda = $"+str(Setting[1]))
            plt.ylim(top=1.5, bottom=-0.1)
        else: raise Exception("Something went horribly wrong")
    plt.legend(loc = "best")
    plt.grid()
    plt.xlabel("Sweeps")
    plt.ylabel(r"$|\langle \phi \rangle|$")
    plt.savefig("Lat_therm_"+str(j+1)+".pdf")
    # plt.show()
    plt.close()