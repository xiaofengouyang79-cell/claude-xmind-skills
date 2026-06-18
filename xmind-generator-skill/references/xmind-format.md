# XMind 文件格式规范

## 概述

XMind 8+ 使用 ZIP 压缩包格式存储思维导图，文件扩展名为 `.xmind`。

## 文件结构

```
*.xmind (ZIP压缩包)
├── content.json      # 主要内容（主题、子主题、样式）
├── metadata.json     # 元数据（创建者信息）
└── manifest.json     # 文件清单
```

## content.json 结构

### 根结构

```json
[
  {
    "id": "唯一标识符",
    "class": "sheet",
    "rootTopic": { ... }
  }
]
```

### 主题节点结构

```json
{
  "id": "唯一标识符",
  "class": "topic",
  "title": "主题标题",
  "style": {
    "properties": {
      "svg:fill": "#颜色代码",
      "fo:color": "#颜色代码",
      "fo:font-family": "字体名称",
      "fo:font-size": "字号",
      "fo:font-weight": "字重",
      "shape-class": "形状类名",
      "border-color": "#边框颜色",
      "border-width": "边框宽度",
      "line-color": "#连接线颜色"
    }
  },
  "children": {
    "attached": [
      { ... },
      { ... }
    ]
  }
}
```

## 样式属性详解

### 背景相关

| 属性 | 说明 | 类型 | 示例 |
|------|------|------|------|
| `svg:fill` | 背景填充色 | 颜色值 | `#1E40AF` |
| `svg:fill-opacity` | 背景透明度 | 0-1 | `1` |

### 文字相关

| 属性 | 说明 | 类型 | 示例 |
|------|------|------|------|
| `fo:color` | 文字颜色 | 颜色值 | `#FFFFFF` |
| `fo:font-family` | 字体 | 字体名 | `Microsoft YaHei` |
| `fo:font-size` | 字号 | 尺寸值 | `18pt` |
| `fo:font-weight` | 字重 | 关键字 | `bold` / `normal` |
| `fo:font-style` | 字体风格 | 关键字 | `italic` / `normal` |
| `fo:text-decoration` | 文本装饰 | 关键字 | `underline` / `none` |
| `fo:text-align` | 文本对齐 | 关键字 | `left` / `center` / `right` |

### 形状相关

| 属性 | 说明 | 类型 | 示例 |
|------|------|------|------|
| `shape-class` | 形状类名 | 类名 | `org.xmind.topicShape.roundedRect` |
| `svg:rx` | 圆角半径 X | 尺寸值 | `8px` |
| `svg:ry` | 圆角半径 Y | 尺寸值 | `8px` |
| `border-color` | 边框颜色 | 颜色值 | `#E5E7EB` |
| `border-width` | 边框宽度 | 尺寸值 | `1pt` |

### 连接线相关

| 属性 | 说明 | 类型 | 示例 |
|------|------|------|------|
| `line-color` | 连接线颜色 | 颜色值 | `#9CA3AF` |
| `line-width` | 连接线宽度 | 尺寸值 | `1pt` |
| `line-class` | 连接线类名 | 类名 | `org.xmind.branchConnection.curved` |

### 形状类名选项

| 类名 | 说明 |
|------|------|
| `org.xmind.topicShape.roundedRect` | 圆角矩形（默认） |
| `org.xmind.topicShape.rect` | 矩形 |
| `org.xmind.topicShape.ellipse` | 椭圆 |
| `org.xmind.topicShape.diamond` | 菱形 |
| `org.xmind.topicShape.cloud` | 云形 |

### 连接线类名选项

| 类名 | 说明 |
|------|------|
| `org.xmind.branchConnection.curved` | 曲线连接 |
| `org.xmind.branchConnection.elbow` | 折线连接 |
| `org.xmind.branchConnection.straight` | 直线连接 |

## metadata.json 结构

```json
{
  "creator": {
    "name": "创建者名称",
    "version": "版本号"
  }
}
```

## manifest.json 结构

```json
{
  "file-entries": {
    "content.json": {},
    "metadata.json": {}
  }
}
```

## ID 生成规则

- 使用 UUID 的前 26 位十六进制字符
- 格式：`uuid.uuid4().hex[:26]`
- 示例：`755cdd1c95f84d2ab6fc07c492`

## 层级结构规范

### 根主题（Root Topic）

- 每个 sheet 只有一个根主题
- 位于 `rootTopic` 字段
- 使用最大字号和最醒目颜色

### 一级主题（Main Topic）

- 根主题的直接子节点
- 位于 `rootTopic.children.attached` 数组
- 使用较大字号和主题浅色背景

### 二级主题（Sub Topic）

- 一级主题的子节点
- 位于各一级主题的 `children.attached` 数组
- 使用中等字号和浅灰背景

### 叶子节点（Leaf Topic）

- 最底层节点，无子节点
- 使用较小字号和白色背景
- 可选：不设置 `children` 字段

## 最佳实践

1. **ID 唯一性**：确保每个节点的 ID 唯一
2. **层级深度**：建议最多 4-5 层
3. **标题长度**：控制在合理范围内
4. **样式一致性**：同级节点使用相同样式
5. **文件大小**：单个文件建议不超过 10MB

## 兼容性

- XMind 8：完全支持
- XMind 2020+：完全支持
- XMind for Web：完全支持
- 其他思维导图软件：可能需要转换格式

---

> 参考：XMind Developer Documentation
> https://xmind.app/developer/
