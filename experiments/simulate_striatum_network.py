# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 13:47:07 2025

@author: zahra.khodadadi
"""

#!/usr/bin/env python3
"""
Simulate a striatum network previously built with build_striatum_network.py.

Steps:
1. Generate external inputs from input_config JSON
2. Run the simulation under MPI
"""

import os
import sys
import subprocess
from snudda.input import SnuddaInput

# -------------------
# Parameters
# -------------------
duration = 3.5         # seconds of biological time
n_cores = 6            # MPI ranks to use
exp_name = "striatum_example"

# Paths
PROJECT_ROOT = os.path.normpath(os.path.join(os.getcwd(), ".."))
network_path = os.path.join(PROJECT_ROOT, "networks", exp_name)

input_config_file = os.path.join(PROJECT_ROOT, "input_config", "striatum-test-input.json")

print(f"Project root   : {PROJECT_ROOT}")
print(f"Network path   : {network_path}")
print(f"Input config   : {input_config_file}")

# -------------------
# 1. Generate input
# -------------------
# print("Generating input spikes...")
# si = SnuddaInput(
#     network_path=network_path,
#     input_config_file=input_config_file,
#     verbose=False,
#     rc=None
# )
# si.generate()
# print("Input spikes written to input-spikes.hdf5")
# -------------------
# 1. Generate input
# -------------------
print("Generating input spikes...")

# --- Debug: read and print your JSON before passing it to Snudda
import json
with open(input_config_file, "r") as f:
    config_data = json.load(f)

print("Input config content (parsed):")
for cell_type, inputs in config_data.items():
    for input_name, details in inputs.items():
        print(f"  {cell_type} -> {input_name}:")
        for k, v in details.items():
            print(f"    {k} : {v} (type={type(v)})")

# --- Now call SnuddaInput, but catch errors
from snudda.input import SnuddaInput
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
print(f"Running simulation for {duration} seconds on {n_cores} cores...")

cmd = [
    "mpiexec",
    "-n", str(n_cores),
    "snudda",
    "simulate",
    network_path,
    "--time", str(duration)
]

# Use subprocess to capture errors nicely in Slurm logs
ret = subprocess.call(cmd)
if ret != 0:
    sys.exit(f"Simulation failed with exit code {ret}")

print("Simulation complete. Results saved under:")
print(f"  {os.path.join(network_path, 'simulation')}")
