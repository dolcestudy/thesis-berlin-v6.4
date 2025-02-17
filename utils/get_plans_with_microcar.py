import xml.etree.ElementTree as ET
import gzip
import math
import pandas as pd

 
def create_plan_file(original_plan_file, output_file, agent_list, microcar_pct):
    
    print(f"Start creating a new plan file: {output_file}")

    num_agents = math.floor(len(agent_list) * microcar_pct/100)
    microcar_agents = set(agent_list[:num_agents])


    # Open the output file and write the XML declaration & DOCTYPE first
    with gzip.open(output_file, "wb") as f_out:
        f_out.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f_out.write(b'<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n\n')
        f_out.write(b'<population>\n\n')

        # Write the coordinate reference system attribute
        f_out.write(b'    <attributes>\n')
        f_out.write(b'        <attribute name="coordinateReferenceSystem" class="java.lang.String">EPSG:25832</attribute>\n')
        f_out.write(b'    </attributes>\n\n')

        f_out.write(b'    <!-- ====================================================================== -->\n\n')


        # Open and parse the XML incrementally
        with gzip.open(original_plan_file, 'rb') as f_in:

            context = ET.iterparse(f_in, events=("start", "end"))
            _, root = next(context)  # Get root element
            person_id = None

            for event, elem in context:

                if event == "start" and elem.tag == "person":
                    person_id = elem.get("id")  # Store the person's ID
                    # print(person_id)


                if event == "end" and elem.tag == "person":
                    # Find the correct <attribute> element
                    for attribute in elem.findall(".//attribute[@name='vehicles']"):
                        vehicles_text = attribute.text
                        if '"car":"' in vehicles_text:
                            # Extract car ID
                            car_prefix = vehicles_text.split('"car":"')[1].split('_car')[0]
                            car_id = f"{car_prefix}_car"

                            # Modify vehicles text by adding microcar
                            microcar_entry = f'"microcar":"{car_prefix}_microcar"'
                            attribute.text = vehicles_text.replace(f'"car":"{car_id}"', f'"car":"{car_id}",{microcar_entry}', 1)

                    # Modify travel mode in plan elements if the car is in the list
                    if person_id in microcar_agents:
                        # print(f"person hit! {person_id}")
                        for plan in elem.findall(".//plan"):
                            for sub_elem in plan.iter():
                                if sub_elem.text and "car" in sub_elem.text:
                                    sub_elem.text = sub_elem.text.replace("car", "microcar")
                                if sub_elem.tail and "car" in sub_elem.tail:
                                    sub_elem.tail = sub_elem.tail.replace("car", "microcar")
                                for attr_key, attr_value in sub_elem.attrib.items():
                                    if "car" in attr_value:
                                        sub_elem.attrib[attr_key] = attr_value.replace("car", "microcar")



                    person_id = None  

                    # Write modified element to output and clear memory
                    f_out.write(ET.tostring(elem, encoding='utf-8'))
                    root.clear()  # Free memory

        # Close the population tag
        f_out.write(b'\n</population>\n')


    print(f"Modifications applied. Check the output file: {output_file}")


# Run the program
if __name__ == "__main__":

    original_plan_file = r"input\v6.4\3pct-plans\berlin-v6.4-3pct-plans-micro00pct-original.xml.gz"
    df = pd.read_csv("potential_persons.csv", header=None)
    agents_list = df[0].tolist()
    # print(potential_agents[1:10])
    
    output_file = [
        r"input\v6.4\berlin-v6.4-3pct-plans-micro00pct.xml.gz",
        r"input\v6.4\berlin-v6.4-3pct-plans-micro20pct.xml.gz",
        r"input\v6.4\berlin-v6.4-3pct-plans-micro40pct.xml.gz",
        r"input\v6.4\berlin-v6.4-3pct-plans-micro60pct.xml.gz",
        r"input\v6.4\berlin-v6.4-3pct-plans-micro80pct.xml.gz",
        r"input\v6.4\berlin-v6.4-3pct-plans-micro100pct.xml.gz"]
    modified_car_pct = [0,20,40,60,80,100]


    for i in range(6):
        create_plan_file(original_plan_file, output_file[i], agents_list, modified_car_pct[i])


