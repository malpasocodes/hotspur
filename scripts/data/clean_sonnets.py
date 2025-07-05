# clean_sonnets.py
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Get the sonnets section
split_point = content.find("THE END")
sonnets_section = content[:split_point]

# The actual sonnets start after the table of contents
# Look for where sonnet 1 begins
sonnet_1_start = sonnets_section.find("1\nFrom fairest creatures")

if sonnet_1_start == -1:
    # Try different pattern
    sonnet_1_start = sonnets_section.find("From fairest creatures")

print(f"Sonnet 1 starts at position: {sonnet_1_start}")

if sonnet_1_start != -1:
    # Extract just the sonnets (skip table of contents)
    just_sonnets = sonnets_section[sonnet_1_start:]
    
    print(f"Just sonnets length: {len(just_sonnets)} characters")
    print("First 300 characters of actual sonnets:")
    print(just_sonnets[:300])
else:
    print("Could not find start of Sonnet 1")
    print("Let's see what comes after the table of contents:")
    # Look for the word "VENUS" which is the last item in table of contents
    venus_pos = sonnets_section.find("VENUS AND ADONIS")
    if venus_pos != -1:
        print("Content after table of contents:")
        print(sonnets_section[venus_pos + 50:venus_pos + 300])