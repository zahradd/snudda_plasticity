import os
import shutil
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
            return True
        else:
            print(f"❌ Failed to copy {src} (return code {result.returncode})")
            return False
    except Exception as e:
        print("⚠️ An error occurred:", e)
        return False

# === Helper to remove files or directories ===
def remove_path(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"🗑️ Removed file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"🗑️ Removed directory: {path}")
        else:
            print(f"⚠️ Path not found: {path}")
    except Exception as e:
        print(f"⚠️ Failed to remove {path}: {e}")


print("=== Script started ===")

# Step 1: Choose network
networks = sorted(os.listdir(network_dir))
print("\nAvailable networks:")
print("  0) Skip network copy")
for i, net in enumerate(networks, start=1):
    print(f"  {i}) {net}")

net_choice = int(input("Select a network by number: "))
network_name = None
if net_choice > 0:
    network_name = networks[net_choice - 1]
    network_path = os.path.join(network_dir, network_name)
else:
    print("⏭️ Skipping network copy")

# Step 2: Choose log
logs = [f.replace('.out', '').replace('.err', '') for f in os.listdir(log_dir)]
logs = sorted(set(logs))  # unique job names without extension

print("\nAvailable logs:")
print("  0) Skip log copy")
for i, log in enumerate(logs, start=1):
    print(f"  {i}) {log}")

log_choice = int(input("Select a log by number: "))
log_name = None
if log_choice > 0:
    log_name = logs[log_choice - 1]
    log_files = [
        os.path.join(log_dir, f"{log_name}.out"),
        os.path.join(log_dir, f"{log_name}.err")
    ]
else:
    log_files = []
    print("⏭️ Skipping log copy")

# Step 3: Define OneDrive destinations
onedrive_base = 'kth_onedrive:Dokument/GitHub/snudda_plasticity'
onedrive_network_dest = f'{onedrive_base}/networks/{network_name}' if network_name else None
onedrive_log_dest = f'{onedrive_network_dest}/log' if network_name else None

# Step 4: Copy network (optional)
if network_name:
    if os.path.exists(network_path):
        copy_network = input(f"Do you want to also copy the network '{network_name}'? (y/n): ")
        if copy_network.lower() == 'y':
            print("\nCopying selected network...")
            if rclone_copy(network_path, onedrive_network_dest):
                remove_network = input(f"Do you want to remove the local network '{network_name}' after copy? (y/n): ")
                if remove_network.lower() == 'y':
                    remove_path(network_path)
        else:
            print(f"⏭️ Skipped copying network '{network_name}', but will still use its folder for logs")
    else:
        print(f"⚠️ Network not found: {network_path}")


# Step 5: Copy logs
if log_files:
    if onedrive_log_dest:
        print(f"\nCopying log files for job '{log_name}'...")
        success = True
        for log_file in log_files:
            if os.path.exists(log_file):
                if not rclone_copy(log_file, onedrive_log_dest):
                    success = False
            else:
                print(f"⚠️ Log file not found: {log_file}")
                success = False

        # Ask once for the pair
        if success:
            remove = input(f"Do you want to remove local log files for '{log_name}' (.out & .err)? (y/n): ")
            if remove.lower() == 'y':
                for log_file in log_files:
                    remove_path(log_file)
    else:
        print("⚠️ Cannot copy logs without selecting a network destination")


print("\n=== Script finished ===")
