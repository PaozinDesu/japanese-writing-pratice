// ================= Kaku · conta, dados do usuário e estatísticas =================
// Protótipo: tudo fica no armazenamento local do navegador (localStorage), separado por usuário.
// Em produção, Auth/UD/Sess devem ser trocados por chamadas a um servidor.
const KS = (() => {
  const P = 'kaku.v1.';
  const mem = (window.__kakuMem = window.__kakuMem || {});
  let ok = false;
  try { localStorage.setItem(P + '__t', '1'); localStorage.removeItem(P + '__t'); ok = true; } catch (e) {}
  const emit = () => { try { window.dispatchEvent(new CustomEvent('kaku:change')); } catch (e) {} };
  return {
    persistent: ok,
    get(k, d) { try { const v = ok ? localStorage.getItem(P + k) : mem[k]; return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { const s = JSON.stringify(v); let saved = false; if (ok) { try { localStorage.setItem(P + k, s); saved = true; } catch (e) {} } if (!saved) mem[k] = s; emit(); },
    del(k) { try { if (ok) localStorage.removeItem(P + k); } catch (e) {} delete mem[k]; emit(); }
  };
})();

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
function normEmail(e) { return String(e || '').trim().toLowerCase(); }
function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
function b64(buf) { let s = ''; new Uint8Array(buf).forEach((b) => { s += String.fromCharCode(b); }); return btoa(s); }
function weakHash(s) { let h1 = 0x811c9dc5, h2 = 0x01000193; for (let r = 0; r < 3000; r++) for (let i = 0; i < s.length; i++) { const c = s.charCodeAt(i); h1 = Math.imul(h1 ^ c, 16777619) >>> 0; h2 = Math.imul(h2 ^ (c + r), 2246822519) >>> 0; } return h1.toString(16) + h2.toString(16); }
async function hashPw(pw, salt, algo) {
  if (algo !== 'weak') {
    try {
      const enc = new TextEncoder();
      const key = await crypto.subtle.importKey('raw', enc.encode(pw), 'PBKDF2', false, ['deriveBits']);
      const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt: enc.encode(salt), iterations: 100000, hash: 'SHA-256' }, key, 256);
      return 'pbkdf2$' + b64(bits);
    } catch (e) { if (algo === 'pbkdf2') return null; }
  }
  return 'weak$' + weakHash(salt + '|' + pw);
}
function newSalt() { const a = new Uint8Array(16); try { crypto.getRandomValues(a); } catch (e) { a.forEach((_, i) => { a[i] = Math.random() * 256 | 0; }); } return b64(a); }

const Auth = {
  users() { return KS.get('users', {}); },
  current() { const s = KS.get('session', null); if (!s) return null; const u = Auth.users()[s.email]; return u && u.id === s.uid ? u : null; },
  checkLogin(f) {
    const e = {}; const email = normEmail(f.email);
    if (!email) e.email = 'Informe seu email.'; else if (!EMAIL_RE.test(email)) e.email = 'Digite um email válido, como nome@exemplo.com.';
    if (!f.pw) e.pw = 'Informe sua senha.';
    return e;
  },
  checkRegister(f) {
    const e = {}; const email = normEmail(f.email); const age = String(f.age == null ? '' : f.age).trim();
    if (!String(f.name || '').trim()) e.name = 'Informe seu nome.';
    if (!email) e.email = 'Informe seu email.'; else if (!EMAIL_RE.test(email)) e.email = 'Digite um email válido, como nome@exemplo.com.';
    else if (Auth.users()[email]) e.email = 'Este email já está cadastrado. Entre com ele ou use outro email.';
    if (!age) e.age = 'Informe sua idade.'; else if (!/^\d{1,3}$/.test(age) || +age < 1 || +age > 120) e.age = 'Digite uma idade entre 1 e 120.';
    if (!f.pw) e.pw = 'Crie uma senha.'; else if (f.pw.length < 6) e.pw = 'A senha precisa ter pelo menos 6 caracteres.';
    if (!f.pw2) e.pw2 = 'Confirme sua senha.'; else if (f.pw && f.pw !== f.pw2) e.pw2 = 'As senhas não coincidem.';
    return e;
  },
  async register(f) {
    const errors = Auth.checkRegister(f);
    if (Object.keys(errors).length) return { ok: false, errors };
    const email = normEmail(f.email), salt = newSalt(), hash = await hashPw(f.pw, salt);
    const users = Auth.users();
    if (users[email]) return { ok: false, errors: { email: 'Este email já está cadastrado. Entre com ele ou use outro email.' } };
    const user = { id: 'u' + uid(), name: String(f.name).trim(), email, age: +String(f.age).trim(), salt, hash, created: Date.now() };
    users[email] = user; KS.set('users', users); KS.set('lastEmail', email);
    return { ok: true, user };
  },
  async login(f) {
    const errors = Auth.checkLogin(f);
    if (Object.keys(errors).length) return { ok: false, errors };
    const email = normEmail(f.email); const u = Auth.users()[email];
    if (!u) return { ok: false, errors: { email: 'Não encontramos uma conta com este email. Confira o endereço ou crie uma conta.' } };
    const algo = u.hash.split('$')[0];
    const h = await hashPw(f.pw, u.salt, algo);
    if (h !== u.hash) return { ok: false, errors: { pw: 'Senha incorreta. Tente novamente.' } };
    KS.set('session', { uid: u.id, email, at: Date.now() }); KS.set('lastEmail', email);
    return { ok: true, user: u };
  },
  logout() { KS.del('session'); }
};

// ---------- dados por usuário ----------
const UD = {
  load(u) { const d = KS.get('user.' + u.id, null) || {}; d.lists = d.lists || []; d.sessions = d.sessions || []; return d; },
  save(u, d) { KS.set('user.' + u.id, d); },
  mut(fn) { const u = Auth.current(); if (!u) return null; const d = UD.load(u); const r = fn(d, u); UD.save(u, d); return r; },
  data() { const u = Auth.current(); return u ? UD.load(u) : null; }
};
function uniq(a) { return Array.from(new Set(a)); }
const Lists = {
  all() { const d = UD.data(); return d ? d.lists : []; },
  get(id) { return Lists.all().find((l) => l.id === id) || null; },
  nameError(name, exceptId) {
    const n = String(name || '').trim();
    if (!n) return 'Dê um nome para a lista.';
    if (n.length > 60) return 'Use no máximo 60 caracteres.';
    if (Lists.all().some((l) => l.id !== exceptId && l.name.toLowerCase() === n.toLowerCase())) return 'Você já tem uma lista com esse nome.';
    return '';
  },
  create(name, chars) {
    const err = Lists.nameError(name); if (err) return { error: err };
    return UD.mut((d) => { const l = { id: 'l' + uid(), name: String(name).trim(), chars: uniq(chars || []), created: Date.now(), updated: Date.now() }; d.lists.unshift(l); return l; }) || { error: 'Entre na sua conta para criar listas.' };
  },
  rename(id, name) { const err = Lists.nameError(name, id); if (err) return { error: err }; UD.mut((d) => { const l = d.lists.find((x) => x.id === id); if (l) { l.name = String(name).trim(); l.updated = Date.now(); } }); return { ok: true }; },
  remove(id) { UD.mut((d) => { d.lists = d.lists.filter((l) => l.id !== id); }); },
  add(id, charIds) { UD.mut((d) => { const l = d.lists.find((x) => x.id === id); if (l) { l.chars = uniq(l.chars.concat(charIds)); l.updated = Date.now(); } }); },
  removeChar(id, cid) { UD.mut((d) => { const l = d.lists.find((x) => x.id === id); if (l) { l.chars = l.chars.filter((c) => c !== cid); l.updated = Date.now(); } }); },
  toggle(id, cid) { const l = Lists.get(id); if (!l) return; if (l.chars.includes(cid)) Lists.removeChar(id, cid); else Lists.add(id, [cid]); }
};

// ---------- sessões de prática ----------
const Sess = {
  start(meta) {
    return UD.mut((d) => {
      d.sessions = d.sessions.filter((s) => s.items.length);
      const s = { id: 's' + uid(), start: Date.now(), end: Date.now(), ms: 0, label: meta.label, src: meta.src || null, planned: meta.n, items: [] };
      d.sessions.push(s); return s.id;
    });
  },
  record(sid, item) { UD.mut((d) => { const s = d.sessions.find((x) => x.id === sid); if (!s) return; s.items.push(item); s.end = item.t; s.ms += item.ms; }); }
};
function charHistory(d) {
  const m = {};
  (d ? d.sessions : []).forEach((s) => s.items.forEach((i) => {
    const h = m[i.c] || (m[i.c] = { n: 0, ok: 0, fail: 0, last: 0, lastOk: true });
    h.n++; if (i.ok) h.ok++; else h.fail++;
    if (i.t >= h.last) { h.last = i.t; h.lastOk = !!i.ok; }
  }));
  return m;
}
// Sorteio ponderado: caracteres com mais erros (e errados na última vez) aparecem com mais frequência.
function charWeight(h) { if (!h) return 1; const err = (h.fail + 0.5) / (h.n + 1); return 0.35 + 3 * err + (h.lastOk ? 0 : 1.2); }
function shuffle(a) { const b = a.slice(); for (let i = b.length - 1; i > 0; i--) { const j = Math.random() * (i + 1) | 0; const t = b[i]; b[i] = b[j]; b[j] = t; } return b; }
function pickChars(ids, n, hist, prioritize) {
  if (!prioritize || !hist) return shuffle(ids).slice(0, n);
  const keyed = ids.map((id) => ({ id, k: Math.pow(Math.random(), 1 / charWeight(hist[id])) }));
  keyed.sort((a, b) => b.k - a.k);
  return shuffle(keyed.slice(0, n).map((x) => x.id));
}

// ---------- estatísticas por período ----------
const PERIODS = [['hoje', 'Hoje'], ['semana', 'Esta semana'], ['mes', 'Este mês'], ['tudo', 'Todo o período']];
function dayStart(t) { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); }
function periodStart(p, now) {
  const d = new Date(dayStart(now));
  if (p === 'hoje') return d.getTime();
  if (p === 'semana') { d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); }
  if (p === 'mes') { d.setDate(1); return d.getTime(); }
  return 0;
}
const MONTHS = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
const WDAYS = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'];
function catOf(id) { return String(id).split(':')[0]; }
function fmtDur(ms) { const m = Math.round(ms / 60000); if (m < 1) return ms > 0 ? '< 1 min' : '0 min'; const h = Math.floor(m / 60); return h ? h + 'h ' + String(m % 60).padStart(2, '0') + 'min' : m + ' min'; }
function fmtInt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
function pct(x) { return x == null ? '—' : Math.round(x * 100) + '%'; }
function fmtDate(t, withTime) { const d = new Date(t); const s = d.getDate() + ' ' + MONTHS[d.getMonth()] + (d.getFullYear() !== new Date().getFullYear() ? ' ' + d.getFullYear() : ''); return withTime ? s + ', ' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0') : s; }
function buckets(period, now, firstT) {
  const out = [];
  if (period === 'hoje') { const t0 = dayStart(now); for (let h = 0; h < 24; h++) out.push({ a: t0 + h * 3600e3, b: t0 + (h + 1) * 3600e3, label: h % 6 === 0 ? h + 'h' : '', full: h + 'h–' + (h + 1) + 'h', cur: new Date(now).getHours() === h }); return out; }
  if (period === 'semana') { const t0 = periodStart('semana', now); for (let i = 0; i < 7; i++) { const a = new Date(t0); a.setDate(a.getDate() + i); const b = new Date(a); b.setDate(b.getDate() + 1); out.push({ a: a.getTime(), b: b.getTime(), label: WDAYS[i], full: WDAYS[i] + ', ' + fmtDate(a.getTime()), cur: a.getTime() === dayStart(now) }); } return out; }
  if (period === 'mes') { const t0 = new Date(periodStart('mes', now)); const m = t0.getMonth(); for (let i = 1; i <= 31; i++) { const a = new Date(t0); a.setDate(i); if (a.getMonth() !== m) break; const b = new Date(a); b.setDate(i + 1); out.push({ a: a.getTime(), b: b.getTime(), label: (i === 1 || i % 5 === 0) ? String(i) : '', full: fmtDate(a.getTime()), cur: a.getTime() === dayStart(now) }); } return out; }
  const end = new Date(periodStart('mes', now)); let start = new Date(firstT ? dayStart(firstT) : now); start.setDate(1);
  const minStart = new Date(end); minStart.setMonth(minStart.getMonth() - 5); if (start > minStart) start = minStart;
  for (let a = new Date(start); a <= end; a.setMonth(a.getMonth() + 1)) { const b = new Date(a); b.setMonth(b.getMonth() + 1); out.push({ a: a.getTime(), b: b.getTime(), label: MONTHS[a.getMonth()], full: MONTHS[a.getMonth()] + ' ' + a.getFullYear(), cur: a.getTime() === end.getTime() }); }
  return out.slice(-18);
}
function computeStats(d, period, now) {
  now = now || Date.now();
  const t0 = periodStart(period, now);
  const items = [], sess = [];
  let firstT = 0;
  (d ? d.sessions : []).forEach((s) => {
    const its = s.items.filter((i) => i.t >= t0 && i.t <= now);
    s.items.forEach((i) => { if (!firstT || i.t < firstT) firstT = i.t; });
    if (its.length) { sess.push({ s, items: its }); its.forEach((i) => items.push(i)); }
  });
  const n = items.length, ok = items.filter((i) => i.ok).length, fail = n - ok;
  const ms = items.reduce((a, i) => a + (i.ms || 0), 0);
  const per = {};
  items.forEach((i) => { const p = per[i.c] || (per[i.c] = { id: i.c, n: 0, ok: 0, fail: 0 }); p.n++; if (i.ok) p.ok++; else p.fail++; });
  const chars = Object.values(per);
  const byCat = { hiragana: { seen: 0, ok: 0 }, katakana: { seen: 0, ok: 0 }, kanji: { seen: 0, ok: 0 } };
  chars.forEach((p) => { const c = byCat[catOf(p.id)]; if (c) { c.seen++; if (p.ok) c.ok++; } });
  const top = chars.slice().sort((a, b) => b.n - a.n || b.ok - a.ok).slice(0, 8);
  const hard = chars.filter((p) => p.fail > 0).sort((a, b) => b.fail - a.fail || a.ok / a.n - b.ok / b.n).slice(0, 8);
  const series = buckets(period, now, firstT).map((B) => { const its = items.filter((i) => i.t >= B.a && i.t < B.b); const k = its.filter((i) => i.ok).length; return Object.assign({}, B, { n: its.length, ok: k, fail: its.length - k, acc: its.length ? k / its.length : null }); });
  const sessions = sess.sort((a, b) => b.s.start - a.s.start).map(({ s, items: its }) => { const k = its.filter((i) => i.ok).length; return { id: s.id, start: s.start, label: s.label, n: its.length, ok: k, fail: its.length - k, acc: k / its.length, ms: its.reduce((a, i) => a + (i.ms || 0), 0), demo: !!s.demo }; });
  return { period, n, ok, fail, rate: n ? ok / n : null, ms, sessions, chars, unique: chars.length, byCat, top, hard, series };
}
function streakOf(d, now) {
  now = now || Date.now();
  const days = new Set();
  (d ? d.sessions : []).forEach((s) => s.items.forEach((i) => days.add(dayStart(i.t))));
  let t = dayStart(now); if (!days.has(t)) { const y = new Date(t); y.setDate(y.getDate() - 1); t = y.getTime(); }
  let n = 0;
  while (days.has(t)) { n++; const y = new Date(t); y.setDate(y.getDate() - 1); t = y.getTime(); }
  return n;
}

// ---------- dados de exemplo (para testar filtros e gráficos) ----------
function demoHistory(D, now) {
  now = now || Date.now();
  const pool = D.characters.filter((e) => e.category !== 'kanji' ? e.group === 'basico' : (e.jlpt === 'N5' || e.jlpt === 'N4')).map((e) => e.id);
  const skill = {}; pool.forEach((id) => { skill[id] = 0.45 + Math.random() * 0.5; });
  const sessions = []; const today = dayStart(now);
  const mk = (t, n) => {
    const chars = shuffle(pool).slice(0, n); const items = []; let tt = t;
    chars.forEach((c) => { const ms = 12000 + Math.random() * 30000; tt += ms; const age = (now - t) / 864e5; const p = Math.min(0.97, skill[c] + (120 - age) / 600); items.push({ c, ok: Math.random() < p ? 1 : 0, v: '', s: 0, t: tt, ms: Math.round(ms), rd: '', mn: '' }); });
    sessions.push({ id: 's' + uid(), start: t, end: tt, ms: items.reduce((a, i) => a + i.ms, 0), label: 'Sessão de exemplo', src: null, planned: n, items, demo: true });
  };
  for (let k = 120; k >= 1; k--) {
    if (Math.random() < 0.28) continue;
    const day = new Date(today); day.setDate(day.getDate() - k);
    const t = day.getTime() + (8 + Math.random() * 13) * 3600e3;
    mk(t, 6 + (Math.random() * 18 | 0));
  }
  mk(Math.max(today + 60e3, now - 20 * 60e3), 12);
  return sessions;
}

// ---------- intenção entre telas (ex.: "Praticar este caractere") ----------
const Intent = {
  set(v) { KS.set('intent', Object.assign({ at: Date.now() }, v)); },
  take() { const v = KS.get('intent', null); if (!v) return null; KS.del('intent'); return Date.now() - v.at < 15 * 60e3 ? v : null; }
};

// ---------- cabeçalho: área do usuário ----------
function acctBind(self) {
  if (self._acctBound) return;
  self._acctBound = true;
  const f = () => { try { self.forceUpdate(); } catch (e) {} };
  window.addEventListener('storage', (e) => { if (!e.key || e.key.indexOf('kaku.') === 0) f(); });
  window.addEventListener('kaku:change', f);
  window.addEventListener('focus', f);
}
function acctVals(self) {
  acctBind(self);
  const u = Auth.current();
  const open = !!self._acctOpen && !!u;
  const d = u ? UD.load(u) : null;
  const streak = d ? streakOf(d) : 0;
  const first = u ? u.name.split(/\s+/)[0] : '';
  const initials = u ? u.name.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join('') : '';
  const here = self._page || 'Main.dc.html';
  return {
    acct: {
      in: !!u, out: !u, name: first, full: u ? u.name : '', email: u ? u.email : '', initials,
      open, openAttr: open ? 'true' : 'false', streak, hasStreak: streak > 0, streakLabel: streak + (streak === 1 ? ' dia' : ' dias'),
      toggle: () => { self._acctOpen = !open; self.forceUpdate(); },
      close: () => { self._acctOpen = false; self.forceUpdate(); },
      logout: () => { self._acctOpen = false; Auth.logout(); },
      toLogin: () => { KS.set('returnTo', here); },
      persistent: KS.persistent, volatile: !KS.persistent
    }
  };
}
// Os quadros rodam num iframe sem permissão de enviar formulários: o Enter e o botão de envio
// chamam o handler diretamente. Para cada função `x` devolvida, cria `xKey` (Enter num campo -> x).
function enterTo(fn) {
  return (ev) => {
    if (!ev || ev.key !== 'Enter' || ev.shiftKey || ev.isComposing || ev.keyCode === 229) return;
    const tag = ev.target && ev.target.tagName;
    if (tag !== 'INPUT') return;
    ev.preventDefault();
    fn(ev);
  };
}
function addEnterKeys(o) {
  if (!o || typeof o !== 'object' || Array.isArray(o)) return;
  Object.keys(o).forEach((k) => { if (typeof o[k] === 'function' && !k.endsWith('Key')) o[k + 'Key'] = enterTo(o[k]); });
}
function withAcct(self, vals) {
  const v = Object.assign(vals || {}, acctVals(self));
  addEnterKeys(v);
  Object.keys(v).forEach((k) => { const x = v[k]; if (x && typeof x === 'object' && !Array.isArray(x)) addEnterKeys(x); });
  return v;
}

// ---------- "Adicionar à lista de prática" (páginas de detalhe) ----------
function listPickerVals(self, charId, accent) {
  const u = Auth.current();
  const open = self._alOpen === charId;
  const lists = u ? UD.load(u).lists : [];
  const msg = self._alMsgFor === charId ? self._alMsg || '' : '';
  const err = self._alErrFor === charId ? self._alErr || '' : '';
  const create = (ev) => {
    if (ev && ev.preventDefault) ev.preventDefault();
    const name = self._alName || '';
    const r = Lists.create(name, [charId]);
    if (r.error) { self._alErr = r.error; self._alErrFor = charId; } else { self._alErr = ''; self._alName = ''; self._alMsg = 'Lista “' + r.name + '” criada com este caractere.'; self._alMsgFor = charId; }
    self.forceUpdate();
  };
  const inCount = lists.filter((l) => l.chars.includes(charId)).length;
  return {
    al: {
      open, closed: !open, openAttr: open ? 'true' : 'false', in: !!u, out: !u,
      label: inCount ? 'Em ' + inCount + (inCount === 1 ? ' lista' : ' listas') : 'Adicionar à lista de prática',
      short: inCount ? 'Em ' + inCount + (inCount === 1 ? ' lista' : ' listas') : 'Adicionar à lista',
      toggle: () => { self._alOpen = open ? null : charId; self._alMsg = ''; self._alErr = ''; self.forceUpdate(); },
      lists: lists.map((l) => {
        const has = l.chars.includes(charId);
        return { name: l.name, count: l.chars.length + (l.chars.length === 1 ? ' caractere' : ' caracteres'), has, not: !has, pressed: has ? 'true' : 'false', bg: has ? '#FBEDEA' : '#FFFFFF', bd: has ? accent : '#E6E0D6',
          pick: () => { Lists.toggle(l.id, charId); self._alMsg = (has ? 'Removido de “' : 'Adicionado a “') + l.name + '”.'; self._alMsgFor = charId; self._alErr = ''; self.forceUpdate(); } };
      }),
      hasLists: lists.length > 0, noLists: lists.length === 0,
      name: self._alName || '', onName: (ev) => { self._alName = ev.target.value; self._alErr = ''; self.forceUpdate(); },
      create, err, hasErr: !!err, msg, hasMsg: !!msg,
      toLogin: () => { KS.set('returnTo', self._page || 'Caracteres.dc.html'); }
    },
    practiceThis: () => Intent.set({ kind: 'chars', chars: [charId], label: 'Caractere ' + charId.split(':')[1] })
  };
}
