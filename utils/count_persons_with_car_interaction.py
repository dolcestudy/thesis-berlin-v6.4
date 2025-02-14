import gzip
import xml.etree.ElementTree as ET

def count_persons_with_car_interaction(xml_gz_file):
    persons_with_car_interaction = set()  # Use a set to store unique person IDs

    # Open the compressed XML file
    with gzip.open(xml_gz_file, 'rt', encoding='utf-8') as f:
        context = ET.iterparse(f, events=("start", "end"))
        person_id = None
        inside_plan = False
        person_count = 0

        for event, elem in context:
            if event == "start":
                if elem.tag == "person":
                    person_id = elem.get("id")  # Store the person's ID
                    person_count += 1
                elif elem.tag == "plan":
                    inside_plan = True  # Track when inside a <plan> element
                # elif inside_plan and elem.tag == "leg" and elem.get("mode") == "car":
                elif inside_plan and elem.tag == "activity" and elem.get("type") == "car interaction":
                    if person_id:
                        persons_with_car_interaction.add(person_id)  # Add to unique set

            elif event == "end":
                if elem.tag == "person":
                    person_id = None  # Reset when leaving a person
                elif elem.tag == "plan":
                    inside_plan = False  # Reset when leaving a plan
                elem.clear()  # Free memory (important for large files)

    return len(persons_with_car_interaction), person_count

# Example usage
xml_gz_file = r"C:\Users\ikuma\Work Place\SRM\Thesis\matsim-berlin\output\micro000pct-sp60-pce0.5-DMC-2.5-MDR-0.24-iter0\berlin-v6.4.output_plans.xml.gz"
count, person_number = count_persons_with_car_interaction(xml_gz_file)
print(f"Number of persons with at least one 'car interaction': {count}")
print(person_number)
