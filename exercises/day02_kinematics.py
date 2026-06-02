#!/usr/bin/env python3
"""
Day 02 — Relativistic Kinematics I: Four-Vectors and √s
========================================================

Objectives (from Book §5.1):
  1. Compute √s for different collision systems
  2. Verify √s_NN formula for fixed-target vs collider
  3. Calculate Lorentz factor γ for different energies
  4. Compare CMS vs Lab frame energies
  5. Compute beam rapidity y_beam

Reference: Sahoo, Chapter 5, Section 5.1
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
from kinematics import y_beam, cms_energy_collider

m_p = 0.938272  # proton mass in GeV

# ============================================================
# Problem 1: √s_NN for RHIC and LHC energies
# ============================================================
print("=" * 60)
print("PROBLEM 1: Center-of-mass energies")
print("=" * 60)

# Collider mode: √s = 2E (for equal beams, ultra-relativistic)
energies_per_beam = [3.85, 5.75, 9.8, 13.5, 19.5, 100]  # GeV per nucleon
print(f"\n{'E_beam (GeV/A)':>15s}  {'√s_NN (GeV)':>12s}")
print("-" * 30)
for E in energies_per_beam:
    sqrtS = 2 * E  # ultra-relativistic approx
    sqrtS_exact = np.sqrt(2 * m_p**2 + 2 * E * m_p + 2 * np.sqrt(E**2 - m_p**2) * E)
    # Actually for collider: √s = 2*E
    sqrtS_collider = 2 * E
    print(f"{E:15.2f}  {sqrtS_collider:12.2f}")


# ============================================================
# Problem 2: Fixed-target vs Collider comparison
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 2: Fixed-target vs Collider")
print("=" * 60)
print("\nFrom Book Eq. (5.3): √s = √(m1² + m2² + 2*E_lab*m2)")
print("From Book Eq. (5.6): √s ≈ 2*E (collider, head-on)\n")

E_lab_values = [10, 30, 100, 158, 400]  # GeV per nucleon
print(f"{'E_lab (GeV)':>12s}  {'√s_FT (GeV)':>12s}  {'√s_Coll (GeV)':>14s}  {'Ratio':>8s}")
print("-" * 50)
for E_lab in E_lab_values:
    sqrtS_ft = np.sqrt(2 * m_p**2 + 2 * E_lab * m_p)
    sqrtS_coll = 2 * E_lab
    print(f"{E_lab:12.1f}  {sqrtS_ft:12.2f}  {sqrtS_coll:14.2f}  {sqrtS_coll/sqrtS_ft:8.1f}x")


# ============================================================
# Problem 3: Lorentz factor γ_cm
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 3: Lorentz factor γ")
print("=" * 60)
print("\nFrom Book Eq. (5.12): γ = √s_NN / (2*m_p)\n")

sqrtS_values = [7.7, 11.5, 14.5, 19.6, 27, 39, 62.4, 200, 2760, 5360]
print(f"{'√s_NN (GeV)':>12s}  {'γ':>10s}  {'β':>10s}  {'v/c':>8s}")
print("-" * 44)
for sqrtS in sqrtS_values:
    gamma = sqrtS / (2 * m_p)
    beta = np.sqrt(1 - 1/gamma**2)
    print(f"{sqrtS:12.1f}  {gamma:10.2f}  {beta:10.6f}  {beta:8.6f}")


# ============================================================
# Problem 4: Beam rapidity y_beam
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 4: Beam rapidity y_beam")
print("=" * 60)
print("\nFrom Book Eq. (5.11): y_beam = arccosh(√s_NN / (2*m_p))\n")

print(f"{'√s_NN (GeV)':>12s}  {'y_beam':>10s}  {'y_target':>10s}")
print("-" * 36)
for sqrtS in [7.7, 19.6, 39, 62.4, 200, 5360]:
    yb = y_beam(sqrtS)
    print(f"{sqrtS:12.1f}  {yb:10.3f}  {-yb:10.3f}")

print("\n→ The rapidity gap (2*y_beam) determines how much rapidity")
print("  space is available for particle production.")


# ============================================================
# Problem 5: Heavy-ion √s_NN from p+p energy
# ============================================================
print("\n" + "=" * 60)
print("PROBLEM 5: √s_NN for different nuclei (Book Eq. 5.15)")
print("=" * 60)
print("\n√s_NN = √s_pp × √(Z1*Z2 / (A1*A2))\n")

sqrtS_pp = 13600  # 13.6 TeV for LHC

nuclei = [
    ("Pb+Pb", 82, 208, 82, 208),
    ("Au+Au", 79, 197, 79, 197),
    ("Xe+Xe", 54, 131, 54, 131),
    ("O+O", 8, 16, 8, 16),
    ("p+Pb", 1, 1, 82, 208),
]

print(f"{'System':>10s}  {'Z1/A1':>8s}  {'Z2/A2':>8s}  {'Factor':>8s}  {'√s_NN (GeV)':>12s}")
print("-" * 55)
for name, Z1, A1, Z2, A2 in nuclei:
    factor = np.sqrt(Z1 * Z2 / (A1 * A2))
    sqrtS_NN = sqrtS_pp * factor
    print(f"{name:>10s}  {Z1/A1:8.4f}  {Z2/A2:8.4f}  {factor:8.4f}  {sqrtS_NN:12.1f}")

print("\n✅ Day 02 exercises complete!")
