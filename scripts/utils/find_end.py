# find_end.py
with open('data/raw/shakespeare_complete.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Look for the end marker
end_pos = content.find("*** END OF THE PROJECT GUTENBERG EBOOK")
print(f"Found end marker at position: {end_pos}")

# Show what's around the end
if end_pos != -1:
    start = max(0, end_pos - 500)
    end = min(len(content), end_pos + 200)
    print("\nContent around the end:")
    print(content[start:end])