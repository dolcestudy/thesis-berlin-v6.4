import pandas as pd

# Read the CSV file
df = pd.read_csv(r"output\micro000pct-sp60-pce0.5-DMC-2.5-MDR-0.24-iter0\berlin-v6.4.output_trips.csv", sep=";",low_memory=False)  # Replace "your_file.csv" with the actual file name

# Group by person and mode, summing the distance
df_result = df.groupby(["person", "main_mode"], as_index=False)["traveled_distance"].sum()

# Save the result to a new CSV file
df_result.to_csv(r"output\micro000pct-sp60-pce0.5-DMC-2.5-MDR-0.24-iter0\ditance_by_person_mode_from_trips.csv", index=False)

# Print the result
print(df_result)
