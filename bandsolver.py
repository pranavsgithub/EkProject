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