import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.optimize as so
import scipy.special as sx

import Theory as Theory
import Utility

saveformat = '.pdf'

Tracker = Utility.Tracker()

verbose = True

M_squared_s = np.linspace(-7,3,41)

lin = np.linspace(M_squared_s.min(), M_squared_s.max(), 1000)

Lambda_s = [10,20,30,40,50]

MEFF_S = []
MEFF_E_S = []

Par_s = []
Cov_s = []

def startpars(L):
    return [1, 1, -0.056*L-0.033, -0.00567*L+0.447]

def fitfunc(x, a, b, c, d):
    RET = np.zeros(len(np.array(x)))
    RET[x<c] = a * np.exp( b * x[x<c] )
    RET[x>=c] = a * np.exp( b * c ) + ( x[x>=c] - c ) * d
    return RET

for Lambda in Lambda_s:
    Lattice_s = []
    TP_s, TPE_s = [], []

    Meff_s, Meff_E_s = [], []

    for M_squared in M_squared_s:
        Lattice_s.append(Theory.Lattice())
        Lattice_s[-1].load("Meff_B/Mu_"+str(M_squared)+"_Lambda_"+str(Lambda))

        TP, TPE = Lattice_s[-1].two_Point_Corr_Full(Tracker = Tracker, Full = False)

        Meff_s.append(-np.log(TP[1]))
        Meff_E_s.append(TPE[1]/TP[1])

    MEFF_S.append(Meff_s)
    MEFF_E_S.append(Meff_E_s)

    Spars = startpars(Lambda)
    par, cov = so.curve_fit(fitfunc, M_squared_s, Meff_s, Spars, sigma = Meff_E_s, absolute_sigma=True)
    Par_s.append(par)
    Cov_s.append(cov)

plt.figure(figsize=(9,6))

i = -1
for Lambda in Lambda_s:
    i+=1
    plt.errorbar(M_squared_s, MEFF_S[i], yerr = MEFF_E_S[i], fmt = "x", label = r"$\lambda = $"+str(Lambda), capsize = 3, color = "C"+str(i))
    plt.plot(lin, fitfunc(lin, *Par_s[i]), color = "C"+str(i), alpha = 0.5)
    Spars = startpars(Lambda)
    # plt.plot(lin, fitfunc(lin,*Spars),"--", color = "C"+str(i), alpha = 0.5)
    X = np.sum(np.square((MEFF_S[i] - fitfunc(M_squared_s, *Par_s[i]))/MEFF_E_S[i]))
    print()
    print(Lambda)
    print(startpars(Lambda))
    print(Par_s[i])
    print(np.sqrt(Cov_s[i].diagonal()))
    print(X, M_squared_s.size - 4, X / (M_squared_s.size - 4))
plt.legend(loc = "best")
plt.grid()
plt.xlabel(r"$\mu^2$")
plt.ylabel(r"$m_\mathrm{eff}$")
plt.savefig("Lat_Meff_B.pdf")
plt.show()
plt.close()