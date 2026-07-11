#!/usr/bin/env python3
"""Splice new Tab 4 CSS/HTML/JS into docs/citizen.html"""

import sys

# ── Paths ──
SRC = r'C:\Users\80526\WorkBuddy\2026-06-05-15-49-56\docs\citizen.html'
DST = SRC  # in-place replacement

# ====================================================================
# NEW TAB 4 CSS (replaces lines 636-1607, 0-indexed: 635-1606)
# ====================================================================
NEW_CSS = r'''
/* ============================================================
   Tab 4: 实战面板 — 市民个人实战游戏面板
   ============================================================ */

/* -- 回合计数器 + 按钮 -- */
.round-counter-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 10px 16px;
  background: var(--bg-elevated);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-subtle);
  flex-wrap: wrap;
}
.round-counter-num {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-counter-glow);
  line-height: 1;
  min-width: 40px;
  text-align: center;
  transition: transform 0.2s;
}
.round-counter-num.pulse { animation: badgePulse 0.35s ease-out; }
.round-counter-label {
  font-size: 0.7rem;
  color: var(--text-muted);
  letter-spacing: 0.05em;
}
.round-btn {
  padding: 8px 18px;
  border-radius: var(--radius-xl);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
}
.round-btn.dawn-btn {
  background: rgba(212,160,23,0.12);
  color: var(--color-rule-glow);
  border-color: rgba(212,160,23,0.25);
}
.round-btn.dawn-btn:hover { background: rgba(212,160,23,0.2); }
.round-btn.end-btn {
  background: rgba(192,57,43,0.1);
  color: var(--color-whisper-glow);
  border-color: rgba(192,57,43,0.2);
}
.round-btn.end-btn:hover { background: rgba(192,57,43,0.18); }

/* -- 三组搜索栏（横向排列） -- */
.search-bars-row {
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 660px;
  flex-wrap: wrap;
}
.search-bar-col {
  flex: 1;
  min-width: 170px;
  position: relative;
}
.search-bar-label {
  font-size: 0.68rem;
  color: var(--text-muted);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}
.search-bar-label.l-whisper { color: var(--color-whisper-glow); }
.search-bar-label.l-counter { color: var(--color-counter-glow); }
.search-bar-label.l-supply { color: var(--color-supply-glow); }
.search-bar-input-wrap {
  position: relative;
}
.search-bar-input {
  width: 100%;
  background: var(--bg-deep);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 8px 32px 8px 12px;
  color: var(--text-primary);
  font-size: 0.78rem;
  outline: none;
  box-sizing: border-box;
}
.search-bar-input:focus {
  border-color: var(--color-counter);
}
.search-bar-input::placeholder {
  color: var(--text-muted);
  font-size: 0.7rem;
}
.search-bar-clear {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 0.85rem;
  cursor: pointer;
  display: none;
  padding: 2px 4px;
}
.search-bar-clear.visible { display: block; }
.search-bar-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
  max-height: 200px;
  overflow-y: auto;
  z-index: 50;
  display: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.search-bar-results.show { display: block; }
.search-bar-result-item {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 0.78rem;
  color: var(--text-primary);
  transition: background 0.15s;
  display: flex;
  align-items: center;
  gap: 6px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.search-bar-result-item:last-child { border-bottom: none; }
.search-bar-result-item:hover,
.search-bar-result-item.focused {
  background: rgba(46,134,193,0.12);
}
.search-bar-result-item .sbr-name { flex: 1; }
.search-bar-result-item .sbr-level {
  font-size: 0.65rem;
  color: var(--text-muted);
}

/* -- 结算栏（回合计分状态） -- */
.play-status-row {
  display: flex;
  gap: 20px;
  padding: 4px 0;
  font-size: 0.7rem;
  color: var(--text-muted);
  flex-wrap: wrap;
  justify-content: center;
}
.play-status-row b { font-weight: 700; }

/* -- 主游戏场景 -- */
.play-scene-wrap {
  width: 100%;
  max-width: 560px;
  margin: 0 auto;
}
.play-scene {
  position: relative;
  width: 100%;
  height: 460px;
  background: radial-gradient(ellipse at center, rgba(46,134,193,0.03) 0%, transparent 70%);
  border: 1px dashed rgba(255,255,255,0.05);
  border-radius: 12px;
  overflow: hidden;
}

/* 角色卡（锚点） */
.play-char {
  position: absolute;
  width: 130px; height: 182px;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: 0 0 16px rgba(255,255,255,0.08), var(--shadow-md);
  border: 2px solid var(--color-character);
  z-index: 100;
  background: var(--bg-card);
  cursor: pointer;
  transition: box-shadow 0.3s;
}
.play-char:hover { box-shadow: 0 0 24px rgba(142,68,173,0.2), var(--shadow-md); }
.play-char img { width: 100%; height: 100%; object-fit: cover; }

/* 场景内方向标签 */
.play-dir-label {
  position: absolute;
  font-size: 0.58rem;
  color: var(--text-muted);
  opacity: 0.45;
  pointer-events: none;
  z-index: 5;
}

/* 场景内卡片通用 */
.play-card {
  position: absolute;
  border-radius: var(--radius-sm);
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.35);
  background: var(--bg-card);
  transition: left 0.35s ease, right 0.35s ease, top 0.35s ease, opacity 0.25s;
  cursor: pointer;
}
.play-card img { width: 100%; height: 100%; object-fit: cover; }
.play-card .play-card-label {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 2px 4px;
  background: rgba(0,0,0,0.75);
  color: var(--text-muted);
  font-size: 0.5rem;
  text-align: center;
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
}
.play-card:hover .play-card-label { opacity: 1; }

/* 专用颜色边框 */
.play-right  { box-shadow: 0 2px 8px rgba(46,134,193,0.2); }
.play-left   { box-shadow: 0 2px 8px rgba(192,57,43,0.2); }
.play-top    { box-shadow: 0 2px 8px rgba(231,76,60,0.2); }
.play-bottom { box-shadow: 0 2px 8px rgba(39,174,96,0.2); }

/* 未激活反击卡（卡背） */
.play-card.inactive-card {
  border: 2px solid var(--color-counter);
}
.play-card-back {
  width: 100%; height: 100%;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: var(--color-counter-glow);
  font-size: 0.68rem;
}
.play-card-back .pcb-icon { font-size: 1.5rem; opacity: 0.6; }
.play-card-back .pcb-label { font-size: 0.6rem; opacity: 0.5; }

/* -- 物资卡手牌条（场景下方） -- */
.supply-hand-wrap {
  width: 100%;
  max-width: 560px;
}
.supply-hand-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2px 4px 6px;
  font-size: 0.7rem;
  color: var(--text-muted);
}
.supply-hand-strip {
  display: flex;
  gap: 8px;
  padding: 4px 0;
  overflow-x: auto;
  align-items: flex-start;
  min-height: 88px;
}
.supply-hand-empty {
  color: var(--text-muted);
  font-size: 0.72rem;
  padding: 16px 0;
  width: 100%;
  text-align: center;
  opacity: 0.5;
}
.supply-hand-card {
  width: 84px;
  height: 118px;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  border: 2px solid var(--border-subtle);
  background: var(--bg-card);
  flex-shrink: 0;
  transition: transform 0.15s, border-color 0.2s, box-shadow 0.2s;
  position: relative;
}
.supply-hand-card:active { transform: scale(0.95); }
.supply-hand-card:hover { border-color: var(--color-supply); box-shadow: 0 2px 10px rgba(39,174,96,0.2); }
.supply-hand-card img { width: 100%; height: 100%; object-fit: cover; }
.supply-hand-card .shc-name {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 3px 4px;
  background: rgba(0,0,0,0.75);
  color: var(--text-muted);
  font-size: 0.55rem;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 已激活计数器标签 */
.active-zone-indicator {
  font-size: 0.7rem;
  color: var(--color-counter-glow);
  padding: 2px 0;
  text-align: center;
  font-weight: 600;
}

/* 场景图例 */
.scene-legend {
  display: flex;
  gap: 12px;
  font-size: 0.62rem;
  color: var(--text-muted);
  flex-wrap: wrap;
  justify-content: center;
  padding: 4px 0 0;
}
.scene-legend .sldot { width: 7px; height: 7px; border-radius: 2px; flex-shrink: 0; }

/* -- 抽屉（弃牌堆 + 对他人使用） -- */
.drawer-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 500;
  display: none;
  justify-content: center;
  align-items: flex-end;
}
.drawer-overlay.open { display: flex; }
.drawer-panel {
  background: var(--bg-surface);
  border-radius: 16px 16px 0 0;
  width: 100%;
  max-width: 500px;
  max-height: 65vh;
  overflow-y: auto;
  padding: 16px;
  border: 1px solid var(--border-subtle);
  border-bottom: none;
  animation: drawerSlideUp 0.25s ease-out;
}
@keyframes drawerSlideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-subtle);
}
.drawer-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}
.drawer-close {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px 8px;
}
.drawer-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-start;
}
.drawer-card-item {
  width: 80px;
  text-align: center;
  cursor: pointer;
}
.drawer-card-thumb {
  width: 80px;
  height: 112px;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  background: var(--bg-card);
  transition: transform 0.15s;
  margin-bottom: 4px;
}
.drawer-card-thumb:active { transform: scale(0.95); }
.drawer-card-thumb img { width: 100%; height: 100%; object-fit: cover; }
.drawer-card-name {
  font-size: 0.6rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.drawer-empty {
  color: var(--text-muted);
  font-size: 0.75rem;
  padding: 20px;
  text-align: center;
  width: 100%;
  opacity: 0.5;
}

/* -- 操作菜单（卡片点击浮窗） -- */
.action-menu-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  z-index: 400;
  display: none;
  justify-content: center;
  align-items: center;
}
.action-menu-overlay.open { display: flex; }
.action-menu {
  background: var(--bg-surface);
  border-radius: 14px;
  padding: 20px;
  border: 1px solid var(--border-subtle);
  min-width: 240px;
  max-width: 320px;
  animation: menuPopIn 0.2s ease-out;
}
@keyframes menuPopIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.action-menu-title {
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-primary);
  text-align: center;
  word-break: break-all;
}
.action-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 14px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.84rem;
  color: var(--text-primary);
  transition: background 0.15s;
  margin-bottom: 3px;
}
.action-menu-item:hover { background: rgba(46,134,193,0.1); }
.action-menu-item .ami-icon { font-size: 1.1rem; width: 26px; text-align: center; flex-shrink: 0; }
.action-menu-item .ami-label { flex: 1; }
.action-menu-cancel {
  display: block;
  width: 100%;
  margin-top: 10px;
  padding: 10px;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.8rem;
}

/* -- 卡牌详情弹窗 -- */
.card-detail-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.7);
  z-index: 600;
  display: none;
  justify-content: center;
  align-items: center;
}
.card-detail-overlay.open { display: flex; }
.card-detail-dialog {
  background: var(--bg-surface);
  border-radius: 14px;
  padding: 20px;
  max-width: 380px;
  width: 90%;
  border: 1px solid var(--border-subtle);
  text-align: center;
  animation: menuPopIn 0.2s ease-out;
}
.card-detail-dialog img {
  max-width: 100%;
  max-height: 260px;
  border-radius: 8px;
  margin-bottom: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
.card-detail-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.card-detail-meta {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 10px;
}
.card-detail-effect {
  font-size: 0.78rem;
  color: var(--text-secondary);
  background: var(--bg-deep);
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  margin-bottom: 14px;
  text-align: left;
  line-height: 1.5;
  max-height: 150px;
  overflow-y: auto;
}
.card-detail-close {
  padding: 8px 28px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 0.82rem;
  transition: background 0.15s;
}
.card-detail-close:hover { background: var(--bg-surface); }

/* -- 回合结束确认 -- */
.confirm-mini-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 400;
  display: none;
  justify-content: center;
  align-items: center;
}
.confirm-mini-overlay.open { display: flex; }
.confirm-mini-dialog {
  background: var(--bg-surface);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-subtle);
  min-width: 260px;
  animation: menuPopIn 0.2s ease-out;
}
.confirm-mini-dialog .cmd-title { font-weight: 600; margin-bottom: 8px; color: var(--text-primary); }
.confirm-mini-dialog .cmd-body { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 16px; }
.confirm-mini-actions { display: flex; gap: 10px; justify-content: center; }
.confirm-mini-btn {
  padding: 8px 20px;
  border-radius: var(--radius-xl);
  cursor: pointer;
  border: 1px solid var(--border-subtle);
  font-size: 0.8rem;
  transition: all 0.15s;
}
.confirm-mini-btn.cancel { background: transparent; color: var(--text-muted); }
.confirm-mini-btn.ok { background: var(--color-counter); color: #fff; border-color: var(--color-counter); }

/* -- 场景响应式 -- */
@media (max-width: 600px) {
  .play-scene { height: 360px; }
  .play-char { width: 100px; height: 140px; }
  .search-bars-row { flex-direction: column; gap: 6px; }
  .search-bar-col { min-width: 0; }
  .supply-hand-card { width: 66px; height: 92px; }
  .drawer-card-thumb { width: 64px; height: 90px; }
  .round-counter-num { font-size: 1.6rem; min-width: 32px; }
  .round-btn { padding: 6px 12px; font-size: 0.75rem; }
}
'''

# ====================================================================
# NEW TAB 4 HTML (replaces lines 1757-1909, 0-indexed: 1756-1908)
# ====================================================================
NEW_HTML = r'''
  <!-- ========== Tab 4: 实战面板 ========== -->
  <div class="test-panel active" id="panel-play">

    <!-- 1. 回合计数器 -->
    <div class="round-counter-wrap" id="roundCounter">
      <button class="round-btn dawn-btn" onclick="playDawnAction()" title="推进至下一回合黎明">🌅 迎接黎明</button>
      <div class="round-counter-num" id="roundNum">0</div>
      <div class="round-counter-label">回合 / 12</div>
      <button class="round-btn end-btn" onclick="playEndRound()" title="结束当前回合">🌙 回合结束</button>
    </div>

    <!-- 2. 结算状态栏 -->
    <div class="play-status-row" id="playStatusRow">
      怪谈<b style="color:var(--color-whisper-glow)" id="playCntWL">0</b>
      &nbsp;·&nbsp; 未激活<b style="color:var(--text-muted)" id="playCntIA">0</b>
      &nbsp;·&nbsp; 已激活<b style="color:var(--color-counter-glow)" id="playCntAC">0</b>
      &nbsp;·&nbsp; 物资<b style="color:var(--color-supply-glow)" id="playCntSP">0</b>
      &nbsp;·&nbsp; 伤害<b style="color:#e74c3c" id="playCntDM">0</b>
      &nbsp;·&nbsp; 弃牌<b style="color:var(--text-muted)" id="playCntDC">0</b>
    </div>

    <!-- 3. 三组搜索栏 -->
    <div class="search-bars-row" id="searchBars">
      <!-- 怪谈卡搜索 -->
      <div class="search-bar-col" id="searchColWhisper">
        <div class="search-bar-label l-whisper">👻 怪谈卡</div>
        <div class="search-bar-input-wrap">
          <input class="search-bar-input" id="searchWhisper" type="text"
                 placeholder="搜索怪谈卡名称…" autocomplete="off"
                 oninput="onSearchBar('whisper',this.value)"
                 onfocus="onSearchBar('whisper',this.value)">
          <button class="search-bar-clear" id="clearWhisper" onclick="clearSearchBar('whisper')">✕</button>
        </div>
        <div class="search-bar-results" id="resultsWhisper"></div>
      </div>
      <!-- 反击卡搜索 -->
      <div class="search-bar-col" id="searchColCounter">
        <div class="search-bar-label l-counter">🃏 反击卡</div>
        <div class="search-bar-input-wrap">
          <input class="search-bar-input" id="searchCounter" type="text"
                 placeholder="搜索反击卡名称…" autocomplete="off"
                 oninput="onSearchBar('counter',this.value)"
                 onfocus="onSearchBar('counter',this.value)">
          <button class="search-bar-clear" id="clearCounter" onclick="clearSearchBar('counter')">✕</button>
        </div>
        <div class="search-bar-results" id="resultsCounter"></div>
      </div>
      <!-- 物资卡搜索 -->
      <div class="search-bar-col" id="searchColSupply">
        <div class="search-bar-label l-supply">🎒 物资卡</div>
        <div class="search-bar-input-wrap">
          <input class="search-bar-input" id="searchSupply" type="text"
                 placeholder="搜索物资卡名称…" autocomplete="off"
                 oninput="onSearchBar('supply',this.value)"
                 onfocus="onSearchBar('supply',this.value)">
          <button class="search-bar-clear" id="clearSupply" onclick="clearSearchBar('supply')">✕</button>
        </div>
        <div class="search-bar-results" id="resultsSupply"></div>
      </div>
    </div>

    <!-- 已激活反击卡指示 -->
    <div class="active-zone-indicator" id="activeZoneLabel" style="display:none;">
      ✅ 已激活反击卡（右侧堆叠·点击操作）
    </div>

    <!-- 4. 主游戏场景 -->
    <div class="play-scene-wrap">
      <div class="play-scene" id="playScene">
        <!-- 方向标签 -->
        <div class="play-dir-label" style="top:4px;left:50%;transform:translateX(-50%);">⬆ 伤害指示卡</div>
        <div class="play-dir-label" style="top:50%;left:4px;transform:translateY(-50%);">⬅ 怪谈卡</div>
        <div class="play-dir-label" style="top:50%;right:4px;transform:translateY(-50%);">➡ 已激活反击卡</div>
        <div class="play-dir-label" style="bottom:4px;left:50%;transform:translateX(-50%);">⬇ 物资卡</div>

        <!-- 角色卡（锚点） -->
        <div class="play-char" id="playChar" onclick="showCharDetail()" title="点击查看角色详情">
          <img src="images/cards/角色卡/角色卡_命运操控者_乐天派幸存者.png" alt="乐天派幸存者"
            onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
          <div style="display:none;width:100%;height:100%;align-items:center;justify-content:center;background:linear-gradient(135deg,#2d1b3d,#1a1a2e);color:var(--color-character-glow);font-size:0.75rem;font-weight:600;text-align:center;">乐天派<br>幸存者</div>
        </div>

        <!-- 场景内卡片由JS动态生成 -->
      </div>

      <!-- 场景图例 -->
      <div class="scene-legend">
        <span><span class="sldot" style="background:var(--color-whisper-glow)"></span>怪谈(左50px)</span>
        <span><span class="sldot" style="background:var(--text-muted)"></span>未激活(左远50px)</span>
        <span><span class="sldot" style="background:var(--color-counter-glow)"></span>已激活(右50px)</span>
        <span><span class="sldot" style="background:#e74c3c"></span>伤害(上50px)</span>
        <span><span class="sldot" style="background:var(--color-supply-glow)"></span>物资(下70px)</span>
      </div>
    </div>

    <!-- 5. 物资卡手牌条 -->
    <div class="supply-hand-wrap" id="supplyHandWrap">
      <div class="supply-hand-header">
        <span>🎒 物资卡手牌</span>
        <span id="supplyHandCount">0 张</span>
      </div>
      <div class="supply-hand-strip" id="supplyHandStrip">
        <div class="supply-hand-empty">暂无物资卡 · 使用上方搜索栏添加</div>
      </div>
    </div>

    <!-- 6. 隐藏抽屉：弃牌堆 -->
    <div class="drawer-overlay" id="drawerDiscard">
      <div class="drawer-panel">
        <div class="drawer-header">
          <span class="drawer-title">🗑️ 弃牌堆</span>
          <button class="drawer-close" onclick="closeDrawer('discard')">✕</button>
        </div>
        <div class="drawer-cards" id="drawerDiscardCards">
          <div class="drawer-empty">弃牌堆为空</div>
        </div>
      </div>
    </div>

    <!-- 7. 隐藏抽屉：对他人使用 -->
    <div class="drawer-overlay" id="drawerUseOthers">
      <div class="drawer-panel">
        <div class="drawer-header">
          <span class="drawer-title">🔀 对他人使用</span>
          <button class="drawer-close" onclick="closeDrawer('useOthers')">✕</button>
        </div>
        <div class="drawer-cards" id="drawerUseOthersCards">
          <div class="drawer-empty">暂无待处理的卡牌</div>
        </div>
      </div>
    </div>

    <!-- 8. 隐藏操作菜单 -->
    <div class="action-menu-overlay" id="actionMenuOverlay" onclick="closeActionMenu()">
      <div class="action-menu" id="actionMenu" onclick="event.stopPropagation()">
        <div class="action-menu-title" id="actionMenuTitle"></div>
        <div id="actionMenuItems"></div>
        <button class="action-menu-cancel" onclick="closeActionMenu()">取消</button>
      </div>
    </div>

    <!-- 9. 隐藏卡牌详情弹窗 -->
    <div class="card-detail-overlay" id="cardDetailOverlay" onclick="closeCardDetail()">
      <div class="card-detail-dialog" id="cardDetailDialog" onclick="event.stopPropagation()">
        <img id="cardDetailImg" src="" alt="">
        <div class="card-detail-name" id="cardDetailName"></div>
        <div class="card-detail-meta" id="cardDetailMeta"></div>
        <div class="card-detail-effect" id="cardDetailEffect"></div>
        <button class="card-detail-close" onclick="closeCardDetail()">关闭</button>
      </div>
    </div>

    <!-- 10. 回合结束确认 -->
    <div class="confirm-mini-overlay" id="confirmMiniOverlay" onclick="closeConfirmMini()">
      <div class="confirm-mini-dialog" id="confirmMiniDialog" onclick="event.stopPropagation()">
        <div class="cmd-title" id="confirmMiniTitle">确认操作</div>
        <div class="cmd-body" id="confirmMiniBody"></div>
        <div class="confirm-mini-actions">
          <button class="confirm-mini-btn cancel" onclick="closeConfirmMini()">取消</button>
          <button class="confirm-mini-btn ok" id="confirmMiniOk">确认</button>
        </div>
      </div>
    </div>

  </div>
'''

# ====================================================================
# NEW TAB 4 JS (replaces lines 2516-3385, 0-indexed: 2515-3384)
# ====================================================================
NEW_JS = r'''
initPlayPanel();

// ============================================================
// Tab 4: 实战面板 — 完整JS逻辑
// ============================================================

// ─── 回合指示卡 ───
const DAY_NAMES = ['零','一','二','三','四','五','六','七','八','九','十','十一','十二'];
const ROUND_INDICATOR_DIR = 'images/cards/回合指示卡/';
const CARD_BACK_URL = 'images/card-back.png';

function getDayName(n) { return '第' + DAY_NAMES[n] + '天'; }
function getRoundCardPath(variant, round) {
  return ROUND_INDICATOR_DIR + '回合指示卡_' + variant + '_' + getDayName(round) + '.png';
}

// ─── 主游戏状态 ───
let PLAY = {
  round: 0,
  scene: {
    whisper: [],    // 怪谈卡（左）
    inactive: [],   // 未激活反击卡（左远·卡背）
    active: [],     // 已激活反击卡（右）
    damage: [],     // 伤害指示卡（上）
    supply: [],     // 已使用物资卡（下）
  },
  supplyHand: [],   // 物资卡手牌
  discard: [],      // 弃牌堆
  useOthers: [],    // 对他人使用队列
  roundHistory: []  // [{round, cards:[4张路径]}]
};

// ─── 场景参数（复刻Tab 3复合堆叠） ───
const PLAY_CHAR_W = 130;
const PLAY_CHAR_H = 182;
const PLAY_STEP_R = 50;  // 已激活反击卡（右）
const PLAY_STEP_L = 50;  // 怪谈卡（左）
const PLAY_STEP_IA = 50; // 未激活反击卡（左远·额外偏移）
const PLAY_STEP_T = 50;  // 伤害卡（上）
const PLAY_STEP_B = 70;  // 物资卡（下）
const PLAY_DAMAGE_H = 100; // 伤害指示卡高度

function getPlayScale() {
  return window.innerWidth <= 600 ? 0.77 : 1;
}

function getPlayCharLeft(s) {
  const sceneW = document.getElementById('playScene').clientWidth;
  const charW = PLAY_CHAR_W * s;
  return (sceneW - charW) / 2;
}

function getPlayCharTop(s) {
  const sceneH = document.getElementById('playScene').clientHeight;
  const charH = PLAY_CHAR_H * s;
  return (sceneH - charH) / 2;
}

// ─── 搜索索引 ───
let SEARCH_IDX = { whisper: [], counter: [], supply: [] };

function buildSearchIndex() {
  if (typeof CARD_DB === 'undefined') return;

  // 怪谈卡：仅名称
  SEARCH_IDX.whisper = (CARD_DB.whispers || []).map(c => ({
    id: c.id, name: c.name, level: c.level || '',
    effect: c.effect || c.description || '',
    img: (typeof getCardImagePath === 'function')
      ? getCardImagePath({ type: 'whispers', level: c.level, name: c.name })
      : ''
  }));

  // 反击卡：名称+等级
  SEARCH_IDX.counter = (CARD_DB.countermeasures || []).map(c => ({
    id: c.id, name: c.name, level: c.level || '',
    effect: c.effect || c.description || '',
    img: (typeof getCardImagePath === 'function')
      ? getCardImagePath({ type: 'countermeasures', level: c.level, name: c.name })
      : ''
  }));

  // 物资卡：名称+等级
  SEARCH_IDX.supply = (CARD_DB.supplies || []).map(c => ({
    id: c.id, name: c.name, level: c.level || '',
    effect: c.effect || c.description || '',
    img: (typeof getCardImagePath === 'function')
      ? getCardImagePath({ type: 'supplies', level: c.level, name: c.name })
      : ''
  }));
}

// ─── 初始化 ───
function initPlayPanel() {
  buildSearchIndex();
  initPlayChar();
  refreshAllPlay();
}

function initPlayChar() {
  const charEl = document.getElementById('playChar');
  const s = getPlayScale();
  const left = getPlayCharLeft(s);
  const top = getPlayCharTop(s);
  charEl.style.left = left + 'px';
  charEl.style.top = top + 'px';
  charEl.style.width = (PLAY_CHAR_W * s) + 'px';
  charEl.style.height = (PLAY_CHAR_H * s) + 'px';
}

// ─── 全局刷新 ───
function refreshAllPlay() {
  refreshPlayScene();
  refreshSupplyHand();
  updatePlayStatus();
}

function refreshPlayScene() {
  buildSceneWhisper();
  buildSceneInactive();
  buildSceneActive();
  buildSceneDamage();
  buildSceneSupply();
  updateActiveZoneLabel();
}

function updatePlayStatus() {
  document.getElementById('playCntWL').textContent = PLAY.scene.whisper.length;
  document.getElementById('playCntIA').textContent = PLAY.scene.inactive.length;
  document.getElementById('playCntAC').textContent = PLAY.scene.active.length;
  document.getElementById('playCntSP').textContent = PLAY.supplyHand.length;
  document.getElementById('playCntDM').textContent = PLAY.scene.damage.length;
  document.getElementById('playCntDC').textContent = PLAY.discard.length;
  document.getElementById('supplyHandCount').textContent = PLAY.supplyHand.length + ' 张';
  document.getElementById('roundNum').textContent = PLAY.round;
}

function updateActiveZoneLabel() {
  const lbl = document.getElementById('activeZoneLabel');
  if (PLAY.scene.active.length > 0) {
    lbl.style.display = 'block';
  } else {
    lbl.style.display = 'none';
  }
}

// ─── 场景构建：通用工具 ───
function clearPlayCards(prefix) {
  const scene = document.getElementById('playScene');
  scene.querySelectorAll('.play-card-' + prefix).forEach(el => el.remove());
}

function createPlayCard(scene, prefix, card, idx, N, style, extraClass, clickHandler) {
  const div = document.createElement('div');
  div.className = 'play-card ' + (extraClass || '') + ' play-card-' + prefix;
  Object.assign(div.style, style);
  div.onclick = function(e) {
    e.stopPropagation();
    if (clickHandler) clickHandler(card, idx);
  };

  if (extraClass === 'inactive-card') {
    // 卡背渲染
    div.title = '未激活反击卡：点击操作';
    div.innerHTML = '<div class="play-card-back">' +
      '<span class="pcb-icon">🃏</span>' +
      '<span class="pcb-label">反击卡</span>' +
      '</div>' +
      '<div class="play-card-label">未激活 · ' + (N - idx) + '</div>';
  } else {
    div.title = '点击操作「' + (card.name || '') + '」（图层-' + (N - idx) + '）';
    if (card.img) {
      div.innerHTML = '<img src="' + card.img + '" alt="' + (card.name || '') + '"' +
        ' onerror="this.style.background=\'#1a1a2e\';this.alt=\'' + (card.name || '') + '\';">' +
        '<div class="play-card-label">' + (card.name || '') + ' · L-' + (N - idx) + '</div>';
    } else {
      div.innerHTML = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#1a1a2e;color:var(--text-muted);font-size:0.7rem;">' + (card.name || '') + '</div>';
    }
  }

  const charEl = document.getElementById('playChar');
  scene.insertBefore(div, charEl);
  return div;
}

// ─── 场景构建：怪谈卡（左） ───
function buildSceneWhisper() {
  clearPlayCards('whisper');
  const scene = document.getElementById('playScene');
  const s = getPlayScale();
  const charLeft = getPlayCharLeft(s);
  const charTop = getPlayCharTop(s);
  const charW = PLAY_CHAR_W * s;
  const charH = PLAY_CHAR_H * s;
  const step = PLAY_STEP_L * s;
  const stack = PLAY.scene.whisper;
  const N = stack.length;
  if (N === 0) return;

  for (let i = 0; i < N; i++) {
    const card = stack[i];
    const left = charLeft - step * (i + 1);
    const z = N - i;
    createPlayCard(scene, 'whisper', card, i, N, {
      left: left + 'px',
      top: charTop + 'px',
      width: charW + 'px',
      height: charH + 'px',
      zIndex: z
    }, 'play-left', function(c) { showWhisperMenu(c); });
  }
}

// ─── 场景构建：未激活反击卡（左远·卡背） ───
function buildSceneInactive() {
  clearPlayCards('inactive');
  const scene = document.getElementById('playScene');
  const s = getPlayScale();
  const charLeft = getPlayCharLeft(s);
  const charTop = getPlayCharTop(s);
  const charW = PLAY_CHAR_W * s;
  const charH = PLAY_CHAR_H * s;
  const stepL = PLAY_STEP_L * s;
  const stepIA = PLAY_STEP_IA * s;
  const stack = PLAY.scene.inactive;
  const N = stack.length;
  if (N === 0) return;

  // 未激活卡在怪谈卡更左侧：基础偏移 = 怪谈卡最远位置 + 额外步长
  const whisperCount = PLAY.scene.whisper.length;
  const baseOffset = stepL * whisperCount;

  for (let i = 0; i < N; i++) {
    const card = stack[i];
    const left = charLeft - baseOffset - stepIA * (i + 1);
    const z = N - i + 10; // 比怪谈卡稍高z-index
    createPlayCard(scene, 'inactive', card, i, N, {
      left: left + 'px',
      top: charTop + 'px',
      width: charW + 'px',
      height: charH + 'px',
      zIndex: z
    }, 'inactive-card play-left', function(c) { showInactiveMenu(c); });
  }
}

// ─── 场景构建：已激活反击卡（右） ───
function buildSceneActive() {
  clearPlayCards('active');
  const scene = document.getElementById('playScene');
  const s = getPlayScale();
  const charLeft = getPlayCharLeft(s);
  const charTop = getPlayCharTop(s);
  const charW = PLAY_CHAR_W * s;
  const charH = PLAY_CHAR_H * s;
  const step = PLAY_STEP_R * s;
  const stack = PLAY.scene.active;
  const N = stack.length;
  if (N === 0) return;

  for (let i = 0; i < N; i++) {
    const card = stack[i];
    const left = charLeft + step * (i + 1);
    const z = N - i;
    createPlayCard(scene, 'active', card, i, N, {
      left: left + 'px',
      top: charTop + 'px',
      width: charW + 'px',
      height: charH + 'px',
      zIndex: z
    }, 'play-right', function(c) { showActiveMenu(c); });
  }
}

// ─── 场景构建：伤害指示卡（上） ───
function buildSceneDamage() {
  clearPlayCards('damage');
  const scene = document.getElementById('playScene');
  const s = getPlayScale();
  const charLeft = getPlayCharLeft(s);
  const charTop = getPlayCharTop(s);
  const charW = PLAY_CHAR_W * s;
  const step = PLAY_STEP_T * s;
  const cardH = PLAY_DAMAGE_H * s;
  const stack = PLAY.scene.damage;
  const N = stack.length;
  if (N === 0) return;

  for (let i = 0; i < N; i++) {
    const card = stack[i];
    const top = charTop - step * (i + 1);
    const z = N - i;
    createPlayCard(scene, 'damage', card, i, N, {
      left: charLeft + 'px',
      top: top + 'px',
      width: charW + 'px',
      height: cardH + 'px',
      zIndex: z
    }, 'play-top', function(c) { showDamageMenu(c); });
  }
}

// ─── 场景构建：已使用物资卡（下） ───
function buildSceneSupply() {
  clearPlayCards('supply');
  const scene = document.getElementById('playScene');
  const s = getPlayScale();
  const charLeft = getPlayCharLeft(s);
  const charTop = getPlayCharTop(s);
  const charW = PLAY_CHAR_W * s;
  const charH = PLAY_CHAR_H * s;
  const step = PLAY_STEP_B * s;
  const stack = PLAY.scene.supply;
  const N = stack.length;
  if (N === 0) return;

  for (let i = 0; i < N; i++) {
    const card = stack[i];
    const top = charTop + step * (i + 1);
    const z = N - i;
    createPlayCard(scene, 'supply', card, i, N, {
      left: charLeft + 'px',
      top: top + 'px',
      width: charW + 'px',
      height: charH + 'px',
      zIndex: z
    }, 'play-bottom', function(c) { showSupplyUsedMenu(c); });
  }
}

// ─── 物资卡手牌条 ───
function refreshSupplyHand() {
  const strip = document.getElementById('supplyHandStrip');
  const cards = PLAY.supplyHand;
  if (cards.length === 0) {
    strip.innerHTML = '<div class="supply-hand-empty">暂无物资卡 · 使用上方搜索栏添加</div>';
    return;
  }
  strip.innerHTML = cards.map((c, i) =>
    '<div class="supply-hand-card" onclick="showSupplyHandMenu(' + i + ')" title="' + (c.name || '') + '">' +
      '<img src="' + (c.img || '') + '" alt="' + (c.name || '') + '"' +
        ' onerror="this.style.background=\'#1a1a2e\';this.alt=\'' + (c.name || '') + '\';">' +
      '<div class="shc-name">' + (c.name || '') + '</div>' +
    '</div>'
  ).join('');
  document.getElementById('supplyHandCount').textContent = cards.length + ' 张';
}

// ─── 搜索条逻辑 ───
function onSearchBar(type, value) {
  const q = value.trim().toLowerCase();
  const resultsEl = document.getElementById('results' + type.charAt(0).toUpperCase() + type.slice(1));
  const clearEl = document.getElementById('clear' + type.charAt(0).toUpperCase() + type.slice(1));
  const pool = SEARCH_IDX[type] || [];

  if (q.length === 0) {
    resultsEl.classList.remove('show');
    resultsEl.innerHTML = '';
    clearEl.classList.remove('visible');
    return;
  }

  clearEl.classList.add('visible');

  // 怪谈卡：仅名称匹配；反击卡/物资卡：名称+效果匹配
  let results;
  if (type === 'whisper') {
    results = pool.filter(c => c.name.toLowerCase().includes(q)).slice(0, 12);
  } else {
    results = pool.filter(c =>
      c.name.toLowerCase().includes(q) ||
      (c.effect && c.effect.toLowerCase().includes(q))
    ).slice(0, 12);
  }

  resultsEl.innerHTML = results.length === 0
    ? '<div class="search-bar-result-item" style="color:var(--text-muted);cursor:default;">没有找到匹配的卡牌</div>'
    : results.map((c, i) =>
        '<div class="search-bar-result-item" onclick="selectSearchResult(\'' + type + '\',' + i + ')" onmouseenter="focusSearchResult(\'' + type + '\',' + i + ')">' +
          '<span class="sbr-name">' + c.name + '</span>' +
          (c.level ? '<span class="sbr-level">' + c.level + '</span>' : '') +
        '</div>'
      ).join('');
  resultsEl.classList.add('show');
}

function focusSearchResult(type, idx) {
  const el = document.getElementById('results' + type.charAt(0).toUpperCase() + type.slice(1));
  const items = el.querySelectorAll('.search-bar-result-item');
  items.forEach(item => item.classList.remove('focused'));
  if (items[idx]) items[idx].classList.add('focused');
}

function selectSearchResult(type, idx) {
  const pool = SEARCH_IDX[type] || [];
  const q = document.getElementById('search' + type.charAt(0).toUpperCase() + type.slice(1)).value.trim().toLowerCase();
  let results;
  if (type === 'whisper') {
    results = pool.filter(c => c.name.toLowerCase().includes(q)).slice(0, 12);
  } else {
    results = pool.filter(c =>
      c.name.toLowerCase().includes(q) ||
      (c.effect && c.effect.toLowerCase().includes(q))
    ).slice(0, 12);
  }

  const card = results[idx];
  if (!card) return;

  // 根据类型执行不同操作
  if (type === 'whisper') {
    // 怪谈卡 → 直接堆叠到场景左侧
    const exists = PLAY.scene.whisper.find(c => c.name === card.name);
    if (!exists) {
      PLAY.scene.whisper.push({ name: card.name, level: card.level, img: card.img, effect: card.effect });
    }
  } else if (type === 'counter') {
    // 反击卡 → 加入未激活区域（卡背）
    const allCounters = [...PLAY.scene.inactive, ...PLAY.scene.active];
    const exists = allCounters.find(c => c.name === card.name);
    if (!exists) {
      PLAY.scene.inactive.push({ name: card.name, level: card.level, img: card.img, effect: card.effect });
    }
  } else if (type === 'supply') {
    // 物资卡 → 加入手牌条
    const exists = PLAY.supplyHand.find(c => c.name === card.name);
    if (!exists) {
      PLAY.supplyHand.push({ name: card.name, level: card.level, img: card.img, effect: card.effect });
    }
  }

  clearSearchBar(type);
  refreshAllPlay();
}

function clearSearchBar(type) {
  document.getElementById('search' + type.charAt(0).toUpperCase() + type.slice(1)).value = '';
  document.getElementById('clear' + type.charAt(0).toUpperCase() + type.slice(1)).classList.remove('visible');
  const resultsEl = document.getElementById('results' + type.charAt(0).toUpperCase() + type.slice(1));
  resultsEl.classList.remove('show');
  resultsEl.innerHTML = '';
}

// 点击其他区域关闭搜索建议
document.addEventListener('click', function(e) {
  ['whisper','counter','supply'].forEach(type => {
    const col = document.getElementById('searchCol' + type.charAt(0).toUpperCase() + type.slice(1));
    if (col && !col.contains(e.target)) {
      const resultsEl = document.getElementById('results' + type.charAt(0).toUpperCase() + type.slice(1));
      resultsEl.classList.remove('show');
    }
  });
});

// ─── 操作菜单系统 ───
let ACTION_TARGET = null; // { type, card, index }

function showActionMenu(title, items, target) {
  ACTION_TARGET = target;
  document.getElementById('actionMenuTitle').textContent = title;
  document.getElementById('actionMenuItems').innerHTML = items.map(item =>
    '<div class="action-menu-item" onclick="closeActionMenu();(' + item.action + ')()">' +
      '<span class="ami-icon">' + item.icon + '</span>' +
      '<span class="ami-label">' + item.label + '</span>' +
    '</div>'
  ).join('');
  document.getElementById('actionMenuOverlay').classList.add('open');
}

function closeActionMenu() {
  document.getElementById('actionMenuOverlay').classList.remove('open');
  ACTION_TARGET = null;
}

// ─── 怪谈卡菜单 ───
function showWhisperMenu(card) {
  showActionMenu('👻 ' + (card.name || '怪谈卡'), [
    { icon: '🔍', label: '确认（查看详情）', action: 'showCardDetail_whisper' },
    { icon: '🗑️', label: '弃牌堆', action: 'discardWhisperCard' }
  ], { type: 'whisper', card: card });
}

function discardWhisperCard() {
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.whisper.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.whisper.splice(idx, 1);
    PLAY.discard.push(card);
  }
  refreshAllPlay();
}

// ─── 未激活反击卡菜单 ───
function showInactiveMenu(card) {
  showActionMenu('🃏? ' + (card.name || '未激活反击卡'), [
    { icon: '✅', label: '激活（翻面→右侧）', action: 'activateInactiveCard' },
    { icon: '🔍', label: '确认（放大查看）', action: 'showCardDetail_inactive' }
  ], { type: 'inactive', card: card });
}

function activateInactiveCard() {
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.inactive.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.inactive.splice(idx, 1);
    PLAY.scene.active.push(card);
  }
  refreshAllPlay();
}

// ─── 已激活反击卡菜单 ───
function showActiveMenu(card) {
  showActionMenu('✅ ' + (card.name || '已激活反击卡'), [
    { icon: '🔍', label: '确认（查看详情）', action: 'showCardDetail_active' },
    { icon: '🗑️', label: '弃牌堆', action: 'discardActiveCard' },
    { icon: '📚', label: '堆叠（角色卡下）', action: 'stackActiveUnderChar' },
    { icon: '🔀', label: '对他人使用', action: 'useActiveOnOthers' }
  ], { type: 'active', card: card });
}

function discardActiveCard() {
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.active.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.active.splice(idx, 1);
    PLAY.discard.push(card);
  }
  refreshAllPlay();
}

function stackActiveUnderChar() {
  // "堆叠到角色卡下" — 在当前设计中，已激活反击卡已经在角色卡右侧堆叠
  // 这里的"堆叠"意思是从右侧挪到角色卡正下方（物资料理区）
  // 实际游戏操作：从"已激活"状态变为"持续适用"状态
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.active.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.active.splice(idx, 1);
    PLAY.scene.supply.push(card); // 放入下部物资区作为"持续适用"
  }
  refreshAllPlay();
}

function useActiveOnOthers() {
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.active.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.active.splice(idx, 1);
    PLAY.useOthers.push(card);
  }
  refreshAllPlay();
}

// ─── 伤害卡菜单 ───
function showDamageMenu(card) {
  showActionMenu('💔 ' + (card.name || '伤害指示卡'), [
    { icon: '🔍', label: '确认（查看详情）', action: 'showCardDetail_damage' },
    { icon: '↩️', label: '移回弃牌堆', action: 'discardDamageCard' }
  ], { type: 'damage', card: card });
}

function discardDamageCard() {
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.damage.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.damage.splice(idx, 1);
    PLAY.discard.push(card);
  }
  refreshAllPlay();
}

// ─── 已使用物资卡菜单 ───
function showSupplyUsedMenu(card) {
  showActionMenu('📦 ' + (card.name || '物资卡'), [
    { icon: '🔍', label: '确认（查看详情）', action: 'showCardDetail_supplyUsed' },
    { icon: '🗑️', label: '弃牌堆', action: 'discardSupplyUsedCard' },
    { icon: '🔀', label: '交易（对他人使用）', action: 'tradeSupplyUsedCard' }
  ], { type: 'supply', card: card });
}

function discardSupplyUsedCard() {
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.supply.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.supply.splice(idx, 1);
    PLAY.discard.push(card);
  }
  refreshAllPlay();
}

function tradeSupplyUsedCard() {
  if (!ACTION_TARGET) return;
  const card = ACTION_TARGET.card;
  const idx = PLAY.scene.supply.findIndex(c => c.name === card.name);
  if (idx >= 0) {
    PLAY.scene.supply.splice(idx, 1);
    PLAY.useOthers.push(card);
  }
  refreshAllPlay();
}

// ─── 物资卡手牌菜单 ───
function showSupplyHandMenu(idx) {
  const card = PLAY.supplyHand[idx];
  if (!card) return;

  showActionMenu('🎒 ' + (card.name || '物资卡'), [
    { icon: '🔍', label: '确认（查看详情）', action: 'showCardDetail_supplyHand' },
    { icon: '✅', label: '使用（堆叠到角色卡下）', action: 'useSupplyHandCard' },
    { icon: '🔀', label: '交易（对他人使用）', action: 'tradeSupplyHandCard' },
    { icon: '🗑️', label: '弃置（弃牌堆）', action: 'discardSupplyHandCard' }
  ], { type: 'supplyHand', card: card, index: idx });
}

function useSupplyHandCard() {
  if (!ACTION_TARGET) return;
  const idx = ACTION_TARGET.index;
  if (idx >= 0 && idx < PLAY.supplyHand.length) {
    const card = PLAY.supplyHand.splice(idx, 1)[0];
    PLAY.scene.supply.push(card);
  }
  refreshAllPlay();
}

function tradeSupplyHandCard() {
  if (!ACTION_TARGET) return;
  const idx = ACTION_TARGET.index;
  if (idx >= 0 && idx < PLAY.supplyHand.length) {
    const card = PLAY.supplyHand.splice(idx, 1)[0];
    PLAY.useOthers.push(card);
  }
  refreshAllPlay();
}

function discardSupplyHandCard() {
  if (!ACTION_TARGET) return;
  const idx = ACTION_TARGET.index;
  if (idx >= 0 && idx < PLAY.supplyHand.length) {
    const card = PLAY.supplyHand.splice(idx, 1)[0];
    PLAY.discard.push(card);
  }
  refreshAllPlay();
}

// ─── 卡牌详情弹窗 ───
function showCardDetail_whisper() { showCardDetail(ACTION_TARGET ? ACTION_TARGET.card : null, '怪谈卡'); }
function showCardDetail_inactive() { showCardDetail(ACTION_TARGET ? ACTION_TARGET.card : null, '反击卡（未激活）'); }
function showCardDetail_active() { showCardDetail(ACTION_TARGET ? ACTION_TARGET.card : null, '反击卡（已激活）'); }
function showCardDetail_damage() { showCardDetail(ACTION_TARGET ? ACTION_TARGET.card : null, '伤害指示卡'); }
function showCardDetail_supplyUsed() { showCardDetail(ACTION_TARGET ? ACTION_TARGET.card : null, '物资卡（使用中）'); }
function showCardDetail_supplyHand() { showCardDetail(ACTION_TARGET ? ACTION_TARGET.card : null, '物资卡'); }

function showCardDetail(card, typeLabel) {
  if (!card) return;
  document.getElementById('cardDetailImg').src = card.img || '';
  document.getElementById('cardDetailImg').onerror = function() { this.style.display = 'none'; };
  document.getElementById('cardDetailImg').style.display = 'block';
  document.getElementById('cardDetailName').textContent = card.name || '未知卡牌';
  document.getElementById('cardDetailMeta').textContent = (typeLabel || '') + (card.level ? ' · ' + card.level : '');
  document.getElementById('cardDetailEffect').textContent = card.effect || '暂无效果描述';
  document.getElementById('cardDetailOverlay').classList.add('open');
}

function closeCardDetail() {
  document.getElementById('cardDetailOverlay').classList.remove('open');
}

// ─── 角色卡详情 ───
function showCharDetail() {
  showCardDetail({
    name: '乐天派幸存者',
    level: '命运操控者',
    effect: '开局健康值6/7（其余角色7/7）。每次成功宣言抹除规则后，额外抽1张反击卡。死亡后化为煞鬼时，保留本角色技能直至游戏结束。',
    img: 'images/cards/角色卡/角色卡_命运操控者_乐天派幸存者.png'
  }, '角色卡');
}

// ─── 抽屉系统 ───
function openDrawer(type) {
  const overlay = document.getElementById('drawer' + type.charAt(0).toUpperCase() + type.slice(1));
  const cardsEl = document.getElementById('drawer' + type.charAt(0).toUpperCase() + type.slice(1) + 'Cards');
  const cards = type === 'discard' ? PLAY.discard : PLAY.useOthers;

  if (cards.length === 0) {
    cardsEl.innerHTML = '<div class="drawer-empty">' + (type === 'discard' ? '弃牌堆为空' : '暂无待处理的卡牌') + '</div>';
    overlay.classList.add('open');
    return;
  }

  cardsEl.innerHTML = cards.map((c, i) =>
    '<div class="drawer-card-item" onclick="drawerCardClick(\'' + type + '\',' + i + ')" title="' + (c.name || '') + '">' +
      '<div class="drawer-card-thumb">' +
        '<img src="' + (c.img || '') + '" alt="' + (c.name || '') + '"' +
          ' onerror="this.style.background=\'#1a1a2e\';this.alt=\'' + (c.name || '') + '\';">' +
      '</div>' +
      '<div class="drawer-card-name">' + (c.name || '') + '</div>' +
    '</div>'
  ).join('');
  overlay.classList.add('open');
}

function closeDrawer(type) {
  document.getElementById('drawer' + type.charAt(0).toUpperCase() + type.slice(1)).classList.remove('open');
}

function drawerCardClick(type, idx) {
  const cards = type === 'discard' ? PLAY.discard : PLAY.useOthers;
  const card = cards[idx];
  if (!card) return;
  showCardDetail(card, type === 'discard' ? '弃牌堆' : '对他人使用');
}

// ─── 回合计数器按钮 ───
function playDawnAction() {
  showConfirmMini(
    '🌅 迎接黎明',
    '推进至下一回合黎明。回合计数 +1，当前叠放的回合指示卡将归档。确定继续吗？',
    function() { advanceRound(); }
  );
}

function playEndRound() {
  showConfirmMini(
    '🌙 回合结束',
    '结束当前回合，叠放4张回合指示卡（A右/A左/B上/B下）。确定继续吗？',
    function() { endCurrentRound(); }
  );
}

function advanceRound() {
  if (PLAY.round >= 12) {
    showConfirmMini('⚠️ 已达上限', '已到达第12回合（游戏结束）。无法继续推进。', null);
    return;
  }
  endCurrentRound();
}

function endCurrentRound() {
  // 叠放当前回合的4张指示卡
  const round = PLAY.round;
  const cards = [
    getRoundCardPath('A右', round),
    getRoundCardPath('A左', round),
    getRoundCardPath('B上', round),
    getRoundCardPath('B下', round)
  ];
  PLAY.roundHistory.push({ round: round, cards: cards });

  // 推进回合
  PLAY.round++;
  if (PLAY.round > 12) PLAY.round = 12;

  // 动画：回合数字闪烁
  const numEl = document.getElementById('roundNum');
  numEl.classList.add('pulse');
  setTimeout(function() { numEl.classList.remove('pulse'); }, 350);

  refreshAllPlay();
}

// ─── 确认对话框 ───
function showConfirmMini(title, body, onOk) {
  document.getElementById('confirmMiniTitle').textContent = title;
  document.getElementById('confirmMiniBody').textContent = body;
  const okBtn = document.getElementById('confirmMiniOk');
  okBtn.onclick = function() {
    closeConfirmMini();
    if (onOk) onOk();
  };
  if (!onOk) okBtn.style.display = 'none';
  else okBtn.style.display = '';
  document.getElementById('confirmMiniOverlay').classList.add('open');
}

function closeConfirmMini() {
  document.getElementById('confirmMiniOverlay').classList.remove('open');
}

// ─── 打开抽屉按钮（从状态栏触发） ───
// 双击状态栏中的弃牌数量可打开抽屉
document.getElementById('playStatusRow').addEventListener('dblclick', function(e) {
  if (e.target.id === 'playCntDC') {
    openDrawer('discard');
  }
});

// ─── 窗口resize ───
window.addEventListener('resize', function() {
  if (document.getElementById('panel-play').classList.contains('active')) {
    initPlayChar();
    refreshPlayScene();
  }
});
'''

print("Script variables loaded successfully.")
print(f"NEW_CSS: {len(NEW_CSS)} chars")
print(f"NEW_HTML: {len(NEW_HTML)} chars")
print(f"NEW_JS: {len(NEW_JS)} chars")

# ====================================================================
# SPLICE LOGIC
# ====================================================================

# Read original
with open(SRC, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original file: {len(lines)} lines")

# Verify key lines
def show_line(idx, label):
    """idx is 0-indexed"""
    if idx < len(lines):
        print(f"  [{label}] line {idx+1}: {lines[idx].rstrip()[:80]}")
    else:
        print(f"  [{label}] line {idx+1}: OUT OF RANGE")

print("\nVerifying boundary lines:")
show_line(634, "CSS-keep-end")      # line 635 - last Tab 3 CSS line
show_line(635, "CSS-replace-start") # line 636 - first old Tab 4 CSS
show_line(1606, "CSS-replace-end")  # line 1607 - last old Tab 4 CSS
show_line(1607, "CSS-keep-resume")  # line 1608 - </style>
show_line(1755, "HTML-keep-end")    # line 1756 - before Tab 4 comment
show_line(1756, "HTML-replace-start") # line 1757 - Tab 4 comment
show_line(1908, "HTML-replace-end") # line 1909 - closing </div>
show_line(1909, "HTML-keep-resume") # line 1910
show_line(2514, "JS-keep-end")      # line 2515 - initComposite();
show_line(2515, "JS-replace-start") # line 2516 - initPlayPanel();
show_line(3384, "JS-replace-end")   # line 3385 - });
show_line(3385, "JS-keep-resume")   # line 3386 - </script>
show_line(3388, "LAST-line")        # line 3389 - </html>

# Build output
output = (
    lines[0:635] +           # Tab 1-3 CSS (lines 1-635)
    ['\n' + NEW_CSS + '\n'] + # New Tab 4 CSS
    lines[1607:1756] +       # </style> through before Tab 4 comment (lines 1608-1756)
    ['\n' + NEW_HTML + '\n'] + # New Tab 4 HTML
    lines[1909:2515] +       # Closing divs through initComposite() (lines 1910-2515)
    ['\n' + NEW_JS + '\n'] + # New Tab 4 JS
    lines[3385:]             # </script> through </html> (lines 3386-3389)
)

print(f"\nOutput: {len(output)} lines (was {len(lines)})")
print(f"CSS block:  lines 636-1607 replaced ({1607-635}=972 lines)")
print(f"HTML block: lines 1757-1909 replaced ({1909-1756}=153 lines)")
print(f"JS block:   lines 2516-3385 replaced ({3385-2515}=870 lines)")

# Backup
import shutil
BAK = SRC + '.bak'
shutil.copy2(SRC, BAK)
print(f"\nBackup saved to: {BAK}")

# Write
with open(DST, 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"Written to: {DST}")
print("Done!")
