#!/bin/bash
#SBATCH -o ./logfile_%x_%j_%N.log
#SBATCH -J run_python_util_file
#SBATCH --get-user-env
#SBATCH --clusters=inter
#SBATCH --partition=cm4_inter
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=112
#SBATCH --export=NONE
#SBATCH --mail-type=end
#SBATCH --mail-user=i.aoyagi@tum.de
#SBATCH --time=7:59:59

# Environment setup
whoami
id
date
hostname

# Load Conda environment
echo "Activating Conda environment..."
source /dss/dsshome1/05/ge83ham2/miniconda3/etc/profile.d/conda.sh
conda activate my_java_env  # Change this to the correct Python environment

# Verify Python installation
echo "Using Conda-installed Python:"
which python || echo "Python not found!"
python --version || echo "Python command failed!"

# Start profiling
echo "Starting performance profiling..."
pidstat -dur -h 10 > profiling.log &

# Navigate to project directory
cd /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/

# Run Python script
echo "Executing Python script..."
python /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/utils/get_microcar_potential_agents.py

# Stop profiling after execution
echo "Stopping profiling..."
pkill pidstat

echo "Script execution completed."
