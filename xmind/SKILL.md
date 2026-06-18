---
name: xmind
description: >
  Create XMind mind map files (.xmind). Use this skill when the user asks to create a mind map,
  mindmap, XMind file, or brainstorming diagram. Produces native .xmind files that open directly
  in the XMind application.
---

# XMind Mind Map Creator

Create `.xmind` files by building a JSON structure and piping it to the bundled script.

## How to create an XMind file

1. Build a JSON object with `path`, `style`, and `sheets` fields (see format below)
2. Write it to a temp file, then run:

```bash
python <skill-dir>/scripts/create_xmind.py /tmp/xmind_input.json
```

Where `<skill-dir>` is the directory containing this SKILL.md file.

### Style selection

在 JSON 中添加 `"style"` 字段选择配色方案（可选值见下方配色速查表），不填则默认使用 `vermillion-orange`（朱砂橙）。

## JSON Input Format

```json
{
  "path": "/Users/user/Desktop/my_mindmap.xmind",
  "style": "vermillion-orange",
  "sheets": [
    {
      "title": "Sheet 1",
      "structureClass": "org.xmind.ui.map.clockwise",
      "rootTopic": {
        "title": "Central Topic",
        "children": [
          {
            "title": "Branch 1",
            "children": [
              { "title": "Sub-topic A" },
              { "title": "Sub-topic B" }
            ]
          }
        ]
      },
      "relationships": [
        { "sourceTitle": "Sub-topic A", "targetTitle": "Sub-topic B", "title": "related" }
      ]
    }
  ]
}
```

## Topic Properties

Each topic object supports:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string (required) | Topic title |
| `children` | array of topics | Child topics |
| `notes` | string or `{plain?, html?}` | Notes. HTML supports: `<strong>`, `<u>`, `<ul>`, `<ol>`, `<li>`, `<br>`. NOT `<code>`. |
| `href` | string | External URL link |
| `attachment` | string | Absolute path to a file to attach (embedded in the .xmind). Mutually exclusive with `href`. |
| `linkToTopic` | string | Title of another topic to link to (internal `xmind:#id` link, works across sheets) |
| `labels` | string[] | Tags/labels |
| `markers` | string[] | Marker IDs: `task-done`, `task-start`, `priority-1` to `priority-9` |
| `callouts` | string[] | Callout text bubbles |
| `boundaries` | `{range, title?}[]` | Visual grouping of children. Range: `"(start,end)"` |
| `summaryTopics` | `{range, title}[]` | Summary topics spanning children ranges |
| `structureClass` | string | Layout (see below) |
| `shape` | string | Topic shape (see shapes below) |
| `position` | `{x, y}` | Absolute position (only for detached topics in free-positioning sheets) |

### Topic shapes

- `org.xmind.topicShape.roundedRect` — rounded rectangle (default)
- `org.xmind.topicShape.diamond` — diamond (use for conditions/decisions)
- `org.xmind.topicShape.ellipserect` — ellipse (use for start/end)
- `org.xmind.topicShape.rect` — rectangle
- `org.xmind.topicShape.underline` — underline only
- `org.xmind.topicShape.circle` — circle
- `org.xmind.topicShape.parallelogram` — parallelogram (use for I/O)

### Layout structures

- `org.xmind.ui.map.clockwise` — balanced map
- `org.xmind.ui.map.unbalanced` — unbalanced map
- `org.xmind.ui.logic.right` — logic chart (right)
- `org.xmind.ui.org-chart.down` — org chart (down)
- `org.xmind.ui.tree.right` — tree (right)
- `org.xmind.ui.fishbone.leftHeaded` — fishbone
- `org.xmind.ui.timeline.horizontal` — timeline

### Task properties

**Simple checkbox** (no dates needed):
- `taskStatus`: `"todo"` or `"done"`

**Planned tasks** (for Gantt/timeline view in XMind):

| Field | Type | Description |
|-------|------|-------------|
| `progress` | number 0.0-1.0 | Completion progress |
| `priority` | number 1-9 | Priority (1=highest) |
| `startDate` | ISO 8601 string | Start date, e.g. `"2026-02-01T00:00:00Z"` |
| `dueDate` | ISO 8601 string | Due date |
| `durationDays` | number | Duration in days (preferred for relative planning) |
| `dependencies` | array | `{targetTitle, type, lag?}` — type: `FS`, `FF`, `SS`, `SF` |

**Two approaches for planned tasks:**

1. **Relative (preferred):** Use `durationDays` + `dependencies`. XMind auto-calculates dates.
2. **Absolute:** Use `startDate` + `dueDate` for fixed dates.

When the user mentions "planning", "schedule", "timeline", "Gantt", "project", "phases", use RELATIVE planned tasks unless specific dates are given.

## Sheet properties

| Field | Type | Description |
|-------|------|-------------|
| `title` | string (required) | Sheet title |
| `rootTopic` | topic (required) | Root topic |
| `relationships` | array | `{sourceTitle, targetTitle, title?, shape?}` — connects topics by title. `shape`: `"org.xmind.relationshipShape.curved"` (default) or `"org.xmind.relationshipShape.straight"` |
| `detachedTopics` | array of topics | Free-floating topics (require `freePositioning: true` and `position` on each topic) |
| `freePositioning` | boolean | Enable free topic positioning (for logic/flow diagrams) |

## Logic / Flow diagrams

For flowcharts, logic diagrams, or algorithmic diagrams, use **free positioning** with **detached topics** and **straight relationships**:

```json
{
  "path": "/tmp/flowchart.xmind",
  "sheets": [{
    "title": "Algorithm",
    "freePositioning": true,
    "rootTopic": {
      "title": "START",
      "shape": "org.xmind.topicShape.ellipserect",
      "structureClass": "org.xmind.ui.map.clockwise"
    },
    "detachedTopics": [
      {"title": "IS X > 0?", "position": {"x": 0, "y": 130}, "shape": "org.xmind.topicShape.diamond"},
      {"title": "PRINT YES", "position": {"x": 200, "y": 130}},
      {"title": "PRINT NO", "position": {"x": -200, "y": 130}},
      {"title": "END", "position": {"x": 0, "y": 260}, "shape": "org.xmind.topicShape.ellipserect"}
    ],
    "relationships": [
      {"sourceTitle": "START", "targetTitle": "IS X > 0?", "shape": "org.xmind.relationshipShape.straight"},
      {"sourceTitle": "IS X > 0?", "targetTitle": "PRINT YES", "title": "YES", "shape": "org.xmind.relationshipShape.straight"},
      {"sourceTitle": "IS X > 0?", "targetTitle": "PRINT NO", "title": "NO", "shape": "org.xmind.relationshipShape.straight"},
      {"sourceTitle": "PRINT YES", "targetTitle": "END", "shape": "org.xmind.relationshipShape.straight"},
      {"sourceTitle": "PRINT NO", "targetTitle": "END", "shape": "org.xmind.relationshipShape.straight"}
    ]
  }]
}
```

**Conventions:** Use **ellipse** for start/end, **diamond** for conditions, **rectangle** (default) for actions, **parallelogram** for I/O. Use `"org.xmind.relationshipShape.straight"` for all connectors. Position topics on a grid (y increments of ~130px, x offsets of ~200px for branches).

When the user mentions "flowchart", "algorithm", "logic diagram", "organigramme de programmation", "diagramme logique", use this pattern.

## Working with large files

When reading a PDF or other large file fails (e.g. "PDF too large"), extract text using CLI tools before building the mind map:

```bash
# Preferred: pdftotext (install: apt install poppler-utils)
pdftotext input.pdf /tmp/extracted.txt

# Fallback if pdftotext unavailable:
python3 -c "
import subprocess, pathlib, sys
p = sys.argv[1]
try:
    subprocess.run(['pdftotext', p, '/tmp/extracted.txt'], check=True)
except FileNotFoundError:
    subprocess.run(['pip', 'install', 'pymupdf'], check=True, capture_output=True)
    import importlib; fitz = importlib.import_module('fitz')
    doc = fitz.open(p)
    pathlib.Path('/tmp/extracted.txt').write_text('\n'.join(page.get_text() for page in doc))
" input.pdf
```

Then read `/tmp/extracted.txt` to build the mind map.

## Important rules

- The output path MUST end with `.xmind`
- Always write the file where the user requests (e.g. ~/Downloads, ~/Desktop)
- IDs are generated automatically
- Topic references in relationships and dependencies are resolved by title
- HTML notes: only `<strong>`, `<u>`, `<ul>`, `<ol>`, `<li>`, `<br>` are supported. `<code>` is NOT supported by XMind.
- Internal links (`linkToTopic`) work across sheets

## Content display rules (重要)

**参数直接写在标题上**：所有具体参数、数值、规格等信息必须作为 topic title 直接展示，不要隐藏在笔记里。用户在思维导图上应一眼就能看到所有关键信息。

**笔记内容展开为子标题**：如果某个节点有补充说明（notes），应将补充内容拆分为子主题（children），而不是写在 notes 里。只有根主题和一级主题可以保留少量简短笔记。

**正确做法：**
```json
{"title": "像素：5000万", "children": [
  {"title": "单位像素面积更大，暗光更好"},
  {"title": "相比P3的6400万像素更注质量"}
]}
```

**错误做法：**
```json
{"title": "像素", "notes": "5000万，单位像素面积更大，暗光表现更好"}
```

## Style / 配色风格选择

生成思维导图时，应提供配色风格选择。30 套配色方案详见 `xmind-templates/references/style-palettes.md`。

### 风格选择流程

1. 根据内容场景推荐 2-4 个匹配的配色方案
2. 用 `AskUserQuestion` 让用户选择
3. 将选中的配色应用到 content.json 的 style 和 theme 中

### 常用风格速查

| 场景 | 推荐风格 | 主色 |
|------|----------|------|
| 数码/科技产品 | 靛蓝紫、深青、烟紫 | `#4F46E5` `#0E7490` `#7E22CE` |
| 商务/正式 | 深海蓝、钴蓝、石墨灰 | `#1E40AF` `#1D4ED8` `#374151` |
| 学习/知识 | 天空蓝、翡翠绿、松石绿 | `#0284C7` `#059669` `#0D9488` |
| 活力/运动 | 朱砂橙、琥珀橙、珊瑚红 | `#EA580C` `#D97706` `#DC2626` |
| 创意/艺术 | 薰衣草紫、暗紫、茄紫红 | `#7C3AED` `#6B21A8` `#A21CAF` |
| 产品评测/对比 | 朱砂橙、靛蓝紫、深青 | `#EA580C` `#4F46E5` `#0E7490` |

### 配色应用

每个配色方案包含 4 级样式，通过 content.json 中 topic 的 `style.properties` 设置：

| 层级 | 背景色 | 文字色 | 字号 | 字重 |
|------|--------|--------|------|------|
| 根主题 | 主色（高饱和） | `#FFFFFF` | 18pt | bold |
| 一级主题 | 主色浅色系 | 深色 | 13pt | bold |
| 二级主题 | 极浅色系 | 中深色 | 11pt | normal |
| 叶子节点 | 近白色 | 灰色 `#6B7280` | 10pt | normal |

同时在 sheet 级别添加 `theme` 对象，确保 XMind 打开时自动应用层级配色。
