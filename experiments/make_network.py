import os
from snudda import SnuddaInit, Snudda
import json

# --- Anchor paths to this file's location (…/experiments) ---
try:
    HERE = os.path.dirname(os.path.abspath(__file__))  # works when running a .py
except NameError:
    HERE = os.getcwd()  # fallback for interactive runs

PROJECT_ROOT = os.path.normpath(os.path.join(HERE, ".."))  # go up one: …/
EXP_NAME = "simple_example"

# --- Write network under …/networks/simple_example ---
network_path = os.path.join(PROJECT_ROOT, "networks", EXP_NAME)
os.makedirs(network_path, exist_ok=True)

# --- Snudda data: use env if set, else …/snudda/data (next to networks/) ---
snudda_data = os.environ.get("SNUDDA_DATA", os.path.join(PROJECT_ROOT, "snudda", "data"))
neurons_dir = os.path.join(snudda_data, "neurons")

print("Resolved paths:")
print(f"  project_root: {PROJECT_ROOT}")
print(f"  network_path: {network_path}")
print(f"  snudda_data : {snudda_data}")
print(f"  neurons_dir : {neurons_dir}")

# --- Step 1: Initialize (writes network-config.json + mesh into ../networks/…) ---
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

# --- Patch network-config.json: replace $SNUDDA_DATA with absolute path ---
config_file = os.path.join(network_path, "network-config.json")
with open(config_file, "r") as f:
    cfg = json.load(f)

def replace_env(obj):
    if isinstance(obj, str) and "$SNUDDA_DATA" in obj:
        return obj.replace("$SNUDDA_DATA", snudda_data)
    if isinstance(obj, dict):
        return {k: replace_env(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [replace_env(v) for v in obj]
    return obj

cfg = replace_env(cfg)

with open(config_file, "w") as f:
    json.dump(cfg, f, indent=4)

print("Patched config to use absolute paths.")

# --- Step 2: Build the full network on Dardel (positions/synapses/pruned) ---
snd = Snudda(network_path=network_path)
snd.create_network()

print("Network created successfully!")
print("Copy these to your laptop for analysis: position.h5, synapses.h5, pruned.h5, network-synapses.hdf5, plus network-config.json.")
