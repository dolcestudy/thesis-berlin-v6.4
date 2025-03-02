import pandas as pd
import gzip
import json
import xml.etree.ElementTree as ET
import csv
import os
import urllib.request
import get_plans_with_microcar

def get_all_persons_by_income(person_file):

    with gzip.open(person_file, "rt", encoding="utf-8") as f:
        df = pd.read_csv(f, sep=";")

    # Convert 'income' to numeric, setting errors='coerce' to convert non-numeric (empty) values to NaN
    df["income"] = pd.to_numeric(df["income"], errors="coerce")

    # Sort by income (ascending), keeping NaN values at the end
    df_sorted = df.sort_values(by="income", ascending=True, na_position="last")

    # Extract only the 'person' column
    sorted_person_list = df_sorted["person"].tolist()

    return sorted_person_list

def get_persons_with_cars_from_legs(legs_file):

    with gzip.open(legs_file, "rt", encoding="utf-8") as f:
        # Read the CSV file
        df = pd.read_csv(f, sep=";")

    # Filter for rows where the mode is 'car'
    persons_with_car = df[df["mode"] == "car"]["person"].unique().tolist()

    return persons_with_car

def get_persons_with_cars_from_plans(plan_file):
    car_user_list = set()  # Use a set to store unique person IDs

    # Open the compressed XML file
    with gzip.open(plan_file, 'rt', encoding='utf-8') as f:
        context = ET.iterparse(f, events=("start", "end"))
        person_id = None
        inside_plan = False

        for event, elem in context:
            if event == "start":
                if elem.tag == "person":
                    person_id = elem.get("id")  # Store the person's ID
                elif elem.tag == "plan":
                    inside_plan = True  # Track when inside a <plan> element
                elif inside_plan and elem.tag == "leg" and elem.get("mode") == "car":
                # elif inside_plan and elem.tag == "activity" and elem.get("type") == "car interaction":
                    if person_id:
                        car_user_list.add(person_id)  # Add to unique set

            elif event == "end":
                if elem.tag == "person":
                    person_id = None  # Reset when leaving a person
                elif elem.tag == "plan":
                    inside_plan = False  # Reset when leaving a plan
                elem.clear()  # Free memory (important for large files)

    return car_user_list

def get_persons_with_special_vehicle_type(plan_file, vehicle_type):
    car_user_list = set()  # Store unique person IDs

    with gzip.open(plan_file, 'rt', encoding='utf-8') as f:
        context = ET.iterparse(f, events=("start", "end"))
        person_id = None

        for event, elem in context:
            if event == "start":
                if elem.tag == "person":
                    person_id = elem.get("id")  # Store the person's ID


            elif event == "end":
                if elem.tag == "attribute" and elem.get("name") == "vehicleTypes":
                    if elem.text and elem.text.strip():  # ✅ Ensure text is available
                        try:
                            vehicle_dict = json.loads(elem.text.strip())  # ✅ JSON parsing
                            if vehicle_type in vehicle_dict.values():
                                car_user_list.add(person_id)
                        except json.JSONDecodeError:
                            print(f"JSON Error for {person_id}: {elem.text.strip()}")
                    else:
                        print(f"Warning: Empty vehicleTypes attribute for person {person_id}")


                elif elem.tag == "person":
                    person_id = None  # ✅ Reset when leaving <person>

                elem.clear()  # ✅ Free memory

    return car_user_list

def get_persons_household_1_2_empty(person_file):

    with gzip.open(person_file, "rt", encoding="utf-8") as f:
        # Read the CSV file
        df = pd.read_csv(f, sep=";", dtype=str, low_memory=False)

    # Convert household_size to numeric
    df["household_size"] = pd.to_numeric(df["household_size"], errors="coerce")

    # Filter where household_size is 1, 2, or NaN (missing)
    filtered_df = df[df["household_size"].isin([1, 2]) | df["household_size"].isna()]

    # Extract only the 'person' column
    person_list = filtered_df["person"].tolist()

    return person_list

def get_persons_car_travel_less_90km(legs_file):

    with gzip.open(legs_file, "rt", encoding="utf-8") as f:
        # Read the CSV file with proper data types
        df = pd.read_csv(f, sep=";", dtype=str, low_memory=False)

    # Convert "distance" column to numeric type
    df["distance"] = pd.to_numeric(df["distance"], errors="coerce")

    # Group by "person" and "mode", then sum the distances
    df_grouped = df.groupby(["person", "mode"], as_index=False)["distance"].sum()

    # Filter for car mode and distance < 200,000 (if "car" exists in your dataset)
    df_filtered = df_grouped[(df_grouped["mode"] == "car") & (df_grouped["distance"] < 90000)]

    # Get the list of persons matching the filter
    person_list = df_filtered["person"].tolist()

    return person_list


if __name__ == '__main__':
    # Input files
    legs_file = "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/output/3pct-micro000pct-sp50-pce0.5-iter0/output_legs.csv.gz"
    persons_file = "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/output/3pct-micro000pct-sp50-pce0.5-iter0/output_persons.csv.gz"
    # plans_file_url = "https://svn.vsp.tu-berlin.de/repos/public-svn/matsim/scenarios/countries/de/berlin/berlin-v6.4/input/berlin-v6.4-3pct.plans.xml.gz"
    plans_file = "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/berlin-v6.4-3pct-plans-micro00pct-original.xml.gz"
    # print("read plans file")
    # urllib.request.urlretrieve(plans_file_url, plans_file)

    print("Step 1: List all agents by income")
    persons_by_income = get_all_persons_by_income(persons_file)
    print(f"All agents: {len(persons_by_income)}")

    print("Step 2: List agents using cars")
    car_user_list = set(get_persons_with_cars_from_legs(legs_file))
    print(f"Agents using cars: {len(car_user_list)}")

    print("Step 3: List agents using mercedes313 and vwCaddy")
    mercedes_list = set(get_persons_with_special_vehicle_type(plans_file, "mercedes313"))
    vwcaddy_list = set(get_persons_with_special_vehicle_type(plans_file, "vwCaddy"))
    print(f"Agents using mercedes313: {len(mercedes_list)}")
    print(f"Agents using vwCaddy: {len(vwcaddy_list)}")

    print("Step 4: List agents traveling less than 90km with cars")
    cartravel_less_200km_list = set(get_persons_car_travel_less_90km(legs_file))
    print(f"Agents with cars traveling less than 90km: {len(cartravel_less_200km_list)}")

    print("Step 5: List agents whose household size is either 1, 2, or none")
    persons_household_1_2_nan_list = set(get_persons_household_1_2_empty(persons_file))
    print(f"Agents with household either 1, 2, and none: {len(persons_household_1_2_nan_list)}")

    print("Step 6: Filter agents by algorithms")
    agents_filtered = [x for x in persons_by_income 
                        if x in car_user_list
                        and x not in mercedes_list 
                        and x not in vwcaddy_list 
                        and x in cartravel_less_200km_list
                        and x in persons_household_1_2_nan_list]
    print(f"Agents identified having the potential to switch to microcars: {len(agents_filtered)}")

    print("Step 7: Write csv file")
    with open("/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/3pct_potential_agents.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        # writer.writerow(["person"])  # Header row (optional)
        for item in agents_filtered:
            writer.writerow([item])  # Write each item as a row

    print("CSV file saved successfully!")

    # make plan files
    original_plan_file = "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/berlin-v6.4-3pct-plans-micro00pct-original.xml.gz"
    potential_person_csv = "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/3pct_potential_agents.csv"
    df = pd.read_csv(potential_person_csv, header=None)
    agents_list = df[0].tolist()
    # print(potential_agents[1:10])
    
    output_file = [
        "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/berlin-v6.4-3pct-plans-micro00pct.xml.gz",
        "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/berlin-v6.4-3pct-plans-micro25pct.xml.gz",
        "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/berlin-v6.4-3pct-plans-micro50pct.xml.gz",
        "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/berlin-v6.4-3pct-plans-micro75pct.xml.gz",
        "/dss/dsshome1/05/ge83ham2/thesis-berlin-v6.4/input/v6.4/berlin-v6.4-3pct-plans-micro100pct.xml.gz"]
    modified_car_pct = [0,25,50,75,100]


    for i in range(5):
        get_plans_with_microcar.create_plan_file(original_plan_file, output_file[i], agents_list, modified_car_pct[i])