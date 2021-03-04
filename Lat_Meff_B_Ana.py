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

M_squared_s = np.linspace(-3,1,17)

Lambda_s = [1,10]

MEFF_S = []
MEFF_E_S = []

for Lambda in Lambda_s:
    Lattice_s = []
    TP_s, TPE_s = [], []

    Meff_s, Meff_E_s = [], []

    for M_squared in M_squared_s:
        Lattice_s.append(Theory.Lattice())
        Lattice_s[-1].load("Meff_B/Mu_"+str(M_squared)+"_Lambda_"+str(Lambda))

        TP, TPE = Lattice_s[-1].two_Point_Corr_Full(Tracker = Tracker)
        TP_s.append(TP)
        TPE_s.append(TPE)

        Meff_s.append(np.log(TP[:-1] / TP[1:]))
        Meff_E_s.append(np.sqrt(np.square(TPE[:-1] / TP[:-1]) + np.square(TPE[1:] / TP[1:])))

    AVG_Range = 1

    MEFF = np.array([M[:AVG_Range].mean() for M in Meff_s])
    MEFF_E = np.array([np.sqrt(np.square(M_E[:AVG_Range]).mean()) for M_E in Meff_E_s])

    MEFF_S.append(MEFF)
    MEFF_E_S.append(MEFF_E)

plt.figure(figsize=(9,6))
i = -1
for Lambda in Lambda_s:
    i+=1
    plt.errorbar(M_squared_s, MEFF_S[i], yerr = MEFF_E[i], fmt = "x", label = r"$\lambda = $"+str(Lambda), capsize = 3)
plt.legend(loc = "best")
plt.grid()
plt.xlabel(r"$\mu^2$")
plt.ylabel(r"$m_\mathrm{eff}$")
plt.savefig("Lat_Meff_B.pdf")
plt.show()
plt.close()