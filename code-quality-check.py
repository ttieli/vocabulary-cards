#!/usr/bin/env python3
"""
Code quality checks for the vocabulary cards project
"""

import re

def check_index_html():
    """Check index.html for potential issues"""
    print("=== Checking index.html ===\n")

    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    warnings = []

    # Check if loadData function exists
    if 'async function loadData()' in content:
        print("✅ loadData() function found")
    else:
        issues.append("❌ loadData() function not found")

    # Check if fetch is used
    if "fetch('cards-data.json')" in content:
        print("✅ Fetches cards-data.json")
    else:
        issues.append("❌ Does not fetch cards-data.json")

    # Check if fallback data exists
    if 'cardsDataFallback' in content:
        print("✅ Has fallback data")
    else:
        warnings.append("⚠️  No fallback data")

    # Check if renderScenes uses loaded data
    if 'const dataToUse = cardsData || cardsDataFallback' in content:
        print("✅ renderScenes uses loaded data with fallback")
    else:
        warnings.append("⚠️  renderScenes might not use loaded data correctly")

    # Check if initApp is called
    if 'initApp()' in content or 'addEventListener' in content and 'DOMContentLoaded' in content:
        print("✅ Initialization logic present")
    else:
        issues.append("❌ No initialization logic found")

    # Check if showCard function uses card-viewer.html
    if 'card-viewer.html?theme=' in content:
        print("✅ showCard uses dynamic card-viewer.html")
    else:
        warnings.append("⚠️  showCard might still use old HTML files")

    return issues, warnings

def check_card_viewer():
    """Check card-viewer.html for potential issues"""
    print("\n=== Checking card-viewer.html ===\n")

    with open('card-viewer.html', 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    warnings = []

    # Check if it loads JSON
    if "fetch('cards-data.json')" in content:
        print("✅ Fetches cards-data.json")
    else:
        issues.append("❌ Does not fetch cards-data.json")

    # Check if it reads URL parameters
    if 'URLSearchParams' in content and 'window.location.search' in content:
        print("✅ Reads URL parameters")
    else:
        issues.append("❌ Does not read URL parameters")

    # Check if it has error handling
    if 'try' in content and 'catch' in content:
        print("✅ Has error handling")
    else:
        warnings.append("⚠️  No error handling")

    # Check if it supports both themes
    if 'mario' in content.lower() and 'zelda' in content.lower():
        print("✅ Supports multiple themes")
    else:
        warnings.append("⚠️  Might not support multiple themes")

    return issues, warnings

def check_image_checker():
    """Check image-checker.html for potential issues"""
    print("\n=== Checking image-checker.html ===\n")

    with open('image-checker.html', 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    warnings = []

    # Check if it loads data from JSON
    if 'async function loadData()' in content:
        print("✅ Has loadData() function")
    else:
        issues.append("❌ No loadData() function")

    # Check if it builds mappings from JSON
    if 'imageWordMappings[card.image]' in content or 'imageWordMappings' in content:
        print("✅ Builds image-word mappings")
    else:
        warnings.append("⚠️  Might not build mappings correctly")

    # Check if it has fallback
    if 'imageWordMappingsFallback' in content or 'Fallback' in content:
        print("✅ Has fallback data")
    else:
        warnings.append("⚠️  No fallback data")

    return issues, warnings

def check_json_validity():
    """Check JSON file validity"""
    print("\n=== Checking cards-data.json ===\n")

    import json

    try:
        with open('cards-data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        print("✅ JSON is valid")

        # Check structure
        if 'version' in data and 'themes' in data and 'cards' in data:
            print("✅ Has correct structure")
        else:
            return ["❌ Missing required top-level keys"], []

        # Check all themes have data
        for theme in data['themes'].keys():
            if theme in data['cards']:
                print(f"✅ Theme '{theme}' has card data")
            else:
                return [f"❌ Theme '{theme}' has no card data"], []

        return [], []

    except json.JSONDecodeError as e:
        return [f"❌ JSON is invalid: {e}"], []
    except FileNotFoundError:
        return ["❌ cards-data.json not found"], []

def main():
    print("=" * 60)
    print("CODE QUALITY CHECK")
    print("=" * 60)
    print()

    all_issues = []
    all_warnings = []

    # Check JSON
    issues, warnings = check_json_validity()
    all_issues.extend(issues)
    all_warnings.extend(warnings)

    # Check index.html
    issues, warnings = check_index_html()
    all_issues.extend(issues)
    all_warnings.extend(warnings)

    # Check card-viewer.html
    issues, warnings = check_card_viewer()
    all_issues.extend(issues)
    all_warnings.extend(warnings)

    # Check image-checker.html
    issues, warnings = check_image_checker()
    all_issues.extend(issues)
    all_warnings.extend(warnings)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()

    if all_issues:
        print(f"❌ CRITICAL ISSUES FOUND: {len(all_issues)}")
        for issue in all_issues:
            print(f"  {issue}")
        print()
    else:
        print("✅ NO CRITICAL ISSUES FOUND!")
        print()

    if all_warnings:
        print(f"⚠️  WARNINGS: {len(all_warnings)}")
        for warning in all_warnings:
            print(f"  {warning}")
        print()
    else:
        print("✅ NO WARNINGS!")
        print()

    if not all_issues and not all_warnings:
        print("🎉 ALL CHECKS PASSED!")
    elif not all_issues:
        print("✅ Code is functional but has some warnings")
    else:
        print("❌ Code has critical issues that need to be fixed")

    return len(all_issues) == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
