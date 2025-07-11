#Function in order to see how the pH and Ammonium conc. change ΔG of Feammox (cultivated with Ferrihydrite)
#Based on Equation (2,3,4 of paper 14 see supplement) write: ".venv\Scripts\streamlit.exe" run "feammox_3.py"
#Annahme: activities neglected, as too low impact

import numpy as np
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.title("Feammox - Thermodynamics")

# parameters
equation_choice = st.selectbox(
    "Choose the equation:",
    ("(1) 3Fe(OH)₃ + 5H⁺ + NH₄⁺ → 3Fe²⁺ + 9H₂O + 0.5N₂", "(2) 6Fe(OH)₃ + 10H⁺ + NH₄⁺ → 6Fe²⁺ + 16H₂O + NO₂⁻", "(3) 8Fe(OH)₃ + 14H⁺ + NH₄⁺ → 8Fe²⁺ + 21H₂O + NO₃⁻")
)
pH = st.number_input("pH", min_value=1.0, max_value=14.0, value=5.0, step=0.1)
NH4 = st. number_input("NH₄⁺ concentration [mol/L]", min_value=0.0, max_value=10.0, value=2.0, step=0.001) # [mmol/L]
#NH4 = NH4_input * 10**(-3) #changing [mmol/L] in [mol/L]
R = 0.008314 #kJ mol^-1
T = 297.15 #Kelvin

C_A = 1 # mol L^-1 -> activity probably in [mol/L]
G0_fA = -699 #kJ mol^-1 -> Fe(OH)3 -> defined

G0_fB = 0 #pH*(-5.69) #kJ mol^-1 -> H+ -> variable ?????

# NH4 #mol L^-1
G0_fC = -79.37 #kJ mol^-1 -> NH4+ -> variable

C_D = 10**(-12) #mol L^-1
G0_fD = -78.87 #kJ mol^-1 -> Fe2+ -> defined

C_E = 1 #mol L^-1
G0_fE = -237.18 #kJ mol^-1 -> H2O -> defined


# calculations
def func_G_r_1(pH, NH4):
    G0_r = 3 * G0_fD + 9 * G0_fE + 0.5 * G0_fF - 3 * G0_fA - 5 * G0_fB - 1 * G0_fC
    G_r = G0_r + R*T*np.log(((C_D**3)*(C_E**9)*(C_F**0.5))/((C_A**3)*((10**(-pH))**5)*(NH4**1)))
    return G_r

def func_G_r_2(pH, NH4):
    G0_r = 6 * G0_fD + 16 * G0_fE + 1 * G0_fF - 6 * G0_fA - 10 * G0_fB - 1 * G0_fC
    G_r = G0_r + R*T*np.log(((C_D**6)*(C_E**16)*(C_F**1))/((C_A**6)*((10**(-pH))**10)*(NH4**1)))
    return G_r

def func_G_r_3(pH, NH4):
    G0_r = 8 * G0_fD + 21 * G0_fE + 1 * G0_fF - 8 * G0_fA - 14 * G0_fB - 1 * G0_fC
    G_r = G0_r + R*T*np.log(((C_D**8)*(C_E**21)*(C_F**1))/((C_A**8)*((10**(-pH))**14)*(NH4**1)))
    return G_r

if equation_choice == "(1) 3Fe(OH)₃ + 5H⁺ + NH₄⁺ → 3Fe²⁺ + 9H₂O + 0.5N₂":
    func_G_r = func_G_r_1
    product = "N₂"
    C_F = 0.001  # mol L^-1
    G0_fF = 0  # kJ mol^-1 -> N2- -> defined
elif equation_choice == "(2) 6Fe(OH)₃ + 10H⁺ + NH₄⁺ → 6Fe²⁺ + 16H₂O + NO₂⁻":
    func_G_r = func_G_r_2
    product = "NO₂⁻"
    C_F = 0.00001  # mol L^-1
    G0_fF = -37.2  # kJ mol^-1 -> NO2- -> defined
elif equation_choice == "(3) 8Fe(OH)₃ + 14H⁺ + NH₄⁺ → 8Fe²⁺ + 21H₂O + NO₃⁻":
    func_G_r = func_G_r_3
    product = "NO₃⁻"
    C_F = 0.00001  # mol L^-1
    G0_fF = -111.3  # kJ mol^-1 -> NO3- -> defined

# calculation of ΔG
st.write(f"ΔG for pH = {pH} and NH₄⁺ = {NH4_input} mol/L is **{func_G_r(pH, NH4):.2f} kJ/mol**")


#--------------------- figures ------------------------------------
# Generation of x values
pH_range = np.arange(1, 14, 0.1)
NH4_range_mol = np.logspace(-3, 0, 200)# von 0.001 mmol/L bis 10 mmol/L, 200 Punkte

G_r_values_NH4 = [func_G_r(pH, NH4*10**-3) for NH4 in NH4_range_mol]
G_r_values_pH = [func_G_r(pH, NH4) for pH in pH_range]


#------------------- figure 1 pH - fixed NH₄⁺ conc.----------------
fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=pH_range,
    y=G_r_values_pH,
    mode='markers+lines',
    marker=dict(size=1, color='blue'),
    name='ΔG in relation to pH (fixed NH₄⁺ conc.)',
    hovertemplate='pH: %{x}<br>ΔG: %{y:.2f} kJ/mol'
))

fig1.add_shape(
    type="line",
    x0=pH_range[0],
    y0=0,
    x1=pH_range[-1],
    y1=0,
    line=dict(color="white", width=1, dash="dash"),
)

fig1.update_layout(
    title='ΔG in relation to pH (fixed NH₄⁺ conc.)',
    xaxis_title='pH',
    yaxis_title='ΔG [kJ/mol]',
    xaxis=dict(tickmode='linear', dtick=1),
    template='simple_white'
)

st.plotly_chart(fig1)


#-------------------- figure 2 NH₄⁺ - fixed pH -------------------------
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=NH4_range_mol,
    y=G_r_values_NH4,
    mode='markers+lines',
    marker=dict(size=1, color='red'),
    name='ΔG in relation to NH₄⁺ (fixed pH)',
    hovertemplate='NH₄⁺: %{x:.4f} mol/L<br>ΔG: %{y:.2f} kJ/mol'
))

fig2.add_shape(
    type="line",
    x0=NH4_range_mol[0],
    y0=0,
    x1=NH4_range_mol[-1],
    y1=0,
    line=dict(color="white", width=1, dash="dash"),
)

fig2.update_layout(
    title='ΔG in relation to NH₄⁺ (fixed pH)',
    xaxis_title='NH₄⁺ [mol/L]',
    yaxis_title='ΔG [kJ/mol]',
    xaxis_type='log',
    template='simple_white'
)

st.plotly_chart(fig2)


#------------------ tables of fixed values -------------------------------
data = {
    "Component": ["Fe(OH)₃", "H⁺", "NH₄⁺", "Fe²⁺", "H₂O", product],
    "Activity": [
        f"{C_A:.0f}",
        f"{10**(-pH):.2e}",
        f"{NH4:.0f}",
        f"{C_D:.2e}",
        f"{C_E:.0f}",
        f"{NH4:.2e}"
    ],
    "ΔG⁰ [kJ/mol]": [
        f"{G0_fA:.0f}",
        f"{G0_fB:.0f}",
        f"{G0_fC:.2f}",
        f"{G0_fD:.2f}",
        f"{G0_fE:.2f}",
        f"{G0_fF:.0f}"
    ]
}

data2 = {
    "Parameter": ["R", "T"],
    "Value": [f"{R:.6f}", f"{T:.2f}"],
    "Unit": ["kJ mol⁻¹ K⁻¹", "K"]
}

df = pd.DataFrame(data)
df2 = pd.DataFrame(data2)

# Tabellen ausgeben ohne Index
st.write("### Overview: Concentrations & Standard Gibbs Energies")
st.table(df)

st.write("### Overview: Constants")
st.table(df2)
