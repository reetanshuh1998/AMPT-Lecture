#!/usr/bin/env python3
"""
Day 06 — AMPT Input/Output: Parameters & Data Format
===================================================
Objectives:
  1. Parse the subset AMPT data file and inspect the event headers
  2. Map out the distribution of impact parameter (b) in collisions
  3. Plot the relationship between initial participants Npart and b
  4. Analyze the reaction plane angle phi_RP distribution (is it isotropic?)
  5. Save plots summarizing the initial collision geometry parameters
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ampt_parser import iter_events

filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_7.7_sub100.dat')
events = [(h, p) for h, p in iter_events(filepath)]
outdir = os.path.dirname(__file__)

print("=" * 60)
print("AMPT I/O AND INITIAL COLLISION GEOMETRY")
print("=" * 60)

# Problem 1: Inspect event headers
print("PROBLEM 1: Header Statistics")
print("-" * 50)
b_list = []
npart_proj = []
npart_targ = []
npart_total = []
phi_rp_list = []
nparts_list = []

for h, p in events:
    b_list.append(h['b'])
    npart_proj.append(h['Npart_proj'])
    npart_targ.append(h['Npart_targ'])
    npart_total.append(h['Npart_proj'] + h['Npart_targ'])
    phi_rp_list.append(h['phi_RP'])
    nparts_list.append(h['nparticles'])

print(f"Total parsed events: {len(events)}")
print(f"Impact parameter b: mean = {np.mean(b_list):.2f} fm, range = [{np.min(b_list):.2f}, {np.max(b_list):.2f}] fm")
print(f"Total Npart:        mean = {np.mean(npart_total):.1f}, max = {np.max(npart_total)}")
print(f"Final particles:    mean = {np.mean(nparts_list):.1f}, range = [{np.min(nparts_list)}, {np.max(nparts_list)}]")

# Problem 2: Impact Parameter Distribution Plot
print("\nPROBLEM 2: Plotting Impact Parameter (b) Distribution")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(b_list, bins=15, color='darkcyan', edgecolor='black', alpha=0.7)
ax.set_xlabel('Impact Parameter $b$ (fm)', fontsize=12)
ax.set_ylabel('Events / Bin', fontsize=12)
ax.set_title('Impact Parameter Distribution (AMPT 7.7 GeV Sub100)', fontsize=14)
fig.savefig(os.path.join(outdir, 'day06_b_distribution.png'), dpi=150)
print("Saved: day06_b_distribution.png")

# Problem 3: Npart vs Impact Parameter (b)
print("\nPROBLEM 3: Participant Nucleons vs Impact Parameter")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(b_list, npart_total, color='firebrick', marker='o', alpha=0.8, edgecolors='black', label='$N_{part}$')
ax.scatter(b_list, npart_proj, color='navy', marker='^', alpha=0.6, label='$N_{part}^{proj}$')
ax.scatter(b_list, npart_targ, color='green', marker='s', alpha=0.6, label='$N_{part}^{targ}$')
ax.set_xlabel('Impact Parameter $b$ (fm)', fontsize=12)
ax.set_ylabel('Number of Participants', fontsize=12)
ax.set_title('Participants vs Collision Centrality Knob ($b$)', fontsize=14)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day06_npart_vs_b.png'), dpi=150)
print("Saved: day06_npart_vs_b.png")

# Problem 4: Reaction Plane Angle phi_RP Distribution
print("\nPROBLEM 4: Reaction Plane Angle phi_RP Distribution")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(phi_rp_list, bins=10, color='goldenrod', edgecolor='black', alpha=0.7)
ax.set_xlabel(r'Reaction Plane Angle $\Psi_{RP}$ (rad)', fontsize=12)
ax.set_ylabel('Events / Bin', fontsize=12)
ax.set_title(r'Distribution of Reaction Plane Angle $\Psi_{RP}$', fontsize=14)
ax.set_ylim(0, len(events)/4)
fig.savefig(os.path.join(outdir, 'day06_phi_rp.png'), dpi=150)
print("Saved: day06_phi_rp.png")

# Problem 5: Nparticles vs Npart Correlation
print("\nPROBLEM 5: Final Multiplicity vs Participant Correlation")
print("-" * 50)
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(npart_total, nparts_list, color='darkorchid', marker='D', alpha=0.8, edgecolors='black')
ax.set_xlabel('Total Number of Participants ($N_{part}$)', fontsize=12)
ax.set_ylabel('Number of Final Particles ($N_{parts}$)', fontsize=12)
ax.set_title('Correlation: Final Hadron Multiplicity vs. $N_{part}$', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day06_nparticles_vs_npart.png'), dpi=150)
print("Saved: day06_nparticles_vs_npart.png")

print("\n✅ Day 06 exercises complete!")
