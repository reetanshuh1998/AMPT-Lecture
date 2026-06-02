#!/usr/bin/env python3
"""
observables.py — Physics observable builders for AMPT analysis.

Provides functions to compute standard heavy-ion observables:
- Charged particle multiplicity (Nch)
- dN/dη, dN/dy distributions
- pT spectra and invariant yield
- Mean pT
- Azimuthal flow (v2 event-plane method)
- Impact parameter distributions
"""

import numpy as np
from ampt_parser import is_charged, iter_events, CHARGED_PIDS
from kinematics import (
    transverse_momentum, rapidity, pseudorapidity,
    azimuthal_angle, energy, transverse_mass
)


# ============================================================
# Single-event observables
# ============================================================

def charged_multiplicity(particles):
    """
    Count charged particles in one event.
    Returns integer Nch.
    """
    count = 0
    for pid in particles['pid']:
        if is_charged(pid):
            count += 1
    return count


def get_charged_mask(particles):
    """Return boolean mask for charged particles."""
    mask = np.zeros(len(particles), dtype=bool)
    for i, pid in enumerate(particles['pid']):
        if is_charged(pid):
            mask[i] = True
    return mask


def get_pid_mask(particles, target_pids):
    """Return boolean mask for specific PIDs."""
    if isinstance(target_pids, int):
        target_pids = [target_pids]
    target_set = set(target_pids)
    return np.array([pid in target_set for pid in particles['pid']])


# ============================================================
# Multi-event histogram builders
# ============================================================

def dNdeta(events_particles, eta_range=(-6, 6), nbins=60, charged_only=True):
    """
    Build dN/dη distribution from a list of events.

    Parameters:
        events_particles: list of (header, particles) tuples
        eta_range: (min, max) pseudorapidity range
        nbins: number of bins
        charged_only: if True, only count charged particles

    Returns:
        (bin_centers, dNdeta_values, dNdeta_errors)
    """
    all_eta = []

    for header, particles in events_particles:
        if charged_only:
            mask = get_charged_mask(particles)
            sel = particles[mask]
        else:
            sel = particles

        eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
        all_eta.append(eta)

    all_eta = np.concatenate(all_eta)
    n_events = len(events_particles)

    counts, bin_edges = np.histogram(all_eta, bins=nbins, range=eta_range)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Normalize: dN/dη per event
    dndeta = counts / (n_events * bin_width)
    dndeta_err = np.sqrt(counts) / (n_events * bin_width)

    return bin_centers, dndeta, dndeta_err


def dNdy(events_particles, y_range=(-4, 4), nbins=40, charged_only=True):
    """
    Build dN/dy distribution from a list of events.

    Returns:
        (bin_centers, dNdy_values, dNdy_errors)
    """
    all_y = []

    for header, particles in events_particles:
        if charged_only:
            mask = get_charged_mask(particles)
            sel = particles[mask]
        else:
            sel = particles

        y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
        all_y.append(y)

    all_y = np.concatenate(all_y)
    n_events = len(events_particles)

    counts, bin_edges = np.histogram(all_y, bins=nbins, range=y_range)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    dndy = counts / (n_events * bin_width)
    dndy_err = np.sqrt(counts) / (n_events * bin_width)

    return bin_centers, dndy, dndy_err


def pt_spectrum(events_particles, pt_range=(0, 4), nbins=40,
                charged_only=True, target_pids=None, eta_cut=None):
    """
    Build transverse momentum spectrum (1/Nev) * dN/dpT.

    Parameters:
        events_particles: list of (header, particles) tuples
        pt_range: (min, max) pT range in GeV/c
        nbins: number of bins
        charged_only: count only charged particles
        target_pids: if set, filter to these PIDs only
        eta_cut: if set, apply |η| < eta_cut

    Returns:
        (bin_centers, spectrum, errors)
    """
    all_pt = []

    for header, particles in events_particles:
        if target_pids is not None:
            mask = get_pid_mask(particles, target_pids)
        elif charged_only:
            mask = get_charged_mask(particles)
        else:
            mask = np.ones(len(particles), dtype=bool)

        sel = particles[mask]

        if eta_cut is not None:
            eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
            eta_mask = np.abs(eta) < eta_cut
            sel = sel[eta_mask]

        pt = transverse_momentum(sel['px'], sel['py'])
        all_pt.append(pt)

    all_pt = np.concatenate(all_pt)
    n_events = len(events_particles)

    counts, bin_edges = np.histogram(all_pt, bins=nbins, range=pt_range)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    spectrum = counts / (n_events * bin_width)
    errors = np.sqrt(counts) / (n_events * bin_width)

    return bin_centers, spectrum, errors


def invariant_yield(events_particles, pt_range=(0.1, 4), nbins=30,
                    target_pids=None, y_cut=0.5):
    """
    Build invariant yield: (1/2π pT) * d²N/(dpT dy)

    From Book §5.2.4: The Lorentz-invariant cross-section is
    E d³σ/dp³ = (1/2π pT) d²σ/(dpT dy)

    Returns:
        (bin_centers, yield_values, yield_errors)
    """
    all_pt = []
    dy = 2 * y_cut  # rapidity window width

    for header, particles in events_particles:
        if target_pids is not None:
            mask = get_pid_mask(particles, target_pids)
        else:
            mask = get_charged_mask(particles)

        sel = particles[mask]

        # Apply rapidity cut
        y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
        y_mask = np.abs(y) < y_cut
        sel = sel[y_mask]

        pt = transverse_momentum(sel['px'], sel['py'])
        all_pt.append(pt)

    all_pt = np.concatenate(all_pt) if all_pt else np.array([])
    n_events = len(events_particles)

    counts, bin_edges = np.histogram(all_pt, bins=nbins, range=pt_range)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Invariant yield: 1/(2π pT) * dN/(dpT dy) / Nevents
    with np.errstate(divide='ignore', invalid='ignore'):
        inv_yield = counts / (n_events * 2 * np.pi * bin_centers * bin_width * dy)
        inv_yield_err = np.sqrt(counts) / (n_events * 2 * np.pi * bin_centers * bin_width * dy)

    inv_yield = np.nan_to_num(inv_yield)
    inv_yield_err = np.nan_to_num(inv_yield_err)

    return bin_centers, inv_yield, inv_yield_err


def mean_pt(events_particles, charged_only=True, target_pids=None, eta_cut=None):
    """
    Compute event-by-event mean pT.

    Returns:
        (mean_pt_values_per_event, overall_mean, overall_std)
    """
    event_means = []

    for header, particles in events_particles:
        if target_pids is not None:
            mask = get_pid_mask(particles, target_pids)
        elif charged_only:
            mask = get_charged_mask(particles)
        else:
            mask = np.ones(len(particles), dtype=bool)

        sel = particles[mask]

        if eta_cut is not None:
            eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
            sel = sel[np.abs(eta) < eta_cut]

        if len(sel) > 0:
            pt = transverse_momentum(sel['px'], sel['py'])
            event_means.append(np.mean(pt))

    event_means = np.array(event_means)
    return event_means, np.mean(event_means), np.std(event_means)


def v2_eventplane(events_particles, pt_bins=None, eta_cut=1.0):
    """
    Compute v2 using the event-plane method.

    v2 = <cos(2(φ - Ψ_EP))>

    where Ψ_EP is the event plane angle estimated from the particles
    themselves (with η-gap for sub-event resolution when possible).

    Returns:
        If pt_bins given: (pt_centers, v2_vs_pt, v2_errors)
        Else: (v2_integrated, v2_error)
    """
    if pt_bins is None:
        pt_bins = np.linspace(0.2, 3.0, 15)

    pt_centers = 0.5 * (pt_bins[:-1] + pt_bins[1:])
    n_pt_bins = len(pt_centers)

    # Accumulators
    cos2_sum = np.zeros(n_pt_bins)
    counts = np.zeros(n_pt_bins)

    for header, particles in events_particles:
        mask = get_charged_mask(particles)
        sel = particles[mask]

        eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
        eta_mask = np.abs(eta) < eta_cut
        sel = sel[eta_mask]
        eta = eta[eta_mask]

        if len(sel) < 3:
            continue

        phi = azimuthal_angle(sel['px'], sel['py'])
        pt = transverse_momentum(sel['px'], sel['py'])

        # Event plane from all particles
        Q2x = np.sum(np.cos(2 * phi))
        Q2y = np.sum(np.sin(2 * phi))
        psi_EP = 0.5 * np.arctan2(Q2y, Q2x)

        # Remove autocorrelation: for each particle, recompute EP without it
        for i in range(len(sel)):
            # Modified event plane without particle i
            q2x_mod = Q2x - np.cos(2 * phi[i])
            q2y_mod = Q2y - np.sin(2 * phi[i])
            psi_mod = 0.5 * np.arctan2(q2y_mod, q2x_mod)

            dphi = phi[i] - psi_mod
            v2_i = np.cos(2 * dphi)

            # Find pT bin
            pt_idx = np.searchsorted(pt_bins, pt[i]) - 1
            if 0 <= pt_idx < n_pt_bins:
                cos2_sum[pt_idx] += v2_i
                counts[pt_idx] += 1

    with np.errstate(divide='ignore', invalid='ignore'):
        v2 = cos2_sum / np.maximum(counts, 1)
        v2_err = 1.0 / np.sqrt(np.maximum(counts, 1))

    return pt_centers, v2, v2_err


def nch_distribution(events_particles, nch_range=None, nbins=50):
    """
    Build charged multiplicity distribution.

    Returns:
        (bin_centers, probability, raw_counts)
    """
    nch_list = []
    for header, particles in events_particles:
        nch_list.append(charged_multiplicity(particles))

    nch_array = np.array(nch_list)

    if nch_range is None:
        nch_range = (0, nch_array.max() + 10)

    counts, bin_edges = np.histogram(nch_array, bins=nbins, range=nch_range)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    probability = counts / len(nch_array)

    return bin_centers, probability, counts


def impact_parameter_distribution(headers, b_range=(0, 15), nbins=30):
    """
    Build impact parameter distribution.

    Returns:
        (bin_centers, counts_normalized)
    """
    b_values = np.array([h['b'] for h in headers])
    counts, bin_edges = np.histogram(b_values, bins=nbins, range=b_range)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    return bin_centers, counts / len(headers)


def npart_distribution(headers, nbins=30):
    """
    Build Npart distribution.

    Returns:
        (bin_centers, counts_normalized)
    """
    npart = np.array([h['Npart_proj'] + h['Npart_targ'] for h in headers])
    counts, bin_edges = np.histogram(npart, bins=nbins, range=(0, npart.max() + 10))
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    return bin_centers, counts / len(headers)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')

    print("observables.py loaded successfully.")
    print("Available functions:")
    for name in dir():
        if not name.startswith('_') and callable(eval(name)):
            print(f"  {name}")
