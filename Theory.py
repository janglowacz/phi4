import sys
import numpy as np
import matplotlib.pyplot as plt
import json

import Utility

class Lattice:
    Accepted = 0
    Tried = 0
    History = []

    # Constrructor of the lattice
    def __init__(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            print("Lattice initialized without parameters")
        else:
            if "Shape" in kwargs and "Size" in kwargs:
                self.Shape = np.array(kwargs["Shape"])
                self.Size = np.array(kwargs["Size"])
                self.Spacing = np.array(self.Size / self.Shape)
            elif "Shape" in kwargs and "Spacing" in kwargs:
                self.Shape = np.array(kwargs["Shape"])
                self.Spacing = np.array(kwargs["Spacing"])
                self.Size = np.array(self.Size * self.Spacing)
            elif "Spacing" in kwargs and "Size" in kwargs:
                self.Size = np.array(kwargs["Size"])
                self.Spacing = np.array(kwargs["Spacing"])
                self.Shape = np.array(self.Size / self.Spacing).astype(int)
            else: raise Exception("Error in determining lattice dimensions")
            self.Phi = np.zeros(self.Shape)
            self.M_squared, self.Lambda =kwargs["Parameters"]
            print("Lattice initialized with parameters")

    # Method to save the lattice into a file
    def save(self, filename):
        DATA = {"Accepted":     self.Accepted,
                "Tried":        self.Tried,
                "History":      [phi.tolist() for phi in self.History],
                "Shape":        self.Shape.tolist(),
                "Size":         self.Size.tolist(),
                "Spacing":      self.Spacing.tolist(),
                "Phi":          self.Phi.tolist(),
                "M_squared":    self.M_squared,
                "Lamda":        self.Lambda}
        with open(filename + ".json", mode = "w") as f:
            f.write(json.dumps(DATA))
        print("Lattice saved to file \'"+filename+".json\'")

    # Method to load the lattice from a file
    def load(self, filename):
        with open(filename + ".json", mode = "r") as f:
            DATA = json.loads(f.read())
        self.Accepted   = DATA["Accepted"]
        self.Tried      = DATA["Tried"]
        self.History    = [np.array(phi) for phi in DATA["History"]]
        self.Shape      = np.array(DATA["Shape"])
        self.Size       = np.array(DATA["Size"])
        self.Spacing    = np.array(DATA["Spacing"])
        self.Spacing    = np.array(DATA["Spacing"])
        self.Phi        = np.array(DATA["Phi"])
        self.M_squared  = DATA["M_squared"]
        self.Lamda      = DATA["Lamda"]    
        print("Lattice initialized from file \'"+filename+".json\'")
        
    # Method to perform 1 sweep over the lattice
    def Sweep(self, Dmax, Steps=1, Save=False, sampling="uniform"):
        for x, _ in np.ndenumerate(self.Phi): # Sweep over all lattice sites
            for _ in range(Steps): # Steps times

                # Execute the Delta_Phi sampling
                if sampling == "uniform": Delta_Phi = np.random.uniform(-Dmax, Dmax)
                elif sampling == "gauss": Delta_Phi = np.random.randn() * Dmax
                else: raise Exception("\'" + str(sampling) + "\' is not a valid sampling type")

                # Determine the change in the action
                Delta_S = self.Delta_S_New(x, Delta_Phi)

                # Perform the Metropolis-Hastings accept-reject step
                if Delta_S < 0 or np.random.uniform(0,1) <= np.exp(-Delta_S):
                    self.Phi[x] += Delta_Phi
                    self.Accepted += 1
                self.Tried += 1
        if Save: self.History.append(self.Phi.copy())

    # Method to calculate the change in action (very simple)
    def Delta_S(self, x, Delta_Phi):
        new_Phi = self.Phi[x] + Delta_Phi
        Delta_Mass_term = self.M_squared/2 * (np.square(new_Phi) - np.square(self.Phi[x]))
        Delta_Four_term = self.Lambda / 24 * (np.power(new_Phi,4) - np.power(self.Phi[x],4))
        Delta_Kin_term = 0
        for i in range(self.Shape.size):
            shift = np.zeros(self.Shape.size)
            shift[i] = 1
            Delta_Kin_term += (np.square(self.Phi[tuple(((x + shift)%self.Shape).astype(int))] - new_Phi) - np.square(self.Phi[tuple(((x + shift)%self.Shape).astype(int))] - self.Phi[x])) / np.square(self.Spacing[i])
        return (Delta_Mass_term + Delta_Four_term + Delta_Kin_term/2) * np.prod(self.Spacing)

    # Method to calculate the change in action (very advanced, produces weird behaviour)
    def Delta_S_Old(self, x, Delta_Phi):
        new_Phi = self.Phi[x] + Delta_Phi
        Delta_Mass_term = (2 * self.Phi[x] + Delta_Phi) * Delta_Phi
        Delta_Four_term = self.Lambda / 24 * (np.power(new_Phi,4) - np.power(self.Phi[x],4))
        Delta_Kin_term = np.sum(-1 / np.square(self.Spacing)) * Delta_Mass_term
        for i in range(self.Shape.size):
            shift = np.zeros(self.Shape.size)
            shift[i] = 1
            Delta_Kin_term += Delta_Phi / np.square(self.Spacing[i]) * (self.Phi[tuple(((x + shift)%self.Shape).astype(int))] + self.Phi[tuple(((x - shift)%self.Shape).astype(int))])
        return (self.M_squared/2 * Delta_Mass_term + Delta_Four_term - Delta_Kin_term/2) * np.prod(self.Spacing)

    # Method to calculate the change in action (similar to the very simple method, but with an added average)
    def Delta_S_New(self, x, Delta_Phi):
        new_Phi = self.Phi[x] + Delta_Phi
        Delta_Mass_term = self.M_squared/2 * (np.square(new_Phi) - np.square(self.Phi[x]))
        Delta_Four_term = self.Lambda / 24 * (np.power(new_Phi,4) - np.power(self.Phi[x],4))
        Delta_Kin_term = 0
        for i in range(self.Shape.size):
            shift = np.zeros(self.Shape.size)
            shift[i] = 1
            a = (np.square(self.Phi[tuple(((x + shift)%self.Shape).astype(int))] - new_Phi) - np.square(self.Phi[tuple(((x + shift)%self.Shape).astype(int))] - self.Phi[x])) / np.square(self.Spacing[i])
            b = (np.square(self.Phi[tuple(((x - shift)%self.Shape).astype(int))] - new_Phi) - np.square(self.Phi[tuple(((x - shift)%self.Shape).astype(int))] - self.Phi[x])) / np.square(self.Spacing[i])
            Delta_Kin_term += (a + b) / 2
        return (Delta_Mass_term + Delta_Four_term + Delta_Kin_term/2) * np.prod(self.Spacing)

    # Method to calculate the two-point correlator of the current field
    def two_Point_Correlator(self, t, phi = None):
        if not type(phi) == np.ndarray: phi = self.Phi
        Phi_Zero = phi[tuple([0]*self.Shape.size)]
        RET = 0
        for x, _ in np.ndenumerate(phi[0]):
            RET += Phi_Zero * phi[t][x]
        return RET

    # Method to calculate the two-point correlator of the current field, averaged over all time values
    def two_Point_Average(self, t, phi = None):
        if not type(phi) == np.ndarray: phi = self.Phi
        RET = 0
        shift = np.zeros(self.Shape.size)
        shift[0] = t
        for x, _ in np.ndenumerate(phi):
            RET += phi[x] * phi[tuple(((x + shift)%self.Shape).astype(int))]
        return RET / self.Shape[0]

    # Method to calculate the average and error of all possible two point correlators
    def two_Point_Corr_Full(self, Tracker = None):
        t_s = np.linspace(0, self.Size[0]//2, self.Shape[0]//2+1)
        TPC = np.zeros([t_s.size, len(self.History)])
        if not Tracker == None:
            runs = len(self.History)*len(t_s)
            Tracker.START()
        for i in range(len(self.History)):
            for t in range(len(t_s)):
                if not Tracker == None: Tracker.FLUSH(t+(i*len(t_s)), runs)
                TPC[t, i] = self.two_Point_Average(t, phi = self.History[i])
        if not Tracker == None:
            Tracker.FLUSH_Final(runs, runs)
            print()
        TP = TPC.mean(axis = 1)
        TP = TP / TPC.mean(axis = 1)[0]
        TPE = np.array([Utility.bootstrap(TPC[t,:], 10000) for t in range(len(t_s))])
        TPE = TPE / TPC.mean(axis = 1)[0]
        return TP, TPE