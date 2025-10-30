#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 Hay Day 图片链接
将 Fandom 图片 URL 从旧格式转换为新格式
"""

import json
import re
from pathlib import Path

BASE_PATH = Path("/Users/tieli/Library/Mobile Documents/com~apple~CloudDocs/铁力个人资料/20251020 塞尔达")

# 需要修复的文件
FILES_TO_FIX = [
    BASE_PATH / "output/hayday-crops.json",
    BASE_PATH / "output/hayday-animals.json",
    BASE_PATH / "output/hayday-products.json",
    BASE_PATH / "output/hayday-phase1-50cards.json",
    BASE_PATH / "cards-data/cards/hayday.json"
]

def fix_image_url(url):
    """
    修复 Fandom 图片 URL

    旧格式: https://static.wikia.nocookie.net/hayday/images/e/e2/Wheat.png/revision/latest?cb=20240218150024
    新格式: https://static.wikia.nocookie.net/hayday/images/e/e2/Wheat.png/revision/latest/scale-to-width-down/400?cb=20240218150024
    """
    if not url or 'wikia.nocookie.net' not in url:
        return url

    # 检查是否已经有 scale-to-width-down
    if 'scale-to-width-down' in url:
        return url

    # 在 revision/latest 后添加 /scale-to-width-down/400
    pattern = r'(/revision/latest)(\?cb=)'
    replacement = r'\1/scale-to-width-down/400\2'

    fixed_url = re.sub(pattern, replacement, url)
    return fixed_url

def fix_file(file_path):
    """修复一个 JSON 文件中的所有图片链接"""
    if not file_path.exists():
        print(f"  ⚠️ 文件不存在: {file_path.name}")
        return 0

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    # 处理 cards 数组
    if 'cards' in data:
        for card in data['cards']:
            if 'image' in card and card['image']:
                old_url = card['image']
                new_url = fix_image_url(old_url)
                if old_url != new_url:
                    card['image'] = new_url
                    fixed_count += 1

    # 保存修复后的文件
    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return fixed_count

def main():
    print("=" * 60)
    print("修复 Hay Day 图片链接")
    print("=" * 60)
    print()

    total_fixed = 0

    for file_path in FILES_TO_FIX:
        print(f"处理: {file_path.name}")
        count = fix_file(file_path)

        if count > 0:
            print(f"  ✓ 已修复 {count} 个图片链接")
            total_fixed += count
        else:
            print(f"  - 无需修复")
        print()

    print("=" * 60)
    print(f"✅ 完成! 总计修复 {total_fixed} 个图片链接")
    print("=" * 60)
    print()

    # 显示修复示例
    print("修复示例:")
    print("  旧格式: .../Wheat.png/revision/latest?cb=20240218150024")
    print("  新格式: .../Wheat.png/revision/latest/scale-to-width-down/400?cb=20240218150024")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
