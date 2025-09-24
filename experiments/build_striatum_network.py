"""
Build a striatum network with Snudda, using BasalGangliaData
but keeping a fixed number of neurons (struct_def).
"""

import os
from snudda import SnuddaInit, SnuddaPlace, SnuddaDetect, SnuddaPrune

# -------------------
# Parameters
# -------------------
number_of_neurons = 200   # <--- choose any number you want
random_seed = 123

# -------------------
# Paths
# -------------------
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(HERE, ".."))      # snudda_plasticity/
network_path = os.path.join(PROJECT_ROOT, "networks", "striatum_example")

# Point to BasalGangliaData repo (default two dirs up from snudda_plasticity)
bg_data_path = os.path.normpath(os.path.join(PROJECT_ROOT, "..", "BasalGangliaData", "data"))

# Use environment variable if defined, else fallback to bg_data_path
snudda_data = os.environ.get("SNUDDA_DATA", bg_data_path)

print(f"Using snudda_data = {snudda_data}")
print(f"Network will be saved at {network_path}")

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
