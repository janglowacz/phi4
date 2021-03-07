# phi4
The code is written in python3.
The packages 'numpy' and 'scipy' are reqired to run the programs.
Certain programs require folders with specific names to be present in the same location the program is executed in.

|> The folder 'Classic.zip' contains all code based upon the classic parametrization.
|> The folder 'Alternative.zip' cotnains all code based upon the alternative parametrization.

=> The 'Theory.py' file contains the Lattice object with saving and loading methods and the implementation of the monte carlo simulation sweep and $\Delta S$. \
It also contains as a set of measurement methods and is imported by all other code.

=> The 'Lat_Vis.py' file contains code to verify the function of the algorithm.
=> The 'Lat_Vis_2d.py' file contains code to visually inspect a 2d lattice.

=> The 'Lat_Acceptance_Ana.py' file contains code to optimize the acceptance of our simulation. \
At default settings for the Lattice size its runtime is quite long.

=> The 'Lat_Therm_Gen.py' file contains code to generate lattices for the thermalization analysis. \
To create all files used by the analysis program this file needs to be executed multiple times while changing the settings it runs on. \
At default settings for the Lattice size its runtime is quite long. \
=> The 'Lat_Therm_Ana.py' file contains code to analyze the generated lattices. \
X> These programs require a folder called 'Therm' to be present.

=> The 'Lat_Finite_Gen.py' file contains code to generate lattices for the finite size. \
Its runtime is extremely long. \
It therefore is recommended to not run it for all lattice sizes and to run multiple versions with different lattice size ranges in parallel. \
=> The 'Lat_Finite_Ana.py' file contains code to analyze the generated latticess. \
At default settings for the Lattice size its runtime is quite long. \
=> The 'Lat_Finite_Plot.py' file contains code to plot data from the analysis. \
X> These programs require a folder called 'Finite_Size' to be present.

=> The 'Lat_Corr_Gen.py' file contains code to generate lattices for correlator extractions. \
Its runtime is quite short. \
=> The 'Lat_Corr_Ana.py' file contains code to analyze the generated lattices. \
X> These programs require a folder called 'Corr' to be present.

=> The 'Lat_Meff_B_Gen.py' file contains code to generate lattices for effective mass measurements. \
To create all files used by the analysis program this file needs to be executed multiple times while changing the settings it runs on. \
At default settings for the Lattice size its runtime is extremely long. \
=> The 'Lat_Meff_B_Ana.py' file contains code to analyze the generated lattices. \
X> These programs require a folder called 'Meff_B' to be present.

=> The 'Scary_Gen.py' file contains code to generate lattices for XXX ??? XXX. \
At default settings for the Lattice size its runtime is quite long. \
=> The 'Scary_Ana.py' file contains code to analyze lattices for XXX ??? XXX. \
X> These programs require a folder called 'Scary_Stuff' to be present.

=> The 'Utility.py' file contains methods to create nice output text as well as a bootstrap method. It is imported by most other code.
