#!/usr/bin/env python3
"""
Comprehensive test suite for vocabulary cards project
"""

import json
import re
from pathlib import Path

def test_json_completeness():
    """Test that all cards have complete data"""
    print("=== Testing JSON Data Completeness ===\n")

    with open('cards-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues = []
    total_cards = 0

    for theme, cards in data['cards'].items():
        for card in cards:
            total_cards += 1

            # Check all required fields
            required = ['word', 'chinese', 'image', 'filename', 'theme']
            for field in required:
                if not card.get(field):
                    issues.append(f"{theme}/{card.get('filename', '?')}: Missing {field}")

            # Check image URL is valid
            image = card.get('image', '')
            if image and not (image.startswith('http://') or image.startswith('https://')):
                issues.append(f"{theme}/{card['filename']}: Invalid image URL")

    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues[:10]:
            print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    else:
        print(f"✅ All {total_cards} cards have complete data")

    return len(issues) == 0

def test_unique_filenames():
    """Test that all filenames are unique within each theme"""
    print("\n=== Testing Unique Filenames ===\n")

    with open('cards-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues = []

    for theme, cards in data['cards'].items():
        filenames = [card['filename'] for card in cards]
        duplicates = [f for f in filenames if filenames.count(f) > 1]

        if duplicates:
            unique_dupes = list(set(duplicates))
            issues.append(f"{theme}: Duplicate filenames: {unique_dupes}")

    if issues:
        print(f"❌ Found duplicate filenames:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ All filenames are unique within their themes")

    return len(issues) == 0

def test_image_urls():
    """Test that image URLs are not duplicated inappropriately"""
    print("\n=== Testing Image URLs ===\n")

    with open('cards-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Collect all image URLs with their cards
    url_to_cards = {}

    for theme, cards in data['cards'].items():
        for card in cards:
            url = card.get('image', '')
            if url:
                if url not in url_to_cards:
                    url_to_cards[url] = []
                url_to_cards[url].append(f"{theme}/{card['filename']} ({card['word']})")

    # Find URLs used multiple times
    duplicates = {url: cards for url, cards in url_to_cards.items() if len(cards) > 1}

    if duplicates:
        print(f"ℹ️  Found {len(duplicates)} images used by multiple cards:")
        for i, (url, cards) in enumerate(list(duplicates.items())[:5]):
            print(f"\n  Image {i+1}:")
            print(f"    URL: {url[:80]}...")
            print(f"    Used by:")
            for card in cards[:3]:
                print(f"      - {card}")
            if len(cards) > 3:
                print(f"      ... and {len(cards) - 3} more")

        if len(duplicates) > 5:
            print(f"\n  ... and {len(duplicates) - 5} more duplicate images")

        print(f"\nℹ️  This is OK if intentional (e.g., same character in different contexts)")
    else:
        print("✅ All images are unique")

    return True  # Not an error

def test_html_files_structure():
    """Test HTML files structure"""
    print("\n=== Testing HTML Files Structure ===\n")

    files_to_check = ['index.html', 'card-viewer.html', 'image-checker.html']
    issues = []

    for filename in files_to_check:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for basic HTML structure
            if not re.search(r'<!DOCTYPE html>', content, re.IGNORECASE):
                issues.append(f"{filename}: Missing DOCTYPE")

            if '<html' not in content.lower():
                issues.append(f"{filename}: Missing <html> tag")

            if '<head>' not in content.lower():
                issues.append(f"{filename}: Missing <head> tag")

            if '<body>' not in content.lower():
                issues.append(f"{filename}: Missing <body> tag")

            # Check for unclosed tags (basic check)
            open_divs = len(re.findall(r'<div[^>]*>', content))
            close_divs = len(re.findall(r'</div>', content))
            if open_divs != close_divs:
                issues.append(f"{filename}: Mismatched <div> tags ({open_divs} open, {close_divs} close)")

        except FileNotFoundError:
            issues.append(f"{filename}: File not found")

    if issues:
        print(f"❌ Found {len(issues)} HTML structure issues:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"✅ All HTML files have valid structure")

    return len(issues) == 0

def test_javascript_syntax():
    """Test for common JavaScript syntax errors"""
    print("\n=== Testing JavaScript Syntax ===\n")

    files_to_check = ['index.html', 'card-viewer.html', 'image-checker.html']
    issues = []

    for filename in files_to_check:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract JavaScript
            js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)

            for i, js in enumerate(js_blocks):
                # Check for common syntax errors
                # Unmatched braces
                open_braces = js.count('{')
                close_braces = js.count('}')
                if open_braces != close_braces:
                    issues.append(f"{filename} script block {i+1}: Unmatched braces ({open_braces} vs {close_braces})")

                # Unmatched parentheses
                open_parens = js.count('(')
                close_parens = js.count(')')
                if open_parens != close_parens:
                    issues.append(f"{filename} script block {i+1}: Unmatched parentheses ({open_parens} vs {close_parens})")

                # Check for async/await usage
                if 'await ' in js and 'async ' not in js:
                    # Check if await is inside an async function
                    if not re.search(r'async\s+function', js):
                        issues.append(f"{filename} script block {i+1}: 'await' used outside async function")

        except FileNotFoundError:
            issues.append(f"{filename}: File not found")

    if issues:
        print(f"❌ Found {len(issues)} JavaScript issues:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"✅ No obvious JavaScript syntax errors")

    return len(issues) == 0

def test_data_consistency():
    """Test data consistency between JSON and what's expected"""
    print("\n=== Testing Data Consistency ===\n")

    with open('cards-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues = []

    # Check theme count
    expected_themes = ['mario', 'zelda', 'zhanglinghe']
    actual_themes = list(data['cards'].keys())

    if set(expected_themes) != set(actual_themes):
        issues.append(f"Theme mismatch: expected {expected_themes}, got {actual_themes}")

    # Check card counts
    expected_counts = {
        'mario': 43,
        'zelda': 70,
        'zhanglinghe': 2
    }

    for theme, expected in expected_counts.items():
        actual = len(data['cards'].get(theme, []))
        if actual != expected:
            issues.append(f"{theme}: Expected {expected} cards, got {actual}")
        else:
            print(f"✅ {theme}: {actual} cards (correct)")

    if issues:
        print(f"\n❌ Found {len(issues)} consistency issues:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"✅ Data is consistent")

    return len(issues) == 0

def main():
    print("=" * 70)
    print("COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()

    tests = [
        ("JSON Completeness", test_json_completeness),
        ("Unique Filenames", test_unique_filenames),
        ("Image URLs", test_image_urls),
        ("HTML Structure", test_html_files_structure),
        ("JavaScript Syntax", test_javascript_syntax),
        ("Data Consistency", test_data_consistency),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Code is ready to use.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
