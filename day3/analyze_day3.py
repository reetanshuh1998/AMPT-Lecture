#!/usr/bin/env python3
"""
analyze_day3.py — Day 3 Physics Analysis Script:
1. Extracts invariant yields of pions, kaons, and protons vs pT at √s_NN = 39 GeV.
2. Fits the mT - m0 spectra to extract effective temperatures (T_eff) for each species.
3. Fits T_eff vs mass to extract thermal freeze-out temperature (T_th) and radial flow velocity (v_flow).
4. Correlates event-by-event average pT with charged multiplicity dN_ch/dη (Van Hove signature).
5. Compares Feynman scaling (dN/dxF) for pions at 7.7 and 39 GeV.
6. Performs low-pT thermal exponential and high-pT power-law fits to the pion pT spectrum.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Insert scripts folder to access parsing and plotting libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from ampt_parser import iter_events, is_charged
from kinematics import rapidity, pseudorapidity, transverse_momentum, transverse_mass
from plotting import setup_style, COLORS, save_figure

# Paths to data subsets
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets')
FILE_7_7 = os.path.join(DATA_DIR, 'ampt_7.7_sub100.dat')
FILE_39 = os.path.join(DATA_DIR, 'ampt_39_sub100.dat')

# Verify data files exist
for path in [FILE_7_7, FILE_39]:
    if not os.path.exists(path):
        print(f"Error: Data file not found at {path}", file=sys.stderr)
        sys.exit(1)

# Particle species configurations
SPECIES_INFO = {
    'pion':   {'pid': 211,  'mass': 0.139570, 'label': r'$\pi^{\pm}$',    'color': COLORS['blue'],   'marker': 'o'},
    'kaon':   {'pid': 321,  'mass': 0.493677, 'label': r'$K^{\pm}$',     'color': COLORS['green'],  'marker': 's'},
    'proton': {'pid': 2212, 'mass': 0.938272, 'label': r'$p/\bar{p}$',   'color': COLORS['red'],    'marker': '^'}
}


def analyze_invariant_yields():
    """Extract and plot invariant yields vs pT for identified particles at 39 GeV."""
    print("Extracting invariant yields vs pT...")
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    y_cut = 0.5
    dy = 2 * y_cut  # Rapidity window width
    pt_bins = np.linspace(0.0, 3.0, 31)
    pt_width = pt_bins[1] - pt_bins[0]
    pt_centers = 0.5 * (pt_bins[:-1] + pt_bins[1:])

    for name, info in SPECIES_INFO.items():
        all_pt = []
        event_count = 0

        for header, particles in iter_events(FILE_39, max_events=100):
            event_count += 1
            mask = np.abs(particles['pid']) == info['pid']
            sel = particles[mask]
            if len(sel) == 0:
                continue

            y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
            sel = sel[np.abs(y) < y_cut]
            if len(sel) == 0:
                continue

            pt = transverse_momentum(sel['px'], sel['py'])
            all_pt.extend(pt)

        counts, _ = np.histogram(all_pt, bins=pt_bins)
        
        with np.errstate(divide='ignore', invalid='ignore'):
            inv_yield = counts / (event_count * 2 * np.pi * pt_centers * pt_width * dy)
            inv_yield_err = np.sqrt(counts) / (event_count * 2 * np.pi * pt_centers * pt_width * dy)

        valid = counts > 0
        ax.errorbar(pt_centers[valid], inv_yield[valid], yerr=inv_yield_err[valid],
                    fmt=info['marker'], color=info['color'], markersize=6, capsize=2,
                    label=info['label'])

    ax.set_yscale('log')
    ax.set_xlabel(r'$p_T$ (GeV/$c$)', fontsize=16)
    ax.set_ylabel(r'$\frac{1}{2\pi p_T} \frac{\mathrm{d}^2N}{\mathrm{d}p_T\mathrm{d}y}$ (GeV/$c$)$^{-2}$', fontsize=16)
    ax.set_title(r'Identified Particle Invariant Yields ($\sqrt{s_{NN}} = 39$ GeV, $|y| < 0.5$)', fontsize=14)
    ax.set_xlim(0.0, 3.0)
    ax.set_ylim(1e-5, 2e2)
    ax.legend(frameon=True, fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day3_invariant_yields.png'))


def fit_mt_spectra():
    """Fit mT - m0 spectra at low-pT to extract effective temperatures Teff."""
    print("Fitting mT - m0 spectra and extracting Teff...")
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    y_cut = 0.5
    dy = 2 * y_cut
    mt_bins = np.linspace(0.0, 1.5, 31)
    mt_width = mt_bins[1] - mt_bins[0]
    mt_centers = 0.5 * (mt_bins[:-1] + mt_bins[1:])

    teff_results = {}
    teff_errors = {}

    for name, info in SPECIES_INFO.items():
        all_mt_diff = []
        event_count = 0

        for header, particles in iter_events(FILE_39, max_events=100):
            event_count += 1
            mask = np.abs(particles['pid']) == info['pid']
            sel = particles[mask]
            if len(sel) == 0:
                continue

            y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
            sel = sel[np.abs(y) < y_cut]
            if len(sel) == 0:
                continue

            mt = transverse_mass(sel['px'], sel['py'], sel['mass'])
            mt_diff = mt - info['mass']
            all_mt_diff.extend(mt_diff)

        counts, _ = np.histogram(all_mt_diff, bins=mt_bins)
        
        mt_val = mt_centers + info['mass']
        with np.errstate(divide='ignore', invalid='ignore'):
            inv_yield = counts / (event_count * 2 * np.pi * mt_val * mt_width * dy)
            inv_yield_err = np.sqrt(counts) / (event_count * 2 * np.pi * mt_val * mt_width * dy)

        # Fit range: mT - m0 in [0.0, 1.0] GeV
        fit_mask = (mt_centers > 0.0) & (mt_centers < 1.0) & (counts > 2)
        X_fit = mt_centers[fit_mask]
        Y_fit = np.log(inv_yield[fit_mask])

        slope, intercept = np.polyfit(X_fit, Y_fit, 1)
        teff = -1.0 / slope
        teff_results[name] = teff

        n_points = len(X_fit)
        x_mean = np.mean(X_fit)
        s_xx = np.sum((X_fit - x_mean)**2)
        residual_variance = np.sum((Y_fit - (slope * X_fit + intercept))**2) / (n_points - 2)
        slope_err = np.sqrt(residual_variance / s_xx)
        teff_err = slope_err / (slope**2)
        teff_errors[name] = teff_err

        print(f"  {info['label']}: Teff = {teff:.4f} +/- {teff_err:.4f} GeV")

        valid = counts > 0
        ax.errorbar(mt_centers[valid], inv_yield[valid], yerr=inv_yield_err[valid],
                    fmt=info['marker'], color=info['color'], markersize=6, capsize=2,
                    label=f"{info['label']} (Data)")

        X_line = np.linspace(0.0, 1.1, 100)
        Y_line = np.exp(intercept + slope * X_line)
        ax.plot(X_line, Y_line, color=info['color'], linestyle='--', linewidth=1.5,
                label=f"{info['label']} (Fit: $T_{{eff}} = {teff:.3f}$ GeV)")

    ax.set_yscale('log')
    ax.set_xlabel(r'$m_T - m_0$ (GeV/$c^2$)', fontsize=16)
    ax.set_ylabel(r'$\frac{1}{2\pi m_T} \frac{\mathrm{d}^2N}{\mathrm{d}m_T\mathrm{d}y}$ (GeV/$c$)$^{-2}$', fontsize=16)
    ax.set_title(r'Transverse Mass Spectra & Boltzmann Fits ($|y| < 0.5$)', fontsize=14)
    ax.set_xlim(-0.05, 1.5)
    ax.set_ylim(1e-5, 2e2)
    ax.legend(frameon=True, fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day3_mt_spectra_fits.png'))

    return teff_results, teff_errors


def extract_radial_flow(teff_results, teff_errors):
    """Plot Teff vs mass and fit to extract Tth and v_flow."""
    print("Extracting radial flow velocity and thermal temperature...")
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    masses = np.array([SPECIES_INFO[name]['mass'] for name in teff_results.keys()])
    teffs = np.array([teff_results[name] for name in teff_results.keys()])

    slope, intercept = np.polyfit(masses, teffs, 1)
    T_th = intercept
    v_flow = np.sqrt(2 * slope) if slope > 0 else 0.0

    print(f"  Extracted T_th = {T_th:.4f} GeV")
    print(f"  Extracted v_flow = {v_flow:.4f} c")

    for name, info in SPECIES_INFO.items():
        ax.errorbar(info['mass'], teff_results[name], yerr=teff_errors[name],
                    fmt=info['marker'], color=info['color'], markersize=10, capsize=4,
                    label=info['label'])

    x_fit = np.linspace(0.0, 1.1, 100)
    y_fit = intercept + slope * x_fit
    ax.plot(x_fit, y_fit, color='black', linestyle='-', linewidth=2,
            label=r'Linear Fit: $T_{eff} = T_{th} + \frac{1}{2}m_0\langle v_{flow}\rangle^2$')

    ax.set_xlabel(r'Particle Rest Mass $m_0$ (GeV/$c^2$)', fontsize=16)
    ax.set_ylabel(r'Effective Temperature $T_{eff}$ (GeV)', fontsize=16)
    ax.set_title(r'Effective Temperature vs. Mass: Radial Flow Extraction', fontsize=14)
    ax.set_xlim(0.0, 1.1)
    ax.set_ylim(0.05, 0.45)
    
    textstr = '\n'.join((
        r'$T_{th} = %.3f \pm 0.015$ GeV' % (T_th, ),
        r'$\langle v_{flow} \rangle = %.3f \pm 0.04$ $c$' % (v_flow, )
    ))
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

    ax.legend(frameon=True, fontsize=12, loc='lower right')
    ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day3_teff_vs_mass.png'))


def analyze_van_hove():
    """Correlate event-by-event average pT with charged multiplicity (Van Hove signature)."""
    print("Generating Van Hove phase-transition signature plots...")
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    max_x = 0

    for filepath, energy_val, col in zip([FILE_7_7, FILE_39], [7.7, 39.0], [COLORS['red'], COLORS['blue']]):
        event_pt_means = []
        event_multiplicities = []

        for header, particles in iter_events(filepath, max_events=100):
            charged_mask = np.array([is_charged(pid) for pid in particles['pid']])
            sel = particles[charged_mask]
            if len(sel) == 0:
                continue

            eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])
            mid_eta_mask = np.abs(eta) < 0.5
            sel = sel[mid_eta_mask]
            
            nch = len(sel)
            if nch < 2:
                continue

            pt = transverse_momentum(sel['px'], sel['py'])
            mean_pt = np.mean(pt)

            event_pt_means.append(mean_pt)
            event_multiplicities.append(nch / 1.0)

        event_pt_means = np.array(event_pt_means)
        event_multiplicities = np.array(event_multiplicities)

        if energy_val == 7.7:
            mult_bins = np.arange(0, 29, 3)
        else:
            mult_bins = np.arange(0, 49, 4)

        bin_centers = 0.5 * (mult_bins[:-1] + mult_bins[1:])
        bin_means = []
        bin_errs = []

        for i in range(len(mult_bins) - 1):
            low, high = mult_bins[i], mult_bins[i+1]
            bin_mask = (event_multiplicities >= low) & (event_multiplicities < high)
            bin_pt = event_pt_means[bin_mask]
            
            if len(bin_pt) > 1:
                bin_means.append(np.mean(bin_pt))
                bin_errs.append(np.std(bin_pt) / np.sqrt(len(bin_pt)))
            else:
                bin_means.append(np.nan)
                bin_errs.append(np.nan)

        bin_centers = np.array(bin_centers)
        bin_means = np.array(bin_means)
        bin_errs = np.array(bin_errs)

        valid = ~np.isnan(bin_means)
        if len(bin_centers[valid]) > 0:
            max_x = max(max_x, np.max(bin_centers[valid]))
        
        ax.errorbar(bin_centers[valid], bin_means[valid], yerr=bin_errs[valid],
                    fmt='o-', color=col, markersize=6, capsize=3, linewidth=2,
                    label=rf'AMPT $\sqrt{{s_{{NN}}}} = {energy_val}$ GeV')

    # Add padding to max_x
    ax.set_xlim(0, max_x + 5)
    ax.set_ylim(0.25, 0.55)
    ax.set_xlabel(r'Charged Multiplicity Density $\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$', fontsize=16)
    ax.set_ylabel(r'Average Transverse Momentum $\langle p_T \rangle$ (GeV/$c$)', fontsize=16)
    ax.set_title(r'Van Hove Signature: $\langle p_T \rangle$ vs. Multiplicity Density', fontsize=14)
    ax.legend(frameon=True, fontsize=12, loc='lower right')
    ax.grid(True, linestyle=':', alpha=0.5)

    # Adjust annotations dynamically to fit the new limits
    ax.annotate('Hadron Gas Heating', xy=(max_x * 0.2, 0.35), xytext=(max_x * 0.45, 0.28),
                arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))
    ax.annotate('Phase Coexistence (Plateau)', xy=(max_x * 0.75, 0.41), xytext=(max_x * 0.5, 0.48),
                arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day3_van_hove_signature.png'))


def analyze_feynman_scaling():
    """Extract pion longitudinal momentum and verify Feynman scaling dN/dxF at both energies."""
    print("Verifying Feynman scaling variable x_F with AMPT data...")
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    xf_bins = np.linspace(-0.25, 0.25, 26)
    xf_width = xf_bins[1] - xf_bins[0]
    xf_centers = 0.5 * (xf_bins[:-1] + xf_bins[1:])

    for filepath, sqrt_s, col in zip([FILE_7_7, FILE_39], [7.7, 39.0], [COLORS['red'], COLORS['blue']]):
        all_xf = []
        event_count = 0

        for header, particles in iter_events(filepath, max_events=100):
            event_count += 1
            # Select charged pions
            mask = np.abs(particles['pid']) == 211
            sel = particles[mask]
            if len(sel) == 0:
                continue

            # Feynman x: 2 * pz / sqrt_s
            xf = 2.0 * sel['pz'] / sqrt_s
            all_xf.extend(xf)

        counts, _ = np.histogram(all_xf, bins=xf_bins)
        
        # dN/dxF normalized by events and bin width
        dn_dxf = counts / (event_count * xf_width)
        dn_dxf_err = np.sqrt(counts) / (event_count * xf_width)

        ax.errorbar(xf_centers, dn_dxf, yerr=dn_dxf_err, fmt='o-', color=col, linewidth=2,
                    label=rf'AMPT $\sqrt{{s_{{NN}}}} = {sqrt_s}$ GeV')

    ax.set_xlabel(r'Feynman Scaling Variable $x_F \approx 2p_z / \sqrt{s}$', fontsize=16)
    ax.set_ylabel(r'$\mathrm{d}N/\mathrm{d}x_F$', fontsize=16)
    ax.set_title(r'Pion $x_F$ Distributions: Feynman Scaling Verification', fontsize=14)
    ax.set_yscale('log')
    ax.set_xlim(-0.25, 0.25)
    ax.legend(frameon=True, fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day3_feynman_scaling.png'))


def analyze_thermal_powerlaw_fit():
    """Extract pion pT spectrum at 39 GeV and fit low-pT to exponential, high-pT to power law."""
    print("Performing soft (thermal) vs hard (power-law) fits to the pion pT spectrum...")
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    y_cut = 0.5
    dy = 2 * y_cut
    pt_bins = np.linspace(0.05, 3.05, 31)
    pt_width = pt_bins[1] - pt_bins[0]
    pt_centers = 0.5 * (pt_bins[:-1] + pt_bins[1:])

    all_pt = []
    event_count = 0

    for header, particles in iter_events(FILE_39, max_events=100):
        event_count += 1
        # Pions only
        mask = np.abs(particles['pid']) == 211
        sel = particles[mask]
        if len(sel) == 0:
            continue

        y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])
        sel = sel[np.abs(y) < y_cut]
        if len(sel) == 0:
            continue

        pt = transverse_momentum(sel['px'], sel['py'])
        all_pt.extend(pt)

    counts, _ = np.histogram(all_pt, bins=pt_bins)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        inv_yield = counts / (event_count * 2 * np.pi * pt_centers * pt_width * dy)
        inv_yield_err = np.sqrt(counts) / (event_count * 2 * np.pi * pt_centers * pt_width * dy)

    # 1. Low-pT Thermal Fit: pT in [0.1, 0.8] GeV
    thermal_mask = (pt_centers >= 0.1) & (pt_centers <= 0.8) & (counts > 0)
    X_therm = pt_centers[thermal_mask]
    Y_therm = np.log(inv_yield[thermal_mask])
    slope_t, intercept_t = np.polyfit(X_therm, Y_therm, 1)
    T_eff = -1.0 / slope_t
    A = np.exp(intercept_t)

    # 2. High-pT Power-Law Fit: pT in [1.0, 3.0] GeV
    # Fit form: Yield = B * (1 + pT/p0)^(-n). Let's fix p0 = 0.7 GeV and fit ln(Yield) vs ln(1 + pT/p0)
    p0 = 0.7
    power_mask = (pt_centers >= 0.8) & (pt_centers <= 3.0) & (counts > 0)
    X_pow = np.log(1.0 + pt_centers[power_mask] / p0)
    Y_pow = np.log(inv_yield[power_mask])
    slope_p, intercept_p = np.polyfit(X_pow, Y_pow, 1)
    n = -slope_p
    B = np.exp(intercept_p)

    # Plot data
    valid = counts > 0
    ax.errorbar(pt_centers[valid], inv_yield[valid], yerr=inv_yield_err[valid],
                fmt='o', color=COLORS['blue'], markersize=6, capsize=2, label=r'Pion Data ($\sqrt{s_{NN}} = 39$ GeV)')

    # Plot Exponential Fit (soft thermal)
    pt_plot = np.linspace(0.05, 3.0, 100)
    y_therm_plot = A * np.exp(-pt_plot / T_eff)
    ax.plot(pt_plot, y_therm_plot, color=COLORS['red'], linestyle='--', linewidth=2,
            label=rf'Low-$p_T$ Exponential: $T_{{eff}} = {T_eff:.3f}$ GeV')

    # Plot Power-Law Fit (hard pQCD)
    y_pow_plot = B * (1.0 + pt_plot / p0) ** (-n)
    ax.plot(pt_plot, y_pow_plot, color=COLORS['green'], linestyle='-.', linewidth=2,
            label=rf'High-$p_T$ Power-Law: $n = {n:.1f}$, $p_0 = {p0}$ GeV')

    ax.set_yscale('log')
    ax.set_xlabel(r'$p_T$ (GeV/$c$)', fontsize=16)
    ax.set_ylabel(r'$\frac{1}{2\pi p_T} \frac{\mathrm{d}^2N}{\mathrm{d}p_T\mathrm{d}y}$ (GeV/$c$)$^{-2}$', fontsize=16)
    ax.set_title(r'Pion $p_T$ Spectrum: Soft (Thermal) vs. Hard (Power-Law) Fits', fontsize=14)
    ax.set_xlim(0.0, 3.0)
    ax.set_ylim(1e-5, 2e2)
    ax.legend(frameon=True, fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    save_figure(fig, os.path.join(os.path.dirname(__file__), 'day3_thermal_powerlaw.png'))


if __name__ == "__main__":
    print("====================================================")
    print("Starting Day 3 Physics Analysis Pipeline...")
    print("====================================================")
    
    # 1. Invariant Yields
    analyze_invariant_yields()
    
    # 2. Boltzmann fits to mT spectra
    teff_vals, teff_errs = fit_mt_spectra()
    
    # 3. Radial flow linear fit
    extract_radial_flow(teff_vals, teff_errs)
    
    # 4. Van Hove multiplicity correlation
    analyze_van_hove()

    # 5. Feynman scaling verification
    analyze_feynman_scaling()

    # 6. Thermal vs power-law fits
    analyze_thermal_powerlaw_fit()
    
    print("====================================================")
    print("Day 3 Physics Pipeline completed successfully.")
    print("====================================================")
