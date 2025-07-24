#Function in order to see how the pH and Ammonium conc. change ΔG of Feammox (cultivated with Ferrihydrite)
#Based on Equation (2,3,4 of paper 14 see supplement) write: ".venv\Scripts\streamlit.exe" run "feammox_3_2.py"
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

st.markdown("### Choose NH₄⁺ concentrations [mol/L]")
NH4_list = st.multiselect(
    label="NH₄⁺ values for pH plot",
    options=[0.0001, 0.001, 0.01, 0.1, 0.5, 1.0, 10.0],
    default=[0.1],
    format_func=lambda x: f"{x:.3f} mol/L"
)

st.markdown("### Choose pH values")
pH_list = st.multiselect(
    label="pH values for NH₄⁺ plot",
    options=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0],
    default=[5.0]
)

# Default-Werte zur Berechnung beibehalten
NH4_input = NH4_list[0] if NH4_list else 0.1
pH = pH_list[0] if pH_list else 5.0



Fe2_input = st. number_input("Fe2 Activity [~mmol/l]", min_value=0.1, max_value=5.0, value=0.5, step=0.1, format="%.3f") # [mol/L]
NH4 = NH4_input #* 10**(-3) # changing [mmol/L] in [mol/L]
R = 0.008314 #kJ mol^-1
T = 297.15 #Kelvin

C_A = 1 # mol L^-1 -> activity probably in [mol/L]
G0_fA = -699 #kJ mol^-1 -> Fe(OH)3 -> defined

G0_fB = 0 #pH*(-5.69) #kJ mol^-1 -> H+ -> variable ?????

# NH4 #mol L^-1
G0_fC = -79.37 #kJ mol^-1 -> NH4+ -> variable

#= 10**(-12) #mol L^-1
C_D = Fe2_input*10**(-3) # mol L^-1
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
    C_F = 0.0001  # mol L^-1
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

#------------------- figure 1 pH - fixed NH₄⁺ conc.----------------
fig1 = go.Figure()

for nh4 in NH4_list:
    G_r_values_pH = [func_G_r(pH_val, nh4) for pH_val in pH_range]
    fig1.add_trace(go.Scatter(
        x=pH_range,
        y=G_r_values_pH,
        mode='lines',
        name=f'NH₄⁺ = {nh4:.3f} mol/L',
        hovertemplate='pH: %{x}<br>ΔG: %{y:.2f} kJ/mol'
    ))

fig1.add_shape(
    type="line",
    x0=pH_range[0],
    y0=0,
    x1=pH_range[-1],
    y1=0,
    line=dict(color="black", width=1, dash="dash"),
)

fig1.update_layout(
    title='ΔG in relation to pH (fixed NH₄⁺ conc.)',
    xaxis=dict(
        title=dict(text='pH', font=dict(color='black')),
        tickfont=dict(color='black'),
        tickcolor='black',
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        title=dict(text='ΔG [kJ/mol]', font=dict(color='black')),
        tickfont=dict(color='black'),
        tickcolor='black',
        showline=True,
        linecolor='black'
    ),
    template='simple_white'
)

st.plotly_chart(fig1)


#-------------------- figure 2 NH₄⁺ - fixed pH -------------------------
fig2 = go.Figure()

for pH_val in pH_list:
    G_r_values_NH4 = [func_G_r(pH_val, nh4) for nh4 in NH4_range_mol]
    fig2.add_trace(go.Scatter(
        x=NH4_range_mol,
        y=G_r_values_NH4,
        mode='lines',
        name=f'pH = {pH_val:.1f}',
        hovertemplate='NH₄⁺: %{x:.4f} mol/L<br>ΔG: %{y:.2f} kJ/mol'
    ))

fig2.add_shape(
    type="line",
    x0=NH4_range_mol[0],
    y0=0,
    x1=NH4_range_mol[-1],
    y1=0,
    line=dict(color="black", width=1, dash="dash"),
)
fig1.update_layout(
    title='ΔG in relation to pH (fixed NH₄⁺ conc.)',
    xaxis=dict(
        title=dict(text='pH', font=dict(color='black')),
        tickfont=dict(color='black'),
        tickcolor='black',
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        title=dict(text='ΔG⁰<sub>f</sub> [kJ/mol]', font=dict(color='black')),
        tickfont=dict(color='black'),
        tickcolor='black',
        showline=True,
        linecolor='black'
    ),
    template='simple_white'
)
fig2.update_layout(
    title='ΔG in relation to NH₄⁺ (fixed pH)',
    xaxis_type='log',
    xaxis=dict(
        title=dict(text='NH₄⁺ [mol/L]', font=dict(color='black')),
        tickmode='linear',
        dtick=1,
        color='black',
        showline=True,
        linecolor='black',
        tickfont=dict(color='black'),
        tickcolor='black'
    ),
    yaxis=dict(
        title=dict(text='ΔG [kJ/mol]', font=dict(color='black')),
        color='black',
        showline=True,
        linecolor='black',
        tickfont=dict(color='black'),
        tickcolor='black'
    ),
    template='simple_white'
)

st.plotly_chart(fig2)


#------------------ tables of fixed values -------------------------------
data = {
    "Component": ["Fe(OH)₃", "H⁺", "NH₄⁺", "Fe²⁺", "H₂O", product],
    "Activity": [
        f"{C_A:.0f}",
        f"{10**(-pH):.2e}",
        f"{NH4:.2e}",
        f"{C_D:.2e}",
        f"{C_E:.0f}",
        f"{C_F:.2e}"
    ],
    "ΔG⁰f [kJ/mol]": [
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
