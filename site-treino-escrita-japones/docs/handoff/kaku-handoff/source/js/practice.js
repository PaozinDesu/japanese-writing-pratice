// ================= Kaku · sessão de prática (usa a mesma base das páginas de caracteres) =================
const SIZES = [10, 20, 30, 50];
const CAT_OPTS = [['hiragana', 'Hiragana'], ['katakana', 'Katakana'], ['kanji', 'Kanji']];
const JLPT_OPTS = ['N5', 'N4', 'N3', 'N2', 'N1'];
function poolOf(D, st, lists) {
  if (st.src === 'list') { const l = lists.find((x) => x.id === st.listId); return l ? l.chars.map((id) => D._idx[id]).filter(Boolean) : []; }
  const cats = st.cats, jl = st.jlpt;
  return D.characters.filter((e) => {
    if (jl.length) return e.category === 'kanji' ? jl.includes(e.jlpt) && (!cats.length || cats.includes('kanji')) : cats.includes(e.category);
    return !cats.length || cats.includes(e.category);
  });
}
function poolLabel(st, lists) {
  if (st.src === 'list') { const l = lists.find((x) => x.id === st.listId); return l ? 'Lista: ' + l.name : 'Lista'; }
  const c = st.cats.map((id) => CAT_OPTS.find((o) => o[0] === id)[1]);
  const j = st.jlpt.slice().sort().reverse();
  if (!c.length && !j.length) return 'Todos os caracteres';
  if (!c.length) return 'Kanji · ' + j.join(' + ');
  return c.join(' + ') + (j.length && st.cats.includes('kanji') ? ' · ' + j.join(' + ') : '');
}
function chipVals(on, accent) { return { pressed: on ? 'true' : 'false', bg: on ? '#1F1C18' : '#FFFFFF', fg: on ? '#FFFFFF' : '#3B3630', bd: on ? '#1F1C18' : '#E6E0D6' }; }
function segVals(on) { return { pressed: on ? 'true' : 'false', bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F1C18' : '#5E5850', fw: on ? '700' : '500', sh: on ? '0 1px 3px rgba(31,28,24,.12)' : 'none' }; }
const EMPTY_T = { c: '', tl: '', tb: '#EFEAE1', tf: '#5E5850', n: 0, jlpt: '', hasJlpt: false, pt: '', en: '', r: '', ro: '', romaji: '', gs: '150px', gsS: '64px' };
function tOf(e) {
  const T = KTYPES[e.category], two = Array.from(e.char).length > 1;
  return { id: e.id, c: e.char, tl: T.label, tb: T.bg, tf: T.fg, n: e.strokes, jlpt: e.jlpt || '', hasJlpt: !!e.jlpt, pt: e.meaning.pt.join('; '), en: e.meaning.en.join('; '),
    r: readingText(e), ro: readingRomaji(e), gs: two ? '108px' : '150px', gsM: two ? '76px' : '104px', gsS: two ? '40px' : '60px', gsG: two ? Math.round(CS * 0.42) + 'px' : Math.round(CS * 0.7) + 'px', isKanji: e.category === 'kanji' };
}

class Component extends DCLogic {
  constructor(...a) {
    super(...a);
    this._page = PAGE;
    this.state = {
      view: 'setup', src: 'filters', cats: [], jlpt: [], listId: null, size: 20, prio: true, memory: false,
      queue: [], i: 0, done: [], sid: null, label: '', saved: false, t0: 0,
      count: 0, res: null, busy: false, showChar: true, rdShow: false, mnShow: false, rdAns: '', mnAns: '', rdRes: '', mnRes: '', over: null,
      guide: true, ghost: false, warn: 0
    };
    Ink.init(this);
  }
  componentDidMount() {
    waitForData(this);
    this.takeIntent();
    this._onStore = (e) => { if (!e || !e.key || e.key === 'kaku.v1.intent') setTimeout(() => this.takeIntent(), 0); };
    window.addEventListener('storage', this._onStore);
  }
  componentWillUnmount() { window.removeEventListener('storage', this._onStore); }
  takeIntent(tries) {
    const D = kdb();
    if (!D) { if ((tries || 0) < 60) setTimeout(() => this.takeIntent((tries || 0) + 1), 200); return; }
    const it = Intent.take(); if (!it) return;
    if (it.kind === 'filters') { this.setState({ view: 'setup', src: 'filters', cats: it.cats || [], jlpt: it.jlpt || [] }); return; }
    if (it.kind === 'chars') this.startWith(it.chars, it.label || 'Prática rápida', null);
    if (it.kind === 'list') { const l = Lists.get(it.listId); if (l && l.chars.length) { this.setState({ src: 'list', listId: l.id }); this.startWith(pickChars(l.chars, Math.min(l.chars.length, this.state.size), charHistory(UD.data()), this.state.prio), 'Lista: ' + l.name, { list: l.id }); } }
  }
  fresh() { return { count: 0, res: null, busy: false, showChar: !this.state.memory, rdShow: false, mnShow: false, rdAns: '', mnAns: '', rdRes: '', mnRes: '', over: null, warn: 0, t0: Date.now() }; }
  startWith(ids, label, src) {
    if (!ids.length) return;
    const u = Auth.current();
    const sid = u ? Sess.start({ label, src, n: ids.length }) : null;
    this.wipe();
    this.setState(Object.assign({ view: 'session', queue: ids, i: 0, done: [], sid, label, saved: !!u }, this.fresh(), { showChar: !this.state.memory }));
  }
  start() {
    const D = kdb(); if (!D) return;
    const st = this.state, lists = Lists.all();
    const pool = poolOf(D, st, lists).map((e) => e.id);
    if (!pool.length) return;
    const n = st.size === 'all' ? pool.length : Math.min(st.size, pool.length);
    const hist = Auth.current() ? charHistory(UD.data()) : null;
    this.startWith(pickChars(pool, n, hist, st.prio), poolLabel(st, lists), st.src === 'list' ? { list: st.listId } : { cats: st.cats, jlpt: st.jlpt });
  }
  finalOk() {
    const st = this.state; if (!st.res) return false;
    if (st.over != null) return st.over;
    return st.res.verdict === 'ok' && st.rdRes !== 'no' && st.mnRes !== 'no';
  }
  commit() {
    const st = this.state, id = st.queue[st.i];
    const item = { c: id, ok: this.finalOk() ? 1 : 0, v: st.res ? st.res.verdict : '', s: st.res ? st.res.sim : 0, t: Date.now(), ms: Math.min(180000, Date.now() - st.t0), rd: st.rdRes || (st.rdShow ? 'shown' : ''), mn: st.mnRes || (st.mnShow ? 'shown' : '') };
    if (st.sid) Sess.record(st.sid, item);
    return st.done.concat([item]);
  }
  next() {
    const st = this.state; if (!st.res) return;
    const done = this.commit();
    this.wipe();
    if (st.i + 1 >= st.queue.length) this.setState({ done, view: 'summary', res: null, count: 0 });
    else this.setState(Object.assign({ done, i: st.i + 1 }, this.fresh()));
  }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
    const st = this.state, D = kdb(), u = Auth.current(), data = u ? UD.load(u) : null, lists = data ? data.lists : [];
    const base = { accent, loading: !D, vSetup: !!D && st.view === 'setup', vSession: !!D && st.view === 'session', vSummary: !!D && st.view === 'summary', logged: !!u, guest: !u,
      toLogin: () => KS.set('returnTo', PAGE) };
    if (!D) return Object.assign(base, { cats: [], jlpts: [], sizes: [], lists: [], t: EMPTY_T, queue: [], results: [] });

    // ---------- configuração ----------
    const cnt = (patch) => poolOf(D, Object.assign({}, st, { src: 'filters' }, patch), lists).length;
    const toggleIn = (arr, v) => arr.includes(v) ? arr.filter((x) => x !== v) : arr.concat([v]);
    const cats = CAT_OPTS.map(([id, label]) => Object.assign({ label, count: fmtInt(D.characters.filter((e) => e.category === id).length), pick: () => this.setState({ cats: toggleIn(st.cats, id) }) }, chipVals(st.cats.includes(id))));
    const jlpts = JLPT_OPTS.map((lv) => Object.assign({ label: lv, count: fmtInt(D.characters.filter((e) => e.jlpt === lv).length), pick: () => this.setState({ jlpt: toggleIn(st.jlpt, lv) }) }, chipVals(st.jlpt.includes(lv))));
    const pool = poolOf(D, st, lists);
    const listCards = lists.map((l) => { const on = st.listId === l.id; return { name: l.name, count: l.chars.length + (l.chars.length === 1 ? ' caractere' : ' caracteres'), preview: l.chars.slice(0, 8).map((id) => id.split(':')[1]).join(' '), pressed: on ? 'true' : 'false', bd: on ? accent : '#E6E0D6', bg: on ? '#FBEDEA' : '#FFFFFF', pick: () => this.setState({ listId: l.id }),
      play: () => { this.setState({ src: 'list', listId: l.id }); this.startWith(pickChars(l.chars, Math.min(l.chars.length, st.size === 'all' ? l.chars.length : st.size), charHistory(data), st.prio), 'Lista: ' + l.name, { list: l.id }); }, empty: !l.chars.length, has: l.chars.length > 0 }; });
    const nPlan = st.size === 'all' ? pool.length : Math.min(st.size, pool.length);
    const hist = data ? charHistory(data) : {};
    const hardAll = Object.keys(hist).map((id) => Object.assign({ id }, hist[id])).filter((h) => h.fail > 0 && D._idx[h.id]).sort((a, b) => charWeight(b) - charWeight(a)).slice(0, 10);
    const lastS = data ? data.sessions.filter((s) => s.items.length).slice(-1)[0] : null;
    const setup = {
      start: () => this.start(), srcFilters: st.src === 'filters', srcList: st.src === 'list',
      srcs: [['filters', 'Filtros'], ['list', 'Minha lista']].map(([id, label]) => Object.assign({ label, pick: () => this.setState({ src: id, listId: id === 'list' && !st.listId && lists[0] ? lists[0].id : st.listId }) }, segVals(st.src === id))),
      noneSel: !st.cats.length && !st.jlpt.length, allChip: chipVals(!st.cats.length && !st.jlpt.length), pickAll: () => this.setState({ cats: [], jlpt: [] }),
      jlptNote: st.jlpt.length > 0 && st.cats.length > 0 && !st.cats.includes('kanji'),
      poolLabel: poolLabel(st, lists), poolCount: fmtInt(pool.length), poolWord: pool.length === 1 ? 'caractere disponível' : 'caracteres disponíveis',
      poolEmpty: pool.length === 0, canStart: pool.length > 0,
      sizes: SIZES.map((n) => Object.assign({ label: String(n), pick: () => this.setState({ size: n }) }, segVals(st.size === n))).concat([Object.assign({ label: 'Todos', pick: () => this.setState({ size: 'all' }) }, segVals(st.size === 'all'))]),
      startLabel: 'Começar · ' + nPlan + (nPlan === 1 ? ' caractere' : ' caracteres'),
      memory: st.memory, copy: !st.memory,
      modes: [[false, 'Com modelo', 'O caractere fica visível para copiar'], [true, 'De memória', 'Você vê só o significado e a leitura']].map(([m, label, sub]) => Object.assign({ label, sub, pick: () => this.setState({ memory: m }), ring: st.memory === m ? accent : '#E6E0D6', rbg: st.memory === m ? '#FBEDEA' : '#FFFFFF', dot: st.memory === m ? accent : '#FFFFFF', dotBd: st.memory === m ? accent : '#B5ADA2' }, segVals(st.memory === m))),
      prio: st.prio && !!u, prioAttr: st.prio && !!u ? 'true' : 'false', prioBg: st.prio && u ? accent : '#D9D1C4', prioX: st.prio && u ? '22px' : '2px', togglePrio: () => { if (u) this.setState({ prio: !st.prio }); },
      hasListsU: lists.length > 0, noListsU: !!u && lists.length === 0,
      hard: hardAll.map((h) => ({ c: D._idx[h.id].char, sub: h.fail + (h.fail === 1 ? ' erro' : ' erros') + ' · ' + Math.round(h.ok / h.n * 100) + '%' })), hasHard: hardAll.length > 0, noHard: hardAll.length === 0,
      reviewHard: () => this.startWith(shuffle(hardAll.map((h) => h.id)), 'Revisão: mais erros', { review: true }),
      hasLast: !!lastS, last: lastS ? { label: lastS.label, when: fmtDate(lastS.start, true), n: lastS.items.length, acc: pct(lastS.items.filter((i) => i.ok).length / lastS.items.length) } : { label: '', when: '', n: 0, acc: '' }
    };

    // ---------- sessão ----------
    const e = st.view === 'session' ? D._idx[st.queue[st.i]] : null;
    const t = e ? tOf(e) : EMPTY_T;
    const r = st.res;
    const idE = r && r.id ? D._idx[r.id] : null;
    const V = r ? ({ ok: { label: 'Correto!', sub: 'Seu desenho corresponde ao caractere pedido.', fg: '#4E6E3A', bg: '#E7EEDF' },
      almost: { label: 'Quase lá', sub: r.shapeOk ? 'Forma reconhecida, mas você usou ' + r.user + (r.user === 1 ? ' traço' : ' traços') + ' — o esperado são ' + r.exp + '.' : 'Reconhecemos o caractere, mas a forma ainda pode ficar mais precisa.', fg: '#7A5210', bg: '#F4EAD6' },
      no: { label: 'Não corresponde', sub: idE ? 'Parece “' + idE.char + '” em vez de “' + e.char + '”. Compare com o modelo e tente de novo.' : 'Não conseguimos reconhecer o desenho. Compare com o modelo e tente de novo.', fg: '#A8292A', bg: '#F8E4E0' } })[r.verdict] : { label: '', sub: '', fg: '#1F1C18', bg: '#FFFFFF' };
    const fin = this.finalOk();
    const doneOk = st.done.filter((i) => i.ok).length;
    const total = st.queue.length || 1;
    const pos = Math.min(st.i + (r ? 1 : 0), total);
    const pill = (on) => ({ bg: on ? '#1F1C18' : '#FFFFFF', fg: on ? '#FFFFFF' : '#5E5850', bd: on ? '#1F1C18' : '#E6E0D6' });
    const g = pill(st.guide), h = pill(st.ghost);
    const answerChip = (res) => res === 'ok' ? { on: true, ok: true, no: false, label: 'Certo', fg: '#4E6E3A', bg: '#E7EEDF' } : res === 'no' ? { on: true, ok: false, no: true, label: 'Não é essa', fg: '#A8292A', bg: '#F8E4E0' } : { on: false, ok: false, no: false, label: '', fg: '#1F1C18', bg: '#FFFFFF' };
    const session = {
      t, label: st.label, numLabel: (st.i + 1) + ' de ' + st.queue.length + (st.queue.length === 1 ? ' caractere' : ' caracteres'),
      progW: Math.round(pos / total * 100) + '%', okN: doneOk, failN: st.done.length - doneOk,
      showChar: st.showChar, hideChar: !st.showChar, toggleChar: () => this.setState({ showChar: !st.showChar }), charBtn: st.showChar ? 'Ocultar caractere' : 'Mostrar caractere',
      memPrompt: st.memory, copyPrompt: !st.memory,
      lead: t.isKanji ? 'Escreva o kanji que significa' : 'Escreva em ' + t.tl.toLowerCase() + ' o som',
      main: t.isKanji ? t.pt : '“' + t.ro + '”',
      mainSub: t.isKanji ? t.en : '',
      isKanji: t.isKanji, isKana: !t.isKanji,
      askRd: !(st.memory && !t.isKanji), askMn: t.isKanji && !st.memory, rdTitle: t.isKanji ? 'Leitura' : 'Som (romaji)',
      rdShow: st.rdShow, rdHide: !st.rdShow, showRd: () => this.setState({ rdShow: true }),
      mnShow: st.mnShow, mnHide: !st.mnShow, showMn: () => this.setState({ mnShow: true }),
      rdAns: st.rdAns, mnAns: st.mnAns, rdChip: answerChip(st.rdRes), mnChip: answerChip(st.mnRes),
      onRd: (ev) => this.setState({ rdAns: ev.target.value, rdRes: '' }), onMn: (ev) => this.setState({ mnAns: ev.target.value, mnRes: '' }),
      checkRd: (ev) => { if (ev && ev.preventDefault) ev.preventDefault(); if (!st.rdAns.trim()) return; const ok = readingOk(D, e, st.rdAns); this.setState({ rdRes: ok ? 'ok' : 'no', rdShow: true }); },
      checkMn: (ev) => { if (ev && ev.preventDefault) ev.preventDefault(); if (!st.mnAns.trim()) return; const ok = meaningOk(e, st.mnAns); this.setState({ mnRes: ok ? 'ok' : 'no', mnShow: true }); },
      count: st.count, emptyHint: st.count === 0 && !r && !st.busy,
      guide: st.guide, ghost: st.ghost, guideP: st.guide ? 'true' : 'false', guideBg: g.bg, guideFg: g.fg, guideBd: g.bd, ghostP: st.ghost ? 'true' : 'false', ghostBg: h.bg, ghostFg: h.fg, ghostBd: h.bd,
      toggleGuide: () => this.setState({ guide: !st.guide }), toggleGhost: () => this.setState({ ghost: !st.ghost }),
      warnOn: st.warn > 0, shakeCls: st.warn > 0 ? (st.warn % 2 ? 'shakeA' : 'shakeB') : '',
      busy: st.busy,
      hasResult: !!r, noResult: !r,
      r: r || { img: '', sim: 0, user: 0, exp: 0 }, v: V, simW: (r ? r.sim : 0) + '%',
      vOk: !!r && r.verdict === 'ok', vAl: !!r && r.verdict === 'almost', vNo: !!r && r.verdict === 'no',
      rid: idE ? tOf(idE) : Object.assign({}, EMPTY_T, { c: '?', tl: 'Não identificado' }), hasRid: !!idE, noRid: !idE, sameRid: !!idE && idE === e,
      fin, finLabel: fin ? 'Acerto' : 'Erro', finFg: fin ? '#4E6E3A' : '#A8292A', finBg: fin ? '#E7EEDF' : '#F8E4E0',
      finWhy: st.over != null ? 'Você ajustou manualmente.' : (!r ? '' : r.verdict === 'no' ? 'O desenho não correspondeu.' : r.verdict === 'almost' ? 'Quase: confira a forma e o número de traços. Se achar que acertou, marque como acerto.' : st.rdRes === 'no' ? 'A leitura informada não confere.' : st.mnRes === 'no' ? 'O significado informado não confere.' : 'Desenho reconhecido' + (st.rdRes === 'ok' || st.mnRes === 'ok' ? ' e resposta certa.' : '.')),
      overs: [[true, 'Acerto'], [false, 'Erro']].map(([v, label]) => Object.assign({ label, pick: () => this.setState({ over: v }) }, segVals(fin === v))),
      isLast: st.i + 1 >= st.queue.length, nextLabel: st.i + 1 >= st.queue.length ? 'Ver resumo' : 'Próximo',
      upcoming: st.queue.slice(st.i + 1, st.i + 7).map((id) => ({ c: st.memory ? '·' : D._idx[id].char })), hasUpcoming: st.i + 1 < st.queue.length,
      saved: st.saved, unsaved: !st.saved,
      setCanvas: this.setCanvas, onDown: this.onDown, onMove: this.onMove, onUp: this.onUp,
      undo: () => { if (st.res || st.busy) return; this.strokes.pop(); Ink.redraw(this); this.setState({ count: this.strokes.length }); },
      clear: () => { this.wipe(); this.setState({ count: 0, res: null, over: null, warn: 0 }); },
      done: async () => {
        if (st.res || st.busy) return;
        if (!this.strokes.length) { this.setState({ warn: st.warn + 1 }); return; }
        this.setState({ busy: true });
        let res = null; try { res = await Rec.evaluate(this, D, e); } catch (err) { res = { id: null, verdict: 'no', sim: 0, user: this.strokes.length, exp: e.strokes, shapeOk: false, strokesOk: false, img: '' }; }
        this.setState({ res, busy: false, showChar: true });
      },
      next: () => this.next(),
      speak: () => say(e ? (e.category === 'kanji' ? (e.readings.kun[0] ? e.readings.kun[0].kana : e.readings.on[0].kana) : e.char) : ''),
      endSession: () => { this.wipe(); if (!st.done.length) this.setState({ view: 'setup', res: null, count: 0 }); else this.setState({ view: 'summary', res: null, count: 0 }); }
    };

    // ---------- resumo ----------
    const n = st.done.length, ok = st.done.filter((i) => i.ok).length, ms = st.done.reduce((a, i) => a + i.ms, 0);
    const wrong = uniq(st.done.filter((i) => !i.ok).map((i) => i.c));
    const summary = {
      sN: n, sOk: ok, sFail: n - ok, sRate: n ? Math.round(ok / n * 100) + '%' : '—', sTime: fmtDur(ms), sLabel: st.label,
      sHead: n ? (ok / n >= 0.8 ? 'Excelente sessão!' : ok / n >= 0.5 ? 'Bom trabalho!' : 'Continue praticando') : 'Sessão encerrada',
      results: st.done.map((i) => { const x = D._idx[i.c]; return { c: x ? x.char : '?', ok: !!i.ok, no: !i.ok, sub: x ? (x.category === 'kanji' ? x.meaning.pt[0] : x.romaji) : '', bd: i.ok ? '#CFE0C3' : '#F1C7C0', bg: i.ok ? '#F4F8F0' : '#FDF3F1' }; }),
      hasWrong: wrong.length > 0, wrongLabel: 'Praticar os ' + wrong.length + ' errados',
      retryWrong: () => this.startWith(shuffle(wrong), 'Revisão da sessão', { review: true }),
      again: () => this.startWith(shuffle(uniq(st.queue)), st.label, null),
      newSession: () => this.setState({ view: 'setup' }),
      barOk: n ? Math.round(ok / n * 100) + '%' : '0%'
    };
    return Object.assign(base, setup, session, summary, { cats, jlpts, lists: listCards });
  }
}
