#!/bin/bash
#SBATCH -o ./logfile_%x_%j_%N.log
#SBATCH -J Inter_berlin_test
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
conda activate my_java_env

# Verify Java installation
echo "Using Conda-installed Java:"
which java || echo "Java not found!"
java -version || echo "Java command failed!"

# Start profiling
echo "Starting performance profiling..."
pidstat -dur -h 10 > profiling.log &

# Navigate to project directory
cd /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/

# Run MATSim using Maven
echo "Executing MATSim via Maven..."
mvn clean compile exec:java \
    -Dexec.mainClass="org.matsim.run.RunSensitivityAnalysis" \
    -Dexec.jvmArgs="-Djava.awt.headless=true -Xmx60G --add-opens java.base/java.lang=ALL-UNNAMED"

# Stop profiling after execution
echo "Stopping profiling..."
pkill pidstat

echo "Simulation completed."
