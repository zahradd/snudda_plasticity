#!/usr/bin/env python3
"""
Build a striatum example network with Snudda.

Steps:
1. Initialize network definition
2. Place neurons
3. Detect candidate synapses
4. Prune connections
"""

import os
from snudda import SnuddaInit, SnuddaPlace, SnuddaDetect, SnuddaPrune

# -------------------
# Parameters
# -------------------
number_of_neurons = 200   # adjust size as needed
random_seed = 123
network_path = os.path.join("networks", "striatum_example")

# -------------------
# Snudda data: use env var if set, else fall back
# -------------------
snudda_data = os.environ.get(
    "SNUDDA_DATA",
    os.path.join(os.getcwd(), "snudda", "data")
)

print(f"Using snudda_data = {snudda_data}")

# -------------------
# 1. Initialize network
# -------------------
struct_def = {"Striatum": number_of_neurons}
print(f"Building striatum network with {number_of_neurons} neurons...")

si = SnuddaInit(
    network_path=network_path,
    struct_def=struct_def,
    random_seed=random_seed,
    snudda_data=snudda_data
)

# -------------------
# 2. Place neurons
# -------------------
print("Placing neurons...")
sp = SnuddaPlace(network_path=network_path, rc=None)
sp.place()

# -------------------
# 3. Detect synapses
# -------------------
print("Detecting candidate synapses...")
sd = SnuddaDetect(network_path=network_path, rc=None)
sd.detect()

# -------------------
# 4. Prune network
# -------------------
print("Pruning synapses...")
sp = SnuddaPrune(network_path=network_path, rc=None)
sp.prune()

print("Network build complete. Files saved in:", network_path)

