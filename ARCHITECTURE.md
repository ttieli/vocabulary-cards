# Vocabulary Cards - Architecture Documentation

## Overview

This project has been refactored to use a centralized JSON data structure, eliminating data duplication and making maintenance easier.

## Architecture Changes

### Before (Old Architecture)
- **Data Storage**: Hardcoded in individual HTML files (115 files in mario/, zelda/, zhanglinghe/ directories)
- **Data Duplication**: Same data embedded in:
  - `index.html` (JavaScript object)
  - `image-checker.html` (image-word mappings)
  - Individual card HTML files (115 files)
- **Maintenance**: Required updating multiple files for any data change
- **Scalability**: Adding new cards meant creating new HTML files and updating multiple places

### After (New Architecture)
- **Single Source of Truth**: `cards-data.json` - centralized data file containing all vocabulary cards
- **Dynamic Loading**: All pages load data from JSON at runtime
- **Dynamic Card Rendering**: `card-viewer.html` - single template that renders any card based on URL parameters
- **No Duplication**: Data exists in one place only

## File Structure

### Core Data File
```
cards-data.json         # Central data storage for all vocabulary cards
```

### Main Pages
```
index.html              # Home page - loads and displays all themes and cards
card-viewer.html        # Dynamic card viewer - renders individual cards via URL parameters
image-checker.html      # Image availability checker - validates all card images
```

### Legacy Files (Deprecated)
```
mario/*.html            # Old individual card files (can be removed)
zelda/*.html            # Old individual card files (can be removed)
zhanglinghe/*.html      # Old individual card files (can be removed)
```

### Utility Scripts
```
extract-all-data.py     # Extract card data from HTML files to JSON
verify-image-mappings.py # Verify image-word mappings
check-mapping-v2.py     # Check word mappings consistency
```

## JSON Data Structure

```json
{
  "version": "1.0.0",
  "updated": "2025-10-24",
  "themes": {
    "mario": {
      "icon": "🏎️",
      "title": "Mario Kart World",
      "subtitle": "Racing Adventure Vocabulary",
      "theme_color": "#e60012"
    },
    "zelda": { ... },
    "zhanglinghe": { ... }
  },
  "cards": {
    "mario": [
      {
        "theme": "mario",
        "filename": "accelerate.html",
        "word": "Accelerate",
        "pronunciation": "/əkˈseləreɪt/",
        "chinese": "加速",
        "image": "https://...",
        "definition_en": "...",
        "definition_zh": "...",
        "example_en": "...",
        "example_zh": "...",
        "category": "Racing"
      }
    ],
    "zelda": [ ... ],
    "zhanglinghe": [ ... ]
  }
}
```

## How It Works

### 1. Home Page (index.html)
1. Loads `cards-data.json` on page load
2. Dynamically generates theme sections
3. Renders word cards for each theme
4. Clicking a card opens it in `card-viewer.html` via iframe

### 2. Card Viewer (card-viewer.html)
- URL format: `card-viewer.html?theme=zelda&file=archer.html`
- Loads card data from JSON based on URL parameters
- Dynamically renders card with theme-specific styling
- Supports both Mario and Zelda themes

### 3. Image Checker (image-checker.html)
1. Loads `cards-data.json` on page load
2. Builds image-word mappings from card data
3. Tests each image URL for availability
4. Displays resolution and HD status
5. Allows filtering and copying unavailable images

## Benefits of New Architecture

1. **Single Source of Truth**: All data in one JSON file
2. **Easy Maintenance**: Update data in one place
3. **No Duplication**: Eliminates sync issues
4. **Scalability**: Add new cards by adding to JSON
5. **Flexibility**: Easy to add new themes or fields
6. **Performance**: Smaller total file size
7. **Data Validation**: Can validate JSON structure
8. **API Ready**: JSON can be used for future API endpoints

## Adding New Cards

### Old Method (Deprecated)
1. Create new HTML file in theme directory
2. Update `index.html` with new card entry
3. Update `image-checker.html` with image mapping
4. Risk of inconsistencies

### New Method
1. Add card object to `cards-data.json` under appropriate theme
2. Done! All pages automatically reflect the change

Example:
```json
{
  "theme": "mario",
  "filename": "newword.html",
  "word": "New Word",
  "pronunciation": "/njuː wɜːrd/",
  "chinese": "新词",
  "image": "https://...",
  "definition_en": "...",
  "definition_zh": "...",
  "example_en": "...",
  "example_zh": "...",
  "category": "Items"
}
```

## Migration Notes

- Old HTML card files are kept for backward compatibility
- Can be safely removed once new architecture is confirmed working
- All data has been extracted and verified in JSON

## Future Enhancements

1. **Backend API**: Serve JSON via REST API
2. **Database**: Store cards in database instead of JSON
3. **Admin Panel**: Web interface to add/edit cards
4. **Search**: Full-text search across all cards
5. **Export**: Export cards to different formats (CSV, Excel, etc.)
6. **Localization**: Support multiple languages
7. **User Progress**: Track learning progress

## Version History

- **v1.0.0** (2025-10-24): Initial refactor to JSON-based architecture
  - Centralized data in `cards-data.json`
  - Created dynamic card viewer
  - Updated all pages to load from JSON
  - Verified data integrity (115 cards total)
