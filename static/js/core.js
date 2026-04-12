/* ═══════════════════════════════════════════════
   FarmCare — core.js
   Shared state, sensor polling, demo mode, toast
═══════════════════════════════════════════════ */

window.FC = window.FC || {};

FC.latest = null;
FC.lang   = 'en';
FC.pollTimer = null;
FC.demoTimer = null;

FC.getBase = function() {
  const ip   = document.getElementById('piIp')?.value?.trim()   || '192.168.182.10';
  const port = document.getElementById('piPort')?.value?.trim() || '5000';
  return `http://${ip}:${port}`;
};

/* ── Toast ─────────────────────────────────────── */
let _toastT;
FC.toast = function(msg, type='') {
  const el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg;
  el.className   = 'show ' + type;
  clearTimeout(_toastT);
  _toastT = setTimeout(() => el.className = '', 3500);
};

/* ── Status dot ────────────────────────────────── */
FC.setStatus = function(state, text) {
  const dot  = document.getElementById('dot');
  const stxt = document.getElementById('stxt');
  if (dot)  dot.className  = 'dot' + (state==='live'?' live':state==='err'?' err':'');
  if (stxt) stxt.textContent = text;
};

/* ── Broadcast sensor data to all visible iframes ─ */
FC.broadcastSensor = function(data) {
  document.querySelectorAll('.tab-frame').forEach(frame => {
    try {
      if (frame.contentWindow && frame.contentWindow.onSensorData) {
        frame.contentWindow.onSensorData(data);
      }
    } catch(e) {}
  });
};

/* ── Broadcast language to all iframes ─────────── */
FC.broadcastLang = function(lang) {
  document.querySelectorAll('.tab-frame').forEach(frame => {
    try {
      if (frame.contentWindow && frame.contentWindow.onLangChange) {
        frame.contentWindow.onLangChange(lang);
      }
    } catch(e) {}
  });
};

/* ── Update UI on new sensor reading ───────────── */
FC.onNewReading = function(data) {
  FC.latest = data;
  const now = new Date();
  const el  = document.getElementById('lastUpd');
  if (el) el.textContent = 'Updated: ' + now.toLocaleTimeString();
  FC.broadcastSensor(data);
  FC.setStatus('live', '● Live');
};

/* ── Poll Raspberry Pi ─────────────────────────── */
FC.startPoll = function() {
  FC.stopAll();
  const url = FC.getBase() + '/sensor_data';
  FC.setStatus('', 'Connecting…');
  async function poll() {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(3500) });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      FC.onNewReading(await res.json());
    } catch(e) {
      FC.setStatus('err', 'Connection Error');
    }
  }
  poll();
  FC.pollTimer = setInterval(poll, 2500);
};

/* ── Demo mode ─────────────────────────────────── */
FC.startDemo = function() {
  FC.stopAll();
  FC.setStatus('live', '● Demo Mode');
  let tn = 0;
  function tick() {
    tn++;
    FC.onNewReading({
      temperature: +(24.5 + Math.sin(tn*0.3)*3  + rand(-0.5,0.5)).toFixed(1),
      moisture:    +(42   + Math.sin(tn*0.2)*10  + rand(-2,2)).toFixed(1),
      ec:          Math.round(350 + Math.sin(tn*0.15)*80 + rand(-10,10)),
      ph:          +(6.8  + Math.sin(tn*0.1)*0.8 + rand(-0.1,0.1)).toFixed(2),
      nitrogen:    Math.round(120 + Math.sin(tn*0.25)*40 + rand(-5,5)),
      phosphorus:  Math.round(85  + Math.sin(tn*0.2)*25  + rand(-3,3)),
      potassium:   Math.round(200 + Math.sin(tn*0.18)*50 + rand(-5,5)),
      timestamp:   new Date().toISOString(),
      read_count:  tn, error_count: 0
    });
  }
  tick();
  FC.demoTimer = setInterval(tick, 2500);
};

FC.stopAll = function() {
  clearInterval(FC.pollTimer);
  clearInterval(FC.demoTimer);
  FC.pollTimer = FC.demoTimer = null;
};

function rand(a, b) { return Math.random() * (b - a) + a; }

/* ── Auto-resize iframe to content ─────────────── */
window.frameReady = function(iframe) {
  try {
    const resize = () => {
      const h = iframe.contentDocument?.body?.scrollHeight;
      if (h) iframe.style.height = h + 'px';
    };
    iframe.contentWindow.addEventListener('resize', resize);
    resize();
    setInterval(resize, 800);
  } catch(e) {}
};
