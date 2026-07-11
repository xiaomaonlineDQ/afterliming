#!/usr/bin/env python3
"""生成《黎明之后》产品报告PPT - 求职/融资/评选用"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── 色彩系统 ──
PURPLE = RGBColor(0x7B, 0x6F, 0x9E)
CORA = RGBColor(0xD4, 0x75, 0x6B)
TEAL = RGBColor(0x4A, 0x90, 0xA4)
AMBER = RGBColor(0xC8, 0x92, 0x3E)
BLUE = RGBColor(0x5B, 0x7C, 0xB0)
DARK_BG = RGBColor(0x1A, 0x1A, 0x2E)
DARK_CARD = RGBColor(0x25, 0x25, 0x42)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
MID_GRAY = RGBColor(0x88, 0x88, 0x99)
ACCENT_LINE = RGBColor(0x3A, 0x3A, 0x5C)

OUTPUT = r"c:\Users\80526\WorkBuddy\2026-06-05-15-49-56\黎明之后_产品报告.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_dark_bg(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BG

def add_accent_bar(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name='Microsoft YaHei'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_multiline_text(slide, left, top, width, height, lines, default_size=14, default_color=LIGHT_GRAY):
    """lines: list of (text, size, color, bold)"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        text = line[0]
        size = line[1] if len(line) > 1 else default_size
        color = line[2] if len(line) > 2 else default_color
        bold = line[3] if len(line) > 3 else False
        p.text = text
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.bold = bold
        p.font.name = 'Microsoft YaHei'
        p.space_after = Pt(6)
    return txBox

def add_card(slide, left, top, width, height):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_CARD
    shape.line.color.rgb = ACCENT_LINE
    shape.line.width = Pt(0.5)
    return shape

def add_title_header(slide, title_text, subtitle_text=None):
    add_accent_bar(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.06), PURPLE)
    add_text_box(slide, Inches(0.8), Inches(0.35), Inches(11), Inches(0.6), title_text, 
                 font_size=28, color=WHITE, bold=True)
    if subtitle_text:
        add_text_box(slide, Inches(0.8), Inches(0.9), Inches(11), Inches(0.4), subtitle_text,
                     font_size=14, color=MID_GRAY)
    # bottom line
    add_accent_bar(slide, Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.02), ACCENT_LINE)

# ═══════════════════════════════════════════
# 第1页：封面
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_dark_bg(slide)

# 顶部装饰线
add_accent_bar(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.12), PURPLE)

# 主标题
add_text_box(slide, Inches(1.5), Inches(2.0), Inches(10), Inches(1.2),
             '黎明之后', font_size=72, color=WHITE, bold=True)

# 副标题
add_text_box(slide, Inches(1.5), Inches(3.2), Inches(10), Inches(0.6),
             '（规则怪谈-推理反击）社交派对游戏', font_size=28, color=CORA)

# 分隔线
add_accent_bar(slide, Inches(1.5), Inches(4.0), Inches(3), Inches(0.04), PURPLE)

# 描述
add_multiline_text(slide, Inches(1.5), Inches(4.3), Inches(8), Inches(1.5), [
    ('你不知道什么能做、什么不能说——但每次违规，理智都会崩溃。', 18, LIGHT_GRAY, False),
    ('你必须在12天内推理出鬼的规则、一条条抹除它们，', 18, LIGHT_GRAY, False),
    ('同时保持自己不饿死、不疯掉、不被身边的人背叛。', 18, LIGHT_GRAY, False),
    ('因为鬼就在你们之中。', 20, CORA, True),
])

# 右下角信息
add_multiline_text(slide, Inches(8), Inches(6.2), Inches(4.5), Inches(1.2), [
    ('产品报告 V1.0', 14, MID_GRAY, False),
    ('2026年7月', 12, MID_GRAY, False),
    ('设计者：小马', 12, MID_GRAY, False),
], default_color=MID_GRAY)

# ═══════════════════════════════════════════
# 第2页：游戏概览
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '游戏概览', 'Game Overview')

# 基本信息卡片
info_items = [
    ('游戏名称', '《黎明之后》'),
    ('游戏类型', '社交推理 + 规则解谜 + 生存策略'),
    ('玩家数量', '6-12人（推荐8人）'),
    ('游戏时长', '90-150分钟'),
    ('年龄建议', '14+'),
    ('核心体验', '解谜 · 生存 · 社交博弈'),
    ('主持人', 'AI市长（豆包等国产大模型）或真人'),
    ('物理组件', '188张卡牌 + 地图 + 角色面板 + 公开规则栏'),
]

for i, (label, value) in enumerate(info_items):
    y = Inches(1.7) + Inches(0.6) * i
    add_text_box(slide, Inches(1.0), y, Inches(2.5), Inches(0.4), label, 
                 font_size=14, color=PURPLE, bold=True)
    add_text_box(slide, Inches(3.5), y, Inches(8), Inches(0.4), value,
                 font_size=14, color=LIGHT_GRAY)

# 右侧一句话
add_card(slide, Inches(8.5), Inches(1.8), Inches(4), Inches(4.5))
add_multiline_text(slide, Inches(8.8), Inches(2.0), Inches(3.4), Inches(4.0), [
    ('"狼人杀的推理深度', 16, WHITE, True),
    ('+ 密室逃脱的解谜快感', 16, WHITE, True),
    ('+ 生存游戏的资源博弈"', 16, WHITE, True),
    ('', 10, MID_GRAY, False),
    ('规则不是附属品——', 13, CORA, True),
    ('规则本身就是游戏。', 13, CORA, True),
    ('', 10, MID_GRAY, False),
    ('AI市长替代真人主持，', 12, LIGHT_GRAY, False),
    ('零门槛开桌，每局生成', 12, LIGHT_GRAY, False),
    ('独一无二的恐怖叙事。', 12, LIGHT_GRAY, False),
])

# ═══════════════════════════════════════════
# 第3页：设计哲学
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '设计哲学', 'Design Philosophy —— 规则为骨')

principles = [
    ('原则一', '不知道规则 → 推理规则', 
     '传统桌游的规则是玩家阅读后遵守的。本游戏的规则是玩家观察后推理的。你不知道边界在哪，但你知道自己越界了——因为理智值在下降。这种"不确定中的确定惩罚"正是灵异怪谈类作品的核心心理机制。我们把它做成了一款桌游。'),
    ('原则二', '规则约束所有人，包括鬼', 
     '鬼制定了隐藏规则，但这些规则同样约束鬼自己。信息不对称是游戏的核心乐趣，但规则面前人人平等——这是博弈空间的保证。鬼也可能被其他鬼利用规则攻击。'),
    ('原则三', '物理实体承载情感', 
     '堆叠式角色面板让玩家"看到"自己的生存历程；公开规则栏让所有人随时感知规则的压迫；硬币掷出的正反面不只是判定，是命运。每一个物理组件都是为了制造某种情感反馈而设计的。'),
]

for i, (title, subtitle, desc) in enumerate(principles):
    y_base = Inches(1.7) + Inches(1.8) * i
    add_card(slide, Inches(0.8), y_base, Inches(11.7), Inches(1.6))
    # number
    add_text_box(slide, Inches(1.1), y_base + Inches(0.15), Inches(0.6), Inches(0.5),
                 str(i+1), font_size=48, color=PURPLE, bold=True)
    # title
    add_text_box(slide, Inches(1.8), y_base + Inches(0.15), Inches(3), Inches(0.4),
                 title, font_size=16, color=CORA, bold=True)
    # subtitle
    add_text_box(slide, Inches(1.8), y_base + Inches(0.55), Inches(9.5), Inches(0.4),
                 subtitle, font_size=15, color=WHITE, bold=True)
    # description
    add_text_box(slide, Inches(1.8), y_base + Inches(0.95), Inches(9.5), Inches(0.55),
                 desc, font_size=11, color=LIGHT_GRAY)

# ═══════════════════════════════════════════
# 第4页：四维规则骨架
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '核心创新：四维规则骨架', 'Rule System Architecture —— 规则不是附属品，规则本身就是游戏')

# 四个维度卡片
dims = [
    ('等级维度', '违规惩罚的严重程度', 'T1重(8张)·T2中(24张)·T3轻(20张)', PURPLE),
    ('可见性维度', '信息不对称的物理载体', '隐藏规则 → 公开规则 → 被抹除规则', TEAL),
    ('状态维度', '规则的活性与消亡', '生效中 ↔ 已抹除（宣言推理的终极目标）', BLUE),
    ('来源维度', '规则的生成与绑定', '普通规则28张(鬼自选) + 特殊规则24张(12地点×2)', AMBER),
]

for i, (title, subtitle, detail, color) in enumerate(dims):
    x = Inches(0.5) + Inches(3.15) * i
    add_card(slide, x, Inches(1.7), Inches(2.95), Inches(2.8))
    # color top bar
    add_accent_bar(slide, x, Inches(1.7), Inches(2.95), Inches(0.08), color)
    add_text_box(slide, x + Inches(0.2), Inches(2.0), Inches(2.55), Inches(0.4),
                 title, font_size=18, color=color, bold=True)
    add_text_box(slide, x + Inches(0.2), Inches(2.4), Inches(2.55), Inches(0.5),
                 subtitle, font_size=12, color=MID_GRAY)
    add_text_box(slide, x + Inches(0.2), Inches(3.0), Inches(2.55), Inches(1.2),
                 detail, font_size=12, color=LIGHT_GRAY)

# 底部总结
add_card(slide, Inches(0.5), Inches(4.8), Inches(12.3), Inches(2.2))
add_accent_bar(slide, Inches(0.5), Inches(4.8), Inches(12.3), Inches(0.06), PURPLE)
add_multiline_text(slide, Inches(1.0), Inches(5.1), Inches(11.3), Inches(1.8), [
    ('整款游戏的建筑逻辑', 20, WHITE, True),
    ('宣言推理 · 双维生存 · 事件卡攻防 · 角色技能 · AI市长叙事', 15, LIGHT_GRAY, False),
    ('全部生长在"规则系统"这副骨架上', 15, CORA, True),
    ('', 8, MID_GRAY, False),
    ('详见设计书附录：四维规则骨架图（SVG）——直观展示52张规则卡在四个维度上的分布与流动关系', 11, MID_GRAY, False),
])

# ═══════════════════════════════════════════
# 第5页：宣言推理
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '核心玩法：宣言推理', 'Declaration & Reasoning —— 让"不知道规则"成为玩法')

# 流程图式展示
steps = [
    ('① 观察', '违反规则的玩家理智下降，所有人观察到"有人受罚了"', PURPLE),
    ('② 猜测', '人类阵营结合AI市长的海龟汤式故事和游戏中的异常现象，推理规则', TEAL),
    ('③ 宣言', '大声宣言："我推理第X条规则——[规则内容]"', CORA),
    ('④ 质询', '鬼可以发起质询，质疑推理过程或证据链', AMBER),
    ('⑤ 判定', '鬼拿出对应规则卡验证。正确→规则抹除；错误→宣言者扣1理智', BLUE),
]

for i, (step, desc, color) in enumerate(steps):
    y = Inches(1.7) + Inches(1.05) * i
    # color dot
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.0), y + Inches(0.1), Inches(0.25), Inches(0.25))
    dot.fill.solid()
    dot.fill.fore_color.rgb = color
    dot.line.fill.background()
    # step title
    add_text_box(slide, Inches(1.5), y, Inches(2.0), Inches(0.45), step,
                 font_size=18, color=color, bold=True)
    # description
    add_text_box(slide, Inches(1.5), y + Inches(0.4), Inches(10), Inches(0.45), desc,
                 font_size=13, color=LIGHT_GRAY)

# 右侧亮点
add_card(slide, Inches(8.5), Inches(1.8), Inches(4.2), Inches(5.0))
add_accent_bar(slide, Inches(8.5), Inches(1.8), Inches(4.2), Inches(0.06), PURPLE)
add_multiline_text(slide, Inches(8.9), Inches(2.1), Inches(3.5), Inches(4.5), [
    ('设计亮点', 16, WHITE, True),
    ('', 8, MID_GRAY, False),
    ('• 每人每回合限1次宣言', 12, LIGHT_GRAY, False),
    ('• 宣言次数达2/4/6次抽事件卡', 12, LIGHT_GRAY, False),
    ('• 宣言成功→规则永久抹除', 12, CORA, True),
    ('• 宣言失败→扣1理智', 12, CORA, True),
    ('• 鬼可发起质询打断', 12, AMBER, False),
    ('• 宣言即合法：玩家互相监督', 12, LIGHT_GRAY, False),
    ('  市长不做法官', 12, MID_GRAY, False),
])

# ═══════════════════════════════════════════
# 第6页：双维属性与生存策略
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '双维属性：两条独立的死亡路径', 'Dual-Dimension Survival —— 饿死 vs 疯掉')

# 左边：健康值
add_card(slide, Inches(0.5), Inches(1.7), Inches(5.8), Inches(5.0))
add_accent_bar(slide, Inches(0.5), Inches(1.7), Inches(5.8), Inches(0.06), TEAL)
add_text_box(slide, Inches(0.9), Inches(2.0), Inches(5), Inches(0.5),
             '健康值（体力）', font_size=22, color=TEAL, bold=True)
add_multiline_text(slide, Inches(0.9), Inches(2.6), Inches(5), Inches(3.5), [
    ('起始：6点（标准）', 15, WHITE, True),
    ('', 8, MID_GRAY, False),
    ('消耗途径：', 14, CORA, True),
    ('• 每日黎明自动扣除（递增：1→2→3...）', 13, LIGHT_GRAY, False),
    ('• 移动消耗（越远扣越多）', 13, LIGHT_GRAY, False),
    ('• 事件卡效果', 13, LIGHT_GRAY, False),
    ('', 8, MID_GRAY, False),
    ('恢复途径：', 14, CORA, True),
    ('• 物资卡（食物类）', 13, LIGHT_GRAY, False),
    ('• 反击卡效果', 13, LIGHT_GRAY, False),
    ('• 交易获取物资', 13, LIGHT_GRAY, False),
    ('', 8, MID_GRAY, False),
    ('死亡条件：健康值降至0 → 饿死', 14, TEAL, True),
])

# 右边：理智值
add_card(slide, Inches(6.8), Inches(1.7), Inches(6.0), Inches(5.0))
add_accent_bar(slide, Inches(6.8), Inches(1.7), Inches(6.0), Inches(0.06), PURPLE)
add_text_box(slide, Inches(7.2), Inches(2.0), Inches(5), Inches(0.5),
             '理智值（精神）', font_size=22, color=PURPLE, bold=True)
add_multiline_text(slide, Inches(7.2), Inches(2.6), Inches(5.2), Inches(3.5), [
    ('起始：6点（标准）', 15, WHITE, True),
    ('', 8, MID_GRAY, False),
    ('消耗途径：', 14, CORA, True),
    ('• 违反鬼的隐藏规则→扣理智', 13, LIGHT_GRAY, False),
    ('• T1规则扣3点 / T2扣2点 / T3扣1点', 13, LIGHT_GRAY, False),
    ('• 怪谈卡效果', 13, LIGHT_GRAY, False),
    ('', 8, MID_GRAY, False),
    ('恢复途径：', 14, CORA, True),
    ('• 反击卡效果（极少）', 13, LIGHT_GRAY, False),
    ('• 特殊角色技能', 13, LIGHT_GRAY, False),
    ('', 8, MID_GRAY, False),
    ('死亡条件：理智值降至0 → 化鬼', 14, PURPLE, True),
    ('化鬼后加入鬼阵营，人类全员抽反击卡', 13, CORA, True),
])

# ═══════════════════════════════════════════
# 第7页：AI市长
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, 'AI市长：桌游主持的范式转移', 'AI Mayor —— 零门槛开桌 + 海龟汤式恐怖叙事')

# 左边：痛点
add_card(slide, Inches(0.5), Inches(1.7), Inches(5.8), Inches(2.8))
add_accent_bar(slide, Inches(0.5), Inches(1.7), Inches(5.8), Inches(0.06), CORA)
add_text_box(slide, Inches(0.9), Inches(2.0), Inches(5), Inches(0.5),
             '传统桌游的痛点', font_size=18, color=CORA, bold=True)
add_multiline_text(slide, Inches(0.9), Inches(2.6), Inches(5), Inches(1.6), [
    ('✕ 需要DM/主持人：缺人就开不了桌', 13, LIGHT_GRAY, False),
    ('✕ DM水平参差：新手DM严重影响体验', 13, LIGHT_GRAY, False),
    ('✕ 规则复杂：学习成本高，劝退新玩家', 13, LIGHT_GRAY, False),
    ('✕ 叙事重复：老玩家反复玩缺乏新鲜感', 13, LIGHT_GRAY, False),
])

# 右边：解决方案
add_card(slide, Inches(6.8), Inches(1.7), Inches(6.0), Inches(2.8))
add_accent_bar(slide, Inches(6.8), Inches(1.7), Inches(6.0), Inches(0.06), TEAL)
add_text_box(slide, Inches(7.2), Inches(2.0), Inches(5), Inches(0.5),
             'AI市长的解决方案', font_size=18, color=TEAL, bold=True)
add_multiline_text(slide, Inches(7.2), Inches(2.6), Inches(5.2), Inches(1.6), [
    ('✓ 零门槛：打开手机/电脑即可开桌', 13, LIGHT_GRAY, False),
    ('✓ 一致性：严格按照预设指令执行，不偏袒', 13, LIGHT_GRAY, False),
    ('✓ 海龟汤叙事：每局生成独一无二的恐怖故事', 13, CORA, True),
    ('✓ 自动化：记录宣言、结算数值、生成终局日记', 13, LIGHT_GRAY, False),
])

# 底部：6步工作流
add_card(slide, Inches(0.5), Inches(4.8), Inches(12.3), Inches(2.2))
add_accent_bar(slide, Inches(0.5), Inches(4.8), Inches(12.3), Inches(0.06), PURPLE)
add_text_box(slide, Inches(0.9), Inches(5.1), Inches(5), Inches(0.5),
             'AI市长6步工作流程', font_size=18, color=PURPLE, bold=True)

flow_steps = [
    ('0.确认玩家', PURPLE), ('1.开局判定', TEAL), ('2.生成故事', CORA),
    ('3.每日黎明', AMBER), ('4.记录回合', BLUE), ('5.结算数值', PURPLE), ('6.终局日记', TEAL),
]
for i, (text, color) in enumerate(flow_steps):
    x = Inches(0.95) + Inches(1.75) * i
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(5.7), Inches(1.55), Inches(0.55))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.fill.background()
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(10)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = 'Microsoft YaHei'
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].space_before = Pt(4)

    if i < len(flow_steps) - 1:
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, 
                                        x + Inches(1.55), Inches(5.85),
                                        Inches(0.2), Inches(0.2))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = MID_GRAY
        arrow.line.fill.background()

add_text_box(slide, Inches(0.9), Inches(6.45), Inches(11.5), Inches(0.4),
             '海龟汤难度叙事 → "不讲因果链，只讲日常碎片" —— 故事让玩家知道"规则长什么样"，但不告诉"规则在哪里"',
             font_size=11, color=MID_GRAY)

# ═══════════════════════════════════════════
# 第8页：卡牌生态
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '卡牌生态体系', 'Card Ecosystem —— 188张物理卡 × 5大图鉴')

card_types = [
    ('规则卡', '52张', 'T1(8)+T2(24)+T3(20)', '游戏的骨架，一切机制的起点', PURPLE),
    ('反击卡', '62张', '基础36+觉醒16+极致8+真理2', '人类阵营的破局手段', TEAL),
    ('怪谈卡', '36张', '流言16+异常10+怪诞6+灾厄4', '鬼阵营的攻击武器', CORA),
    ('角色卡', '12张', '12个独特角色+技能', '不对称能力+叙事身份', AMBER),
    ('个人目的卡', '26张', '公开+隐藏双目标', '个人胜利条件，增加博弈层次', BLUE),
]

for i, (name, count, detail, desc, color) in enumerate(card_types):
    x = Inches(0.5) + Inches(2.55) * i
    add_card(slide, x, Inches(1.7), Inches(2.35), Inches(2.5))
    add_accent_bar(slide, x, Inches(1.7), Inches(2.35), Inches(0.08), color)
    add_text_box(slide, x + Inches(0.15), Inches(2.0), Inches(2.0), Inches(0.4),
                 name, font_size=18, color=color, bold=True)
    add_text_box(slide, x + Inches(0.15), Inches(2.4), Inches(2.0), Inches(0.35),
                 count, font_size=24, color=WHITE, bold=True)
    add_text_box(slide, x + Inches(0.15), Inches(2.8), Inches(2.0), Inches(0.5),
                 detail, font_size=11, color=LIGHT_GRAY)
    add_text_box(slide, x + Inches(0.15), Inches(3.25), Inches(2.0), Inches(0.6),
                 desc, font_size=11, color=MID_GRAY)

# 底部分布图
add_card(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.5))
add_text_box(slide, Inches(0.9), Inches(4.8), Inches(11.5), Inches(0.45),
             '卡牌物理区域设计', font_size=16, color=WHITE, bold=True)

zones = [
    ('反击卡区域', '未激活区(盖放) → 已激活区(公开) → 持续适用区 → 弃牌区', TEAL),
    ('怪谈卡区域', '未激活池(鬼共享) → 已激活池 → 目标角色下/弃牌堆', CORA),
    ('物资卡区域', '手牌(隐藏) → 使用 → 弃牌堆', AMBER),
    ('公开规则栏', '四分区物理板：公开规则 / 被抹除规则 / 已激活怪谈 / 回合指示', PURPLE),
]

for i, (zone, flow, color) in enumerate(zones):
    y = Inches(5.4) + Inches(0.5) * i
    add_text_box(slide, Inches(0.9), y, Inches(2.5), Inches(0.4), zone,
                 font_size=13, color=color, bold=True)
    add_text_box(slide, Inches(3.4), y, Inches(8.5), Inches(0.4), flow,
                 font_size=11, color=LIGHT_GRAY)

# ═══════════════════════════════════════════
# 第9页：角色设计哲学
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '角色设计哲学', 'Character Design —— 12个即插即用的叙事身份')

chars = [
    ('乐天派', '开局健康7(高1点)、理智5(低1点)', '乐观的生存主义者，体力充沛但神经大条'),
    ('法医侦探', '宣言时额外获取1条线索信息', '专业训练带来推理优势，但身体条件普通'),
    ('社恐大学生', '被质询时可选择沉默（免于回答）', '内向但敏锐，社交回避反而成为保护'),
    ('街道主任', '每回合可保护1人免受1次怪谈攻击', '街道工作经验赋予的庇护能力'),
    ('整顿末世零零后', '无视1条低级规则的约束', 'Z世代的叛逆在末世成了生存优势'),
    ('……', '共12个角色，每局6-12人自由组合', '每个角色有独特叙事背景 + 主动/被动技能'),
]

for i, (name, skill, flavor) in enumerate(chars):
    y = Inches(1.7) + Inches(0.85) * i
    add_text_box(slide, Inches(1.0), y, Inches(2.0), Inches(0.4), name,
                 font_size=15, color=CORA, bold=True)
    add_text_box(slide, Inches(3.0), y, Inches(4.5), Inches(0.4), skill,
                 font_size=12, color=WHITE)
    add_text_box(slide, Inches(7.5), y, Inches(5), Inches(0.4), flavor,
                 font_size=11, color=MID_GRAY)

# ═══════════════════════════════════════════
# 第10页：竞争差异化
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '竞争差异化', 'Competitive Differentiation —— 为什么《黎明之后》不可替代')

# 对比表
comparisons = [
    ('维度', '狼人杀', '阿瓦隆', '密室逃脱', '《黎明之后》', True),
    ('推理类型', '身份推理', '阵营推理', '谜题推理', '规则推理 ✦', False),
    ('信息机制', '夜晚信息', '任务结果', '线索收集', '海龟汤式叙事 ✦', False),
    ('死亡机制', '投票淘汰', '无', '无', '双维属性自然死亡 ✦', False),
    ('主持人', '必需', '必需', '必需', 'AI市长/可选 ✦', False),
    ('重玩性', '中', '中', '低', '极高（规则组合爆炸）✦', False),
    ('叙事', '无', '无', '固定', '每局独有 ✦', False),
    ('策略深度', '中低', '中', '中低', '高（多维度博弈）✦', False),
    ('入门门槛', '低', '低', '低', '中（AI辅助降低）✦', False),
]

for i, row in enumerate(comparisons):
    is_header = row[-1]
    y = Inches(1.7) + Inches(0.5) * i
    bg_color = DARK_CARD if is_header else DARK_BG
    text_color = WHITE if is_header else LIGHT_GRAY
    weight = True if is_header else False

    for j, cell in enumerate(row[:-1]):
        x = Inches(0.8) + Inches(2.5) * j
        cell_color = text_color
        if j == 4 and not is_header:  # 黎明之后列高亮
            cell_color = CORA
        add_text_box(slide, x, y, Inches(2.3), Inches(0.4), cell,
                     font_size=12 if not is_header else 14, color=cell_color, bold=weight)

# 底部亮点
add_card(slide, Inches(0.5), Inches(6.2), Inches(12.3), Inches(0.9))
add_text_box(slide, Inches(0.9), Inches(6.35), Inches(11.5), Inches(0.6),
             '✦ 核心差异化标签：规则推理 × AI市长 × 双维生存 × 海龟汤叙事 × 规则组合爆炸重玩性',
             font_size=14, color=CORA, bold=True)

# ═══════════════════════════════════════════
# 第11页：市场机会与路线图
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)
add_title_header(slide, '市场机会与开发路线图', 'Market & Roadmap')

# 市场机会
add_card(slide, Inches(0.5), Inches(1.7), Inches(6.0), Inches(2.5))
add_accent_bar(slide, Inches(0.5), Inches(1.7), Inches(6.0), Inches(0.06), TEAL)
add_text_box(slide, Inches(0.9), Inches(2.0), Inches(5), Inches(0.5),
             '市场机会', font_size=18, color=TEAL, bold=True)
add_multiline_text(slide, Inches(0.9), Inches(2.6), Inches(5.2), Inches(1.3), [
    ('• 中国桌游市场年增长30%+，社交推理品类高速扩张', 12, LIGHT_GRAY, False),
    ('• 狼人杀/阿瓦隆/血染钟楼验证了品类需求', 12, LIGHT_GRAY, False),
    ('• "规则推理"品类几乎空白——无直接竞品', 12, CORA, True),
    ('• AI辅助降低门槛，扩大潜在用户群', 12, LIGHT_GRAY, False),
    ('• 目标：社交聚会场景 + 桌游吧 + 线上剧本杀平台', 12, LIGHT_GRAY, False),
])

# 目标用户
add_card(slide, Inches(6.8), Inches(1.7), Inches(6.0), Inches(2.5))
add_accent_bar(slide, Inches(6.8), Inches(1.7), Inches(6.0), Inches(0.06), AMBER)
add_text_box(slide, Inches(7.2), Inches(2.0), Inches(5), Inches(0.5),
             '目标用户画像', font_size=18, color=AMBER, bold=True)
add_multiline_text(slide, Inches(7.2), Inches(2.6), Inches(5.2), Inches(1.3), [
    ('• 核心玩家：18-35岁社交推理爱好者', 12, LIGHT_GRAY, False),
    ('• 扩展用户：派对/团建场景的轻度玩家', 12, LIGHT_GRAY, False),
    ('• 潜在用户：线上剧本杀/密室逃脱爱好者', 12, LIGHT_GRAY, False),
    ('• 渠道：桌游吧、Kickstarter/摩点众筹、电商', 12, LIGHT_GRAY, False),
    ('• 定价区间：¥198-298（标准版）', 12, WHITE, True),
])

# 路线图
add_card(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.6))
add_accent_bar(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(0.06), PURPLE)
add_text_box(slide, Inches(0.9), Inches(4.8), Inches(11.5), Inches(0.5),
             '开发路线图', font_size=18, color=PURPLE, bold=True)

phases = [
    ('V1.x 核心机制\n(已完成)', '12角色\n62反击卡\n36怪谈卡\n52规则卡\n双维属性\n宣言推理', PURPLE),
    ('V2.0 系统完善\n(已完成)', 'AI市长指令\n网站第一期\n卡牌数据库\n9张流程图\n设计书+PPT', TEAL),
    ('V3.0 成品打磨\n(计划中)', '美术设计\n网站第二期\nAI对话功能\n盲测迭代\n工业化文件', CORA),
    ('V4.0 商业发布\n(未来)', '众筹上线\n生产供应链\n渠道合作\n线上版本\n社区运营', AMBER),
]

for i, (phase, items, color) in enumerate(phases):
    x = Inches(0.9) + Inches(3.1) * i
    add_card(slide, x, Inches(5.4), Inches(2.9), Inches(1.4))
    add_accent_bar(slide, x, Inches(5.4), Inches(2.9), Inches(0.06), color)
    add_text_box(slide, x + Inches(0.15), Inches(5.6), Inches(2.6), Inches(0.6),
                 phase, font_size=12, color=color, bold=True)
    add_text_box(slide, x + Inches(0.15), Inches(6.05), Inches(2.6), Inches(0.6),
                 items, font_size=10, color=LIGHT_GRAY)

    if i < len(phases) - 1:
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                        x + Inches(2.92), Inches(6.0),
                                        Inches(0.18), Inches(0.18))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = MID_GRAY
        arrow.line.fill.background()

# ═══════════════════════════════════════════
# 第12页：结尾
# ═══════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_dark_bg(slide)

add_accent_bar(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.12), PURPLE)

add_text_box(slide, Inches(1.5), Inches(2.2), Inches(10), Inches(1.0),
             '谢谢', font_size=64, color=WHITE, bold=True)

add_accent_bar(slide, Inches(1.5), Inches(3.4), Inches(3), Inches(0.04), PURPLE)

add_multiline_text(slide, Inches(1.5), Inches(3.8), Inches(10), Inches(2.5), [
    ('《黎明之后》', 28, WHITE, True),
    ('（规则怪谈-推理反击）社交派对游戏', 20, CORA, False),
    ('', 14, MID_GRAY, False),
    ('"规则不是附属品，规则本身就是游戏。"', 16, LIGHT_GRAY, False),
    ('', 14, MID_GRAY, False),
    ('版本：V2.0  |  文档：设计书 + 产品报告 + 完整设计稿', 14, MID_GRAY, False),
    ('网站：GitHub Pages（搭建中）  |  知识库：腾讯乐享', 14, MID_GRAY, False),
])

# 保存
prs.save(OUTPUT)
print(f"PPT saved to: {OUTPUT}")
print(f"Slides: {len(prs.slides)}")
