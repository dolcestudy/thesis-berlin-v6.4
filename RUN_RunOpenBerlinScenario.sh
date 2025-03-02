#!/bin/bash
#SBATCH -o ./logfile_%x_%j_%N.log
#SBATCH -J Inter_berlin_test
#SBATCH --get-user-env
#SBATCH --clusters=inter
#SBATCH --partition=cm4_inter
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=56
#SBATCH --export=NONE
#SBATCH --mail-type=end
#SBATCH --mail-user=i.aoyagi@tum.de
#SBATCH --time=7:59:59



whoami
id

date
hostname

# Load Conda environment
echo "Activating Conda environment..."
source /dss/dsshome1/05/ge83ham2/miniconda3/etc/profile.d/conda.sh
conda activate my_java_env

# Verify Java is available
echo "Using Conda-installed Java:"
which java || echo "Java not found!"
java -version || echo "Java command failed!"

# Start profiling
pidstat -dur -h 10 > profiling.log &

# Define classpath
classpath="/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/matsim-berlin-6.4-v6.0-363-g4b9ab48-dirty.jar"
# classpath="/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/matsim-berlin-6.4-v6.0-363-g4b9ab48.jar"

echo "***"
echo "Classpath: $classpath"
echo "***"

# Define Java command using the absolute path
java_command="$(which java) -Djava.awt.headless=true -Xmx488G -cp $classpath --add-opens java.base/java.lang=ALL-UNNAMED"

# Define main class
main="org.matsim.run.RunOpenBerlinScenario"

# Define arguments (if any)
arguments="--config /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/original-config-files/berlin-v6.4.config-original.xml"

# Construct full command
command="$java_command $main $arguments"
# command="$java_command $main"

echo ""
echo "Executing command: $command"
echo ""

# Run Java application
$command

# Stop profiling
pkill pidstat

# mvn exec:java \
#     -Dexec.mainClass="org.matsim.run.RunSensitivityAnalysis" \
#     -Dexec.jvmArgs="-Djava.awt.headless=true -Xmx488G --add-opens java.base/java.lang=ALL-UNNAMED"
