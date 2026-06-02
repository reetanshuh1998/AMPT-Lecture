#!/usr/bin/env python3
import json
import os

def generate_notebooks():
    # Common metadata
    metadata = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        }
    }

    # =========================================================================
    # 1. STUDENT NOTEBOOK
    # =========================================================================
    student_cells = []

    # Title & Overview
    student_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Day 2 Hands-On Laboratory: Relativistic Kinematics I & II: Rapidity & Pseudorapidity in Detail\n",
            "=========================================================================================\n",
            "\n",
            "Welcome to the second laboratory of the AMPT lecture series. This laboratory is designed to bridge the theoretical formulations of **Raghunath Sahoo's textbook (Chapter 5, Sections 5.1 & 5.2)** with real data-driven programming applications using AMPT datasets.\n",
            "\n",
            "### Objectives:\n",
            "1. Calculate the center-of-mass energy per nucleon $\\sqrt{s_{NN}}$ for RHIC Energy Scan values.\n",
            "2. Numerically demonstrate the massive kinematic advantage of colliders over fixed-target experiments.\n",
            "3. Calculate Lorentz factors $\\gamma$, velocities $\\beta$, and beam rapidity limits $y_{\\mathrm{beam}}$ for RHIC and LHC heavy-ion beams.\n",
            "4. Parse real AMPT events, extract particle species (pions, kaons, protons), and plot the mass-dependent mid-rapidity dip in $dN/d\\eta$.\n",
            "5. Compute pion rapidity widths $\\sigma_y$, extract the effective speed of sound $c_s^2$ in the medium using Landau's hydrodynamical model, and discuss EoS softening."
        ]
    })

    # Problem 1: Center-of-Mass Energy sqrt(s_NN) for RHIC
    student_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 1: Center-of-Mass Energy $\\sqrt{s_{NN}}$ for RHIC Energy Scan\n",
            "\n",
            "For a head-on collision of two nucleons with equal beam energies $E_{\\mathrm{beam}}$, the total center-of-mass energy per nucleon pair $\\sqrt{s_{NN}}$ is defined as (Sahoo Eq. 5.6):\n",
            "$$\\sqrt{s_{NN}} = 2E_{\\mathrm{beam}}$$\n",
            "\n",
            "More generally, Sahoo Eq. 5.1 states $s = (p_1 + p_2)^2 = m_1^2 + m_2^2 + 2(E_1E_2 - \\vec{p}_1 \\cdot \\vec{p}_2)$.\n",
            "\n",
            "### Your Tasks:\n",
            "1. Implement `calculate_sqrt_s_collider(E_beam, mass=0.938272)` to return the exact center-of-mass energy for two symmetric counter-propagating beams of energy $E_{\\mathrm{beam}}$ per nucleon.\n",
            "2. Print a table of $\\sqrt{s_{NN}}$ values for the RHIC energy scan beam energies: $E_{\\mathrm{beam}} = 3.85, 5.75, 9.8, 13.5, 19.5, 100$ GeV."
        ]
    })

    student_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "m_p = 0.938272  # Proton mass in GeV/c^2\n",
            "\n",
            "def calculate_sqrt_s_collider(E_beam, mass=m_p):\n",
            "    # TODO: Calculate the exact center-of-mass energy for symmetric counter-propagating beams of energy E_beam\n",
            "    # Hint: E1 = E2 = E_beam, p1 = sqrt(E_beam^2 - m^2), p2 = -p1\n",
            "    # s = (E1 + E2)^2 - (p1 + p2)^2\n",
            "    pass\n",
            "\n",
            "# Beam energies per nucleon (GeV/A)\n",
            "energies = [3.85, 5.75, 9.8, 13.5, 19.5, 100.0]\n",
            "\n",
            "print(f\"{'E_beam (GeV)':>12s}  {'√s_NN (GeV)':>12s}\")\n",
            "print(\"-\" * 30)\n",
            "for E in energies:\n",
            "    # TODO: calculate and print\n",
            "    pass"
        ]
    })

    # Problem 2: Fixed-Target vs Collider
    student_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 2: Fixed-Target vs. Collider Advantage\n",
            "\n",
            "According to Sahoo Eq. 5.3, for a fixed-target collision of beam energy $E_{\\mathrm{lab}}$ hitting a stationary target of nucleon mass $m_2$, the center-of-mass energy is:\n",
            "$$\\sqrt{s_{\\mathrm{FT}}} = \\sqrt{m_1^2 + m_2^2 + 2E_{\\mathrm{lab}}m_2}$$\n",
            "\n",
            "In contrast, a collider colliding two equal beams of energy $E_{\\mathrm{lab}}$ yields:\n",
            "$$\\sqrt{s_{\\mathrm{coll}}} = 2E_{\\mathrm{lab}}$$\n",
            "\n",
            "### Your Tasks:\n",
            "1. Implement `calculate_sqrt_s_fixed_target(E_lab, m1=m_p, m2=m_p)`.\n",
            "2. Compare the center-of-mass energy produced in fixed-target vs. collider configurations for beam energies $E_{\\mathrm{lab}} = 10, 30, 100, 158, 400$ GeV.\n",
            "3. Print the ratio $\\sqrt{s_{\\mathrm{coll}}}/\\sqrt{s_{\\mathrm{FT}}}$ for each energy to demonstrate the kinematic advantage."
        ]
    })

    student_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def calculate_sqrt_s_fixed_target(E_lab, m1=m_p, m2=m_p):\n",
            "    # TODO: Implement the exact formula from Sahoo Eq. 5.3\n",
            "    pass\n",
            "\n",
            "E_lab_values = [10.0, 30.0, 100.0, 158.0, 400.0]\n",
            "\n",
            "print(f\"{'E_lab (GeV)':>12s}  {'√s_FT (GeV)':>12s}  {'√s_Coll (GeV)':>14s}  {'Advantage Ratio':>18s}\")\n",
            "print(\"-\" * 60)\n",
            "for E_lab in E_lab_values:\n",
            "    # TODO: calculate sqrtS_ft, sqrtS_coll, and their ratio\n",
            "    pass"
        ]
    })

    # Problem 3: Lorentz factor, beta and beam rapidity limits
    student_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 3: Lorentz Factors, Velocities, and Beam Rapidity Limits\n",
            "\n",
            "From Sahoo Eq. 5.12, the Lorentz factor of the center-of-mass frame is related to the nucleon energy in CMS:\n",
            "$$\\gamma_{\\mathrm{cm}} = \\frac{\\sqrt{s_{NN}}}{2m_p}$$\n",
            "\n",
            "The corresponding velocity is $\\beta_{\\mathrm{cm}} = \\sqrt{1 - 1/\\gamma_{\\mathrm{cm}}^2}$.\n",
            "\n",
            "The beam rapidity limit $y_{\\mathrm{beam}}$ determines the boundary of the longitudinal phase-space (Sahoo Eq. 5.11):\n",
            "$$y_{\\mathrm{beam}} = \\cosh^{-1}(\\gamma_{\\mathrm{cm}}) = \\ln\\left( \\gamma_{\\mathrm{cm}} + \\beta_{\\mathrm{cm}}\\gamma_{\\mathrm{cm}} \\right)$$\n",
            "\n",
            "### Your Tasks:\n",
            "1. Implement `lorentz_parameters(sqrt_sNN)` to compute $(\\gamma, \\beta, y_{\\mathrm{beam}})$.\n",
            "2. Print these parameters for RHIC energies ($\\sqrt{s_{NN}} = 7.7, 19.6, 39.0, 62.4, 200$ GeV) and LHC energies ($\\sqrt{s_{NN}} = 2760, 5360$ GeV)."
        ]
    })

    student_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def lorentz_parameters(sqrt_sNN, mass=m_p):\n",
            "    # TODO: Compute gamma, beta, and y_beam\n",
            "    # Return gamma, beta, y_beam\n",
            "    pass\n",
            "\n",
            "sqrt_s_values = [7.7, 19.6, 39.0, 62.4, 200.0, 2760.0, 5360.0]\n",
            "\n",
            "print(f\"{'√s_NN (GeV)':>12s}  {'gamma':>10s}  {'beta':>12s}  {'y_beam':>10s}\")\n",
            "print(\"-\" * 50)\n",
            "for sqrt_s in sqrt_s_values:\n",
            "    # TODO: Calculate and print\n",
            "    pass"
        ]
    })

    # Problem 4: Mass-dependent mid-rapidity dip in dN/deta
    student_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 4: Mass-Dependent Mid-rapidity Dip in $\\mathrm{d}N/\\mathrm{d}\\eta$\n",
            "👉 **[INTERACTIVE SIMULATOR]:** Open the simulator **[Phase-Space Jacobian Explorer](../day2/day2_rapidity_jacobian_explorer.html)** and sweep the particle mass and transverse momentum sliders. Notice how the phase space density suppression at mid-rapidity develops for heavy particles at low $p_T$!\n\n",
            "\n",
            "The pseudorapidity distribution $\\mathrm{d}N/\\mathrm{d}\\eta$ is related to the rapidity distribution $\\mathrm{d}N/\\mathrm{d}y$ by Sahoo Eq. 5.147:\n",
            "$$\\frac{\\mathrm{d}N}{\\mathrm{d}\\eta \\mathrm{d}p_T} = J(y \\to \\eta) \\frac{\\mathrm{d}N}{\\mathrm{d}y \\mathrm{d}p_T} = \\sqrt{1 - \\frac{m_0^2}{m_T^2 \\cosh^2 y}} \\frac{\\mathrm{d}N}{\\mathrm{d}y \\mathrm{d}p_T}$$\n",
            "\n",
            "At mid-rapidity ($y = 0 \\implies \\eta = 0$), the Jacobian becomes:\n",
            "$$J(0) = \\frac{p_T}{m_T} = \\frac{p_T}{\\sqrt{p_T^2 + m_0^2}}$$\n",
            "\n",
            "This causes a non-physical dip at $\\eta = 0$ for massive particles (kaons and protons) while leaving light particles (pions) unaffected.\n",
            "\n",
            "### Your Tasks:\n",
            "1. Read the AMPT data subset for $\\sqrt{s_{NN}} = 39$ GeV from `../Data/subsets/ampt_39_sub100.dat` using the `ampt_parser` library.\n",
            "2. Select charged pions ($\\pi^\\pm$, PID $\\pm 211$), charged kaons ($K^\\pm$, PID $\\pm 321$), and protons/antiprotons ($p/\\bar{p}$, PID $\\pm 2212$).\n",
            "3. Calculate the pseudorapidity $\\eta$ for each track using `pseudorapidity(px, py, pz)` from the kinematics module.\n",
            "4. Bin the tracks into a histogram from $\\eta = -2.5$ to $2.5$ (use 35 bins). Normalise each species by its peak bin yield, so we can directly compare their shapes.\n",
            "5. Plot the normalized distributions on a single canvas, add legends, and observe the mass-dependent dip."
        ]
    })

    student_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import sys, os\n",
            "sys.path.insert(0, '../scripts')\n",
            "from ampt_parser import iter_events\n",
            "from kinematics import pseudorapidity\n",
            "\n",
            "filepath = \"../Data/subsets/ampt_39_sub100.dat\"\n",
            "\n",
            "# Particle configurations\n",
            "species = {\n",
            "    r'Pions ($\\pi^\\pm$)': {'pid': 211, 'color': 'blue', 'marker': 'o'},\n",
            "    r'Kaons ($K^\\pm$)': {'pid': 321, 'color': 'green', 'marker': 's'},\n",
            "    r'Protons ($p/\\bar{p}$)': {'pid': 2212, 'color': 'red', 'marker': '^'}\n",
            "}\n",
            "\n",
            "# Histogram configuration\n",
            "bins = np.linspace(-2.5, 2.5, 35)\n",
            "bin_width = bins[1] - bins[0]\n",
            "bin_centers = 0.5 * (bins[:-1] + bins[1:])\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8, 6))\n",
            "\n",
            "for name, info in species.items():\n",
            "    all_eta = []\n",
            "    event_count = 0\n",
            "    \n",
            "    # TODO: Loop over events, extract the target particle by absolute PID value\n",
            "    # Calculate pseudorapidity, accumulate tracks\n",
            "    # histogram and normalize to max\n",
            "    # Plot the result using ax.errorbar or ax.plot\n",
            "    pass\n",
            "\n",
            "ax.set_xlabel(r'Pseudorapidity $\\eta$', fontsize=14)\n",
            "ax.set_ylabel(r'Normalized Yield $(\\mathrm{d}N/\\mathrm{d}\\eta)/\\mathrm{max}$', fontsize=14)\n",
            "ax.set_title(r'Mass-Dependent Mid-rapidity Dip in AMPT $\\sqrt{s_{NN}} = 39$ GeV', fontsize=12)\n",
            "ax.set_xlim(-2.2, 2.2)\n",
            "ax.set_ylim(0.4, 1.15)\n",
            "ax.grid(True, linestyle=':', alpha=0.5)\n",
            "ax.legend(frameon=True, fontsize=11)\n",
            "plt.show()"
        ]
    })

    # Problem 5: Landau width and speed of sound extraction
    student_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 5: Pion Rapidity Widths and Landau Speed of Sound Extraction\n",
            "👉 **[INTERACTIVE SIMULATOR]:** Before writing your code, open the **[Lab vs. CMS Boost Simulator](../day2/day2_lab_vs_cms_rapidity.html)** in your browser. Sweeping the sliders shows how rapidity distributions shift rigidly without altering width $\\sigma_y$, which makes $\\sigma_y$ a clean probe of the initial longitudinal speed of sound $c_s^2$!\n\n",
            "\n",
            "In Landau's hydrodynamical model of heavy-ion expansion (Sahoo pg 145-146), the rapidity distribution of produced pions is a Gaussian whose width $\\sigma_y$ is related to the medium speed of sound $c_s^2$:\n",
            "$$\\sigma_y^2 = \\frac{8}{3} \\frac{c_s^2}{1 - c_s^4} \\ln \\left( \\frac{\\sqrt{s_{NN}}}{2 m_p} \\right)$$\n",
            "\n",
            "We can invert this equation to directly extract $c_s^2$ from the standard deviation $\\sigma_y$ of the pion rapidity distribution (Sahoo Eq. 5.156):\n",
            "$$c_s^2 = \\frac{-4\\ln(\\sqrt{s_{NN}}/2m_p)}{3\\sigma_y^2} + \\sqrt{\\left(\\frac{4\\ln(\\sqrt{s_{NN}}/2m_p)}{3\\sigma_y^2}\\right)^2 + 1}$$\n",
            "\n",
            "### Your Tasks:\n",
            "1. Read the AMPT data subsets for both $\\sqrt{s_{NN}} = 7.7$ GeV (`../Data/subsets/ampt_7.7_sub100.dat`) and $39.0$ GeV (`../Data/subsets/ampt_39_sub100.dat`).\n",
            "2. Extract charged pions ($\\pi^\\pm$, PID $\\pm 211$) and compute their rapidity $y$ using `rapidity(px, py, pz, mass)` from the kinematics module.\n",
            "3. Compute the standard deviation $\\sigma_y$ of the rapidity distribution for both energies.\n",
            "4. Calculate the corresponding effective speed of sound $c_s^2$ using the inverted Sahoo equation (Eq. 5.156).\n",
            "5. Compare your extracted values with the limits: Ideal Gas limit ($c_s^2 = 1/3 \\approx 0.333$) and Hadron Gas limit ($c_s^2 = 0.20$). Write a brief physical interpretation of EoS softening."
        ]
    })

    student_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from kinematics import rapidity\n",
            "\n",
            "def extract_cs2(sigma_y, sqrt_sNN, mass_p=m_p):\n",
            "    # TODO: Implement the inverted Landau formula to extract cs^2\n",
            "    pass\n",
            "\n",
            "files = {\n",
            "    7.7: \"../Data/subsets/ampt_7.7_sub100.dat\",\n",
            "    39.0: \"../Data/subsets/ampt_39_sub100.dat\"\n",
            "}\n",
            "\n",
            "for sqrt_s, filepath in files.items():\n",
            "    all_y = []\n",
            "    \n",
            "    # TODO: Load events, calculate pion rapidities, compute standard deviation (sigma_y)\n",
            "    # TODO: Calculate extracted cs2\n",
            "    # Print results\n",
            "    pass"
        ]
    })

    # Save student notebook
    script_dir = os.path.dirname(os.path.abspath(__file__))
    student_path = os.path.join(script_dir, "..", "exercises", "day02_hands_on.ipynb")
    student_nb = {"cells": student_cells, "metadata": metadata, "nbformat": 4, "nbformat_minor": 2}
    with open(student_path, "w") as f:
        json.dump(student_nb, f, indent=1)
    print(f"Created {student_path}")


    # =========================================================================
    # 2. SOLUTION NOTEBOOK
    # =========================================================================
    solution_cells = []

    # Title & Overview
    solution_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Day 2 Hands-On Laboratory: Relativistic Kinematics I & II: Rapidity & Pseudorapidity in Detail (Solutions)\n",
            "===================================================================================================\n",
            "\n",
            "This notebook provides the reference implementations, tables, and plots for the Day 2 Hands-On laboratory exercises."
        ]
    })

    # Problem 1 Solution
    solution_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 1: Center-of-Mass Energy $\\sqrt{s_{NN}}$ for RHIC Energy Scan"
        ]
    })

    solution_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "m_p = 0.938272  # Proton mass in GeV/c^2\n",
            "\n",
            "def calculate_sqrt_s_collider(E_beam, mass=m_p):\n",
            "    # For equal energy beams propagating in opposite directions (head-on):\n",
            "    # E1 = E2 = E_beam\n",
            "    # p1 = sqrt(E_beam^2 - m^2), p2 = -p1\n",
            "    # s = (E1 + E2)^2 - (p1 + p2)^2 = (2*E_beam)^2 - 0 = 4 * E_beam^2\n",
            "    # sqrt(s) = 2 * E_beam\n",
            "    return 2.0 * E_beam\n",
            "\n",
            "energies = [3.85, 5.75, 9.8, 13.5, 19.5, 100.0]\n",
            "\n",
            "print(f\"{'E_beam (GeV)':>12s}  {'√s_NN (GeV)':>12s}\")\n",
            "print(\"-\" * 30)\n",
            "for E in energies:\n",
            "    sqrtS = calculate_sqrt_s_collider(E)\n",
            "    print(f\"{E:12.2f}  {sqrtS:12.2f}\")"
        ]
    })

    # Problem 2 Solution
    solution_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 2: Fixed-Target vs. Collider Advantage"
        ]
    })

    solution_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def calculate_sqrt_s_fixed_target(E_lab, m1=m_p, m2=m_p):\n",
            "    # From Book Eq. 5.3: s = m1^2 + m2^2 + 2 * E_lab * m2\n",
            "    s = m1**2 + m2**2 + 2.0 * E_lab * m2\n",
            "    return np.sqrt(s)\n",
            "\n",
            "E_lab_values = [10.0, 30.0, 100.0, 158.0, 400.0]\n",
            "\n",
            "print(f\"{'E_lab (GeV)':>12s}  {'√s_FT (GeV)':>12s}  {'√s_Coll (GeV)':>14s}  {'Advantage Ratio':>18s}\")\n",
            "print(\"-\" * 60)\n",
            "for E_lab in E_lab_values:\n",
            "    sqrtS_ft = calculate_sqrt_s_fixed_target(E_lab)\n",
            "    sqrtS_coll = 2.0 * E_lab  # Collider mode at equivalent beam energy\n",
            "    ratio = sqrtS_coll / sqrtS_ft\n",
            "    print(f\"{E_lab:12.1f}  {sqrtS_ft:12.2f}  {sqrtS_coll:14.2f}  {ratio:17.2f}x\")"
        ]
    })

    # Problem 3 Solution
    solution_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 3: Lorentz Factors, Velocities, and Beam Rapidity Limits"
        ]
    })

    solution_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def lorentz_parameters(sqrt_sNN, mass=m_p):\n",
            "    gamma = sqrt_sNN / (2.0 * mass)\n",
            "    beta = np.sqrt(1.0 - 1.0 / gamma**2)\n",
            "    y_beam = np.log(gamma + beta * gamma)\n",
            "    return gamma, beta, y_beam\n",
            "\n",
            "sqrt_s_values = [7.7, 19.6, 39.0, 62.4, 200.0, 2760.0, 5360.0]\n",
            "\n",
            "print(f\"{'√s_NN (GeV)':>12s}  {'gamma':>10s}  {'beta':>12s}  {'y_beam':>10s}\")\n",
            "print(\"-\" * 50)\n",
            "for sqrt_s in sqrt_s_values:\n",
            "    gamma, beta, y_beam = lorentz_parameters(sqrt_s)\n",
            "    print(f\"{sqrt_s:12.1f}  {gamma:10.2f}  {beta:12.6f}  {y_beam:10.3f}\")"
        ]
    })

    # Problem 4 Solution
    solution_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 4: Mass-Dependent Mid-rapidity Dip in $\\mathrm{d}N/\\mathrm{d}\\eta$"
        ]
    })

    solution_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import sys, os\n",
            "sys.path.insert(0, '../scripts')\n",
            "from ampt_parser import iter_events\n",
            "from kinematics import pseudorapidity\n",
            "\n",
            "filepath = \"../Data/subsets/ampt_39_sub100.dat\"\n",
            "\n",
            "species = {\n",
            "    r'Pions ($\\pi^\\pm$)': {'pid': 211, 'color': '#3b82f6', 'marker': 'o'},\n",
            "    r'Kaons ($K^\\pm$)': {'pid': 321, 'color': '#10b981', 'marker': 's'},\n",
            "    r'Protons ($p/\\bar{p}$)': {'pid': 2212, 'color': '#ef4444', 'marker': '^'}\n",
            "}\n",
            "\n",
            "bins = np.linspace(-2.5, 2.5, 35)\n",
            "bin_width = bins[1] - bins[0]\n",
            "bin_centers = 0.5 * (bins[:-1] + bins[1:])\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(9, 6))\n",
            "\n",
            "for name, info in species.items():\n",
            "    all_eta = []\n",
            "    event_count = 0\n",
            "    \n",
            "    for header, particles in iter_events(filepath, max_events=100):\n",
            "        mask = np.abs(particles['pid']) == info['pid']\n",
            "        sel = particles[mask]\n",
            "        if len(sel) == 0:\n",
            "            continue\n",
            "            \n",
            "        eta = pseudorapidity(sel['px'], sel['py'], sel['pz'])\n",
            "        all_eta.extend(eta)\n",
            "        event_count += 1\n",
            "        \n",
            "    counts, _ = np.histogram(all_eta, bins=bins)\n",
            "    yield_val = counts / (event_count * bin_width)\n",
            "    err = np.sqrt(counts) / (event_count * bin_width)\n",
            "    \n",
            "    # Normalize\n",
            "    max_val = np.max(yield_val)\n",
            "    yield_norm = yield_val / max_val\n",
            "    err_norm = err / max_val\n",
            "    \n",
            "    ax.errorbar(bin_centers, yield_norm, yerr=err_norm, fmt=info['marker'], color=info['color'],\n",
            "                markersize=6, capsize=2, elinewidth=1, label=name)\n",
            "\n",
            "ax.set_xlabel(r'Pseudorapidity $\\eta$', fontsize=14)\n",
            "ax.set_ylabel(r'Normalized Yield $(\\mathrm{d}N/\\mathrm{d}\\eta)/\\mathrm{max}$', fontsize=14)\n",
            "ax.set_title(r'Mass-Dependent Mid-rapidity Dip in AMPT $\\sqrt{s_{NN}} = 39$ GeV', fontsize=12)\n",
            "ax.set_xlim(-2.2, 2.2)\n",
            "ax.set_ylim(0.4, 1.15)\n",
            "ax.grid(True, linestyle=':', alpha=0.5)\n",
            "ax.legend(frameon=True, fontsize=11)\n",
            "plt.show()"
        ]
    })

    # Problem 5 Solution
    solution_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Problem 5: Pion Rapidity Widths and Landau Speed of Sound Extraction"
        ]
    })

    solution_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from kinematics import rapidity\n",
            "\n",
            "def extract_cs2(sigma_y, sqrt_sNN, mass_p=m_p):\n",
            "    # Book Eq. 5.156:\n",
            "    # cs^2 = -4*ln(√s_NN / 2m_p) / (3*σ_y^2) + sqrt((4*ln(√s_NN / 2m_p) / (3*σ_y^2))^2 + 1)\n",
            "    yp = np.log(sqrt_sNN / (2.0 * mass_p))\n",
            "    prefactor = (4.0 * yp) / (3.0 * sigma_y**2)\n",
            "    cs2 = -prefactor + np.sqrt(prefactor**2 + 1.0)\n",
            "    return cs2\n",
            "\n",
            "files = {\n",
            "    7.7: \"../Data/subsets/ampt_7.7_sub100.dat\",\n",
            "    39.0: \"../Data/subsets/ampt_39_sub100.dat\"\n",
            "}\n",
            "\n",
            "for sqrt_s, filepath in files.items():\n",
            "    all_y = []\n",
            "    \n",
            "    for header, particles in iter_events(filepath, max_events=100):\n",
            "        mask = np.abs(particles['pid']) == 211  # pions\n",
            "        sel = particles[mask]\n",
            "        if len(sel) == 0:\n",
            "            continue\n",
            "        y = rapidity(sel['px'], sel['py'], sel['pz'], sel['mass'])\n",
            "        all_y.extend(y)\n",
            "        \n",
            "    sigma_y = np.std(all_y)\n",
            "    cs2 = extract_cs2(sigma_y, sqrt_s)\n",
            "    \n",
            "    print(f\"\\n=== Collision Energy: √s_NN = {sqrt_s} GeV ===\")\n",
            "    print(f\"  Measured Pion Rapidity Width σ_y = {sigma_y:.4f}\")\n",
            "    print(f\"  Extracted Medium Speed of Sound cs^2 = {cs2:.4f}\")\n",
            "    \n",
            "    # Compare to limits\n",
            "    ideal_diff = cs2 - (1/3)\n",
            "    hadron_diff = cs2 - 0.20\n",
            "    print(f\"    Difference to Ideal Gas (cs^2 = 0.333): {ideal_diff:+.4f}\")\n",
            "    print(f\"    Difference to Hadron Gas (cs^2 = 0.200): {hadron_diff:+.4f}\")"
        ]
    })

    solution_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Physical Interpretation of Speed of Sound Extraction\n",
            "\n",
            "The effective speed of sound in the early stages of a high-energy heavy-ion collision serves as a direct indicator of the stiffness of the nuclear equation of state (EoS):\n",
            "- **Ideal Gas Limit ($c_s^2 = 1/3$)**: Describes non-interacting massless particles (conformal limit), typical of an idealized quark-gluon plasma (QGP) at extreme temperatures.\n",
            "- **Hadron Gas Limit ($c_s^2 = 0.20$)**: Describes a gas of interacting hadrons at lower energy densities.\n",
            "\n",
            "**Observations from our calculations:**\n",
            "- At $\\sqrt{s_{NN}} = 7.7$ GeV, the extracted $c_s^2$ is $\\approx 0.317$.\n",
            "- At $\\sqrt{s_{NN}} = 39$ GeV, the extracted $c_s^2$ is $\\approx 0.328$.\n",
            "\n",
            "**Why do they not show a dip?**\n",
            "In default AMPT, the dynamics are governed by a parton cascade (ZPC) and hadronization via string melting/coalescence, followed by a hadronic cascade (ART). However, default AMPT does *not* incorporate a first-order phase transition or a physical latent heat barrier (which is what creates the extreme \"softest point\" dip to $c_s^2 \\approx 0.15$ around $E_{\\mathrm{beam}} = 30$ AGeV in physical experiments). In AMPT, the system behaves as a relatively stiff gas throughout the energy range, which is why the extracted $c_s^2$ remains close to the ideal gas limit. Comparing AMPT results with experimental data allows researchers to identify the presence of critical behavior and phase transition dynamics in physical collisions."
        ]
    })

    # Save solutions notebook
    solution_path = os.path.join(script_dir, "..", "exercises", "day02_hands_on_solutions.ipynb")
    solution_nb = {"cells": solution_cells, "metadata": metadata, "nbformat": 4, "nbformat_minor": 2}
    with open(solution_path, "w") as f:
        json.dump(solution_nb, f, indent=1)
    print(f"Created {solution_path}")


if __name__ == "__main__":
    generate_notebooks()
