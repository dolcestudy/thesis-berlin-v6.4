import xml.etree.ElementTree as ET
from collections import Counter
import gzip

# Path to the XML file
xml_file = r"utils\legacy\berlin-v6.4.output_allVehicles.xml"  # Replace with your file path

# Dictionary to store counts of each vehicle type
vehicle_counts = Counter()

# Open and parse the gzipped XML file
# with gzip.open(xml_file, 'rt', encoding='utf-8') as f:
tree = ET.parse(xml_file)

root = tree.getroot()

# Define the namespace used in the XML
namespace = {"ns": "http://www.matsim.org/files/dtd"}

TOTAL = 0

# Count <vehicle> elements
for vehicle in root.findall("ns:vehicle", namespace):
    vehicle_type = vehicle.get("type")
    if vehicle_type:
        vehicle_counts[vehicle_type] += 1
        TOTAL += 1

# Output the results
print("Vehicle Type Counts:")
for vehicle_type, count in vehicle_counts.items():
    print(f"{vehicle_type}: {count}")

print(TOTAL)

