// ================= Kaku · prática de leitura (usa a mesma base e a mesma validação de leituras da escrita) =================
const R_CATS = [['hiragana', 'Hiragana'], ['katakana', 'Katakana'], ['kanji', 'Kanji']];
const R_JLPT = ['N5', 'N4', 'N3', 'N2', 'N1'];
const R_SIZES = [10, 20, 30, 50];
function readingPool(D, cats, jlpt) {
  return D.characters.filter((e) => cats.includes(e.category) && (e.category !== 'kanji' || !jlpt.length || jlpt.includes(e.jlpt)));
}
// Ordem aleatória, sem repetir o mesmo caractere em sequência (nem entre o fim de uma sessão e o início da próxima).
function readingOrder(ids, n, avoidFirst) {
  let q = shuffle(ids).slice(0, n);
  if (q.length > 1 && q[0] === avoidFirst) { const j = 1 + (Math.random() * (q.length - 1) | 0); const t = q[0]; q[0] = q[j]; q[j] = t; }
  for (let i = 1; i < q.length; i++) if (q[i] === q[i - 1]) { const j = q.findIndex((x, k) => k > i && x !== q[i - 1]); if (j > 0) { const t = q[i]; q[i] = q[j]; q[j] = t; } }
  return q;
}
function answerOf(e) {
  // Resposta principal exibida + todas as aceitas
  if (e.category !== 'kanji') return { main: e.romaji, all: [e.romaji], kana: e.reading };
  const ro = uniq((e.readingsRomaji || []).map((r) => String(r).replace(/[()]/g, '')));
  return { main: ro.join(', '), all: ro, kana: e.readings.on.map((o) => o.kana).concat(e.readings.kun.map((k) => k.display)).join('、') };
}
// Histórico de leitura por usuário (guardado à parte do histórico de escrita).
const ReadSess = {
  start(label, n) { return UD.mut((d) => { d.readSessions = (d.readSessions || []).filter((x) => x.items.length); const x = { id: 'r' + uid(), start: Date.now(), label, planned: n, items: [] }; d.readSessions.push(x); return x.id; }); },
  record(sid, item) { UD.mut((d) => { const x = (d.readSessions || []).find((y) => y.id === sid); if (x) { x.items.push(item); x.end = item.t; } }); }
};
function readHistory(d) { return charHistory({ sessions: d && d.readSessions ? d.readSessions : [] }); }
function cleanAnswer(s) { return String(s || '').trim().replace(/\s+/g, ' ').toLowerCase(); }

class Component extends DCLogic {
  constructor(...a) {
    super(...a);
    this._page = PAGE;
    this.state = { view: 'setup', src: 'filters', cats: [], jlpt: [], listId: null, size: 20, prio: true, queue: [], i: 0, ans: '', res: null, done: [], label: '', lastIds: [], sid: null, t0: 0 };
    this.inputEl = null; this.nextEl = null;
    this.setInput = (el) => { this.inputEl = el; };
    this.setNext = (el) => { this.nextEl = el; };
  }
  componentDidMount() { waitForData(this); }
  focusSoon(which) { setTimeout(() => { const el = which === 'next' ? this.nextEl : this.inputEl; try { if (el) el.focus(); } catch (e) {} }, 30); }
  begin(ids, label) {
    if (!ids.length) return;
    const prevLast = this.state.queue[this.state.queue.length - 1];
    const q = readingOrder(ids, ids.length, prevLast);
    const sid = Auth.current() ? ReadSess.start(label, q.length) : null;
    this.setState({ view: 'quiz', queue: q, i: 0, ans: '', res: null, done: [], label, lastIds: ids, sid, t0: Date.now() });
    this.focusSoon('input');
  }
  start() {
    const D = kdb(); const st = this.state; if (!D) return;
    const lists = Lists.all();
    const pool = poolOf(D, st, lists).map((e) => e.id);
    const n = st.size === 'all' ? pool.length : Math.min(st.size, pool.length);
    const hist = Auth.current() ? readHistory(UD.data()) : null;
    this.begin(pickChars(pool, n, hist, st.prio), 'Leitura · ' + poolLabel(st, lists));
  }
  record(item) {
    if (this.state.sid) ReadSess.record(this.state.sid, Object.assign({ t: Date.now(), ms: Math.min(180000, Date.now() - this.state.t0) }, item));
    this.setState({ t0: Date.now() });
  }
  submit(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    const st = this.state; if (st.res) { this.next(); return; }
    const a = cleanAnswer(st.ans); if (!a) return;
    const D = kdb(), e = D._idx[st.queue[st.i]];
    const ok = readingOk(D, e, a);
    this.setState({ res: { ok, given: st.ans.trim(), skipped: false }, done: st.done.concat([{ id: e.id, ok, given: st.ans.trim() }]) });
    this.record({ c: e.id, ok: ok ? 1 : 0, given: st.ans.trim() });
    this.focusSoon('next');
  }
  skip() {
    const st = this.state; if (st.res) return;
    const done = st.done.concat([{ id: st.queue[st.i], ok: false, given: '', skipped: true }]);
    this.record({ c: st.queue[st.i], ok: 0, given: '', skipped: 1 });
    this.advance(done);
  }
  next() { this.advance(this.state.done); }
  advance(done) {
    const st = this.state;
    if (st.i + 1 >= st.queue.length) { this.setState({ done, view: 'result', res: null, ans: '' }); return; }
    this.setState({ done, i: st.i + 1, res: null, ans: '' });
    this.focusSoon('input');
  }
  renderVals() {
    const accent = this.props.accent ?? '#dc2626';
    const st = this.state, D = kdb();
    const base = { accent, loading: !D, vSetup: !!D && st.view === 'setup', vQuiz: !!D && st.view === 'quiz', vResult: !!D && st.view === 'result', inSession: !!D && st.view !== 'setup', toLogin: () => KS.set('returnTo', PAGE) };
    if (!D) return Object.assign(base, { cats: [], jlpts: [], sizes: [], rightList: [], wrongList: [], c: {} });
    const u = Auth.current(), data = u ? UD.load(u) : null, lists = data ? data.lists : [];
    const toggleIn = (arr, v) => arr.includes(v) ? arr.filter((x) => x !== v) : arr.concat([v]);
    const pool = poolOf(D, st, lists);
    const nPlan = st.size === 'all' ? pool.length : Math.min(st.size, pool.length);
    const hist = data ? readHistory(data) : {};
    const hardAll = Object.keys(hist).map((id) => Object.assign({ id }, hist[id])).filter((h) => h.fail > 0 && D._idx[h.id]).sort((a, b) => charWeight(b) - charWeight(a)).slice(0, 10);
    const lastS = data && data.readSessions ? data.readSessions.filter((x) => x.items.length).slice(-1)[0] : null;
    const setup = {
      logged: !!u, guest: !u, start: () => this.start(),
      srcFilters: st.src === 'filters', srcList: st.src === 'list',
      srcs: [['filters', 'Filtros'], ['list', 'Minha lista']].map(([id, label]) => Object.assign({ label, pick: () => this.setState({ src: id, listId: id === 'list' && !st.listId && lists[0] ? lists[0].id : st.listId }) }, segVals(st.src === id))),
      noneSel: !st.cats.length && !st.jlpt.length, allChip: chipVals(!st.cats.length && !st.jlpt.length), pickAll: () => this.setState({ cats: [], jlpt: [] }),
      cats: CAT_OPTS.map(([id, label]) => Object.assign({ label, count: fmtInt(D.characters.filter((e) => e.category === id).length), pick: () => this.setState({ cats: toggleIn(st.cats, id) }) }, chipVals(st.cats.includes(id)))),
      jlpts: JLPT_OPTS.map((lv) => Object.assign({ label: lv, count: fmtInt(D.characters.filter((e) => e.jlpt === lv).length), pick: () => this.setState({ jlpt: toggleIn(st.jlpt, lv) }) }, chipVals(st.jlpt.includes(lv)))),
      jlptNote: st.jlpt.length > 0 && st.cats.length > 0 && !st.cats.includes('kanji'),
      lists: lists.map((l) => { const on = st.listId === l.id; return { name: l.name, count: l.chars.length + (l.chars.length === 1 ? ' caractere' : ' caracteres'), preview: l.chars.slice(0, 8).map((id) => id.split(':')[1]).join(' '), pressed: on ? 'true' : 'false', bd: on ? accent : '#e7e5e4', bg: on ? '#fef2f2' : '#ffffff', pick: () => this.setState({ listId: l.id }),
        play: () => { this.setState({ src: 'list', listId: l.id }); this.begin(pickChars(l.chars, Math.min(l.chars.length, st.size === 'all' ? l.chars.length : st.size), readHistory(data), st.prio), 'Leitura · Lista: ' + l.name); }, empty: !l.chars.length, has: l.chars.length > 0 }; }),
      hasListsU: lists.length > 0, noListsU: !!u && lists.length === 0,
      poolLabel: poolLabel(st, lists), poolCount: fmtInt(pool.length), poolWord: pool.length === 1 ? 'caractere disponível' : 'caracteres disponíveis',
      poolEmpty: pool.length === 0, canStart: pool.length > 0,
      sizes: R_SIZES.map((n) => Object.assign({ label: String(n), pick: () => this.setState({ size: n }) }, segVals(st.size === n))).concat([Object.assign({ label: 'Todos', pick: () => this.setState({ size: 'all' }) }, segVals(st.size === 'all'))]),
      startLabel: 'Iniciar prática · ' + nPlan + (nPlan === 1 ? ' caractere' : ' caracteres'),
      prio: st.prio && !!u, prioAttr: st.prio && u ? 'true' : 'false', prioBg: st.prio && u ? accent : '#d6d3d1', prioX: st.prio && u ? '22px' : '2px', togglePrio: () => { if (u) this.setState({ prio: !st.prio }); },
      hard: hardAll.map((h) => ({ c: D._idx[h.id].char, sub: h.fail + (h.fail === 1 ? ' erro' : ' erros') + ' · ' + Math.round(h.ok / h.n * 100) + '%' })), hasHard: hardAll.length > 0, noHard: hardAll.length === 0,
      reviewHard: () => this.begin(hardAll.map((h) => h.id), 'Leitura · Revisão: mais erros'),
      hasLast: !!lastS, last: lastS ? { label: lastS.label, when: fmtDate(lastS.start, true), n: lastS.items.length, acc: pct(lastS.items.filter((i) => i.ok).length / lastS.items.length) } : { label: '', when: '', n: 0, acc: '' }
    };
    // ---------- quiz ----------
    const e = st.view === 'quiz' ? D._idx[st.queue[st.i]] : null;
    const T = e ? KTYPES[e.category] : { label: '', bg: '#f5f5f4', fg: '#44403c' };
    const A = e ? answerOf(e) : { main: '', all: [], kana: '' };
    const okN = st.done.filter((d) => d.ok).length, failN = st.done.length - okN;
    const answered = st.done.length;
    const r = st.res;
    const quiz = {
      c: e ? { ch: e.char, fs: Array.from(e.char).length > 1 ? '128px' : '160px', fsM: Array.from(e.char).length > 1 ? '96px' : '128px', tl: T.label, tb: T.bg, tf: T.fg, jlpt: e.jlpt || '', hasJlpt: !!e.jlpt,
        main: A.main, kana: A.kana, meaning: e.category === 'kanji' ? e.meaning.pt.join('; ') : '', hasMeaning: e.category === 'kanji' } : {},
      qLabel: 'Questão ' + (st.i + 1) + ' de ' + st.queue.length,
      scoreLabel: okN + (okN === 1 ? ' acerto' : ' acertos') + ' • ' + failN + (failN === 1 ? ' erro' : ' erros'),
      rateLabel: answered ? Math.round(okN / answered * 100) + '% de acerto' : '— de acerto',
      progW: Math.round((st.i + (r ? 1 : 0)) / Math.max(1, st.queue.length) * 100) + '%',
      ans: st.ans, onAns: (ev) => { if (!st.res) this.setState({ ans: ev.target.value }); },
      submit: (ev) => this.submit(ev), skip: () => this.skip(), next: () => this.next(),
      canSubmit: !r && cleanAnswer(st.ans).length > 0, cannotSubmit: !r && !cleanAnswer(st.ans).length,
      asking: !r, answered: !!r, locked: !!r,
      isOk: !!r && r.ok, isWrong: !!r && !r.ok, given: r ? r.given : '',
      inputBd: r ? (r.ok ? '#15803d' : '#dc2626') : '#d6d3d1', inputBg: r ? (r.ok ? '#f0fdf4' : '#fef2f2') : '#ffffff',
      nextLabel: st.i + 1 >= st.queue.length ? 'Ver resultado' : 'Próximo caractere',
      setInput: this.setInput, setNext: this.setNext,
      end: () => this.setState({ view: st.done.length ? 'result' : 'setup', res: null, ans: '' })
    };
    // ---------- resultado ----------
    const total = st.done.length;
    const wrong = st.done.filter((d) => !d.ok), right = st.done.filter((d) => d.ok);
    const result = {
      rTotal: total, rOk: right.length, rFail: wrong.length, rRate: total ? Math.round(right.length / total * 100) + '%' : '—',
      rHead: !total ? 'Prática encerrada' : right.length / total >= 0.8 ? 'Excelente leitura!' : right.length / total >= 0.5 ? 'Bom trabalho!' : 'Continue praticando',
      rLabel: st.label.replace(/^Leitura · /, '') + (st.queue.length > total ? ' · encerrada na questão ' + (total + 1) + ' de ' + st.queue.length : ''),
      rightList: right.map((d) => { const x = D._idx[d.id]; return { ch: x.char, sub: answerOf(x).all[0] }; }), hasRight: right.length > 0, noRight: !right.length,
      wrongList: wrong.map((d) => { const x = D._idx[d.id], a = answerOf(x); return { ch: x.char, given: d.skipped ? 'Pulado' : d.given, skipped: !!d.skipped, answered: !d.skipped, correct: a.main, kana: a.kana, meaning: x.category === 'kanji' ? x.meaning.pt.join('; ') : '—' }; }),
      hasWrong: wrong.length > 0, noWrong: !wrong.length, barOk: total ? Math.round(right.length / total * 100) + '%' : '0%',
      again: () => this.begin(st.lastIds.length ? st.lastIds : st.queue, st.label),
      onlyWrong: () => this.begin(uniq(wrong.map((d) => d.id)), 'Revisão dos erros'),
      backSetup: () => this.setState({ view: 'setup', res: null, ans: '' })
    };
    return Object.assign(base, setup, quiz, result);
  }
}
