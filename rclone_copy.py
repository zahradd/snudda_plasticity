import os
import subprocess

network_path = '/cfs/klemming/home/z/zahrakh/snudda_plasticity/networks/simple_example'
log_path = '/cfs/klemming/home/z/zahrakh/snudda_plasticity/log'
onedrive_destination = 'kth_onedrive:Dokument/GitHub/data-plot/data/gabaPlasticity.data/simple_example'

def rclone_copy(src, dst):
    try:
        command = ['rclone', 'copy', src, dst, '--progress']
        print("Running:", " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        print("returncode:", result.returncode)
        if result.returncode == 0:
            print(f"Successfully copied {src} -> {dst}")
        else:
            print(f"Failed to copy {src}")
    except Exception as e:
        print("An error occurred:", e)

if os.path.exists(network_path):
    rclone_copy(network_path, onedrive_destination)
else:
    print(f"Path does not exist: {network_path}")

if os.path.exists(log_path):
    rclone_copy(log_path, onedrive_destination)
else:
    print(f"Path does not exist: {log_path}")
