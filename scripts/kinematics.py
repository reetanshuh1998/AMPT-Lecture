#!/usr/bin/env python3
"""
kinematics.py — Relativistic kinematic variable calculators for AMPT analysis.

All formulas follow Chapter 5 of Sahoo, "Relativistic Kinematics".
Units: GeV for energy/momentum/mass, natural units (c=1).
"""

import numpy as np


def energy(px, py, pz, mass):
    """
    Relativistic energy: E = √(p² + m²)

    Parameters:
        px, py, pz: momentum components (GeV/c)
        mass: rest mass (GeV/c²)

    Returns:
        E in GeV
    """
    return np.sqrt(px**2 + py**2 + pz**2 + mass**2)


def transverse_momentum(px, py):
    """
    Transverse momentum: pT = √(px² + py²)

    This is the momentum component perpendicular to the beam axis.
    Key observable in heavy-ion collisions — insensitive to Lorentz boost
    along the beam direction.

    Returns:
        pT in GeV/c
    """
    return np.sqrt(px**2 + py**2)


def rapidity(px, py, pz, mass):
    """
    Rapidity: y = 0.5 * ln((E + pz) / (E - pz))

    From Book §5.2.2: Rapidity is additive under Lorentz boosts along
    the beam axis. The shape of the rapidity distribution dN/dy is
    invariant under such boosts — only the position shifts by y_cm.

    EXAMPLE: pion (m_pi ≈ 0.140 GeV) with pz = 1.0 GeV/c
    >>> y = rapidity(0.0, 0.0, 1.0, 0.140)
    >>> print(f"y = {y:.3f}")  # y ≈ 2.662

    INVARIANCE & ADDITIVITY:
    Linear addition under longitudinal Lorentz boosts:
    >>> y_boosted = y + y_beam

    Returns:
        y (dimensionless)
    """
    E = energy(px, py, pz, mass)
    # Clip to avoid division by zero or log of negative
    ratio = np.clip((E + pz) / np.maximum(E - pz, 1e-30), 1e-30, None)
    return 0.5 * np.log(ratio)


def pseudorapidity(px, py, pz):
    """
    Pseudorapidity: η = -ln(tan(θ/2)) = 0.5 * ln((|p| + pz) / (|p| - pz))

    From Book §5.2.3: In the limit m → 0 (or p >> m), η → y.
    Pseudorapidity depends only on the emission angle θ, not on mass.
    It is the experimentally preferred variable since detectors measure
    angles more easily than mass.

    Returns:
        η (dimensionless)
    """
    p = np.sqrt(px**2 + py**2 + pz**2)
    ratio = np.clip((p + pz) / np.maximum(p - pz, 1e-30), 1e-30, None)
    return 0.5 * np.log(ratio)


def transverse_mass(px, py, mass):
    """
    Transverse mass: mT = √(pT² + m²)

    From Book §5.2.7: The mT distribution follows an exponential shape
    for thermal spectra: dN/dmT ∝ exp(-mT/T), where T is the slope
    parameter related to the kinetic freeze-out temperature.

    Returns:
        mT in GeV/c²
    """
    pT = transverse_momentum(px, py)
    return np.sqrt(pT**2 + mass**2)


def azimuthal_angle(px, py):
    """
    Azimuthal angle: φ = atan2(py, px)

    Returns:
        φ in radians [-π, π]
    """
    return np.arctan2(py, px)


def polar_angle(px, py, pz):
    """
    Polar angle: θ = atan2(pT, pz)

    Returns:
        θ in radians [0, π]
    """
    pT = transverse_momentum(px, py)
    return np.arctan2(pT, pz)


def total_momentum(px, py, pz):
    """Total momentum magnitude |p| = √(px² + py² + pz²)"""
    return np.sqrt(px**2 + py**2 + pz**2)


def beta(px, py, pz, mass):
    """
    Velocity β = |p| / E = v/c

    Returns:
        β (dimensionless, 0 ≤ β < 1)
    """
    p = total_momentum(px, py, pz)
    E = energy(px, py, pz, mass)
    return p / np.maximum(E, 1e-30)


def gamma_factor(px, py, pz, mass):
    """
    Lorentz factor: γ = E / m = 1/√(1 - β²)

    Returns:
        γ (dimensionless, γ ≥ 1)
    """
    E = energy(px, py, pz, mass)
    return E / np.maximum(mass, 1e-30)


def invariant_mass_pair(px1, py1, pz1, m1, px2, py2, pz2, m2):
    """
    Invariant mass of a particle pair:
    M_inv = √((E1+E2)² - (px1+px2)² - (py1+py2)² - (pz1+pz2)²)

    This is a Lorentz scalar — same in all reference frames.

    Returns:
        M_inv in GeV/c²
    """
    E1 = energy(px1, py1, pz1, m1)
    E2 = energy(px2, py2, pz2, m2)

    E_tot = E1 + E2
    px_tot = px1 + px2
    py_tot = py1 + py2
    pz_tot = pz1 + pz2

    s = E_tot**2 - px_tot**2 - py_tot**2 - pz_tot**2
    return np.sqrt(np.maximum(s, 0))


def cms_energy(E_beam, m_target):
    """
    Center-of-mass energy for fixed-target:
    √s = √(m1² + m2² + 2*E_beam*m2)

    From Book Eq. (5.3).
    """
    return np.sqrt(2 * E_beam * m_target + m_target**2 + m_target**2)


def cms_energy_collider(E1, E2):
    """
    Center-of-mass energy for collider (head-on):
    √s ≈ 2√(E1*E2)

    From Book Eq. (5.6), in the ultra-relativistic limit.
    """
    return 2.0 * np.sqrt(E1 * E2)


def y_beam(sqrt_sNN, m_nucleon=0.938272):
    """
    Beam rapidity: y_beam = arccosh(√s_NN / (2*m_p))

    From Book Eq. (5.11).
    """
    return np.arccosh(sqrt_sNN / (2.0 * m_nucleon))


def feynman_x(pz, sqrt_s):
    """
    Feynman-x: x_F = 2*pz_cm / √s

    From Book §5.2.6: Feynman scaling variable.
    """
    return 2.0 * pz / sqrt_s


# ============================================================
# Convenience functions that work with structured particle arrays
# ============================================================

def compute_kinematics(particles):
    """
    Add kinematic variables to a particle structured array.

    Parameters:
        particles: numpy structured array with fields pid, px, py, pz, mass

    Returns:
        dict with arrays: pT, y, eta, phi, E, mT, p_total
    """
    px = particles['px']
    py = particles['py']
    pz = particles['pz']
    m = particles['mass']

    return {
        'pT': transverse_momentum(px, py),
        'y': rapidity(px, py, pz, m),
        'eta': pseudorapidity(px, py, pz),
        'phi': azimuthal_angle(px, py),
        'E': energy(px, py, pz, m),
        'mT': transverse_mass(px, py, m),
        'p_total': total_momentum(px, py, pz),
    }


if __name__ == "__main__":
    # Quick self-test
    print("=== Kinematics Self-Test ===")

    # A pion with px=0.3, py=0.4, pz=1.0, mass=0.140
    px, py, pz, m = 0.3, 0.4, 1.0, 0.140
    print(f"Particle: px={px}, py={py}, pz={pz}, m={m} GeV")
    print(f"  E   = {energy(px, py, pz, m):.4f} GeV")
    print(f"  pT  = {transverse_momentum(px, py):.4f} GeV/c")
    print(f"  y   = {rapidity(px, py, pz, m):.4f}")
    print(f"  η   = {pseudorapidity(px, py, pz):.4f}")
    print(f"  mT  = {transverse_mass(px, py, m):.4f} GeV/c²")
    print(f"  φ   = {azimuthal_angle(px, py):.4f} rad")
    print(f"  β   = {beta(px, py, pz, m):.4f}")
    print(f"  γ   = {gamma_factor(px, py, pz, m):.4f}")

    # Beam rapidity for RHIC 200 GeV
    print(f"\ny_beam(200 GeV) = {y_beam(200.0):.3f}")
    print(f"y_beam(7.7 GeV) = {y_beam(7.7):.3f}")
    print(f"y_beam(39 GeV)  = {y_beam(39.0):.3f}")
