#!/usr/bin/env python3
"""字节内部基础设施框架导航查询工具"""
import json
import sys
import os

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_frameworks(data, query):
    """模糊搜索框架：匹配 name、aliases、tags、category name、description"""
    query_lower = query.lower().strip()
    results = []
    
    # 建立 category id -> name 的映射
    cat_map = {c['id']: c for c in data['categories']}
    
    for fw in data['frameworks']:
        score = 0
        # 精确匹配 name
        if fw['name'].lower() == query_lower:
            score = 100
        # 精确匹配 alias
        elif any(a.lower() == query_lower for a in fw.get('aliases', [])):
            score = 90
        # name 包含
        elif query_lower in fw['name'].lower():
            score = 80
        # alias 包含
        elif any(query_lower in a.lower() for a in fw.get('aliases', [])):
            score = 70
        # tag 匹配
        elif any(query_lower in t.lower() for t in fw.get('tags', [])):
            score = 50
        # category name 匹配
        elif query_lower in cat_map.get(fw['category'], {}).get('name', '').lower():
            score = 40
        # description 包含
        elif query_lower in fw.get('description', '').lower():
            score = 30
        
        if score > 0:
            results.append((score, fw))
    
    results.sort(key=lambda x: -x[0])
    return [r[1] for r in results]

def get_category_frameworks(data, category_query):
    """按分类获取框架列表"""
    cat_query = category_query.lower().strip()
    matched_cat_ids = []
    
    for cat in data['categories']:
        if cat_query in cat['name'].lower() or cat_query in cat['id'].lower():
            matched_cat_ids.append(cat['id'])
    
    if not matched_cat_ids:
        return None, []
    
    cat_map = {c['id']: c for c in data['categories']}
    results = {}
    for cat_id in matched_cat_ids:
        results[cat_id] = {
            'category': cat_map[cat_id],
            'frameworks': [fw for fw in data['frameworks'] if fw['category'] == cat_id]
        }
    return results

def format_framework_card(fw, cat_map):
    """格式化单个框架卡片"""
    cat = cat_map.get(fw['category'], {})
    lines = []
    lines.append(f"### {cat.get('icon', '📦')} {fw['name']}")
    lines.append(f"")
    lines.append(f"**分类**: {cat.get('name', fw['category'])}  ")
    lines.append(f"**简介**: {fw['description']}")
    lines.append(f"")
    
    # 链接
    has_todo = False
    lines.append("**文档链接**:")
    lines.append("")
    for link in fw.get('links', []):
        if link['url'] == 'TODO':
            lines.append(f"- {link['title']}: ⚠️ `待补充`")
            has_todo = True
        else:
            lines.append(f"- [{link['title']}]({link['url']})")
    lines.append("")
    
    # 标签
    if fw.get('tags'):
        lines.append(f"**标签**: {' '.join(['`' + t + '`' for t in fw['tags']])}")
        lines.append("")
    
    if has_todo:
        lines.append("> 💡 部分链接待补充，请使用「添加链接」功能更新对应的内网文档地址")
        lines.append("")
    
    return '\n'.join(lines)

def format_full_nav(data):
    """格式化完整导航"""
    cat_map = {c['id']: c for c in data['categories']}
    lines = []
    lines.append("# 🗺️ 字节内部基础设施框架导航")
    lines.append("")
    lines.append(f"> 共 {len(data['frameworks'])} 个框架，{len(data['categories'])} 个分类 | 版本 {data['meta']['version']} | 更新于 {data['meta']['last_updated']}")
    lines.append("")
    
    for cat in data['categories']:
        fws = [fw for fw in data['frameworks'] if fw['category'] == cat['id']]
        if not fws:
            continue
        
        lines.append(f"## {cat['icon']} {cat['name']}")
        lines.append(f"_{cat['description']}_")
        lines.append("")
        lines.append("| 框架 | 简介 | 文档 |")
        lines.append("|------|------|------|")
        
        for fw in fws:
            link_parts = []
            for link in fw.get('links', []):
                if link['url'] == 'TODO':
                    link_parts.append(f"{link['title']}(待补充)")
                else:
                    link_parts.append(f"[{link['title']}]({link['url']})")
            links_str = " · ".join(link_parts) if link_parts else "-"
            lines.append(f"| **{fw['name']}** | {fw['description'][:50]}{'...' if len(fw['description'])>50 else ''} | {links_str} |")
        
        lines.append("")
    
    return '\n'.join(lines)

def format_category_view(results, data):
    """格式化分类视图"""
    cat_map = {c['id']: c for c in data['categories']}
    lines = []
    
    for cat_id, info in results.items():
        cat = info['category']
        fws = info['frameworks']
        
        lines.append(f"## {cat['icon']} {cat['name']}")
        lines.append(f"_{cat['description']}_")
        lines.append("")
        
        for fw in fws:
            lines.append(format_framework_card(fw, cat_map))
    
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 3:
        print("Usage: python nav_query.py <json_path> <command> [args]")
        print("Commands: search, category, all, add")
        sys.exit(1)
    
    json_path = sys.argv[1]
    command = sys.argv[2]
    data = load_data(json_path)
    cat_map = {c['id']: c for c in data['categories']}
    
    if command == 'all':
        print(format_full_nav(data))
    
    elif command == 'search' and len(sys.argv) > 3:
        query = ' '.join(sys.argv[3:])
        results = search_frameworks(data, query)
        if results:
            if len(results) == 1:
                print(format_framework_card(results[0], cat_map))
            else:
                print(f"找到 {len(results)} 个匹配结果：\n")
                for fw in results:
                    print(format_framework_card(fw, cat_map))
                    print("---\n")
        else:
            print(f"未找到与「{query}」相关的框架。\n")
            print("💡 提示：")
            print("- 试试用框架的英文名或缩写搜索")
            print("- 输入分类名（如「存储」「消息队列」）浏览该类别")
            print("- 输入「全部」查看完整导航")
    
    elif command == 'category' and len(sys.argv) > 3:
        query = ' '.join(sys.argv[3:])
        results = get_category_frameworks(data, query)
        if results:
            print(format_category_view(results, data))
        else:
            print(f"未找到「{query}」相关的分类。\n")
            print("可用分类：")
            for cat in data['categories']:
                print(f"  {cat['icon']} {cat['name']}")
    
    elif command == 'add':
        # 输出当前数据供编辑
        print(json.dumps(data, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
