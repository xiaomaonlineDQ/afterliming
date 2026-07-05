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
  personal_goal: '个人目的卡'
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
  personal_goal: 'goal'
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

// --- Render full card ---
function renderCard(card) {
  const type = card._type || card.type;
  const typeClass = TYPE_CSS_CLASS[type] || '';
  const levelInfo = LEVEL_MAP[card.level || card.difficulty] || { cn: card.level || card.difficulty, css: '' };

  return `
    <div class="card ${typeClass}-card" data-id="${card.id}" data-type="${type}" data-level="${card.level || card.difficulty || ''}">
      <div class="card-header">
        <span class="card-title">${card.name}</span>
      </div>
      <div style="display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap;">
        <span class="card-badge ${typeClass}">${TYPE_MAP[type] || type}</span>
        <span class="badge-rarity ${levelInfo.css}">${levelInfo.cn}</span>
      </div>
      <div style="color:var(--text-muted);font-size:0.85rem;line-height:1.6;">
        ${card.effect || card.rule_text || card.skill_effect || card.goal_text || ''}
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
