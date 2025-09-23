#!/bin/bash -l
#SBATCH --job-name=snudda_init
#SBATCH --partition=main
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH -A naiss2025-5-309
#SBATCH -o /cfs/klemming/home/z/zahrakh/snudda_plasticity/log/%x-%j.out
#SBATCH -e /cfs/klemming/home/z/zahrakh/snudda_plasticity/log/%x-%j.err
# --- Environment setup ---
module load snic-env
module load cray-python

# Activate virtual environment
source ~/venvs/snudda-plasticity/bin/activate

# Project directory (go into experiments folder where make_network.py lives)
cd /cfs/klemming/home/z/zahrakh/snudda_plasticity/experiments

export DATA="$PWD"
export SNUDDA_DATA=/cfs/klemming/home/z/zahrakh/snudda_plasticity/snudda/data

# Safety tweaks
unset DISPLAY
ulimit -s unlimited
export SNUDDA_NUMPROC=$SLURM_CPUS_PER_TASK

# --- Run Python job ---
python build_striatum_network.py
