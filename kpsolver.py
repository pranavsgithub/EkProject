#solver for kronig-penney condition

import numpy as np
import matplotlib.pyplot as plt

def kp_solver(E,a,b,V0):
    if E<=0 or E>= V0:
     return np.nan
    alpha = np.sqrt(V0-E)
    beta = np.sqrt(E)
    const_term = (alpha**2 - beta**2)/(2*alpha*beta)
    F = (const_term*np.sinh(alpha*b)*np.sin(beta*(a-b)) +
         np.cosh(alpha*b)*np.cos(beta*(a-b)))
    return F

def allowed_regions(a,b,V0, points=5000):
    energies = np.linspace(1e-4,V0-1e-4,points)
    rhs = np.array([kp_solver(E,a,b,V0) for E in energies])
    allowed_bool = (np.abs(rhs)<=1)
    return{"energy": energies, "rhs": rhs, "allowed_regions": allowed_bool}

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

def plot_kp(a,b,V0):
    data = allowed_regions(a,b,V0)
    energies = data["energy"]
    rhs = data["rhs"]
    allowed = data["allowed_regions"]
    plt.figure(figsize = (10,6))
    plt.plot(energies, rhs, label="Rhs", color="blue", linewidth=1.5)
    plt.axhline(1, color="red", linestyle="--", alpha=0.7, label="Boundaries")
    plt.axhline(-1, color="red", linestyle="--", alpha=0.7)
    plt.fill_between(energies,-2,2, where=allowed, color="lightgreen", alpha=0.3,label="Allowed Bands")
    plt.title("Kronig Penney Model solutions")
    plt.xlabel("Energy")
    plt.ylabel("Rhs")
    plt.ylim(-2,2)
    plt.xlim(0,V0)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    unit_cell = float(input("Enter a: "))
    barrier_width = float(input("Enter b: "))
    barrier_height = float(input("Enter V0: "))

    plot_kp(unit_cell,barrier_width,barrier_height)
