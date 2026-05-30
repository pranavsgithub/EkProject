import numpy as np

def band_struc_compute(a, n_bands=4):
    k = np.linspace(-10,10,1000)
    G = 2*np.pi / a
    bands = []
    for n in range(-n_bands, n_bands+1):
        E = 0.5*(k+n*G)**2
        bands.append(E)

    return{"k":k,"G":G, "bands": bands, "a":a}

def bandgap(band_data, V0):
    k = band_data["k"]
    bands = band_data["bands"]
    gap = np.pi/band_data["a"]
    width = 0.2
    newbands = []
    for E in bands:
        E_new = E.copy()
        mask = np.abs(np.abs(k)-gap)<width
        E_new[mask] += V0/2
        newbands.append(E_new)
    return {**band_data, "bands": newbands}

def dos(band_data, bins=1000):
    all_energies = np.concatenate(band_data["bands"])
    dos,edges = np.histogram(all_energies,bins=bins)
    edge_centres = (edges[1:] + edges[:-1])/2
    return{"edge centres": edge_centres, "dos": dos}