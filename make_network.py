import os
from snudda import SnuddaInit

network_path = os.path.join("networks", "simple_example")
os.makedirs(network_path, exist_ok=True)

# --- Snudda data directory ---
snudda_data = os.environ.get(
    "SNUDDA_DATA",
    os.path.join("..", "..", "snudda", "data")  # fallback if not set
)

# --- Neurons directory ---
neurons_dir = os.path.expandvars("$DATA/neurons")
if "$" in neurons_dir or neurons_dir == "/neurons":
    neurons_dir = os.path.join(snudda_data, "neurons")

si = SnuddaInit(network_path=network_path, random_seed=12345, snudda_data=snudda_data)

if "$" in neurons_dir or neurons_dir == "/neurons":
    neurons_dir = os.path.join("..", "..", "snudda", "data", "neurons")

si.define_striatum(
    num_dSPN=100, num_iSPN=100,
    num_FS=0, num_LTS=0, num_ChIN=0,
    neuron_density=80500,
    volume_type="cube",
    neurons_dir=neurons_dir
)

si.write_json()
print(f"Network written to {network_path}")
