#!/usr/bin/env python3
"""
Day 11 — Medium Modification in AMPT: Knobs & Effects
=====================================================
Objectives:
  1. Understand parton cascade parameters in ZPC (screening mass mu, parton cross section sigma)
  2. Implement an analytical calculation for the relationship between mu, alpha_s, and sigma
  3. Formulate how to read and extract information on the interaction rate and mean free path of partons
  4. Compare the expected transverse momentum spectra and elliptic flow (v2) of Default vs String Melting
  5. Analyze how changing the parton cross section (e.g., 3mb vs 6mb) affects final-state flow
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

outdir = os.path.dirname(__file__)

print("=" * 60)
print("MEDIUM MODIFICATION AND PARTON CASCADE DYNAMICS")
print("=" * 60)

# Problem 1: Relationship between screening mass mu, alpha_s and parton cross section sigma
print("PROBLEM 1: Parton Cross Section Calculations")
print("-" * 50)
print("The leading-order perturbative QCD parton-parton elastic cross section in ZPC is:")
print("  σ_parton ≈ 9/2 * π * α_s^2 / μ^2")
print("where:")
print("  α_s = strong coupling constant")
print("  μ = screening mass (fm^-1 or GeV) [1 fm^-1 ≈ 0.1973 GeV]")
print("  σ_parton in mb [1 fm^2 = 10 mb]")

def compute_partonic_cross_section(alpha_s, mu_fm):
    # Convert mu from fm^-1 to GeV
    hbar_c = 0.19732697 # GeV*fm
    mu_gev = mu_fm * hbar_c
    
    # Calculate cross section in fm^2
    # σ_parton = (9/2) * pi * alpha_s^2 / mu^2
    # 1/mu^2 is in GeV^-2. We convert to fm^2 by multiplying by (hbar_c)^2
    sigma_fm2 = (4.5 * np.pi * alpha_s**2) / (mu_gev**2) * (hbar_c**2)
    
    # Convert fm^2 to mb (1 fm^2 = 10 mb)
    sigma_mb = sigma_fm2 * 10
    return sigma_mb

# Parameters from AMPT configurations
alphas_list = [0.33, 0.47, 0.33, 0.47]
mu_list = [2.265, 3.2264, 2.2814, 3.2] # in fm^-1

print(f"{'α_s':>6s} | {'μ (fm⁻¹)':>10s} | {'Expected σ (mb)':>16s} | {'Computed σ (mb)':>16s}")
print("-" * 60)
for a, m in zip(alphas_list, mu_list):
    computed = compute_partonic_cross_section(a, m)
    # Expected values typically used in AMPT:
    # (a=0.33, m=2.265) -> ~ 3 mb
    # (a=0.47, m=3.2264) -> ~ 3 mb
    # (a=0.33, m=2.2814) -> ~ 3 mb (slightly different)
    # (a=0.33, m=1.6) -> ~ 6 mb
    print(f"{a:6.2f} | {m:10.4f} | {3.0 if m>2 else 6.0:16.1f} | {computed:16.2f}")

# Problem 2: Compute Mean Free Path (λ) of Partons
print("\nPROBLEM 2: Parton Mean Free Path")
print("-" * 50)
print("The mean free path λ is given by: λ = 1 / (n * σ)")
print("where n is the parton density (partons/fm^3) and σ is the cross section (fm^2).")

densities = np.array([2.0, 5.0, 10.0]) # partons/fm^3 (from early to late QGP stage)
sigmas_mb = [3.0, 6.0, 10.0] # mb

print(f"{'Density n (fm⁻³)':<18s} | {'σ (mb)':<8s} | {'σ (fm²)':<8s} | {'Mean Free Path λ (fm)':<22s}")
print("-" * 65)
for n in densities:
    for s_mb in sigmas_mb:
        s_fm2 = s_mb / 10.0
        mfp = 1.0 / (n * s_fm2)
        print(f"{n:<18.1f} | {s_mb:<8.1f} | {s_fm2:<8.2f} | {mfp:<22.3f}")

# Problem 3: Conceptual simulation of Parton Energy Loss (dE/dx)
print("\nPROBLEM 3: Parton Energy Loss Model")
print("-" * 50)
print("Simple radiative energy loss: dE/dx = -k * x^p where p ≈ 1 (BDMPS model has p=1, pathlength squared dependence for average loss).")

x = np.linspace(0, 5, 100) # path length in fm
k_3mb = 0.5 # energy loss coefficient for 3 mb
k_6mb = 1.0 # energy loss coefficient for 6 mb

# Energy vs path length for initial 10 GeV parton
E0 = 10.0
E_3mb = E0 - 0.5 * k_3mb * x**2
E_6mb = E0 - 0.5 * k_6mb * x**2

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, E_3mb, label=r'$\sigma = 3$ mb ($k=0.5$ GeV/fm$^2$)', color='blue', linewidth=2)
ax.plot(x, E_6mb, label=r'$\sigma = 6$ mb ($k=1.0$ GeV/fm$^2$)', color='red', linestyle='--', linewidth=2)
ax.axhline(0, color='black', linestyle=':', alpha=0.5)
ax.set_xlabel('Path Length $x$ (fm)', fontsize=12)
ax.set_ylabel('Parton Energy $E(x)$ (GeV)', fontsize=12)
ax.set_title('Toy Model: Radiative Energy Loss in Partonic Medium', fontsize=14)
ax.legend(fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day11_energy_loss.png'), dpi=150)
print("Saved: day11_energy_loss.png")

# Problem 4: Hadronization effect (Coalescence vs Lund String fragmentation)
print("\nPROBLEM 4: Hadronization: String Melting vs Default Spectra Comparison")
print("-" * 50)
print("""
Default AMPT (Lund fragmentation):
- Energy stored in strings directly fragments into hadrons.
- Low pT is dominated by soft thermal-like fragmentation.
- Fewer mid-pT particles, lower collective flow.

String Melting AMPT (Quark Coalescence):
- Strings melt into constituent quarks (u, d, s, anti-quarks).
- Quarks undergo ZPC scattering, building up substantial collective flow.
- Nearby quarks in phase space recombine (coalesce) into mesons (q-qbar) and baryons (q-q-q).
- Leads to mass ordering, baryon-to-meson enhancement at intermediate pT, and stronger v2.
""")

# Problem 5: Plotting toy v2 dependency on parton cross section sigma
print("\nPROBLEM 5: Collective Flow Sensitivity to Parton Cross Section")
print("-" * 50)
# v2 builds up as partons scatter. More scattering = higher v2.
sigmas = np.linspace(0, 10, 50)
# Simple saturation model: v2 = v2_max * (1 - exp(-sigma / sigma_0))
v2_max = 0.15
sigma_0 = 4.0
v2_sat = v2_max * (1.0 - np.exp(-sigmas / sigma_0))

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(sigmas, v2_sat, color='forestgreen', linewidth=2.5)
ax.axvline(3.0, color='blue', linestyle=':', label='Typical default (3 mb)')
ax.axvline(6.0, color='red', linestyle=':', label='Strong melting (6 mb)')
ax.set_xlabel('Parton Cross Section $\\sigma_{parton}$ (mb)', fontsize=12)
ax.set_ylabel('Saturated Elliptic Flow $v_2$', fontsize=12)
ax.set_title('Collectivity Sensitivity to Partonic Scattering Cross Section', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.5)
fig.savefig(os.path.join(outdir, 'day11_v2_vs_sigma.png'), dpi=150)
print("Saved: day11_v2_vs_sigma.png")

print("\n✅ Day 11 exercises complete!")
