#!/usr/bin/env python3
"""
Verify image-word mappings based on image filenames
"""

import json
import re
from urllib.parse import urlparse, unquote

def extract_word_from_image_url(url):
    """Try to extract the expected word from image URL"""
    # Parse URL to get filename
    path = urlparse(url).path
    filename = path.split('/')[-1]

    # Remove file extension and common prefixes
    filename = re.sub(r'\.(png|jpg|jpeg|gif)$', '', filename, flags=re.IGNORECASE)
    filename = re.sub(r'^\d+px-', '', filename)  # Remove width prefix like "120px-"
    filename = unquote(filename)  # URL decode

    # Extract potential word
    # Common patterns:
    # - MKW_Item_Name
    # - MKWorld_Item_Name
    # - BotW_Item_Name
    # - Item_Name

    patterns = [
        r'MKW?orld?_.*?_([A-Z][a-z]+(?:_[A-Z][a-z]+)*)',  # MKWorld_Icon_Rainbow_Road
        r'MKW_([A-Z][a-z]+(?:_[A-Z][a-z]+)*)_',  # MKW_Banana_Roulette
        r'BotW_([A-Z][a-z]+(?:_[A-Z][a-z]+)*)_',  # BotW_Link_Shooting
        r'([A-Z][a-z]+(?:_[A-Z][a-z]+)*)$',  # Link_Shooting_Artwork
    ]

    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            word = match.group(1).replace('_', ' ')
            return word

    # If no pattern matches, just return cleaned filename
    return filename.replace('_', ' ')

# Load JSON data
with open('cards-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Verifying Image-Word Mappings ===\n")

issues = []
total_cards = 0

for theme in ["mario", "zelda", "zhanglinghe"]:
    cards = data["cards"][theme]
    print(f"\n=== {theme.upper()} ({len(cards)} cards) ===")

    for card in cards:
        total_cards += 1
        word = card.get("word", "N/A")
        image_url = card.get("image", "")
        filename = card.get("filename", "")

        if not image_url:
            issues.append(f"❌ {theme}/{filename}: No image URL")
            continue

        # Extract word from image URL
        url_word = extract_word_from_image_url(image_url)

        # Check if they match (case-insensitive, allowing for plurals)
        word_lower = word.lower().replace(' ', '')
        url_word_lower = url_word.lower().replace(' ', '')

        # Allow some flexibility in matching
        is_match = (
            word_lower == url_word_lower or
            word_lower in url_word_lower or
            url_word_lower in word_lower or
            word_lower == url_word_lower + 's' or
            word_lower + 's' == url_word_lower
        )

        if not is_match:
            # This might be a mismatch
            print(f"⚠️  {filename}:")
            print(f"    Card word: '{word}'")
            print(f"    URL suggests: '{url_word}'")
            print(f"    Image: {image_url}")
            issues.append({
                "theme": theme,
                "filename": filename,
                "card_word": word,
                "url_word": url_word,
                "image_url": image_url
            })

print(f"\n\n=== Summary ===")
print(f"Total cards checked: {total_cards}")
print(f"Potential mismatches: {len(issues)}")

if issues:
    print("\n⚠️  Review these potential mismatches manually to determine if they're actual issues.")
    print("Note: Some mismatches may be intentional (e.g., using a related image).")
else:
    print("\n✅ No obvious mismatches detected!")

# Save issues to file for review
if issues:
    with open('image-mapping-issues.json', 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)
    print(f"\n📝 Issues saved to image-mapping-issues.json for review")
