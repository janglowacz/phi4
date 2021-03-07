# phi4
The code is written in python3.
The packages 'numpy' and 'scipy' are reqired to run the programs.
Certain programs require folders with specific names to be present in the same location the program is executed in.

=> The 'Theory.py' file contains the Lattice object with saving and loading methods and the implementation of the monte carlo simulation sweep and $\Delta S$. \
It also contains as a set of measurement methods and is imported by all other code.

=> The 'Lat_Acceptance_Ana.py' file contains code to optimize the acceptance of our simulation. \
At default settings for the Lattice size its runtime is quite long.

=> The 'Lat_Therm_Gen.py' file contains code to generate lattices for thermalization analysis. \
To create all files used by the analysis program this file needs to be executed multiple times while changing the settings it runs on. \
At default settings for the Lattice size its runtime is quite long. \
=> The 'Lat_Therm_Ana.py' file contains code to analyze the generated lattices for thermalization analysis. \
X> These programs require a folder called 'Therm' to be present.

=> The 'Lat_Finite_Gen.py' file contains code to generate lattices for finite size analysis. \
Its runtime is extremely long. \
It therefore is recommended to not run it for all lattice sizes and to run multiple versions with different lattice size ranges in parallel. \
=> The 'Lat_Finite_Ana.py' file contains code to analyze lattices for finite size analysis. \
At default settings for the Lattice size its runtime is quite long. \
=> The 'Lat_Finite_Plot.py' file contains code to plot data for finite size analysis. \
X> These programs require a folder called 'Finite_Size' to be present.

=> The 'Lat_Corr_Gen.py' file contains code to generate lattices for correlator analysis. \
Its runtime is quite short. \
=> The 'Lat_Corr_Ana.py' file contains code to analyze lattices for correlator analysis. \
X> These programs require a folder called 'Corr' to be present.

=> The 'Lat_Meff_B_Gen.py' file contains code to generate lattices for symmetry breaking in dependence of musquared analysis. \
To create all files used by the analysis program this file needs to be executed multiple times while changing the settings it runs on. \
At default settings for the Lattice size its runtime is extremely long. \
=> The 'Lat_Meff_B_Ana.py' file contains code to analyze lattices for symmetry breaking in dependence of musquared analysis. \
X> These programs require a folder called 'Meff_B' to be present.

=> The 'Scary_Gen.py' file contains code to generate lattices for scary analysis. \
At default settings for the Lattice size its runtime is quite long. \
=> The 'Scary_Ana.py' file contains code to analyze lattices for scary analysis. \
X> These programs require a folder called 'Scary_Stuff' to be present.

=> The 'Utility.py' file contains methods to create nice output text as well as a bootstrap method. It is imported by most other code.
