#!/usr/bin/env python3
"""
Day 13 — Advanced Analysis: Correlations & Performance
======================================================
Objectives:
  1. Understand two-particle angular correlations (delta phi = phi_1 - phi_2)
  2. Implement an azimuthal correlation algorithm to calculate the correlation function C(delta phi)
  3. Identify the "near-side" (delta phi ≈ 0) jet peak and the "away-side" (delta phi ≈ pi) di-jet back-to-back peak
  4. Perform optimization of correlation calculations via NumPy vectorization
  5. Save correlation plots showing the structures representing collective flow (cos 2dphi modulation)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import time
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ampt_parser import iter_events, is_charged
from kinematics import pseudorapidity, transverse_momentum, azimuthal_angle

outdir = os.path.dirname(__file__)
filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_39_sub100.dat')
events = [(h, p) for h, p in iter_events(filepath)]

print("=" * 60)
print("ADVANCED ANALYSIS: TWO-PARTICLE AZIMUTHAL CORRELATIONS")
print("=" * 60)

# Problem 1 & 2: Two-particle correlation algorithm (delta phi = phi_1 - phi_2)
print("PROBLEM 1 & 2: Computing Azimuthal Correlation Function C(Δφ)")
print("-" * 50)

def compute_dphi_distribution(events, pt_min=0.5, pt_max=2.0, eta_max=1.0):
    dphi_list = []
    
    for h, particles in events:
        pids = particles['pid']
        px = particles['px']
        py = particles['py']
        pz = particles['pz']
        
        eta = pseudorapidity(px, py, pz)
        pt = transverse_momentum(px, py)
        phi = azimuthal_angle(px, py)
        
        c_mask = [is_charged(pid) for pid in pids]
        sel_mask = np.logical_and(c_mask, np.abs(eta) < eta_max)
        sel_mask = np.logical_and(sel_mask, pt > pt_min)
        sel_mask = np.logical_and(sel_mask, pt < pt_max)
        
        event_phi = phi[sel_mask]
        n_sel = len(event_phi)
        
        if n_sel < 2:
            continue
            
        # Two-particle combinations in the same event
        # Double loop optimization using meshgrid
        phi1, phi2 = np.meshgrid(event_phi, event_phi)
        # Lower triangle indices to avoid self-correlations and double-counting
        idx = np.tril_indices(n_sel, k=-1)
        
        dphi = phi1[idx] - phi2[idx]
        
        # Keep delta phi within [-pi, pi] or [0, 2*pi]
        # Standard convention is to fold it to [-pi/2, 3*pi/2] or [-pi, pi]
        # We will map to [-pi/2, 3*pi/2]
        dphi = np.where(dphi < -np.pi/2, dphi + 2*np.pi, dphi)
        dphi = np.where(dphi >= 1.5*np.pi, dphi - 2*np.pi, dphi)
        
        dphi_list.extend(dphi)
        
    return np.array(dphi_list)

# Problem 3: Save and interpret azimuthal correlation plot
print("\nPROBLEM 3: Running correlation analysis and saving plots...")
print("-" * 50)

dphi_arr = compute_dphi_distribution(events, pt_min=0.5, pt_max=2.0)

fig, ax = plt.subplots(figsize=(8, 6))
bins = np.linspace(-np.pi/2, 1.5*np.pi, 40)
bin_centers = 0.5 * (bins[:-1] + bins[1:])
counts, _ = np.histogram(dphi_arr, bins=bins)

# Normalize by the number of trigger particles or scale so it's readable
norm_counts = counts / (len(events) * (bins[1] - bins[0]))

ax.plot(bin_centers, norm_counts, 'o-', color='darkgreen', linewidth=2)
ax.set_xlabel(r'$\Delta\phi = \phi_1 - \phi_2$ (rad)', fontsize=12)
ax.set_ylabel(r'$C(\Delta\phi)$ (Normalized Yield)', fontsize=12)
ax.set_title('Two-Particle Azimuthal Correlation $C(\\Delta\\phi)$ (AMPT 39 GeV)', fontsize=14)

# Draw indicator labels
ax.axvline(0, color='red', linestyle='--', alpha=0.7)
ax.text(0.1, np.max(norm_counts)*0.9, 'Near-Side Peak\n(Jet)', color='red', fontsize=10)
ax.axvline(np.pi, color='blue', linestyle='--', alpha=0.7)
ax.text(np.pi+0.1, np.max(norm_counts)*0.85, 'Away-Side Peak\n(Di-jet / Back-to-back)', color='blue', fontsize=10)

ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day13_azimuthal_correlation.png'), dpi=150)
print("Saved: day13_azimuthal_correlation.png")

# Problem 4: Performance optimization demonstration
print("\nPROBLEM 4: Performance Benchmarking (Vectorized vs. Iterative)")
print("-" * 50)

# Create a dummy large event to benchmark
dummy_phi = np.random.uniform(-np.pi, np.pi, 500)

# 1. Iterative method (slow)
def slow_correlation(phi_arr):
    n = len(phi_arr)
    dphi = []
    for i in range(n):
        for j in range(i):
            dp = phi_arr[i] - phi_arr[j]
            if dp < -np.pi/2:
                dp += 2*np.pi
            elif dp >= 1.5*np.pi:
                dp -= 2*np.pi
            dphi.append(dp)
    return dphi

# 2. Vectorized method (fast)
def fast_correlation(phi_arr):
    n = len(phi_arr)
    phi1, phi2 = np.meshgrid(phi_arr, phi_arr)
    idx = np.tril_indices(n, k=-1)
    dphi = phi1[idx] - phi2[idx]
    dphi = np.where(dphi < -np.pi/2, dphi + 2*np.pi, dphi)
    dphi = np.where(dphi >= 1.5*np.pi, dphi - 2*np.pi, dphi)
    return dphi

t0 = time.time()
res_slow = slow_correlation(dummy_phi)
t_slow = time.time() - t0

t0 = time.time()
res_fast = fast_correlation(dummy_phi)
t_fast = time.time() - t0

print(f"Num combinations: {len(res_slow)}")
print(f"Iterative calculation time:  {t_slow:.4f} seconds")
print(f"Vectorized calculation time: {t_fast:.4f} seconds")
print(f"Speedup factor: {t_slow / max(t_fast, 1e-6):.1f}x !")

# Problem 5: Discuss flow modulation (cos 2dphi)
print("\nPROBLEM 5: Collective Flow Modulation (v2)")
print("-" * 50)
print("""
In heavy-ion collisions, the correlation function can be expanded as a Fourier series:
  C(Δφ) ∝ 1 + 2 v_1^2 cos(Δφ) + 2 v_2^2 cos(2Δφ) + 2 v_3^2 cos(3Δφ) + ...
  
where:
  - v_2 is the elliptic flow parameter we calculated on Day 10.
  - The v_2^2 term manifests as a cos(2Δφ) modulation (two symmetric ridges at Δφ = 0 and Δφ = π).
  - This ridge-like correlation structure was one of the key discoveries at RHIC and LHC, indicating the presence of strongly interacting partonic medium (QGP).
""")

print("\n✅ Day 13 exercises complete!")
