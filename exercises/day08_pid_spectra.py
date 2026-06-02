#!/usr/bin/env python3
"""
Day 08 — Transverse Momentum Spectra & Particle Identification
=============================================================
Objectives:
  1. Build pT spectra from AMPT data for identified particles: pions, kaons, and protons
  2. Study the mass hierarchy of pT spectra (slope differences at low pT)
  3. Calculate and plot the K/pi and p/pi ratios as a function of pT
  4. Perform Tsallis or Boltzmann-like fit on each PID spectrum to extract temperature (T) and radial flow (beta)
  5. Discuss radial flow and mass ordering effects in heavy-ion collisions
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from ampt_parser import iter_events
from kinematics import transverse_momentum, rapidity
from observables import pt_spectrum

outdir = os.path.dirname(__file__)
filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_39_sub100.dat')
events = [(h, p) for h, p in iter_events(filepath)]

print("=" * 60)
print("IDENTIFIED PARTICLE SPECTRA AND PID RATIOS")
print("=" * 60)

# Particle groups
pid_groups = {
    'pions': [211, -211],
    'kaons': [321, -321],
    'protons': [2212, -2212]
}
masses = {'pions': 0.1396, 'kaons': 0.4937, 'protons': 0.9383}
colors = {'pions': 'royalblue', 'kaons': 'forestgreen', 'protons': 'crimson'}

# Problem 1 & 2: Build identified pT spectra & study mass hierarchy
print("PROBLEM 1 & 2: Identified Particle pT Spectra")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))

pt_bins = np.linspace(0.1, 3.0, 30)
bin_centers = 0.5 * (pt_bins[:-1] + pt_bins[1:])
spectra_data = {}

for name, pids in pid_groups.items():
    c, v, e = pt_spectrum(events, pt_range=(0.1, 3.0), nbins=29, charged_only=False,
                          target_pids=pids, eta_cut=1.0)
    # Save for ratio calculations
    spectra_data[name] = (v, e)
    ax.errorbar(c, v, yerr=e, fmt='o-', color=colors[name], label=f'{name.capitalize()}')

ax.set_yscale('log')
ax.set_xlabel(r'$p_T$ (GeV/c)', fontsize=12)
ax.set_ylabel(r'$dN/dp_T$ (GeV/c)$^{-1}$', fontsize=12)
ax.set_title('Identified Particle $p_T$ Spectra (AMPT 39 GeV)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day08_identified_spectra.png'), dpi=150)
print("Saved: day08_identified_spectra.png")

# Problem 3: Calculate and plot K/pi and p/pi ratios vs pT
print("\nPROBLEM 3: Identified Particle Ratios vs pT")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))

v_pi, e_pi = spectra_data['pions']
v_k, e_k = spectra_data['kaons']
v_p, e_p = spectra_data['protons']

# Avoid division by zero
mask = v_pi > 0
k_to_pi = np.zeros_like(v_pi)
p_to_pi = np.zeros_like(v_pi)
err_k_to_pi = np.zeros_like(v_pi)
err_p_to_pi = np.zeros_like(v_pi)

k_to_pi[mask] = v_k[mask] / v_pi[mask]
p_to_pi[mask] = v_p[mask] / v_pi[mask]

# Relative errors: delta(A/B) = (A/B) * sqrt((dA/A)^2 + (dB/B)^2)
err_k_to_pi[mask] = k_to_pi[mask] * np.sqrt((e_k[mask]/np.maximum(v_k[mask], 1e-10))**2 + (e_pi[mask]/np.maximum(v_pi[mask], 1e-10))**2)
err_p_to_pi[mask] = p_to_pi[mask] * np.sqrt((e_p[mask]/np.maximum(v_p[mask], 1e-10))**2 + (e_pi[mask]/np.maximum(v_pi[mask], 1e-10))**2)

ax.errorbar(bin_centers[mask], k_to_pi[mask], yerr=err_k_to_pi[mask], fmt='s-', color='forestgreen', label=r'$K / \pi$ ratio')
ax.errorbar(bin_centers[mask], p_to_pi[mask], yerr=err_p_to_pi[mask], fmt='d-', color='crimson', label=r'$p / \pi$ ratio')

ax.set_xlabel(r'$p_T$ (GeV/c)', fontsize=12)
ax.set_ylabel(r'Particle Ratio', fontsize=12)
ax.set_title('Identified Particle Ratios vs. $p_T$ (AMPT 39 GeV)', fontsize=14)
ax.set_ylim(0, 1.2)
ax.legend(fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day08_particle_ratios.png'), dpi=150)
print("Saved: day08_particle_ratios.png")

# Problem 4: Blast-Wave or Boltzmann Fit (Simple thermal model: dN/dpT ~ pT * exp(-mT / T))
print("\nPROBLEM 4: Thermal/Boltzmann-like Fit to Spectra")
print("-" * 50)
def thermal_model(pT, N0, T, m0):
    mT = np.sqrt(pT**2 + m0**2)
    return N0 * pT * np.exp(-mT / T)

for name in ['pions', 'kaons', 'protons']:
    m0 = masses[name]
    v, e = spectra_data[name]
    
    # We fit in the low-to-medium pT range
    fit_mask = (bin_centers > 0.2) & (bin_centers < 2.0) & (v > 0)
    x_fit = bin_centers[fit_mask]
    y_fit = v[fit_mask]
    y_err = e[fit_mask]
    
    try:
        # Wrap the function to fix mass m0
        func = lambda pT, N0, T: thermal_model(pT, N0, T, m0)
        popt, pcov = curve_fit(func, x_fit, y_fit, p0=[1000, 0.2], sigma=y_err, maxfev=2000)
        print(f"  {name.capitalize()}: Fitted Temperature T = {popt[1]*1000:.1f} ± {np.sqrt(pcov[1,1])*1000:.1f} MeV")
    except Exception as ex:
        print(f"  {name.capitalize()} fit failed: {ex}")

print("\n✅ Day 08 exercises complete!")
