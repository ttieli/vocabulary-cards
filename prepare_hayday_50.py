#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准备 Hay Day 主题的 50 条词汇数据
Phase 1 Step 1.2: 从三个源文件中选择50个优质词汇
"""

import json
from pathlib import Path
from datetime import datetime

# 配置路径
BASE_PATH = Path("/Users/tieli/Library/Mobile Documents/com~apple~CloudDocs/铁力个人资料/20251020 塞尔达")
OUTPUT_PATH = BASE_PATH / "output"

# 源文件
CROPS_FILE = OUTPUT_PATH / "hayday-crops.json"
ANIMALS_FILE = OUTPUT_PATH / "hayday-animals.json"
PRODUCTS_FILE = OUTPUT_PATH / "hayday-products.json"

# 输出文件
OUTPUT_FILE = OUTPUT_PATH / "hayday-phase1-50cards.json"

def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def select_crops(crops_data, count=20):
    """
    从农作物中选择 20 个
    优先选择低等级、有完整信息的作物
    """
    cards = crops_data['cards']

    # 按等级排序，选择前20个
    sorted_cards = sorted(cards, key=lambda x: x.get('level', 999))
    selected = sorted_cards[:count]

    print(f"✓ 已选择 {len(selected)} 个农作物:")
    for card in selected[:5]:
        print(f"  - {card['word']} (Level {card.get('level', '?')})")
    print(f"  ... 等 {len(selected)} 个")

    return selected

def select_animals(animals_data, count=22):
    """
    从动物中选择 22 个
    优先选择农场动物和低等级动物
    """
    cards = animals_data['cards']

    # 按类别排序：Farm Animal > Sanctuary Animal > Others
    farm_animals = [c for c in cards if c.get('category') == 'Farm Animal']
    sanctuary_animals = [c for c in cards if c.get('category') == 'Sanctuary Animal']
    other_animals = [c for c in cards if c.get('category') not in ['Farm Animal', 'Sanctuary Animal']]

    # 优先选择农场动物(全选10个) + 圣域动物(选10个) + 其他(选4个)
    selected = farm_animals + sanctuary_animals[:10] + other_animals[:4]
    selected = selected[:count]  # 确保不超过22个

    print(f"✓ 已选择 {len(selected)} 个动物:")
    print(f"  - Farm Animals: {len([c for c in selected if c.get('category') == 'Farm Animal'])} 个")
    print(f"  - Sanctuary Animals: {len([c for c in selected if c.get('category') == 'Sanctuary Animal'])} 个")
    print(f"  - Others: {len([c for c in selected if c.get('category') not in ['Farm Animal', 'Sanctuary Animal']])} 个")
    for card in selected[:5]:
        print(f"  - {card['word']} ({card.get('category', '?')})")
    print(f"  ... 等 {len(selected)} 个")

    return selected

def select_products(products_data):
    """
    选择所有 8 个产品
    """
    cards = products_data['cards']

    print(f"✓ 已选择 {len(cards)} 个产品:")
    for card in cards:
        print(f"  - {card['word']}")

    return cards

def validate_card(card):
    """
    验证卡片是否包含所有必需字段
    """
    required_fields = [
        'word', 'pronunciation', 'chinese', 'image',
        'definition_zh', 'definition_en', 'theme', 'filename'
    ]

    for field in required_fields:
        if field not in card or not card[field]:
            return False, f"缺少字段: {field}"

    return True, "OK"

def generate_hayday_50_cards():
    """
    生成包含 50 个 Hay Day 词汇的 JSON 文件
    """
    print("=" * 60)
    print("开始准备 Hay Day Phase 1 词汇数据 (50 cards)")
    print("=" * 60)
    print()

    # 1. 加载源文件
    print("Step 1: 加载源文件...")
    crops_data = load_json(CROPS_FILE)
    animals_data = load_json(ANIMALS_FILE)
    products_data = load_json(PRODUCTS_FILE)
    print(f"  - 农作物: {len(crops_data['cards'])} 个")
    print(f"  - 动物: {len(animals_data['cards'])} 个")
    print(f"  - 产品: {len(products_data['cards'])} 个")
    print()

    # 2. 选择词汇
    print("Step 2: 选择词汇...")
    selected_crops = select_crops(crops_data, 20)
    print()
    selected_animals = select_animals(animals_data, 22)
    print()
    selected_products = select_products(products_data)
    print()

    # 3. 合并所有选择的卡片
    all_selected = selected_crops + selected_animals + selected_products
    total_count = len(all_selected)

    print(f"Step 3: 合并选择的卡片...")
    print(f"  总计: {total_count} 个词汇")
    print()

    # 4. 验证所有卡片
    print("Step 4: 验证卡片数据完整性...")
    invalid_cards = []
    for card in all_selected:
        is_valid, msg = validate_card(card)
        if not is_valid:
            invalid_cards.append(f"{card.get('word', 'Unknown')}: {msg}")

    if invalid_cards:
        print("  ⚠️ 发现不完整的卡片:")
        for err in invalid_cards:
            print(f"    - {err}")
        print()
    else:
        print("  ✓ 所有卡片数据完整")
        print()

    # 5. 生成输出数据
    output_data = {
        "theme": "hayday",
        "theme_name": "Hay Day农场",
        "theme_name_en": "Hay Day Farm",
        "description": "卡通农场(Hay Day)游戏中的英语词汇 - Phase 1 精选50词",
        "total_count": total_count,
        "generated_at": datetime.now().isoformat(),
        "source_files": [
            "hayday-crops.json (20 cards)",
            "hayday-animals.json (15 cards)",
            "hayday-products.json (8 cards)"
        ],
        "cards": all_selected
    }

    # 6. 保存到文件
    print("Step 5: 保存到文件...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 已保存到: {OUTPUT_FILE}")
    print(f"  文件大小: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
    print()

    # 7. 总结
    print("=" * 60)
    print("✅ 完成! Hay Day Phase 1 词汇数据已准备就绪")
    print("=" * 60)
    print()
    print("📊 数据统计:")
    print(f"  - 农作物: {len(selected_crops)} 个")
    print(f"  - 动物: {len(selected_animals)} 个")
    print(f"  - 产品: {len(selected_products)} 个")
    print(f"  - 总计: {total_count} 个")
    print()
    print("📁 输出文件:")
    print(f"  {OUTPUT_FILE}")
    print()
    print("🔜 下一步:")
    print("  运行 merge_to_cards_data.py 将这些词汇合并到 cards-data.json")
    print()

if __name__ == "__main__":
    try:
        generate_hayday_50_cards()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
