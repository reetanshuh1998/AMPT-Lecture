#!/usr/bin/env python3
"""
ampt_parser.py — Core parser for AMPT ampt.dat output files.

Provides streaming, memory-efficient iteration over events.
Each event yields a header dict and a NumPy array of particles.
"""

import numpy as np
from collections import OrderedDict


# PDG particle names for common PIDs in AMPT
PID_NAMES = {
    211: "π+", -211: "π-", 111: "π0",
    321: "K+", -321: "K-", 311: "K0", -311: "K0bar",
    310: "K0_S", 130: "K0_L",
    2212: "p", -2212: "pbar",
    2112: "n", -2112: "nbar",
    3122: "Λ", -3122: "Λbar",
    3222: "Σ+", 3212: "Σ0", 3112: "Σ-",
    -3222: "Σbar-", -3212: "Σbar0", -3112: "Σbar+",
    3322: "Ξ0", 3312: "Ξ-",
    -3322: "Ξbar0", -3312: "Ξbar+",
    3334: "Ω-", -3334: "Ωbar+",
    22: "γ", 11: "e-", -11: "e+",
    13: "μ-", -13: "μ+",
    333: "φ", 113: "ρ0", 213: "ρ+", -213: "ρ-",
    223: "ω",
    411: "D+", -411: "D-", 421: "D0", -421: "D0bar",
    443: "J/ψ",
}

# Charged particles (|charge| > 0)
CHARGED_PIDS = {
    211, -211, 321, -321, 2212, -2212,
    3222, -3222, 3112, -3112, 3312, -3312,
    3334, -3334, 11, -11, 13, -13,
    213, -213, 411, -411,
}


def parse_event_header(line):
    """
    Parse an AMPT event header line into a dictionary.

    Format: event_id test_run nparticles impact_param
            Npart_proj Npart_targ N_el_proj N_inel_proj N_el_targ N_inel_targ phi_RP

    Returns:
        dict with keys: event_id, test_run, nparticles, b, Npart_proj, Npart_targ,
                        N_el_proj, N_inel_proj, N_el_targ, N_inel_targ, phi_RP
    """
    parts = line.split()
    return OrderedDict([
        ('event_id', int(parts[0])),
        ('test_run', int(parts[1])),
        ('nparticles', int(parts[2])),
        ('b', float(parts[3])),
        ('Npart_proj', int(parts[4])),
        ('Npart_targ', int(parts[5])),
        ('N_el_proj', int(parts[6])),
        ('N_inel_proj', int(parts[7])),
        ('N_el_targ', int(parts[8])),
        ('N_inel_targ', int(parts[9])),
        ('phi_RP', float(parts[10])),
    ])


def _safe_float(s):
    """Convert string to float, handling Fortran overflow ('********')."""
    try:
        return float(s)
    except ValueError:
        return float('nan')


def parse_particle_line(line):
    """
    Parse a single particle line.

    Format: PID px py pz mass x y z t

    Handles Fortran overflow values ('********') by converting to NaN.

    Returns:
        tuple: (pid, px, py, pz, mass, x, y, z, t)
    """
    parts = line.split()
    pid = int(parts[0])
    px, py, pz = _safe_float(parts[1]), _safe_float(parts[2]), _safe_float(parts[3])
    mass = _safe_float(parts[4])
    x, y, z, t = _safe_float(parts[5]), _safe_float(parts[6]), _safe_float(parts[7]), _safe_float(parts[8])
    return (pid, px, py, pz, mass, x, y, z, t)


def iter_events(filepath, max_events=None):
    """
    Generator that yields (header_dict, particles_array) for each event.

    Parameters:
        filepath: path to AMPT ampt.dat file
        max_events: if set, stop after this many events

    Yields:
        (header, particles) where:
            header: dict from parse_event_header
            particles: numpy structured array with fields:
                pid (int), px, py, pz, mass, x, y, z, t (float64)
    """
    dt = np.dtype([
        ('pid', np.int32),
        ('px', np.float64), ('py', np.float64), ('pz', np.float64),
        ('mass', np.float64),
        ('x', np.float64), ('y', np.float64), ('z', np.float64), ('t', np.float64),
    ])

    event_count = 0
    with open(filepath, 'r') as f:
        while True:
            if max_events is not None and event_count >= max_events:
                break

            header_line = f.readline()
            if not header_line:
                break

            header_line = header_line.strip()
            if not header_line:
                continue

            header = parse_event_header(header_line)
            nparticles = header['nparticles']

            # Read all particle lines for this event
            particles = np.empty(nparticles, dtype=dt)
            for i in range(nparticles):
                pline = f.readline()
                if not pline:
                    break
                data = parse_particle_line(pline)
                particles[i] = data

            event_count += 1
            yield header, particles


def load_all_events(filepath, max_events=None):
    """
    Load all events into lists. Returns (headers_list, particles_list).
    """
    headers = []
    all_particles = []
    for header, particles in iter_events(filepath, max_events):
        headers.append(header)
        all_particles.append(particles)
    return headers, all_particles


def get_pid_name(pid):
    """Return human-readable name for a PID."""
    return PID_NAMES.get(pid, f"PID={pid}")


def is_charged(pid):
    """Check if a PID corresponds to a charged particle."""
    return abs(pid) in CHARGED_PIDS or pid in CHARGED_PIDS


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ampt_parser.py <ampt.dat> [max_events]")
        sys.exit(1)

    fpath = sys.argv[1]
    maxev = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    print(f"Reading first {maxev} events from {fpath}...")
    for header, particles in iter_events(fpath, max_events=maxev):
        print(f"\nEvent {header['event_id']}: {header['nparticles']} particles, "
              f"b={header['b']:.2f} fm, Npart={header['Npart_proj']+header['Npart_targ']}")

        # Count by species
        unique, counts = np.unique(particles['pid'], return_counts=True)
        top5 = sorted(zip(counts, unique), reverse=True)[:5]
        for cnt, pid in top5:
            print(f"  {get_pid_name(pid):>8s}: {cnt:5d}")
