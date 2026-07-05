#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《黎明之后》卡牌数据提取脚本
从5个MD图鉴文件中提取所有卡牌数据，生成统一的JSON数据库
"""

import re
import json
import os

BASE_DIR = r"C:\Users\80526\WorkBuddy\2026-06-05-15-49-56"
OUTPUT = os.path.join(BASE_DIR, "黎明之后_卡牌数据库.json")

WHISPERS_FILE = "黎明之后_怪谈卡图鉴.md"
COUNTERMEASURES_FILE = "黎明之后_反击卡图鉴.md"
RULES_FILE = "黎明之后_规则卡图鉴.md"
CHARACTERS_FILE = "黎明之后_角色卡图鉴.md"
GOALS_FILE = "黎明之后_个人目的卡图鉴.md"


def read_file(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def clean_text(t):
    """清理多行文本，合并为单行"""
    if not t:
        return ""
    t = re.sub(r'\n+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


# ============================================================
# 1. 怪谈卡解析
# ============================================================
def parse_whispers(text):
    """解析怪谈卡图鉴，返回卡牌列表"""
    cards = []
    
    # 分割策略：按 --- 分割，然后检查每段是否包含**等级**：来识别卡牌
    # 非卡牌章节关键词
    skip_keywords = [
        '设计原则', '等级体系', '待设计卡牌', '更新日志',
        '怪谈卡图鉴', '使用说明', '物理区域', '核心机制',
        '旧体系', '新体系', '等级命名', '设计状态'
    ]
    
    sections = text.split('\n---\n')
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # 找到 ## 标题
        heading_match = re.search(r'##\s+(.+)', section)
        if not heading_match:
            continue
        
        name = heading_match.group(1).strip()
        
        # 跳过低级标题（### 和 ####）
        # 检查是否是真正的 ## 级别标题（前面没有更多 #）
        lines = section.split('\n')
        for line in lines:
            if line.startswith('## ') and not line.startswith('### '):
                name = line[3:].strip()
                break
        
        # 再次确认是 ## 级别
        if heading_match and name:
            # 检查是否是 card section
            has_level = '**等级**' in section or '**所属牌库**' in section
            
            # 跳过非卡牌章节
            skip = False
            for kw in skip_keywords:
                if kw in section[:200]:
                    skip = True
                    break
            if skip:
                continue
            
            if not has_level:
                continue
            
            # 提取字段
            def extract_field_whisper(field_name):
                """从怪谈卡section中提取字段值"""
                # 匹配 **field_name**：content 或 **field_name**: content
                pattern = rf'\*\*{field_name}\*\*[：:]\s*(.*?)(?=\n\*\*|\n```|\Z)'
                match = re.search(pattern, section, re.DOTALL)
                if match:
                    val = match.group(1).strip()
                    # 如果以 ``` 开头（完整文本块），跳过
                    if val.startswith('```'):
                        return ""
                    return val
                return ""
            
            level = clean_text(extract_field_whisper('等级'))
            activation = clean_text(extract_field_whisper('激活条件'))
            trigger = clean_text(extract_field_whisper('发动条件'))
            effect = clean_text(extract_field_whisper('效果'))
            design = clean_text(extract_field_whisper('设计理念') or extract_field_whisper('设计意图'))
            
            cards.append({
                "id": "",
                "name": name,
                "type": "whisper",
                "level": level,
                "activation_condition": activation,
                "trigger_condition": trigger,
                "effect": effect,
                "flavor": design[:100] if design else "",
                "status": "active"
            })
    
    # 按文档顺序分配 ID
    for i, card in enumerate(cards, 1):
        card["id"] = f"w_{i:03d}"
    
    return cards

# ============================================================
# 2. 反击卡解析
# ============================================================
def parse_countermeasures(text):
    """解析反击卡图鉴，返回卡牌列表"""
    cards = []
    
    # 找到"六、卡牌图鉴"章节之后的全部内容
    catalog_start = text.find('## 六、卡牌图鉴')
    if catalog_start == -1:
        catalog_start = text.find('六、卡牌图鉴')
    if catalog_start == -1:
        catalog_start = 0
    
    catalog_text = text[catalog_start:]
    
    # 移除"七、设计意图汇总"及之后的内容
    end_marker = text.find('## 七、设计意图汇总')
    if end_marker > catalog_start:
        catalog_text = text[catalog_start:end_marker]
    
    # 按小节分割（6.1, 6.2, 6.3, 6.4）
    subsections = re.split(r'\n### 6\.\d', catalog_text)
    
    # 移除第一个空元素或前言
    if subsections and '基础等级' not in subsections[0].split('\n')[0]:
        # 第一个可能包含6.1的标题，尝试修复
        pass
    
    # 直接使用正则匹配所有卡牌：#### X.X.X 【卡名】
    card_pattern = re.compile(
        r'####\s+\d+\.\d+(?:\.\d+)?\s+\*?\*?【(.+?)】\*?\*?\s*\n(.*?)(?=\n####\s+\d+\.|\n###\s+6\.|\n##\s+七、|\Z)',
        re.DOTALL
    )
    
    matches = card_pattern.findall(catalog_text)
    
    for name, body in matches:
        name = name.strip()
        
        def extract_field_cm(field_name):
            pattern = rf'\*\*{field_name}\*\*[：:]\s*(.*?)(?=\n\*\*|\n```|\n####|\n###|\Z)'
            match = re.search(pattern, body, re.DOTALL)
            if match:
                return match.group(1).strip()
            return ""
        
        level = clean_text(extract_field_cm('等级'))
        activation = clean_text(extract_field_cm('激活条件'))
        trigger = clean_text(extract_field_cm('发动条件'))
        effect = clean_text(extract_field_cm('效果'))
        cost = clean_text(extract_field_cm('攻击条件') or extract_field_cm('使用时机'))
        design = clean_text(extract_field_cm('设计师思路') or extract_field_cm('设计师说明') or extract_field_cm('设计意图') or extract_field_cm('设计师思路'))
        
        # 从触发条件中提取cost信息 (如果包含 "（cost）")
        if not cost:
            cost_match = re.search(r'（cost）', trigger)
            if cost_match:
                cost = "需支付cost（见发动条件）"
        
        cards.append({
            "id": "",
            "name": name,
            "type": "countermeasure",
            "level": level,
            "activation_condition": activation,
            "trigger_condition": trigger,
            "effect": effect,
            "cost": cost,
            "flavor": design[:100] if design else "",
            "status": "active"
        })
    
    # 按文档顺序分配 ID
    for i, card in enumerate(cards, 1):
        card["id"] = f"c_{i:03d}"
    
    return cards

# ============================================================
# 3. 规则卡解析
# ============================================================
def parse_rules(text):
    """解析规则卡图鉴，返回卡牌列表"""
    cards = []
    
    # 找到"规则卡列表"章节
    list_start = text.find('## 规则卡列表')
    if list_start == -1:
        list_start = text.find('规则卡列表')
    
    rules_text = text[list_start:] if list_start >= 0 else text
    
    # 移除"并入总库统计"及之后的内容
    end_marker = text.find('## 并入总库统计')
    if end_marker > list_start:
        rules_text = text[list_start:end_marker]
    
    # 解析普通规则卡表格
    # 找到 T1/T2/T3 各节
    t_sections = re.split(r'\n#### T[123]', rules_text)
    
    # 如果第一个元素不包含表格，跳过
    t_labels = ['T1', 'T2', 'T3']
    section_idx = 0
    
    for section in t_sections:
        if section_idx == 0:
            # 可能是前言部分，检查是否包含表格
            if '| 编号 | 规则文本' not in section:
                section_idx += 1
                continue
        
        # 确定当前等级
        # 找到等级标记
        t_match = re.search(r'T([123]).*?(-\d)', section)
        if not t_match:
            # 尝试从上下文推断
            for label in t_labels:
                if f'#### {label}' in section:
                    t_level = label
                    penalty = {'T1': '-3', 'T2': '-2', 'T3': '-1'}[t_level]
                    break
            else:
                section_idx += 1
                continue
        else:
            t_level = f'T{t_match.group(1)}'
            penalty = t_match.group(2).strip()
        
        # 解析表格行
        table_rows = re.findall(
            r'\|\s*(T\d-\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|',
            section
        )
        
        for row_id, rule_text, trigger_limit, note in table_rows:
            # 清理 rule_text
            rule_text = rule_text.strip()
            # 移除加粗标记
            rule_text = re.sub(r'\*\*', '', rule_text)
            trigger_limit = trigger_limit.strip()
            note = note.strip()
            
            # 计算难度
            difficulty = t_level
            
            # 判断类别
            category = "公开规则"
            if '隐藏' in note.lower():
                category = "隐藏规则"
            
            cards.append({
                "id": "",
                "name": f"规则 {row_id}",
                "type": "rule",
                "category": category,
                "difficulty": difficulty,
                "rule_text": rule_text,
                "penalty": penalty,
                "trigger_limit": trigger_limit,
                "note": note,
                "status": "active"
            })
        
        section_idx += 1
    
    # 解析特殊规则卡表格
    special_start = rules_text.find('### 特殊规则卡')
    if special_start > 0:
        special_text = rules_text[special_start:]
        
        # 特殊规则表格: | 地点 | 规则1 | 规则2 | 状态 |
        special_rows = re.findall(
            r'\|\s*(?:①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|11|12)[^\|]*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(✅.*?)?\|',
            special_text
        )
        
        for rule1, rule2, status in special_rows:
            rule1 = rule1.strip()
            rule2 = rule2.strip()
            
            for rule_text in [rule1, rule2]:
                if not rule_text:
                    continue
                
                # 提取惩罚值，如（-2）, （-1）, （-3）
                penalty_match = re.search(r'（-(\d)）', rule_text)
                if penalty_match:
                    penalty = f'-{penalty_match.group(1)}'
                    if penalty == '-3':
                        difficulty = 'T1'
                    elif penalty == '-2':
                        difficulty = 'T2'
                    else:
                        difficulty = 'T3'
                else:
                    penalty = '-1'
                    difficulty = 'T3'
                
                cards.append({
                    "id": "",
                    "name": f"特殊规则: {rule_text[:30]}...",
                    "type": "rule",
                    "category": "特殊规则",
                    "difficulty": difficulty,
                    "rule_text": clean_text(rule_text),
                    "penalty": penalty,
                    "trigger_limit": "",
                    "note": "特殊规则卡",
                    "status": "active"
                })
    
    # 按文档顺序分配 ID
    for i, card in enumerate(cards, 1):
        card["id"] = f"r_{i:03d}"
    
    return cards

# ============================================================
# 4. 角色卡解析
# ============================================================
def parse_characters(text):
    """解析角色卡图鉴，返回卡牌列表"""
    cards = []
    
    # 跳过"角色类型分配方案"章节之前的目录等
    # 直接找 ## 标题后面跟着角色名的部分
    
    # 已知的12个角色名列表
    known_characters = [
        '乐天派幸存者', '天生幸运儿', '倒霉体质者', '逻辑严谨理科生',
        '内向社恐大学生', '沉寂的上班族', '灵异研究者', '豪门之后',
        '外卖单王', '法医侦探', '街道社区主任', '整顿末世零零后'
    ]
    
    # 找到目录之后的内容
    toc_end = text.find('## 角色类型分配方案')
    if toc_end > 0:
        # 找到这个section结束的位置
        next_section = text.find('\n## ', toc_end + 10)
        # 如果找不到，用角色类型分配方案之后
        char_text = text[toc_end:]
    else:
        char_text = text
    
    for char_name in known_characters:
        # 找到角色的 ## 标题
        pattern = rf'\n## {re.escape(char_name)}\s*\n'
        match = re.search(pattern, text)
        if not match:
            continue
        
        # 找到下一个 ## 标题的位置
        start_pos = match.start()
        next_match = re.search(r'\n## (?!' + re.escape(char_name) + r')', text[start_pos + 5:])
        if next_match:
            end_pos = start_pos + 5 + next_match.start()
            char_section = text[start_pos:end_pos]
        else:
            char_section = text[start_pos:]
        
        # 提取字段
        def extract_field_ch(field_name):
            pattern = rf'\*\*{field_name}\*\*[：:]\s*(.*?)(?=\n\*\*|\n```|\n##|\Z)'
            match = re.search(pattern, char_section, re.DOTALL)
            if match:
                return match.group(1).strip()
            return ""
        
        # 提取技能名
        skill_name = extract_field_ch('专属被动')
        
        # 提取人设
        flavor = extract_field_ch('人设')
        
        # 提取面板数值
        health = 6
        sanity = 6
        
        # 查找面板数值修正表格
        health_match = re.search(r'健康值上限.*?(\d+)点', char_section)
        sanity_match = re.search(r'理智值上限.*?(\d+)点', char_section)
        
        # 优先找面板修正表格
        panel_rows = re.findall(
            r'\|\s*健康值上限\s*\|\s*\d+点\s*\|\s*(\d+)点',
            char_section
        )
        if panel_rows:
            health = int(panel_rows[0])
        
        panel_rows = re.findall(
            r'\|\s*理智值上限\s*\|\s*\d+点\s*\|\s*(\d+)点',
            char_section
        )
        if panel_rows:
            sanity = int(panel_rows[0])
        
        # 构建技能效果文本
        skill_effect_parts = []
        
        # 查找技能描述
        skill_sections = re.findall(
            r'### 技能[一二三四五六七八九十].*?\n(.*?)(?=\n### 技能|\n### 设计|\n### 代价|\n## |\Z)',
            char_section, re.DOTALL
        )
        
        if skill_sections:
            skill_effect = '; '.join([clean_text(s)[:200] for s in skill_sections])
        else:
            # 尝试提取所有技能相关文本
            skill_text = ""
            for label in ['技能一', '技能二', '技能三', '技能四', '技能五']:
                found = re.search(rf'### {label}[^\n]*\n(.*?)(?=\n###|\n##|\Z)', char_section, re.DOTALL)
                if found:
                    skill_text += clean_text(found.group(1))[:200] + '; '
            skill_effect = skill_text.strip('; ')
        
        cards.append({
            "id": "",
            "name": char_name,
            "type": "character",
            "skill_name": clean_text(skill_name) if skill_name else "",
            "skill_effect": skill_effect if skill_effect else "",
            "health": health,
            "sanity": sanity,
            "flavor": clean_text(flavor)[:200] if flavor else "",
            "status": "active"
        })
    
    # 按文档顺序分配 ID
    for i, card in enumerate(cards, 1):
        card["id"] = f"ch_{i:03d}"
    
    return cards


# ============================================================
# 5. 个人目的卡解析
# ============================================================
def parse_personal_goals(text):
    """解析个人目的卡图鉴，返回卡牌列表"""
    cards = []
    
    # 找到"二、卡牌图鉴"章节
    catalog_start = text.find('## 二、卡牌图鉴')
    if catalog_start == -1:
        catalog_start = text.find('二、卡牌图鉴')
    if catalog_start == -1:
        catalog_start = 0
    
    # 移除"三、设计索引"及之后
    end_marker = text.find('## 三、设计索引')
    if end_marker > catalog_start:
        goals_text = text[catalog_start:end_marker]
    else:
        goals_text = text[catalog_start:]
    
    # 匹配每张卡: #### XX 【卡名】
    card_pattern = re.compile(
        r'####\s+(\d+)\s+【(.+?)】\s*\n(.*?)(?=\n####\s+\d+\s+【|\n##\s+三、|\Z)',
        re.DOTALL
    )
    
    matches = card_pattern.findall(goals_text)
    
    for number, name, body in matches:
        name = name.strip()
        
        # 提取秘密目标
        goal_match = re.search(r'\*\*秘密目标\*\*[：:]\s*(.*?)(?=\n\*\*|\n####|\Z)', body, re.DOTALL)
        goal_text = clean_text(goal_match.group(1)) if goal_match else ""
        
        # 提取叙事提示
        narrative_match = re.search(r'\*\*叙事提示\*\*[：:]\s*(.*?)(?=\n\*\*|\n####|\Z)', body, re.DOTALL)
        narrative = clean_text(narrative_match.group(1)) if narrative_match else ""
        
        cards.append({
            "id": "",
            "name": name,
            "type": "personal_goal",
            "goal_text": goal_text,
            "condition": narrative,
            "status": "active"
        })
    
    # 按文档顺序分配 ID
    for i, card in enumerate(cards, 1):
        card["id"] = f"pg_{i:03d}"
    
    return cards


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 60)
    print("  《黎明之后》卡牌数据提取工具")
    print("=" * 60)
    print()
    
    # 读取并解析各图鉴
    print("[1/5] 解析怪谈卡图鉴...")
    whispers_text = read_file(WHISPERS_FILE)
    whispers = parse_whispers(whispers_text)
    print(f"      提取到 {len(whispers)} 张怪谈卡")
    
    print("[2/5] 解析反击卡图鉴...")
    cm_text = read_file(COUNTERMEASURES_FILE)
    countermeasures = parse_countermeasures(cm_text)
    print(f"      提取到 {len(countermeasures)} 张反击卡")
    
    print("[3/5] 解析规则卡图鉴...")
    rules_text = read_file(RULES_FILE)
    rules = parse_rules(rules_text)
    print(f"      提取到 {len(rules)} 张规则卡")
    
    print("[4/5] 解析角色卡图鉴...")
    chars_text = read_file(CHARACTERS_FILE)
    characters = parse_characters(chars_text)
    print(f"      提取到 {len(characters)} 张角色卡")
    
    print("[5/5] 解析个人目的卡图鉴...")
    goals_text = read_file(GOALS_FILE)
    personal_goals = parse_personal_goals(goals_text)
    print(f"      提取到 {len(personal_goals)} 张个人目的卡")
    
    # 按等级统计
    print("\n--- 统计 ---")
    
    # 怪谈卡等级分布
    w_levels = {}
    for c in whispers:
        lv = c['level']
        w_levels[lv] = w_levels.get(lv, 0) + 1
    print(f"怪谈卡等级分布: {w_levels}")
    
    # 反击卡等级分布
    c_levels = {}
    for c in countermeasures:
        lv = c['level']
        c_levels[lv] = c_levels.get(lv, 0) + 1
    print(f"反击卡等级分布: {c_levels}")
    
    # 规则卡难度分布
    r_diffs = {}
    for c in rules:
        d = c['difficulty']
        r_diffs[d] = r_diffs.get(d, 0) + 1
    print(f"规则卡难度分布: {r_diffs}")
    
    # 构建输出
    output = {
        "version": "1.0",
        "generated": "2026-07-05",
        "source": "Based on 黎明之后 V1.9.3 catalogs",
        "cards": {
            "whispers": whispers,
            "countermeasures": countermeasures,
            "rules": rules,
            "characters": characters,
            "personal_goals": personal_goals
        }
    }
    
    total = sum(len(v) for v in output["cards"].values())
    
    # 写入JSON
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功! 总计 {total} 张卡牌")
    print(f"   怪谈卡: {len(whispers)} 张")
    print(f"   反击卡: {len(countermeasures)} 张")
    print(f"   规则卡: {len(rules)} 张")
    print(f"   角色卡: {len(characters)} 张")
    print(f"   个人目的卡: {len(personal_goals)} 张")
    print(f"\n输出文件: {OUTPUT}")


if __name__ == '__main__':
    main()
