import gzip
import xml.etree.ElementTree as ET

# Path to your .gz compressed XML file
file_path = r'output\berlin-v6.3-10pct\emission-analysis\output_event_emission.xml.gz'

# Initialize the CO2 total sum
total_co2 = 0.0
total_fc = 0.0

# Open and parse the gzip file
with gzip.open(file_path, 'rt') as f:
    # Use iterparse for efficient memory usage
    for event, elem in ET.iterparse(f, events=("start", "end")):
        if event == "start" and elem.tag == "event":
            # Check for CO2e attribute and add its value to the total if it exists
            co2_total = elem.attrib.get("CO2e")
            if co2_total is not None:
                total_co2 += float(co2_total)


            # Check for FC_MJ attribute and add its value to the total if it exists
            fc_total = elem.attrib.get("FC_MJ")
            if fc_total is not None:
                total_fc += float(fc_total)
        # Clear element to save memory
        elem.clear()

print("Total CO2:", total_co2)
print("TOTAL FC: ", total_fc, "MJ")


# ubuntu
# grep -o 'CO2e="[0-9.]*"' output_emission_events.xml | sed 's/CO2e="//; s/"//' | awk '{sum += $1} END {print sum}'