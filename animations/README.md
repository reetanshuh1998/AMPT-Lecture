# Graduate Physics Animation Suite: Learning Guides

This directory contains **6 interactive HTML5/JavaScript simulators** designed to validate the core physics concepts of Relativistic Heavy-Ion Kinematics and AMPT transport modeling, as detailed in **Chapter 5 of Sahoo's textbook**.

---

## 🚀 1. Velocity Saturation Comparison
* **File**: [01_velocity_saturation_comparison.html](01_velocity_saturation_comparison.html)
* **Learning Objective**: Understand why the speed of light $c$ is the absolute cosmic speed limit. Observe how non-linear relativistic transformations prevent velocities from exceeding $c$.
* **Difficulty**: Beginner
* **Recommended Run Time**: 2–3 minutes
* **Key Takeaway**: Under classical addition ($v_c = \sum v_i$), 10 successive boosts of $0.1c$ linearly reach $1.0c$ and exceed it. Relativistically, the denominator dampening factor in $w = \frac{v+u}{1+vu/c^2}$ forces the total velocity to saturate asymptotically at $0.763c$ (and remains $<1c$ for infinite boosts).
* **Reference**: Sahoo Chapter 5.1.2; Beamer Slide 14.

---

## 📐 2. Spacetime Minkowski Diagram
* **File**: [02_spacetime_minkowski_diagram.html](02_spacetime_minkowski_diagram.html)
* **Learning Objective**: Visualize Lorentz boosts as hyperbolic coordinate rotations in Minkowski space and explore the Relativity of Simultaneity.
* **Difficulty**: Intermediate
* **Recommended Run Time**: 4–5 minutes
* **Key Takeaway**: Boosts skew the time axis $ct'$ and spatial axis $x'$ symmetrically towards the invariant light cone ($x = \pm ct$). The faint moving coordinate grid shows length contraction and time dilation. Toggling the *Simultaneity Demo* reveals how events $A$ and $B$, simultaneous in the rest frame ($ct = 1.0$), occur at different times in the moving frame ($t'_B < t'_A$).
* **Reference**: Sahoo Chapter 5.1; Beamer Slide 16 & 21.

---

## 🌐 3. Lorentz Boost Demonstrator (dN/dy vs. dN/dη)
* **File**: [rapidity_boost.html](rapidity_boost.html)
* **Learning Objective**: Contrast the Lorentz-invariance of rapidity $y$ with the shift and shape-change of pseudorapidity $\eta$ under boosts.
* **Difficulty**: Intermediate
* **Recommended Run Time**: 3–5 minutes
* **Key Takeaway**: True rapidity distributions $dN/dy$ shift rigidly along the rapidity axis without changing shape under boosts. Pseudorapidity distributions $dN/d\eta$ skew and change shape because the Jacobian factor $J(y \to \eta)$ depends non-trivially on the boost velocity $\beta$ and particle mass.
* **Reference**: Sahoo Chapter 5.2.2; Beamer Slide 18 & 26.

---

## 💥 4. Heavy-Ion Collision Stages
* **File**: [collision_animation.html](collision_animation.html)
* **Learning Objective**: Chronologically trace the 5 dynamical epochs of a heavy-ion collision from initial Lorentz-contracted nuclei to final-state freeze-out.
* **Difficulty**: Advanced
* **Recommended Run Time**: 5 minutes
* **Key Takeaway**: Observe Woods-Saxon nucleon distributions, Lorentz contraction of oncoming nuclei, the formation and cooling of QGP (fireball temperature decay), parton coalescence, hadronization, and freeze-out scatterings.
* **Reference**: Sahoo Chapter 5.3; Beamer Slide 22.

---

## 🧲 5. Time Projection Chamber (TPC) Event Display
* **File**: [event_display.html](event_display.html)
* **Learning Objective**: Visualize charged hadron tracking, momentum measurement from helical gas ionization curvature, and PID via Time-of-Flight or RICH.
* **Difficulty**: Intermediate
* **Recommended Run Time**: 3–4 minutes
* **Key Takeaway**: Track curvature in magnetic fields relates to transverse momentum $p_T$ via $p_T = 0.3 \, B \, R$.Gas ionization loss $dE/dx$ separates particle species ($\pi, K, p$) at lower momentum.
* **Reference**: Sahoo Chapter 5.4; Beamer Slides 8–11.

---

## 📊 6. Transverse Spectra Builder
* **File**: [pt_spectrum_builder.html](pt_spectrum_builder.html)
* **Learning Objective**: Model thermal transverse momentum $p_T$ spectra and extract freeze-out temperatures using exponential fits.
* **Difficulty**: Beginner
* **Recommended Run Time**: 2–3 minutes
* **Key Takeaway**: Transverse mass $m_T = \sqrt{p_T^2 + m^2}$ spectra scale exponentially as $\frac{1}{2\pi p_T} \frac{dN}{dp_T} \propto \exp(-m_T/T)$, where the inverse slope parameter $T$ represents the thermal freeze-out temperature.
* **Reference**: Sahoo Chapter 5.4.1; Beamer Slide 25.
