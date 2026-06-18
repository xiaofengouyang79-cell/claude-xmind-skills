#!/usr/bin/env python3
"""
XMind Generator Script
Converts xmind-skill JSON format to .xmind ZIP file.
Supports style themes, canvas themes, and all topic properties.

Usage:
    python create_xmind.py < input.json
    python create_xmind.py path/to/input.json
"""
import json
import zipfile
import uuid
import sys
import re
import os

def gen_id():
    return uuid.uuid4().hex[:26]

# 30 style palettes
PALETTES = {
    "deep-sea-blue":       {"root": "#1E40AF", "root_fg": "#FFFFFF", "main": "#DBEAFE", "main_fg": "#1E3A8A", "sub": "#EFF6FF", "sub_fg": "#1E40AF", "leaf": "#F8FAFC", "leaf_fg": "#6B748B", "line": "#93C5FD"},
    "emerald-green":       {"root": "#059669", "root_fg": "#FFFFFF", "main": "#D1FAE5", "main_fg": "#065F46", "sub": "#ECFDF5", "sub_fg": "#047857", "leaf": "#F0FDF4", "leaf_fg": "#6B7280", "line": "#6EE7B7"},
    "coral-red":           {"root": "#DC2626", "root_fg": "#FFFFFF", "main": "#FEE2E2", "main_fg": "#991B1B", "sub": "#FEF2F2", "sub_fg": "#B91C1C", "leaf": "#FFF5F5", "leaf_fg": "#6B7280", "line": "#FCA5A5"},
    "indigo-purple":       {"root": "#4F46E5", "root_fg": "#FFFFFF", "main": "#E0E7FF", "main_fg": "#3730A3", "sub": "#EEF2FF", "sub_fg": "#4338CA", "leaf": "#F5F7FF", "leaf_fg": "#6B7280", "line": "#A5B4FC"},
    "amber-orange":        {"root": "#D97706", "root_fg": "#FFFFFF", "main": "#FEF3C7", "main_fg": "#92400E", "sub": "#FFFBEB", "sub_fg": "#B45309", "leaf": "#FFFEF5", "leaf_fg": "#6B7280", "line": "#FCD34D"},
    "rose-pink":           {"root": "#BE185D", "root_fg": "#FFFFFF", "main": "#FCE7F3", "main_fg": "#9D174D", "sub": "#FDF2F8", "sub_fg": "#BE185D", "leaf": "#FFF5F9", "leaf_fg": "#6B7280", "line": "#F9A8D4"},
    "graphite-gray":       {"root": "#374151", "root_fg": "#FFFFFF", "main": "#F3F4F6", "main_fg": "#1F2937", "sub": "#F9FAFB", "sub_fg": "#374151", "leaf": "#FFFFFF", "leaf_fg": "#6B7280", "line": "#D1D5DB"},
    "sky-blue":            {"root": "#0284C7", "root_fg": "#FFFFFF", "main": "#BAE6FD", "main_fg": "#0C4A6E", "sub": "#E0F2FE", "sub_fg": "#0369A1", "leaf": "#F0F9FF", "leaf_fg": "#6B7280", "line": "#7DD3FC"},
    "olive-green":         {"root": "#65A30D", "root_fg": "#FFFFFF", "main": "#ECFCCB", "main_fg": "#3F6212", "sub": "#F7FEE7", "sub_fg": "#4D7C0F", "leaf": "#FEFCE8", "leaf_fg": "#6B7280", "line": "#BEF264"},
    "lavender-purple":     {"root": "#7C3AED", "root_fg": "#FFFFFF", "main": "#EDE9FE", "main_fg": "#5B21B6", "sub": "#F5F3FF", "sub_fg": "#6D28D9", "leaf": "#FAF5FF", "leaf_fg": "#6B7280", "line": "#C4B5FD"},
    "vermillion-orange":   {"root": "#EA580C", "root_fg": "#FFFFFF", "main": "#FFEDD5", "main_fg": "#9A3412", "sub": "#FFF7ED", "sub_fg": "#C2410C", "leaf": "#FFFBEB", "leaf_fg": "#6B7280", "line": "#FDBA74"},
    "celadon-blue":        {"root": "#0891B2", "root_fg": "#FFFFFF", "main": "#CFFAFE", "main_fg": "#155E75", "sub": "#ECFEFF", "sub_fg": "#0E7490", "leaf": "#F0FDFA", "leaf_fg": "#6B7280", "line": "#67E8F9"},
    "corn-yellow":         {"root": "#CA8A04", "root_fg": "#FFFFFF", "main": "#FEF9C3", "main_fg": "#854D0E", "sub": "#FEFCE8", "sub_fg": "#A16207", "leaf": "#FFFFF0", "leaf_fg": "#6B7280", "line": "#FDE047"},
    "eggplant-purple":     {"root": "#A21CAF", "root_fg": "#FFFFFF", "main": "#F5D0FE", "main_fg": "#86198F", "sub": "#FAE8FF", "sub_fg": "#A21CAF", "leaf": "#FDF4FF", "leaf_fg": "#6B7280", "line": "#E879F9"},
    "turquoise-green":     {"root": "#0D9488", "root_fg": "#FFFFFF", "main": "#99F6E4", "main_fg": "#115E59", "sub": "#CCFBF1", "sub_fg": "#134E4A", "leaf": "#F0FDFA", "leaf_fg": "#6B7280", "line": "#5EEAD4"},
    "wine-red":            {"root": "#7C2D12", "root_fg": "#FFFFFF", "main": "#FED7AA", "main_fg": "#9A3412", "sub": "#FFF7ED", "sub_fg": "#C2410C", "leaf": "#FFFBEB", "leaf_fg": "#6B7280", "line": "#FDBA74"},
    "cobalt-blue":         {"root": "#1D4ED8", "root_fg": "#FFFFFF", "main": "#BFDBFE", "main_fg": "#1E3A8A", "sub": "#DBEAFE", "sub_fg": "#1E40AF", "leaf": "#EFF6FF", "leaf_fg": "#6B7280", "line": "#93C5FD"},
    "moss-green":          {"root": "#15803D", "root_fg": "#FFFFFF", "main": "#BBF7D0", "main_fg": "#166534", "sub": "#DCFCE7", "sub_fg": "#15803D", "leaf": "#F0FDF4", "leaf_fg": "#6B7280", "line": "#86EFAC"},
    "brick-red":           {"root": "#B91C1C", "root_fg": "#FFFFFF", "main": "#FECACA", "main_fg": "#7F1D1D", "sub": "#FEE2E2", "sub_fg": "#991B1B", "leaf": "#FEF2F2", "leaf_fg": "#6B7280", "line": "#FCA5A5"},
    "dark-purple":         {"root": "#6B21A8", "root_fg": "#FFFFFF", "main": "#E9D5FF", "main_fg": "#581C87", "sub": "#F3E8FF", "sub_fg": "#6B21A8", "leaf": "#FAF5FF", "leaf_fg": "#6B7280", "line": "#C084FC"},
    "deep-cyan":           {"root": "#0E7490", "root_fg": "#FFFFFF", "main": "#A5F3FC", "main_fg": "#155E75", "sub": "#CFFAFE", "sub_fg": "#0E7490", "leaf": "#ECFEFF", "leaf_fg": "#6B7280", "line": "#67E8F9"},
    "golden-orange":       {"root": "#B45309", "root_fg": "#FFFFFF", "main": "#FDE68A", "main_fg": "#78350F", "sub": "#FEF3C7", "sub_fg": "#92400E", "leaf": "#FFFBEB", "leaf_fg": "#6B7280", "line": "#FCD34D"},
    "magenta":             {"root": "#DB2777", "root_fg": "#FFFFFF", "main": "#FBCFE8", "main_fg": "#9D174D", "sub": "#FCE7F3", "sub_fg": "#BE185D", "leaf": "#FDF2F8", "leaf_fg": "#6B7280", "line": "#F9A8D4"},
    "lead-gray":           {"root": "#4B5563", "root_fg": "#FFFFFF", "main": "#E5E7EB", "main_fg": "#1F2937", "sub": "#F3F4F6", "sub_fg": "#374151", "leaf": "#F9FAFB", "leaf_fg": "#6B7280", "line": "#D1D5DB"},
    "jade-green":          {"root": "#047857", "root_fg": "#FFFFFF", "main": "#A7F3D0", "main_fg": "#064E3B", "sub": "#D1FAE5", "sub_fg": "#065F46", "leaf": "#ECFDF5", "leaf_fg": "#6B7280", "line": "#6EE7B7"},
    "violet":              {"root": "#5B21B6", "root_fg": "#FFFFFF", "main": "#DDD6FE", "main_fg": "#4C1D95", "sub": "#EDE9FE", "sub_fg": "#5B21B6", "leaf": "#F5F3FF", "leaf_fg": "#6B7280", "line": "#A78BFA"},
    "copper-orange":       {"root": "#C2410C", "root_fg": "#FFFFFF", "main": "#FFEDD5", "main_fg": "#9A3412", "sub": "#FFF7ED", "sub_fg": "#C2410C", "leaf": "#FFFBEB", "leaf_fg": "#6B7280", "line": "#FB923C"},
    "navy-blue":           {"root": "#1E3A8A", "root_fg": "#FFFFFF", "main": "#BFDBFE", "main_fg": "#1E3A8A", "sub": "#DBEAFE", "sub_fg": "#1E40AF", "leaf": "#EFF6FF", "leaf_fg": "#6B7280", "line": "#60A5FA"},
    "grass-green":         {"root": "#16A34A", "root_fg": "#FFFFFF", "main": "#BBF7D0", "main_fg": "#166534", "sub": "#DCFCE7", "sub_fg": "#15803D", "leaf": "#F0FDF4", "leaf_fg": "#6B7280", "line": "#4ADE80"},
    "smoke-purple":        {"root": "#7E22CE", "root_fg": "#FFFFFF", "main": "#E9D5FF", "main_fg": "#581C87", "sub": "#F3E8FF", "sub_fg": "#6B21A8", "leaf": "#FAF5FF", "leaf_fg": "#6B7280", "line": "#C084FC"},
}

def get_palette(style_name):
    """Get palette by name or return default (vermillion-orange)."""
    if style_name and style_name in PALETTES:
        return PALETTES[style_name]
    return PALETTES["vermillion-orange"]

def make_style(palette, level):
    """Generate XMind style properties for a given level."""
    level_map = {
        0: ("root", "18pt", "bold"),
        1: ("main", "13pt", "bold"),
        2: ("sub", "11pt", "normal"),
        3: ("leaf", "10pt", "normal"),
    }
    key, font_size, font_weight = level_map.get(level, ("leaf", "10pt", "normal"))
    return {
        "svg:fill": palette[f"{key}"],
        "fo:color": palette[f"{key}_fg"],
        "fo:font-family": "Microsoft YaHei",
        "fo:font-size": font_size,
        "fo:font-weight": font_weight,
        "shape-class": "org.xmind.topicShape.roundedRect",
        "line-color": palette["line"],
        "line-width": "2pt"
    }

def convert_topic(src, palette, depth=0):
    """Convert xmind-skill topic to xmind content.json topic."""
    topic = {
        "id": gen_id(),
        "class": "topic",
        "title": src.get("title", "")
    }

    topic["style"] = {"properties": make_style(palette, depth)}

    # Notes: only keep for root (depth 0) and main branches (depth 1)
    if "notes" in src and src["notes"] and depth <= 1:
        topic["notes"] = {"plain": {"content": src["notes"]}}

    # Children
    if "children" in src and src["children"]:
        topic["children"] = {
            "attached": [convert_topic(c, palette, depth + 1) for c in src["children"]]
        }

    # Labels
    if "labels" in src:
        topic["labels"] = src["labels"]

    # Markers
    if "markers" in src:
        topic["markers"] = [{"markerId": m} for m in src["markers"]]

    # Structure class
    if "structureClass" in src:
        topic["structureClass"] = src["structureClass"]

    # Shape
    if "shape" in src:
        topic["style"]["properties"]["shape-class"] = src["shape"]

    return topic

def create_theme(palette):
    """Create sheet theme for auto-applying styles in XMind."""
    return {
        "id": gen_id(),
        "centralTopic": {
            "properties": {
                "svg:fill": palette["root"],
                "fo:color": palette["root_fg"],
                "fo:font-family": "Microsoft YaHei",
                "fo:font-size": "18pt",
                "fo:font-weight": "bold",
                "shape-class": "org.xmind.topicShape.roundedRect"
            }
        },
        "mainTopic": {
            "properties": {
                "svg:fill": palette["main"],
                "fo:color": palette["main_fg"],
                "fo:font-family": "Microsoft YaHei",
                "fo:font-size": "13pt",
                "fo:font-weight": "bold",
                "shape-class": "org.xmind.topicShape.roundedRect"
            }
        },
        "subTopic": {
            "properties": {
                "svg:fill": palette["sub"],
                "fo:color": palette["sub_fg"],
                "fo:font-family": "Microsoft YaHei",
                "fo:font-size": "11pt"
            }
        },
        "floatingTopic": {
            "properties": {
                "svg:fill": palette["leaf"],
                "fo:color": palette["leaf_fg"],
                "fo:font-family": "Microsoft YaHei",
                "fo:font-size": "10pt"
            }
        }
    }

def main():
    # Read input
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    output_path = data.get("path", "output.xmind")
    style = data.get("style", "vermillion-orange")
    palette = get_palette(style)

    sheets = []
    for sheet in data.get("sheets", []):
        root = sheet.get("rootTopic", {})
        structure = sheet.get("structureClass", "org.xmind.ui.map.clockwise")

        root_topic = convert_topic(root, palette, 0)
        root_topic["structureClass"] = structure

        sheet_data = {
            "id": gen_id(),
            "class": "sheet",
            "title": sheet.get("title", "Sheet 1"),
            "rootTopic": root_topic,
            "theme": create_theme(palette)
        }

        # Relationships
        if "relationships" in sheet:
            sheet_data["relationships"] = []
            for rel in sheet["relationships"]:
                r = {
                    "id": gen_id(),
                    "class": "relationship",
                    "title": rel.get("title", ""),
                    "source": {"topicId": rel["sourceTitle"]},
                    "end1": {"topicId": rel["sourceTitle"]},
                    "end2": {"topicId": rel["targetTitle"]}
                }
                if rel.get("shape"):
                    r["shape"] = {"type": rel["shape"]}
                sheet_data["relationships"].append(r)

        # Free positioning
        if sheet.get("freePositioning"):
            sheet_data["freePositioning"] = True
            sheet_data["topicPositioning"] = "free"

        sheets.append(sheet_data)

    content = sheets
    metadata = {"creator": {"name": "XMind Generator", "version": "3.0"}}
    manifest = {"file-entries": {"content.json": {}, "metadata.json": {}}}

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"OK: {output_path}")

if __name__ == "__main__":
    main()
