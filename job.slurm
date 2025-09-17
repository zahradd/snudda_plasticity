#!/bin/bash -l
#SBATCH --job-name=snudda_init
#SBATCH --partition=main
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH -A naiss2025-5-309
#SBATCH -o log/%x-%j.out
#SBATCH -e log/%x-%j.err

# --- Environment setup ---
module load snic-env
module load cray-python
source "$HOME/Snudda/snudda_plasticity/bin/activate"

# Optional: for your Python script's neurons_dir
export DATA="$HOME/Snudda"

unset DISPLAY
ulimit -s unlimited
mkdir -p log

# --- Run Python directly ---
python make_network.py
