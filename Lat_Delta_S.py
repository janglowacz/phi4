import sys
import numpy as np
import matplotlib.pyplot as plt
import json

import Theory as Theory

import Utility

Parameters = [-1,1]
Size = [10,10,10,10]
Spacing = [1,1,1,1]

Lattice1 = Theory.Lattice(Parameters = Parameters, Size = Size, Spacing = Spacing)
Lattice2 = Theory.Lattice(Parameters = Parameters, Size = Size, Spacing = Spacing)
Lattice3 = Theory.Lattice(Parameters = Parameters, Size = Size, Spacing = Spacing)

Lattice2.calc_crazy_stuff()
Lattice3.calc_other_stuff()

Lattice1.Phi = np.ones(Lattice1.Shape)*0.1
Lattice2.Phi = np.ones(Lattice2.Shape)*0.1
Lattice3.Phi = np.ones(Lattice3.Shape)*0.1

Tracker = Utility.Tracker()

Thermalization = 20
Sweeps = 50

Steps = 5

print("Thermalization:")
Tracker.START()
for k in range(Thermalization):
    Tracker.FLUSH(k, Thermalization)
    Lattice1.Sweep(Steps = Steps)
    Lattice2.Sweep_ALT(Steps = Steps)
    Lattice3.Sweep_NEW(Steps = Steps)
Tracker.FLUSH_Final(Thermalization, Thermalization)
print()

print("Sweeps:")
Tracker.START()
for k in range(Sweeps):
    Tracker.FLUSH(k, Sweeps)
    Lattice1.Sweep(Steps = Steps, Save = True)
    Lattice2.Sweep_ALT(Steps = Steps, Save = True)
    Lattice3.Sweep_NEW(Steps = Steps, Save = True)
Tracker.FLUSH_Final(Sweeps, Sweeps)
print()

print("Acceptance 1:",Lattice1.Accepted/Lattice1.Tried)
print("Acceptance 2:",Lattice2.Accepted/Lattice1.Tried)
print("Acceptance 3:",Lattice3.Accepted/Lattice1.Tried)

Lattice1.save("Comparison/Type1")
Lattice2.save("Comparison/Type2")
Lattice3.save("Comparison/Type3")