import pandas as pd

# Path to your Excel file
excel_file_path = "input/v6.3/emission-average/excel-data/EFA_HOT_Vehcat_hot_avr_WTT.XLSX"

# Path to save the CSV file
csv_file_path = "input/v6.3/emission-average/csv-data/hot_avr_2020_WTT.csv"

# Read the Excel file
df = pd.read_excel(excel_file_path)

# Save as CSV with ';' as the separator
df.to_csv(csv_file_path, index=False, sep=';')

print(f"Excel file has been successfully converted to CSV at {csv_file_path}")
