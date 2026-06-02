#!/usr/bin/env python3
"""
Day 03 — Rapidity & Pseudorapidity (Book §5.2.2–5.2.3)
======================================================

Objectives:
  1. Compute rapidity y and pseudorapidity η for all particles in an event
  2. Compare y vs η for pions, kaons, and protons
  3. Show that η → y for massless/high-pT particles
  4. Plot dN/dy and dN/dη for comparison
  5. Demonstrate rapidity is additive under boosts
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ampt_parser import iter_events, get_pid_name
from kinematics import rapidity, pseudorapidity, transverse_momentum, energy

filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_7.7_sub100.dat')

# Problem 1: Compute y and η for Event 1
print("PROBLEM 1: Rapidity vs Pseudorapidity for Event 1")
for header, particles in iter_events(filepath, max_events=1):
    y = rapidity(particles['px'], particles['py'], particles['pz'], particles['mass'])
    eta = pseudorapidity(particles['px'], particles['py'], particles['pz'])
    pT = transverse_momentum(particles['px'], particles['py'])

    print(f"{'PID':>6s}  {'pT':>7s}  {'y':>8s}  {'η':>8s}  {'|y-η|':>8s}")
    for i in range(min(15, len(particles))):
        print(f"{particles['pid'][i]:6d}  {pT[i]:7.3f}  {y[i]:8.4f}  {eta[i]:8.4f}  {abs(y[i]-eta[i]):8.4f}")

# Problem 2: y vs η scatter for different species
print("\nPROBLEM 2: y vs η comparison by particle species")
all_data = {211: {'y':[], 'eta':[]}, 321: {'y':[], 'eta':[]}, 2212: {'y':[], 'eta':[]}}

for header, particles in iter_events(filepath, max_events=50):
    y = rapidity(particles['px'], particles['py'], particles['pz'], particles['mass'])
    eta = pseudorapidity(particles['px'], particles['py'], particles['pz'])
    for pid_key in all_data:
        mask = np.abs(particles['pid']) == pid_key
        all_data[pid_key]['y'].extend(y[mask])
        all_data[pid_key]['eta'].extend(eta[mask])

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
names = {211: 'π±', 321: 'K±', 2212: 'p/p̄'}
for ax, (pid, data) in zip(axes, all_data.items()):
    ax.scatter(data['y'], data['eta'], s=1, alpha=0.3)
    ax.plot([-5, 5], [-5, 5], 'r--', label='η = y')
    ax.set_xlabel('y (rapidity)'); ax.set_ylabel('η (pseudorapidity)')
    ax.set_title(f'{names[pid]}')
    ax.legend(); ax.set_aspect('equal')
    ax.set_xlim(-4, 4); ax.set_ylim(-4, 4)

fig.suptitle('Rapidity vs Pseudorapidity — AMPT 7.7 GeV', fontsize=14)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(__file__), 'day03_y_vs_eta.png'), dpi=150)
print("Saved: day03_y_vs_eta.png")

# Problem 3: |y - η| vs pT
print("\nPROBLEM 3: |y - η| decreases with pT (mass effect vanishes)")
all_pt, all_diff = [], []
for header, particles in iter_events(filepath, max_events=50):
    y = rapidity(particles['px'], particles['py'], particles['pz'], particles['mass'])
    eta = pseudorapidity(particles['px'], particles['py'], particles['pz'])
    pT = transverse_momentum(particles['px'], particles['py'])
    mask = np.abs(particles['pid']) == 2212  # protons (heaviest common)
    all_pt.extend(pT[mask])
    all_diff.extend(np.abs(y[mask] - eta[mask]))

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(all_pt, all_diff, s=2, alpha=0.3, color='steelblue')
ax.set_xlabel('pT (GeV/c)'); ax.set_ylabel('|y - η|')
ax.set_title('|y - η| vs pT for protons — approaches 0 at high pT')
fig.savefig(os.path.join(os.path.dirname(__file__), 'day03_diff_vs_pt.png'), dpi=150)
print("Saved: day03_diff_vs_pt.png")

# Problem 4: dN/dy vs dN/dη
from observables import dNdeta, dNdy
events = [(h, p) for h, p in iter_events(filepath, max_events=100)]

eta_c, eta_v, eta_e = dNdeta(events, eta_range=(-4, 4), nbins=40)
y_c, y_v, y_e = dNdy(events, y_range=(-4, 4), nbins=40)

fig, ax = plt.subplots(figsize=(8, 5))
ax.errorbar(eta_c, eta_v, yerr=eta_e, fmt='o', markersize=4, label='dN/dη (charged)')
ax.errorbar(y_c, y_v, yerr=y_e, fmt='s', markersize=4, label='dN/dy (charged)')
ax.set_xlabel('η or y'); ax.set_ylabel('dN/d(η or y)')
ax.set_title('AMPT 7.7 GeV — dN/dη vs dN/dy')
ax.legend()
fig.savefig(os.path.join(os.path.dirname(__file__), 'day03_dndeta_vs_dndy.png'), dpi=150)
print("Saved: day03_dndeta_vs_dndy.png")

# Problem 5: Rapidity additivity
print("\nPROBLEM 5: Rapidity is additive under boosts")
print("y_lab = y_cm + y_boost")
y_boost_values = [0.5, 1.0, 1.5, 2.0]
for y_b in y_boost_values:
    print(f"  Boost y={y_b}: particle at y_cm=0 → y_lab={y_b:.1f}")

print("\n✅ Day 03 exercises complete!")
