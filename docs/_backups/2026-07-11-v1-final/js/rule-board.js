// ==================== 公开规则板引擎 ====================
// 从 toolbox/rule-board.html 移植至 citizen.html 个人面板
// 图片路径适配：citizen.html 在 docs/ 根目录，无需 ../ 前缀

const RB_STORAGE_KEY = 'dawn_rule_board_v1';

// --- 数据准备 ---
function rbGetAllRules() {
  if (typeof CARD_DB === 'undefined' || !CARD_DB.rules) return [];
  return CARD_DB.rules.map(function(r) { var c = {}; for (var k in r) c[k] = r[k]; c._type = 'rules'; return c; });
}

// 规则卡图片路径（citizen.html在docs/根目录，不需要../前缀）
function rbGetRuleImagePath(card) {
  var name = card.name;
  var BASE = '';
  if (name.indexOf('规则 ') === 0) {
    var code = name.replace('规则 ', '');
    return BASE + 'images/cards/规则卡/规则卡_' + code + '.png';
  }
  if (name.indexOf('特殊规则') === 0) {
    var rulesArr = CARD_DB.rules || [];
    for (var i = 0; i < rulesArr.length; i++) {
      if (rulesArr[i].id === card.id) {
        if (i >= 30) {
          var offset = i - 30;
          var pairNum = String(Math.floor(offset / 2) + 1);
          if (pairNum.length < 2) pairNum = '0' + pairNum;
          var letter = offset % 2 === 0 ? 'A' : 'B';
          return BASE + 'images/cards/规则卡/规则卡_S-' + pairNum + letter + '.png';
        }
        break;
      }
    }
  }
  return null;
}

function rbGetRuleDifficulty(card) {
  var d = card.difficulty || '';
  if (d.indexOf('T') === 0) return d;
  if (d.indexOf('S') === 0 || card.category === '特殊规则') return 'S';
  return 'S';
}

function rbGetRuleBadgeClass(card) {
  var d = rbGetRuleDifficulty(card);
  if (d === 'T1') return 'rb-badge-t1';
  if (d === 'T2') return 'rb-badge-t2';
  if (d === 'T3') return 'rb-badge-t3';
  return 'rb-badge-s';
}

// --- 状态管理 ---
var rbState = {};
var rbAllRules = [];
var rbActiveTab = 'all';
var rbSelectedCardId = null;

function rbLoadState() {
  try {
    var raw = localStorage.getItem(RB_STORAGE_KEY);
    if (raw) {
      var state = JSON.parse(raw);
      if (state && typeof state === 'object') return state;
    }
  } catch(e) {}
  return { 1: [], 2: [], 3: [], 4: [] };
}

function rbSaveState(state) {
  localStorage.setItem(RB_STORAGE_KEY, JSON.stringify(state));
  var el = document.getElementById('rbSaveStatus');
  if (!el) return;
  el.textContent = '已保存 ' + new Date().toLocaleTimeString('zh-CN', {hour:'2-digit',minute:'2-digit'});
  setTimeout(function() { el.textContent = ''; }, 2000);
}

function rbGetZoneCards(state, zoneId) {
  return state[zoneId] || [];
}

function rbIsCardInAnyZone(state, cardId) {
  for (var z = 1; z <= 4; z++) {
    if ((state[z] || []).indexOf(cardId) >= 0) return z;
  }
  return null;
}

function rbMoveCard(state, cardId, fromZone, toZone) {
  var newState = JSON.parse(JSON.stringify(state));
  if (fromZone !== null && newState[fromZone]) {
    newState[fromZone] = newState[fromZone].filter(function(id) { return id !== cardId; });
  }
  if (toZone !== null && newState[toZone] !== undefined) {
    if (newState[toZone].indexOf(cardId) < 0) {
      newState[toZone].push(cardId);
    }
  }
  return newState;
}

// --- 渲染 ---
function rbInit() {
  rbAllRules = rbGetAllRules();
  rbState = rbLoadState();
  rbBuildPoolTabs();
  rbApplyTabFilter();
  rbRenderAllZones();
  rbSetupDragDrop();
  rbSetupTouch();
}

function rbBuildPoolTabs() {
  var diffs = {};
  rbAllRules.forEach(function(r) {
    var d = rbGetRuleDifficulty(r);
    diffs[d] = (diffs[d] || 0) + 1;
  });
  var tabs = [
    { key: 'all', label: '全部', count: rbAllRules.length },
    { key: 'T1', label: 'T1', count: diffs['T1'] || 0 },
    { key: 'T2', label: 'T2', count: diffs['T2'] || 0 },
    { key: 'T3', label: 'T3', count: diffs['T3'] || 0 },
    { key: 'S',  label: '特殊规则', count: diffs['S'] || 0 }
  ];
  var container = document.getElementById('rbPoolTabs');
  if (!container) return;
  container.innerHTML = tabs.map(function(t) {
    return '<button class="rb-pool-tab' + (rbActiveTab === t.key ? ' active' : '') + '" data-tab="' + t.key + '">'
      + t.label + ' <small style="opacity:0.7">' + t.count + '</small></button>';
  }).join('');
  container.querySelectorAll('.rb-pool-tab').forEach(function(btn) {
    btn.addEventListener('click', function() {
      rbActiveTab = btn.dataset.tab;
      container.querySelectorAll('.rb-pool-tab').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      rbApplyTabFilter();
    });
  });
}

function rbApplyTabFilter() {
  var poolCards = rbAllRules.filter(function(r) { return !rbIsCardInAnyZone(rbState, r.id); });
  var filtered = poolCards;
  if (rbActiveTab !== 'all') {
    filtered = poolCards.filter(function(r) { return rbGetRuleDifficulty(r) === rbActiveTab; });
  }
  rbRenderPoolCards(filtered);
  var cntEl = document.getElementById('rbPoolCount');
  if (cntEl) cntEl.textContent = '(' + filtered.length + ')';
}

function rbRenderPoolCards(cards) {
  var container = document.getElementById('rbPoolCards');
  if (!container) return;
  if (cards.length === 0) {
    container.innerHTML = '<div class="rb-zone-empty">卡池已空</div>';
    return;
  }
  container.innerHTML = cards.map(function(c) { return rbBuildCardHTML(c, 'pool'); }).join('');
  rbBindCardEvents(container);
}

function rbRenderAllZones() {
  for (var z = 1; z <= 4; z++) { rbRenderZone(z); }
}

function rbRenderZone(zoneId) {
  var body = document.getElementById('rbZone' + zoneId + 'Body');
  var count = document.getElementById('rbZone' + zoneId + 'Count');
  if (!body || !count) return;
  var cardIds = rbGetZoneCards(rbState, zoneId);
  var cards = [];
  for (var i = 0; i < cardIds.length; i++) {
    var found = null;
    for (var j = 0; j < rbAllRules.length; j++) {
      if (rbAllRules[j].id === cardIds[i]) { found = rbAllRules[j]; break; }
    }
    if (found) cards.push(found);
  }

  count.textContent = cards.length;

  if (cards.length === 0) {
    body.innerHTML = '<div class="rb-zone-empty">' +
      (zoneId === 4 ? '宣言成功抹除的规则置于此处' : '从卡池拖拽规则卡到此处') +
      '</div>';
    return;
  }

  body.innerHTML = cards.map(function(c) { return rbBuildCardHTML(c, 'zone', zoneId); }).join('');
  rbBindCardEvents(body);
}

function rbBuildCardHTML(card, location, zoneId) {
  var imgPath = rbGetRuleImagePath(card) || '';
  var text = card.rule_text || '';
  var badgeClass = rbGetRuleBadgeClass(card);
  var diff = card.difficulty || 'S';

  if (location === 'zone') {
    return '<div class="rb-card in-zone" data-card-id="' + card.id + '" data-from="zone" data-zone="' + (zoneId || '') + '" draggable="true">'
      + '<button class="rb-card-return" data-action="return" data-card-id="' + card.id + '" data-zone="' + zoneId + '">← 返回卡池</button>'
      + '<div class="rb-card-img">'
      + (imgPath
        ? '<img src="' + imgPath + '" alt="' + card.name + '" loading="lazy" onerror="this.parentElement.innerHTML=\'<div style=display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-muted);font-size:0.72rem>' + card.name + '</div>\'">'
        : '<div style="display:flex;align-items:center;justify-content:center;height:100%;min-height:60px;color:var(--text-muted);font-size:0.72rem">' + card.name + '</div>')
      + '</div></div>';
  }

  return '<div class="rb-card" data-card-id="' + card.id + '" data-from="pool" data-zone="" draggable="true">'
    + '<div class="rb-card-img">'
    + (imgPath
      ? '<img src="' + imgPath + '" alt="' + card.name + '" loading="lazy" onerror="this.parentElement.innerHTML=\'<span style=font-size:0.6rem;padding:4px>' + card.name.charAt(0) + '</span>\'">'
      : '' + card.name.charAt(0))
    + '</div>'
    + '<div class="rb-card-info">'
    + '<div class="rb-card-name">' + card.name + '</div>'
    + '<div class="rb-card-text">' + text + '</div>'
    + '<span class="rb-card-badge ' + badgeClass + '">' + diff + '</span>'
    + '</div></div>';
}

function rbBindCardEvents(container) {
  container.querySelectorAll('[data-action="return"]').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var cardId = btn.dataset.cardId;
      var fromZone = parseInt(btn.dataset.zone);
      rbState = rbMoveCard(rbState, cardId, fromZone, null);
      rbSaveState(rbState);
      rbRenderZone(fromZone);
      rbApplyTabFilter();
    });
  });

  container.querySelectorAll('.rb-card[draggable]').forEach(function(card) {
    card.addEventListener('dragstart', rbHandleDragStart);
    card.addEventListener('dragend', rbHandleDragEnd);
  });
}

// ============ PC 拖拽 ============
function rbSetupDragDrop() {
  for (var z = 1; z <= 4; z++) {
    (function(zoneId) {
      var zone = document.getElementById('rbZone' + zoneId);
      if (!zone) return;
      zone.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        zone.classList.add('drag-over');
      });
      zone.addEventListener('dragleave', function() {
        zone.classList.remove('drag-over');
      });
      zone.addEventListener('drop', function(e) {
        e.preventDefault();
        zone.classList.remove('drag-over');
        var cardId = e.dataTransfer.getData('text/plain');
        if (!cardId) return;
        var fromZone = rbIsCardInAnyZone(rbState, cardId);
        if (fromZone === zoneId) return;
        rbState = rbMoveCard(rbState, cardId, fromZone, zoneId);
        rbSaveState(rbState);
        if (fromZone) rbRenderZone(fromZone);
        rbRenderZone(zoneId);
        rbApplyTabFilter();
      });
    })(z);
  }

  var pool = document.getElementById('rbPoolPanel');
  if (pool) {
    pool.addEventListener('dragover', function(e) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    });
    pool.addEventListener('drop', function(e) {
      e.preventDefault();
      var cardId = e.dataTransfer.getData('text/plain');
      if (!cardId) return;
      var fromZone = rbIsCardInAnyZone(rbState, cardId);
      if (!fromZone) return;
      rbState = rbMoveCard(rbState, cardId, fromZone, null);
      rbSaveState(rbState);
      rbRenderZone(fromZone);
      rbApplyTabFilter();
    });
  }
}

function rbHandleDragStart(e) {
  var cardId = this.dataset.cardId;
  e.dataTransfer.setData('text/plain', cardId);
  e.dataTransfer.effectAllowed = 'move';
  this.classList.add('dragging');
}

function rbHandleDragEnd() {
  this.classList.remove('dragging');
}

// ============ 触屏选择模式 ============
function rbSetupTouch() {
  document.addEventListener('click', function(e) {
    var panel = document.getElementById('panel-ruleboard');
    if (!panel || !panel.classList.contains('active')) return;

    var card = e.target.closest('.rb-card');
    if (!card) {
      if (rbSelectedCardId) {
        rbDeselectAll();
        rbSelectedCardId = null;
      }
      return;
    }
    if (e.target.closest('[data-action="return"]')) return;

    var cardId = card.dataset.cardId;

    if (rbSelectedCardId === cardId) {
      rbDeselectAll();
      rbSelectedCardId = null;
      return;
    }

    if (!rbSelectedCardId) {
      rbSelectCard(cardId);
      return;
    }

    var clickedCardZone = card.dataset.zone ? parseInt(card.dataset.zone) : null;

    if (clickedCardZone) {
      var fromZone1 = rbIsCardInAnyZone(rbState, rbSelectedCardId);
      if (fromZone1 !== clickedCardZone) {
        rbState = rbMoveCard(rbState, rbSelectedCardId, fromZone1, clickedCardZone);
        rbSaveState(rbState);
        if (fromZone1) rbRenderZone(fromZone1);
        rbRenderZone(clickedCardZone);
        rbApplyTabFilter();
      }
    } else {
      var fromZone2 = rbIsCardInAnyZone(rbState, rbSelectedCardId);
      if (fromZone2) {
        rbState = rbMoveCard(rbState, rbSelectedCardId, fromZone2, null);
        rbSaveState(rbState);
        rbRenderZone(fromZone2);
        rbApplyTabFilter();
      }
    }

    rbDeselectAll();
    rbSelectedCardId = null;
  });

  for (var z = 1; z <= 4; z++) {
    (function(zoneId) {
      var zoneEl = document.getElementById('rbZone' + zoneId);
      if (!zoneEl) return;
      zoneEl.addEventListener('click', function(e) {
        if (!rbSelectedCardId) return;
        if (e.target.closest('.rb-card')) return;
        var fromZone = rbIsCardInAnyZone(rbState, rbSelectedCardId);
        if (fromZone === zoneId) {
          rbDeselectAll();
          rbSelectedCardId = null;
          return;
        }
        rbState = rbMoveCard(rbState, rbSelectedCardId, fromZone, zoneId);
        rbSaveState(rbState);
        if (fromZone) rbRenderZone(fromZone);
        rbRenderZone(zoneId);
        rbApplyTabFilter();
        rbDeselectAll();
        rbSelectedCardId = null;
      });
    })(z);
  }
}

function rbSelectCard(cardId) {
  rbDeselectAll();
  rbSelectedCardId = cardId;
  document.querySelectorAll('.rb-card[data-card-id="' + cardId + '"]').forEach(function(c) { c.classList.add('selected'); });
  var el = document.getElementById('rbSaveStatus');
  if (el) {
    el.textContent = '已选择：点击目标分区放置（或再次点击取消）';
    setTimeout(function() { if (el.textContent.indexOf('已选择') >= 0) el.textContent = ''; }, 3000);
  }
}

function rbDeselectAll() {
  document.querySelectorAll('.rb-card.selected').forEach(function(c) { c.classList.remove('selected'); });
}

// ============ 重置 ============
function rbResetBoard() {
  if (!confirm('确定要清空所有分区？全部规则卡将返回卡池。')) return;
  rbState = { 1: [], 2: [], 3: [], 4: [] };
  rbSaveState(rbState);
  rbSelectedCardId = null;
  rbDeselectAll();
  for (var z = 1; z <= 4; z++) rbRenderZone(z);
  rbApplyTabFilter();
}
