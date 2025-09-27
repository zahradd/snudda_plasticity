#!/usr/bin/env python3
"""
Build a striatum network with only dSPN and iSPN neurons.
Step-by-step: Init -> Place -> Detect -> Prune
"""

import os
from snudda import SnuddaInit, SnuddaPlace, SnuddaDetect, SnuddaPrune

# -------------------
# Parameters
# -------------------
num_dSPN = 200
num_iSPN = 200
random_seed = 123
network_name = "first"   # keep the same

# -------------------
# Paths
# -------------------
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(HERE, ".."))       # snudda_plasticity/
network_path = os.path.join(PROJECT_ROOT, "networks", network_name)

# Prefer BasalGangliaData if available, else fallback to snudda/data
bg_data_path = os.path.normpath(os.path.join(PROJECT_ROOT, "..", "BasalGangliaData", "data"))
snudda_data = os.environ.get("SNUDDA_DATA", bg_data_path)

print(f"Using snudda_data = {snudda_data}")
print(f"Network will be saved at {network_path}")

# -------------------
# 1. Initialize network config
# -------------------
si = SnuddaInit(
    network_path=network_path,
    random_seed=random_seed,
    snudda_data=snudda_data
)

si.define_striatum(
    num_dSPN=num_dSPN,
    num_iSPN=num_iSPN,
    num_FS=0,
    num_LTS=0,
    num_ChIN=0,
    neuron_density=80500,
    volume_type="cube",
    neurons_dir=os.path.join(snudda_data, "neurons", "striatum")
)

si.write_json()
print("Step 1 complete: network-config.json written")

# -------------------
# 2. Place neurons
# -------------------
print("Placing neurons...")
sp = SnuddaPlace(network_path=network_path, rc=None)
sp.place()
print("Step 2 complete: neuron positions written")

# -------------------
# 3. Detect candidate synapses
# -------------------
print("Detecting synapses...")
sd = SnuddaDetect(network_path=network_path, rc=None)
sd.detect()
print("Step 3 complete: synapse candidates written")

# -------------------
# 4. Prune synapses
# -------------------
print("Pruning synapses...")
sp = SnuddaPrune(network_path=network_path, rc=None)
sp.prune()
print("Step 4 complete: pruned network saved")

print("✅ Network build finished successfully.")
print(f"Results saved in: {network_path}")
