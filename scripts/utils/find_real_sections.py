# find_real_sections.py
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# The table of contents shows the titles, but let's find where they actually appear as section headers
# Let's look for "THE END" which you mentioned marks the end of each section

end_positions = []
start_pos = 0
while True:
    pos = content.find("THE END", start_pos)
    if pos == -1:
        break
    end_positions.append(pos)
    start_pos = pos + 1

print(f"Found {len(end_positions)} instances of 'THE END'")

# Show what comes after the first few "THE END" markers
for i, pos in enumerate(end_positions[:3]):
    print(f"\n--- After THE END #{i+1} (position {pos}) ---")
    # Show 100 characters after "THE END"
    next_section = content[pos:pos + 150]
    print(next_section)