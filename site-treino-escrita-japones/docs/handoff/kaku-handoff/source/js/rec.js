// ================= Kaku · desenho e reconhecimento (qualquer caractere da base) =================
// A referência é o próprio caractere renderizado com a fonte manuscrita do site.
// Assim, qualquer caractere que entrar na base passa a ter exercício, sem traçado cadastrado à mão.
const RES = 2;
const GLYPH_FONT = '"Klee One","Hiragino Mincho ProN","Yu Mincho","Noto Serif CJK JP","Noto Sans CJK JP",serif';
const Ink = {
  init(self) {
    self.strokes = []; self.cur = null; self.cv = null; self.ctx = null;
    self.setCanvas = (el) => { if (!el || el === self.cv) return; self.cv = el; el.width = CS * RES; el.height = CS * RES; self.ctx = el.getContext('2d'); Ink.redraw(self); };
    self.onDown = (e) => { if (self.state.res || self.state.busy || !self.ctx) return; e.preventDefault(); try { self.cv.setPointerCapture(e.pointerId); } catch (_) {} const p = Ink.pt(self, e); p.w = 22; self.cur = [p]; Ink.dot(self, p); };
    self.onMove = (e) => { if (!self.cur) return; e.preventDefault(); const p = Ink.pt(self, e); const a = self.cur[self.cur.length - 1]; const dist = Math.hypot(p.x - a.x, p.y - a.y); if (dist < 2) return; const v = dist / Math.max(1, p.t - a.t); const tw = Math.max(13, Math.min(28, 30 - v * 5)); p.w = a.w * 0.65 + tw * 0.35; self.cur.push(p); Ink.seg(self, a, p); };
    self.onUp = () => { if (!self.cur) return; self.strokes.push(self.cur); self.cur = null; self.setState({ count: self.strokes.length, warn: 0 }); };
    self.wipe = () => { self.strokes = []; self.cur = null; Ink.redraw(self); };
  },
  pt(self, e) { const r = self.cv.getBoundingClientRect(); return { x: (e.clientX - r.left) * (CS * RES / r.width), y: (e.clientY - r.top) * (CS * RES / r.height), t: e.timeStamp || Date.now() }; },
  seg(self, a, b) { const c = self.ctx; c.strokeStyle = '#1F1C18'; c.lineCap = 'round'; c.lineJoin = 'round'; c.lineWidth = (a.w + b.w) / 2 * (CS / 560 + 0.3); c.beginPath(); c.moveTo(a.x, a.y); c.lineTo(b.x, b.y); c.stroke(); },
  dot(self, p) { const c = self.ctx; c.fillStyle = '#1F1C18'; c.beginPath(); c.arc(p.x, p.y, p.w / 2 * (CS / 560 + 0.3), 0, Math.PI * 2); c.fill(); },
  redraw(self) { if (!self.ctx) return; self.ctx.clearRect(0, 0, CS * RES, CS * RES); self.strokes.forEach((s) => { Ink.dot(self, s[0]); for (let i = 1; i < s.length; i++) Ink.seg(self, s[i - 1], s[i]); }); }
};

const Rec = {
  N: 64, F: 52, R: 4, LW: 3, SIG: 4.5,
  OK: 0.6, ID_MIN: 0.33,
  cache: new Map(),
  ctx(n) { const c = document.createElement('canvas'); c.width = n; c.height = n; return c.getContext('2d', { willReadFrequently: true }); },
  alpha(x, n) { const d = x.getImageData(0, 0, n, n).data; const m = new Uint8Array(n * n); for (let i = 0; i < n * n; i++) m[i] = d[i * 4 + 3] > 60 ? 1 : 0; return m; },
  box(m, n) { let x0 = n, y0 = n, x1 = -1, y1 = -1; for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) if (m[y * n + x]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } return x1 < 0 ? null : { x0, y0, w: x1 - x0 + 1, h: y1 - y0 + 1 }; },
  // Formas "normais" são esticadas para o mesmo quadrado (cada pessoa escreve com proporções diferentes);
  // formas muito alongadas (一, ー, 丨) mantêm a proporção.
  fit(w, h) { const r = Math.min(w, h) / Math.max(w, h); if (r >= 0.35) return { sx: Rec.F / w, sy: Rec.F / h }; const s = Rec.F / Math.max(w, h); return { sx: s, sy: s }; },
  glyph(ch) {
    if (Rec.cache.has(ch)) return Rec.cache.get(ch);
    const S = 220, fs = 150, N = Rec.N;
    const font = fs + 'px ' + GLYPH_FONT;
    const x = Rec.ctx(S); x.font = font; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#000'; x.fillText(ch, S / 2, S / 2);
    const b = Rec.box(Rec.alpha(x, S), S);
    if (!b) { Rec.cache.set(ch, null); return null; }
    const k = Rec.fit(b.w, b.h), sc = Math.sqrt(k.sx * k.sy);
    const draw = (lw) => {
      const y = Rec.ctx(N);
      y.setTransform(k.sx, 0, 0, k.sy, N / 2 - (b.x0 + b.w / 2) * k.sx, N / 2 - (b.y0 + b.h / 2) * k.sy);
      y.font = font; y.textAlign = 'center'; y.textBaseline = 'middle'; y.fillStyle = '#000'; y.fillText(ch, S / 2, S / 2);
      if (lw) { y.lineWidth = lw / sc; y.strokeStyle = '#000'; y.lineJoin = 'round'; y.strokeText(ch, S / 2, S / 2); }
      return Rec.alpha(y, N);
    };
    const g = { thin: draw(0), wide: draw(2 * Rec.R) };
    Rec.cache.set(ch, g);
    return g;
  },
  user(strokes, size) {
    const N = Rec.N;
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    strokes.forEach((s) => s.forEach((p) => { x0 = Math.min(x0, p.x); x1 = Math.max(x1, p.x); y0 = Math.min(y0, p.y); y1 = Math.max(y1, p.y); }));
    const w = Math.max(x1 - x0, 1), h = Math.max(y1 - y0, 1);
    const k = Rec.fit(w, h), sc = Math.sqrt(k.sx * k.sy);
    const draw = (lw) => {
      const y = Rec.ctx(N);
      y.setTransform(k.sx, 0, 0, k.sy, N / 2 - (x0 + w / 2) * k.sx, N / 2 - (y0 + h / 2) * k.sy);
      y.lineWidth = lw / sc; y.lineCap = 'round'; y.lineJoin = 'round'; y.strokeStyle = '#000';
      strokes.forEach((s) => { y.beginPath(); y.moveTo(s[0].x, s[0].y); if (s.length === 1) y.lineTo(s[0].x + 0.5, s[0].y); for (let i = 1; i < s.length; i++) y.lineTo(s[i].x, s[i].y); y.stroke(); });
      return Rec.alpha(y, N);
    };
    return { thin: draw(Rec.LW), wide: draw(Rec.LW + 2 * Rec.R) };
  },
  // Distância de cada pixel até o traço mais próximo (chanfro 3-4), para uma comparação tolerante.
  dist(m) {
    const N = Rec.N, D = new Float32Array(N * N);
    for (let i = 0; i < N * N; i++) D[i] = m[i] ? 0 : 1e6;
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const i = y * N + x; let v = D[i];
      if (x > 0) v = Math.min(v, D[i - 1] + 3); if (y > 0) { v = Math.min(v, D[i - N] + 3); if (x > 0) v = Math.min(v, D[i - N - 1] + 4); if (x < N - 1) v = Math.min(v, D[i - N + 1] + 4); } D[i] = v; }
    for (let y = N - 1; y >= 0; y--) for (let x = N - 1; x >= 0; x--) { const i = y * N + x; let v = D[i];
      if (x < N - 1) v = Math.min(v, D[i + 1] + 3); if (y < N - 1) { v = Math.min(v, D[i + N] + 3); if (x < N - 1) v = Math.min(v, D[i + N + 1] + 4); if (x > 0) v = Math.min(v, D[i + N - 1] + 4); } D[i] = v; }
    for (let i = 0; i < N * N; i++) D[i] /= 3;
    return D;
  },
  score(u, g) {
    if (!u.d) u.d = Rec.dist(u.thin); if (!g.d) g.d = Rec.dist(g.thin);
    const s2 = 2 * Rec.SIG * Rec.SIG;
    let a = 0, pa = 0, b = 0, rb = 0;
    for (let i = 0; i < u.thin.length; i++) { if (u.thin[i]) { a++; pa += Math.exp(-g.d[i] * g.d[i] / s2); } if (g.thin[i]) { b++; rb += Math.exp(-u.d[i] * u.d[i] / s2); } }
    const P = a ? pa / a : 0, R = b ? rb / b : 0;
    return P + R ? 2 * P * R / (P + R) : 0;
  },
  candidates(D, t, userN) {
    const out = [t], seen = new Set([t.id]);
    const add = (e) => { if (e && !seen.has(e.id)) { seen.add(e.id); out.push(e); } };
    (t.related || []).slice(0, 8).forEach((id) => add(D._idx[id]));
    const len = Array.from(t.char).length;
    const near = D.characters.filter((e) => e.id !== t.id && Math.abs(e.strokes - userN) <= 1 && Array.from(e.char).length === len &&
      (t.category === 'kanji' ? e.category === 'kanji' || e.strokes <= 4 : (e.category !== 'kanji' || e.strokes <= 5)));
    shuffle(near).sort((a, b) => (a.jlpt === t.jlpt ? 0 : 1) - (b.jlpt === t.jlpt ? 0 : 1)).slice(0, 60).forEach(add);
    return out;
  },
  async fonts(text) {
    try { if (document.fonts && document.fonts.load) await Promise.race([document.fonts.load('150px "Klee One"', text), new Promise((r) => setTimeout(r, 1500))]); } catch (e) {}
  },
  async evaluate(self, D, t) {
    const cands = Rec.candidates(D, t, self.strokes.length);
    await Rec.fonts(cands.map((e) => e.char).join(''));
    const u = Rec.user(self.strokes, CS * RES), n = self.strokes.length;
    let best = null, bestTot = -9, bestF = 0, tf = 0, tTot = -9;
    cands.forEach((e) => {
      const g = Rec.glyph(e.char); if (!g) return;
      const f = Rec.score(u, g), tot = f - 0.035 * Math.abs(n - e.strokes);
      if (e === t) { tf = f; tTot = tot; }
      if (tot > bestTot) { bestTot = tot; best = e; bestF = f; }
    });
    let id = tTot >= bestTot - 0.04 ? t : best;
    if ((id === t ? tf : bestF) < Rec.ID_MIN) id = null;
    const shapeOk = tf >= Rec.OK, strokesOk = n === t.strokes;
    const verdict = id === t && shapeOk && strokesOk ? 'ok' : (id === t ? 'almost' : 'no');
    let img = ''; try { img = self.cv.toDataURL('image/png'); } catch (e) {}
    return { id: id ? id.id : null, verdict, sim: Math.round(tf * 100), user: n, exp: t.strokes, shapeOk, strokesOk, img };
  }
};

// ---------- respostas de leitura e significado ----------
function kanaTable(D) { if (D._kana) return D._kana; const m = {}; D.characters.forEach((e) => { if (e.category !== 'kanji' && e.romaji) m[e.char] = e.romaji; }); D._kana = m; return m; }
function kanaToRomaji(D, s) {
  const m = kanaTable(D), ch = Array.from(s); let out = '', dbl = false;
  for (let i = 0; i < ch.length; i++) {
    const c = ch[i], two = c + (ch[i + 1] || '');
    if (c === 'っ' || c === 'ッ') { dbl = true; continue; }
    if (c === 'ー') { out += out.slice(-1); continue; }
    let r;
    if (ch[i + 1] && m[two]) { r = m[two]; i++; } else r = m[c] != null ? m[c] : c;
    if (dbl && r) { out += r[0]; dbl = false; }
    out += r;
  }
  return out;
}
function canonRo(s) {
  s = String(s || '').toLowerCase().replace(/ā/g, 'aa').replace(/ī/g, 'ii').replace(/ū/g, 'uu').replace(/ē/g, 'ee').replace(/ō/g, 'ou').replace(/ô/g, 'ou').replace(/[^a-z]/g, '');
  return s.replace(/jy/g, 'j').replace(/shi/g, 'si').replace(/sh/g, 'sy').replace(/chi/g, 'ti').replace(/ch/g, 'ty').replace(/tsu/g, 'tu').replace(/fu/g, 'hu')
    .replace(/ji/g, 'zi').replace(/j/g, 'zy').replace(/di/g, 'zi').replace(/du/g, 'zu').replace(/oo/g, 'ou').replace(/nn/g, 'n').replace(/wo/g, 'o');
}
function readingKeys(D, e) {
  const k = new Set();
  const addRo = (r) => { const s = String(r); k.add(canonRo(s)); k.add(canonRo(s.replace(/\(.*?\)/g, ''))); };
  if (e.category === 'kanji') {
    (e.readingsRomaji || []).forEach(addRo);
    e.readings.on.concat(e.readings.kun).forEach((r) => { k.add(canonRo(kanaToRomaji(D, r.kana))); if (r.display) k.add(canonRo(kanaToRomaji(D, r.display.replace(/\(.*?\)/g, '')))); });
  } else { addRo(e.romaji); if (e.reading) k.add(canonRo(kanaToRomaji(D, e.reading))); }
  k.delete('');
  return k;
}
function readingOk(D, e, ans) {
  const a = String(ans || '').trim(); if (!a) return false;
  const ro = /[぀-ヿ]/.test(a) ? kanaToRomaji(D, a) : a;
  return readingKeys(D, e).has(canonRo(ro));
}
function meaningTokens(e) {
  const toks = [];
  e.meaning.pt.concat(e.meaning.en).forEach((m) => norm(m).replace(/\(.*?\)/g, ' ').split(/[,;\/]| ou | or /).forEach((t) => {
    t = t.replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim().replace(/^(o|a|os|as|um|uma|the|to|an) /, '');
    if (t) toks.push(t);
  }));
  return toks;
}
function meaningOk(e, ans) {
  const a = norm(ans).replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim().replace(/^(o|a|os|as|um|uma|the|to|an) /, '');
  if (a.length < 2) return false;
  return meaningTokens(e).some((t) => t === a || (a.length >= 3 && (' ' + t + ' ').includes(' ' + a + ' ')) || (t.length >= 4 && (' ' + a + ' ').includes(' ' + t + ' ')));
}
function readingText(e) {
  if (e.category !== 'kanji') return e.char + ' · ' + e.romaji;
  const on = e.readings.on.map((o) => o.kana).join('、'), kun = e.readings.kun.map((k) => k.display).join('、');
  return [on, kun].filter(Boolean).join(' ／ ');
}
function readingRomaji(e) { return e.category === 'kanji' ? (e.readingsRomaji || []).join(', ') : e.romaji; }
