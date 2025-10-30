# 英语词汇卡片网站 📚

游戏主题英语学习卡片集，包含115张精美设计的词汇卡片。采用数据驱动架构，支持无限扩展主题。

## 🎮 在线访问

访问 [https://ttieli.github.io/vocabulary-cards/](https://ttieli.github.io/vocabulary-cards/) 查看所有卡片

## 📊 内容统计

- **总卡片数**: 115张
- **主题分类**: 3个
  - 🗡️ 塞尔达传说 (70张)
  - 🏎️ 马里奥赛车 (43张)
  - 📝 张凌赫 (2张)

## ✨ 特色功能

- 🎨 精美的渐变配色设计
- 🔍 实时搜索功能（支持中英文）
- 📱 响应式布局，完美适配移动端
- 🎯 主题颜色自动区分
- ⚡ 智能图片预加载，即时显示
- 🎭 模板驱动，支持无限主题扩展
- 🔄 纯静态页面，加载快速

## 📁 项目结构

```
📦 vocabulary-cards (7个核心文件)
├── 📄 index.html          # 主页导航 + ImagePreloader模块
├── 📄 card.html           # 动态卡片查看器（模板驱动渲染）
├── 📄 cards-data.json     # 词汇数据源（唯一数据源）
├── 📄 image-checker.html  # 图片可用性检查工具
├── 📄 404.html            # 旧链接重定向页面
├── 📄 favicon.svg         # 网站图标
└── 📄 README.md           # 项目文档
```

### 架构特点

- ✅ **单一数据源**: 所有数据存储在 `cards-data.json`
- ✅ **模板驱动**: 主题配置化，无需修改代码
- ✅ **智能预加载**: 三级图片预加载策略
- ✅ **极简架构**: 仅7个文件，维护成本极低
- ✅ **快速部署**: GitHub Pages 自动部署

---

## 🎯 如何添加新主题

### 步骤1: 在 `cards-data.json` 中添加主题配置

打开 `cards-data.json`，在 `themes` 对象中添加新主题：

```json
{
  "themes": {
    "pokemon": {
      "icon": "⚡",
      "title": "Pokémon World",
      "subtitle": "Catch 'Em All Vocabulary",
      "theme_color": "#ffcb05",
      "layout": "horizontal",
      "badge_text": "POKÉMON",
      "show_header": true
    }
  }
}
```

#### 主题配置参数说明

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `icon` | String | 主题图标（emoji） | `"⚡"` |
| `title` | String | 主题标题 | `"Pokémon World"` |
| `subtitle` | String | 主题副标题 | `"Catch 'Em All Vocabulary"` |
| `theme_color` | String | 主题主色（十六进制） | `"#ffcb05"` |
| `layout` | String | 卡片布局：`"horizontal"` 或 `"vertical"` | `"horizontal"` |
| `badge_text` | String/null | 卡片头部徽章文本，`null`则不显示 | `"POKÉMON"` |
| `show_header` | Boolean | 是否显示卡片头部 | `true` |

#### 布局说明

- **`horizontal`** (水平布局): 图片在左，内容在右（适合横向图片）
- **`vertical`** (垂直布局): 图片在上，内容在下（适合竖向图片）

### 步骤2: 添加主题专属CSS样式

打开 `card.html`，在 `<style>` 标签中添加主题CSS变量：

```css
/* 在 card.html 的 <style> 中添加 */
body.pokemon {
    --theme-primary: #ffcb05;
    --theme-secondary: #3d7dca;
    --theme-accent: #ff0000;
    --theme-text: #2a75bb;
    --theme-text-dark: #003a70;
    --theme-border: rgba(255, 203, 5, 0.6);
    --theme-bg-gradient-start: #fff9e6;
    --theme-bg-gradient-end: #ffe680;
}
```

### 步骤3: 添加词汇卡片数据

在 `cards-data.json` 的 `cards` 对象中添加新主题的卡片数组：

```json
{
  "cards": {
    "pokemon": [
      {
        "theme": "pokemon",
        "filename": "pikachu.html",
        "word": "Electric",
        "pronunciation": "/ɪˈlektrɪk/",
        "chinese": "电的",
        "image": "https://example.com/pikachu.png",
        "definition_en": "Related to electricity.",
        "definition_zh": "与电有关的。",
        "example_en": "Pikachu has electric powers.",
        "example_zh": "皮卡丘有电系能力。",
        "category": "Type"
      }
    ]
  }
}
```

### 完成！

保存文件后，新主题会自动出现在首页，无需修改任何HTML或JavaScript代码！

---

## 📝 如何添加新单词

### 方法1: 为现有主题添加单词

在 `cards-data.json` 中找到对应主题的数组，添加新卡片对象：

```json
{
  "cards": {
    "mario": [
      {
        "theme": "mario",
        "filename": "turbo.html",
        "word": "Turbo",
        "pronunciation": "/ˈtɜːrbəʊ/",
        "chinese": "涡轮增压",
        "image": "https://mario.wiki.gallery/images/turbo.png",
        "definition_en": "A device that increases engine power.",
        "definition_zh": "增加引擎动力的装置。",
        "example_en": "Activate turbo mode for maximum speed!",
        "example_zh": "激活涡轮模式以获得最大速度！",
        "category": "Racing"
      }
      // ... 其他卡片
    ]
  }
}
```

### 卡片字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `theme` | String | ✅ | 所属主题名称（必须与themes中定义的一致） |
| `filename` | String | ✅ | 卡片文件名（建议用单词小写+.html） |
| `word` | String | ✅ | 英文单词 |
| `pronunciation` | String | ❌ | 音标（可选） |
| `chinese` | String | ✅ | 中文翻译 |
| `image` | String | ✅ | 图片URL（支持外部链接） |
| `definition_en` | String | ❌ | 英文定义（可选） |
| `definition_zh` | String | ❌ | 中文定义（可选） |
| `example_en` | String | ❌ | 英文例句（可选） |
| `example_zh` | String | ❌ | 中文例句（可选） |
| `category` | String | ❌ | 单词分类标签（可选） |

### 方法2: 批量添加单词

1. 打开 `cards-data.json`
2. 复制现有卡片对象作为模板
3. 批量修改字段内容
4. 保存文件

### 验证新单词

添加完成后，可以使用 `image-checker.html` 检查图片是否可用：

```
https://ttieli.github.io/vocabulary-cards/image-checker.html
```

---

## 🚀 本地预览

```bash
# 克隆仓库
git clone https://github.com/ttieli/vocabulary-cards.git

# 进入目录
cd vocabulary-cards

# 使用浏览器打开 index.html
open index.html
```

或者使用本地服务器：

```bash
# Python 3
python3 -m http.server 8000

# 访问 http://localhost:8000
```

## 🎨 卡片特点

- **高清图片**: 支持任意分辨率（推荐1280x720以上）
- **双语设计**: 英文 + 中文 + 音标
- **智能加载**: 图片懒加载 + 预加载优化
- **优雅降级**: 图片加载失败自动显示占位图
- **响应式**: 完美适配手机、平板、桌面

## 📝 技术栈

- 纯 HTML/CSS/JavaScript
- 无需任何框架和依赖
- 数据驱动架构（JSON + 模板渲染）
- CSS 变量（动态主题色）
- 智能图片预加载（viewport detection）
- 完全静态，可部署到任何静态托管服务

## 🔧 部署到GitHub Pages

1. Fork或克隆此仓库到你的GitHub账户
2. 进入仓库设置（Settings）
3. 在左侧菜单找到 "Pages"
4. Source 选择 "Deploy from a branch"
5. Branch 选择 `main` 分支和 `/ (root)` 目录
6. 点击 Save，等待几分钟
7. 访问 `https://你的用户名.github.io/vocabulary-cards/`

## 🛠️ 常见问题

### Q: 添加新主题后首页没显示？

**A**: 检查以下几点：
1. `cards-data.json` 中 `themes` 和 `cards` 两处都已添加
2. 主题名称（key）在两处必须一致
3. JSON 格式正确（注意逗号和引号）
4. 清除浏览器缓存后刷新

### Q: 卡片样式不对？

**A**: 确保在 `card.html` 的 `<style>` 中添加了主题CSS变量，变量名格式为 `body.主题名 { ... }`

### Q: 图片无法显示？

**A**:
1. 检查图片URL是否可访问
2. 使用 `image-checker.html` 工具验证图片
3. 某些网站禁止外部引用，需使用支持的图床

### Q: 如何修改现有卡片？

**A**: 直接编辑 `cards-data.json`，找到对应卡片修改字段即可，保存后自动生效

## 📄 许可

个人学习使用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

💡 **提示**:
- 点击卡片可查看详细内容
- 使用搜索框快速查找单词
- 所有数据统一在 `cards-data.json` 管理，修改后立即生效
