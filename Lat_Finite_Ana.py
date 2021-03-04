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

Lattice_s = []
TP_s, TPE_s = [], []

Meff_s, Meff_E_s = [], []

for N in N_s:
    Lattice_s.append(Theory.Lattice())
    Lattice_s[-1].load("Finite_Size/Test_"+dim+"_N_"+str(N))

    TP, TPE = Lattice_s[-1].two_Point_Corr_Full(Tracker = Tracker)
    TP_s.append(TP)
    TPE_s.append(TPE)

    Meff_s.append(np.log(TP[:-1] / TP[1:]))
    Meff_E_s.append(np.sqrt(np.square(TPE[:-1] / TP[:-1]) + np.square(TPE[1:] / TP[1:])))

AVG_Range = 1

MEFF = np.array([M[:AVG_Range].mean() for M in Meff_s])
MEFF_E = np.array([np.sqrt(np.square(M_E[:AVG_Range]).mean()) for M_E in Meff_E_s])

AVG = (MEFF / np.square(MEFF_E)).sum() / (1 / np.square(MEFF_E)).sum()
ERR = np.sqrt(MEFF.size / (1 / np.square(MEFF_E)).sum())

np.save("Lat_Finite_"+dim+"_MEFF",MEFF)
np.save("Lat_Finite_"+dim+"_MEFF_E",MEFF_E)