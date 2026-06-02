#!/usr/bin/env python3
"""
Day 04 — Invariant Yield, pT Spectra & mT Scaling (Book §5.2.4, §5.2.7)
=======================================================================

Objectives:
  1. Build pT spectra from AMPT data for charged particles
  2. Compute invariant yield (1/2πpT) d²N/(dpT dy)
  3. Fit exponential and extract slope parameter T
  4. Check mT scaling: plot as function of mT - m0
  5. Compare spectra for π, K, p — verify mass hierarchy
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from ampt_parser import iter_events
from kinematics import transverse_momentum, rapidity, transverse_mass
from observables import pt_spectrum, invariant_yield, get_pid_mask

filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_7.7_sub100.dat')
events = [(h, p) for h, p in iter_events(filepath)]
outdir = os.path.dirname(__file__)

# Problem 1: Charged pT spectrum
print("PROBLEM 1: Charged particle pT spectrum")
pt_c, pt_v, pt_e = pt_spectrum(events, pt_range=(0, 3.5), nbins=35, eta_cut=1.0)
fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(pt_c, pt_v, yerr=pt_e, fmt='o', markersize=4, color='steelblue')
ax.set_yscale('log'); ax.set_xlabel(r'$p_T$ (GeV/c)'); ax.set_ylabel(r'dN/dp$_T$')
ax.set_title('Charged pT Spectrum — AMPT 7.7 GeV, |η| < 1.0')
fig.savefig(os.path.join(outdir, 'day04_pt_spectrum.png'), dpi=150)
print("Saved: day04_pt_spectrum.png")

# Problem 2: Invariant yield
print("\nPROBLEM 2: Invariant yield")
iy_c, iy_v, iy_e = invariant_yield(events, pt_range=(0.2, 3.0), nbins=25, y_cut=0.5)
fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(iy_c, iy_v, yerr=iy_e, fmt='o', markersize=4, color='crimson')
ax.set_yscale('log'); ax.set_xlabel(r'$p_T$ (GeV/c)')
ax.set_ylabel(r'$\frac{1}{2\pi p_T} \frac{d^2N}{dp_T dy}$')
ax.set_title('Invariant Yield — AMPT 7.7 GeV, |y| < 0.5')
fig.savefig(os.path.join(outdir, 'day04_inv_yield.png'), dpi=150)
print("Saved: day04_inv_yield.png")

# Problem 3: Exponential fit
print("\nPROBLEM 3: Exponential fit to extract T")
def exp_func(pT, A, T):
    return A * np.exp(-pT / T)

mask = (pt_c > 0.3) & (pt_c < 2.5) & (pt_v > 0)
try:
    popt, pcov = curve_fit(exp_func, pt_c[mask], pt_v[mask], p0=[100, 0.2], sigma=pt_e[mask])
    print(f"  Fitted: A = {popt[0]:.2f}, T = {popt[1]*1000:.1f} MeV")
    print(f"  Inverse slope parameter T = {popt[1]*1000:.1f} MeV")
except:
    print("  Fit failed — try adjusting range")

# Problem 4: mT scaling
print("\nPROBLEM 4: mT scaling — check universality")
pid_groups = {'π±': [211, -211], 'K±': [321, -321], 'p/p̄': [2212, -2212]}
masses = {'π±': 0.140, 'K±': 0.494, 'p/p̄': 0.938}
colors = ['blue', 'green', 'red']

fig, ax = plt.subplots(figsize=(8, 6))
for (name, pids), col in zip(pid_groups.items(), colors):
    c, v, e = pt_spectrum(events, pt_range=(0, 3), nbins=25, charged_only=False,
                          target_pids=pids, eta_cut=1.0)
    # Convert to mT - m0
    m0 = masses[name]
    mT = np.sqrt(c**2 + m0**2)
    mT_m0 = mT - m0
    ax.errorbar(mT_m0, v, yerr=e, fmt='o', markersize=4, color=col, label=name)

ax.set_yscale('log'); ax.set_xlabel(r'$m_T - m_0$ (GeV)')
ax.set_ylabel(r'dN/dp$_T$'); ax.legend()
ax.set_title('mT Scaling Check — AMPT 7.7 GeV')
fig.savefig(os.path.join(outdir, 'day04_mT_scaling.png'), dpi=150)
print("Saved: day04_mT_scaling.png")

# Problem 5: Mass hierarchy in pT spectra
print("\nPROBLEM 5: Mass hierarchy — π > K > p at low pT")
fig, ax = plt.subplots(figsize=(8, 6))
for (name, pids), col in zip(pid_groups.items(), colors):
    c, v, e = pt_spectrum(events, pt_range=(0, 3), nbins=25, charged_only=False,
                          target_pids=pids, eta_cut=1.0)
    ax.errorbar(c, v, yerr=e, fmt='o-', markersize=4, color=col, label=name)

ax.set_yscale('log'); ax.set_xlabel(r'$p_T$ (GeV/c)')
ax.set_ylabel(r'dN/dp$_T$'); ax.legend()
ax.set_title('Identified Particle pT Spectra — AMPT 7.7 GeV')
fig.savefig(os.path.join(outdir, 'day04_pid_spectra.png'), dpi=150)
print("Saved: day04_pid_spectra.png")

print("\n✅ Day 04 exercises complete!")
