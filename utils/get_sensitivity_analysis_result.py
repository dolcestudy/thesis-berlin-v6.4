import pandas as pd
import os
import re

def get_travel_duration(dir_name):


    file_path = dir_name + '/ph_modestats.csv'

    try:
        # Read the CSV file with ';' as separator
        df = pd.read_csv(file_path, delimiter=';')

        # Sum all the values in the first row excluding the 'Iteration' column
        total_travel_duration = df.iloc[-1, 1:].sum()

        return total_travel_duration
    
    except Exception as e:
        return None

def get_avgSpeed_congestionIndex(dir_name):

    file_path = dir_name + "/analysis/traffic/traffic_stats_by_road_type_daily.csv"

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        row = df[df["Road Type"] == "all"]

        # Extract the values
        congestion_index = row["Congestion Index"].values[0]
        avg_speed = row["Avg. Speed [km/h]"].values[0]

        return congestion_index, avg_speed


    except Exception as e:
        return None, None

def get_co2eq_fuelconsump(dir_name):

    file_path = get_first_excel_file(dir_name + "/emission-analysis")

    try:
        df = pd.read_excel(file_path, sheet_name='Summary_By_Time')
        sum_fc_mj = df['Sum_FC_MJ'].sum()
        sum_co2e = df['Sum_CO2e'].sum()

        return sum_co2e, sum_fc_mj
    
    except Exception as e:
        return None, None

def get_parameters(path):
    pattern = r"micro(\d+)pct-sp(\d+)-pce([\d\.]+)-iter\d+"
    match = re.search(pattern, path)
    
    if match:
        micro_pct = int(match.group(1))  # Extracts 60
        sp = int(match.group(2))  # Extracts 45
        pce = float(match.group(3))  # Extracts 0.5
        return micro_pct, sp, pce
    else:
        return None, None, None  # Return None if the pattern doesn't match

def get_first_excel_file(directory):
    for file in os.listdir(directory):
        if file.endswith((".xlsx", ".xls")):  # Check for Excel files
            return os.path.join(directory, file)
    return None  # Return None if no Excel file is found

if __name__ == "__main__":
    # Specify the root directory and output file path
    root_dir = 'output/3pct-0iteration/'
    output_file = 'output/sensitivity_analysis_results.xlsx'

    df = pd.DataFrame(columns=["number", "micro_pct", "speed", "pce", "total_travel_duration", "avg_speed", "congestion_index", "co2e", "fuel_consumption"])

    subdirs = [name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]

    for i, subdir in enumerate(subdirs, start=1):  # 'start=1' to make "number" start from 1
        
        print(f"Processing {subdir}")

        path = root_dir + subdir
        
        micro_pct, sp, pce = get_parameters(path)
        congestion_index, avg_speed = get_avgSpeed_congestionIndex(path)
        total_travel_dur = get_travel_duration(path)
        co2eq, fuel_consump = get_co2eq_fuelconsump(path)

        df.loc[len(df)] = [i, micro_pct, sp, pce, total_travel_dur, avg_speed, congestion_index, co2eq, fuel_consump]  # Append as a new row

    print(df)
    df.to_excel(output_file, index=False)
