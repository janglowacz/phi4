import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

Lattice = Theory.Lattice(Parameters = [1,1], Size = [10,10,10,10], Spacing = [1,1,1,1])
Lattice.Phi = np.ones(Lattice.Shape)*0

Tracker = Utility.Tracker()

Thermalization = 20
Sweeps = 100

Steps = 5
Sweep_Dmax = np.sqrt(Lattice.Spacing[0])

print("Size:",Lattice.Size)
print("Spacing:",Lattice.Spacing)
print("Shape:",Lattice.Shape)

print()

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

Lattice.save("Corr")