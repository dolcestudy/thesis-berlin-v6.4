#!/bin/bash

# Input and output files
INPUT_FILE="berlin-v6.3-10pct-plans.xml"
OUTPUT_FILE="berlin-v6.3-10pct-plans-microcar100-4.xml"


sed -E '
/<attribute name="vehicles".*"car":/ {
    s/"car":"([^"]+)_car"/"car":"\1_car","microcar":"\1_microcar"/
    s/^,\s*// # Remove any leading commas, if present
}' "$INPUT_FILE" |

# Step 2: Replace all "car" with "microcar" inside the <plan> element
awk '
BEGIN { inside_plan = 0 }
/<plan/ { inside_plan = 1 }
{
    if (inside_plan) {
        gsub("car", "microcar")
    }
}
{
    print
}
/<\/plan>/ { inside_plan = 0 }
' > "$OUTPUT_FILE"

echo "Modifications applied. Check the output file: $OUTPUT_FILE"
