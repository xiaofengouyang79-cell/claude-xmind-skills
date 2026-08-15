# Claude XMind Skills

三套 Claude Code XMind 思维导图技能包，帮助你在 Claude Code 中快速创建专业的 XMind 思维导图。

## 📦 包含的技能（各司其职，按需选择）

| 技能 | 定位 | 何时用 |
|------|------|--------|
| **xmind-generator-skill** ⭐ | **设计驱动主技能** — 13 套主题 · 8 大设计流派 · 自动彩虹分支配色/智能文字对比 | 日常思维导图、知识梳理、读书笔记、成长/学习路径、人物生平（**首选**）|
| **xmind** | 高级格式 — 流程图、甘特图、关系线、自由定位、任务依赖 | 流程图 / 逻辑图 / 项目管理 / 甘特图 |
| **xmind-templates** | 模板与配色参考库 — 30 套配色 + 6 类场景模板 | 查阅配色速查表、场景模板 |

> **推荐路径**：日常做思维导图 → 用 `xmind-generator-skill`；需要流程图/Gantt → 用 `xmind`；需要配色灵感 → 查 `xmind-templates`。

## 🎨 13 套主题 · 8 大设计流派（xmind-generator-skill）

| 设计流派 | 主题 | 设计来源 |
|----------|------|----------|
| 经典六色 | `business` `fresh` `warm` `tech` `rose` `slate` | 内置 |
| 蒙多海报 | `mondo`（丝网复古双色）| Mondo 海报风 |
| 编辑杂志 | `editorial`（白纸黑字+一个强调色）| frontend-design |
| 野兽派 | `brutalist`（纯原色·直角）| frontend-design |
| 复古霓虹 | `neon`（暗底霓虹）| frontend-design |
| 手绘线稿 | `ink`（线框无填充）| ian-xiaohei-illustrations |
| 生成艺术 | `spectrum`（色谱沿序涌现）| algorithmic-art |
| 画廊色场 | `gallery`（几何静默）| canvas-design |

## 🚀 安装方法

将这三个文件夹复制到你的 Claude Code skills 目录：

```bash
# Linux / macOS
cp -r xmind-generator-skill ~/.claude/skills/
cp -r xmind ~/.claude/skills/
cp -r xmind-templates ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse xmind-generator-skill "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse xmind "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse xmind-templates "$env:USERPROFILE\.claude\skills\"
```

## 📖 使用方法

### 日常思维导图（xmind-generator-skill）

在 Claude Code 中直接说「帮我做一个关于 XX 的思维导图」，或使用命令行：

```bash
py -3 xmind-generator-skill/scripts/generate_xmind.py \
  --title "主题" --theme spectrum --input content.json --output output.xmind
py -3 xmind-generator-skill/scripts/generate_xmind.py --list-themes   # 查 13 套主题
```

### 流程图 / 甘特图（xmind）

输入 `/xmind`，用 `create_xmind.py` 处理 `{path, style, sheets}` 格式的 JSON，支持 relationships、callouts、boundaries、task 依赖（Gantt）。

## 支持的类型

- 📚 **读书笔记** / 🎓 **课程教案** / 📊 **产品分析**
- 🗂️ **项目规划·甘特图** / 🔄 **流程图·逻辑图** / 🏢 **组织架构**
- 🧭 **成长路径·学习路径** / 👤 **人物生平·历史脉络** / 💡 **头脑风暴**

## ⚙️ 依赖

- Python 3.6+（无第三方依赖）
- XMind 软件（用于打开生成的 .xmind 文件）

## 📄 许可

MIT License

## 🙏 致谢

- 基于 [apeyroux/mcp-xmind](https://github.com/apeyroux/mcp-xmind) 的 xmind skill
- XMind 是 XMind Ltd. 的注册商标
