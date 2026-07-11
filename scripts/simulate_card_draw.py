#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《黎明之后》牌库抽取概率模拟

模拟三类牌库的抽取概率：
  1. 反击卡（62张，四等级，6条获取机制）
  2. 物资卡（63张+18官方，五等级，两种获取方式）
  3. 规则卡（52张=28普通+24特殊，鬼开局抽取）

运行：python scripts/simulate_card_draw.py
输出：控制台统计报告 + website/抽卡概率报告.html
"""

import random
import json
import math
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

# ============================================================
# 1. 反击卡抽取模拟
# ============================================================

class CountermeasureDeck:
    """反击卡牌库"""
    # 四等级：基础12种×3=36, 觉醒8种×2=16, 极致8种×1=8, 真理2种×1=2
    POOL = {
        "基础": 36,
        "觉醒": 16,
        "极致": 8,
        "真理": 2,
    }
    TOTAL = 62

    def __init__(self):
        self.deck = []
        for level, count in self.POOL.items():
            self.deck.extend([level] * count)
        self.reset()

    def reset(self):
        self.remaining = list(self.deck)
        random.shuffle(self.remaining)

    def draw(self, n=1) -> List[str]:
        drawn = self.remaining[:n]
        self.remaining = self.remaining[n:]
        return drawn

    def draw_initial_basic(self) -> str:
        """开局自选1张基础卡（A初始）"""
        for i, c in enumerate(self.remaining):
            if c == "基础":
                return self.remaining.pop(i)
        return None

    def remaining_count(self) -> int:
        return len(self.remaining)


def simulate_countermeasure_draws(
    num_players: int = 6,
    num_games: int = 500,
    avg_turns: int = 9,
    death_rate: float = 0.4,
    purge_rate: float = 0.5,
    challenge_success_rate: float = 0.3,
) -> Dict:
    """
    模拟反击卡抽取

    参数：
      num_players: 人类玩家数（不含鬼）
      num_games: 模拟局数
      avg_turns: 平均存活回合数
      death_rate: 每局死亡/化鬼概率（触发C不屈）
      purge_rate: 宣言抹除成功率（触发D智慧）
      challenge_success_rate: 质询鬼成功率（触发E奖赏）

    A初始: 每人开局1基础自选 + 2随机 = 3张（开局3张）
    C不屈: 每次有人死亡/化鬼，剩余全员各抽1张
    D智慧: 每2次抹除抽1张（最多3张）
    E奖赏: 每次质询成功抽1张（可多次）
    F存活: 存活到3/6/9/12回合各抽1张（最多4张）
    """
    results = {
        "基础": 0,
        "觉醒": 0,
        "极致": 0,
        "真理": 0,
    }
    total_draws = 0
    draws_per_game = []

    for _ in range(num_games):
        deck = CountermeasureDeck()
        game_draws = []

        # A初始：每人自选1基础 + 随机2张
        for _ in range(num_players):
            basic = deck.draw_initial_basic()
            if basic:
                game_draws.append(basic)
            rand2 = deck.draw(2)
            game_draws.extend(rand2)

        # 模拟游戏进程中的抽取
        # C不屈：death_rate概率触发，每次死亡剩余全员各抽1
        deaths = int(num_players * death_rate)
        for _ in range(deaths):
            survivors = num_players - deaths
            for _ in range(survivors):
                if deck.remaining_count() > 0:
                    game_draws.extend(deck.draw(1))

        # D智慧：宣言抹除2/4/6次各抽1张
        purges = int(avg_turns * purge_rate)
        wisdom_draws = purges // 2
        wisdom_draws = min(wisdom_draws, 3 * num_players)  # 每人最多3次
        for _ in range(wisdom_draws):
            if deck.remaining_count() > 0:
                game_draws.extend(deck.draw(1))

        # E奖赏：质询成功抽1张
        challenges = int(avg_turns * challenge_success_rate * num_players)
        for _ in range(challenges):
            if deck.remaining_count() > 0:
                game_draws.extend(deck.draw(1))

        # F存活：3/6/9/12回合
        survived_turns = min(avg_turns, 12)
        survival_draws = sum(1 for t in [3, 6, 9, 12] if t <= survived_turns)
        for _ in range(survival_draws * num_players):
            if deck.remaining_count() > 0:
                game_draws.extend(deck.draw(1))

        # 统计
        for card in game_draws:
            results[card] += 1
        total_draws += len(game_draws)
        draws_per_game.append(len(game_draws))

    return {
        "total_games": num_games,
        "total_draws": total_draws,
        "avg_draws_per_game": total_draws / num_games,
        "counts": results,
        "percentages": {k: v/total_draws*100 for k, v in results.items()},
    }


# ============================================================
# 2. 物资卡抽取模拟
# ============================================================

class SupplyDeck:
    """物资卡牌库"""
    # 五等级：官方物资18张 + 普通34 + 中级18 + 高级8 + 绝顶3 = 81张
    OFFICIAL_POOL = {"保障餐A": 18}
    NORMAL_POOL = {
        "普通物资": 34,
        "中级物资": 18,
        "高级物资": 8,
        "绝顶物资": 3,
    }

    def __init__(self):
        self.official = list(self.OFFICIAL_POOL.keys()) * 18  # 18张保障餐A
        self.normal = []
        for level, count in self.NORMAL_POOL.items():
            self.normal.extend([level] * count)
        self.reset()

    def reset(self):
        self.remaining_official = list(self.official)
        random.shuffle(self.remaining_official)
        self.remaining_normal = list(self.normal)
        random.shuffle(self.remaining_normal)

    def official_supply(self, n=3) -> List[str]:
        """官方补给：抽n张保障餐A"""
        drawn = self.remaining_official[:n]
        self.remaining_official = self.remaining_official[n:]
        return drawn

    def explore(self) -> str:
        """地图探索：从普通牌库抽1张"""
        if self.remaining_normal:
            return self.remaining_normal.pop(0)
        return None

    def official_remaining(self) -> int:
        return len(self.remaining_official)

    def normal_remaining(self) -> int:
        return len(self.remaining_normal)


def simulate_supply_draws(
    num_players: int = 6,
    num_games: int = 500,
    avg_turns: int = 9,
    explore_prob: float = 0.6,
) -> Dict:
    """
    模拟物资卡抽取

    官方补给: 每回合3张保障餐A，18张库存用完即止
    地图探索: 每次健康-1，从63张普通牌库获取1张
    """
    official_results = Counter()
    normal_results = Counter()
    official_exhausted_turn = []

    for _ in range(num_games):
        deck = SupplyDeck()

        # 第0天每人1张官方物资
        for _ in range(num_players):
            if deck.official_remaining() > 0:
                drawn = deck.official_supply(1)
                official_results.update(drawn)

        exhausted_at = None
        for turn in range(1, avg_turns + 1):
            # 官方补给（每人可选）
            players_supply = int(num_players * (1 - explore_prob))
            for _ in range(players_supply):
                before = deck.official_remaining()
                if before >= 3:
                    drawn = deck.official_supply(3)
                    official_results.update(drawn)
                elif before > 0:
                    drawn = deck.official_supply(before)
                    official_results.update(drawn)
                # 检查是否刚耗尽
                if before > 0 and deck.official_remaining() == 0:
                    if exhausted_at is None:
                        exhausted_at = turn

            # 地图探索
            players_explore = int(num_players * explore_prob)
            for _ in range(players_explore):
                card = deck.explore()
                if card:
                    normal_results.update([card])

        if exhausted_at:
            official_exhausted_turn.append(exhausted_at)

    return {
        "total_games": num_games,
        "official": {
            "counts": dict(official_results),
            "avg_exhaust_turn": sum(official_exhausted_turn)/max(len(official_exhausted_turn), 1),
            "exhaust_rate": len(official_exhausted_turn)/num_games*100,
        },
        "normal": {
            "counts": dict(normal_results),
            "total": sum(normal_results.values()),
        },
        "normal_percentages": {
            k: v/sum(normal_results.values())*100
            for k, v in normal_results.items()
        } if normal_results else {},
    }


# ============================================================
# 3. 规则卡抽取模拟
# ============================================================

class RuleDeck:
    """规则卡牌库"""
    # 28张普通规则: T1=4, T2=20, T3=4
    # 24张特殊规则: 12地点×2
    POOL = {
        "T1_普通": 4,
        "T2_普通": 20,
        "T3_普通": 4,
        "特殊": 24,
    }
    TOTAL = 52

    def __init__(self):
        self.deck = []
        for rule_type, count in self.POOL.items():
            self.deck.extend([rule_type] * count)
        self.reset()

    def reset(self):
        self.remaining = list(self.deck)
        random.shuffle(self.remaining)

    def draw(self, n: int) -> List[str]:
        drawn = self.remaining[:n]
        self.remaining = self.remaining[n:]
        return drawn


def simulate_rule_draws(
    num_players: int = 6,
    num_games: int = 1000,
) -> Dict:
    """
    模拟规则卡抽取

    鬼开局抽X张（X=人类玩家数-1，6人局=5张）
    """
    # X = num_players - 1
    draw_count = num_players - 1
    results = Counter()

    combo_stats = {
        "no_T1": 0,       # 没抽到T1
        "no_special": 0,  # 没抽到特殊
        "all_high": 0,    # 全是T2/T3
        "multi_special": 0,  # 多张特殊
    }

    for _ in range(num_games):
        deck = RuleDeck()
        drawn = deck.draw(draw_count)
        results.update(drawn)

        counts = Counter(drawn)
        if counts.get("T1_普通", 0) == 0:
            combo_stats["no_T1"] += 1
        if counts.get("特殊", 0) == 0:
            combo_stats["no_special"] += 1
        if counts.get("T1_普通", 0) == 0 and counts.get("特殊", 0) == 0:
            combo_stats["all_high"] += 1
        if counts.get("特殊", 0) >= 2:
            combo_stats["multi_special"] += 1

    total_draws = sum(results.values())

    # 统计前5张中含特殊规则的分布
    special_in_hand_dist = defaultdict(int)
    for _ in range(num_games):
        deck = RuleDeck()
        drawn = deck.draw(draw_count)
        special_in_hand_dist[Counter(drawn).get("特殊", 0)] += 1

    return {
        "total_games": num_games,
        "draw_count": draw_count,
        "total_draws": total_draws,
        "counts": dict(results),
        "percentages": {k: v/total_draws*100 for k, v in results.items()},
        "combo_stats": {k: v/num_games*100 for k, v in combo_stats.items()},
        "special_distribution": {
            k: v/num_games*100 for k, v in sorted(special_in_hand_dist.items())
        },
    }


# ============================================================
# 4. 综合报告生成
# ============================================================

COUNTER_RESULTS = None
SUPPLY_RESULTS = None
RULE_RESULTS = None


def run_all():
    global COUNTER_RESULTS, SUPPLY_RESULTS, RULE_RESULTS
    print("=" * 60)
    print("  《黎明之后》牌库抽取概率模拟")
    print("=" * 60)

    # 反击卡
    print("\n[1/3] 模拟反击卡抽取（500局）...")
    COUNTER_RESULTS = simulate_countermeasure_draws(
        num_players=6, num_games=500, avg_turns=9,
        death_rate=0.4, purge_rate=0.5, challenge_success_rate=0.3
    )

    # 物资卡
    print("[2/3] 模拟物资卡抽取（500局）...")
    SUPPLY_RESULTS = simulate_supply_draws(
        num_players=6, num_games=500, avg_turns=9, explore_prob=0.6
    )

    # 规则卡
    print("[3/3] 模拟规则卡抽取（1000局）...")
    RULE_RESULTS = simulate_rule_draws(
        num_players=6, num_games=1000
    )

    # 终端报告
    print("\n" + "=" * 60)
    print("  📊 反击卡抽取报告")
    print("=" * 60)
    c = COUNTER_RESULTS
    total = c["total_draws"]
    print(f"  模拟局数: {c['total_games']}")
    print(f"  总抽取: {total} 张")
    print(f"  平均每局: {c['avg_draws_per_game']:.1f} 张")
    print(f"  牌库总量: 62 张")
    print()
    for level in ["基础", "觉醒", "极致", "真理"]:
        cnt = c["counts"].get(level, 0)
        pct = c["percentages"].get(level, 0)
        bar = "█" * int(pct / 2)
        pool_pct = {"基础": 36, "觉醒": 16, "极致": 8, "真理": 2}[level]
        print(f"  {level:4s}  | {cnt:5d} 张 ({pct:5.1f}%)  {bar}  牌库占比: {pool_pct/62*100:.1f}%")

    print("\n" + "=" * 60)
    print("  📦 物资卡抽取报告")
    print("=" * 60)
    s = SUPPLY_RESULTS
    print(f"  模拟局数: {s['total_games']}")
    print(f"  [官方物资·保障餐A]")
    for name, cnt in sorted(s["official"]["counts"].items(), key=lambda x: -x[1]):
        print(f"    {name}: {cnt} 张")
    print(f"  官方物资平均耗尽回合: {s['official']['avg_exhaust_turn']:.1f}")
    print(f"  耗尽概率: {s['official']['exhaust_rate']:.1f}%")
    print(f"  [普通物资牌库]")
    for name, pct in sorted(s["normal_percentages"].items(), key=lambda x: -x[1]):
        cnt = s["normal"]["counts"].get(name, 0)
        bar = "█" * int(pct / 2)
        print(f"    {name:6s}  | {cnt:5d} 张 ({pct:5.1f}%)  {bar}")

    print("\n" + "=" * 60)
    print("  📜 规则卡抽取报告")
    print("=" * 60)
    r = RULE_RESULTS
    print(f"  模拟局数: {r['total_games']}")
    print(f"  每局抽取: {r['draw_count']} 张（人类数-1）")
    print(f"  牌库总量: 52 张")
    print()
    for rt in ["T1_普通", "T2_普通", "T3_普通", "特殊"]:
        cnt = r["counts"].get(rt, 0)
        pct = r["percentages"].get(rt, 0)
        bar = "█" * int(pct / 2)
        pool_pct = {"T1_普通": 4, "T2_普通": 20, "T3_普通": 4, "特殊": 24}[rt]
        print(f"  {rt:6s}  | {cnt:5d} 张 ({pct:5.1f}%)  {bar}  牌库占比: {pool_pct/52*100:.1f}%")

    print("\n  [组合概率]")
    for key, pct in r["combo_stats"].items():
        labels = {
            "no_T1": "未抽到T1规则",
            "no_special": "未抽到特殊规则",
            "all_high": "全是T2/T3规则",
            "multi_special": "抽到≥2张特殊规则",
        }
        print(f"    {labels.get(key, key)}: {pct:.1f}%")

    print("\n  [手中特殊规则张数分布]")
    for k, pct in r["special_distribution"].items():
        bar = "█" * int(pct / 2)
        print(f"    {k}张特殊规则: {pct:5.1f}%  {bar}")

    print("\n" + "=" * 60)
    print("  ✅ 模拟完成！HTML报告已生成。")
    print("=" * 60)


def generate_html_report():
    """生成可视化HTML报告"""
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>黎明之后 · 抽卡概率报告</title>
<style>
  :root {
    --bg: #0a0a0f;
    --purple: #7B6F9E;
    --coral: #D4756B;
    --teal: #4A90A4;
    --amber: #C8923E;
    --blue: #5B7CB0;
    --text: #e8e6f0;
    --text-dim: #8888a0;
    --card-bg: rgba(255,255,255,0.04);
    --border: rgba(255,255,255,0.08);
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg); color: var(--text);
    font-family: "Microsoft YaHei","PingFang SC",sans-serif;
    line-height:1.7; padding:40px;
    max-width:1100px; margin:0 auto;
  }
  h1 {
    font-size:28px; font-weight:700; letter-spacing:2px;
    text-align:center; margin-bottom:8px;
    text-shadow: 0 0 30px rgba(123,111,158,0.3);
  }
  .subtitle { text-align:center; color:var(--text-dim); font-size:14px; margin-bottom:40px; }

  .section {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 28px; margin-bottom: 28px;
  }
  .section h2 {
    font-size:20px; margin-bottom:16px;
    display:flex; align-items:center; gap:10px;
  }
  .section h2 .icon { font-size:22px; }

  .stats-grid {
    display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
    gap:14px; margin-bottom:20px;
  }
  .stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 16px;
  }
  .stat-card .label { font-size:12px; color:var(--text-dim); margin-bottom:4px; }
  .stat-card .value { font-size:26px; font-weight:700; }
  .stat-card .note { font-size:11px; color:var(--text-dim); margin-top:4px; }

  table { width:100%; border-collapse:collapse; margin:16px 0; }
  th, td { padding:10px 16px; text-align:left; }
  th {
    font-size:12px; color:var(--text-dim); font-weight:500;
    border-bottom:1px solid var(--border);
  }
  td { font-size:14px; border-bottom:1px solid rgba(255,255,255,0.04); }
  tr:last-child td { border-bottom:none; }

  .bar-container { display:flex; align-items:center; gap:10px; }
  .bar-track {
    flex:1; height:12px; background:rgba(255,255,255,0.06);
    border-radius:6px; overflow:hidden;
  }
  .bar-fill {
    height:100%; border-radius:6px;
    transition: width 0.6s ease;
  }
  .bar-label { min-width:50px; text-align:right; font-size:13px; font-weight:600; }
  .bar-ref { min-width:80px; font-size:12px; color:var(--text-dim); text-align:right; }

  .highlight { color:var(--amber); font-weight:600; }
  .tag {
    display:inline-block; padding:3px 10px; border-radius:12px;
    font-size:11px; margin:2px 4px;
  }
  .tag-purple { background:rgba(123,111,158,0.2); color:var(--purple); }
  .tag-coral { background:rgba(212,117,107,0.2); color:var(--coral); }
  .tag-teal { background:rgba(74,144,164,0.2); color:var(--teal); }
  .tag-amber { background:rgba(200,146,62,0.2); color:var(--amber); }

  .insight {
    background: rgba(200,146,62,0.08);
    border-left: 3px solid var(--amber);
    padding: 14px 18px; border-radius: 0 12px 12px 0;
    margin: 16px 0; font-size:13px;
  }
  .insight strong { color:var(--amber); }

  footer {
    text-align:center; color:var(--text-dim); font-size:12px;
    padding: 40px 0 20px;
  }

  .combo-row { display:flex; gap:16px; flex-wrap:wrap; margin:12px 0; }
  .combo-chip {
    background:rgba(255,255,255,0.04);
    border:1px solid var(--border);
    border-radius:10px; padding:12px 18px;
    text-align:center; min-width:130px;
  }
  .combo-chip .pct { font-size:22px; font-weight:700; margin-bottom:4px; }
  .combo-chip .label { font-size:12px; color:var(--text-dim); }
</style>
</head>
<body>

<h1>黎明之后 · 牌库抽取概率报告</h1>
<p class="subtitle">Python 蒙特卡洛模拟 · 反击卡 / 物资卡 / 规则卡</p>

'''
    # ====== 反击卡 ======
    c = COUNTER_RESULTS
    html += '''
<div class="section">
  <h2><span class="icon">⚔️</span> 反击卡抽取模拟</h2>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">模拟局数</div>
      <div class="value" style="color:var(--purple)">''' + str(c['total_games']) + '''</div>
    </div>
    <div class="stat-card">
      <div class="label">总抽取张数</div>
      <div class="value" style="color:var(--coral)">''' + str(c['total_draws']) + '''</div>
    </div>
    <div class="stat-card">
      <div class="label">平均每局抽取</div>
      <div class="value" style="color:var(--teal)">''' + f"{c['avg_draws_per_game']:.1f}" + '''</div>
      <div class="note">牌库总量 62 张</div>
    </div>
    <div class="stat-card">
      <div class="label">每局牌库消耗率</div>
      <div class="value" style="color:var(--amber)">''' + f"{c['avg_draws_per_game']/62*100:.1f}%" + '''</div>
    </div>
  </div>

  <table>
    <tr><th>等级</th><th>抽取张数</th><th>实际概率</th><th>vs 牌库占比</th><th>分布</th></tr>
'''
    for level in ["基础", "觉醒", "极致", "真理"]:
        cnt = c["counts"].get(level, 0)
        pct = c["percentages"].get(level, 0)
        pool_pct = {"基础": 36, "觉醒": 16, "极致": 8, "真理": 2}[level]
        pool_p = pool_pct / 62 * 100
        diff = pct - pool_p
        diff_str = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"
        diff_color = "var(--coral)" if diff > 0 else "var(--teal)"
        color = {"基础":"var(--coral)","觉醒":"var(--teal)","极致":"var(--amber)","真理":"var(--purple)"}[level]
        html += f'''
    <tr>
      <td><span class="tag tag-{({"基础":"coral","觉醒":"teal","极致":"amber","真理":"purple"}[level])}">{level}</span></td>
      <td>{cnt} 张</td>
      <td><strong>{pct:.1f}%</strong></td>
      <td>牌库 {pool_p:.1f}% <span style="color:{diff_color}">({diff_str})</span></td>
      <td>
        <div class="bar-container">
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{color}"></div></div>
          <div class="bar-label">{pct:.1f}%</div>
        </div>
      </td>
    </tr>'''

    html += '''
  </table>

  <div class="insight">
    <strong>💡 关键发现：</strong>
    开局A初始（自选1基础+随机2张）占总抽取量的最大比重。
    基础卡占比最高（自选机制确保至少1张），真理卡最低（仅2张）。<br>
    实际抽取分布接近牌库天然占比——抽取机制设计合理，无明显偏向。
  </div>
</div>
'''

    # ====== 物资卡 ======
    s = SUPPLY_RESULTS
    html += '''
<div class="section">
  <h2><span class="icon">📦</span> 物资卡抽取模拟</h2>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">官方物资平均耗尽回合</div>
      <div class="value" style="color:var(--amber)">''' + f"第{s['official']['avg_exhaust_turn']:.1f}回合" + '''</div>
    </div>
    <div class="stat-card">
      <div class="label">官方物资耗尽概率</div>
      <div class="value" style="color:var(--coral)">''' + f"{s['official']['exhaust_rate']:.1f}%" + '''</div>
      <div class="note">18张库存，每回合可选抽3张</div>
    </div>
    <div class="stat-card">
      <div class="label">普通物资总抽取</div>
      <div class="value" style="color:var(--teal)">''' + str(s['normal']['total']) + '''</div>
      <div class="note">63张普通牌库</div>
    </div>
  </div>

  <h3 style="margin-top:20px;margin-bottom:10px;font-size:15px;">普通物资牌库 各等级抽取分布</h3>
  <table>
    <tr><th>等级</th><th>抽取张数</th><th>概率</th><th>牌库占比</th><th>分布</th></tr>
'''
    pool_pcts = {"普通物资": 34/63*100, "中级物资": 18/63*100, "高级物资": 8/63*100, "绝顶物资": 3/63*100}
    colors = {"普通物资":"var(--teal)","中级物资":"var(--purple)","高级物资":"var(--amber)","绝顶物资":"var(--coral)"}
    for name, pct in sorted(s["normal_percentages"].items(), key=lambda x: -x[1]):
        cnt = s["normal"]["counts"].get(name, 0)
        pool_p = pool_pcts.get(name, 0)
        diff = pct - pool_p
        diff_str = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"
        diff_color = "var(--coral)" if diff > 0 else "var(--teal)"
        color = colors.get(name, "var(--teal)")
        html += f'''
    <tr>
      <td>{name}</td>
      <td>{cnt} 张</td>
      <td><strong>{pct:.1f}%</strong></td>
      <td>{pool_p:.1f}% <span style="color:{diff_color}">({diff_str})</span></td>
      <td>
        <div class="bar-container">
          <div class="bar-track"><div class="bar-fill" style="width:{pct*1.5}%;background:{color}"></div></div>
          <div class="bar-label">{pct:.1f}%</div>
        </div>
      </td>
    </tr>'''

    html += '''
  </table>

  <div class="insight">
    <strong>💡 关键发现：</strong>
    官方物资（保障餐A）是确定性补给——每回合固定可选3张，18张库存大约在第''' + f"{s['official']['avg_exhaust_turn']:.0f}" + '''回合耗尽。<br>
    地图探索的物资分布完全等于牌库天然占比——抽取是均匀随机的，无偏向。<br>
    官方物资耗尽后，玩家必须转向地图探索，风险（撞鬼）与收益并存。
  </div>
</div>
'''

    # ====== 规则卡 ======
    r = RULE_RESULTS
    html += '''
<div class="section">
  <h2><span class="icon">📜</span> 规则卡抽取模拟</h2>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">模拟局数</div>
      <div class="value" style="color:var(--purple)">''' + str(r['total_games']) + '''</div>
    </div>
    <div class="stat-card">
      <div class="label">每局抽取</div>
      <div class="value" style="color:var(--coral)">''' + str(r['draw_count']) + ''' 张</div>
      <div class="note">人类数-1（6人局=5张）</div>
    </div>
    <div class="stat-card">
      <div class="label">牌库总量</div>
      <div class="value" style="color:var(--teal)">52 张</div>
      <div class="note">28普通 + 24特殊</div>
    </div>
  </div>

  <table>
    <tr><th>规则类型</th><th>抽取张数</th><th>概率</th><th>牌库占比</th><th>分布</th></tr>
'''
    pool_pcts_r = {"T1_普通": 4/52*100, "T2_普通": 20/52*100, "T3_普通": 4/52*100, "特殊": 24/52*100}
    colors_r = {"T1_普通":"var(--coral)","T2_普通":"var(--teal)","T3_普通":"var(--purple)","特殊":"var(--amber)"}
    labels_r = {"T1_普通":"T1·普通","T2_普通":"T2·普通","T3_普通":"T3·普通","特殊":"特殊规则"}
    for rt in ["T1_普通", "T2_普通", "T3_普通", "特殊"]:
        cnt = r["counts"].get(rt, 0)
        pct = r["percentages"].get(rt, 0)
        pool_p = pool_pcts_r[rt]
        diff = pct - pool_p
        diff_str = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"
        diff_color = "var(--coral)" if diff > 0 else "var(--teal)"
        color = colors_r[rt]
        html += f'''
    <tr>
      <td>{labels_r[rt]}</td>
      <td>{cnt} 张</td>
      <td><strong>{pct:.1f}%</strong></td>
      <td>{pool_p:.1f}% <span style="color:{diff_color}">({diff_str})</span></td>
      <td>
        <div class="bar-container">
          <div class="bar-track"><div class="bar-fill" style="width:{pct*1.8}%;background:{color}"></div></div>
          <div class="bar-label">{pct:.1f}%</div>
        </div>
      </td>
    </tr>'''

    html += '''
  </table>

  <h3 style="margin-top:20px;margin-bottom:10px;font-size:15px;">开局手牌组合概率</h3>
  <div class="combo-row">
'''
    combo_labels = {
        "no_T1": "未抽到T1规则",
        "no_special": "未抽到特殊规则",
        "all_high": "全是T2/T3",
        "multi_special": "≥2张特殊规则",
    }
    for key, pct in r["combo_stats"].items():
        color = "var(--coral)" if pct > 50 else "var(--amber)" if pct > 25 else "var(--teal)"
        html += f'''
    <div class="combo-chip">
      <div class="pct" style="color:{color}">{pct:.1f}%</div>
      <div class="label">{combo_labels.get(key, key)}</div>
    </div>'''

    html += '''
  </div>

  <h3 style="margin-top:20px;margin-bottom:10px;font-size:15px;">手中特殊规则张数分布</h3>
  <div class="combo-row">
'''
    for k, pct in r["special_distribution"].items():
        color = "var(--amber)" if k >= 3 else "var(--coral)" if k == 2 else "var(--teal)"
        html += f'''
    <div class="combo-chip">
      <div class="pct" style="color:{color}">{pct:.1f}%</div>
      <div class="label">{int(k)}张特殊规则</div>
    </div>'''

    html += '''
  </div>

  <div class="insight">
    <strong>💡 关键发现：</strong>
    特殊规则（24张）占总牌库的46.2%，5张手牌中<span class="highlight">期望含约2.3张特殊规则</span>。<br>
    T1规则仅4张（7.7%），未抽到的概率为''' + f"{r['combo_stats']['no_T1']:.1f}%" + '''——大多数开局鬼手中没有"简单规则"可出。<br>
    这意味着鬼的隐藏规则以T2（难度中等）和特殊规则为主，推理难度适中。
  </div>
</div>
'''

    html += '''
<footer>
  《黎明之后》牌库抽取概率报告 · Python蒙特卡洛模拟生成 · ''' + f"{c['total_games']}局反击卡 + {s['total_games']}局物资卡 + {r['total_games']}局规则卡" + '''
</footer>
</body>
</html>
'''
    return html


if __name__ == "__main__":
    run_all()

    # 生成HTML报告
    html = generate_html_report()
    report_path = "website/抽卡概率报告.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n📄 HTML报告已保存: {report_path}")
