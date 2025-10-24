#!/usr/bin/env python3
"""
Extract all card data from HTML files and create centralized JSON
"""

import re
import json
from pathlib import Path

def extract_card_data(filepath, theme):
    """Extract all data from a card HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    data = {
        "theme": theme,
        "filename": filepath.name
    }

    # Extract word
    match = re.search(r'<div class="word-english">([^<]+)</div>', html_content)
    if match:
        data["word"] = match.group(1).strip()

    # Extract pronunciation
    match = re.search(r'<div class="pronunciation">([^<]+)</div>', html_content)
    if match:
        data["pronunciation"] = match.group(1).strip()

    # Extract Chinese
    match = re.search(r'<div class="word-chinese">([^<]+)</div>', html_content)
    if match:
        data["chinese"] = match.group(1).strip()

    # Extract image URL
    match = re.search(r'<img[^>]+src="([^"]+)"[^>]*alt="[^"]*"[^>]*class="card-image"', html_content)
    if match:
        data["image"] = match.group(1).strip()

    # Extract definition (both English and Chinese)
    match = re.search(r'<div class="definition">(.*?)</div>', html_content, re.DOTALL)
    if match:
        def_content = match.group(1)

        # Extract English definition
        en_match = re.search(r'<strong>英文:</strong>\s*([^<]+?)(?:<br>|$)', def_content, re.DOTALL)
        if en_match:
            data["definition_en"] = en_match.group(1).strip()

        # Extract Chinese definition
        zh_match = re.search(r'<strong>中文:</strong>\s*([^<]+?)(?:</div>|$)', def_content, re.DOTALL)
        if zh_match:
            data["definition_zh"] = zh_match.group(1).strip()

    # Extract example (both English and Chinese)
    match = re.search(r'<div class="example">(.*?)</div>', html_content, re.DOTALL)
    if match:
        example_content = match.group(1)

        # Split by <br>
        parts = re.split(r'<br>|\n', example_content)
        if len(parts) >= 2:
            # English example (with quotes)
            en_example = parts[0].strip()
            en_example = re.sub(r'^["\']|["\']$', '', en_example)  # Remove quotes
            data["example_en"] = en_example.strip()

            # Chinese example
            zh_example = parts[1].strip()
            data["example_zh"] = zh_example.strip()

    # Extract category
    match = re.search(r'<span class="category">([^<]+)</span>', html_content)
    if match:
        data["category"] = match.group(1).strip()

    return data

# Extract data from all themes
all_cards = {
    "mario": [],
    "zelda": [],
    "zhanglinghe": []
}

theme_info = {
    "mario": {
        "icon": "🏎️",
        "title": "Mario Kart World",
        "subtitle": "Racing Adventure Vocabulary",
        "theme_color": "#e60012"
    },
    "zelda": {
        "icon": "🗡️",
        "title": "The Legend of Zelda",
        "subtitle": "Adventure & Exploration Words",
        "theme_color": "#00a870"
    },
    "zhanglinghe": {
        "icon": "📝",
        "title": "Zhang Linghe",
        "subtitle": "Special Collection",
        "theme_color": "#7c3aed"
    }
}

# Process each theme
for theme in ["mario", "zelda", "zhanglinghe"]:
    theme_dir = Path(theme)
    if not theme_dir.exists():
        continue

    print(f"\n=== Processing {theme.upper()} ===")

    for html_file in sorted(theme_dir.glob("*.html")):
        try:
            card_data = extract_card_data(html_file, theme)
            all_cards[theme].append(card_data)
            print(f"✅ {html_file.name}: {card_data.get('word', 'N/A')}")
        except Exception as e:
            print(f"❌ Error processing {html_file.name}: {e}")

    print(f"Total: {len(all_cards[theme])} cards")

# Create final data structure
final_data = {
    "version": "1.0.0",
    "updated": "2025-10-24",
    "themes": theme_info,
    "cards": all_cards
}

# Save to JSON file
output_file = "cards-data.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Data extracted successfully!")
print(f"📦 Saved to {output_file}")
print(f"\nTotal cards: {sum(len(cards) for cards in all_cards.values())}")
print(f"  - Mario: {len(all_cards['mario'])}")
print(f"  - Zelda: {len(all_cards['zelda'])}")
print(f"  - Zhanglinghe: {len(all_cards['zhanglinghe'])}")
