// ========================================
// 《黎明之后》官网 — 公共脚本
// ========================================

// --- Navigation ---
document.addEventListener('DOMContentLoaded', () => {
  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  // Highlight active nav link
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Animate elements on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate-in').forEach(el => {
    el.style.animationPlayState = 'paused';
    observer.observe(el);
  });

  // Accordion
  document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
      header.classList.toggle('open');
      header.nextElementSibling.classList.toggle('open');
    });
  });
});

// --- Card Type Mappings ---
const TYPE_MAP = {
  whispers: '怪谈卡',
  countermeasures: '反击卡',
  rules: '规则卡',
  characters: '角色卡',
  personal_goals: '个人目的卡',
  whisper: '怪谈卡',
  countermeasure: '反击卡',
  rule: '规则卡',
  character: '角色卡',
  personal_goal: '个人目的卡',
  supplies: '物资卡',
  supply: '物资卡'
};

const TYPE_CSS_CLASS = {
  whispers: 'whisper',
  countermeasures: 'countermeasure',
  rules: 'rule',
  characters: 'character',
  personal_goals: 'goal',
  whisper: 'whisper',
  countermeasure: 'countermeasure',
  rule: 'rule',
  character: 'character',
  personal_goal: 'goal',
  supplies: 'supply',
  supply: 'supply'
};

const LEVEL_MAP = {
  // Whispers
  '流言': { cn: '流言', css: 'rumor', order: 1 },
  '异常': { cn: '异常', css: 'anomaly', order: 2 },
  '怪诞': { cn: '怪诞', css: 'grotesque', order: 3 },
  '灾厄': { cn: '灾厄', css: 'disaster', order: 4 },
  // Countermeasures
  '基础': { cn: '基础', css: 'basic', order: 1 },
  '觉醒': { cn: '觉醒', css: 'awaken', order: 2 },
  '极致': { cn: '极致', css: 'extreme', order: 3 },
  '真理': { cn: '真理', css: 'truth', order: 4 },
  // Rules
  'T1': { cn: 'T1', css: 'basic', order: 1 },
  'T2': { cn: 'T2', css: 'awaken', order: 2 },
  'T3': { cn: 'T3', css: 'extreme', order: 3 },
  '普通': { cn: '普通', css: 'basic', order: 1 },
  '特殊': { cn: '特殊', css: 'extreme', order: 3 },
  // Characters
  '命运操控者': { cn: '命运操控者', css: 'truth', order: 4 },
  '攻击者': { cn: '攻击者', css: 'extreme', order: 3 },
  '自保型': { cn: '自保型', css: 'basic', order: 1 },
  '情报型': { cn: '情报型', css: 'awaken', order: 2 },
  '资源型': { cn: '资源型', css: 'goal', order: 2 },
  // Supplies (物资卡)
  '官方物资': { cn: '官方', css: 'basic', order: 1 },
  '普通物资': { cn: '普通', css: 'rumor', order: 2 },
  '中级物资': { cn: '中级', css: 'awaken', order: 3 },
  '高级物资': { cn: '高级', css: 'extreme', order: 4 },
  '绝顶物资': { cn: '绝顶', css: 'truth', order: 5 },
};

// --- Get all cards flat ---
function getAllCards() {
  const all = [];
  for (const [type, cards] of Object.entries(CARD_DB)) {
    cards.forEach(card => {
      all.push({ ...card, _type: type });
    });
  }
  return all;
}

// --- Render card badge ---
function renderBadge(type, level) {
  const cssClass = TYPE_CSS_CLASS[type] || '';
  const typeName = TYPE_MAP[type] || type;
  const levelInfo = LEVEL_MAP[level] || { cn: level, css: '' };
  return `<span class="card-badge ${cssClass}">${typeName}</span>
          <span class="badge-rarity ${levelInfo.css}">${levelInfo.cn}</span>`;
}

// --- Build image path for a card (type-aware, matches actual file naming) ---
function getCardImagePath(card) {
  const type = card._type || card.type;
  const name = card.name;
  const level = card.level || card.difficulty || '';
  const levelInfo = LEVEL_MAP[level] || { cn: level };
  const safeName = name.replace(/[\/\\:*?"<>|]/g, '_')
    .replace(/Ⅰ/g, '_I').replace(/Ⅱ/g, '_II').replace(/Ⅲ/g, '_III')
    .replace(/Ⅳ/g, '_IV').replace(/Ⅴ/g, '_V');

  switch (type) {
    case 'whispers':
      // 怪谈卡/怪谈卡_{等级}_{名称}.png
      return `images/cards/怪谈卡/怪谈卡_${levelInfo.cn}_${safeName}.png`;

    case 'countermeasures':
      // 天数指示卡用"反击卡"前缀，普通反击卡用"事件卡"前缀
      const cmPrefix = name.startsWith('第') ? '反击卡' : '事件卡';
      return `images/cards/反击卡/${cmPrefix}_${levelInfo.cn}_${safeName}.png`;

    case 'rules':
      // 普通规则: 规则卡/规则卡_T1-01.png
      if (name.startsWith('规则 ')) {
        const code = name.replace('规则 ', '');
        return `images/cards/规则卡/规则卡_${code}.png`;
      }
      // 特殊规则: r_031→S-01A, r_032→S-01B, ... 从30号(0-based)开始偏移
      if (name.startsWith('特殊规则')) {
        const rulesArr = CARD_DB.rules || [];
        const idx = rulesArr.findIndex(r => r.id === card.id);
        if (idx >= 30) {
          const offset = idx - 30;
          const pairNum = String(Math.floor(offset / 2) + 1).padStart(2, '0');
          const letter = offset % 2 === 0 ? 'A' : 'B';
          return `images/cards/规则卡/规则卡_S-${pairNum}${letter}.png`;
        }
      }
      return null;

    case 'characters':
      // 角色卡/角色卡_{等级}_{名称}.png
      return `images/cards/角色卡/角色卡_${levelInfo.cn}_${safeName}.png`;

    case 'supplies':
      // 天数指示卡直接使用"物资卡_第X天.png"格式（无等级后缀）
      if (name.startsWith('第')) {
        return `images/cards/物资卡/物资卡_${safeName}.png`;
      }
      // 普通物资卡: 物资卡_{等级}_{名称}.png
      return `images/cards/物资卡/物资卡_${levelInfo.cn}_${safeName}.png`;

    case 'personal_goals':
      // 个人目的卡/个人目的卡_{序号}_{名称}.png
      const num = card.id.replace('pg_', '');
      const padded = String(parseInt(num)).padStart(2, '0');
      return `images/cards/个人目的卡/个人目的卡_${padded}_${safeName}.png`;

    default:
      return null;
  }
}

// --- Render full card ---
function renderCard(card) {
  const type = card._type || card.type;
  const typeClass = TYPE_CSS_CLASS[type] || '';
  const levelInfo = LEVEL_MAP[card.level || card.difficulty] || { cn: card.level || card.difficulty, css: '' };
  const typeName = TYPE_MAP[type] || '';

  const imgPath = getCardImagePath(card);
  const isHorizontal = type === 'rules' || type === 'personal_goals';

  return `
    <div class="card ${typeClass}-card" data-id="${card.id}" data-type="${type}" data-level="${card.level || card.difficulty || ''}" onclick="window.location.href='card-detail.html?id=${card.id}&type=${type}'" style="cursor:pointer;">
      <div class="card-img-wrap${isHorizontal ? ' horizontal' : ''}">
        <img src="${imgPath}" alt="${card.name}" loading="lazy"
             onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
        <div class="img-placeholder" style="display:none;">
          <span class="ph-icon">🃏</span>
          <span class="ph-label">${typeName} · ${levelInfo.cn}</span>
          <span class="ph-size">${isHorizontal ? '2640×930' : '630×880'}</span>
        </div>
      </div>
      <div class="card-header">
        <span class="card-title">${card.name}</span>
      </div>
      <div style="display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap;">
        <span class="card-badge ${typeClass}">${TYPE_MAP[type] || type}</span>
        <span class="badge-rarity ${levelInfo.css}">${levelInfo.cn}</span>
      </div>
      <div style="color:var(--text-muted);font-size:0.85rem;line-height:1.6;">
        ${(card.effect || card.rule_text || card.skill_effect || card.goal_text || '').substring(0, 80)}${(card.effect || card.rule_text || card.skill_effect || card.goal_text || '').length > 80 ? '...' : ''}
      </div>
    </div>
  `;
}

// --- URL params helper ---
function getParam(name) {
  const url = new URL(window.location.href);
  return url.searchParams.get(name);
}

// --- Filter helpers ---
function setupFilterButtons(containerSelector, filterFn) {
  const container = document.querySelector(containerSelector);
  if (!container) return;

  container.addEventListener('click', (e) => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;

    // Toggle active
    const wasActive = btn.classList.contains('active');
    container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    if (!wasActive || btn.dataset.value === 'all') {
      btn.classList.add('active');
    } else {
      container.querySelector('.filter-btn[data-value="all"]')?.classList.add('active');
    }

    filterFn();
  });
}

// --- Search helper ---
function setupSearch(inputSelector, filterFn) {
  const input = document.querySelector(inputSelector);
  if (!input) return;
  input.addEventListener('input', filterFn);
}

// --- Format skill effect text (for characters) ---
// Splits by '---' into major sections, then by '; ' into individual lines
function formatSkillEffect(text) {
  if (!text || !text.trim()) {
    return '<div class="skill-empty">技能效果待补充</div>';
  }

  // Split by --- into major sections
  const sections = text.split(/\s*---\s*/);

  if (sections.length === 1) {
    // No sections, just format lines
    return '<div class="skill-section">' + formatSkillLines(sections[0]) + '</div>';
  }

  // Multiple sections
  return sections.map((section, i) => {
    const lines = formatSkillLines(section.trim());
    if (!lines) return '';
    return `<div class="skill-section">
      <div class="skill-section-label">技能 ${i + 1}</div>
      ${lines}
    </div>`;
  }).filter(Boolean).join('');
}

// Helper: split a text block into individual skill lines
function formatSkillLines(text) {
  if (!text || !text.trim()) return '';

  // Split by ; or ；(Chinese semicolon) followed by optional space
  const parts = text.split(/[;；]\s*/).filter(p => p.trim());

  if (parts.length === 0) return `<div class="skill-line">${escapeHtml(text.trim())}</div>`;

  return parts.map(p => {
    const trimmed = p.trim();
    if (!trimmed) return '';
    // Skip markdown table rows (contain |)
    if (trimmed.startsWith('|') || trimmed.startsWith('-')) {
      return `<div class="skill-line" style="padding-left:0;font-family:var(--font-mono);font-size:0.8rem;">${escapeHtml(trimmed)}</div>`;
    }
    return `<div class="skill-line">${escapeHtml(trimmed)}</div>`;
  }).filter(Boolean).join('');
}

// Simple HTML escape
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
