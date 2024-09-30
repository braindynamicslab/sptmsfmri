#!/bin/bash
#
#SBATCH -J mriqc
#SBATCH --array=1-214
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

LINE_NUM=$( expr $SLURM_ARRAY_TASK_ID )
SUBJECT=$(awk "NR==$LINE_NUM" <sublist path>)

singularity run <.simg path> <data path> <output path> participant --participant-label ${SUBJECT} --n_procs 16 --ants-nthreads 8 -f --mem_gb 30 -vv -w <work path> --email <email>

mriqc_exit=$?
echo MRIQC finished

