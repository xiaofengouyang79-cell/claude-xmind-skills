# XMind 文件格式规范（v2）

## 文件结构

```
*.xmind (ZIP)
├── content.json      # 主题、子主题、样式、结构
├── metadata.json     # 元数据
└── manifest.json     # 文件清单
```

## 节点结构

```json
{
  "id": "26位hex",
  "class": "topic",
  "title": "标题（可含 emoji 前缀）",
  "style": { "properties": { ... } },
  "children": { "attached": [ ... ] },
  "markers": [ { "markerId": "priority-1" } ],
  "notes": { "plain": { "content": "备注文本" } },
  "labels": [ "标签" ],
  "structure-class": "org.xmind.ui.logic.right"
}
```

## 样式属性

### 背景
| 属性 | 说明 |
|------|------|
| `svg:fill` | 填充色 |
| `svg:fill-opacity` | 透明度 0–1 |

### 文字
| 属性 | 说明 |
|------|------|
| `fo:color` | 文字色 |
| `fo:font-family` | 字体 |
| `fo:font-size` | 字号（pt）|
| `fo:font-weight` | `bold` / `normal` |
| `fo:font-style` | `italic` / `normal` |
| `fo:text-align` | `left` / `center` / `right` |

### 形状与边框
| 属性 | 说明 |
|------|------|
| `shape-class` | `org.xmind.topicShape.roundedRect` / `rect` / `ellipse` / `diamond` / `cloud` |
| `border-color` | 边框色 |
| `border-width` | 边框宽（pt）|

### 连接线
| 属性 | 说明 |
|------|------|
| `line-class` | `org.xmind.branchConnection.curved` / `elbow` / `straight` |
| `line-color` | 连线色 |
| `line-width` | 连线宽（pt）|

## 结构类型（structure-class）

| 友好名 | 类名 |
|--------|------|
| map（默认）| `org.xmind.ui.map.unbalanced` |
| logic-right | `org.xmind.ui.logic.right` |
| logic-left | `org.xmind.ui.logic.left` |
| org-chart | `org.xmind.ui.org-chart.down` |
| tree-right | `org.xmind.ui.tree.right` |
| tree-left | `org.xmind.ui.tree.left` |
| timeline | `org.xmind.ui.timeline.horizontal` |
| fishbone | `org.xmind.ui.fishbone.rightHeaded` |

## 标记（markers）

`priority-1` ~ `priority-6`、`star`、`flag`、`flag-red`、`task-start`、`task-done`、`arrow-up`、`arrow-down`、`smile`、`month` 等。

## 层级与配色（脚本内置规则）

| 层级 | 填充 | 文字 | 字重 | 说明 |
|------|------|------|------|------|
| root | 主题主色 | 自动 | bold 20pt | 最醒目 |
| main | 分支强调色（彩虹）| 自动 | bold 14pt | 每支不同色相 |
| sub | tint(强调色, 0.88) | darken(强调色, 0.55) | bold 12pt | 同色系浅色 |
| leaf | tint(强调色, 0.97) | 深灰 #334155 | normal 11pt | 近白底 |
| deep | 无填充 | 中灰 #475569 | normal 10pt | 防视觉噪声 |

- **彩虹分支**：一级分支按 `accents[]` 循环取色，分支内子节点继承同一强调色。
- **智能对比**：`readable_text()` 按 WCAG 对比度自动选白字/深字。
- **曲线连线**：统一 `curved`，主分支连线同分支色。

## 兼容性

XMind 8 / 2020+ / Web 均可打开。其他思维导图软件可能需要转换格式。
