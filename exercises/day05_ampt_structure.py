#!/usr/bin/env python3
"""
Day 05 — AMPT Model: Structure, Components, Physics
====================================================
Objectives:
  1. Walk through AMPT model structure (HIJING → ZPC → Hadronization → ART)
  2. Examine input.ampt parameters
  3. Understand ISOFT (Default=1, String Melting=4)
  4. Install AMPT (walkthrough steps)
  5. Compare Default vs String Melting conceptually
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np

print("=" * 60)
print("AMPT MODEL STRUCTURE")
print("=" * 60)

print("""
AMPT (A Multi-Phase Transport) Model Stages:
═══════════════════════════════════════════

   A + B  (Gold + Gold nuclei)
     │
     ▼
  ┌─────────────────┐
  │   HIJING v1.383 │  Initial conditions:
  │                 │  • Minijet partons (hard scatterings)
  │                 │  • Excited strings (soft interactions)
  │                 │  • Spectator nucleons
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   ZPC            │  Zhang's Parton Cascade:
  │                 │  • Elastic parton-parton scatterings
  │                 │  • σ_parton ∝ 1/μ² (screening mass)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐      ┌──────────────────────┐
  │  Hadronization   │      │  Version Choice:      │
  │                 │◄─────│  ISOFT=1: Lund String  │
  │                 │      │  ISOFT=4: Coalescence  │
  └────────┬────────┘      └──────────────────────┘
           │
           ▼
  ┌─────────────────┐
  │  Extended ART    │  Hadron Cascade:
  │                 │  • π, K, p, Λ, Ξ, Ω interactions
  │                 │  • Time = NTMAX × DT fm/c
  └────────┬────────┘
           │
           ▼
  Final Particle Spectra (ampt.dat)
""")

# Problem 1: input.ampt parameter study
print("PROBLEM 1: Key input.ampt Parameters")
print("-" * 50)
params = {
    "EFRM": ("200", "√s_NN in GeV (CMS frame)"),
    "FRAME": ("CMS", "Reference frame"),
    "PROJ/TARG": ("A/A", "Projectile/Target type"),
    "IAP/IZP": ("197/79", "Au: A=197, Z=79"),
    "NEVNT": ("100", "Number of events to generate"),
    "BMIN/BMAX": ("0/15", "Impact parameter range (fm)"),
    "ISOFT": ("1 or 4", "1=Default, 4=String Melting"),
    "NTMAX": ("150", "Hadron cascade time steps"),
    "DT": ("0.2", "Time step (fm/c), total time = 30 fm/c"),
    "Screening mass": ("2.265", "μ in fm⁻¹, σ_parton ∝ 1/μ²"),
    "dpcoal/drcoal": ("1d6/1d6", "Coalescence parameters (String Melting)"),
}

for key, (val, desc) in params.items():
    print(f"  {key:>18s} = {val:>8s}  │ {desc}")

# Problem 2: Parton cross section vs screening mass
print("\n\nPROBLEM 2: Parton Cross Section")
print("-" * 50)
mu_values = [2.265, 3.2264, 2.2814]
sigma_values = [3, 3, 6]  # mb
alpha_values = [0.33, 0.47, 0.33]

print("From AMPT documentation:")
print(f"{'μ (fm⁻¹)':>10s}  {'α':>6s}  {'σ (mb)':>8s}")
for mu, sigma, alpha in zip(mu_values, sigma_values, alpha_values):
    print(f"{mu:10.4f}  {alpha:6.2f}  {sigma:8d}")

# Problem 3: Installation steps
print("\n\nPROBLEM 3: AMPT Installation Walkthrough")
print("-" * 50)
print("""
Steps to install AMPT:
  1. Download from: http://myweb.ecu.edu/linz/ampt/
  2. Unzip: unzip ampt-v1.26t7-v2.26t7.zip
  3. Edit input.ampt with your settings
  4. Compile: make
  5. Run: sh exec &  or  ./exec
  
Required: Fortran compiler (gfortran)
  
Output files are in ana/ directory:
  • ampt.dat    — final-state particles (what we analyze!)
  • zpc.dat     — parton cascade output
  • npart*.dat  — participant info
""")

# Problem 4: Default vs String Melting
print("PROBLEM 4: Default vs String Melting Comparison")
print("-" * 50)
print("""
┌─────────────────┬──────────────────┬──────────────────┐
│                 │   Default (v1)   │  String Melt (v2)│
├─────────────────┼──────────────────┼──────────────────┤
│ ISOFT           │        1         │        4         │
│ Hadronization   │ Lund String Frag │ Quark Coalescence│
│ Partons         │ Minijets only    │ All strings melt │
│ QGP phase       │ Minimal          │ Full partonic    │
│ Coalescence     │ Not used         │ dpcoal, drcoal   │
│ Physics         │ Hadronic-dominant│ Partonic-dominant│
│ Best for        │ Low-energy       │ RHIC/LHC energies│
└─────────────────┴──────────────────┴──────────────────┘
""")

# Problem 5: Calculate cascade termination time
print("PROBLEM 5: Cascade Termination Time")
print("-" * 50)
NTMAX_values = [150, 200, 300]
DT_values = [0.2, 0.3]
print(f"{'NTMAX':>6s}  {'DT (fm/c)':>10s}  {'t_cut (fm/c)':>12s}")
for nt in NTMAX_values:
    for dt in DT_values:
        print(f"{nt:6d}  {dt:10.1f}  {nt*dt:12.1f}")

print("\n✅ Day 05 exercises complete!")
