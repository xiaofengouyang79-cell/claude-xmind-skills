---
name: xmind-generator-skill
description: >-
  生成高颜值、专业级 XMind 思维导图（.xmind）文件。设计驱动：内置「设计四原则（亲近/对比/重复/对齐）+ 视觉三要素（结构/配色/丰富度）」，
  自动彩虹分支配色、智能文字对比、色阶层级、曲线连线、图标与优先级标记、备注与任意深度层级。内置 13 套主题、覆盖 8 大设计流派
  （经典六色 + Mondo 海报 / 编辑杂志 / 野兽派 / 复古霓虹 / 手绘线稿 / 生成艺术 / 画廊色场），融合 canvas-design、qiaomu-mondo-poster-design、
  algorithmic-art、ian-xiaohei-illustrations、frontend-design 的设计 DNA。当用户需要制作思维导图、知识结构图、脑图、学习笔记、项目规划、
  读书总结、方案梳理、人物生平梳理、成长路径 / 学习路径，或提到 xmind / mindmap / 思维导图 / 脑图 / 心智图，即应使用本技能，
  即使用户没有明确说出"思维导图"这几个字。本技能已整合原 xmind-templates 的 30 套配色与模板体系。
---

# XMind Generator Skill（设计驱动版 v3）

用设计思维生成「一眼高级感」的 XMind 思维导图。核心不是画图，而是**把内容组织得清晰 + 好看**——清晰来自结构与对齐，好看来自配色与对比。

## 何时使用

- 制作任何思维导图 / 知识结构图 / 脑图 / 心智图
- 学习笔记、知识体系梳理、读书总结
- 项目规划、方案梳理、汇报提纲
- 人物生平、历史脉络、时间线回顾
- **成长路径 / 学习路径 / 知识地图**（如某位作者/某领域的体系梳理）
- 会议纪要、决策树、SWOT / 鱼骨等结构化分析

**不需要**：多人实时协作、复杂数据可视化图表、大量图片嵌入。

## 设计四原则（所有输出的总纲）

输出前用这四条自查，绝大多数"杂乱感"都来自没做好某一条：

1. **亲近**：一个分支 = 一个语义组，相关元素聚在一起。
2. **对比**：层级靠"明暗深浅"，分支靠"色相"，重点靠"加粗+标记"。
3. **重复**：同层级同字号同形状同边框；所有连线同曲线。
4. **对齐**：同级节点对齐，层级递进有序。

> 配色三要义（少用颜色 / 降低饱和度 / 智能对比）、结构选择、丰富度详见 `references/design-principles.md`；8 大设计流派的设计 DNA 详见 `references/design-styles.md`。

## 工作流

### Step 1 · 澄清需求（动手前必做）

若用户已给出完整大纲直接进 Step 2；否则快速对齐：主题 / 用途场景 / 核心模块（一级分支）/ 展开深度。

### Step 2 · 选主题与结构

**13 套主题 · 8 大设计家族**（详见 `assets/themes.json`，`--list-themes` 可查）：

| 家族 | 主题 | 设计来源 |
|------|------|----------|
| 经典六色 | `business` `fresh` `warm` `tech` `rose` `slate` | 内置 |
| 蒙多海报 | `mondo`（丝网复古双色）| qiaomu-mondo-poster-design |
| 编辑杂志 | `editorial`（白纸黑字+一个强调色）| frontend-design |
| 野兽派 | `brutalist`（纯原色·直角）| frontend-design |
| 复古霓虹 | `neon`（暗底霓虹）| frontend-design |
| 手绘线稿 | `ink`（线框无填充）| ian-xiaohei-illustrations |
| 生成艺术 | `spectrum`（色谱沿序涌现）| algorithmic-art |
| 画廊色场 | `gallery`（几何静默·原色色块）| canvas-design |

**结构类型**（`--structure`）：`map`（默认）、`logic-right`/`logic-left`、`org-chart`、`tree-right`/`tree-left`、`timeline`、`fishbone`。

### Step 3 · 设计内容结构

三种模式：
- **知识型**：概念 → 原理 → 方法 → 应用 → 案例 → 总结
- **人物生平**：人生轨迹 → 核心贡献 → 关键事件 → 风格特点 → 时代启示
- **成长/学习路径**：起点认知 → 分层进阶（由浅到深）→ 认知工具 → 践行路径

**组织规范**：一级分支 3–7 个、同级对称；每个分支一个语义主题；叶子是可理解的最小单元；标题长度 根 5–15 字 / 一级 3–10 字 / 叶子 5–25 字。

### Step 4 · 生成文件

输入是 JSON 大纲，输出 `.xmind`。节点可选字段：`title`（必填）、`children`、`emoji`、`marker`、`note`、`labels`、`color`。

```bash
py -3 scripts/generate_xmind.py \
  --title "根主题标题" \
  --theme spectrum \
  --structure map \
  --input content.json \
  --output "输出路径.xmind"

py -3 scripts/generate_xmind.py --list-themes   # 查主题
py -3 scripts/generate_xmind.py --verify "文件.xmind"   # 校验
```

> 无 `python` 时用 `py -3`；Python 3.x，无第三方依赖。

### Step 5 · 验证与交付

脚本自动输出节点总数与一级分支；确认是有效 `.xmind`、各分支带不同强调色、文字对比正确、XMind ≥ 8.0 可打开。

## 设计自动化的保证（脚本内置）

- **彩虹分支配色**：一级分支循环分配 7 色强调色，同分支子/叶继承该色系。
- **智能文字对比**：`readable_text()` 按 WCAG 对比度自动选白字/深字。
- **色阶层级**：主（深色块）→ 次（浅色 tint）→ 叶（近白 tint）→ 深（无填充）。
- **曲线连线**：统一 `curved`，主分支连线同分支色。
- **流派扩展**：主题可指定 `shape`（直角/圆角）与 `fill_mode`（solid 实心 / line 线稿）。

## 常见问题

- **打不开**：确认 `.xmind` 后缀、XMind ≥ 8.0。
- **换配色/结构**：改 `--theme` / `--structure` 重新生成。
- **加图片**：XMind 打开后选中主题 → 插入 → 图片（保持风格统一）。
- **导出 PNG/PDF**：XMind 打开 → 文件 → 导出。

## 参考资源

- `references/design-principles.md` — 设计四原则 + 视觉三要素（配色三要义、结构、丰富度）
- `references/design-styles.md` — 8 大设计流派设计 DNA 与主题选择速查
- `references/xmind-format.md` — XMind 8+ 格式与样式属性规范
- `assets/themes.json` — 13 套主题设计 token
- `scripts/generate_xmind.py` — 生成器源码
- `examples/` — 示例大纲（zhurongji.json 人物生平 / liurun.json 成长路径）
