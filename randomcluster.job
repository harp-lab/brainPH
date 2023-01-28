#!/bin/bash
#
#SBATCH --job-name=randomcluster_2
#SBATCH --output=randomcluster_2_job.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --partition=amd-hdr100
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=4069

# load your Anaconda module here and activate your virtual environment (if needed)
set -e
source /home/ashovon/venvs/brainph/bin/activate

python -u /home/ashovon/brainPH/cluster_calculation_random.py