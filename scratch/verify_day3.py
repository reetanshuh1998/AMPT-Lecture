#!/usr/bin/env python3
"""
verify_day3.py — Verification script for Day 3 materials.
Checks file presence, compiles Python files to check syntax, and parses Jupyter notebooks.
"""

import os
import json
import py_compile
import sys

# Workspace directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FILES_TO_CHECK = [
    # Day 3 scripts
    os.path.join(BASE_DIR, 'day3', 'analyze_day3.py'),
    # Animations
    os.path.join(BASE_DIR, 'animations', '06_feynman_scaling_plateau.html'),
    os.path.join(BASE_DIR, 'animations', '09_pt_mt_spectra_analyzer.html'),
    os.path.join(BASE_DIR, 'animations', '10_van_hove_phase_transition.html'),
    os.path.join(BASE_DIR, 'animations', '11_detector_luminosity_meaning.html'),
    os.path.join(BASE_DIR, 'animations', '12_pt_thermal_powerlaw.html'),
    # Exercises
    os.path.join(BASE_DIR, 'exercises', 'day03_hands_on.ipynb'),
    os.path.join(BASE_DIR, 'exercises', 'day03_hands_on_solutions.ipynb'),
    # Presentation
    os.path.join(BASE_DIR, 'presentation_day3.tex')
]

def main():
    print("====================================================")
    print("Starting Day 3 Static Verification Suite...")
    print("====================================================")
    
    all_ok = True
    
    # 1. Check file existence
    print("\n1. Checking file existence...")
    for f in FILES_TO_CHECK:
        rel_path = os.path.relpath(f, BASE_DIR)
        if os.path.exists(f):
            print(f"  [OK] Found {rel_path}")
        else:
            print(f"  [FAIL] Missing {rel_path}")
            all_ok = False
            
    # 2. Check Python syntax compilation
    print("\n2. Compiling Python scripts...")
    py_files = [f for f in FILES_TO_CHECK if f.endswith('.py')]
    for py_f in py_files:
        rel_path = os.path.relpath(py_f, BASE_DIR)
        try:
            py_compile.compile(py_f, doraise=True)
            print(f"  [OK] Compiled {rel_path} successfully (syntax is correct)")
        except py_compile.PyCompileError as e:
            print(f"  [FAIL] Compilation error in {rel_path}:\n{e}")
            all_ok = False
            
    # 3. Check Jupyter Notebook JSON syntax
    print("\n3. Validating Jupyter Notebook JSON structures...")
    ipynb_files = [f for f in FILES_TO_CHECK if f.endswith('.ipynb')]
    for ipynb_f in ipynb_files:
        rel_path = os.path.relpath(ipynb_f, BASE_DIR)
        try:
            with open(ipynb_f, 'r') as f:
                data = json.load(f)
            # Basic Jupyter structural checks
            if 'cells' in data and 'metadata' in data and 'nbformat' in data:
                print(f"  [OK] JSON parsed successfully for {rel_path}")
            else:
                print(f"  [FAIL] Missing standard Jupyter keys in {rel_path}")
                all_ok = False
        except json.JSONDecodeError as e:
            print(f"  [FAIL] JSON syntax error in {rel_path}:\n{e}")
            all_ok = False
            
    # 4. Check HTML structures
    print("\n4. Checking HTML structure...")
    html_files = [f for f in FILES_TO_CHECK if f.endswith('.html')]
    for html_f in html_files:
        rel_path = os.path.relpath(html_f, BASE_DIR)
        try:
            with open(html_f, 'r') as f:
                content = f.read()
            if "<!DOCTYPE html>" in content and "</html>" in content:
                print(f"  [OK] Valid HTML skeleton in {rel_path}")
            else:
                print(f"  [FAIL] Invalid HTML skeleton in {rel_path}")
                all_ok = False
        except Exception as e:
            print(f"  [FAIL] Error reading {rel_path}:\n{e}")
            all_ok = False

    print("\n====================================================")
    if all_ok:
        print("ALL STATIC CHECKS PASSED SUCCESSFULLY!")
        print("The files are syntactically valid and properly placed.")
    else:
        print("SOME CHECKS FAILED. Please review the errors above.")
    print("====================================================")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
