import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

M_squared_s = np.linspace(-7,3,41)

Lambda = 50

for M_squared in M_squared_s:
    print()
    print("Lambda:", Lambda)
    Lattice = Theory.Lattice(Parameters = [M_squared, Lambda], Size = [10,10,10,10], Spacing = [1,1,1,1])
    Lattice.History = []
    Lattice.Phi = np.ones(Lattice.Shape)*0.1

    Tracker = Utility.Tracker()

    Thermalization = 50
    Sweeps = 50

    Steps = 4

    print("Size:",Lattice.Size)
    print("Spacing:",Lattice.Spacing)
    print("Shape:",Lattice.Shape)


    print("Thermalization:")
    Tracker.START()
    for k in range(Thermalization):
        Tracker.FLUSH(k, Thermalization)
        Lattice.Sweep(Steps = Steps)
    Tracker.FLUSH_Final(Thermalization, Thermalization)
    print()

    print("Sweeps:")
    Tracker.START()
    for k in range(Sweeps):
        Tracker.FLUSH(k, Sweeps)
        Lattice.Sweep(Steps = Steps, Save = True)
    Tracker.FLUSH_Final(Sweeps, Sweeps)
    print()

    print("Acceptance:",Lattice.Accepted/Lattice.Tried)

    Lattice.save("Meff_B/Mu_"+str(M_squared)+"_Lambda_"+str(Lambda))