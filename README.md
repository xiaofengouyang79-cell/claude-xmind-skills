# Claude XMind Skills

三套 Claude Code XMind 思维导图技能包，帮助你在 Claude Code 中快速创建专业的 XMind 思维导图。

## 📦 包含的技能

| 技能 | 说明 | 核心功能 |
|------|------|----------|
| **xmind** | 主技能 — 通过 JSON 结构创建 .xmind 文件 | 基础思维导图、流程图、甘特图、逻辑图 |
| **xmind-generator-skill** | 增强生成器 — 支持更多高级格式 | 主题样式、模板系统、高级布局 |
| **xmind-templates** | 模板与配色库 — 30 套配色 + 6 类场景模板 | 配色速查、场景模板、风格推荐 |

## 🚀 安装方法

将这三个文件夹复制到你的 Claude Code skills 目录：

```bash
# Linux / macOS
cp -r xmind ~/.claude/skills/
cp -r xmind-generator-skill ~/.claude/skills/
cp -r xmind-templates ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse xmind "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse xmind-generator-skill "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse xmind-templates "$env:USERPROFILE\.claude\skills\"
```

## 📖 使用方法

在 Claude Code 中输入 `/xmind` 即可启动，然后告诉 Claude 你想创建的思维导图内容。

### 支持的类型

- 📚 **读书笔记** — 章节结构和要点梳理
- 🎓 **课程/教案** — 教学内容、知识点
- 📊 **产品分析** — 竞品对比、功能拆解
- 🗂️ **项目规划** — 任务分解、甘特图
- 🔄 **流程图** — 算法逻辑、决策流程
- 🏢 **组织架构** — 团队结构、角色分工
- 💡 **头脑风暴** — 创意发散、问题分析

### 30 套配色方案

| 场景 | 推荐风格 | 主色 |
|------|----------|------|
| 数码/科技 | 靛蓝紫、深青、烟紫 | `#4F46E5` `#0E7490` `#7E22CE` |
| 商务/正式 | 深海蓝、钴蓝、石墨灰 | `#1E40AF` `#1D4ED8` `#374151` |
| 学习/知识 | 天空蓝、翡翠绿、松石绿 | `#0284C7` `#059669` `#0D9488` |
| 活力/运动 | 朱砂橙、琥珀橙、珊瑚红 | `#EA580C` `#D97706` `#DC2626` |
| 创意/艺术 | 薰衣草紫、暗紫、茄紫红 | `#7C3AED` `#6B21A8` `#A21CAF` |

## ⚙️ 依赖

- Python 3.6+
- XMind 软件（用于打开生成的 .xmind 文件）

## 📄 许可

MIT License

## 🙏 致谢

- 基于 [apeyroux/mcp-xmind](https://github.com/apeyroux/mcp-xmind) 的 xmind skill
- XMind 是 XMind Ltd. 的注册商标
