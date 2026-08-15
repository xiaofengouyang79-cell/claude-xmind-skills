# XMind Generator Skill — 设计驱动版 v3

> 把「好看即真理」的思维导图美化技巧，固化成可复用的生成器。内置设计四原则 + 视觉三要素，自动彩虹分支配色、智能文字对比、色阶层级。

## 一键生成

```bash
py -3 scripts/generate_xmind.py \
  --title "我的思维导图" \
  --theme spectrum \
  --input content.json \
  --output "输出.xmind"
```

## 13 套主题 · 8 大设计家族

```bash
py -3 scripts/generate_xmind.py --list-themes
```

| 家族 | 主题 | 设计来源 |
|------|------|----------|
| 经典六色 | business / fresh / warm / tech / rose / slate | 内置 |
| 蒙多海报 | mondo（丝网复古双色）| qiaomu-mondo-poster-design |
| 编辑杂志 | editorial（白纸黑字）| frontend-design |
| 野兽派 | brutalist（纯原色·直角）| frontend-design |
| 复古霓虹 | neon（暗底霓虹）| frontend-design |
| 手绘线稿 | ink（线框无填充）| ian-xiaohei-illustrations |
| 生成艺术 | spectrum（色谱沿序涌现）| algorithmic-art |
| 画廊色场 | gallery（几何静默）| canvas-design |

## 输入格式（content.json）

```json
[
  {
    "title": "一级分支",
    "emoji": "🚀",
    "children": [
      { "title": "二级主题", "marker": "priority-1" },
      { "title": "叶子节点", "note": "备注" }
    ]
  }
]
```

## 相比 v1 的升级

| 维度 | v1 | v3（本版） |
|------|----|----|
| 分支配色 | 所有分支同一浅色 | **彩虹分支配色**，每支不同强调色 |
| 层级 | 主/次/叶全用灰色 | 主→次→叶**色阶明度递进** |
| 文字对比 | 硬编码 | **按明度自动适配**黑/白字 |
| 连线 | 灰色折线 | **曲线 + 分支配色** |
| 层级深度 | 3 层后塌缩 | **任意深度**（深层无填充防噪声） |
| 丰富度 | 无 | 图标 / 优先级标记 / 备注 / 标签 |
| 主题数 | 4（子/叶全灰） | **13（8 大设计流派，全层级设计 token）** |
| 流派扩展 | 无 | 支持直角 shape / 线稿 fill_mode |

## 文件结构

```
xmind-generator-skill/
├── SKILL.md                        # 主文档（触发 + 工作流）
├── README.md                       # 快速开始（本文件）
├── assets/themes.json              # 13 套主题设计 token
├── examples/                       # 示例大纲（朱镕基 / 刘润）
├── references/
│   ├── design-principles.md        # 设计四原则 + 配色三要义
│   ├── design-styles.md            # 8 大设计流派设计 DNA
│   └── xmind-format.md             # XMind 8+ 格式规范
└── scripts/generate_xmind.py       # 生成器
```
