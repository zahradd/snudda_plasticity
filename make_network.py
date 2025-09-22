import os
from snudda import SnuddaInit, Snudda

# --- Paths ---
network_path = os.path.join("networks", "simple_example")
os.makedirs(network_path, exist_ok=True)

# Snudda data dir: use environment variable if available, otherwise fallback
snudda_data = os.environ.get(
    "SNUDDA_DATA",
    os.path.join("..", "..", "snudda", "data")
)

# Neurons directory
neurons_dir = os.path.join(snudda_data, "neurons")

# --- Step 1: Initialize network ---
si = SnuddaInit(
    network_path=network_path,
    random_seed=12345,
    snudda_data=snudda_data
)

si.define_striatum(
    num_dSPN=100, num_iSPN=100,
    num_FS=0, num_LTS=0, num_ChIN=0,
    neuron_density=80500,
    volume_type="cube",
    neurons_dir=neurons_dir
)

si.write_json()
print(f"Network config written to {network_path}")

# --- Step 2: Build the full network (heavy step, run on Dardel) ---
snd = Snudda(network_path=network_path)
snd.create_network()

print("Network created successfully!")
print("Now copy the .h5 files (position.h5, synapses.h5, pruned.h5) and config to your laptop for plotting.")
