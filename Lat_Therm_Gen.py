import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

Settings = [[-1,0,0.1]]
Settings1 = [[1,1,0.1],[0,1,0.1],[-1,1,0.1],[-2,1,0.1]]
Settings2 = [[-1,-1,0.1],[-1,1,0.1],[-1,1,0.1],[-1,2,0.1]]
Settings3 = [[1,-1,0.1],[1,0,0.1],[1,1,0.1],[1,2,0.1]]
Settings4 = [[-1,1,0],[-1,1,0.1],[-1,1,0.5],[-1,1,1]]
Settings5 = [[-1,0,0.1],[-1,5,0.1],[-1,25,0.1],[-1,125,0.1]]

Lambda = 1

for Setting in Settings5:
    print()
    Lattice = Theory.Lattice(Parameters = Setting[:-1], Size = [10,10,10,10], Spacing = [1,1,1,1])
    Lattice.History = []
    Lattice.Phi = np.ones(Lattice.Shape)*Setting[-1]

    Tracker = Utility.Tracker()

    Sweeps = 1000

    Steps = 1

    print("Size:",Lattice.Size)
    print("Spacing:",Lattice.Spacing)
    print("Shape:",Lattice.Shape)

    print("Sweeps:")
    Tracker.START()
    for k in range(Sweeps):
        Tracker.FLUSH(k, Sweeps)
        Lattice.Sweep(Steps = Steps, Save = True)
    Tracker.FLUSH_Final(Sweeps, Sweeps)
    print()

    print("Acceptance:",Lattice.Accepted/Lattice.Tried)

    Lattice.save("therm/Mu_"+str(Setting[0])+"_Lambda_"+str(Setting[1])+"_Offset_"+str(Setting[2]))