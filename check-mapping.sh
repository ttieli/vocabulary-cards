#!/bin/bash

echo "=== Checking word mappings between HTML files and index.html ==="
echo ""

# Function to extract word from HTML file
extract_word() {
    grep -oP '<div class="word-english">\K[^<]+' "$1" || \
    grep -oP '<h1[^>]*>\K[^<]+(?=</h1>)' "$1" || \
    echo "NOT_FOUND"
}

# Check zelda cards
echo "=== ZELDA Cards Mapping Issues ==="
for file in zelda/*.html; do
    filename=$(basename "$file")
    actual_word=$(extract_word "$file")

    # Search for this filename in index.html
    expected_word=$(grep -B2 "\"filename\": \"$filename\"" index.html | grep "\"word\":" | sed 's/.*"word": "\(.*\)".*/\1/')

    if [ "$actual_word" != "$expected_word" ]; then
        echo "❌ $filename: Expected='$expected_word' but HTML shows='$actual_word'"
    fi
done

echo ""
echo "=== MARIO Cards Mapping Issues ==="
for file in mario/*.html; do
    filename=$(basename "$file")
    actual_word=$(extract_word "$file")

    # Search for this filename in index.html
    expected_word=$(grep -B2 "\"filename\": \"$filename\"" index.html | grep "\"word\":" | sed 's/.*"word": "\(.*\)".*/\1/')

    if [ "$actual_word" != "$expected_word" ]; then
        echo "❌ $filename: Expected='$expected_word' but HTML shows='$actual_word'"
    fi
done

echo ""
echo "=== ZHANGLINGHE Cards Mapping Issues ==="
for file in zhanglinghe/*.html; do
    filename=$(basename "$file")
    actual_word=$(extract_word "$file")

    # Search for this filename in index.html
    expected_word=$(grep -B2 "\"filename\": \"$filename\"" index.html | grep "\"word\":" | sed 's/.*"word": "\(.*\)".*/\1/')

    if [ "$actual_word" != "$expected_word" ]; then
        echo "❌ $filename: Expected='$expected_word' but HTML shows='$actual_word'"
    fi
done

echo ""
echo "=== Checking for files in directories but not in index.html ==="
echo ""
echo "ZELDA:"
for file in zelda/*.html; do
    filename=$(basename "$file")
    if ! grep -q "\"filename\": \"$filename\"" index.html; then
        actual_word=$(extract_word "$file")
        echo "⚠️  $filename (word: $actual_word) - exists in directory but NOT in index.html"
    fi
done

echo ""
echo "MARIO:"
for file in mario/*.html; do
    filename=$(basename "$file")
    if ! grep -q "\"filename\": \"$filename\"" index.html; then
        actual_word=$(extract_word "$file")
        echo "⚠️  $filename (word: $actual_word) - exists in directory but NOT in index.html"
    fi
done

echo ""
echo "=== Summary ==="
echo "Total Zelda HTML files: $(ls zelda/*.html | wc -l)"
echo "Total Zelda entries in index.html: $(grep -c '"filename":.*\.html"' index.html | head -1 || grep '"zelda":' -A 1000 index.html | grep -c '"filename":')"
echo "Total Mario HTML files: $(ls mario/*.html | wc -l)"
echo "Total Mario entries in index.html: $(grep '"mario":' -A 1000 index.html | grep '"filename":' | head -43 | wc -l)"
