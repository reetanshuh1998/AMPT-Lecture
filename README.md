# Relativistic Heavy-Ion Kinematics & AMPT Course
===================================================

A comprehensive 14-day hands-on graduate-level course linking theoretical **relativistic kinematics** with numerical **heavy-ion transport modeling** using **AMPT (A Multi-Phase Transport)** simulations.

Designed as a rigorous textbook-driven syllabus grounded deeply in **Chapter 5** of *Relativistic Kinematics: A Journey in Spacetime* (Lecture Notes in Physics, 1046) by **Raghunath Sahoo**.

---

## 🚀 Quick Start

### 1. Environment Setup
Install the necessary computational physics libraries:
```bash
pip install numpy matplotlib scipy jupyter
```

### 2. Slide Deck Compilation
The master presentation slide deck covers the theoretical formulations and experimental detector physics. Compile the Beamer LaTeX deck:
```bash
pdflatex presentation.tex
```
*Result:* Success output generated in [presentation.pdf](file:///home/reet/AMPT-Lecture/presentation.pdf) (27 pages).

### 3. Open Laboratory Notebooks
Launch Jupyter to access the hands-on exercises and full solution references:
```bash
jupyter notebook exercises/day01_hands_on.ipynb
```
*Student Notebook:* [day01_hands_on.ipynb](file:///home/reet/AMPT-Lecture/exercises/day01_hands_on.ipynb) — scaffolded templates with LaTeX equation guides.
*Instructor/Reference Solutions:* [day01_hands_on_solutions.ipynb](file:///home/reet/AMPT-Lecture/exercises/day01_hands_on_solutions.ipynb) — fully solved cells, verified calculations, and generated plots.

---

## 🎨 Interactive HTML5/JS Physics Simulators
The course includes **7 fully functional, interactive animations** located in the `animations/` folder. They can be opened in any web browser instantly to dynamically explore relativistic kinematics:

*   🌐 **[Velocity Saturation Comparison](file:///home/reet/AMPT-Lecture/animations/01_velocity_saturation_comparison.html)** — Classical vs. Relativistic velocity addition: see why successive boosts saturate at $c$, validating Day 1 Laboratory Problem 1.
*   🌐 **[Spacetime Minkowski Diagram](file:///home/reet/AMPT-Lecture/animations/02_spacetime_minkowski_diagram.html)** — Interactive Lorentz boosts: watch hyperbolic axis rotations, moving grids skewing, and toggle the Simultaneity Demo!
*   🌐 **[Resolution vs. Energy Explorer](file:///home/reet/AMPT-Lecture/animations/03_debroglie_resolution_probing.html)** — Wave-particle duality de Broglie wave probe, Airy disk resolution, and concentric target shell penetration visualizer. Validates Slide 4.
*   🌐 **[Collision Kinematics](file:///home/reet/AMPT-Lecture/animations/collision_animation.html)** — Run colliding beams and target nuclei to observe fixed-target center-of-mass energy limits vs. collider linear advantages.
*   🌐 **[Lorentz Boost Demonstrator](file:///home/reet/AMPT-Lecture/animations/rapidity_boost.html)** — Dynamically apply collinear boosts to observe relativistic velocity addition saturation at $c$ while rapidity adds linearly.
*   🌐 **[TPC event display](file:///home/reet/AMPT-Lecture/animations/event_display.html)** — An interactive 3D event tracker simulating charged hadron curvature inside a Time Projection Chamber under high magnetic fields.
*   🌐 **[Transverse Spectra Builder](file:///home/reet/AMPT-Lecture/animations/pt_spectrum_builder.html)** — Interactively adjust slope parameters to fit exponential thermal transverse mass $m_T$ distributions.

---

## 📅 Course Syllabus Layout

### 📌 Week 1: Relativistic Kinematics Fundamentals
*   **Day 1:** Foundations of Relativistic Kinematics, collinear boosts, rapidity additivity proofs, CMS kinematics, layered onion detector configurations (ALICE/STAR/CMS), and Bjorken scaling spacetime-momentum correlations.
*   **Day 2:** Kinematics I: 4-vectors & CMS energy conversions.
*   **Day 3:** Kinematics II: Rapidity, Pseudorapidity boundaries, and physical limits.
*   **Day 4:** Kinematics III: Invariant Yield & Phase Space Jacobian invariance.

### 📌 Week 2: AMPT Physics & Mechanics
*   **Day 5:** AMPT transport stages (HIJING initial overlap, ZPC parton cascade, coalescence hadronization, ART hadronic transport).
*   **Day 6:** AMPT Data parsing: streaming event headers and particle tracking.
*   **Day 7:** Single-Particle Observables: multiplicity counts & transverse spectra ($p_T$).

### 📌 Week 3: Thermodynamics & Collectivity
*   **Day 8:** Transverse Spectra, Identified Particles & thermal $m_T$ scaling.
*   **Day 9:** Centrality & Geometry: Glauber vs. AMPT overlap models.
*   **Day 10:** Collective Flow: Elliptic Flow ($v_2$) Event Plane evaluations.
*   **Day 11:** Medium Modification: Parton cross sections, Debye screening, and mean free path.

### 📌 Week 4: Advanced Scans & Modular Pipelines
*   **Day 12:** Energy Scan: Beam Energy Scan (STAR at RHIC) systematic comparisons.
*   **Day 13:** Advanced Analysis: Vectorized two-particle correlations ($\Delta\eta, \Delta\phi$).
*   **Day 14:** Course Wrap-Up: Building a reproducible modular HEP data pipeline.

---

## 📚 References & Standards
1.  **Sahoo, Raghunath (2021).** *Relativistic Kinematics: A Journey in Spacetime* (Lecture Notes in Physics, 1046). Springer.
2.  **Lin, Z.-W., Ko, C. M., Li, B.-A., Zhang, B., & Pal, S. (2005).** *A Multi-Phase Transport Model for Relativistic Heavy-Ion Collisions*. Physical Review C, 72(6), 064901.
3.  **Bethe-Bloch & Cherenkov Formulations:** Particle Data Group (PDG) standards.
