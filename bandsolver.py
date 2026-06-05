from kpsolver import *
def band_compute(a,b,V0,
                 points=5000, zones=4):
    kp_data = allowed_regions(a,b,V0, points)
    energies = kp_data["energy"]
    rhs = kp_data["rhs"]
    allowed = kp_data["allowed_regions"]
    allowed_E = energies[allowed]
    allowed_rhs = rhs[allowed]
    k_pos = np.arccos(allowed_rhs)/a
    k_dash = -k_pos
    G = 2 * np.pi / a
    k_all = []
    E_all = []
    for n in range(-zones, zones+1):
        shift = n*G
        k_all.extend(k_pos+shift)
        E_all.extend(allowed_E)
        k_all.extend(k_dash+shift)
        E_all.extend(allowed_E)

    return{"k_pos": k_pos  , "k_dash": k_dash, "energy":allowed_E, "k_all":k_all,
           "E_all":E_all, "G": G}

def band_seperator(allowed_E, threshold_factor=10):
    dE = np.diff(allowed_E)
    spacing = np.median(dE)
    threshold = threshold_factor*spacing
    split_indices = np.where(dE>threshold)[0]
    horizontal_bands = []
    start = 0
    for idx in split_indices:
        horizontal_bands.append(allowed_E[start:idx+1])
        start = idx + 1

    horizontal_bands.append(allowed_E[start:])
    return horizontal_bands

def kp_dos(new_band_data, bins=5000):
    k = new_band_data["k_pos"]
    E = new_band_data["energy"]
    idx = np.argsort(k)
    k = k[idx]
    E = E[idx]
    dEbydK = np.gradient(E,k)
    weights = 1/((np.abs(dEbydK)) + 1e-6)
    np.histogram(E)
    dos, edges = np.histogram(
        E,
        bins=bins,
        weights=weights
    )
    centres = (edges[1:] + edges[:-1]) / 2
    return {"energy": centres, "dos": dos}
    # energies = new_band_data["E_all"]
    # dos,edges = np.histogram(energies,bins=bins)
