import pandas as pd
import os

def extract_traffic_stats(root_dir, output_file_path):
    summary_list = []

    # Walk through all directories and subdirectories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == 'traffic_stats_by_road_type_daily.csv':
                file_path = os.path.join(subdir, file)

                try:
                    # Read the CSV file
                    data = pd.read_csv(file_path)

                    # Extract the first row ("all" road type)
                    first_row = data.iloc[0:1][['Road Type', 'Congestion Index', 'Avg. Speed [km/h]']]

                    # Get the parent folder name (grand-grandparent folder)
                    parent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(subdir)))

                    # Add the parent folder name to the data
                    first_row.insert(0, 'parent folder name', parent_folder_name)

                    # Append to the summary list
                    summary_list.append(first_row)

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Concatenate all extracted data
    summary_data = pd.concat(summary_list, ignore_index=True)

    # Save to a single Excel file
    summary_data.to_excel(output_file_path, index=False)

if __name__ == "__main__":
    # Specify the root directory and output file path
    root_directory = 'output'
    output_file = r'output\combined_traffic_stats.xlsx'

    # Run the extraction
    extract_traffic_stats(root_directory, output_file)
    print(f"Combined traffic stats saved to {output_file}")
