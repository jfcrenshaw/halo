
# This module supplies the HALO efficiency matrix to any file that needs it
# The format:
#                 | 1n measured as 1n   2n measured as 1n |
#                 | 1n measured as 2n   2n measured as 2n |
#
# using Geant4 simulations, it was found that for neutron energies 0.5-6 MeV,
# this matrix took the values:
#                               | 0.2659  0.3615 |
#                               |    0    0.0855 |
#
# However, these were adjusted using experimental values from Colin Bruulsema.
# See the tech note for more details
#
# The current used values are seen in the function below:
#
# There is also a matrix for HALO-1kT, using e = 0.53 and calculating the others
# with the normal formulae (not the altered ones mentioned above)

import numpy as np

def effmatrix(config='halo1'):

    if config == 'halo1' or config == 'Halo1' or config == 'HALO1' or config == 1:
        M11 = 0.283
        M12 = 0.376
        M21 = 0
        M22 = 0.097
        M = np.matrix([[M11,M12],[M21,M22]])
    elif config == 'halo2' or config == 'Halo2' or config == 'HALO2' or config == 2:
        M11 = 0.530
        M12 = 0.498
        M21 = 0
        M22 = 0.281
        M = np.matrix([[M11,M12],[M21,M22]])
    else:
        print('Invalid experiment configuration. Please provide either halo1 or halo2')
   

    return M