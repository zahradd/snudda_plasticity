#!/bin/bash -l
#SBATCH --job-name=snudda_init
#SBATCH --partition=main
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks=6
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
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

# -------------------------
# Compile NEURON mechanisms
# -------------------------
echo "Compiling NEURON mod files..."
cd /cfs/klemming/home/z/zahrakh/snudda_plasticity/snudda/data/neurons/mechanisms

rm -rf x86_64

export CXX=CC
export CC=cc
export FC=ftn
export MPICC=cc
export MPICXX=CC

which nrnivmodl
srun -n 1 nrnivmodl .

cd /cfs/klemming/home/z/zahrakh/snudda_plasticity/experiments
echo "Compilation complete."
# -------------------------

# --- Run Python job ---
python simulate_striatum_network.py
