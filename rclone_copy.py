import os
import subprocess

# === SET THIS TO YOUR RCLONE CONFIG PASSWORD ===
RCLONE_PASSWORD = "BAGHnav12!@12"

# Paths to your generated network and log directory
network_path = '/cfs/klemming/home/z/zahrakh/snudda_plasticity/networks/simple_example'
log_path = '/cfs/klemming/home/z/zahrakh/snudda_plasticity/log'

# Destination on OneDrive (top-level)
onedrive_destination = 'kth_onedrive:Dokument/GitHub/data-plot/data/gabaPlasticity.data/simple_example'

def rclone_copy(src, dst):
    try:
        command = ['rclone', 'copy', src, dst, '--progress', '--create-empty-src-dirs']
        print(f"Running: {' '.join(command)}")
        # Inject the RCLONE_CONFIG_PASS environment variable
        env = os.environ.copy()
        env["RCLONE_CONFIG_PASS"] = RCLONE_PASSWORD
        result = subprocess.run(command, env=env)
        if result.returncode == 0:
            print(f"Successfully copied {src} -> {dst}")
        else:
            print(f"Failed to copy {src} (return code {result.returncode})")
    except Exception as e:
        print("An error occurred:", e)

print("Script started")

# Copy network folder
if os.path.exists(network_path):
    print("Copying network folder...")
    rclone_copy(network_path, onedrive_destination)
else:
    print(f"Path does not exist: {network_path}")

# Copy log folder
if os.path.exists(log_path):
    print("Copying log folder...")
    rclone_copy(log_path, onedrive_destination)
else:
    print(f"Path does not exist: {log_path}")

print("Script finished")
