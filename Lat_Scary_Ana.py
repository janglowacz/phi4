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

    Meff_s.append(np.log(TP[1] / TP[0]))
    Meff_E_s.append(np.sqrt(np.square(TPE[1] / TP[1]) + np.square(TPE[0] / TP[0])))

Phi_mean_s = np.array(Phi_mean_s)
Phi_mean_E_s = np.array(Phi_mean_E_s)
Meff_s = np.array(Meff_s)
Meff_E_s = np.array(Meff_E_s)

# ====================================================================================

M_AVG = (Meff_s / np.square(Meff_E_s)).sum() / (1 / np.square(Meff_E_s)).sum()
M_ERR = np.sqrt(Meff_s.size / (1 / np.square(Meff_E_s)).sum())

plt.figure(figsize=(9,6))
plt.errorbar(J_s, Meff_s, yerr = Meff_E_s, fmt = "x", label = r"$m_\mathrm{eff}$", color = "C0", capsize = 3)
plt.hlines(M_AVG, J_s.min(), J_s.max(), label = r"average $m_\mathrm{eff}$", color = "C1")
plt.axhspan(M_AVG - M_ERR, M_AVG + M_ERR, alpha = 0.2 , color = "C1")
plt.legend(loc = "best")
plt.grid()
plt.xlabel(r"$J$")
plt.ylabel(r"$m_\mathrm{eff}$")
plt.savefig(f"Scary_plot_M{saveformat}")
plt.show()
plt.close()

# ====================================================================================

par, cov = so.curve_fit(func, Phi_mean_s, J_s, [1,1])

x = np.linspace(-3,3,1000)

plt.plot(Phi_mean_s, J_s, "X", label="measurement", color="C0")
plt.plot(x, func(x, *par), label="fit", color="C1")
plt.legend(loc="best")
plt.grid()
plt.xlabel(r"$<\phi>$")
plt.ylabel("J")
plt.savefig(f"Scary_plot_J{saveformat}")
plt.show()
plt.close()

# ====================================================================================

a, b = par
a_v, b_v = cov[0,0], cov[1,1]
Z, Z_E = np.square(M_AVG)/a, np.sqrt(np.square(np.square(M_AVG/a))*a_v+np.square(2*M_ERR*M_AVG/a))
L, L_E = b*np.square(Z), np.sqrt(np.square(np.square(Z))*b_v + np.square(b*2*Z*Z_E))

print("Results:")
print(f"Renormalized Mass M = {M_AVG} +/- {M_ERR}")
print(f"Renormalized Field Strength Z = {Z} +/- {Z_E}")
print(f"Renormalized Coupling Constant Lambda = {L} +/- {L_E}")