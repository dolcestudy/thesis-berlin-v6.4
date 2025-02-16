import pandas as pd
import os

def sum_travel_durations(root_dir, output_file_path):
    summary_list = []

    # Walk through all directories and subdirectories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == 'ph_modestats.csv':
                file_path = os.path.join(subdir, file)

                try:
                    # Read the CSV file with ';' as separator
                    data = pd.read_csv(file_path, delimiter=';')

                    # Sum all the values in the first row excluding the 'Iteration' column
                    total_sum = data.iloc[0, 1:].sum()

                    # Get the parent folder name (immediate parent folder)
                    parent_folder_name = os.path.basename(subdir)

                    # Append to the summary list
                    summary_list.append({
                        'parent folder name': parent_folder_name,
                        'sum of travel duration': total_sum
                    })

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Convert the list of summaries to a DataFrame
    summary_data = pd.DataFrame(summary_list)

    # Save the combined summary to a single Excel file
    summary_data.to_excel(output_file_path, index=False)

if __name__ == "__main__":
    # Specify the root directory and output file path
    root_directory = 'output'
    output_file = r'output\combined_travel_durations.xlsx'

    # Run the summarization
    sum_travel_durations(root_directory, output_file)
    print(f"Combined travel durations saved to {output_file}")
