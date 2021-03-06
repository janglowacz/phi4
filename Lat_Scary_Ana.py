import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.optimize as so
import scipy.integrate as integrate

import Theory as Theory
import Utility

saveformat = '.pdf'

Tracker = Utility.Tracker()

verbose = True

def func(x, a, b):
    return a*x + b/6 * np.power(x,3)

def integrated_func(x, a, b):
    return a/2*np.power(x,2) + b/24*np.power(x,4)

J_s = np.linspace(-6,6,25)
N = 6

Phi_mean_s, Phi_mean_E_s = [], []

TP_s, TPE_s = [], []
Meff_s, Meff_E_s = [], []

for J in J_s:
    Lattice = Theory.Lattice()
    Lattice.load(f"Scary_Stuff/Scary_N_{N}_J_{J}")

    Phi_mean, Phi_mean_E = Lattice.Expectation_Value()
    Phi_mean_s.append(Phi_mean)
    Phi_mean_E_s.append(Phi_mean_E)

    TP, TPE = Lattice.two_Point_Corr_Full(Tracker=Tracker, Full=False)
    TP_s.append(TP)
    TPE_s.append(TPE)

    Meff_s.append(-np.log(TP[1]))
    Meff_E_s.append(TPE[1]/TP[1])

Phi_mean_s = np.array(Phi_mean_s)
Phi_mean_E_s = np.array(Phi_mean_E_s)
Meff_s = np.array(Meff_s)
Meff_E_s = np.array(Meff_E_s)

# ====================================================================================

M_AVG = Meff_s[12]
M_ERR = Meff_E_s[12]

# ====================================================================================

par, cov = so.curve_fit(func, Phi_mean_s, J_s, [1,1])

x = np.linspace(-3,3,1000)

plt.errorbar(Phi_mean_s, J_s, xerr = Phi_mean_E_s, fmt = "x", label="measurement", color="C0", capsize = 3)
plt.plot(x, func(x, *par), label="fit", color="C1")
plt.legend(loc="best")
plt.grid()
plt.xlabel(r"$\langle\phi\rangle$")
plt.ylabel("J")
plt.savefig(f"Scary_plot_J{saveformat}")
plt.show()
plt.close()

plt.plot(x, integrated_func(x, *par), label="integrated fit", color="C1")
plt.legend(loc="best")
plt.grid()
plt.xlabel(r"$\langle\phi\rangle$")
plt.ylabel("Effective Potential")
plt.savefig(f"Scary_plot_integral_J{saveformat}")
plt.show()
plt.close()

# ====================================================================================

a, b = par
a_v, b_v = cov[0,0], cov[1,1]
Z, Z_E = np.square(M_AVG)/a, np.sqrt(np.square(np.square(M_AVG/a))*a_v+np.square(2*M_ERR*M_AVG/a))
L, L_E = b*np.square(Z), np.sqrt(np.square(np.square(Z))*b_v + np.square(b*2*Z*Z_E))

print("Results:")
print(f"Renormalized Mass M = {M_AVG} +/- {M_ERR}")
print(f"Field Strength renormalization factor Z = {Z} +/- {Z_E}")
print(f"Renormalized Coupling Constant Lambda = {L} +/- {L_E}")