import xml.etree.ElementTree as ET
import pandas as pd
import gzip
from collections import defaultdict

# Function to parse a gzipped XML file
def parse_gzipped_xml(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
    return tree

# Parse vehicle.xml.gz to map vehicle IDs to their types
def parse_vehicle_file(vehicle_file):
    tree = parse_gzipped_xml(vehicle_file)
    root = tree.getroot()

    # Namespace handling for vehicleDefinitions
    ns = {'ns': "http://www.matsim.org/files/dtd"}
    vehicle_map = {}

    for vehicle in root.findall('ns:vehicle', ns):
        vehicle_id = vehicle.attrib['id']
        vehicle_type = vehicle.attrib['type']
        vehicle_map[vehicle_id] = vehicle_type
        print(vehicle_type)

    return vehicle_map

# Efficient XML parsing with iterparse
def parse_event_file_efficient(event_file, vehicle_map):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'FC_MJ': 0.0, 'CO2e': 0.0})))

    with gzip.open(event_file, 'rt', encoding='utf-8') as f:
        context = ET.iterparse(f, events=('start', 'end'))
        for event, elem in context:
            if event == 'start' and elem.tag == 'event':
                if elem.attrib.get('type') == 'warmEmissionEvent':
                    time = float(elem.attrib['time'])
                    link_id = elem.attrib['linkId']
                    vehicle_id = elem.attrib['vehicleId']
                    fc_mj = float(elem.attrib['FC_MJ'])
                    co2e = float(elem.attrib['CO2e'])

                    print(time, ": ", vehicle_id)

                    vehicle_type = vehicle_map.get(vehicle_id, 'unknown')

                    # Aggregate FC_MJ and CO2e
                    data[vehicle_type][time][link_id]['FC_MJ'] += fc_mj
                    data[vehicle_type][time][link_id]['CO2e'] += co2e

                elem.clear()  # Free memory for processed elements

    return data

# Convert aggregated data to a pandas DataFrame
def aggregate_data_to_dataframe(data):
    rows = []
    for vehicle_type, times in data.items():
        for time, links in times.items():
            for link_id, emissions in links.items():
                rows.append({
                    'vehicleType': vehicle_type,
                    'time': time,
                    'linkId': link_id,
                    'sum_FC_MJ': emissions['FC_MJ'],
                    'sum_CO2e': emissions['CO2e']
                })

    return pd.DataFrame(rows)

# Main execution
if __name__ == "__main__":
    vehicle_file = r"output\micro100-sp60-pce0.5-DMC2.5-MDR0.24-iter10\emission-analysis\output_vehicles.xml.gz"
    event_file = r"output\micro100-sp60-pce0.5-DMC2.5-MDR0.24-iter10\emission-analysis\output_event_emission.xml.gz"
    output_excel_file = "emissions_summary.xlsx"

    # Parse XML files
    print("Start parsing the vehicle file")
    vehicle_map = parse_vehicle_file(vehicle_file)
    print("Start parsing the event file")
    data = parse_event_file_efficient(event_file, vehicle_map)

    # Convert to DataFrame and save to Excel
    df = aggregate_data_to_dataframe(data)
    df.to_excel(output_excel_file, index=False)

    print(f"Excel file created: {output_excel_file}")
