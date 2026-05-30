import numpy as np

def band_struc_compute(a, n_bands=4):
    k = np.linspace(-10,10,1000)
    G = 2*np.pi / a
    bands = []
    for n in range(-n_bands, n_bands+1):
        E = 0.5*(k+n*G)**2
        bands.append(E)

    return{"k":k,"G":G, "bands": bands}