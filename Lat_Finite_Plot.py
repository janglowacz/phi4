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

N_s = np.linspace(3,20,18)

dim = "4dim"

MEFF = np.load("Lat_Finite_"+dim+"_MEFF.npy")
MEFF_E = np.load("Lat_Finite_"+dim+"_MEFF_E.npy")

AVG = (MEFF / np.square(MEFF_E)).sum() / (1 / np.square(MEFF_E)).sum()
ERR = np.sqrt(MEFF.size / (1 / np.square(MEFF_E)).sum())

i = -1
for k in N_s:
    i+=1
    print(k, MEFF[i], MEFF_E[i] / MEFF[i])

plt.figure(figsize=(9,6))
plt.errorbar(N_s, MEFF, yerr = MEFF_E, fmt = "x", label = "values", color = "C0", capsize = 3)
plt.hlines(AVG, N_s.min(), N_s.max(), label = "average", color = "C1")
plt.axhspan(AVG - ERR, AVG + ERR, alpha = 0.2 , color = "C1")
plt.legend(loc = "best")
plt.grid()
plt.xlabel(r"$N$")
plt.ylabel(r"$m_\mathrm{eff}$")
plt.savefig("Lat_Finite_"+dim+".pdf")
plt.show()
plt.close()

plt.figure(figsize=(9,6))
plt.plot(N_s, MEFF_E, ".", label = "values", color = "C0")
plt.hlines(ERR, N_s.min(), N_s.max(), label = "average", color = "C1")
plt.legend(loc = "best")
plt.yscale("log")
plt.grid()
plt.xlabel(r"$N$")
plt.ylabel(r"$\sigma_{m_\mathrm{eff}}$")
plt.savefig("Lat_Finite_"+dim+"_err.pdf")
plt.show()
plt.close()