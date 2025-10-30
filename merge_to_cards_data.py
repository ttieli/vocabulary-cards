#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并 Hay Day 词汇到 cards-data.json
Phase 1 Step 1.3: 安全合并数据
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

# 配置路径
BASE_PATH = Path("/Users/tieli/Library/Mobile Documents/com~apple~CloudDocs/铁力个人资料/20251020 塞尔达")
CARDS_DATA_FILE = BASE_PATH / "cards-data.json"
HAYDAY_SOURCE_FILE = BASE_PATH / "output/hayday-phase1-50cards.json"

def backup_file(file_path):
    """创建文件备份"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{file_path.stem}.backup.{timestamp}{file_path.suffix}"
    backup_path = file_path.parent / backup_name
    shutil.copy(file_path, backup_path)
    return backup_path

def merge_hayday_data():
    """合并 Hay Day 数据到 cards-data.json"""
    print("=" * 60)
    print("Phase 1 Step 1.3: 合并 Hay Day 词汇到 cards-data.json")
    print("=" * 60)
    print()

    # Step 1: 备份原文件
    print("Step 1: 备份原文件...")
    if not CARDS_DATA_FILE.exists():
        print(f"  ❌ 错误: {CARDS_DATA_FILE} 文件不存在")
        return False

    backup_path = backup_file(CARDS_DATA_FILE)
    print(f"  ✓ 已备份到: {backup_path.name}")
    print()

    # Step 2: 加载数据
    print("Step 2: 加载数据...")
    with open(CARDS_DATA_FILE, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    with open(HAYDAY_SOURCE_FILE, 'r', encoding='utf-8') as f:
        hayday_data = json.load(f)

    print(f"  ✓ 已加载现有数据: {len(existing_data.get('themes', {}))} 个主题")
    print(f"  ✓ 已加载 Hay Day 数据: {hayday_data['total_count']} 个词汇")
    print()

    # Step 3: 检查是否已存在 hayday 主题
    if 'hayday' in existing_data.get('themes', {}):
        print("  ⚠️ 警告: hayday 主题已存在,将被覆盖")
        response = input("  是否继续? (y/n): ")
        if response.lower() != 'y':
            print("  操作已取消")
            return False
        print()

    # Step 4: 合并主题配置
    print("Step 3: 合并主题配置...")
    if 'themes' not in existing_data:
        existing_data['themes'] = {}

    existing_data['themes']['hayday'] = {
        "icon": "🌾",
        "title": "Hay Day Farm",
        "subtitle": "Farm Life & Agriculture Vocabulary",
        "theme_color": "#8BC34A",
        "layout": "horizontal",
        "badge_text": "FARM LIFE",
        "show_header": True
    }
    print("  ✓ 已添加 Hay Day 主题配置")
    print()

    # Step 5: 合并卡片数据
    print("Step 4: 合并卡片数据...")
    if 'cards' not in existing_data:
        existing_data['cards'] = {}

    existing_data['cards']['hayday'] = hayday_data['cards']
    print(f"  ✓ 已添加 {len(hayday_data['cards'])} 个 Hay Day 词汇卡片")
    print()

    # Step 6: 验证数据完整性
    print("Step 5: 验证数据完整性...")
    hayday_cards = existing_data['cards']['hayday']
    required_fields = ['word', 'pronunciation', 'chinese', 'image',
                      'definition_zh', 'definition_en', 'theme', 'filename']

    invalid_cards = []
    for card in hayday_cards:
        for field in required_fields:
            if field not in card or not card[field]:
                invalid_cards.append(f"{card.get('word', 'Unknown')}: 缺少 {field}")
                break

    if invalid_cards:
        print(f"  ⚠️ 发现 {len(invalid_cards)} 个不完整的卡片:")
        for err in invalid_cards[:5]:
            print(f"    - {err}")
        if len(invalid_cards) > 5:
            print(f"    ... 等 {len(invalid_cards)} 个")
        print()
        print("  是否仍要继续保存? (y/n): ")
        response = input()
        if response.lower() != 'y':
            print("  操作已取消")
            return False
    else:
        print("  ✓ 所有卡片数据完整")
    print()

    # Step 7: 保存更新后的文件
    print("Step 6: 保存更新后的文件...")
    with open(CARDS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    file_size = CARDS_DATA_FILE.stat().st_size / 1024
    print(f"  ✓ 已保存到: {CARDS_DATA_FILE}")
    print(f"  文件大小: {file_size:.1f} KB")
    print()

    # Step 8: 生成统计报告
    print("Step 7: 生成统计报告...")
    total_themes = len(existing_data['themes'])
    total_cards = sum(len(cards) for cards in existing_data['cards'].values())

    print(f"  总主题数: {total_themes} 个")
    print(f"  总词汇数: {total_cards} 个")
    print()
    print("  各主题词汇数量:")
    for theme, cards in existing_data['cards'].items():
        theme_name = existing_data['themes'][theme].get('title', theme)
        print(f"    - {theme_name}: {len(cards)} 个")
    print()

    # Step 9: 完成
    print("=" * 60)
    print("✅ 完成! Hay Day 词汇已成功合并到 cards-data.json")
    print("=" * 60)
    print()
    print("📝 备份文件:")
    print(f"  {backup_path}")
    print()
    print("🔜 下一步:")
    print("  1. 在浏览器中测试 Hay Day 卡片")
    print("  2. 提交到 Git")
    print("  3. 推送到 GitHub")
    print()

    return True

if __name__ == "__main__":
    try:
        success = merge_hayday_data()
        if not success:
            print("❌ 合并失败")
            exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
