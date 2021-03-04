import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

Lattice = Theory.Lattice(Parameters = [1,0], Size = [50], Spacing = [1])
Lattice.Phi = np.ones(Lattice.Shape)*0
Lattice.calc_crazy_stuff()

Tracker = Utility.Tracker()

Thermalization = 100
Sweeps = 1000

Steps = 2
Sweep_Dmax = np.sqrt(Lattice.Spacing[0])

print("Thermalization:")
Tracker.START()
for k in range(Thermalization):
    Tracker.FLUSH(k, Thermalization)
    Lattice.Sweep_ALT(Sweep_Dmax, Steps = Steps)
Tracker.FLUSH_Final(Thermalization, Thermalization)
print()

print("Sweeps:")
Tracker.START()
for k in range(Sweeps):
    Tracker.FLUSH(k, Sweeps)
    Lattice.Sweep_ALT(Sweep_Dmax, Steps = Steps, Save = True)
Tracker.FLUSH_Final(Sweeps, Sweeps)
print()

print("Acceptance:",Lattice.Accepted/Lattice.Tried)

if False:
    Lattice2 = Theory.Lattice(Parameters = [1,0], Size = [50], Spacing = [1])
    Lattice2.Phi = np.ones(Lattice2.Shape)*0
    Lattice2.calc_crazy_stuff()

    Thermalization = 100
    Sweeps = 1000

    Steps = 2
    Sweep_Dmax = np.sqrt(Lattice2.Spacing[0])

    print("Thermalization:")
    Tracker.START()
    for k in range(Thermalization):
        Tracker.FLUSH(k, Thermalization)
        Lattice2.Sweep_ALT(Sweep_Dmax, Steps = Steps)
    Tracker.FLUSH_Final(Thermalization, Thermalization)
    print()

    print("Sweeps:")
    Tracker.START()
    for k in range(Sweeps):
        Tracker.FLUSH(k, Sweeps)
        Lattice2.Sweep_ALT(Sweep_Dmax, Steps = Steps, Save = True)
    Tracker.FLUSH_Final(Sweeps, Sweeps)
    print()

    print("Acceptance:",Lattice2.Accepted/Lattice2.Tried)


t_s = np.linspace(0,Lattice.Size[0],Lattice.Shape[0])

bins = np.linspace(-2.05, 2.05, 42)

plt.hist([np.array(Lattice.History).flatten()], bins, alpha = 0.5, label = ["ours"], density=True)
# plt.hist([np.array(Lattice.History).flatten(), np.array(Lattice2.History).flatten()], bins, alpha = 0.5, label = ["ours","weird"], density=True)

x_s = np.linspace(-2.05,2.05,1000)
omega = np.sqrt(Lattice.M_squared * (1 + np.square(Lattice.Spacing[0]) * Lattice.M_squared / 4) )

plt.plot(x_s,[np.sqrt(1/np.pi)*np.exp(-np.square(x)) for x in x_s],label="continuum solution")
plt.plot(x_s,[np.sqrt(omega/np.pi)*np.exp(-omega*np.square(x)) for x in x_s],"--",label="lattice solution")

plt.legend(loc="best")
plt.grid()
plt.xlabel("field")
plt.ylabel("probablity")
plt.show()
plt.close()