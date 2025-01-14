import gzip
import xml.etree.ElementTree as ET
from collections import defaultdict

def calculate_carpool_percentage_gz(events_file):
    # Dictionary to track passenger count per vehicle
    vehicle_passenger_count = defaultdict(int)
    total_car_trips = 0
    carpool_trips = 0

    # Open the gzipped XML file
    with gzip.open(events_file, 'rt', encoding='utf-8') as f:
        # Parse the XML content
        context = ET.iterparse(f, events=("start", "end"))
        for event, elem in context:
            if event == "start" and elem.tag == "event":
                if elem.attrib.get('type') == 'PersonEntersVehicle':
                    vehicle_id = elem.attrib.get('vehicle')
                    # Check if the vehicle is a car
                    if vehicle_id.startswith("car"):
                        vehicle_passenger_count[vehicle_id] += 1
            # Clear the element to save memory
            elem.clear()

    # Count car trips and carpool trips
    for vehicle_id, passenger_count in vehicle_passenger_count.items():
        total_car_trips += 1
        if passenger_count >= 3:
            carpool_trips += 1

    # Calculate percentage
    if total_car_trips == 0:
        return 0.0
    return (carpool_trips / total_car_trips) * 100


# Example usage
events_file = r"output\micro100-sp45-pce0.5-DMC2.5-MDR0.24-iter10\output_events.xml.gz"
percentage = calculate_carpool_percentage_gz(events_file)
print(f"Percentage of car trips with 3 or more people: {percentage:.2f}%")
