import streamlit as st
import numpy as np
import plotly.graph_objects as go
from functions import band_struc_compute
from functions import bandgap

# def band_struc_compute(a, n_bands=4):
#     k = np.linspace(-10,10,1000)
#     G = 2*np.pi / a
#     bands = []
#     for n in range(-n_bands, n_bands+1):
#         E = 0.5*(k+n*G)**2
#         bands.append(E)
#
#     return{"k":k,"G":G, "bands": bands}

st.title("Band theory simulator")
st.write("Note: All units are currently arbitrary")
st.write("Move the sliders to view how various parameters affect electronic structure and conductivity")
a = st.sidebar.slider("Unit cell width, a",  1.0, 10.0, 5.0, 0.1)
b = st.sidebar.slider("Potential barrier width, b", 0.1, 5.0, 1.0, 0.1)
V0 = st.sidebar.slider("Potential barrier height (V0)", 0.1, 20.0, 5.0, 0.1)
n = st.sidebar.slider("Free electron per unit volume n", 1.0, 100.0, 50.0)
T = st.sidebar.slider("Temperature in Kelvin", 1.0, 1000.0, 300.0)


st.write("All physical constants such as mass and reduced planck constant assumed to be 1")

#k = np.linspace(-10,10,1000)

#G = 2 * np.pi / a

# st.subheader("Reciprocal Space Information")
#
# col1, col2 = st.columns(2)
#
# with col1:
#     st.metric("Unit Cell width (a)", f"{a:.2f}")
#
# with col2:
#     st.metric("Reciprocal Lattice Vector (G)", f"{G:.3f}")
#
# k = np.linspace(-10, 10, 1000)
#
fig = go.Figure()
# for nlv in range(-4,5):
#     E = 0.5*(k+nlv*G)**2
#     fig.add_trace(go.Scatter(x=k,y=E, mode="lines", name=f"Band {nlv}"))

band_data = band_struc_compute(a)
band_data = bandgap(band_data, V0)
k = band_data["k"]
bands = band_data["bands"]
for i,E in enumerate(bands):
    fig.add_trace(go.Scatter(x=k, y=E, mode="lines", name=f"Band {i}"))
brilbound = np.pi / a
fig.add_vline(x=brilbound,line_dash="dash", annotation_text="pi/a")
fig.add_vline(x=-brilbound,line_dash="dash", annotation_text="-pi/a")
fig.update_layout(title="E v/s k graph indicating bands and Brillouin zone boundaries/bragg planes",
                  xaxis_title= 'k( Wave vec)',yaxis_title= "E v/s k (Wave vec)", height = 700)
st.plotly_chart(fig)

st.header("Current values")
st.write(f"Unit cell width a = {a}")
st.write(f"Potential barrier width b = {b}")
st.write(f"Potential barrier height V0 = {V0}")
st.write(f"Free electron per unit volume = {n}")
st.write(f"Temperature in Kelvin T = {T}")


