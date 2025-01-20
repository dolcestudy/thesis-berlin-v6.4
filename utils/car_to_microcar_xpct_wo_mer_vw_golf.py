import xml.etree.ElementTree as ET
import gzip
import random
import math

# Extracts a list of car IDs from the vehicle definitions XML file
def get_car_list(vehicle_definitions_file: str) -> list:
    vehicle_tree = ET.parse(vehicle_definitions_file)
    vehicle_root = vehicle_tree.getroot()
    namespace = {"ns": "http://www.matsim.org/files/dtd"}

    return [
        vehicle.attrib["id"]
        for vehicle in vehicle_root.findall(".//ns:vehicle", namespace)
        if vehicle.attrib["type"].endswith("car")
    ]

# 
def create_plan_file(input_file, output_file, vehicle_file, microcar_pct):
    
    print(f"Start creating a new plan file: {output_file}")

    with gzip.open(input_file, 'rb') as f:
        # Parse the XML files
        tree = ET.parse(f)
        root = tree.getroot()

    # # Parse the XML files
    # tree = ET.parse(input_file)
    # root = tree.getroot()

    # Generate a random list of cars to modify
    all_car_list = get_car_list(vehicle_file)
    num_to_select = math.floor(len(all_car_list) * microcar_pct/100)
    changed_car_list = random.sample(all_car_list, num_to_select)

    # Iterate through all <person> elements and modify them
    for person in root.findall(".//person"):

        # skip car to microcar process if vehicle type is either mercedes or vwCaddy or golf
        skip_processing = False
        for vehicle_type_attr in person.findall(".//attribute[@name='vehicleTypes'][@class='org.matsim.vehicles.PersonVehicleTypes']"):
            if vehicle_type_attr.text and ("mercedes313" in vehicle_type_attr.text or "vwCaddy" in vehicle_type_attr.text or "golf1.4" in vehicle_type_attr.text):
                skip_processing = True
                break
        if skip_processing:
            continue


        # Modify vehicle type from "car" to "microcar" for selected cars
        for attribute in person.findall(".//attribute[@name='vehicles']"):
            vehicles_text = attribute.text
            if '"car":' in vehicles_text:
                # check if the car is in the list
                car_id = vehicles_text.split('"car":"')[1].split('"')[0]
                # Modify car to microcar if the selected car is in the list
                if car_id in changed_car_list:

                    car_prefix = vehicles_text.split('"car":"')[1].split('_car')[0]
                    microcar_entry = f'"microcar":"{car_prefix}_microcar"'
                    vehicles_text = vehicles_text.replace(f'"car":"{car_prefix}_car"', f'"car":"{car_prefix}_car",{microcar_entry}', 1)
                    attribute.text = vehicles_text

                    for plan in person.findall(".//plan"):
                        for elem in plan.iter():
                            if elem.text and "car" in elem.text:
                                elem.text = elem.text.replace("car", "microcar")
                            if elem.tail and "car" in elem.tail:
                                elem.tail = elem.tail.replace("car", "microcar")
                            for attr_key, attr_value in elem.attrib.items():
                                if "car" in attr_value:
                                    elem.attrib[attr_key] = attr_value.replace("car", "microcar")



    # Write the modified XML to the output file with gzip compression
    with gzip.open(output_file, "wb") as file:
        file.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        file.write(b'<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n')
        tree.write(file, encoding="utf-8")

    print(f"Modifications applied. Check the output file: {output_file}")


# Run the program
if __name__ == "__main__":

    # setting
    input_file = r"input\v6.4\berlin-v6.4-10pct-plans-micro00pct.xml.gz"
    vehicle_id_file = r"utils\berlin-v6.4.output_allVehicles.xml"
    output_file = [
        # r"input\v6.3\berlin-v6.3-10pct-plans-micro20pct.xml.gz",
        # r"input\v6.3\berlin-v6.3-10pct-plans-micro40pct.xml.gz",
        # r"input\v6.3\berlin-v6.3-10pct-plans-micro60pct.xml.gz",
        # r"input\v6.3\berlin-v6.3-10pct-plans-micro80pct.xml.gz",
        r"input\v6.4\berlin-v6.4-10pct-plans-micro100pct.xml.gz"]
    modified_car_pct = [100]

    for i in range(1):
        create_plan_file(input_file, output_file[i], vehicle_id_file, modified_car_pct[i])


