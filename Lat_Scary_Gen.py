import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

N = 6

start = -6
stop = +6
steps = 25

J_s = np.linspace(start,stop,steps)

for J in J_s:
    print()
    Lattice = Theory.Lattice(Parameters = [-1,2], Size = [N,N,N,N], Spacing = [1,1,1,1])
    Lattice.History = []
    Lattice.Phi = np.ones(Lattice.Shape)*0

    Tracker = Utility.Tracker()

    Thermalization = 50
    Sweeps = 100

    Steps = 4

    print("Size:",Lattice.Size)
    print("Spacing:",Lattice.Spacing)
    print("Shape:",Lattice.Shape)
    print()


    print("Thermalization:")
    Tracker.START()
    for k in range(Thermalization):
        Tracker.FLUSH(k, Thermalization)
        Lattice.Sweep(J = J, Steps = Steps)
    Tracker.FLUSH_Final(Thermalization, Thermalization)
    print()

    print("Sweeps:")
    Tracker.START()
    for k in range(Sweeps):
        Tracker.FLUSH(k, Sweeps)
        Lattice.Sweep(J = J, Steps = Steps, Save = True)
    Tracker.FLUSH_Final(Sweeps, Sweeps)
    print()

    print("Acceptance:",Lattice.Accepted/Lattice.Tried)

    Lattice.save(f"Scary_Stuff/Scary_N_{N}_J_{J}")