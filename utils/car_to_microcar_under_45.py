import xml.etree.ElementTree as ET
import pandas as pd
import gzip
import math

import car_to_microcar_xpct as utils 

# Function to convert time in h:mm:ss format to seconds
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def get_car_ids_under_45kmh(trips_csv_gz_file) -> list:

    trips_csv_gz_file = r'C:\berlin\output\micro000-iter0\output_trips.csv.gz'

    # Load the CSV file
    with gzip.open(trips_csv_gz_file, 'rt') as f:
        df = pd.read_csv(f, sep=';', dtype={'start_facility_id': str, 'end_facility_id': str})

    # Filter by main_mode = "car"
    car_trips = df[df['main_mode'] == 'car'].copy()

    # Convert 'trav_time' to seconds
    car_trips['trav_time_seconds'] = car_trips['trav_time'].apply(time_to_seconds)

    # Calculate speed (in km/h) for each trip
    car_trips['speed_kmh'] = (car_trips['traveled_distance'] / car_trips['trav_time_seconds']) * 3.6

    # Group by 'person' and calculate the maximum average speed
    max_ave_speeds = car_trips.groupby('person')['speed_kmh'].max()

    # Filter persons with a maximum average speed under 45 km/h
    slow_persons = max_ave_speeds[max_ave_speeds < 45].index.tolist()
    slow_cars = [person + "_car" for person in slow_persons]

    return slow_cars

if __name__ == "__main__":

    trips_csv_gz_file = r"C:\berlin\output\micro000-iter0\output_trips.csv.gz"
    input_plan_file = r"input\v6.3\berlin-v6.3-10pct-plans-micro00pct.xml"
    vehicle_id_file = r"utils\allVehicles_list.xml"
    output_plan_file = r"input\v6.3\berlin-v6.3-10pct-plans-micro-under45kmh.xml.gz"


    # Parse the XML files
    tree = ET.parse(input_plan_file)
    root = tree.getroot()

    # Generate a list of cars to be modifed to microcar
    changed_car_list = get_car_ids_under_45kmh(trips_csv_gz_file)
    print(len(changed_car_list))


    # Iterate through all <person> elements and modify them
    for person in root.findall(".//person"):

        # Modify vehicle type from "car" to "freight" for specific cars
        for attr in person.findall(".//attribute[@name='vehicleTypes'][@class='org.matsim.vehicles.PersonVehicleTypes']"):
            if attr.text and any(x in attr.text for x in ["mercedes313", "vwCaddy"]) and "car" in attr.text:
                print(attr.text)
                attr.text = attr.text.replace('"car"', '"freight"')
                utils.car_to_x_in_plan(person, "freight")
                break

        # Modify vehicle type from "car" to "microcar" for selected cars
        for attribute in person.findall(".//attribute[@name='vehicles']"):
            vehicles_text = attribute.text
            if '"car":' in vehicles_text:
                car_id = vehicles_text.split('"car":"')[1].split('"')[0]
                if car_id in changed_car_list:
                    utils.add_microcar_in_vehicles_attribute(person)
                    utils.car_to_x_in_plan(person, "microcar")


    # Write the modified XML to the output file with gzip compression
    with gzip.open(output_plan_file, "wb") as file:
        file.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        file.write(b'<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n')
        tree.write(file, encoding="utf-8")

    print(f"Modifications applied. Check the output file: {output_plan_file}")