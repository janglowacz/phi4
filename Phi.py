import sys
import numpy as np
import matplotlib.pyplot as plt
import time

import Theory as Theory
import Utility

saveformat = '.pdf'

verbose = True

Lattice = Theory.Lattice(Parameters = [1,1], Size = [30,10,10,10], Spacing = [1,1,1,1])
Lattice.Phi = np.ones(Lattice.Shape)*0

Tracker = Utility.Tracker()

if Lattice.Shape.size > 1:
    t_s_2 = np.linspace(0,int(Lattice.Size[0]/2),int(Lattice.Shape[0]/2+1))
    two_point_correlators = np.zeros(t_s_2.size+1)

Thermalization = 10
Sweeps = 1

Steps = 1
Sweep_Dmax = np.sqrt(Lattice.Spacing[0])

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
    if Lattice.Shape.size > 1:
        for t in range(t_s_2.size+1):
            two_point_correlators[t] += Lattice.two_Point_Average(t) / Sweeps
Tracker.FLUSH_Final(Sweeps, Sweeps)
print()

print("Acceptance:",Lattice.Accepted/Lattice.Tried)

if Lattice.Shape.size > 1:
    masses = [np.log10(two_point_correlators[t]/two_point_correlators[t+1]) for t in range(t_s_2.size)]
    print(masses)

if Lattice.Shape.size == 2:
    t_s = np.linspace(0,Lattice.Size[0],Lattice.Shape[0]+1)
    x_s = np.linspace(0,Lattice.Size[1],Lattice.Shape[1]+1)
    plt.pcolormesh(x_s,t_s,Lattice.Phi,cmap="viridis",rasterized=True)

    cbar = plt.colorbar()
    #cbar.set_label(r"$\langle m\rangle$")
    plt.xlabel("x_1")
    plt.ylabel("x_0")
    plt.tight_layout()
    plt.show()
    plt.close()

if Lattice.Shape.size == 1:
    t_s = np.linspace(0,Lattice.Size[0],Lattice.Shape[0])

    for i in range(2):
        plt.plot(t_s,Lattice.History[-(i+1)],label=str(-(i+1)))

    plt.legend(loc="best")
    plt.grid()
    plt.xlabel("t")
    plt.ylabel("field")
    plt.show()
    plt.close()

    plt.hist(np.array(Lattice.History).flatten(), bins = np.linspace(-2.05, 2.05, 42), density = True)
    x_s = np.linspace(-2.05,2.05,1000)
    omega = np.sqrt(Lattice.M_squared * (1 + np.square(Lattice.Spacing[0]) * Lattice.M_squared / 4) )

    plt.plot(x_s,[np.sqrt(1/np.pi)*np.exp(-np.square(x)) for x in x_s],label="continuum solution",color="C1")
    plt.plot(x_s,[np.sqrt(omega/np.pi)*np.exp(-omega*np.square(x)) for x in x_s],"--",label="lattice solution",color="C2")

    plt.legend(loc="best")
    plt.grid()
    plt.xlabel("field")
    plt.ylabel("probablity")
    plt.show()
    plt.close()

if Lattice.Shape.size > 1:
    plt.plot(t_s_2,two_point_correlators[:t_s_2.size],".",label="plot",color="C0")
    # plt.plot(t_s_2,masses,".",label="plot",color="C0")

    plt.legend(loc="best")
    plt.yscale("log")
    plt.grid()
    plt.xlabel("t")
    plt.ylabel("mass")
    plt.show()
    plt.close()