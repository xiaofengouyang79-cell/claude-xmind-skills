# XMind Generator Skill

> 专业级 XMind 思维导图生成器，支持多种视觉主题、自动层级样式、丰富内容结构。

## 功能特性

- ✅ 生成标准 XMind 8+ 格式文件
- ✅ 4 种精心设计的视觉主题
- ✅ 自动层级样式（根主题 → 一级 → 二级 → 叶子）
- ✅ 支持无限层级嵌套
- ✅ 即开即用，双击即可编辑

## 快速开始

### 方法 1：直接使用脚本

```bash
# 查看可用主题
python scripts/generate_xmind.py --list-themes

# 验证已有文件
python scripts/generate_xmind.py --verify "文件路径.xmind"

# 生成新文件
python scripts/generate_xmind.py \
  --title "思维导图标题" \
  --theme business \
  --input content.json \
  --output output.xmind
```

### 方法 2：在 Claude Code 中使用

只需告诉 Claude：

```
请帮我创建一个关于 [主题] 的思维导图，使用 [主题风格] 风格
```

Claude 会自动：
1. 澄清需求和内容结构
2. 选择合适的视觉主题
3. 生成完整的 XMind 文件
4. 验证并交付

## 视觉主题

| 主题 | 命令参数 | 根主题色 | 适用场景 |
|------|----------|----------|----------|
| 🌿 清新自然 | `fresh` | 翠绿 #059669 | 学习笔记、知识梳理、生活规划 |
| 💼 商务专业 | `business` | 深蓝 #1E40AF | 项目规划、工作方案、汇报展示 |
| 🌅 温暖柔和 | `warm` | 珊瑚红 #DC2626 | 健康养生、亲子教育、创意脑暴 |
| 🔮 科技冷调 | `tech` | 靛蓝 #4F46E5 | 技术架构、数据分析、系统设计 |

## 内容结构格式

输入 JSON 文件格式：

```json
[
  {
    "title": "一级主题 A",
    "children": [
      {
        "title": "二级主题 A.1",
        "children": [
          {"title": "叶子节点 A.1.1"},
          {"title": "叶子节点 A.1.2"}
        ]
      },
      {
        "title": "二级主题 A.2"
      }
    ]
  },
  {
    "title": "一级主题 B",
    "children": [...]
  }
]
```

## 文件结构

```
xmind-generator-skill/
├── SKILL.md                    # Skill 主文档（详细使用说明）
├── README.md                   # 本文件（快速参考）
├── assets/
│   └── themes.json            # 主题配置文件
├── references/
│   └── xmind-format.md       # XMind 格式规范说明
└── scripts/
    └── generate_xmind.py     # 生成脚本
```

## 层级样式说明

| 层级 | 字号 | 字重 | 背景色 | 文字色 |
|------|------|------|--------|--------|
| 根主题 | 18pt | Bold | 主题主色 | 白色 |
| 一级主题 | 13pt | Bold | 主题浅色 | 主题深色 |
| 二级主题 | 11pt | Normal | 浅灰 #F9FAFB | 深灰 #374151 |
| 叶子节点 | 10pt | Normal | 白色 #FFFFFF | 中灰 #6B7280 |

## 最佳实践

### 内容组织

1. **层次清晰**：最多 4-5 层，避免过深
2. **逻辑完整**：每个主题下的子主题要完整覆盖
3. **粒度适中**：叶子节点是可执行/可理解的最小单元
4. **平衡对称**：同级主题的详细程度尽量一致

### 标题规范

- **根主题**：简洁明确，5-15 字
- **一级主题**：概括性强，3-10 字
- **二级主题**：具体明确，5-15 字
- **叶子节点**：可执行/可理解，10-30 字

### 常见内容结构模式

**方案型**（工作方案、项目规划）
```
背景 → 目标 → 方案 → 执行 → 保障 → 风险
```

**知识型**（学习笔记、知识梳理）
```
概念 → 原理 → 方法 → 应用 → 案例 → 总结
```

**流程型**（工作流程、操作指南）
```
准备 → 步骤1 → 步骤2 → 步骤3 → 检查 → 优化
```

**分类型**（分类整理、对比分析）
```
类别A → 类别B → 类别C → 类别D → 总结对比
```

## 常见问题

### Q: XMind 打不开文件？
A: 检查文件扩展名是否为 `.xmind`，确认 XMind 版本 ≥ 8.0

### Q: 如何修改样式？
A: 用 XMind 打开后，右键主题 → 格式 → 修改样式

### Q: 如何添加图片？
A: 用 XMind 打开后，选中主题 → 插入 → 图片

### Q: 如何导出为其他格式？
A: 用 XMind 打开后，文件 → 导出 → 选择格式（PDF/PNG/Markdown 等）

## 技术细节

### XMind 文件格式

XMind 8+ 使用 ZIP 压缩包格式，内部包含：
- `content.json` - 主题内容和样式
- `metadata.json` - 元数据（创建者信息）
- `manifest.json` - 文件清单

### 样式属性

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `svg:fill` | 背景填充色 | `#1E40AF` |
| `fo:color` | 文字颜色 | `#FFFFFF` |
| `fo:font-family` | 字体 | `Microsoft YaHei` |
| `fo:font-size` | 字号 | `18pt` |
| `fo:font-weight` | 字重 | `bold` |
| `shape-class` | 形状样式 | `org.xmind.topicShape.roundedRect` |
| `border-color` | 边框颜色 | `#E5E7EB` |
| `border-width` | 边框宽度 | `1pt` |
| `line-color` | 连接线颜色 | `#9CA3AF` |

## 参考资源

- [XMind 官方文档](https://xmind.app/user-guide/)
- [XMind 开发者文档](https://xmind.app/developer/)
- [思维导图设计原则](https://www.mindmapping.com/)

---

**版本**: 1.0
**格式**: XMind 8+ JSON
**许可证**: MIT
