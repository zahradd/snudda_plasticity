import os
import subprocess

# === SET THIS TO YOUR RCLONE CONFIG PASSWORD ===
RCLONE_PASSWORD = "BAGHnav12!@12"

# Ask user for network and log names
network_name = input("Enter the network name: ").strip()
log_name = input("Enter the log name (without .out/.err): ").strip()

# Build paths
network_path = f'/cfs/klemming/home/z/zahrakh/snudda_plasticity/networks/{network_name}'
log_dir = '/cfs/klemming/home/z/zahrakh/snudda_plasticity/log'
# Exact log files to copy
log_files = [
    os.path.join(log_dir, f"{log_name}.out"),
    os.path.join(log_dir, f"{log_name}.err")
]

# Destination paths on OneDrive
onedrive_network_dest = f'kth_onedrive:Dokument/GitHub/snudda_plasticity/networks/{network_name}'
onedrive_log_dest = f'{onedrive_network_dest}/log'

def rclone_copy(src, dst):
    try:
        command = ['rclone', 'copy', src, dst, '--progress', '--create-empty-src-dirs']
        print(f"Running: {' '.join(command)}")
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

# Copy the network folder
if os.path.exists(network_path):
    print("Copying network folder...")
    rclone_copy(network_path, onedrive_network_dest)
else:
    print(f"Path does not exist: {network_path}")

# Copy the specific log files
for log_file in log_files:
    if os.path.exists(log_file):
        print(f"Copying log file {log_file}...")
        rclone_copy(log_file, onedrive_log_dest)
    else:
        print(f"Log file not found: {log_file}")

print("Script finished")
