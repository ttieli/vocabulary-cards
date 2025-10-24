#!/usr/bin/env python3
"""
Fix word mappings for Zelda vocabulary cards
"""

# Correct word data for the 6 mismatched files
corrections = {
    "cooking.html": {
        "word": "Cooking",
        "pronunciation": "/ˈkʊkɪŋ/",
        "chinese": "烹饪;烹调",
        "definition_en": "The practice or skill of preparing food by combining, mixing, and heating ingredients.",
        "definition_zh": "通过混合、搅拌和加热食材来准备食物的技能或做法。",
        "example_en": "Link improves his cooking skills to create powerful dishes.",
        "example_zh": "林克提高烹饪技能来制作强大的料理。",
        "category": "活动",
        "image": "https://cdn.wikimg.net/en/zeldawiki/images/7/71/BotW_Hyrule_Day_Artwork.jpg"
    },
    "elixir.html": {
        "word": "Elixir",
        "pronunciation": "/ɪˈlɪksər/",
        "chinese": "药剂;灵药",
        "definition_en": "A magical or medicinal potion that heals or grants special abilities.",
        "definition_zh": "具有治疗或赋予特殊能力的魔法或药用药水。",
        "example_en": "Link brews elixirs to restore health and gain temporary powers.",
        "example_zh": "林克调制灵药来恢复生命值并获得临时能力。",
        "category": "物品",
        "image": "https://cdn.wikimg.net/en/zeldawiki/images/9/99/BotW_Expansion_Pass_Artwork.png"
    },
    "korok.html": {
        "word": "Korok",
        "pronunciation": "/ˈkɔːrɒk/",
        "chinese": "克洛格;树精",
        "definition_en": "A small forest spirit in the shape of a wooden creature with leaves.",
        "definition_zh": "形状像木制生物并长着叶子的小型森林精灵。",
        "example_en": "Finding all the Koroks hidden across Hyrule is a great challenge.",
        "example_zh": "找到隐藏在海拉鲁各处的所有克洛格是一个巨大的挑战。",
        "category": "角色",
        "image": "https://cdn.wikimg.net/en/zeldawiki/images/a/a1/BotW_Forest_of_Spirits_Daytime.png"
    },
    "ore.html": {
        "word": "Ore",
        "pronunciation": "/ɔːr/",
        "chinese": "矿石;矿砂",
        "definition_en": "A naturally occurring solid material from which a metal or valuable mineral can be extracted.",
        "definition_zh": "可以从中提取金属或贵重矿物的天然固体材料。",
        "example_en": "Link mines ore deposits to collect valuable materials for crafting.",
        "example_zh": "林克开采矿石以收集用于制作的宝贵材料。",
        "category": "物品",
        "image": "https://cdn.wikimg.net/en/zeldawiki/images/9/91/BotW_Building_Concept_Artwork.jpg"
    },
    "paraglider.html": {
        "word": "Paraglider",
        "pronunciation": "/ˈpærəɡlaɪdər/",
        "chinese": "滑翔伞",
        "definition_en": "A lightweight, free-flying, foot-launched aircraft with no rigid structure.",
        "definition_zh": "一种轻便的、自由飞行的、用脚起飞的无刚性结构飞行器。",
        "example_en": "The paraglider allows Link to glide safely from high places.",
        "example_zh": "滑翔伞让林克能够从高处安全滑翔。",
        "category": "物品",
        "image": "https://cdn.wikimg.net/en/zeldawiki/images/9/99/BotW_Expansion_Pass_Artwork.png"
    },
    "rupee.html": {
        "word": "Rupee",
        "pronunciation": "/ruːˈpiː/",
        "chinese": "卢比;货币",
        "definition_en": "The currency used throughout Hyrule for trading and purchasing items.",
        "definition_zh": "在海拉鲁各地用于交易和购买物品的货币。",
        "example_en": "Link collects rupees to buy equipment and supplies from merchants.",
        "example_zh": "林克收集卢比从商人那里购买装备和补给。",
        "category": "物品",
        "image": "https://cdn.wikimg.net/en/zeldawiki/images/9/91/BotW_Building_Concept_Artwork.jpg"
    }
}

# HTML template
def generate_html(data):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["word"]} - 塞尔达英语单词卡</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }}

        .page {{
            width: 100%;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .card {{
            width: 100%;
            background: #ffffff;
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 15px 50px rgba(0,0,0,0.4);
            border: 5px solid #d4a574;
            display: flex;
            flex-direction: column;
        }}

        .card-image-container {{
            width: 100%;
            min-height: 300px;
            background: linear-gradient(180deg, #e8dcc8 0%, #f5ede0 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .card-image {{
            max-width: 100%;
            max-height: 400px;
            object-fit: contain;
        }}

        .card-content {{
            padding: 30px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}

        .word-english {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2e7d8f;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}

        .pronunciation {{
            font-size: 1.3em;
            color: #8b7355;
            font-style: italic;
            margin-bottom: 15px;
        }}

        .word-chinese {{
            font-size: 1.6em;
            color: #3d6b5c;
            margin-bottom: 20px;
            font-weight: 600;
        }}

        .definition {{
            font-size: 1em;
            color: #4a4a4a;
            line-height: 1.6;
            margin-bottom: 15px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.6);
            border-left: 4px solid #5fb878;
            border-radius: 6px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }}

        .definition strong {{
            color: #2e7d8f;
        }}

        .example {{
            font-size: 0.95em;
            color: #5a5a5a;
            font-style: italic;
            padding: 15px;
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
            border-radius: 6px;
            margin-top: 10px;
            border: 2px solid #a8d5a3;
            line-height: 1.5;
        }}

        .category {{
            display: inline-block;
            padding: 8px 20px;
            background: linear-gradient(135deg, #4a90a4 0%, #5fb878 100%);
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 15px;
            box-shadow: 0 2px 8px rgba(74, 144, 164, 0.4);
            font-weight: 600;
            align-self: flex-start;
        }}

        .page-number {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            font-size: 1em;
            color: #666;
            font-weight: bold;
        }}

        /* iPad (portrait and landscape) */
        @media screen and (max-width: 1024px) {{
            .page {{
                max-width: 700px;
                padding: 15px;
            }}

            .card-image-container {{
                min-height: 250px;
            }}

            .card-image {{
                max-height: 350px;
            }}

            .word-english {{
                font-size: 2.2em;
            }}

            .pronunciation {{
                font-size: 1.2em;
            }}

            .word-chinese {{
                font-size: 1.4em;
            }}

            .card-content {{
                padding: 25px;
            }}
        }}

        /* Mobile devices */
        @media screen and (max-width: 768px) {{
            .page {{
                max-width: 100%;
                padding: 10px;
                margin: 10px auto;
            }}

            .card {{
                border-radius: 20px;
                border-width: 3px;
            }}

            .card-image-container {{
                min-height: 200px;
                padding: 15px;
            }}

            .card-image {{
                max-height: 250px;
            }}

            .card-content {{
                padding: 20px;
            }}

            .word-english {{
                font-size: 1.8em;
                margin-bottom: 8px;
            }}

            .pronunciation {{
                font-size: 1em;
                margin-bottom: 12px;
            }}

            .word-chinese {{
                font-size: 1.2em;
                margin-bottom: 15px;
            }}

            .definition {{
                font-size: 0.9em;
                padding: 12px;
                margin-bottom: 12px;
            }}

            .example {{
                font-size: 0.85em;
                padding: 12px;
            }}

            .category {{
                font-size: 0.8em;
                padding: 6px 15px;
                margin-top: 12px;
            }}

            .page-number {{
                bottom: 10px;
                right: 10px;
                font-size: 0.9em;
            }}
        }}

        /* Small mobile devices */
        @media screen and (max-width: 480px) {{
            .page {{
                padding: 5px;
                margin: 5px auto;
            }}

            .card-image-container {{
                min-height: 150px;
                padding: 10px;
            }}

            .card-image {{
                max-height: 200px;
            }}

            .word-english {{
                font-size: 1.5em;
            }}

            .pronunciation {{
                font-size: 0.9em;
            }}

            .word-chinese {{
                font-size: 1.1em;
            }}

            .definition {{
                font-size: 0.85em;
            }}

            .example {{
                font-size: 0.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="card">
            <div class="card-image-container">
                <img src="{data["image"]}" alt="{data["word"]}" class="card-image">
            </div>
            <div class="card-content">
                <div class="word-english">{data["word"]}</div>
                <div class="pronunciation">{data["pronunciation"]}</div>
                <div class="word-chinese">{data["chinese"]}</div>
                <div class="definition">
                    <strong>英文:</strong> {data["definition_en"]}<br><br>
                    <strong>中文:</strong> {data["definition_zh"]}
                </div>
                <div class="example">
                    "{data["example_en"]}"<br>
                    {data["example_zh"]}
                </div>
                <span class="category">{data["category"]}</span>
            </div>
        </div>
        <div class="page-number">Zelda Cards</div>
    </div>
</body>
</html>
'''

# Fix each file
for filename, data in corrections.items():
    filepath = f'zelda/{filename}'
    html_content = generate_html(data)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Fixed {filename} - now displays '{data['word']}'")

print("\n🎉 All 6 files have been corrected!")
