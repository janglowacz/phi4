import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

M_squared_s = np.linspace(-3,1,17)

Lambda = 10

for M_squared in M_squared_s:
    print()
    Lattice = Theory.Lattice(Parameters = [M_squared, Lambda], Size = [6,6,6,6], Spacing = [1,1,1,1])
    Lattice.History = []
    Lattice.Phi = np.ones(Lattice.Shape)*0

    Tracker = Utility.Tracker()

    Thermalization = 20
    Sweeps = 50

    Steps = 5
    Sweep_Dmax = np.sqrt(Lattice.Spacing[0])

    print("Size:",Lattice.Size)
    print("Spacing:",Lattice.Spacing)
    print("Shape:",Lattice.Shape)


    print("Thermalization:")
    Tracker.START()
    for k in range(Thermalization):
        Tracker.FLUSH(k, Thermalization)
        Lattice.Sweep(Sweep_Dmax, Steps = Steps)
    Tracker.FLUSH_Final(Thermalization, Thermalization)
    print()

    print("Sweeps:")
    Tracker.START()
    for k in range(Sweeps):
        Tracker.FLUSH(k, Sweeps)
        Lattice.Sweep(Sweep_Dmax, Steps = Steps, Save = True)
    Tracker.FLUSH_Final(Sweeps, Sweeps)
    print()

    print("Acceptance:",Lattice.Accepted/Lattice.Tried)

    Lattice.save("Meff_B/Mu_"+str(M_squared)+"_Lambda_"+str(Lambda))