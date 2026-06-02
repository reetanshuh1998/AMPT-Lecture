#!/usr/bin/env python3
"""
Day 07 — Single-Particle Observables: dN/deta, dN/dy, <pT>
=========================================================
Objectives:
  1. Calculate the pseudorapidity (eta) and rapidity (y) distributions of charged particles
  2. Plot dN/deta and dN/dy comparing √s_NN = 7.7 and 39 GeV subset files
  3. Study the difference between rapidity (mass-dependent) and pseudorapidity (massless assumption)
  4. Compute average pT (<pT>) for charged particles and investigate its energy dependence
  5. Validate results against the Relativistic Kinematics textbook (Chapter 5)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ampt_parser import iter_events
from kinematics import pseudorapidity, rapidity, transverse_momentum
from observables import charged_multiplicity

outdir = os.path.dirname(__file__)

# Paths to data subsets
file_7_7 = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_7.7_sub100.dat')
file_39 = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_39_sub100.dat')

events_7_7 = [(h, p) for h, p in iter_events(file_7_7)]
events_39 = [(h, p) for h, p in iter_events(file_39)]

print("=" * 60)
print("SINGLE-PARTICLE OBSERVABLES: dN/dη, dN/dy, <pT>")
print("=" * 60)

# Helper function to extract kinematic arrays for charged hadrons
def get_charged_hadron_kinematics(events):
    eta_all = []
    y_all = []
    pt_all = []
    for h, particles in events:
        # filter charged particles
        # Let's import is_charged from ampt_parser
        from ampt_parser import is_charged
        pids = particles['pid']
        px = particles['px']
        py = particles['py']
        pz = particles['pz']
        mass = particles['mass']
        
        # calculate pT and filter out very soft or hard particles if needed
        pt = transverse_momentum(px, py)
        eta = pseudorapidity(px, py, pz)
        
        # energy calculation E = sqrt(p^2 + m^2)
        p2 = px**2 + py**2 + pz**2
        E = np.sqrt(p2 + mass**2)
        y = rapidity(E, pz)
        
        mask = [is_charged(pid) for pid in pids]
        
        eta_all.extend(eta[mask])
        y_all.extend(y[mask])
        pt_all.extend(pt[mask])
        
    return np.array(eta_all), np.array(y_all), np.array(pt_all)

# Problem 1 & 2: Calculate and plot dN/deta & dN/dy comparison
print("PROBLEM 1 & 2: Pseudorapidity (η) and Rapidity (y) Distributions")
print("-" * 50)
eta_7, y_7, pt_7 = get_charged_hadron_kinematics(events_7_7)
eta_39, y_39, pt_39 = get_charged_hadron_kinematics(events_39)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# dN/deta
bins_eta = np.linspace(-5.0, 5.0, 41)
bin_width_eta = bins_eta[1] - bins_eta[0]
w_7_eta = np.ones_like(eta_7) / (len(events_7_7) * bin_width_eta)
w_39_eta = np.ones_like(eta_39) / (len(events_39) * bin_width_eta)

axes[0].hist(eta_7, bins=bins_eta, weights=w_7_eta, histtype='step', color='navy', linewidth=2, label=r'$\sqrt{s_{NN}}=7.7$ GeV')
axes[0].hist(eta_39, bins=bins_eta, weights=w_39_eta, histtype='step', color='crimson', linewidth=2, label=r'$\sqrt{s_{NN}}=39$ GeV')
axes[0].set_xlabel(r'Pseudorapidity $\eta$', fontsize=12)
axes[0].set_ylabel(r'$dN_{ch}/d\eta$', fontsize=12)
axes[0].set_title(r'Charged Pseudorapidity Distribution $dN_{ch}/d\eta$', fontsize=13)
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.5)

# dN/dy
bins_y = np.linspace(-4.0, 4.0, 33)
bin_width_y = bins_y[1] - bins_y[0]
w_7_y = np.ones_like(y_7) / (len(events_7_7) * bin_width_y)
w_39_y = np.ones_like(y_39) / (len(events_39) * bin_width_y)

axes[1].hist(y_7, bins=bins_y, weights=w_7_y, histtype='step', color='navy', linewidth=2, label=r'$\sqrt{s_{NN}}=7.7$ GeV')
axes[1].hist(y_39, bins=bins_y, weights=w_39_y, histtype='step', color='crimson', linewidth=2, label=r'$\sqrt{s_{NN}}=39$ GeV')
axes[1].set_xlabel(r'Rapidity $y$', fontsize=12)
axes[1].set_ylabel(r'$dN_{ch}/dy$', fontsize=12)
axes[1].set_title(r'Charged Rapidity Distribution $dN_{ch}/dy$', fontsize=13)
axes[1].legend()
axes[1].grid(True, linestyle='--', alpha=0.5)

fig.savefig(os.path.join(outdir, 'day07_rapidity_comparison.png'), dpi=150)
print("Saved: day07_rapidity_comparison.png")

# Problem 3: Rapidity vs Pseudorapidity (eta - y)
print("\nPROBLEM 3: Rapidity vs Pseudorapidity Comparison")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))
diff_7 = eta_7 - y_7
diff_39 = eta_39 - y_39

bins_diff = np.linspace(-1.0, 1.0, 50)
ax.hist(diff_7, bins=bins_diff, density=True, alpha=0.5, color='navy', label=r'7.7 GeV ($\eta - y$)')
ax.hist(diff_39, bins=bins_diff, density=True, alpha=0.5, color='crimson', label=r'39 GeV ($\eta - y$)')
ax.set_xlabel(r'$\eta - y$', fontsize=12)
ax.set_ylabel('Probability Density', fontsize=12)
ax.set_title(r'Kinematic Difference $\eta - y$ for Charged Hadrons', fontsize=14)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day07_eta_y_difference.png'), dpi=150)
print("Saved: day07_eta_y_difference.png")

# Problem 4 & 5: Mean pT computation and mass relations
print("\nPROBLEM 4 & 5: Average Transverse Momentum (<pT>)")
print("-" * 50)
print(f"Average <pT> at 7.7 GeV: {np.mean(pt_7):.4f} GeV/c")
print(f"Average <pT> at 39 GeV:  {np.mean(pt_39):.4f} GeV/c")

# Calculate mid-rapidity <pT> (|y| < 0.5)
mid_mask_7 = np.abs(y_7) < 0.5
mid_mask_39 = np.abs(y_39) < 0.5
print(f"Mid-rapidity (|y| < 0.5) <pT> at 7.7 GeV: {np.mean(pt_7[mid_mask_7]):.4f} GeV/c")
print(f"Mid-rapidity (|y| < 0.5) <pT> at 39 GeV:  {np.mean(pt_39[mid_mask_39]):.4f} GeV/c")

print("\n✅ Day 07 exercises complete!")
