#!/usr/bin/env python3
"""
analyze_day2.py — Day 2 Physics Analysis Script:
1. Calculates and compares dN/dy vs dN/dη for charged particles.
2. Extracts the mass-dependent mid-rapidity dip in dN/dη for pions, kaons, and protons.
3. Computes pion rapidity width σ_y and compares with Landau hydrodynamic model predictions.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Insert scripts folder to access parsing and plotting libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from ampt_parser import iter_events, get_pid_name, is_charged
from kinematics import rapidity, pseudorapidity, transverse_momentum, transverse_mass
from plotting import setup_style, COLORS, save_figure

# Paths to data subsets
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets')
FILE_7_7 = os.path.join(DATA_DIR, 'ampt_7.7_sub100.dat')
FILE_39 = os.path.join(DATA_DIR, 'ampt_39_sub100.dat')

# Check if data files exist
for path in [FILE_7_7, FILE_39]:
    if not os.path.exists(path):
        print(f"Error: Data file not found at {path}", file=sys.stderr)
        print("Please verify the Data path.", file=sys.stderr)
        sys.exit(1)


def analyze_dndy_vs_dndeta():
    """Generates Plot 1: dN/dy vs dN/dη for charged particles at 7.7 and 39 GeV."""
    print("Generating Plot 1: dN/dy vs dN/dη...")
    setup_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    for filepath, energy_val, ax in zip([FILE_7_7, FILE_39], [7.7, 39.0], [ax1, ax2]):
        all_y = []
        all_eta = []
        event_count = 0

        for header, particles in iter_events(filepath, max_events=100):
            # Mask for charged particles
            charged_mask = np.array([is_charged(pid) for pid in particles['pid']])
            sel = particles[charged_mask]
            if len(sel) == 0:
                continue

            y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
            eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
            all_y.extend(y)
            all_eta.extend(eta)
            event_count += 1

        # Histograms
        bins = np.linspace(-4.5, 4.5, 45)
        bin_width = bins[1] - bins[0]
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        y_counts, _ = np.histogram(all_y, bins=bins)
        eta_counts, _ = np.histogram(all_eta, bins=bins)

        # Normalize to yield per event per unit rapidity
        y_yield = y_counts / (event_count * bin_width)
        eta_yield = eta_counts / (event_count * bin_width)
        y_err = np.sqrt(y_counts) / (event_count * bin_width)
        eta_err = np.sqrt(eta_counts) / (event_count * bin_width)

        ax.errorbar(bin_centers, y_yield, yerr=y_err, fmt='o', color=COLORS['red'],
                    markersize=5, capsize=2, label=r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}y$')
        ax.errorbar(bin_centers, eta_yield, yerr=eta_err, fmt='s', color=COLORS['blue'],
                    markersize=5, capsize=2, label=r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$')

        ax.set_xlabel(r'$y$ or $\eta$', fontsize=16)
        ax.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}(y\ \mathrm{or}\ \eta)$', fontsize=16)
        ax.set_title(f'AMPT Charged Multiplicity ($\\sqrt{{s_{{NN}}}}$ = {energy_val} GeV)', fontsize=14)
        ax.set_xlim(-4.2, 4.2)
        ax.legend(frameon=True, fontsize=12)
        ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_dndy_vs_dndeta.png'))


def analyze_species_dip():
    """Generates Plot 2: Mass-dependent mid-rapidity dip in dN/dη at 39 GeV."""
    print("Generating Plot 2: Mass-dependent mid-rapidity dip in dN/dη...")
    setup_style()
    fig, ax = plt.subplots(figsize=(9, 6.5))

    species = {
        'Pions ($\pi^\pm$)': {'pid': 211, 'color': COLORS['blue'], 'marker': 'o'},
        'Kaons ($K^\pm$)': {'pid': 321, 'color': COLORS['green'], 'marker': 's'},
        'Protons ($p/\bar{p}$)': {'pid': 2212, 'color': COLORS['red'], 'marker': '^'}
    }

    # Bins close to mid-rapidity to resolve the shape
    bins = np.linspace(-2.5, 2.5, 35)
    bin_width = bins[1] - bins[0]
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    for name, info in species.items():
        all_eta = []
        event_count = 0

        for header, particles in iter_events(FILE_39, max_events=100):
            # Select species by absolute PID
            mask = np.abs(particles['pid']) == info['pid']
            sel = particles[mask]
            if len(sel) == 0:
                continue

            eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
            all_eta.extend(eta)
            event_count += 1

        counts, _ = np.histogram(all_eta, bins=bins)
        yield_val = counts / (event_count * bin_width)
        err = np.sqrt(counts) / (event_count * bin_width)

        # Normalize to the maximum value of each species to compare shape/dips directly
        max_val = np.max(yield_val)
        yield_norm = yield_val / max_val
        err_norm = err / max_val

        ax.errorbar(bin_centers, yield_norm, yerr=err_norm, fmt=info['marker'], color=info['color'],
                    markersize=6, capsize=2, elinewidth=1, label=name)

    ax.set_xlabel(r'Pseudorapidity $\eta$', fontsize=16)
    ax.set_ylabel(r'Normalized yield $(\mathrm{d}N/\mathrm{d}\eta) / \mathrm{max}$', fontsize=16)
    ax.set_title(r'Mass-Dependent Mid-rapidity Dip in $\mathrm{d}N/\mathrm{d}\eta$ ($\sqrt{s_{NN}} = 39$ GeV)', fontsize=14)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(0.4, 1.15)
    ax.legend(frameon=True, fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5)

    # Inset or text explaining the physics
    physics_text = (
        r"$\mathbf{Jacobian\ Effect:}$" "\n"
        r"$\frac{\mathrm{d}N}{\mathrm{d}\eta} = \beta_{L} \frac{\mathrm{d}N}{\mathrm{d}y} = \sqrt{1 - \frac{m_0^2}{m_T^2\cosh^2 y}} \frac{\mathrm{d}N}{\mathrm{d}y}$" "\n"
        r"$\mathrm{At\ } \eta = 0 \Rightarrow J = p_T / m_T < 1$" "\n"
        r"$\bullet\ \mathrm{Pions\ (light): } J \approx 1 \rightarrow \mathrm{No\ Dip}$" "\n"
        r"$\bullet\ \mathrm{Protons\ (heavy): } J \ll 1 \rightarrow \mathrm{Deep\ Dip}$"
    )
    ax.text(-2.0, 0.45, physics_text, fontsize=11, fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1', alpha=0.9))

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_species_eta_dip.png'))


def analyze_landau_width():
    """Generates Plot 3: Pion rapidity distribution width compared with Landau model predictions."""
    print("Generating Plot 3: Landau rapidity width comparison...")
    setup_style()
    fig, ax = plt.subplots(figsize=(9, 6.5))

    # Calculate actual pion rapidity widths from 7.7 and 39 GeV data
    ampt_widths = {}
    for filepath, energy_val in zip([FILE_7_7, FILE_39], [7.7, 39.0]):
        all_y = []
        for header, particles in iter_events(filepath, max_events=100):
            # Select pions
            mask = np.abs(particles['pid']) == 211
            sel = particles[mask]
            if len(sel) == 0:
                continue
            y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
            all_y.extend(y)
        
        # Calculate standard deviation
        ampt_widths[energy_val] = np.std(all_y)
        print(f"  AMPT Pion rapidity width σ_y at {energy_val} GeV = {ampt_widths[energy_val]:.4f}")

    # Generate Landau model curves
    # √s_NN range from 3 GeV to 100 GeV
    sqrtS_arr = np.linspace(3, 100, 200)
    m_p = 0.938272

    # Ideal Landau width (cs^2 = 1/3)
    # σ_y = √(ln(√s / 2m_p))
    width_ideal = np.sqrt(np.maximum(np.log(sqrtS_arr / (2 * m_p)), 0))

    # Realistic Landau width for QGP/hadron gas (e.g. cs^2 = 0.20)
    # σ_y^2 = (8/3) * (cs^2 / (1 - cs^4)) * ln(√s / 2m_p)
    cs2 = 0.20
    prefactor = (8.0 / 3.0) * (cs2 / (1.0 - cs2**2))
    width_realistic = np.sqrt(np.maximum(prefactor * np.log(sqrtS_arr / (2 * m_p)), 0))

    # Plot theoretical curves
    ax.plot(sqrtS_arr, width_ideal, '-', color=COLORS['red'], linewidth=2,
            label=r'Landau Ideal Gas ($c_s^2 = 1/3$)')
    ax.plot(sqrtS_arr, width_realistic, '--', color=COLORS['blue'], linewidth=2,
            label=r'Landau Hadron Gas ($c_s^2 = 0.20$)')

    # Plot AMPT results
    ax.scatter([7.7], [ampt_widths[7.7]], color=COLORS['purple'], marker='o', s=120, zorder=5,
               label=r'AMPT $\pi^\pm$ ($\sqrt{s_{NN}}$ = 7.7 GeV)')
    ax.scatter([39.0], [ampt_widths[39.0]], color=COLORS['green'], marker='D', s=100, zorder=5,
               label=r'AMPT $\pi^\pm$ ($\sqrt{s_{NN}}$ = 39 GeV)')

    ax.set_xlabel(r'Center-of-mass energy $\sqrt{s_{NN}}$ (GeV)', fontsize=16)
    ax.set_ylabel(r'Rapidity Width $\sigma_y$', fontsize=16)
    ax.set_title(r'Pion Rapidity Width $\sigma_y$ vs. Landau Hydrodynamics', fontsize=14)
    ax.set_xlim(3, 85)
    ax.set_ylim(0.3, 2.5)
    ax.set_xscale('log') # Log scale is perfect for energy ranges
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xticks([3, 5, 10, 20, 39, 62.4, 80])
    ax.legend(frameon=True, fontsize=11, loc='upper left')
    ax.grid(True, which='both', linestyle=':', alpha=0.5)

    # Inset text
    formula_text = (
        r"$\mathbf{Landau\ Hydrodynamic\ Prediction:}$" "\n"
        r"$\sigma_y^2 = \frac{8}{3} \frac{c_s^2}{1 - c_s^4} \ln\left(\frac{\sqrt{s_{NN}}}{2 m_p}\right)$" "\n\n"
        r"$\bullet\ \sigma_y(7.7\ \mathrm{GeV}) = $ " + f"{ampt_widths[7.7]:.3f}\n"
        r"$\bullet\ \sigma_y(39\ \mathrm{GeV}) = $ " + f"{ampt_widths[39.0]:.3f}"
    )
    ax.text(25, 0.45, formula_text, fontsize=10, fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1', alpha=0.9))

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_landau_width.png'))


if __name__ == "__main__":
    print("Starting Day 2 Data Analysis on subsets...")
    analyze_dndy_vs_dndeta()
    analyze_species_dip()
    analyze_landau_width()
    print("Day 2 Analysis complete. Plots saved in day2 folder.")
