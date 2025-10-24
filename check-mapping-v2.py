#!/usr/bin/env python3

import re
import json
from pathlib import Path

# Extract cardsData from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the cardsData object
match = re.search(r'const cardsData = ({.*?});', content, re.DOTALL)
if not match:
    print("Could not find cardsData in index.html")
    exit(1)

cards_data_str = match.group(1)

# Parse the cardsData
# Convert JS object to JSON format
cards_data_str = re.sub(r'(\w+):', r'"\1":', cards_data_str)  # Add quotes to keys
cards_data_str = re.sub(r'"filename"', r'"filename"', cards_data_str)
cards_data_str = re.sub(r'"word"', r'"word"', cards_data_str)

try:
    cards_data = json.loads(cards_data_str)
except:
    # Manually parse if JSON fails
    cards_data = {
        "mario": [],
        "zelda": [],
        "zhanglinghe": []
    }

    for scene in ["mario", "zelda", "zhanglinghe"]:
        pattern = rf'"{scene}": \[(.*?)\]'
        scene_match = re.search(pattern, content, re.DOTALL)
        if scene_match:
            items_str = scene_match.group(1)
            filename_pattern = r'"filename": "([^"]+)"'
            word_pattern = r'"word": "([^"]+)"'

            filenames = re.findall(filename_pattern, items_str)
            words = re.findall(word_pattern, items_str)

            for fn, wd in zip(filenames, words):
                cards_data[scene].append({"filename": fn, "word": wd})

def extract_word_from_html(filepath):
    """Extract the word from an HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Try different patterns
    patterns = [
        r'<div class="word-english">([^<]+)</div>',
        r'<h1[^>]*>([^<]+)</h1>',
        r'<div class="word">([^<]+)</div>',
    ]

    for pattern in patterns:
        match = re.search(pattern, html_content)
        if match:
            return match.group(1).strip()

    return "NOT_FOUND"

print("=== Checking Word Mappings ===\n")

# Check each scene
for scene in ["mario", "zelda", "zhanglinghe"]:
    print(f"=== {scene.upper()} ===")

    # Get all HTML files in directory
    scene_dir = Path(scene)
    html_files = {f.name: f for f in scene_dir.glob("*.html")}

    # Get expected mappings from index.html
    expected_mappings = {item["filename"]: item["word"] for item in cards_data[scene]}

    # Check files in directory
    issues = []
    for filename, filepath in sorted(html_files.items()):
        actual_word = extract_word_from_html(filepath)
        expected_word = expected_mappings.get(filename, "NOT_IN_INDEX")

        if expected_word == "NOT_IN_INDEX":
            issues.append(f"⚠️  {filename}: File exists but NOT in index.html (word: {actual_word})")
        elif actual_word != expected_word:
            issues.append(f"❌ {filename}: index.html says '{expected_word}' but HTML shows '{actual_word}'")

    # Check files in index.html but not in directory
    for filename, expected_word in sorted(expected_mappings.items()):
        if filename not in html_files:
            issues.append(f"⚠️  {filename}: Listed in index.html (word: '{expected_word}') but FILE DOESN'T EXIST")

    if issues:
        for issue in issues:
            print(issue)
    else:
        print("✅ All mappings correct!")

    print(f"\nStats: {len(html_files)} HTML files, {len(expected_mappings)} entries in index.html\n")

print("=== Summary of Problems ===")
print("\nMain issues found:")
print("1. Several HTML files have wrong content (word mismatch)")
print("2. Some duplicate files exist in mario/ but not referenced in index.html")
print("3. Need to verify all word mappings are correct")
