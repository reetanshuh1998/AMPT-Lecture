#!/usr/bin/env python3
"""
Day 09 — Centrality & Geometry: b, Npart, Ncoll
==============================================
Objectives:
  1. Determine the charged particle multiplicity (Nch) in the mid-pseudorapidity region (|eta| < 0.5 or 1.0)
  2. Order events by Nch to define centrality percentiles (0-10%, 10-30%, 30-50%, 50-100%)
  3. Calculate average impact parameter <b> and average participant nucleons <Npart> for each centrality class
  4. Plot Nch vs b and display centrality division lines
  5. Check correlation between Npart and Nch and discuss Glauber model vs AMPT dynamical outcomes
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ampt_parser import iter_events, is_charged
from kinematics import pseudorapidity

outdir = os.path.dirname(__file__)
filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_39_sub100.dat')
events = [(h, p) for h, p in iter_events(filepath)]

print("=" * 60)
print("COLLISION CENTRALITY DETERMINATION & GEOMETRY")
print("=" * 60)

# Problem 1: Compute charged multiplicity Nch per event in |eta| < 1.0
print("PROBLEM 1: Compute Charged Multiplicity (Nch) in |eta| < 1.0")
print("-" * 50)
nch_list = []
b_list = []
npart_list = []

for h, particles in events:
    pids = particles['pid']
    px = particles['px']
    py = particles['py']
    pz = particles['pz']
    
    eta = pseudorapidity(px, py, pz)
    
    # filter: charged particles with |eta| < 1.0
    charged_mask = [is_charged(pid) for pid in pids]
    eta_mask = np.abs(eta) < 1.0
    nch = np.sum(np.logical_and(charged_mask, eta_mask))
    
    nch_list.append(nch)
    b_list.append(h['b'])
    npart_list.append(h['Npart_proj'] + h['Npart_targ'])

nch_arr = np.array(nch_list)
b_arr = np.array(b_list)
npart_arr = np.array(npart_list)

print(f"Computed Nch for {len(events)} events.")
print(f"Max Nch: {np.max(nch_arr)}, Min Nch: {np.min(nch_arr)}, Mean Nch: {np.mean(nch_arr):.1f}")

# Problem 2 & 3: Define centrality percentiles and compute <b> & <Npart>
print("\nPROBLEM 2 & 3: Centrality Classes and Geometric Statistics")
print("-" * 50)
# Sort events in descending order of Nch
sorted_indices = np.argsort(nch_arr)[::-1]
sorted_nch = nch_arr[sorted_indices]
sorted_b = b_arr[sorted_indices]
sorted_npart = npart_arr[sorted_indices]

# Centrality percentiles divisions
percentiles = [0, 10, 30, 50, 100]
class_names = ["0-10%", "10-30%", "30-50%", "50-100%"]
n_events = len(events)

centrality_stats = {}

print(f"{'Centrality Class':<18s} | {'Nch Range':<12s} | {'Mean Nch':<8s} | {'Mean b (fm)':<12s} | {'Mean Npart':<10s}")
print("-" * 70)

for i in range(len(percentiles) - 1):
    start_idx = int(np.floor(percentiles[i] / 100.0 * n_events))
    end_idx = int(np.floor(percentiles[i+1] / 100.0 * n_events))
    
    class_nch = sorted_nch[start_idx:end_idx]
    class_b = sorted_b[start_idx:end_idx]
    class_npart = sorted_npart[start_idx:end_idx]
    
    centrality_stats[class_names[i]] = {
        'nch_min': np.min(class_nch),
        'nch_max': np.max(class_nch),
        'mean_nch': np.mean(class_nch),
        'mean_b': np.mean(class_b),
        'mean_npart': np.mean(class_npart),
        'boundary_nch': class_nch[-1] if len(class_nch) > 0 else 0
    }
    
    print(f"{class_names[i]:<18s} | "
          f"{np.min(class_nch):3d}-{np.max(class_nch):3d}  | "
          f"{np.mean(class_nch):8.1f} | "
          f"{np.mean(class_b):12.2f} | "
          f"{np.mean(class_npart):10.1f}")

# Problem 4: Plot Nch vs b with Centrality Division Boundaries
print("\nPROBLEM 4: Plotting Nch vs. Impact Parameter (b)")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(b_arr, nch_arr, color='navy', alpha=0.7, edgecolors='black', label='AMPT Events')

# Draw boundaries
colors = ['red', 'orange', 'green']
for i in range(len(percentiles) - 2):
    class_name = class_names[i]
    boundary_val = centrality_stats[class_name]['boundary_nch']
    ax.axhline(boundary_val, color=colors[i], linestyle='--', linewidth=1.5,
               label=f'{class_names[i]} / {class_names[i+1]} boundary ({boundary_val})')

ax.set_xlabel('Impact Parameter $b$ (fm)', fontsize=12)
ax.set_ylabel('Charged Multiplicity $N_{ch}$ ($|\eta| < 1$)', fontsize=12)
ax.set_title('Centrality Determination via Charged Multiplicity', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day09_centrality_determination.png'), dpi=150)
print("Saved: day09_centrality_determination.png")

# Problem 5: Plot Nch vs Npart
print("\nPROBLEM 5: Nch vs Npart Correlation Plot")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(npart_arr, nch_arr, color='forestgreen', alpha=0.7, edgecolors='black')
# Fit straight line
slope, intercept = np.polyfit(npart_arr, nch_arr, 1)
x_fit = np.linspace(np.min(npart_arr), np.max(npart_arr), 100)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color='red', linestyle='-', linewidth=2, label=f'Fit: $N_{{ch}} \\approx {slope:.2f} \\cdot N_{{part}} {intercept:+.1f}$')

ax.set_xlabel('Participant Nucleons $N_{part}$', fontsize=12)
ax.set_ylabel('Charged Multiplicity $N_{ch}$ ($|\eta| < 1$)', fontsize=12)
ax.set_title('Linearity check: Multiplicity vs Participant Nucleons', fontsize=14)
ax.legend(fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day09_nch_vs_npart.png'), dpi=150)
print("Saved: day09_nch_vs_npart.png")

print("\n✅ Day 09 exercises complete!")
