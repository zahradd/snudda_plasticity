#!/bin/bash
# Force reset local repository to match the remote repository (origin)

# Exit immediately if a command fails
set -e

# Navigate to the Git repository directory
# (change this if your repo lives elsewhere)

# Load modules if needed (remove if not relevant)
# module load rclone

echo "Fetching latest changes from origin..."
git fetch origin

echo "Resetting local branch to origin/master..."
git reset --hard origin/master

echo "Repository is now in sync with GitHub (origin/master)."
