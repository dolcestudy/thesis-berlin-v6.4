import xml.etree.ElementTree as ET



# 1. vwCaddy, mercedes313 -> LCV so don't change to microcar
# 2. car, golf1.4 -> change to microcar

# Input and output files
input_file = r"input\v6.3\berlin-v6.3-10pct-plans.xml"
output_file = r"input\v6.3\berlin-v6.3-10pct-plans-micro100-2.xml"

# Parse the XML file
tree = ET.parse(input_file)
root = tree.getroot()

# Iterate through all <person> elements
for person in root.findall(".//person"):
    
    # Check for the "vehicleTypes" attribute
    skip_processing = False
    for vehicle_type_attr in person.findall(".//attribute[@name='vehicleTypes'][@class='org.matsim.vehicles.PersonVehicleTypes']"):
        if vehicle_type_attr.text and ("mercedes313" in vehicle_type_attr.text or "vwCaddy" in vehicle_type_attr.text):
            skip_processing = True
            break

    # Skip processing for this person if conditions are met
    if skip_processing:
        continue

    # Step 1: Modify the "vehicles" attribute to add "microcar"
    for attribute in person.findall(".//attribute[@name='vehicles']"):
        vehicles_text = attribute.text
        if '"car":' in vehicles_text:
            # Extract the car prefix
            car_prefix = vehicles_text.split('"car":"')[1].split('_car')[0]
            # Add microcar entry
            microcar_entry = f'"microcar":"{car_prefix}_microcar"'
            # Insert microcar into the vehicles text
            vehicles_text = vehicles_text.replace(f'"car":"{car_prefix}_car"', f'"car":"{car_prefix}_car",{microcar_entry}', 1)
            print(vehicles_text)
            attribute.text = vehicles_text

    # Step 2: Replace all occurrences of "car" with "microcar" inside <plan> elements. this includes "golf 1.4"
    for plan in person.findall(".//plan"):
        for elem in plan.iter():
            if elem.text and "car" in elem.text:
                elem.text = elem.text.replace("car", "microcar")
            if elem.tail and "car" in elem.tail:
                elem.tail = elem.tail.replace("car", "microcar")
            for attr_key, attr_value in elem.attrib.items():
                if "car" in attr_value:
                    elem.attrib[attr_key] = attr_value.replace("car", "microcar")

# Write the modified XML to the output file with the DOCTYPE declaration
with open(output_file, "wb") as file:
    file.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
    file.write(b'<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n')
    tree.write(file, encoding="utf-8")
    
print(f"Modifications applied. Check the output file: {output_file}")
