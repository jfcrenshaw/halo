
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

import numpy as np

def effmatrix():

    M11 = 0.283
    M12 = 0.376
    M21 = 0
    M22 = 0.097

    M = np.matrix([[M11,M12],[M21,M22]])

    return M