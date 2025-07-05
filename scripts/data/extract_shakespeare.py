# extract_shakespeare.py
with open('data/raw/shakespeare_complete.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Find the boundaries
start_marker = "THE SONNETS"
end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

# Extract just the Shakespeare content
shakespeare_content = content[start_pos:end_pos].strip()

print(f"Extracted content length: {len(shakespeare_content)} characters")
print("First 300 characters:")
print(shakespeare_content[:300])
print("\nLast 300 characters:")
print(shakespeare_content[-300:])

# Save the clean content
with open('data/processed/shakespeare_only.txt', 'w', encoding='utf-8') as file:
    file.write(shakespeare_content)

print("\nSaved clean Shakespeare content to data/processed/shakespeare_only.txt")