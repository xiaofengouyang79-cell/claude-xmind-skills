---
name: xmind-generator-skill
description: 生成专业级 XMind 思维导图文件（.xmind），支持多种视觉主题、自动布局、丰富样式。当用户需要制作思维导图、知识结构图、方案梳理、项目规划、学习笔记时使用。输出为 XMind 原生格式，可直接用 XMind 软件打开编辑。
---

# XMind Generator Skill

> 来源识别: xmind-generator-skill 基于 XMind 8+ JSON 格式规范创建，输出标准 .xmind 文件（ZIP 压缩包内含 content.json + metadata.json + manifest.json）。

## 这个 Skill 做什么

生成一份**专业级 XMind 思维导图文件**，支持：

- **4 种视觉主题**：清新自然 / 商务专业 / 温暖柔和 / 科技冷调
- **自动层级样式**：根主题、一级主题、二级主题、叶子节点各有专属样式
- **丰富的内容结构**：支持多层级嵌套、图标标记、颜色区分
- **即开即用**：输出 .xmind 文件，双击即可用 XMind 打开编辑

### 视觉主题

| 主题 | 根主题色 | 一级主题色 | 适用场景 |
|------|----------|------------|----------|
| 🌿 清新自然 | 翠绿 #059669 | 浅绿 #D1FAE5 | 学习笔记、知识梳理、生活规划 |
| 💼 商务专业 | 深蓝 #1E40AF | 浅蓝 #DBEAFE | 项目规划、工作方案、汇报展示 |
| 🌅 温暖柔和 | 珊瑚红 #DC2626 | 浅粉 #FEE2E2 | 健康养生、亲子教育、创意脑暴 |
| 🔮 科技冷调 | 靛蓝 #4F46E5 | 浅紫 #E0E7FF | 技术架构、数据分析、系统设计 |

## 何时使用

**合适的场景**：
- 需要制作思维导图整理思路
- 知识体系梳理和学习笔记
- 项目规划和方案设计
- 会议纪要和决策树
- 教学大纲和课程设计
- 个人成长规划和目标管理

**不合适的场景**：
- 需要多人实时协作（用在线工具）
- 需要复杂图表和数据可视化（用专业工具）
- 需要大量图片嵌入（XMind 图片支持有限）

## XMind 文件格式规范

### 文件结构

```
*.xmind (ZIP压缩包)
├── content.json      # 主要内容（主题、子主题、样式）
├── metadata.json     # 元数据（创建者信息）
└── manifest.json     # 文件清单
```

### content.json 结构

```json
[
  {
    "id": "唯一ID",
    "class": "sheet",
    "rootTopic": {
      "id": "唯一ID",
      "class": "topic",
      "title": "根主题标题",
      "style": {
        "properties": {
          "svg:fill": "#颜色",
          "fo:color": "#文字颜色",
          "fo:font-family": "Microsoft YaHei",
          "fo:font-size": "18pt",
          "shape-class": "org.xmind.topicShape.roundedRect",
          "fo:font-weight": "bold"
        }
      },
      "children": {
        "attached": [
          {
            "id": "唯一ID",
            "class": "topic",
            "title": "子主题标题",
            "style": { ... },
            "children": { ... }
          }
        ]
      }
    }
  }
]
```

### 样式属性说明

| 属性 | 说明 | 示例值 |
|------|------|--------|
| `svg:fill` | 背景填充色 | `#1E40AF` |
| `fo:color` | 文字颜色 | `#FFFFFF` |
| `fo:font-family` | 字体 | `Microsoft YaHei` |
| `fo:font-size` | 字号 | `18pt` / `13pt` / `11pt` / `10pt` |
| `fo:font-weight` | 字重 | `bold` / `normal` |
| `shape-class` | 形状样式 | `org.xmind.topicShape.roundedRect` |
| `border-color` | 边框颜色 | `#E5E7EB` |
| `border-width` | 边框宽度 | `1pt` |
| `line-color` | 连接线颜色 | `#9CA3AF` |

### 主题层级样式规范

#### 根主题（Root Topic）
- 字号：18pt
- 字重：bold
- 背景：主题主色
- 文字：白色
- 形状：圆角矩形

#### 一级主题（Main Topic）
- 字号：13pt
- 字重：bold
- 背景：主题浅色
- 文字：主题深色
- 形状：圆角矩形

#### 二级主题（Sub Topic）
- 字号：11pt
- 字重：normal
- 背景：浅灰 #F9FAFB
- 文字：深灰 #374151
- 边框：灰色 #E5E7EB
- 形状：圆角矩形

#### 叶子节点（Leaf Topic）
- 字号：10pt
- 字重：normal
- 背景：白色 #FFFFFF
- 文字：中灰 #6B7280
- 边框：浅灰 #F3F4F6
- 形状：圆角矩形

## 工作流

### Step 1 · 需求澄清（**动手前必做**）

**如果用户已经给了完整的大纲和结构**，可以直接进 Step 2。

**如果用户只给了主题或模糊想法**，用以下问题逐个对齐：

| # | 问题 | 为什么要问 |
|---|------|-----------|
| 1 | **主题是什么？** | 确定根节点标题 |
| 2 | **用途/场景？** | 决定视觉主题和内容深度 |
| 3 | **希望包含哪些主要内容模块？** | 确定一级主题 |
| 4 | **每个模块需要展开到什么程度？** | 确定层级深度 |
| 5 | **偏好哪种视觉风格？** | 清新/商务/温暖/科技 |
| 6 | **有没有特殊要求？** | 如需标记重点、添加备注等 |

#### 主题选择参考

| 如果用户说... | 推荐主题 |
|---|------|
| 学习、知识、教育、健康、生活 | 🌿 清新自然 |
| 工作、项目、汇报、商务、正式 | 💼 商务专业 |
| 养生、亲子、创意、温暖、柔和 | 🌅 温暖柔和 |
| 技术、架构、数据、系统、分析 | 🔮 科技冷调 |

### Step 2 · 内容结构设计

#### 结构设计原则

1. **层次清晰**：最多 4-5 层，避免过深
2. **逻辑完整**：每个主题下的子主题要完整覆盖
3. **粒度适中**：叶子节点是可执行/可理解的最小单元
4. **平衡对称**：同级主题的详细程度尽量一致

#### 内容结构模板

```
根主题
├── 一级主题 A（概述/背景）
│   ├── 二级主题 A.1
│   │   ├── 叶子节点
│   │   └── 叶子节点
│   └── 二级主题 A.2
├── 一级主题 B（核心内容）
│   ├── 二级主题 B.1
│   └── 二级主题 B.2
├── 一级主题 C（核心内容）
├── 一级主题 D（核心内容）
└── 一级主题 E（总结/注意事项）
```

#### 常见内容结构模式

**方案型**（适合工作方案、项目规划）
```
背景 → 目标 → 方案 → 执行 → 保障 → 风险
```

**知识型**（适合学习笔记、知识梳理）
```
概念 → 原理 → 方法 → 应用 → 案例 → 总结
```

**流程型**（适合工作流程、操作指南）
```
准备 → 步骤1 → 步骤2 → 步骤3 → 检查 → 优化
```

**分类型**（适合分类整理、对比分析）
```
类别A → 类别B → 类别C → 类别D → 总结对比
```

### Step 3 · 生成 XMind 文件

#### 3.1 准备工作

1. 确认内容结构和层级关系
2. 选择视觉主题（清新/商务/温暖/科技）
3. 为每个节点生成唯一 ID（使用 uuid.uuid4().hex[:26]）

#### 3.2 样式配置

根据选择的主题，配置各层级样式：

```python
# 清新自然主题
THEME_FRESH = {
    "root": {
        "svg:fill": "#059669",
        "fo:color": "#FFFFFF",
        "fo:font-size": "18pt",
        "fo:font-weight": "bold"
    },
    "main": {
        "svg:fill": "#D1FAE5",
        "fo:color": "#065F46",
        "fo:font-size": "13pt",
        "fo:font-weight": "bold"
    },
    "sub": {
        "svg:fill": "#F9FAFB",
        "fo:color": "#374151",
        "fo:font-size": "11pt",
        "border-color": "#E5E7EB"
    },
    "leaf": {
        "svg:fill": "#FFFFFF",
        "fo:color": "#6B7280",
        "fo:font-size": "10pt",
        "border-color": "#F3F4F6"
    }
}
```

#### 3.3 生成代码结构

```python
import json
import zipfile
import uuid

def gen_id():
    return uuid.uuid4().hex[:26]

def create_topic(title, children=None, style=None):
    topic = {
        "id": gen_id(),
        "class": "topic",
        "title": title
    }
    if style:
        topic["style"] = {"properties": style}
    if children:
        topic["children"] = {"attached": children}
    return topic

def create_xmind(root_title, main_topics, theme="fresh"):
    content = [{
        "id": gen_id(),
        "class": "sheet",
        "rootTopic": create_topic(root_title, main_topics, get_theme("root", theme))
    }]
    
    metadata = {"creator": {"name": "XMind Generator", "version": "1.0"}}
    manifest = {"file-entries": {"content.json": {}, "metadata.json": {}}}
    
    return content, metadata, manifest

def save_xmind(content, metadata, manifest, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
```

#### 3.4 输出文件

- 文件格式：`.xmind`
- 文件位置：`G:/claude-output/` 或用户指定位置
- 文件命名：`{主题名称}.xmind`

### Step 4 · 验证与交付

1. **验证文件格式**：确认是有效的 ZIP 压缩包
2. **验证内容结构**：检查 JSON 格式正确、层级完整
3. **验证样式**：确认各层级样式配置正确
4. **告知用户**：说明文件位置、如何打开、可编辑的内容

## 内容组织最佳实践

### 标题规范

- **根主题**：简洁明确，5-15 字
- **一级主题**：概括性强，3-10 字
- **二级主题**：具体明确，5-15 字
- **叶子节点**：可执行/可理解，10-30 字

### 层级规范

- 最多 4-5 层（根 + 3-4 级子主题）
- 每个主题下的子主题数量：3-7 个为宜
- 同级主题的详细程度保持一致

### 内容规范

- 使用陈述句而非疑问句
- 避免重复和冗余
- 重要信息放在前面
- 使用动词开头描述行动项

## 常见问题

### Q: XMind 打不开文件？
A: 检查文件扩展名是否为 `.xmind`，确认 XMind 版本 ≥ 8.0

### Q: 如何修改样式？
A: 用 XMind 打开后，右键主题 → 格式 → 修改样式

### Q: 如何添加图片？
A: 用 XMind 打开后，选中主题 → 插入 → 图片

### Q: 如何导出为其他格式？
A: 用 XMind 打开后，文件 → 导出 → 选择格式（PDF/PNG/Markdown 等）

## 参考资源

- XMind 官方文档：https://xmind.app/user-guide/
- XMind 格式规范：https://xmind.app/developer/
- 思维导图设计原则：https://www.mindmapping.com/

---

<!-- provenance: xmind-generator-skill | 基于 XMind 8+ JSON 格式规范 -->
