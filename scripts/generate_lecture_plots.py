#!/usr/bin/env python3
"""
generate_lecture_plots.py — Master script to generate all plots used
in the 14-day AMPT lecture series.

Generates plots for:
  1. dN/dη distributions (7.7 and 39 GeV)
  2. dN/dy distributions
  3. pT spectra (all charged, and by PID)
  4. Invariant yield
  5. Impact parameter distributions
  6. Nch distributions
  7. Rapidity distributions
  8. v2 vs pT
  9. Energy comparison overlays
 10. Nch vs b correlation

Output: PDF files in plots/ directory (also PNG for preview)
"""

import os
import sys
import numpy as np

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from ampt_parser import iter_events, load_all_events, get_pid_name, CHARGED_PIDS
from kinematics import (
    transverse_momentum, rapidity, pseudorapidity, azimuthal_angle,
    energy, transverse_mass, y_beam
)
from observables import (
    dNdeta, dNdy, pt_spectrum, invariant_yield, mean_pt,
    v2_eventplane, nch_distribution, impact_parameter_distribution,
    npart_distribution, charged_multiplicity, get_charged_mask, get_pid_mask
)
from plotting import (
    setup_style, create_figure, save_figure, add_ampt_label,
    plot_dndeta, plot_dndy, plot_pt_spectrum, plot_invariant_yield,
    plot_v2, plot_histogram, COLORS, MARKERS, PARTICLE_LABELS
)

import matplotlib.pyplot as plt


def load_data(data_dir):
    """Load all events from both energy files."""
    print("=" * 60)
    print("Loading AMPT data...")
    print("=" * 60)

    data = {}
    files = {
        7.7: os.path.join(data_dir, "ampt_7.7_default.dat"),
        39: os.path.join(data_dir, "ampt_39_default.dat"),
    }

    for energy_gev, filepath in files.items():
        if not os.path.exists(filepath):
            print(f"  [SKIP] {filepath} not found")
            continue

        print(f"  Loading {energy_gev} GeV data...")
        events = []
        headers = []
        for header, particles in iter_events(filepath):
            headers.append(header)
            events.append((header, particles))

        data[energy_gev] = {'events': events, 'headers': headers}
        print(f"    Loaded {len(events)} events")

    return data


def plot_01_dndeta(data, plot_dir):
    """Plot 1: dN/dη for both energies."""
    print("\n[1] Generating dN/dη plot...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        eta_range = (-4, 4) if energy_gev < 20 else (-6, 6)
        centers, vals, errs = dNdeta(d['events'], eta_range=eta_range, nbins=40)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.errorbar(centers, vals, yerr=errs, fmt=MARKERS[i], color=colors[i],
                    markersize=5, capsize=2, label=label)

    ax.set_xlabel(r'$\eta$')
    ax.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$')
    ax.set_title('Charged Particle Pseudorapidity Distribution')
    ax.legend()
    add_ampt_label(ax, 0, x=0.68, y=0.40, additional='Au+Au, all centralities')
    save_figure(fig, os.path.join(plot_dir, 'dndeta_comparison.pdf'))


def plot_02_dndy(data, plot_dir):
    """Plot 2: dN/dy for both energies."""
    print("[2] Generating dN/dy plot...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        y_range = (-3, 3) if energy_gev < 20 else (-5, 5)
        centers, vals, errs = dNdy(d['events'], y_range=y_range, nbins=30)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.errorbar(centers, vals, yerr=errs, fmt=MARKERS[i], color=colors[i],
                    markersize=5, capsize=2, label=label)

    ax.set_xlabel(r'$y$')
    ax.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}y$')
    ax.set_title('Charged Particle Rapidity Distribution')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'dndy_comparison.pdf'))


def plot_03_pt_spectra(data, plot_dir):
    """Plot 3: pT spectra for both energies."""
    print("[3] Generating pT spectra...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        centers, vals, errs = pt_spectrum(d['events'], pt_range=(0, 4),
                                          nbins=40, eta_cut=1.0)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.errorbar(centers, vals, yerr=errs, fmt=MARKERS[i], color=colors[i],
                    markersize=5, capsize=2, label=label)

    ax.set_xlabel(r'$p_T$ (GeV/$c$)')
    ax.set_ylabel(r'$\frac{1}{N_{\mathrm{ev}}} \frac{\mathrm{d}N}{\mathrm{d}p_T}$ (GeV/$c$)$^{-1}$')
    ax.set_yscale('log')
    ax.set_title(r'Charged Particle $p_T$ Spectrum, $|\eta| < 1.0$')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'pt_spectrum_comparison.pdf'))


def plot_04_pt_by_pid(data, plot_dir):
    """Plot 4: pT spectra by particle species (π, K, p)."""
    print("[4] Generating PID-specific pT spectra...")

    pid_groups = {
        r'$\pi^{\pm}$': [211, -211],
        r'$K^{\pm}$': [321, -321],
        r'$p/\bar{p}$': [2212, -2212],
    }
    pid_colors = [COLORS['blue'], COLORS['green'], COLORS['red']]

    for energy_gev, d in sorted(data.items()):
        fig, ax = create_figure()

        for j, (plabel, pids) in enumerate(pid_groups.items()):
            centers, vals, errs = pt_spectrum(
                d['events'], pt_range=(0, 3.5), nbins=35,
                charged_only=False, target_pids=pids, eta_cut=1.0
            )
            ax.errorbar(centers, vals, yerr=errs, fmt=MARKERS[j],
                        color=pid_colors[j], markersize=5, capsize=2, label=plabel)

        ax.set_xlabel(r'$p_T$ (GeV/$c$)')
        ax.set_ylabel(r'$\frac{1}{N_{\mathrm{ev}}} \frac{\mathrm{d}N}{\mathrm{d}p_T}$ (GeV/$c$)$^{-1}$')
        ax.set_yscale('log')
        ax.set_title(f'Identified Particle $p_T$ Spectra, $|\\eta| < 1.0$')
        ax.legend()
        add_ampt_label(ax, energy_gev, x=0.60, y=0.95)
        save_figure(fig, os.path.join(plot_dir, f'pt_by_pid_{energy_gev}GeV.pdf'))


def plot_05_invariant_yield(data, plot_dir):
    """Plot 5: Invariant yield."""
    print("[5] Generating invariant yield...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        centers, vals, errs = invariant_yield(d['events'], pt_range=(0.2, 3.5),
                                              nbins=25, y_cut=0.5)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.errorbar(centers, vals, yerr=errs, fmt=MARKERS[i], color=colors[i],
                    markersize=5, capsize=2, label=label)

    ax.set_xlabel(r'$p_T$ (GeV/$c$)')
    ax.set_ylabel(r'$\frac{1}{2\pi p_T} \frac{\mathrm{d}^2 N}{\mathrm{d}p_T \mathrm{d}y}$ (GeV/$c$)$^{-2}$')
    ax.set_yscale('log')
    ax.set_title(r'Invariant Yield, $|y| < 0.5$')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'invariant_yield.pdf'))


def plot_06_impact_param(data, plot_dir):
    """Plot 6: Impact parameter distribution."""
    print("[6] Generating impact parameter distribution...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        b_max = max(h['b'] for h in d['headers']) + 1
        centers, vals = impact_parameter_distribution(d['headers'],
                                                       b_range=(0, b_max), nbins=25)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        width = centers[1] - centers[0] if len(centers) > 1 else 0.5
        ax.bar(centers + i * width * 0.4, vals, width=width * 0.4,
               color=colors[i], alpha=0.7, edgecolor='black', linewidth=0.5,
               label=label)

    ax.set_xlabel(r'$b$ (fm)')
    ax.set_ylabel('Probability')
    ax.set_title('Impact Parameter Distribution')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'impact_parameter.pdf'))


def plot_07_nch_distribution(data, plot_dir):
    """Plot 7: Charged multiplicity distribution."""
    print("[7] Generating Nch distribution...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        centers, prob, _ = nch_distribution(d['events'], nbins=40)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.step(centers, prob, where='mid', color=colors[i],
                linewidth=1.5, label=label)

    ax.set_xlabel(r'$N_{\mathrm{ch}}$')
    ax.set_ylabel('Probability')
    ax.set_title('Charged Particle Multiplicity Distribution')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'nch_distribution.pdf'))


def plot_08_nch_vs_b(data, plot_dir):
    """Plot 8: Nch vs impact parameter (centrality correlation)."""
    print("[8] Generating Nch vs b correlation...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        b_vals = []
        nch_vals = []
        for header, particles in d['events']:
            b_vals.append(header['b'])
            nch_vals.append(charged_multiplicity(particles))

        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.scatter(b_vals, nch_vals, c=colors[i], s=8, alpha=0.4, label=label)

    ax.set_xlabel(r'$b$ (fm)')
    ax.set_ylabel(r'$N_{\mathrm{ch}}$')
    ax.set_title(r'Charged Multiplicity vs Impact Parameter')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'nch_vs_b.pdf'))


def plot_09_v2(data, plot_dir):
    """Plot 9: v2 vs pT."""
    print("[9] Generating v2 vs pT...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        pt_centers, v2, v2_err = v2_eventplane(d['events'], eta_cut=1.0)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.errorbar(pt_centers, v2, yerr=v2_err, fmt=MARKERS[i], color=colors[i],
                    markersize=5, capsize=2, label=label)

    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel(r'$p_T$ (GeV/$c$)')
    ax.set_ylabel(r'$v_2\{EP\}$')
    ax.set_title(r'Elliptic Flow $v_2$ vs $p_T$, $|\eta| < 1.0$')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'v2_vs_pt.pdf'))


def plot_10_phi_distribution(data, plot_dir):
    """Plot 10: Azimuthal angle distribution."""
    print("[10] Generating φ distribution...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        all_phi = []
        for header, particles in d['events']:
            mask = get_charged_mask(particles)
            sel = particles[mask]
            phi = azimuthal_angle(sel['px'], sel['py'])
            all_phi.append(phi)
        all_phi = np.concatenate(all_phi)

        counts, edges = np.histogram(all_phi, bins=36, range=(-np.pi, np.pi))
        centers = 0.5 * (edges[:-1] + edges[1:])
        width = edges[1] - edges[0]
        norm_counts = counts / (len(d['events']) * width)

        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.step(centers, norm_counts, where='mid', color=colors[i],
                linewidth=1.5, label=label)

    ax.set_xlabel(r'$\phi$ (rad)')
    ax.set_ylabel(r'$\frac{1}{N_{\mathrm{ev}}} \frac{\mathrm{d}N}{\mathrm{d}\phi}$')
    ax.set_title('Azimuthal Angle Distribution')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'phi_distribution.pdf'))


def plot_11_npart(data, plot_dir):
    """Plot 11: Npart distribution."""
    print("[11] Generating Npart distribution...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        centers, vals = npart_distribution(d['headers'], nbins=30)
        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.step(centers, vals, where='mid', color=colors[i],
                linewidth=1.5, label=label)

    ax.set_xlabel(r'$N_{\mathrm{part}}$')
    ax.set_ylabel('Probability')
    ax.set_title('Number of Participants Distribution')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'npart_distribution.pdf'))


def plot_12_eta_y_comparison(data, plot_dir):
    """Plot 12: Compare η vs y for pions (showing they converge at high pT)."""
    print("[12] Generating η vs y comparison...")

    for energy_gev, d in sorted(data.items()):
        fig, axes = create_figure(1, 2, figsize=(14, 6))

        # Get pion data
        all_eta = []
        all_y = []
        all_pt = []
        for header, particles in d['events']:
            mask = get_pid_mask(particles, [211, -211])
            sel = particles[mask]
            all_eta.append(pseudorapidity(sel['px'], sel['py'], sel['pz']))
            all_y.append(rapidity(sel['px'], sel['py'], sel['pz'], sel['mass']))
            all_pt.append(transverse_momentum(sel['px'], sel['py']))

        all_eta = np.concatenate(all_eta)
        all_y = np.concatenate(all_y)
        all_pt = np.concatenate(all_pt)

        # Left: 2D scatter η vs y
        axes[0].hexbin(all_y, all_eta, gridsize=40, cmap='YlOrRd', mincnt=1)
        axes[0].plot([-6, 6], [-6, 6], 'k--', alpha=0.5, label=r'$\eta = y$')
        axes[0].set_xlabel(r'$y$')
        axes[0].set_ylabel(r'$\eta$')
        axes[0].set_title(r'$\eta$ vs $y$ for $\pi^{\pm}$')
        axes[0].legend()
        axes[0].set_aspect('equal')

        # Right: distributions overlaid
        y_range = (-3, 3) if energy_gev < 20 else (-5, 5)
        c_eta, edges_eta = np.histogram(all_eta, bins=40, range=y_range)
        c_y, edges_y = np.histogram(all_y, bins=40, range=y_range)
        bin_w = (y_range[1] - y_range[0]) / 40
        bc = np.linspace(y_range[0] + bin_w/2, y_range[1] - bin_w/2, 40)

        n_ev = len(d['events'])
        axes[1].step(bc, c_eta / (n_ev * bin_w), where='mid',
                     color=COLORS['blue'], linewidth=1.5, label=r'$\mathrm{d}N/\mathrm{d}\eta$')
        axes[1].step(bc, c_y / (n_ev * bin_w), where='mid',
                     color=COLORS['red'], linewidth=1.5, label=r'$\mathrm{d}N/\mathrm{d}y$')
        axes[1].set_xlabel(r'$\eta$ or $y$')
        axes[1].set_ylabel(r'$\mathrm{d}N/\mathrm{d}\eta$ or $\mathrm{d}N/\mathrm{d}y$')
        axes[1].set_title(r'$\pi^{\pm}$: $\eta$ vs $y$ distributions')
        axes[1].legend()

        fig.suptitle(f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV, AMPT Au+Au', fontsize=14)
        fig.tight_layout()
        save_figure(fig, os.path.join(plot_dir, f'eta_vs_y_{energy_gev}GeV.pdf'))


def plot_13_mean_pt_vs_nch(data, plot_dir):
    """Plot 13: Mean pT vs Nch."""
    print("[13] Generating <pT> vs Nch...")
    fig, ax = create_figure()

    colors = [COLORS['blue'], COLORS['red']]
    for i, (energy_gev, d) in enumerate(sorted(data.items())):
        nch_list = []
        mpt_list = []
        for header, particles in d['events']:
            mask = get_charged_mask(particles)
            sel = particles[mask]
            if len(sel) > 0:
                pt = transverse_momentum(sel['px'], sel['py'])
                nch_list.append(len(sel))
                mpt_list.append(np.mean(pt))

        label = f'$\\sqrt{{s_{{NN}}}}$ = {energy_gev} GeV'
        ax.scatter(nch_list, mpt_list, c=colors[i], s=8, alpha=0.4, label=label)

    ax.set_xlabel(r'$N_{\mathrm{ch}}$')
    ax.set_ylabel(r'$\langle p_T \rangle$ (GeV/$c$)')
    ax.set_title(r'Mean $p_T$ vs Charged Multiplicity')
    ax.legend()
    save_figure(fig, os.path.join(plot_dir, 'mean_pt_vs_nch.pdf'))


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_dir, "Data")
    plot_dir = os.path.join(project_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)

    data = load_data(data_dir)

    if not data:
        print("ERROR: No data files found!")
        sys.exit(1)

    plot_01_dndeta(data, plot_dir)
    plot_02_dndy(data, plot_dir)
    plot_03_pt_spectra(data, plot_dir)
    plot_04_pt_by_pid(data, plot_dir)
    plot_05_invariant_yield(data, plot_dir)
    plot_06_impact_param(data, plot_dir)
    plot_07_nch_distribution(data, plot_dir)
    plot_08_nch_vs_b(data, plot_dir)
    plot_09_v2(data, plot_dir)
    plot_10_phi_distribution(data, plot_dir)
    plot_11_npart(data, plot_dir)
    plot_12_eta_y_comparison(data, plot_dir)
    plot_13_mean_pt_vs_nch(data, plot_dir)

    print("\n" + "=" * 60)
    print(f"All plots generated in: {plot_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
