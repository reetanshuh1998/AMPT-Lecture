#!/usr/bin/env python3
"""
Day 01 — Warm-Up: Reading AMPT Data Files
==========================================

Objectives:
  1. Read an AMPT .dat file line by line
  2. Count events and total lines
  3. Parse event headers
  4. List all unique particle IDs (PIDs)
  5. Count particles per event and plot a simple histogram

Data: Use the subset file Data/subsets/ampt_7.7_sub100.dat (100 events)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# ============================================================
# Problem 1: Count lines and events
# ============================================================
print("=" * 60)
print("PROBLEM 1: Count lines and events")
print("=" * 60)

filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_7.7_sub100.dat')

total_lines = 0
total_events = 0
with open(filepath, 'r') as f:
    for line in f:
        total_lines += 1

# Re-read to count events (event headers have >=10 columns)
with open(filepath, 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 10:
            try:
                int(parts[0])  # event id
                int(parts[2])  # nparticles
                total_events += 1
            except ValueError:
                pass

print(f"Total lines: {total_lines}")
print(f"Total events: {total_events}")
print(f"Average particles per event: {(total_lines - total_events) / max(total_events, 1):.0f}")


# ============================================================
# Problem 2: Parse the first 3 event headers
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 2: Parse event headers")
print("=" * 60)

from ampt_parser import iter_events

count = 0
for header, particles in iter_events(filepath, max_events=3):
    count += 1
    print(f"\nEvent {header['event_id']}:")
    print(f"  Particles: {header['nparticles']}")
    print(f"  Impact parameter b = {header['b']:.2f} fm")
    print(f"  Npart = {header['Npart_proj']} + {header['Npart_targ']} = {header['Npart_proj'] + header['Npart_targ']}")


# ============================================================
# Problem 3: List all unique PIDs
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 3: Unique particle IDs")
print("=" * 60)

import numpy as np
from ampt_parser import get_pid_name

all_pids = set()
for header, particles in iter_events(filepath):
    for pid in particles['pid']:
        all_pids.add(int(pid))

print(f"\nFound {len(all_pids)} unique PIDs:")
for pid in sorted(all_pids):
    print(f"  PID {pid:>6d} → {get_pid_name(pid)}")


# ============================================================
# Problem 4: Particles per event histogram
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 4: Particles per event histogram")
print("=" * 60)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

npart_list = []
for header, particles in iter_events(filepath):
    npart_list.append(header['nparticles'])

plt.figure(figsize=(8, 5))
plt.hist(npart_list, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
plt.xlabel('Number of particles per event')
plt.ylabel('Count')
plt.title('AMPT 7.7 GeV — Particles per Event (100 events)')
plt.tight_layout()
outpath = os.path.join(os.path.dirname(__file__), 'day01_npart_hist.png')
plt.savefig(outpath, dpi=150)
print(f"Saved histogram → {outpath}")
print(f"Mean particles/event: {np.mean(npart_list):.1f}")
print(f"Min: {np.min(npart_list)}, Max: {np.max(npart_list)}")


# ============================================================
# Problem 5: Print momentum components of first 10 particles
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 5: First 10 particles of Event 1")
print("=" * 60)

for header, particles in iter_events(filepath, max_events=1):
    print(f"{'PID':>6s}  {'px':>8s}  {'py':>8s}  {'pz':>8s}  {'mass':>6s}")
    print("-" * 45)
    for i in range(min(10, len(particles))):
        p = particles[i]
        print(f"{p['pid']:6d}  {p['px']:8.4f}  {p['py']:8.4f}  {p['pz']:8.4f}  {p['mass']:6.3f}")

print("\n✅ Day 01 exercises complete!")
