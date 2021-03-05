import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

start = 6
stop = 12

N_s = np.linspace(start, stop,  stop - start + 1)

for N in N_s:
    print()
    Lattice = Theory.Lattice(Parameters = [1,1], Size = [N,N,N,N], Spacing = [1,1,1,1])
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

    Lattice.save("Finite_Size/Test_4dim_N_"+str(N))