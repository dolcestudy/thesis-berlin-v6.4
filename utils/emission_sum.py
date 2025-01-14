import xml.etree.ElementTree as ET

# Load the XML file
file_path = r"C:\berlin\output-detailed-offline\detailed_emission_events.xml"  # Path to your file
tree = ET.parse(file_path)
root = tree.getroot()

# Initialize sums for the emissions
emission_sums = {
    "HC": 0.0,
    "CO": 0.0,
    "NOx": 0.0,
    "FC": 0.0,
    "FC_MJ": 0.0,
    "PM": 0.0,
    "PN": 0.0,
    "CO2_TOTAL": 0.0,
    "CO2_rep": 0.0,
    "NO2": 0.0,
    "CH4": 0.0,
    "NMHC": 0.0,
    "Pb": 0.0,
    "SO2": 0.0,
    "N2O": 0.0,
    "NH3": 0.0,
    "PM_non_exhaust": 0.0,
    "Benzene": 0.0,
    "PM2_5": 0.0,
    "BC_exhaust": 0.0,
    "PM2_5_non_exhaust": 0.0,
    "BC_non_exhaust": 0.0,
    "CO2e": 0.0,
    "PM": 0.0

}

# Iterate through the XML elements
for event in root.findall('event'):
    # Check if the event is an emission event
    if event.attrib.get("type") in ["coldEmissionEvent", "warmEmissionEvent"]:
        # Sum up the values for specified emissions
        for key in emission_sums.keys():
            if key in event.attrib:
                emission_sums[key] += float(event.attrib[key])

# Print the total sums
print("Emission Totals:")
for key, value in emission_sums.items():
    print(f"{key}: {value:.2f}")
