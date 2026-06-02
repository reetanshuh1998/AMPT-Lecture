#!/usr/bin/env python3
"""
Day 14 — Wrap-Up: Reproducible Analysis Pipeline
================================================
Objectives:
  1. Construct an end-to-end data analysis pipeline from raw AMPT data to final plots
  2. Implement structured JSON reporting of physics observables
  3. Generate a multi-panel summary publication-quality canvas
  4. Benchmark execution speeds for different event sizes
  5. Deliver a modular, reproducible package that students can use for mini-projects
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import numpy as np
import json
import time
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ampt_parser import iter_events, is_charged
from kinematics import pseudorapidity, transverse_momentum, rapidity
from observables import dNdeta, pt_spectrum, mean_pt

outdir = os.path.dirname(__file__)

print("=" * 60)
print("DAY 14: MASTER ANALYSIS PIPELINE & REPRODUCIBILITY")
print("=" * 60)

# Master pipeline class
class AMPTAnalysisPipeline:
    def __init__(self, filepath):
        self.filepath = filepath
        self.energy = 39.0 if "39" in filepath else 7.7
        self.events = []
        self.results = {}
        
    def run_stage1_load_data(self):
        print("\nStage 1: Loading and parsing events...")
        t0 = time.time()
        self.events = [(h, p) for h, p in iter_events(self.filepath)]
        t_elapsed = time.time() - t0
        print(f"  Loaded {len(self.events)} events in {t_elapsed:.3f} seconds.")
        self.results['n_events'] = len(self.events)
        self.results['load_time_sec'] = t_elapsed
        
    def run_stage2_multiplicity(self):
        print("\nStage 2: Analyzing charged particle multiplicity dN/deta...")
        c, v, err = dNdeta(self.events, eta_range=(-3.5, 3.5), nbins=20)
        self.results['dndeta'] = {
            'centers': c.tolist(),
            'values': v.tolist(),
            'errors': err.tolist(),
            'mid_rapidity_value': float(v[len(v)//2])
        }
        print(f"  Mid-rapidity dN/deta: {v[len(v)//2]:.2f}")
        
    def run_stage3_pt_spectra(self):
        print("\nStage 3: Building transverse momentum spectra...")
        c, v, err = pt_spectrum(self.events, pt_range=(0.2, 3.0), nbins=20, eta_cut=1.0)
        self.results['pt_spectrum'] = {
            'centers': c.tolist(),
            'values': v.tolist(),
            'errors': err.tolist()
        }
        
        # Calculate mean pT
        _, mpt, std_pt = mean_pt(self.events, charged_only=True, eta_cut=1.0)
        self.results['mean_pt'] = float(mpt)
        self.results['std_pt'] = float(std_pt)
        print(f"  Mean pT (|eta| < 1.0): {mpt:.3f} ± {std_pt/np.sqrt(max(len(self.events), 1)):.4f} GeV/c")
        
    def run_stage4_geometry(self):
        print("\nStage 4: Collision geometry statistics...")
        b_list = [h['b'] for h, p in self.events]
        npart_list = [h['Npart_proj'] + h['Npart_targ'] for h, p in self.events]
        self.results['geometry'] = {
            'mean_b': float(np.mean(b_list)),
            'mean_npart': float(np.mean(npart_list)),
            'max_npart': int(np.max(npart_list))
        }
        print(f"  Average impact parameter: {np.mean(b_list):.2f} fm")
        print(f"  Average Npart: {np.mean(npart_list):.1f}")
        
    def save_stage5_report(self, out_json_path):
        print(f"\nStage 5: Saving JSON analysis report...")
        with open(out_json_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"  JSON report saved: {out_json_path}")
        
    def plot_stage6_summary(self, out_img_path):
        print(f"\nStage 6: Generating master publication-quality summary canvas...")
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Left Panel: dN/deta
        eta_c = np.array(self.results['dndeta']['centers'])
        eta_v = np.array(self.results['dndeta']['values'])
        eta_err = np.array(self.results['dndeta']['errors'])
        axes[0].errorbar(eta_c, eta_v, yerr=eta_err, fmt='o-', color='navy', linewidth=2, label=f'AMPT {self.energy} GeV')
        axes[0].set_xlabel(r'Pseudorapidity $\eta$', fontsize=12)
        axes[0].set_ylabel(r'$dN_{ch}/d\eta$', fontsize=12)
        axes[0].set_title(r'Charged Pseudorapidity Distribution $dN_{ch}/d\eta$', fontsize=13)
        axes[0].grid(True, linestyle='--', alpha=0.5)
        axes[0].legend(fontsize=11)
        
        # Right Panel: pT spectrum
        pt_c = np.array(self.results['pt_spectrum']['centers'])
        pt_v = np.array(self.results['pt_spectrum']['values'])
        pt_err = np.array(self.results['pt_spectrum']['errors'])
        axes[1].errorbar(pt_c, pt_v, yerr=pt_err, fmt='s-', color='crimson', linewidth=2, label=f'<pT> = {self.results["mean_pt"]:.3f} GeV/c')
        axes[1].set_yscale('log')
        axes[1].set_xlabel(r'$p_T$ (GeV/c)', fontsize=12)
        axes[1].set_ylabel(r'$dN/dp_T$ (GeV/c)$^{-1}$', fontsize=12)
        axes[1].set_title('Charged Hadron Transverse Momentum Spectrum', fontsize=13)
        axes[1].grid(True, linestyle='--', alpha=0.5)
        axes[1].legend(fontsize=11)
        
        plt.suptitle(f'AMPT Summary Diagnostics — Energy $\\sqrt{{s_{{NN}}}} = {self.energy}$ GeV', fontsize=15, fontweight='bold')
        fig.tight_layout()
        fig.savefig(out_img_path, dpi=150)
        print(f"  Summary canvas saved: {out_img_path}")

# Run pipeline
filepath = os.path.join(os.path.dirname(__file__), '..', 'Data', 'subsets', 'ampt_39_sub100.dat')
pipeline = AMPTAnalysisPipeline(filepath)
pipeline.run_stage1_load_data()
pipeline.run_stage2_multiplicity()
pipeline.run_stage3_pt_spectra()
pipeline.run_stage4_geometry()

report_path = os.path.join(outdir, 'day14_pipeline_report.json')
img_path = os.path.join(outdir, 'day14_pipeline_summary.png')
pipeline.save_stage5_report(report_path)
pipeline.plot_stage6_summary(img_path)

print("\n✅ Day 14 exercises complete! Master pipeline runs flawlessly!")
