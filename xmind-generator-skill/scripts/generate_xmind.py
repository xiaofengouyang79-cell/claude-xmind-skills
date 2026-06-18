#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XMind Generator - 专业级思维导图生成器
基于 XMind 8+ JSON 格式规范
"""

import json
import zipfile
import uuid
import os
import sys
from typing import List, Dict, Optional, Any

# ============================================================
# 主题配置
# ============================================================

THEMES = {
    "fresh": {
        "name": "清新自然",
        "root": {
            "svg:fill": "#059669",
            "fo:color": "#FFFFFF",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "18pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "main": {
            "svg:fill": "#D1FAE5",
            "fo:color": "#065F46",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "13pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "sub": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "11pt",
            "fo:color": "#374151",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#F9FAFB",
            "border-color": "#E5E7EB",
            "border-width": "1pt",
            "line-color": "#9CA3AF"
        },
        "leaf": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "10pt",
            "fo:color": "#6B7280",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#FFFFFF",
            "border-color": "#F3F4F6",
            "border-width": "1pt",
            "line-color": "#D1D5DB"
        }
    },
    "business": {
        "name": "商务专业",
        "root": {
            "svg:fill": "#1E40AF",
            "fo:color": "#FFFFFF",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "18pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "main": {
            "svg:fill": "#DBEAFE",
            "fo:color": "#1E40AF",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "13pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "sub": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "11pt",
            "fo:color": "#374151",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#F9FAFB",
            "border-color": "#E5E7EB",
            "border-width": "1pt",
            "line-color": "#9CA3AF"
        },
        "leaf": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "10pt",
            "fo:color": "#6B7280",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#FFFFFF",
            "border-color": "#F3F4F6",
            "border-width": "1pt",
            "line-color": "#D1D5DB"
        }
    },
    "warm": {
        "name": "温暖柔和",
        "root": {
            "svg:fill": "#DC2626",
            "fo:color": "#FFFFFF",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "18pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "main": {
            "svg:fill": "#FEE2E2",
            "fo:color": "#991B1B",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "13pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "sub": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "11pt",
            "fo:color": "#374151",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#F9FAFB",
            "border-color": "#E5E7EB",
            "border-width": "1pt",
            "line-color": "#9CA3AF"
        },
        "leaf": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "10pt",
            "fo:color": "#6B7280",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#FFFFFF",
            "border-color": "#F3F4F6",
            "border-width": "1pt",
            "line-color": "#D1D5DB"
        }
    },
    "tech": {
        "name": "科技冷调",
        "root": {
            "svg:fill": "#4F46E5",
            "fo:color": "#FFFFFF",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "18pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "main": {
            "svg:fill": "#E0E7FF",
            "fo:color": "#3730A3",
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "13pt",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "fo:font-weight": "bold"
        },
        "sub": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "11pt",
            "fo:color": "#374151",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#F9FAFB",
            "border-color": "#E5E7EB",
            "border-width": "1pt",
            "line-color": "#9CA3AF"
        },
        "leaf": {
            "fo:font-family": "Microsoft YaHei",
            "fo:font-size": "10pt",
            "fo:color": "#6B7280",
            "shape-class": "org.xmind.topicShape.roundedRect",
            "svg:fill": "#FFFFFF",
            "border-color": "#F3F4F6",
            "border-width": "1pt",
            "line-color": "#D1D5DB"
        }
    }
}


def gen_id() -> str:
    """生成唯一ID"""
    return uuid.uuid4().hex[:26]


def get_theme_style(level: str, theme: str = "business") -> Dict[str, str]:
    """获取主题样式"""
    return THEMES.get(theme, THEMES["business"]).get(level, {})


def create_topic(
    title: str,
    children: Optional[List[Dict]] = None,
    level: str = "leaf",
    theme: str = "business"
) -> Dict[str, Any]:
    """
    创建主题节点

    Args:
        title: 主题标题
        children: 子主题列表
        level: 层级 (root/main/sub/leaf)
        theme: 主题名称

    Returns:
        主题节点字典
    """
    topic = {
        "id": gen_id(),
        "class": "topic",
        "title": title,
        "style": {
            "properties": get_theme_style(level, theme)
        }
    }

    if children:
        topic["children"] = {"attached": children}

    return topic


def build_topics(
    items: List[Dict[str, Any]],
    level: str = "sub",
    theme: str = "business"
) -> List[Dict]:
    """
    递归构建主题树

    Args:
        items: 内容结构列表，每项包含 title 和可选的 children
        level: 当前层级
        theme: 主题名称

    Returns:
        主题节点列表
    """
    topics = []

    for item in items:
        title = item.get("title", "")
        children_data = item.get("children", [])

        # 确定子节点的层级
        if level == "main":
            child_level = "sub"
        elif level == "sub":
            child_level = "leaf"
        else:
            child_level = "leaf"

        # 递归构建子节点
        children = None
        if children_data:
            children = build_topics(children_data, child_level, theme)

        # 创建当前节点
        topic = create_topic(title, children, level, theme)
        topics.append(topic)

    return topics


def create_xmind_content(
    root_title: str,
    main_topics: List[Dict],
    theme: str = "business"
) -> List[Dict]:
    """
    创建完整的 XMind 内容结构

    Args:
        root_title: 根主题标题
        main_topics: 一级主题列表
        theme: 主题名称

    Returns:
        XMind content 结构
    """
    # 构建一级主题
    children = build_topics(main_topics, "main", theme)

    # 创建根主题
    root_topic = create_topic(root_title, children, "root", theme)

    # 创建 sheet
    content = [{
        "id": gen_id(),
        "class": "sheet",
        "rootTopic": root_topic
    }]

    return content


def create_metadata(title: str) -> Dict:
    """创建元数据"""
    return {
        "creator": {
            "name": title,
            "version": "1.0"
        }
    }


def create_manifest() -> Dict:
    """创建文件清单"""
    return {
        "file-entries": {
            "content.json": {},
            "metadata.json": {}
        }
    }


def save_xmind(
    content: List[Dict],
    metadata: Dict,
    manifest: Dict,
    output_path: str
) -> str:
    """
    保存为 XMind 文件

    Args:
        content: XMind 内容
        metadata: 元数据
        manifest: 文件清单
        output_path: 输出路径

    Returns:
        输出文件路径
    """
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 写入 ZIP 文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    return output_path


def verify_xmind(file_path: str) -> Dict[str, Any]:
    """
    验证 XMind 文件

    Args:
        file_path: 文件路径

    Returns:
        验证结果字典
    """
    result = {
        "valid": False,
        "file_size": 0,
        "root_title": "",
        "main_topics_count": 0,
        "main_topics": []
    }

    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            result["error"] = "文件不存在"
            return result

        # 检查文件大小
        result["file_size"] = os.path.getsize(file_path)

        # 读取 ZIP 文件
        with zipfile.ZipFile(file_path, 'r') as zf:
            # 检查必要文件
            file_list = zf.namelist()
            if "content.json" not in file_list:
                result["error"] = "缺少 content.json"
                return result

            # 读取内容
            content = json.loads(zf.read("content.json"))

            # 验证结构
            if not content or not isinstance(content, list):
                result["error"] = "content.json 格式错误"
                return result

            sheet = content[0]
            root_topic = sheet.get("rootTopic", {})

            result["root_title"] = root_topic.get("title", "")

            # 统计一级主题
            children = root_topic.get("children", {}).get("attached", [])
            result["main_topics_count"] = len(children)
            result["main_topics"] = [t.get("title", "") for t in children]

            result["valid"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def print_structure(content: List[Dict], indent: int = 0) -> None:
    """打印主题结构"""
    for sheet in content:
        root = sheet.get("rootTopic", {})
        print(f"{'  ' * indent}[Root] {root.get('title', '')}")
        _print_children(root, indent + 1)


def _print_children(topic: Dict, indent: int) -> None:
    """递归打印子主题"""
    children = topic.get("children", {}).get("attached", [])
    for child in children:
        print(f"{'  ' * indent}  |- {child.get('title', '')}")
        _print_children(child, indent + 1)


# ============================================================
# 命令行接口
# ============================================================

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="XMind 思维导图生成器")
    parser.add_argument("--title", type=str, help="根主题标题")
    parser.add_argument("--theme", type=str, default="business",
                       choices=["fresh", "business", "warm", "tech"],
                       help="视觉主题")
    parser.add_argument("--input", type=str, help="输入 JSON 文件路径")
    parser.add_argument("--output", type=str, help="输出 XMind 文件路径")
    parser.add_argument("--verify", type=str, help="验证 XMind 文件")
    parser.add_argument("--list-themes", action="store_true", help="列出可用主题")

    args = parser.parse_args()

    # 列出主题
    if args.list_themes:
        print("\n可用主题：")
        for key, theme in THEMES.items():
            print(f"  {key}: {theme['name']}")
        return

    # 验证文件
    if args.verify:
        result = verify_xmind(args.verify)
        print("\n验证结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 生成文件
    if not args.title or not args.input or not args.output:
        parser.error("生成文件需要 --title, --input, --output 参数")

    # 读取输入
    with open(args.input, 'r', encoding='utf-8') as f:
        main_topics = json.load(f)

    # 创建内容
    content = create_xmind_content(args.title, main_topics, args.theme)
    metadata = create_metadata(args.title)
    manifest = create_manifest()

    # 保存文件
    output_path = save_xmind(content, metadata, manifest, args.output)

    # 验证结果
    result = verify_xmind(output_path)

    print(f"\n[OK] XMind 文件已生成: {output_path}")
    print(f"   文件大小: {result['file_size']} bytes")
    print(f"   根主题: {result['root_title']}")
    print(f"   一级主题: {result['main_topics_count']} 个")
    print(f"\n主题结构：")
    print_structure(content)


if __name__ == "__main__":
    main()
