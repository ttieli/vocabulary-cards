#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 hayday-crops.json 中缺少定义的作物
"""

import json
from pathlib import Path

BASE_PATH = Path("/Users/tieli/Library/Mobile Documents/com~apple~CloudDocs/铁力个人资料/20251020 塞尔达")
CROPS_FILE = BASE_PATH / "output/hayday-crops.json"

# 待添加的定义数据
DEFINITIONS = {
    "Indigo": {
        "definition_zh": "靛蓝是一种用于提取天然蓝色染料的植物,在历史上被广泛用于纺织品染色。在游戏中,靛蓝在13级解锁,生长时间为45分钟,用于制作蓝色染料。",
        "definition_en": "A plant used to extract natural blue dye, historically used for coloring textiles. Takes 45 minutes to grow and is used to make blue dye.",
        "example_en": "Grow indigo plants to produce beautiful blue dyes for your products.",
        "example_zh": "种植靛蓝植物来为你的产品制作美丽的蓝色染料。"
    },
    "Chili Pepper": {
        "definition_zh": "辣椒是一种辛辣的蔬菜,富含维生素C和辣椒素,可以为食物增添辣味。在游戏中,辣椒在25级解锁,生长时间为2小时,用于制作辣味食品。",
        "definition_en": "A spicy vegetable rich in vitamin C and capsaicin that adds heat to dishes. Takes 2 hours to grow and is used for spicy recipes.",
        "example_en": "Harvest chili peppers to make spicy salsa and hot sauces.",
        "example_zh": "收获辣椒来制作辣味沙拉酱和辣酱。"
    },
    "Blueberries": {
        "definition_zh": "蓝莓是一种小型的蓝紫色浆果,富含抗氧化剂,被誉为超级食物。在游戏中,蓝莓在30级解锁,用于制作蓝莓派和果汁。",
        "definition_en": "Small blue-purple berries rich in antioxidants, considered a superfood. Used to make blueberry pie and juices.",
        "example_en": "Pick fresh blueberries to bake delicious blueberry muffins.",
        "example_zh": "采摘新鲜蓝莓来烘焙美味的蓝莓松饼。"
    },
    "Potato": {
        "definition_zh": "土豆是一种重要的根茎类作物,富含淀粉和营养,可以用多种方式烹饪。在游戏中,土豆在35级解锁,用于制作薯条、土豆泥等食品。",
        "definition_en": "An important root vegetable rich in starch and nutrients that can be cooked in many ways. Used to make fries and mashed potatoes.",
        "example_en": "Grow potatoes to make crispy french fries for your customers.",
        "example_zh": "种植土豆来为你的顾客制作酥脆的炸薯条。"
    },
    "Cacao": {
        "definition_zh": "可可是巧克力的原料,来自可可树的种子。在游戏中,可可在36级解锁,生长时间较长,用于制作巧克力和可可粉。",
        "definition_en": "The source of chocolate, made from cacao tree seeds. Unlocked at level 36 and used to make chocolate and cocoa powder.",
        "example_en": "Harvest cacao pods to produce rich chocolate products.",
        "example_zh": "收获可可豆荚来生产浓郁的巧克力产品。"
    },
    "Coffee Bean": {
        "definition_zh": "咖啡豆是咖啡饮料的原料,经过烘焙后具有独特的香气和风味。在游戏中,咖啡豆在42级解锁,用于制作各种咖啡饮品。",
        "definition_en": "The raw material for coffee beverages, with unique aroma and flavor after roasting. Used to make various coffee drinks.",
        "example_en": "Grow coffee beans to brew fresh espresso for your café.",
        "example_zh": "种植咖啡豆来为你的咖啡馆冲泡新鲜浓缩咖啡。"
    },
    "Chamomile": {
        "definition_zh": "洋甘菊是一种具有药用价值的草本植物,常用于制作舒缓镇静的花草茶。在游戏中,洋甘菊在45级解锁,用于制作洋甘菊茶。",
        "definition_en": "A medicinal herb commonly used to make soothing and calming herbal tea. Unlocked at level 45 for making chamomile tea.",
        "example_en": "Harvest chamomile flowers to brew relaxing herbal tea.",
        "example_zh": "收获洋甘菊花朵来冲泡放松的花草茶。"
    }
}

def fix_incomplete_crops():
    """修复缺少定义的作物"""
    print("=" * 60)
    print("修复 hayday-crops.json 中缺少定义的作物")
    print("=" * 60)
    print()

    # 1. 加载文件
    print("Step 1: 加载文件...")
    with open(CROPS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"  总作物数: {len(data['cards'])}")
    print()

    # 2. 查找并修复不完整的卡片
    print("Step 2: 查找并修复不完整的卡片...")
    fixed_count = 0

    for card in data['cards']:
        word = card['word']

        # 检查是否缺少定义
        if word in DEFINITIONS and 'definition_zh' not in card:
            # 添加缺少的字段
            card['definition_zh'] = DEFINITIONS[word]['definition_zh']
            card['definition_en'] = DEFINITIONS[word]['definition_en']
            card['example_en'] = DEFINITIONS[word]['example_en']
            card['example_zh'] = DEFINITIONS[word]['example_zh']

            fixed_count += 1
            print(f"  ✓ 已修复: {word}")

    print()
    print(f"  总计修复: {fixed_count} 个作物")
    print()

    # 3. 保存文件
    print("Step 3: 保存文件...")
    with open(CROPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 已保存到: {CROPS_FILE}")
    print()

    # 4. 验证所有卡片
    print("Step 4: 验证所有卡片...")
    incomplete = []
    for card in data['cards']:
        if 'definition_zh' not in card or not card['definition_zh']:
            incomplete.append(card['word'])

    if incomplete:
        print(f"  ⚠️ 仍有 {len(incomplete)} 个作物缺少定义:")
        for word in incomplete:
            print(f"    - {word}")
    else:
        print("  ✓ 所有作物都已有完整定义")

    print()
    print("=" * 60)
    print("✅ 完成!")
    print("=" * 60)
    print()

if __name__ == "__main__":
    try:
        fix_incomplete_crops()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
