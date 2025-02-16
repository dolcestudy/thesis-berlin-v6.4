import pandas as pd
import os

def summarize_emissions_in_directory(root_dir, output_file_path):
    summary_list = []

    # Walk through all directories and subdirectories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(subdir, file)
                
                try:
                    data = pd.read_excel(file_path, sheet_name='Summary_By_Time')
                    sum_fc_mj = data['Sum_FC_MJ'].sum()
                    sum_co2e = data['Sum_CO2e'].sum()

                    summary_list.append({
                        'input_file_name': os.path.basename(file_path),
                        'Sum_FC_MJ': sum_fc_mj,
                        'Sum_CO2e': sum_co2e
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
    output_file = r'output\combined_emissions_summary.xlsx'

    # Run the summarization
    summarize_emissions_in_directory(root_directory, output_file)
    print(f"Combined summary saved to {output_file}")
