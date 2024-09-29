#!/bin/bash
#
#SBATCH -J mriqc
#SBATCH --array=1
#SBATCH --time=24:00:00
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=4G
#SBATCH -p <partitions>

# Outputs ----------------------------------
#SBATCH -o log-ng/%A-%a.out
#SBATCH -e log-ng/%A-%a.err
#SBATCH --mail-user=<email>
#SBATCH --mail-type=ALL
# ------------------------------------------
module load system

unset PYTHONPATH
singularity run <.simg path> <data path> <output path> group

mriqc_exit=$?
echo MRIQC finished

