# find_sections.py
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Find where sonnets start (should be at the beginning)
sonnets_start = content.find("THE SONNETS")
print(f"THE SONNETS starts at position: {sonnets_start}")

# Find where the first play starts
first_play_start = content.find("ALL'S WELL THAT ENDS WELL")
print(f"ALL'S WELL THAT ENDS WELL starts at position: {first_play_start}")

# Show what's between them (this should be all the sonnets)
print(f"\nSonnets section length: {first_play_start - sonnets_start} characters")

# Show the beginning of the sonnets section
print("\nFirst 200 characters of sonnets:")
print(content[sonnets_start:sonnets_start + 200])

# Show what comes right before the first play
print("\nLast 200 characters before first play:")
print(content[first_play_start - 200:first_play_start])