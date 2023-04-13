#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from astropy import units

from progs import ProgModel

# Constants
Msun = units.M_sun.to(units.g)
Rsun = units.R_sun.to(units.cm)

# Extract data for 15.2 solar mass model.
# In theory we could do a loop over all models here and fill an array/list
model = "15.2"
prog = ProgModel(model, 's16')

# compute compactness xi_2.5 = 2.5 / R( m = 2.5Msun )
xi_2p5 = prog.get_compactness(2.5)
print(f"xi_2.5 = {xi_2p5}")

# === Progenitor final mass, radius ===
# Progs stors data as pandas dataframes. 
# Most quantities such as mass, density, temperature, mass fractions are in prog.profile
# You can do println(prog.profile), and print(prog.network) to learn more
n = len(prog.profile['mass']) - 1
M_preSN = prog.profile["mass"][n] / Msun
R_preSN = prog.profile["radius_edge"][n] / Rsun
print(f"R_presn = {R_preSN}")
print(f"M_presn = {M_preSN}")
# Note that the final mass is different from the ZAMS mass (15.2),
# due to mass loss from stellar winds.

# === Progenitor Shell Masses ===
# The general approach for determining hydrogen envelope mass, helium shell mass, etc
# Is to define cutoffs on relevant mass fractions. For the H envelope, we count all mass
# where the H mass fraction is "sufficiently high." 0.15 works, but in general 
# this requires some tuning when working with lots of models to make sure it works for all.
tol = 0.15
ind = np.min(np.where(prog.profile['h1'] > tol))
# M_env = total mass - mass under envelope
M_env = (prog.profile['mass'][n] - prog.profile['mass'][ind]) / Msun
print(f"M_env = {M_env}")

# Helium core
# Here we maximum mass corrdinate where the helium mass fraction he4 is above
# a threshold (0.6). Above that, we enter the H envelope
# It is useful to plot the mass fraction as a function of enclosed mass to test this.

# Note that this defines the Helium Core, e.g., everything below the envelope.
# How would you modify this to get the helium Shell mass? See the plot produced.
M_He_core = np.max((prog.profile['mass'][prog.profile['he4'] > 0.6])) / Msun
print(f"M_He = {M_He_core}")

# Carbon-Oxygen core
M_CO_core = np.max(prog.profile['mass'][prog.profile['c12'] > 0.05]) / Msun
print(f"M_CO = {M_CO_core}")

# Iron Core
M_Fe_core = np.min(prog.profile['mass'][prog.profile['si28'] > 0.2]) / Msun
print(f"M_Fe = {M_Fe_core}")

# To get a feel for the process, we'll plot the He mass fraction along with our
# threshold to see how we determine the core mass

fig, ax = plt.subplots()
M = prog.profile["mass"] / Msun
X_He = prog.profile["he4"]
ax.plot(M, X_He)
ax.axvline(M_He_core, color="black", ls="--", lw=1.5)
ax.set(ylabel=r"X$_{He}$", xlabel=r"Mass [M$_{\odot}$]")
plt.show()
