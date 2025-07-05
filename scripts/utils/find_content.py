# find_content.py
with open('data/raw/shakespeare_complete.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Look for "SONNETS" which should be the first item in your table of contents
sonnets_pos = content.find("SONNETS")
print(f"Found 'SONNETS' at position: {sonnets_pos}")

# Show 200 characters before and after where "SONNETS" appears
if sonnets_pos != -1:
    start = max(0, sonnets_pos - 1500)
    end = min(len(content), sonnets_pos + 1500)
    print("\nContent around 'SONNETS':")
    print(content[start:end])