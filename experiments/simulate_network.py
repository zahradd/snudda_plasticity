# -*- coding: utf-8 -*-
"""
Simulate a striatum network previously built with build_striatum_network.py.

Steps:
1. Generate external inputs from input_config JSON
2. Run the simulation under MPI
"""

import os
import sys
import subprocess
import json
from snudda.input import SnuddaInput

# -------------------
# Parameters
# -------------------
duration = 0.5          # seconds of biological time
n_ranks = int(os.environ.get("SLURM_NTASKS", "6"))          # MPI ranks from SLURM
n_threads = int(os.environ.get("SLURM_CPUS_PER_TASK", "1")) # threads per rank
network_name = "first"   # keep the same

# -------------------
# Paths
# -------------------
PROJECT_ROOT = os.path.normpath(os.path.join(os.getcwd(), ".."))
network_path = os.path.join(PROJECT_ROOT, "networks", network_name)

input_config_file = os.path.join(PROJECT_ROOT, "input_config", "striatum-test-input.json")

print(f"Project root   : {PROJECT_ROOT}")
print(f"Network path   : {network_path}")
print(f"Input config   : {input_config_file}")
print(f"MPI ranks      : {n_ranks}")
print(f"Threads/rank   : {n_threads}")

# -------------------
# 1. Generate input
# -------------------
print("Generating input spikes...")

with open(input_config_file, "r") as f:
    config_data = json.load(f)

print("Input config content (parsed):")
for cell_type, inputs in config_data.items():
    for input_name, details in inputs.items():
        print(f"  {cell_type} -> {input_name}:")
        for k, v in details.items():
            print(f"    {k} : {v} (type={type(v)})")

try:
    si = SnuddaInput(
        network_path=network_path,
        input_config_file=input_config_file,
        verbose=False,
        rc=None
    )
    si.generate()
    print("Input spikes written to input-spikes.hdf5")
except Exception as e:
    import traceback
    print("\n[ERROR] SnuddaInput.generate() failed")
    traceback.print_exc()
    sys.exit(1)

# -------------------
# 2. Run the simulation
# -------------------
print(f"Running simulation for {duration} seconds on {n_ranks} ranks × {n_threads} threads...")

cmd = [
    "srun",
    "-n", str(n_ranks),
    "snudda",
    "simulate",
    network_path,
    "--time", str(duration)
]

ret = subprocess.call(cmd)
if ret != 0:
    sys.exit(f"Simulation failed with exit code {ret}")

print("Simulation complete. Results saved under:")
print(f"  {os.path.join(network_path, 'simulation')}")
