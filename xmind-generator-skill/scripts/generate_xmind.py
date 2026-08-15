#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XMind Pro 生成器 — 设计驱动的思维导图生成器
============================================
基于 XMind 8+ JSON 格式规范，内建「设计四原则 + 三要素」：

  设计四原则：亲近 · 对比 · 重复 · 对齐
  视觉三要素：结构 · 配色 · 丰富度

核心改进（相比 v1）：
  1. 彩虹分支配色 —— 每条一级分支自动分配不同强调色，一眼高级感
  2. 智能文字对比 —— 根据填充色明度自动选择黑/白文字（WCAG 4.5:1）
  3. 色阶层级 —— 主/次/叶三级用「同色系深浅」递进，告别千篇一律的灰
  4. 曲线连接线 + 分支配色连线 —— 结构与配色统一
  5. 支持图标、优先级标记、备注、外框分组，任意深度层级
"""

import json
import zipfile
import uuid
import os
import sys
from typing import List, Dict, Optional, Any, Tuple

# ============================================================
# 结构类型映射（XMind 8 结构类名）
# ============================================================

STRUCTURES = {
    "map": "org.xmind.ui.map.unbalanced",            # 默认平衡图（放射）
    "logic-right": "org.xmind.ui.logic.right",       # 逻辑图（右）
    "logic-left": "org.xmind.ui.logic.left",         # 逻辑图（左）
    "org-chart": "org.xmind.ui.org-chart.down",      # 组织结构图
    "tree-right": "org.xmind.ui.tree.right",         # 树形图（右）
    "tree-left": "org.xmind.ui.tree.left",           # 树形图（左）
    "timeline": "org.xmind.ui.timeline.horizontal",  # 时间轴
    "fishbone": "org.xmind.ui.fishbone.rightHeaded", # 鱼骨图
}

# 常用优先级/状态标记（映射到 XMind 8 合法 markerId）
MARKER_ALIASES = {
    "priority-1": "priority-1", "priority-2": "priority-2", "priority-3": "priority-3",
    "priority-4": "priority-4", "priority-5": "priority-5", "priority-6": "priority-6",
    "p1": "priority-1", "p2": "priority-2", "p3": "priority-3",
    "star": "star-red", "starred": "star-red",
    "flag": "flag-red", "flag-red": "flag-red", "flag-orange": "flag-orange",
    "flag-green": "flag-green", "flag-blue": "flag-blue",
    "todo": "task-start", "task-start": "task-start", "task-done": "task-done",
    "arrow-up": "arrow-up", "arrow-down": "arrow-down", "arrow-right": "arrow-right",
    "smile": "smiley-smile", "month": "month-jan",
}

DEFAULT_THEME = {
    "root": "#1E3A8A",
    "paper": "#F8FAFC",
    "accents": ["#2563EB", "#0EA5E9", "#7C3AED", "#DB2777", "#F59E0B", "#10B981", "#475569"],
}

FONT_FAMILY = "Microsoft YaHei"
FONT_SIZES = {"root": "20pt", "main": "14pt", "sub": "12pt", "leaf": "11pt", "deep": "10pt"}
LINE_CLASS = "org.xmind.branchConnection.curved"
INK = "#334155"          # 正文深灰（浅底上的正文色）
INK_MUTED = "#475569"    # 深层节点文字色


# ============================================================
# 颜色工具
# ============================================================

def _hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02X}{:02X}{:02X}".format(max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def tint(hex_color: str, ratio: float) -> str:
    """向白色混合：ratio 越大越接近白（0=原色, 1=纯白）"""
    r, g, b = _hex_to_rgb(hex_color)
    r = int(r + (255 - r) * ratio)
    g = int(g + (255 - g) * ratio)
    b = int(b + (255 - b) * ratio)
    return _rgb_to_hex(r, g, b)


def darken(hex_color: str, factor: float) -> str:
    """乘系数压暗：factor 越小越暗（0=黑, 1=原色）"""
    r, g, b = _hex_to_rgb(hex_color)
    return _rgb_to_hex(int(r * factor), int(g * factor), int(b * factor))


def luminance(hex_color: str) -> float:
    """相对亮度 0~1（sRGB）"""
    r, g, b = _hex_to_rgb(hex_color)
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """WCAG 对比度 (L1+0.05)/(L2+0.05)，L1 为较亮者"""
    lf, lb = luminance(fg), luminance(bg)
    lighter, darker = (lf, lb) if lf >= lb else (lb, lf)
    return (lighter + 0.05) / (darker + 0.05)


def readable_text(hex_color: str) -> str:
    """智能配色：根据背景明度自动选择对比度更高的文字色（白 / 深）"""
    white, dark = "#FFFFFF", "#1F2937"
    return white if contrast_ratio(white, hex_color) >= contrast_ratio(dark, hex_color) else dark


def normalize_color(c: str) -> Optional[str]:
    if not c:
        return None
    c = c.strip()
    if c.startswith("#") and len(c.lstrip("#")) in (3, 6):
        return c
    return None


# ============================================================
# 主题加载
# ============================================================

def load_themes() -> Dict[str, Any]:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "assets", "themes.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"themes": {"business": DEFAULT_THEME}, "font_sizes": FONT_SIZES}


# ============================================================
# 样式构建
# ============================================================

def build_style(theme: Dict[str, Any], level: str, branch_idx: int,
                accent: str, overrides: Optional[Dict] = None) -> Dict[str, str]:
    """按层级 + 分支强调色构建节点样式（对比/重复/对齐原则落地）

    支持主题级 shape（直角/圆角）与 fill_mode（solid 实心 / line 线稿无填充），
    以承载不同设计流派（野兽派直角、手绘线稿等）的视觉 DNA。
    """
    overrides = overrides or {}
    o_fill = normalize_color(overrides.get("fill") or overrides.get("color"))
    shape = theme.get("shape", "org.xmind.topicShape.roundedRect")
    line_mode = theme.get("fill_mode", "solid") == "line"

    def base(weight: str, size_key: str) -> Dict[str, str]:
        return {
            "fo:font-family": FONT_FAMILY,
            "fo:font-size": FONT_SIZES[size_key],
            "fo:font-weight": weight,
            "shape-class": shape,
            "line-class": LINE_CLASS,
        }

    if level == "root":
        fill = o_fill or theme.get("root", DEFAULT_THEME["root"])
        style = base("bold", "root")
        style.update({
            "svg:fill": fill,
            "fo:color": readable_text(fill),
            "line-width": "3pt",
        })
    elif level == "main":
        style = base("bold", "main")
        style.update({"line-width": "2pt", "line-color": accent})
        if line_mode:
            style.update({
                "fo:color": darken(accent, 0.45),
                "border-color": accent,
                "border-width": "2pt",
            })
        else:
            fill = o_fill or accent
            style.update({"svg:fill": fill, "fo:color": readable_text(fill)})
    elif level == "sub":
        style = base("bold", "sub")
        style.update({"line-width": "1pt", "line-color": tint(accent, 0.45)})
        if line_mode:
            style.update({
                "fo:color": darken(accent, 0.5),
                "border-color": tint(accent, 0.4),
                "border-width": "1pt",
            })
        else:
            style.update({
                "svg:fill": o_fill or tint(accent, 0.88),
                "fo:color": darken(accent, 0.55),
                "border-color": tint(accent, 0.55),
                "border-width": "1pt",
            })
    elif level == "leaf":
        style = base("normal", "leaf")
        style.update({"line-width": "1pt", "line-color": tint(accent, 0.72)})
        if line_mode:
            style.update({
                "fo:color": INK,
                "border-color": tint(accent, 0.7),
                "border-width": "1pt",
            })
        else:
            style.update({
                "svg:fill": o_fill or tint(accent, 0.97),
                "fo:color": INK,
                "border-color": tint(accent, 0.72),
                "border-width": "1pt",
            })
    else:  # deep：不再用填充，仅文字，避免视觉噪声
        style = base("normal", "deep")
        style.update({
            "fo:color": INK_MUTED,
            "line-width": "1pt",
            "line-color": tint(accent, 0.82),
        })

    # 允许用户对单个节点覆盖关键样式
    for key in ("font-size", "font-weight", "font-family"):
        if overrides.get(key):
            style["fo:" + key] = overrides[key]
    return style


# ============================================================
# 节点构建
# ============================================================

def gen_id() -> str:
    return uuid.uuid4().hex[:26]


def _level_name(depth: int) -> str:
    if depth <= 0:
        return "root"
    if depth == 1:
        return "main"
    if depth == 2:
        return "sub"
    if depth == 3:
        return "leaf"
    return "deep"


def build_topic(item: Dict[str, Any], theme: Dict[str, Any],
                depth: int, branch_idx: int, accent: str) -> Dict[str, Any]:
    title = str(item.get("title", ""))
    emoji = item.get("emoji")
    if emoji:
        title = f"{emoji} {title}".strip()

    level = _level_name(depth)
    topic: Dict[str, Any] = {
        "id": gen_id(),
        "class": "topic",
        "title": title,
        "style": {"properties": build_style(theme, level, branch_idx, accent, item)},
    }

    # 优先级/状态标记
    marker = item.get("marker")
    if marker:
        mid = MARKER_ALIASES.get(marker, marker)
        topic["markers"] = [{"markerId": mid}]

    # 备注
    note = item.get("note")
    if note:
        topic["notes"] = {"plain": {"content": str(note)}}

    # 标签
    labels = item.get("labels")
    if labels:
        topic["labels"] = [str(x) for x in labels]

    # 子节点（同分支继承同一强调色）
    children = item.get("children") or []
    if children:
        child_topics = []
        for ci, child in enumerate(children):
            # 一级分支：每个主分支用不同强调色（彩虹分支）
            if depth == 0:
                child_idx = ci
                child_accent = theme["accents"][ci % len(theme["accents"])]
            else:
                child_idx = branch_idx
                child_accent = accent
            child_topics.append(build_topic(child, theme, depth + 1, child_idx, child_accent))
        topic["children"] = {"attached": child_topics}

    return topic


def create_content(root_title: str, main_topics: List[Dict],
                   theme: Dict[str, Any], structure: Optional[str] = None) -> List[Dict]:
    root_emoji = None
    root_topic = build_topic({"title": root_title}, theme, 0, 0, theme.get("root", DEFAULT_THEME["root"]))

    # 一级分支
    root_topic["children"] = {"attached": []}
    for ci, item in enumerate(main_topics):
        accent = theme["accents"][ci % len(theme["accents"])]
        root_topic["children"]["attached"].append(
            build_topic(item, theme, 1, ci, accent)
        )

    # 可选结构（默认不写，保持最兼容；用户指定时写入）
    if structure and structure != "map":
        sc = STRUCTURES.get(structure, structure)
        root_topic["structure-class"] = sc

    sheet: Dict[str, Any] = {
        "id": gen_id(),
        "class": "sheet",
        "title": root_title,
        "rootTopic": root_topic,
    }

    # 画布背景（纸张色，柔和统一）
    paper = theme.get("paper")
    if paper:
        sheet["theme"] = {
            "id": gen_id(),
            "class": "theme",
            "title": "XMind Pro",
            "map": {
                "svg:fill": paper,
            },
        }

    return [sheet]


# ============================================================
# 打包 / 校验
# ============================================================

def save_xmind(content: List[Dict], title: str, output_path: str) -> str:
    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)

    metadata = {
        "creator": {
            "name": "XMind Pro Generator",
            "version": "2.0",
            "title": title,
        }
    }
    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
            "manifest.json": {},
        }
    }

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    return output_path


def verify_xmind(file_path: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {"valid": False}
    try:
        if not os.path.exists(file_path):
            result["error"] = "文件不存在"
            return result
        result["file_size"] = os.path.getsize(file_path)
        with zipfile.ZipFile(file_path, "r") as zf:
            names = zf.namelist()
            if "content.json" not in names:
                result["error"] = "缺少 content.json"
                return result
            content = json.loads(zf.read("content.json"))
        sheet = content[0]
        root = sheet["rootTopic"]
        mains = root.get("children", {}).get("attached", [])

        # 递归统计节点
        def count(t):
            n = 1
            for c in t.get("children", {}).get("attached", []):
                n += count(c)
            return n

        result.update({
            "valid": True,
            "root_title": root.get("title", ""),
            "main_branches": [t.get("title", "") for t in mains],
            "main_count": len(mains),
            "total_nodes": count(root),
        })
    except Exception as e:
        result["error"] = str(e)
    return result


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    p = argparse.ArgumentParser(description="XMind Pro 思维导图生成器（设计驱动）")
    p.add_argument("--title", help="根主题标题")
    p.add_argument("--theme", default="business", help="视觉主题（见 --list-themes）")
    p.add_argument("--structure", default="map", help="结构类型：" + "/".join(STRUCTURES.keys()))
    p.add_argument("--input", help="输入内容 JSON 文件")
    p.add_argument("--output", help="输出 .xmind 路径")
    p.add_argument("--list-themes", action="store_true", help="列出可用主题")
    p.add_argument("--verify", help="校验已有 .xmind 文件")
    args = p.parse_args()

    themes = load_themes()["themes"]

    if args.list_themes:
        families = [
            ("classic", "经典六色"),
            ("mondo-poster", "蒙多海报 · qiaomu-mondo-poster-design"),
            ("editorial", "编辑杂志 · frontend-design"),
            ("brutalist", "野兽派 · frontend-design"),
            ("neon", "复古霓虹 · frontend-design"),
            ("hand-drawn", "手绘线稿 · ian-xiaohei-illustrations"),
            ("generative", "生成艺术 · algorithmic-art"),
            ("gallery", "画廊色场 · canvas-design"),
        ]
        print("\n可用主题（按设计家族）：")
        for fam, label in families:
            members = [(k, t) for k, t in themes.items() if t.get("family") == fam]
            if not members:
                continue
            print(f"\n  【{label}】")
            for k, t in members:
                print(f"    {k:12s} {t.get('icon','')} {t.get('name','')}")
        print("\n可用结构：", ", ".join(STRUCTURES.keys()))
        return

    if args.verify:
        print(json.dumps(verify_xmind(args.verify), ensure_ascii=False, indent=2))
        return

    if not (args.title and args.input and args.output):
        p.error("生成需要 --title / --input / --output")

    theme = themes.get(args.theme, themes.get("business"))
    with open(args.input, "r", encoding="utf-8") as f:
        main_topics = json.load(f)

    content = create_content(args.title, main_topics, theme, args.structure)
    save_xmind(content, args.title, args.output)
    result = verify_xmind(args.output)

    print(f"\n[OK] XMind 已生成: {args.output}")
    print(f"  主题: {theme.get('name')} | 结构: {args.structure}")
    print(f"  大小: {result.get('file_size', 0)} bytes | 节点: {result.get('total_nodes', 0)} 个")
    print(f"  一级分支 ({result.get('main_count', 0)}):")
    for b in result.get("main_branches", []):
        print(f"    · {b}")


if __name__ == "__main__":
    main()
