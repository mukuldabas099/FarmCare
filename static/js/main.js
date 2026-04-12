/* ═══════════════════════════════════════════════
   FarmCare — main.js  v4.0
   Navigation flow:
     langSplash → modulePage → setupPage (soil only) → mainApp
                                          └──────────────→ diseaseApp
   Back/forward arrows always visible after splash.
═══════════════════════════════════════════════ */

/* ── Page IDs in navigation order ─────────────── */
const PAGES = ['langSplash', 'modulePage', 'setupPage', 'mainApp', 'diseaseApp'];

/* Current step index */
let _step = 0;

/* Which module was chosen: 'soil' | 'disease' */
let _module = null;

/* ── Show/hide helpers ─────────────────────────── */
function _showOnly(pageId) {
  PAGES.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (id === pageId) {
      el.classList.remove('hidden');
    } else {
      el.classList.add('hidden');
    }
  });
  _updateArrows();
}

/* ── Arrow visibility ──────────────────────────── */
function _updateArrows() {
  const arrows = document.getElementById('navArrows');
  if (!arrows) return;

  /* Hide arrows on language splash */
  if (_step === 0) {
    arrows.style.display = 'none';
    return;
  }
  arrows.style.display = 'flex';

  const btnBack    = document.getElementById('btnBack');
  const btnForward = document.getElementById('btnForward');

  /* Back always enabled once past lang splash */
  if (btnBack) btnBack.disabled = (_step <= 1);

  /* Forward: disabled when on mainApp or diseaseApp (terminal pages) */
  if (btnForward) {
    const onTerminal = (_step >= 3);
    btnForward.disabled = onTerminal;
  }
}

/* ── Navigate back ─────────────────────────────── */
function navBack() {
  if (_step <= 1) return;

  if (_step === 3 || _step === 4) {
    /* From app → back to module selection */
    if (_step === 3) FC.stopAll();
    _step = 1;
    _showOnly('modulePage');
    return;
  }

  if (_step === 2) {
    /* From setup → back to module selection */
    _step = 1;
    _showOnly('modulePage');
    return;
  }

  /* Default: go to module page */
  _step = 1;
  _showOnly('modulePage');
}

/* ── Navigate forward ──────────────────────────── */
function navForward() {
  if (_step === 1) {
    /* Module page → prompt to pick a module */
    FC.toast('👆 Tap a module card to continue', '');
    return;
  }
  if (_step === 2) {
    /* Setup → enter app (demo if Pi not configured) */
    demoAndGo();
    return;
  }
}

/* ══════════════════════════════════════════════
   STEP 1 — Language selection
══════════════════════════════════════════════ */
function selectLang(lang) {
  FC.lang = lang;
  _step = 1;
  _showOnly('modulePage');
  applyT();
}

/* ══════════════════════════════════════════════
   STEP 2 — Module selection
══════════════════════════════════════════════ */
function selectModule(module) {
  _module = module;

  if (module === 'disease') {
    /* Disease module → skip Pi setup, go straight to disease app */
    _step = 4;
    _showOnly('diseaseApp');
    applyT();
    /* Push language into disease iframe */
    setTimeout(() => {
      try {
        const df = document.getElementById('if-crop-disease');
        if (df && df.contentWindow && df.contentWindow.onLangChange) {
          df.contentWindow.onLangChange(FC.lang);
        }
      } catch(e) {}
      frameReady(document.getElementById('if-crop-disease'));
    }, 400);
    FC.toast('🔬 Crop Disease AI ready', '');

  } else {
    /* Soil module → show Pi setup page */
    _step = 2;
    _showOnly('setupPage');
    applyT();
  }
}

/* ══════════════════════════════════════════════
   STEP 3 — Setup page: connect to Pi
══════════════════════════════════════════════ */
async function connectAndGo() {
  const btn = document.getElementById('S_connect_btn');
  if (btn) { btn.textContent = '⏳ Connecting…'; btn.disabled = true; }

  try {
    const res = await fetch(FC.getBase() + '/health', {
      signal: AbortSignal.timeout(4000)
    });
    if (!res.ok) throw new Error('Pi responded with error');
    enterSoilApp('live');
  } catch(e) {
    FC.toast('❌ Cannot reach Pi — switching to Demo Mode.', 'err');
    if (btn) { btn.textContent = t('connect_btn'); btn.disabled = false; }
    setTimeout(() => enterSoilApp('demo'), 1500);
  }
}

function demoAndGo() {
  enterSoilApp('demo');
}

function enterSoilApp(mode) {
  _step = 3;
  _showOnly('mainApp');
  applyT();

  if (mode === 'live') {
    FC.startPoll();
    FC.toast('✅ Connected to Pi!', 'ok');
  } else {
    FC.startDemo();
    FC.toast('⚡ Demo mode active', 'wrn');
  }

  /* Kick weather update */
  try { fetch(FC.getBase() + '/weather').catch(() => {}); } catch(e) {}

  /* Resize first iframe */
  setTimeout(() => {
    document.querySelectorAll('.tab-frame').forEach(f => {
      if (f.contentDocument) frameReady(f);
    });
  }, 800);
}

/* ══════════════════════════════════════════════
   Tab switching (Soil app)
══════════════════════════════════════════════ */
let _activeTab = 'dashboard';

function switchTab(name) {
  document.querySelectorAll('.tab-btn').forEach(b  => b.classList.remove('active'));
  document.querySelectorAll('.tab-page').forEach(p => p.classList.remove('active'));

  document.querySelector(`[data-tab="${name}"]`)?.classList.add('active');
  document.getElementById(`tab-${name}`)?.classList.add('active');
  _activeTab = name;

  if (FC.latest) {
    setTimeout(() => {
      const frame = document.getElementById(`if-${name}`);
      if (frame?.contentWindow?.onSensorData)  frame.contentWindow.onSensorData(FC.latest);
      if (frame?.contentWindow?.onLangChange)  frame.contentWindow.onLangChange(FC.lang);
    }, 150);
  }

  setTimeout(() => {
    const frame = document.getElementById(`if-${name}`);
    if (frame) frameReady(frame);
  }, 300);
}

/* ══════════════════════════════════════════════
   Initialise arrow state on page load
══════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  _updateArrows();
});
