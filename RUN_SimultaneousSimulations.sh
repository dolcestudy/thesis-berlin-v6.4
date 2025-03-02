#!/bin/bash
#SBATCH -o ./sh-log/logfile_%x_%j_%N.log
#SBATCH -J sim_simulation
#SBATCH --get-user-env
#SBATCH --clusters=inter
#SBATCH --partition=cm4_inter
#SBATCH --ntasks=8
#SBATCH --nodes=1
#SBATCH --cpus-per-task=25
#SBATCH --export=none
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


# Maven 実行オプション
main_class="org.matsim.run.RunDynamicAnalysis"
jvm_args="-Djava.awt.headless=true -Xmx60G --add-opens java.base/java.lang=ALL-UNNAMED"

iter_num=1
speeds=(50 70 90 120)
pces=(0.5 0.6 0.7)
plans=(berlin-v6.4-3pct-plans-micro20pct.xml.gz berlin-v6.4-3pct-plans-micro40pct.xml.gz berlin-v6.4-3pct-plans-micro60pct.xml.gz berlin-v6.4-3pct-plans-micro80pct.xml.gz berlin-v6.4-3pct-plans-micro100pct.xml.gz)

index=0
# ネストしたループで全組み合わせを作成
for speed in "${speeds[@]}"; do
    for pce in "${pces[@]}"; do
        for plan in "${plans[@]}"; do
            declare "arg_$index=$speed $pce $plan"
            index=$((index + 1))
        done
    done
done

# 変数の確認
echo "arg_0 = $arg_0"
echo "arg_1 = $arg_1"
echo "arg_2 = $arg_2"


# # Maven コマンドを変数に格納
# java_command="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$exec_args\""


# # コマンドを表示（デバッグ用）
# echo "Executing: $java_command"

# # 実行
# eval $java_command


# # commands
java_command_0="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_0\""
java_command_1="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_1\""
java_command_2="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_2\""
java_command_3="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_3\""
java_command_4="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_4\""
java_command_5="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_5\""
java_command_6="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_6\""
java_command_7="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_7\""
java_command_8="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_8\""
java_command_9="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_9\""
java_command_10="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_10\""
java_command_11="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_11\""
java_command_12="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_12\""
java_command_13="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_13\""
java_command_14="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_14\""
java_command_15="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_15\""
java_command_16="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_16\""
java_command_17="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_17\""
java_command_18="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_18\""
java_command_19="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_19\""
java_command_20="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_20\""
java_command_21="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_21\""
java_command_22="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_22\""
java_command_23="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_23\""
java_command_24="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_24\""
java_command_25="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_25\""
java_command_26="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_26\""
java_command_27="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_27\""
java_command_28="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_28\""
java_command_29="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_29\""
java_command_30="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_30\""
java_command_31="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_31\""
java_command_32="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_32\""
java_command_33="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_33\""
java_command_34="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_34\""
java_command_35="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_35\""
java_command_36="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_36\""
java_command_37="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_37\""
java_command_38="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_38\""
java_command_39="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_39\""
java_command_40="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_40\""
java_command_41="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_41\""
java_command_42="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_42\""
java_command_43="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_43\""
java_command_44="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_44\""
java_command_45="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_45\""
java_command_46="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_46\""
java_command_47="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_47\""
java_command_48="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_48\""
java_command_49="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_49\""
java_command_50="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_50\""
java_command_51="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_51\""
java_command_52="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_52\""
java_command_53="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_53\""
java_command_54="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_54\""
java_command_55="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_55\""
java_command_56="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_56\""
java_command_57="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_57\""
java_command_58="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_58\""
java_command_59="mvn clean compile exec:java -Dexec.mainClass=\"$main_class\" -Dexec.jvmArgs=\"$jvm_args\" -Dexec.args=\"$iter_num $arg_59\""

# Run the commands
# (
#   eval $java_command_0 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_0.log 2>&1
# ) &

# (
#   eval $java_command_1 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_1.log 2>&1
# ) 




# # Run the commands
(
  eval $java_command_0 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_0.log 2>&1 && \
  eval $java_command_1 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_1.log 2>&1 && \
  eval $java_command_2 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_2.log 2>&1 && \
  eval $java_command_3 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_3.log 2>&1 && \
  eval $java_command_4 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_4.log 2>&1 && \
  eval $java_command_5 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_5.log 2>&1 && \
  eval $java_command_6 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_6.log 2>&1 && \
  eval $java_command_7 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_7.log 2>&1
) &

(
  eval $java_command_8 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_8.log 2>&1 && \
  eval $java_command_9 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_9.log 2>&1 && \
  eval $java_command_10 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_10.log 2>&1 && \
  eval $java_command_11 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_11.log 2>&1 && \
  eval $java_command_12 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_12.log 2>&1 && \
  eval $java_command_13 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_13.log 2>&1 && \
  eval $java_command_14 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_14.log 2>&1 && \
  eval $java_command_15 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_15.log 2>&1
) &

(
  eval $java_command_16 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_16.log 2>&1 && \
  eval $java_command_17 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_17.log 2>&1 && \
  eval $java_command_18 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_18.log 2>&1 && \
  eval $java_command_19 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_19.log 2>&1 && \
  eval $java_command_20 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_20.log 2>&1 && \
  eval $java_command_21 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_21.log 2>&1 && \
  eval $java_command_22 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_22.log 2>&1 && \
  eval $java_command_23 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_23.log 2>&1
) &

(
  eval $java_command_24 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_24.log 2>&1 && \
  eval $java_command_25 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_25.log 2>&1 && \
  eval $java_command_26 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_26.log 2>&1 && \
  eval $java_command_27 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_27.log 2>&1 && \
  eval $java_command_28 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_28.log 2>&1 && \
  eval $java_command_29 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_29.log 2>&1 && \
  eval $java_command_30 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_30.log 2>&1 && \
  eval $java_command_31 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_31.log 2>&1
) &

(
  eval $java_command_32 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_32.log 2>&1 && \
  eval $java_command_33 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_33.log 2>&1 && \
  eval $java_command_34 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_34.log 2>&1 && \
  eval $java_command_35 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_35.log 2>&1 && \
  eval $java_command_36 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_36.log 2>&1 && \
  eval $java_command_37 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_37.log 2>&1 && \
  eval $java_command_38 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_38.log 2>&1 && \
  eval $java_command_39 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_39.log 2>&1
) &

(
  eval $java_command_40 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_40.log 2>&1 && \
  eval $java_command_41 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_41.log 2>&1 && \
  eval $java_command_42 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_42.log 2>&1 && \
  eval $java_command_43 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_43.log 2>&1 && \
  eval $java_command_44 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_44.log 2>&1 && \
  eval $java_command_45 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_45.log 2>&1 && \
  eval $java_command_46 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_46.log 2>&1 && \
  eval $java_command_47 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_47.log 2>&1
) &

(
  eval $java_command_48 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_48.log 2>&1 && \
  eval $java_command_49 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_49.log 2>&1 && \
  eval $java_command_50 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_50.log 2>&1 && \
  eval $java_command_51 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_51.log 2>&1 && \
  eval $java_command_52 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_52.log 2>&1 && \
  eval $java_command_53 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_53.log 2>&1 && \
  eval $java_command_54 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_54.log 2>&1 && \
  eval $java_command_55 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_55.log 2>&1
) &

(
  eval $java_command_56 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_56.log 2>&1 && \
  eval $java_command_57 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_57.log 2>&1 && \
  eval $java_command_58 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_58.log 2>&1 && \
  eval $java_command_59 > /dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/simulation_log/logfile_java_command_59.log 2>&1
) 

# Stop profiling after execution
echo "Stopping profiling..."
pkill pidstat

# Wait for all commands to complete
wait

echo "All commands have completed."
date
