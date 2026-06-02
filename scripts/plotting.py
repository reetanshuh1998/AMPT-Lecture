#!/usr/bin/env python3
"""
plotting.py — Publication-quality plotting utilities for AMPT analysis.

Uses matplotlib with HEP-style formatting:
- Clean fonts (serif or sans-serif matching publications)
- Proper axis labels with units
- Error bars
- Legend formatting
- Color palettes suitable for HEP papers
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Global style configuration
# ============================================================

# HEP-style color palette
COLORS = {
    'blue': '#2166ac',
    'red': '#b2182b',
    'green': '#1b7837',
    'orange': '#e66101',
    'purple': '#7b3294',
    'cyan': '#0571b0',
    'brown': '#8c510a',
    'pink': '#c51b7d',
    'gray': '#636363',
}

# Marker styles
MARKERS = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']

# Energy labels
ENERGY_LABELS = {
    7.7: r'$\sqrt{s_{NN}}$ = 7.7 GeV',
    11.5: r'$\sqrt{s_{NN}}$ = 11.5 GeV',
    14.5: r'$\sqrt{s_{NN}}$ = 14.5 GeV',
    19.6: r'$\sqrt{s_{NN}}$ = 19.6 GeV',
    27: r'$\sqrt{s_{NN}}$ = 27 GeV',
    39: r'$\sqrt{s_{NN}}$ = 39 GeV',
    62.4: r'$\sqrt{s_{NN}}$ = 62.4 GeV',
    200: r'$\sqrt{s_{NN}}$ = 200 GeV',
}

# Particle labels
PARTICLE_LABELS = {
    211: r'$\pi^{+}$',
    -211: r'$\pi^{-}$',
    111: r'$\pi^{0}$',
    321: r'$K^{+}$',
    -321: r'$K^{-}$',
    2212: r'$p$',
    -2212: r'$\bar{p}$',
    3122: r'$\Lambda$',
    -3122: r'$\bar{\Lambda}$',
}


def setup_style():
    """Configure matplotlib for publication-quality plots."""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 14,
        'axes.labelsize': 16,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 11,
        'legend.frameon': True,
        'legend.framealpha': 0.8,
        'legend.edgecolor': '0.8',
        'figure.figsize': (8, 6),
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.linewidth': 1.2,
        'xtick.major.width': 1.0,
        'ytick.major.width': 1.0,
        'xtick.minor.visible': True,
        'ytick.minor.visible': True,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.top': True,
        'ytick.right': True,
        'axes.grid': False,
    })


def create_figure(nrows=1, ncols=1, figsize=None, squeeze=True):
    """Create a figure with subplots, using HEP style."""
    setup_style()
    if figsize is None:
        figsize = (8 * ncols, 6 * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=squeeze)
    return fig, axes


def plot_dndeta(ax, bin_centers, dndeta, errors=None, label='', color=None,
                marker='o', **kwargs):
    """Plot dN/dη distribution with error bars."""
    if color is None:
        color = COLORS['blue']
    ax.errorbar(bin_centers, dndeta, yerr=errors, fmt=marker, color=color,
                markersize=5, capsize=2, label=label, **kwargs)
    ax.set_xlabel(r'$\eta$')
    ax.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$')


def plot_dndy(ax, bin_centers, dndy, errors=None, label='', color=None,
              marker='o', **kwargs):
    """Plot dN/dy distribution with error bars."""
    if color is None:
        color = COLORS['red']
    ax.errorbar(bin_centers, dndy, yerr=errors, fmt=marker, color=color,
                markersize=5, capsize=2, label=label, **kwargs)
    ax.set_xlabel(r'$y$')
    ax.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}y$')


def plot_pt_spectrum(ax, bin_centers, spectrum, errors=None, label='',
                     color=None, marker='o', logy=True, **kwargs):
    """Plot pT spectrum, typically on log scale."""
    if color is None:
        color = COLORS['blue']
    ax.errorbar(bin_centers, spectrum, yerr=errors, fmt=marker, color=color,
                markersize=5, capsize=2, label=label, **kwargs)
    ax.set_xlabel(r'$p_T$ (GeV/$c$)')
    ax.set_ylabel(r'$\frac{1}{N_{\mathrm{ev}}} \frac{\mathrm{d}N}{\mathrm{d}p_T}$ (GeV/$c$)$^{-1}$')
    if logy:
        ax.set_yscale('log')


def plot_invariant_yield(ax, bin_centers, inv_yield, errors=None, label='',
                         color=None, marker='o', **kwargs):
    """Plot invariant yield vs pT."""
    if color is None:
        color = COLORS['blue']
    ax.errorbar(bin_centers, inv_yield, yerr=errors, fmt=marker, color=color,
                markersize=5, capsize=2, label=label, **kwargs)
    ax.set_xlabel(r'$p_T$ (GeV/$c$)')
    ax.set_ylabel(r'$\frac{1}{2\pi p_T} \frac{\mathrm{d}^2 N}{\mathrm{d}p_T \mathrm{d}y}$ (GeV/$c$)$^{-2}$')
    ax.set_yscale('log')


def plot_v2(ax, pt_centers, v2, errors=None, label='', color=None,
            marker='o', **kwargs):
    """Plot v2 vs pT."""
    if color is None:
        color = COLORS['blue']
    ax.errorbar(pt_centers, v2, yerr=errors, fmt=marker, color=color,
                markersize=5, capsize=2, label=label, **kwargs)
    ax.set_xlabel(r'$p_T$ (GeV/$c$)')
    ax.set_ylabel(r'$v_2$')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)


def plot_histogram(ax, bin_centers, values, label='', color=None, **kwargs):
    """Generic histogram-style bar plot."""
    if color is None:
        color = COLORS['blue']
    width = bin_centers[1] - bin_centers[0] if len(bin_centers) > 1 else 1
    ax.bar(bin_centers, values, width=width * 0.9, color=color, alpha=0.7,
           edgecolor='black', linewidth=0.5, label=label, **kwargs)


def add_ampt_label(ax, energy_gev, x=0.05, y=0.95, additional=''):
    """Add AMPT label with energy to a plot."""
    text = f'AMPT, Au+Au\n{ENERGY_LABELS.get(energy_gev, f"√s_NN = {energy_gev} GeV")}'
    if additional:
        text += f'\n{additional}'
    ax.text(x, y, text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))


def save_figure(fig, filepath, close=True):
    """Save figure as PDF (for LaTeX) and PNG (for preview)."""
    fig.savefig(filepath, bbox_inches='tight')
    if filepath.endswith('.pdf'):
        fig.savefig(filepath.replace('.pdf', '.png'), bbox_inches='tight', dpi=150)
    if close:
        plt.close(fig)
    print(f"  Saved: {filepath}")


if __name__ == "__main__":
    # Quick demo
    setup_style()
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    x = np.linspace(-4, 4, 40)
    y = 100 * np.exp(-x**2 / 2)
    ax.plot(x, y, 'o-', color=COLORS['blue'])
    ax.set_xlabel(r'$\eta$')
    ax.set_ylabel(r'$\mathrm{d}N_{\mathrm{ch}}/\mathrm{d}\eta$')
    ax.set_title('Demo plot')
    save_figure(fig, '/tmp/demo_plot.pdf')
    print("Demo plot saved.")
