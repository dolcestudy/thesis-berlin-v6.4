import xml.etree.ElementTree as ET
from collections import defaultdict

def get_unique_allowed_speeds(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize a set to store unique allowed_speed values
    unique_speeds = set()

    # Iterate over all link elements
    for link in root.findall(".//link"):
        # Find the attributes element within each link
        attributes = link.find("attributes")
        if attributes is not None:
            # Find the allowed_speed attribute within the attributes element
            for attribute in attributes.findall("attribute"):
                if attribute.get("name") == "allowed_speed":
                    # Add the value of allowed_speed to the set
                    unique_speeds.add(round(float(attribute.text)*3.6))

    return unique_speeds


def get_allowed_speed_counts(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Dictionary to store counts of attributes for each unique allowed_speed
    speed_attribute_counts = defaultdict(int)

    # Iterate over all link elements
    for link in root.findall(".//link"):
        # Find the attributes element within each link
        attributes = link.find("attributes")
        if attributes is not None:
            # Find the allowed_speed attribute within the attributes element
            for attribute in attributes.findall("attribute"):
                if attribute.get("name") == "allowed_speed":
                    allowed_speed = round(3.6*float(attribute.text))
                    # Count the number of attributes for this allowed_speed
                    speed_attribute_counts[allowed_speed] += len(attributes.findall("attribute"))

    return speed_attribute_counts




# Specify the path to your XML file
file_path = r"C:\Users\ikuma\Downloads\berlin-v6.3-network-with-pt (2).xml"

# Get unique allowed_speed values
unique_speeds = get_unique_allowed_speeds(file_path)

# Get counts of attributes for each unique allowed_speed
speed_counts = get_allowed_speed_counts(file_path)



# Print the unique values
print("Unique allowed_speed values:", unique_speeds)

# Print the results
# Sort the results by allowed_speed and print them
print("Allowed_speed counts (sorted by allowed_speed):")
for speed in sorted(speed_counts.keys()):
    print(f"Allowed_speed: {speed}, Number of Attributes: {speed_counts[speed]}")