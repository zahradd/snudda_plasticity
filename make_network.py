import os
import subprocess

# === SET THIS TO YOUR RCLONE CONFIG PASSWORD ===
RCLONE_PASSWORD = "BAGHnav12!@12"

base_path = '/cfs/klemming/home/z/zahrakh/snudda_plasticity'
network_dir = os.path.join(base_path, 'networks')
log_dir = os.path.join(base_path, 'log')

# === Helper to run rclone ===
def rclone_copy(src, dst):
    try:
        command = ['rclone', 'copy', src, dst, '--progress', '--create-empty-src-dirs']
        print(f"Running: {' '.join(command)}")
        env = os.environ.copy()
        env["RCLONE_CONFIG_PASS"] = RCLONE_PASSWORD
        result = subprocess.run(command, env=env)
        if result.returncode == 0:
            print(f"✅ Successfully copied {src} -> {dst}")
        else:
            print(f"❌ Failed to copy {src} (return code {result.returncode})")
    except Exception as e:
        print("⚠️ An error occurred:", e)


print("=== Script started ===")

# Step 1: Choose network
networks = sorted(os.listdir(network_dir))
print("\nAvailable networks:")
for i, net in enumerate(networks, start=1):
    print(f"  {i}) {net}")

net_choice = int(input("Select a network by number: ")) - 1
network_name = networks[net_choice]
network_path = os.path.join(network_dir, network_name)

# Step 2: Choose log
logs = [f.replace('.out', '').replace('.err', '') for f in os.listdir(log_dir)]
logs = sorted(set(logs))  # unique job names without extension

print("\nAvailable logs:")
for i, log in enumerate(logs, start=1):
    print(f"  {i}) {log}")

log_choice = int(input("Select a log by number: ")) - 1
log_name = logs[log_choice]

# Build full log file paths
log_files = [
    os.path.join(log_dir, f"{log_name}.out"),
    os.path.join(log_dir, f"{log_name}.err")
]

# Step 3: Define OneDrive destinations
onedrive_network_dest = f'kth_onedrive:Dokument/GitHub/snudda_plasticity/networks/{network_name}'
onedrive_log_dest = f'{onedrive_network_dest}/log'

# Step 4: Copy network
if os.path.exists(network_path):
    print("\nCopying selected network...")
    rclone_copy(network_path, onedrive_network_dest)
else:
    print(f"⚠️ Network not found: {network_path}")

# Step 5: Copy selected logs
for log_file in log_files:
    if os.path.exists(log_file):
        print(f"\nCopying log file {log_file}...")
        rclone_copy(log_file, onedrive_log_dest)
    else:
        print(f"⚠️ Log file not found: {log_file}")

print("\n=== Script finished ===")
