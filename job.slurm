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

# Activate virtual environment
source ~/venvs/snudda-plasticity/bin/activate

# Project directory
cd /cfs/klemming/home/z/zahrakh/snudda_plasticity
export DATA="$PWD"

# Safety tweaks
unset DISPLAY
ulimit -s unlimited
mkdir -p log

# --- Run Python job ---
python make_network.py
