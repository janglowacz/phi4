import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

Values = np.linspace(0,2,21)

Lambda = 1

Acceptances = []

for Value in Values:
    print()
    Lattice = Theory.Lattice(Parameters = [-1,1], Size = [10,10,10,10], Spacing = [1,1,1,1])
    Lattice.History = []
    Lattice.Phi = np.ones(Lattice.Shape)*0.1

    Tracker = Utility.Tracker()

    Sweeps = 10

    Steps = 1
    Sweep_Dmax = np.sqrt(Lattice.Spacing[0]*Value)

    Tracker.START()
    for k in range(Sweeps):
        Tracker.FLUSH(k, Sweeps)
        Lattice.Dmax = Sweep_Dmax
        Lattice.Sweep(Steps = Steps, Save = True)
    Tracker.FLUSH_Final(Sweeps, Sweeps)
    print()

    Acceptances.append(Lattice.Accepted/Lattice.Tried)
    print(Value,":",Lattice.Accepted/Lattice.Tried)


plt.figure(figsize=(9,6))
plt.plot(Values,Acceptances,".", label = "Acceptance")
plt.legend(loc = "best")
plt.grid()
plt.xlabel("Value")
plt.ylabel("Acceptance")
plt.savefig("Lat_Acceptance.pdf")
# plt.show()
plt.close()