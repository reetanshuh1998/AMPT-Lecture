#!/usr/bin/env python3
"""
Day 10 — Collective Flow: v2, Event Plane Method
================================================
Objectives:
  1. Understand the source of anisotropic flow (spatial eccentricity translating to momentum anisotropy)
  2. Implement/use the Event Plane Method to compute elliptic flow (v2)
  3. Calculate and plot v2 as a function of transverse momentum (pT) for charged particles
  4. Build identified particle v2 (pions vs protons) to demonstrate mass ordering at low pT
  5. Contrast results between central and semi-peripheral collisions to show geometric origin
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ampt_parser import iter_events, is_charged, get_pid_name
from kinematics import pseudorapidity, transverse_momentum, azimuthal_angle
from observables import v2_eventplane

outdir = os.path.dirname(__file__)
filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_39_sub100.dat')
events = [(h, p) for h, p in iter_events(filepath)]

print("=" * 60)
print("COLLECTIVE FLOW: ELLIPTIC FLOW (v2)")
print("=" * 60)

# Problem 1 & 2: Calculate overall charged v2 vs pT
print("PROBLEM 1 & 2: Elliptic Flow (v2) vs pT for Charged Hadrons")
print("-" * 50)
pt_bins = np.linspace(0.2, 2.5, 10)
pt_c, v2_c, v2_e = v2_eventplane(events, pt_bins=pt_bins, eta_cut=1.0)

fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(pt_c, v2_c, yerr=v2_e, fmt='o-', color='darkmagenta', linewidth=2, markersize=6, label='Charged Hadrons')
ax.set_xlabel(r'$p_T$ (GeV/c)', fontsize=12)
ax.set_ylabel(r'Elliptic Flow $v_2$', fontsize=12)
ax.set_title(r'Elliptic Flow $v_2(p_T)$ via Event-Plane Method', fontsize=14)
ax.set_ylim(-0.02, 0.25)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()
fig.savefig(os.path.join(outdir, 'day10_v2_charged.png'), dpi=150)
print("Saved: day10_v2_charged.png")

# Problem 3: Identified particle flow (pions vs protons) to demonstrate mass ordering
print("\nPROBLEM 3: Identified Particle v2 (Pions vs. Protons)")
print("-" * 50)

def compute_v2_pid(events, target_pids, pt_bins):
    pt_centers = 0.5 * (pt_bins[:-1] + pt_bins[1:])
    n_pt_bins = len(pt_centers)
    cos2_sum = np.zeros(n_pt_bins)
    counts = np.zeros(n_pt_bins)
    
    target_set = set(target_pids)
    
    for header, particles in events:
        pids = particles['pid']
        px = particles['px']
        py = particles['py']
        pz = particles['pz']
        
        # Calculate kinematics for all particles in event to determine Event Plane
        c_mask = [is_charged(pid) for pid in pids]
        c_eta = pseudorapidity(px[c_mask], py[c_mask], pz[c_mask])
        c_phi = azimuthal_angle(px[c_mask], py[c_mask])
        
        # Event plane angle using charged particles
        Q2x = np.sum(np.cos(2 * c_phi))
        Q2y = np.sum(np.sin(2 * c_phi))
        psi_EP = 0.5 * np.arctan2(Q2y, Q2x)
        
        # Now calculate v2 for our target PID particles in the event
        pid_mask = np.array([pid in target_set for pid in pids])
        if not np.any(pid_mask):
            continue
            
        p_pt = transverse_momentum(px[pid_mask], py[pid_mask])
        p_phi = azimuthal_angle(px[pid_mask], py[pid_mask])
        p_eta = pseudorapidity(px[pid_mask], py[pid_mask], pz[pid_mask])
        
        # Keep mid-rapidity particles
        eta_cut_mask = np.abs(p_eta) < 1.0
        p_pt = p_pt[eta_cut_mask]
        p_phi = p_phi[eta_cut_mask]
        
        for i in range(len(p_pt)):
            # Subtract autocorrelation from Q-vector if particle is charged
            # For simplicity, we just use the event plane psi_EP as-is for the PID subset
            dphi = p_phi[i] - psi_EP
            v2_i = np.cos(2 * dphi)
            
            pt_idx = np.searchsorted(pt_bins, p_pt[i]) - 1
            if 0 <= pt_idx < n_pt_bins:
                cos2_sum[pt_idx] += v2_i
                counts[pt_idx] += 1
                
    v2 = cos2_sum / np.maximum(counts, 1)
    v2_err = 1.0 / np.sqrt(np.maximum(counts, 1))
    return pt_centers, v2, v2_err

pion_pids = [211, -211]
proton_pids = [2212, -2212]

c_pion, v2_pion, err_pion = compute_v2_pid(events, pion_pids, pt_bins)
c_proton, v2_proton, err_proton = compute_v2_pid(events, proton_pids, pt_bins)

fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(c_pion, v2_pion, yerr=err_pion, fmt='o-', color='royalblue', linewidth=2, label='Pions ($\pi^\\pm$)')
ax.errorbar(c_proton, v2_proton, yerr=err_proton, fmt='s-', color='crimson', linewidth=2, label='Protons ($p/\\bar{p}$)')
ax.set_xlabel(r'$p_T$ (GeV/c)', fontsize=12)
ax.set_ylabel(r'Elliptic Flow $v_2$', fontsize=12)
ax.set_title('Identified Particle $v_2$ vs. $p_T$ (AMPT 39 GeV)', fontsize=14)
ax.set_ylim(-0.02, 0.25)
ax.legend(fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day10_v2_identified.png'), dpi=150)
print("Saved: day10_v2_identified.png")

# Problem 4 & 5: Centrality dependence of flow (central vs peripheral)
print("\nPROBLEM 4 & 5: Geometric Origin (Central vs. Peripheral Collisions)")
print("-" * 50)
# Split events into:
# Central (b < 4.0 fm)
# Semi-Peripheral (b >= 6.0 fm)
central_events = [e for e in events if e[0]['b'] < 4.0]
peripheral_events = [e for e in events if e[0]['b'] >= 6.0]

print(f"Number of central events (b < 4.0 fm): {len(central_events)}")
print(f"Number of semi-peripheral events (b >= 6.0 fm): {len(peripheral_events)}")

c_cent, v2_cent, err_cent = v2_eventplane(central_events, pt_bins=pt_bins, eta_cut=1.0)
c_per, v2_per, err_per = v2_eventplane(peripheral_events, pt_bins=pt_bins, eta_cut=1.0)

fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(c_cent, v2_cent, yerr=err_cent, fmt='o-', color='teal', linewidth=2, label='Central collisions ($b < 4$ fm)')
ax.errorbar(c_per, v2_per, yerr=err_per, fmt='s-', color='darkorange', linewidth=2, label='Semi-peripheral ($b \\ge 6$ fm)')
ax.set_xlabel(r'$p_T$ (GeV/c)', fontsize=12)
ax.set_ylabel(r'Elliptic Flow $v_2$', fontsize=12)
ax.set_title('Centrality/Geometry Dependence of Elliptic Flow', fontsize=14)
ax.set_ylim(-0.05, 0.3)
ax.legend(fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day10_v2_centrality.png'), dpi=150)
print("Saved: day10_v2_centrality.png")

print("\n✅ Day 10 exercises complete!")
