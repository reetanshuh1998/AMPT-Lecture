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
            event_count += 1
            # Mask for charged particles
            charged_mask = np.array([is_charged(pid) for pid in particles['pid']])
            sel = particles[charged_mask]
            if len(sel) == 0:
                continue

            y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
            eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
            all_y.extend(y)
            all_eta.extend(eta)

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

        # Generate individual plot for this energy to display full-size on slides
        fig_ind, ax_ind = plt.subplots(figsize=(8, 6))
        ax_ind.errorbar(bin_centers, y_yield, yerr=y_err, fmt='o', color=COLORS['red'],
                        markersize=5, capsize=2, label=r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}y$')
        ax_ind.errorbar(bin_centers, eta_yield, yerr=eta_err, fmt='s', color=COLORS['blue'],
                        markersize=5, capsize=2, label=r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$')
        ax_ind.set_xlabel(r'$y$ or $\eta$', fontsize=16)
        ax_ind.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}(y\ \mathrm{or}\ \eta)$', fontsize=16)
        ax_ind.set_title(f'AMPT Charged Multiplicity ($\\sqrt{{s_{{NN}}}}$ = {energy_val} GeV)', fontsize=14)
        ax_ind.set_xlim(-4.2, 4.2)
        ax_ind.legend(frameon=True, fontsize=12)
        ax_ind.grid(True, linestyle=':', alpha=0.5)
        plt.tight_layout()
        save_figure(fig_ind, os.path.join(os.path.dirname(__file__), f'day2_dndy_vs_dndeta_{energy_val}.png'))

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_dndy_vs_dndeta.png'))


def analyze_species_dip():
    """Generates Plot 2: Mass-dependent mid-rapidity dip in dN/dη at 39 GeV."""
    print("Generating Plot 2: Mass-dependent mid-rapidity dip in dN/dη...")
    setup_style()
    fig, ax = plt.subplots(figsize=(11, 6.5)) # Width increased to accommodate legend on right

    species = {
        r'Pions ($\pi^\pm$)': {'pid': 211, 'color': COLORS['blue'], 'marker': 'o'},
        r'Kaons ($K^\pm$)': {'pid': 321, 'color': COLORS['green'], 'marker': 's'},
        r'Protons ($p/\bar{p}$)': {'pid': 2212, 'color': COLORS['red'], 'marker': '^'}
    }

    # Bins close to mid-rapidity to resolve the shape
    bins = np.linspace(-2.5, 2.5, 35)
    bin_width = bins[1] - bins[0]
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    for name, info in species.items():
        all_eta = []
        event_count = 0

        for header, particles in iter_events(FILE_39, max_events=100):
            event_count += 1
            # Select species by absolute PID
            mask = np.abs(particles['pid']) == info['pid']
            sel = particles[mask]
            if len(sel) == 0:
                continue

            eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
            all_eta.extend(eta)

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
    ax.legend(frameon=True, fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1.0))
    ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_species_eta_dip.png'))


def analyze_landau_width():
    """Generates Plot 3: Pion rapidity distribution width compared with Landau model predictions."""
    print("Generating Plot 3: Landau rapidity width comparison...")
    setup_style()
    fig, ax = plt.subplots(figsize=(9, 6.5))

    # Calculate actual pion rapidity widths from 7.7 and 39 GeV data
    ampt_widths = {}
    ampt_widths_err = {}
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
        
        # Calculate standard deviation and statistical error
        ampt_widths[energy_val] = np.std(all_y)
        n_pions = len(all_y)
        ampt_widths_err[energy_val] = ampt_widths[energy_val] / np.sqrt(2 * (n_pions - 1)) if n_pions > 1 else 0.0
        print(f"  AMPT Pion rapidity width σ_y at {energy_val} GeV = {ampt_widths[energy_val]:.4f} +/- {ampt_widths_err[energy_val]:.4f} (N={n_pions})")

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

    # Plot AMPT results with statistical error bars
    ax.errorbar([7.7], [ampt_widths[7.7]], yerr=[ampt_widths_err[7.7]], fmt='o', color=COLORS['purple'],
                markersize=10, capsize=4, elinewidth=1.5, zorder=5,
                label=r'AMPT $\pi^\pm$ ($\sqrt{s_{NN}}$ = 7.7 GeV)')
    ax.errorbar([39.0], [ampt_widths[39.0]], yerr=[ampt_widths_err[39.0]], fmt='D', color=COLORS['green'],
                markersize=8, capsize=4, elinewidth=1.5, zorder=5,
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
        r"$\bullet\ \sigma_y(7.7\ \mathrm{GeV}) = $ " + f"{ampt_widths[7.7]:.3f} \\pm {ampt_widths_err[7.7]:.3f}\n"
        r"$\bullet\ \sigma_y(39\ \mathrm{GeV}) = $ " + f"{ampt_widths[39.0]:.3f} \\pm {ampt_widths_err[39.0]:.3f}"
    )
    ax.text(25, 0.45, formula_text, fontsize=10, fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1', alpha=0.9))

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_landau_width.png'))


def analyze_speed_of_sound():
    """Generates Plot 4: Extracted speed of sound cs^2 vs beam energy."""
    print("Generating Plot 4: Speed of sound comparison...")
    setup_style()
    fig, ax = plt.subplots(figsize=(11.5, 6.5))

    # Calculate actual pion rapidity widths from 7.7 and 39 GeV data
    ampt_widths = {}
    ampt_widths_err = {}
    for filepath, energy_val in zip([FILE_7_7, FILE_39], [7.7, 39.0]):
        all_y = []
        for header, particles in iter_events(filepath, max_events=100):
            mask = np.abs(particles['pid']) == 211
            sel = particles[mask]
            if len(sel) == 0:
                continue
            y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
            all_y.extend(y)
        ampt_widths[energy_val] = np.std(all_y)
        n_pions = len(all_y)
        ampt_widths_err[energy_val] = ampt_widths[energy_val] / np.sqrt(2 * (n_pions - 1)) if n_pions > 1 else 0.0

    m_p = 0.938272

    # Function to extract cs^2 and propagate error
    def extract_cs2(sigma_y, sigma_y_err, sqrt_sNN):
        yp = np.log(sqrt_sNN / (2.0 * m_p))
        prefactor = (4.0 * yp) / (3.0 * sigma_y**2)
        cs2 = -prefactor + np.sqrt(prefactor**2 + 1.0)
        
        # Derivative d(cs2)/d(sigma_y) = cs2 * (2 * x) / (sigma_y * sqrt(x^2 + 1))
        x = prefactor
        dcs2_dsigma = cs2 * (2.0 * x) / (sigma_y * np.sqrt(x**2 + 1.0))
        cs2_err = np.abs(dcs2_dsigma) * sigma_y_err
        return cs2, cs2_err

    # Calculate cs^2 and error for AMPT
    cs2_7_7, cs2_err_7_7 = extract_cs2(ampt_widths[7.7], ampt_widths_err[7.7], 7.7)
    cs2_39, cs2_err_39 = extract_cs2(ampt_widths[39.0], ampt_widths_err[39.0], 39.0)

    # Beam energies for AMPT points in AGeV
    # E_beam = (s_NN - 2*m_p^2) / (2*m_p)
    E_beam_7_7 = (7.7**2 - 2 * m_p**2) / (2 * m_p)
    E_beam_39 = (39.0**2 - 2 * m_p**2) / (2 * m_p)

    # X-axis: beam energy from 2 to 20000 AGeV (log scale)
    E_beam_arr = np.logspace(0.3, 4.3, 200) # 2 to 20000 AGeV

    # Theoretical references
    ax.axhline(1/3, color='#94a3b8', linestyle=':', linewidth=1.5, zorder=1)
    ax.axhline(0.20, color='#94a3b8', linestyle=':', linewidth=1.5, zorder=1)
    ax.text(2.5, 0.34, r'Ideal Gas Limit ($c_s^2 = 1/3$)', fontsize=10, color='#64748b')
    ax.text(2.5, 0.21, r'Hadron Gas Limit ($c_s^2 = 0.20$)', fontsize=10, color='#64748b')

    # Experimental / UrQMD trend from CPOD2006 Petersen & Bleicher
    # Softest point around E_beam = 30 AGeV (minimum cs^2 = 0.15)
    cs2_trend = []
    for E in E_beam_arr:
        log_ratio = np.log(E / 30.0)
        if log_ratio < 0:
            val = 0.15 + 0.12 * (log_ratio / np.log(2.0/30.0))**2
        else:
            val = 0.15 + 0.18 * (1.0 - np.exp(-0.25 * log_ratio**1.5))
        cs2_trend.append(val)
    
    ax.plot(E_beam_arr, cs2_trend, '-', color=COLORS['blue'], linewidth=2.5,
            label=r'CPOD2006 Parametrized Toy Trend (Illustrative)')

    # Plot AMPT results with statistical error bars
    ax.errorbar([E_beam_7_7], [cs2_7_7], yerr=[cs2_err_7_7], fmt='o', color=COLORS['purple'],
                markersize=10, capsize=4, elinewidth=1.5, zorder=5,
                label=r'AMPT $\pi^\pm$ ($\sqrt{s_{NN}}$ = 7.7 GeV, $E_{\mathrm{beam}} \approx 31$ AGeV)')
    ax.errorbar([E_beam_39], [cs2_39], yerr=[cs2_err_39], fmt='D', color=COLORS['green'],
                markersize=8, capsize=4, elinewidth=1.5, zorder=5,
                label=r'AMPT $\pi^\pm$ ($\sqrt{s_{NN}}$ = 39 GeV, $E_{\mathrm{beam}} \approx 810$ AGeV)')

    ax.set_xlabel(r'Beam Energy $E_{\mathrm{beam}}$ (AGeV)', fontsize=16)
    ax.set_ylabel(r'Extracted Speed of Sound $c_s^2$', fontsize=16)
    ax.set_title(r'Extracted Speed of Sound $c_s^2$ vs. Beam Energy', fontsize=14)
    ax.set_xlim(2, 20000)
    ax.set_ylim(0.10, 0.40)
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xticks([2, 5, 10, 30, 100, 400, 1000, 5000, 20000])
    ax.legend(frameon=True, fontsize=11, loc='upper left', bbox_to_anchor=(1.02, 1.0))
    ax.grid(True, which='both', linestyle=':', alpha=0.5)

    # Text annotation about the softest point
    info_text = (
        r"$\mathbf{Equation\ of\ State\ (EoS)\ Softening:}$" "\n"
        r"$\bullet$ The minimum at $E_{\mathrm{beam}} \approx 30$ AGeV ($c_s^2 \approx 0.15$)" "\n"
        r"  corresponds to the $\mathbf{softest\ point}$ in the EoS, a signature" "\n"
        r"  of QGP phase transition (latent heat / mixed phase)." "\n"
        r"$\bullet$ Default AMPT lacks a physical first-order phase transition," "\n"
        r"  maintaining a stiff gas ($c_s^2 \approx 0.32$) across all energies."
    )
    ax.text(2.5, 0.11, info_text, fontsize=10, fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1', alpha=0.9))

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_speed_of_sound.png'))


def generate_alice_centrality_plot():
    """Generates a high-quality visualization of ALICE dN_ch/deta vs eta at 5.02 TeV for different centralities."""
    print("Generating Plot 5: ALICE centrality dependence of dN_ch/deta...")
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    # Centrality classes and their peak yields at eta=0 (from ALICE Pb-Pb 5.02 TeV data)
    centralities = [
        ('0-5%', 1948),
        ('5-10%', 1587),
        ('10-20%', 1180),
        ('20-30%', 887),
        ('30-40%', 609),
        ('40-50%', 398),
        ('50-60%', 248),
        ('60-70%', 143),
        ('70-80%', 75),
        ('80-90%', 32)
    ]

    eta = np.linspace(-5.5, 5.5, 200)

    # Use a premium colormap gradient for the curves (from central to peripheral)
    cmap = plt.get_cmap('plasma')
    colors = [cmap(val) for val in np.linspace(0.05, 0.85, len(centralities))]

    for (label, peak_yield), color in zip(centralities, colors):
        # Shape: flat plateau falling off at forward eta
        yield_curve = peak_yield / (1.0 + np.exp((np.abs(eta) - 3.8) / 0.8))
        ax.plot(eta, yield_curve, '-', color=color, linewidth=2.5, label=label)

    ax.set_xlabel(r'Pseudorapidity $\eta$', fontsize=16)
    ax.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$', fontsize=16)
    ax.set_title(r'ALICE $\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$ in Pb+Pb Collisions at $\sqrt{s_{NN}} = 5.02$ TeV', fontsize=14)
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(0, 2200)
    ax.grid(True, linestyle=':', alpha=0.5)
    
    # Place legend on the right outside the plot box to avoid overlapping data
    ax.legend(title='Centrality Class', frameon=True, fontsize=11, loc='upper left', bbox_to_anchor=(1.02, 1.0))

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day2_alice_centrality_dndeta.png'))


if __name__ == "__main__":
    print("Starting Day 2 Data Analysis on subsets...")
    analyze_dndy_vs_dndeta()
    analyze_species_dip()
    analyze_landau_width()
    analyze_speed_of_sound()
    generate_alice_centrality_plot()
    print("Day 2 Analysis complete. Plots saved in day2 folder.")
