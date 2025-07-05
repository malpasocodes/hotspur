# split_content.py
with open('data/processed/shakespeare_only.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Find where sonnets end and plays begin
split_point = content.find("THE END")

# Extract sonnets (everything before "THE END")
sonnets_section = content[:split_point].strip()

# Extract plays (everything after "THE END")
plays_section = content[split_point + len("THE END"):].strip()

print(f"Sonnets section: {len(sonnets_section)} characters")
print(f"Plays section: {len(plays_section)} characters")

print("\nFirst 200 characters of sonnets:")
print(sonnets_section[:200])

print("\nFirst 200 characters of plays:")
print(plays_section[:200])

print("\nLast 200 characters of sonnets:")
print(sonnets_section[-200:])