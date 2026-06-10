#!/usr/bin/env python3
"""
make_subdata.py — Extract 100-event subsets from AMPT ampt.dat files.

Creates smaller data files for student hands-on exercises.
"""

import os
import sys

def extract_events(input_path, output_path, max_events=100):
    """
    Stream through an AMPT ampt.dat file and write out the first
    `max_events` events (header + all particle lines per event).
    """
    events_written = 0
    lines_written = 0

    with open(input_path, 'r') as fin, open(output_path, 'w') as fout:
        while events_written < max_events:
            # Read event header
            header_line = fin.readline()
            if not header_line:
                print(f"  [INFO] Reached end of file after {events_written} events.")
                break

            parts = header_line.split()
            # Event header has exactly 11 columns; anything else is corrupt/done
            if len(parts) != 11:
                print(f"  [WARN] Unexpected header line ({len(parts)} cols): {header_line.strip()}")
                break

            # Number of particles in this event is the 3rd column
            nparticles = int(parts[2])

            # Write header
            fout.write(header_line)
            lines_written += 1

            # Write all particle lines for this event
            for _ in range(nparticles):
                particle_line = fin.readline()
                if not particle_line:
                    print(f"  [WARN] Unexpected EOF in middle of event {events_written + 1}")
                    break
                fout.write(particle_line)
                lines_written += 1

            events_written += 1

    print(f"  Wrote {events_written} events ({lines_written} lines) → {output_path}")
    return events_written


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, "Data")
    subset_dir = os.path.join(data_dir, "subsets")

    os.makedirs(subset_dir, exist_ok=True)

    files = [
        ("ampt_7.7_default.dat", "ampt_7.7_sub100.dat"),
        ("ampt_39_default.dat", "ampt_39_sub100.dat"),
    ]

    for input_name, output_name in files:
        input_path = os.path.join(data_dir, input_name)
        output_path = os.path.join(subset_dir, output_name)

        if not os.path.exists(input_path):
            print(f"  [SKIP] {input_path} not found.")
            continue

        print(f"Processing {input_name}...")
        extract_events(input_path, output_path, max_events=100)

    print("\nDone! Subset files created in:", subset_dir)


if __name__ == "__main__":
    main()
