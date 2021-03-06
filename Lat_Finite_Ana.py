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

    TP, TPE = Lattice_s[-1].two_Point_Corr_Full(Tracker = Tracker, Full = False)

    Meff_s.append(-np.log(TP[1]))
    Meff_E_s.append(TPE[1]/TP[1])

AVG = (Meff_s / np.square(Meff_E_s)).sum() / (1 / np.square(Meff_E_s)).sum()
ERR = np.sqrt(Meff_s.size / (1 / np.square(Meff_E_s)).sum())

np.save("Lat_Finite_"+dim+"_MEFF",Meff_s)
np.save("Lat_Finite_"+dim+"_MEFF_E",Meff_E_s)