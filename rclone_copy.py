import os
import subprocess

# Paths to your generated network and log directory
network_path = '/cfs/klemming/home/z/zahrakh/snudda_plasticity/networks/simple_example'
log_path = '/cfs/klemming/home/z/zahrakh/snudda_plasticity/log'

# Destination on OneDrive (top-level)
onedrive_destination = 'kth_onedrive:Dokument/GitHub/data-plot/data/gabaPlasticity.data/simple_example'

def rclone_copy(src, dst):
    try:
        command = ['rclone', 'copy', src, dst, '--progress']
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f" Successfully copied {src} -> {dst}")
        else:
            print(f"Failed to copy {src}")
            print(result.stderr)
    except Exception as e:
        print("An error occurred:", e)

# Copy network folder
if os.path.exists(network_path):
    rclone_copy(network_path, f"{onedrive_destination}/networks/simple_example")
else:
    print(f"Path does not exist: {network_path}")

# Copy log folder
if os.path.exists(log_path):
    rclone_copy(log_path, f"{onedrive_destination}/log")
else:
    print(f"Path does not exist: {log_path}")
