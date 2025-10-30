#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拆分 cards-data.json 到模块化文件夹结构
Phase 2 Step 2.2: 创建模块化数据文件
"""

import json
from pathlib import Path
from datetime import datetime

# 配置路径
BASE_PATH = Path("/Users/tieli/Library/Mobile Documents/com~apple~CloudDocs/铁力个人资料/20251020 塞尔达")
SOURCE_FILE = BASE_PATH / "cards-data.json"
CARDS_DATA_DIR = BASE_PATH / "cards-data"
CARDS_DIR = CARDS_DATA_DIR / "cards"

def split_to_modular():
    """拆分cards-data.json到模块化结构"""
    print("=" * 60)
    print("Phase 2 Step 2.2: 拆分到模块化文件夹结构")
    print("=" * 60)
    print()

    # Step 1: 读取源文件
    print("Step 1: 读取源文件...")
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"  ✓ 已读取 {len(data.get('themes', {}))} 个主题")
    print(f"  ✓ 已读取 {sum(len(cards) for cards in data.get('cards', {}).values())} 个词汇")
    print()

    # Step 2: 创建 config.json
    print("Step 2: 创建 config.json...")
    config = {
        "version": "2.0",
        "created_at": datetime.now().isoformat(),
        "description": "Vocabulary Cards Data - Modular Structure",
        "data_structure": {
            "themes": "themes.json - Theme configurations",
            "cards": "cards/*.json - Individual theme card data"
        }
    }

    config_file = CARDS_DATA_DIR / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 已创建: {config_file.name}")
    print()

    # Step 3: 创建 themes.json
    print("Step 3: 创建 themes.json...")
    themes_data = {
        "themes": data.get('themes', {})
    }

    themes_file = CARDS_DATA_DIR / "themes.json"
    with open(themes_file, 'w', encoding='utf-8') as f:
        json.dump(themes_data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 已创建: {themes_file.name}")
    print(f"    包含 {len(themes_data['themes'])} 个主题配置")
    print()

    # Step 4: 创建各主题的卡片文件
    print("Step 4: 创建各主题的卡片文件...")
    cards_data = data.get('cards', {})

    for theme_id, cards in cards_data.items():
        theme_file = CARDS_DIR / f"{theme_id}.json"

        theme_card_data = {
            "theme": theme_id,
            "theme_name": data['themes'][theme_id].get('title', theme_id),
            "total_count": len(cards),
            "cards": cards
        }

        with open(theme_file, 'w', encoding='utf-8') as f:
            json.dump(theme_card_data, f, ensure_ascii=False, indent=2)

        file_size = theme_file.stat().st_size / 1024
        print(f"  ✓ 已创建: cards/{theme_id}.json ({len(cards)} 个词汇, {file_size:.1f} KB)")

    print()

    # Step 5: 生成统计报告
    print("Step 5: 生成统计报告...")
    print(f"  文件夹结构:")
    print(f"    cards-data/")
    print(f"    ├── config.json")
    print(f"    ├── themes.json")
    print(f"    └── cards/")
    for theme_id in cards_data.keys():
        print(f"        ├── {theme_id}.json")
    print()

    total_size = (
        (CARDS_DATA_DIR / "config.json").stat().st_size +
        (CARDS_DATA_DIR / "themes.json").stat().st_size +
        sum((CARDS_DIR / f"{theme_id}.json").stat().st_size for theme_id in cards_data.keys())
    ) / 1024

    print(f"  总文件大小: {total_size:.1f} KB")
    print(f"  原文件大小: {SOURCE_FILE.stat().st_size / 1024:.1f} KB")
    print()

    # Step 6: 完成
    print("=" * 60)
    print("✅ 完成! 已成功拆分到模块化结构")
    print("=" * 60)
    print()
    print("📁 新的文件结构:")
    print(f"  {CARDS_DATA_DIR}/")
    print()
    print("🔜 下一步:")
    print("  1. 创建 data-loader.js")
    print("  2. 修改 index.html 使用新的数据加载器")
    print("  3. 测试新结构")
    print()

if __name__ == "__main__":
    try:
        split_to_modular()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
