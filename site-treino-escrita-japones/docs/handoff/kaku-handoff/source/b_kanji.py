from common import *
from b_listpick import list_picker
from b_chars import DBJS, DATA_HEAD, glyph_box, LBL, BACK_BTN
from b_comp import comp_section

from ui import CARD
S = comp_section(76, full=True)

def seg(lst, label):
    return ('<div role="group" aria-label="' + label + '" style="display:flex;gap:4px;padding:4px;background:#F2EEE6;border-radius:999px;">'
            '<sc-for list="{{' + lst + '}}" as="f" hint-placeholder-count="3"><button onClick="{{f.pick}}" aria-pressed="{{f.pressed}}" style="height:38px;padding:0 14px;border:none;border-radius:999px;background-color:{{f.bg}};color:{{f.fg}};font-weight:{{f.fw}};box-shadow:{{f.sh}};font-size:14px;cursor:pointer;transition:background-color .2s ease;">{{f.label}}</button></sc-for></div>')

SELECT = 'height:40px;padding:0 36px 0 14px;border-radius:12px;border:1px solid #E6E0D6;background:#FFFFFF;font-size:14px;color:#1F1C18;cursor:pointer;'

reading_rows = '''<div style="display:flex;flex-direction:column;gap:8px;">
<sc-if value="{{hasOn}}" hint-placeholder-val="{{true}}"><div style="display:flex;align-items:flex-start;gap:10px;"><span style="width:74px;flex-shrink:0;font-size:13px;color:#5E5850;padding-top:6px;">On'yomi</span><div style="display:flex;flex-wrap:wrap;gap:6px;"><sc-for list="{{onR}}" as="o" hint-placeholder-count="2"><span style="display:flex;align-items:baseline;gap:6px;padding:5px 10px;border-radius:10px;border:1px solid #E6E0D6;"><span class="jp" style="font-size:16px;">{{o.k}}</span><span style="font-size:13px;color:#726B61;">{{o.r}}</span></span></sc-for></div></div></sc-if>
<sc-if value="{{hasKun}}" hint-placeholder-val="{{true}}"><div style="display:flex;align-items:flex-start;gap:10px;"><span style="width:74px;flex-shrink:0;font-size:13px;color:#5E5850;padding-top:6px;">Kun'yomi</span><div style="display:flex;flex-wrap:wrap;gap:6px;"><sc-for list="{{kunR}}" as="o" hint-placeholder-count="2"><span style="display:flex;align-items:baseline;gap:6px;padding:5px 10px;border-radius:10px;border:1px solid #E6E0D6;"><span class="jp" style="font-size:16px;">{{o.k}}</span><span style="font-size:13px;color:#726B61;">{{o.r}}</span></span></sc-for></div></div></sc-if>
</div>'''

examples = '''<div style="''' + CARD + '''padding:20px;display:flex;flex-direction:column;gap:4px;">
<h3 style="''' + LBL + '''margin-bottom:6px;">Exemplos de palavras</h3>
<sc-for list="{{examples}}" as="x" hint-placeholder-count="3">
<div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-top:1px solid #EFEAE1;">
<span class="jp" style="font-size:22px;min-width:70px;">{{x.w}}</span>
<div style="display:flex;flex-direction:column;gap:2px;min-width:0;"><span style="font-size:13px;color:#5E5850;"><span class="jp">{{x.r}}</span> · {{x.ro}}</span><span style="font-size:14px;font-weight:500;">{{x.pt}} <span style="color:#726B61;font-weight:400;">· {{x.en}}</span></span></div>
</div>
</sc-for>
</div>'''

sentence_order = '''<div style="display:flex;flex-direction:column;gap:16px;">
<div style="''' + CARD + '''padding:20px;display:flex;flex-direction:column;gap:8px;">
<h3 style="''' + LBL + '''">Frase de exemplo</h3>
<sc-if value="{{hasSentence}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:8px;"><span class="jp" style="font-size:19px;line-height:1.5;">{{d.sja}}</span>
<span style="font-size:14px;line-height:1.45;">{{d.spt}}</span>
<span style="font-size:13px;line-height:1.45;color:#726B61;">{{d.sen}}</span></div></sc-if>
<sc-if value="{{noSentence}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;line-height:1.5;color:#5E5850;">Ficha essencial: a frase de exemplo deste kanji ainda será adicionada.</p></sc-if>
</div>
<div style="''' + CARD + '''padding:20px;display:flex;flex-direction:column;gap:12px;">
<h3 style="''' + LBL + '''">Ordem dos traços · {{d.n}}</h3>
<sc-if value="{{hasOrder}}" hint-placeholder-val="{{true}}">''' + frames('frames', 52) + '''</sc-if>
<sc-if value="{{noOrder}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;line-height:1.5;color:#5E5850;">Animação ainda não disponível para este kanji.</p></sc-if>
</div>
</div>'''

detail = '''<div style="display:flex;flex-direction:column;gap:22px;padding:4px 4px 40px;">
<div style="''' + CARD + '''padding:26px;display:flex;gap:26px;align-items:flex-start;">
<div style="width:236px;flex-shrink:0;">''' + glyph_box(200) + '''</div>
<div style="display:flex;flex-direction:column;gap:14px;flex-grow:1;min-width:0;">
''' + BACK_BTN + '''
<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
<span style="font-size:11px;font-weight:700;padding:4px 10px;border-radius:999px;background:#1F1C18;color:#FFFFFF;">{{d.jlpt}}</span>
<span style="font-size:13px;color:#5E5850;">{{metaLine}}</span>
<sc-if value="{{d.essential}}" hint-placeholder-val="{{false}}"><span title="Significados, leituras, radical, componentes e 1 exemplo. Frases e mais exemplos em expansão." style="font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;background:#F4EAD6;color:#7A5210;">Ficha essencial</span></sc-if>
</div>
<div style="display:flex;flex-direction:column;gap:2px;">
<span class="disp" style="font-size:32px;font-weight:700;line-height:1.2;">{{d.pt}}</span>
<span style="font-size:16px;color:#5E5850;">{{d.en}}</span>
</div>
''' + reading_rows + '''
<div style="display:flex;gap:8px;flex-wrap:wrap;">
<button class="btn soft" onClick="{{speak}}" style="height:40px;padding:0 14px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:14px;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('speaker', 18) + '''Ouvir</button>
<sc-if value="{{hasOrder}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{replay}}" style="height:40px;padding:0 14px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:14px;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('replay', 18) + '''Ver traços</button></sc-if>
<a href="Praticar.dc.html" onClick="{{practiceThis}}" class="btn" style="height:40px;padding:0 16px;border-radius:999px;background-color:''' + ACC + ''';color:#FFFFFF;font-size:14px;font-weight:700;text-decoration:none;display:flex;align-items:center;gap:6px;">''' + ic('brush', 18) + '''Praticar</a>
</div>
''' + list_picker(compact=True, show_practice=False) + '''
</div>
</div>

<div style="display:flex;flex-direction:column;gap:6px;">
<h2 class="disp" style="margin:0;font-size:28px;font-weight:700;">Componentes do Kanji</h2>
<p style="margin:0;font-size:14px;color:#5E5850;">Primeiro o que se vê (decomposição gráfica); depois, quando há informação confiável, como o kanji foi formado historicamente.</p>
</div>
''' + S['decomp'] + S['formation'] + '''
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:start;">
<div style="''' + CARD + '''padding:20px;display:flex;flex-direction:column;gap:14px;">''' + S['used'] + '''
<sc-if value="{{cx.usedMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{showAllUsed}}" style="align-self:flex-start;height:34px;padding:0 12px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;font-size:13px;cursor:pointer;">Ver todos na lista</button></sc-if>
<sc-if value="{{cx.hasUsed}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{filterBySelf}}" style="align-self:flex-start;height:34px;padding:0 12px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:13px;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('search', 14, 2) + '''Filtrar a lista por <span class="jp">{{d.c}}</span></button></sc-if>
</div>
<div style="''' + CARD + '''padding:20px;display:flex;flex-direction:column;gap:18px;">''' + S['rel'] + S['same'] + '''</div>
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:start;">''' + examples + sentence_order + '''</div>
</div>'''

body = '''<div style="width:1440px;height:1400px;box-sizing:border-box;background:#F7F4EE;display:flex;flex-direction:column;overflow:hidden;">
''' + nav('caracteres') + '''
<main style="display:flex;flex-direction:column;min-height:0;flex-grow:1;">
<section style="padding:28px 64px 18px;display:flex;flex-direction:column;gap:16px;">
<div style="display:flex;align-items:flex-end;justify-content:space-between;gap:24px;">
<div style="display:flex;flex-direction:column;gap:6px;">
<nav aria-label="Trilha" style="font-size:13px;color:#726B61;display:flex;gap:6px;align-items:center;"><a href="Caracteres.dc.html" style="text-decoration:none;">Caracteres</a><span aria-hidden="true">/</span><span>Kanji</span></nav>
<h1 class="disp" style="margin:0;font-size:42px;font-weight:700;">Kanji</h1>
<p style="margin:0;font-size:16px;color:#5E5850;">Veja como cada kanji é formado e navegue entre caracteres que compartilham componentes.</p>
</div>
<p role="status" style="margin:0;font-size:14px;color:#726B61;">Mostrando <strong style="color:#1F1C18;">{{shown}}</strong> de {{total}} kanji</p>
</div>
<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
<label style="position:relative;display:flex;align-items:center;width:380px;height:46px;">
<span style="position:absolute;left:14px;display:flex;color:#726B61;">''' + ic('search', 18) + '''</span>
<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Pesquisar kanji</span>
<input type="search" value="{{query}}" onChange="{{onQuery}}" placeholder="{{placeholder}}" style="width:100%;height:46px;box-sizing:border-box;padding:0 14px 0 42px;border:1px solid #E6E0D6;border-radius:14px;background:#FFFFFF;font-size:15px;color:#1F1C18;outline:none;">
</label>
''' + seg('modes', 'Tipo de busca') + '''
<span aria-hidden="true" style="width:1px;height:26px;background:#E0D9CD;"></span>
''' + seg('jlpts', 'Nível JLPT') + '''
</div>
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
<label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#5E5850;font-weight:700;">Radical
<select value="{{rad}}" onChange="{{onRad}}" style="''' + SELECT + '''"><sc-for list="{{radOpts}}" as="o" hint-placeholder-count="5"><option value="{{o.v}}">{{o.label}}</option></sc-for></select></label>
<label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#5E5850;font-weight:700;">Traços
<select value="{{strokes}}" onChange="{{onStrokes}}" style="''' + SELECT + '''"><sc-for list="{{strokeOpts}}" as="o" hint-placeholder-count="5"><option value="{{o.v}}">{{o.label}}</option></sc-for></select></label>
<sc-if value="{{hasComp}}" hint-placeholder-val="{{false}}"><span style="display:flex;align-items:center;gap:8px;height:40px;padding:0 6px 0 14px;border-radius:999px;background:#1F1C18;color:#FFFFFF;font-size:14px;">Componente <span class="jp" style="font-size:18px;">{{comp}}</span><button onClick="{{clearComp}}" aria-label="Remover filtro de componente" style="width:30px;height:30px;border-radius:999px;border:none;background:rgba(255,255,255,.15);color:#FFFFFF;cursor:pointer;display:flex;align-items:center;justify-content:center;">''' + ic('x', 14, 2.2) + '''</button></span></sc-if>
<sc-if value="{{anyFilter}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{clearFilters}}" style="height:36px;padding:0 12px;border:none;border-radius:999px;background:transparent;color:''' + ACC + ''';font-size:13px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('x', 14, 2) + '''Limpar filtros</button></sc-if>
</div>
<sc-if value="{{hasBanner}}" hint-placeholder-val="{{false}}">
<div class="rise" style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-radius:16px;background:#FFFFFF;border:1px solid #E6E0D6;">
<span class="jp" style="width:46px;height:46px;flex-shrink:0;border-radius:12px;background:#FBEDEA;display:flex;align-items:center;justify-content:center;font-size:28px;">{{banner.c}}</span>
<div style="display:flex;flex-direction:column;gap:2px;flex-grow:1;"><span style="font-size:15px;font-weight:700;">{{banner.title}}</span><span style="font-size:13px;color:#5E5850;">{{banner.sub}}</span></div>
</div>
</sc-if>
</section>
<div style="display:flex;gap:24px;padding:0 64px 28px;min-height:0;flex-grow:1;">
<div style="width:520px;flex-shrink:0;overflow-y:auto;scrollbar-width:thin;padding:4px 6px 24px 2px;">
<sc-if value="{{loading}}" hint-placeholder-val="{{false}}"><p style="margin:40px 0;text-align:center;color:#726B61;">Carregando kanji…</p></sc-if>
<sc-if value="{{empty}}" hint-placeholder-val="{{false}}"><div style="padding:48px 20px;border:1px dashed #D9D1C4;border-radius:20px;text-align:center;display:flex;flex-direction:column;gap:6px;"><p style="margin:0;font-size:16px;font-weight:500;">Nenhum kanji encontrado</p><p style="margin:0;font-size:14px;color:#726B61;">Tente outro componente, significado ou limpe os filtros.</p></div></sc-if>
<sc-for list="{{groups}}" as="g" hint-placeholder-count="2">
<div style="display:flex;flex-direction:column;gap:10px;margin-bottom:20px;">
<h2 style="margin:0;font-size:13px;font-weight:700;letter-spacing:.06em;color:#5E5850;display:flex;align-items:center;gap:8px;"><span style="padding:3px 9px;border-radius:999px;background:#1F1C18;color:#FFFFFF;">{{g.level}}</span>{{g.count}} kanji</h2>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;">
<sc-for list="{{g.items}}" as="it" hint-placeholder-count="10">
<button class="card" onClick="{{it.pick}}" aria-pressed="{{it.cur}}" aria-label="{{it.c}}, {{it.pt}}" style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 6px 8px;border-radius:14px;border:1px solid {{it.bd}};box-shadow:{{it.sh}};background:#FFFFFF;cursor:pointer;color:#1F1C18;min-width:0;">
<span class="jp" style="font-size:38px;line-height:1.1;">{{it.c}}</span>
<span style="font-size:11px;color:#5E5850;width:100%;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.pt}}</span>
</button>
</sc-for>
</div>
<sc-if value="{{g.hasMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{g.more}}" style="align-self:center;height:40px;padding:0 18px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:13px;font-weight:500;cursor:pointer;">{{g.moreLabel}}</button></sc-if>
</div>
</sc-for>
</div>
<div style="flex-grow:1;min-width:0;overflow-y:auto;scrollbar-width:thin;">
<sc-if value="{{ready}}" hint-placeholder-val="{{true}}">''' + detail + '''</sc-if>
</div>
</div>
</main>
</div>'''

script = acctify(DBJS + js('account.js') + r'''
const RANGES = { '': null, a: [1, 4], b: [5, 8], c: [9, 12], d: [13, 16], e: [17, 99] };
function cjkChar(q) { const a = Array.from(q); return a.length === 1 && /[⺀-鿿豈-﫿]|[\uD840-\uD87F][\uDC00-\uDFFF]/.test(q); }
function compMaps(D) {
  if (D._cm) return D._cm;
  const toStd = {}, toVar = {}, meaning = new Map(), search = new Map();
  D.characters.forEach((e) => {
    if (e.category !== 'kanji') return;
    meaning.set(e.char, e.meaning.pt.join(' / ')); search.set(e.char, e.meaning.pt.join(' ') + ' ' + e.meaning.en.join(' '));
    (e.decomposition || []).forEach((d) => {
      if (d.lookalike) return;
      if (!meaning.has(d.c)) { meaning.set(d.c, d.meaning || ''); search.set(d.c, d.meaning || ''); }
      if (d.standard) { toStd[d.c] = d.standard; (toVar[d.standard] = toVar[d.standard] || new Set()).add(d.c); }
    });
  });
  D._cm = { toStd, toVar, meaning, search };
  return D._cm;
}
function compSet(D, q) {
  const set = new Set(); q = (q || '').trim(); if (!q) return set;
  const M = compMaps(D);
  if (cjkChar(q)) { set.add(q); (M.toVar[q] || []).forEach((v) => set.add(v)); if (M.toStd[q]) set.add(M.toStd[q]); return set; }
  const nq = norm(q);
  M.search.forEach((m, c) => { if (norm(m).split(/[^a-z0-9]+/).some((w) => w && w.startsWith(nq))) set.add(c); });
  return set;
}
function hasComp(e, set) { return set.has(e.char) || e.containsComponents.some((c) => set.has(c)); }
function kanjiList(D, st) {
  let L = D.characters.filter((e) => e.category === 'kanji');
  if (st.jlpt) L = L.filter((e) => e.jlpt === st.jlpt);
  if (st.rad) L = L.filter((e) => e.radical.standard === st.rad);
  const R = RANGES[st.strokes || '']; if (R) L = L.filter((e) => e.strokes >= R[0] && e.strokes <= R[1]);
  if (st.comp) { const cs = compSet(D, st.comp); L = L.filter((e) => hasComp(e, cs)); }
  const q = norm(st.query).trim();
  if (q) {
    if (st.mode === 'meaning') L = L.filter((e) => norm(e.meaning.pt.join(' ') + ' ' + e.meaning.en.join(' ')).includes(q));
    else if (st.mode === 'comp') { const cs = compSet(D, st.query); L = L.filter((e) => hasComp(e, cs)); }
    else L = L.filter((e) => e._hay.includes(q) || e.char === st.query.trim());
  }
  return L;
}
class Component extends DCLogic {
  constructor(...a) {
    super(...a);
    this._page = 'Kanji.dc.html';
    this.state = { mode: 'all', query: '', jlpt: null, rad: '', strokes: '', comp: null, sel: 'kanji:明', anim: 0, hist: [] };
  }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
    const st = this.state;
    const D = kdb();
    const seg = (key, items) => items.map(([id, label]) => { const on = st[key] === id; return { label, pressed: on ? 'true' : 'false', bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F1C18' : '#5E5850', fw: on ? '700' : '500', sh: on ? '0 1px 3px rgba(31,28,24,.12)' : 'none', pick: () => this.setState({ [key]: id }) }; });
    const base = { accent, loading: !D, ready: false, groups: [], shown: 0, total: 0, radOpts: [], strokeOpts: [], query: st.query, rad: st.rad, strokes: st.strokes };
    if (!D) return Object.assign(base, { modes: [], jlpts: [], cx: EMPTY_CX });
    const K = D.characters.filter((e) => e.category === 'kanji');
    const list = kanjiList(D, st);
    const levels = ['N5', 'N4', 'N3', 'N2', 'N1'];
    const gkey = JSON.stringify([st.mode, st.query, st.jlpt, st.rad, st.strokes, st.comp]);
    if (!this._glim || this._glim.key !== gkey) this._glim = { key: gkey, n: {} };
    const groups = levels.map((lv) => {
      const all = list.filter((e) => e.jlpt === lv); const lim = this._glim.n[lv] || 60;
      const items = all.slice(0, lim).map((e) => {
        const on = e.id === st.sel;
        return { c: e.char, pt: e.meaning.pt[0], cur: on ? 'true' : 'false', bd: on ? accent : '#E6E0D6', sh: on ? '0 0 0 3px ' + accent + '2E' : 'none', pick: () => { if (e.id !== st.sel) this.setState({ sel: e.id, anim: st.anim + 1, mdetail: true, hist: (st.hist || []).concat([st.sel]).slice(-30) }); else this.setState({ mdetail: true }); } };
      });
      return { level: 'JLPT ' + lv, count: all.length, items, hasMore: all.length > lim, moreLabel: 'Mostrar mais ' + lv + ' (' + (all.length - lim) + ' restantes)', more: () => { this._glim.n[lv] = lim + 120; this.forceUpdate(); } };
    }).filter((g) => g.count > 0);
    const radCount = {};
    K.forEach((e) => { const r = e.radical; radCount[r.standard] = radCount[r.standard] || { n: 0, num: r.number, pt: r.meaning.pt }; radCount[r.standard].n++; });
    const radOpts = [{ v: '', label: 'Todos os radicais' }].concat(Object.keys(radCount).sort((a, b) => radCount[a].num - radCount[b].num).map((k) => ({ v: k, label: k + '  ' + radCount[k].pt + ' (' + radCount[k].n + ')' })));
    const strokeOpts = [['', 'Todos'], ['a', '1–4 traços'], ['b', '5–8 traços'], ['c', '9–12 traços'], ['d', '13–16 traços'], ['e', '17 ou mais']].map(([v, label]) => ({ v, label }));
    const e = D._idx[st.sel] || K[0];
    const onComp = (c) => this.setState({ comp: c, mode: 'all', query: '', mdetail: false });
    const det = Object.assign(detailOf(this, e, accent), listPickerVals(this, e.id, accent));
    det.cx = compOf(this, e, onComp);
    det.noSentence = !det.hasSentence;
    det.metaLine = [e.strokes + ' traços', DIFF_LABEL[e.difficulty], e.gradeLabel].filter(Boolean).join(' · ');
    // banner for component search
    const compQ = st.comp || (st.mode === 'comp' && st.query.trim()) || '';
    let banner = null;
    if (compQ) {
      const cs = compSet(D, compQ); const M = compMaps(D);
      const main = cjkChar(compQ) ? compQ : Array.from(cs)[0];
      const n = list.length;
      banner = cs.size ? { c: main || '？', title: cjkChar(compQ) ? 'Componente ' + compQ + (M.meaning.get(compQ) ? ' — ' + M.meaning.get(compQ) : '') : 'Componentes com “' + compQ + '”: ' + Array.from(cs).slice(0, 8).join(' '), sub: n + (n === 1 ? ' kanji contém' : ' kanji contêm') + ' este componente (incluindo formas de radical, como 亻 para 人 e 氵 para 水).' } : { c: '？', title: 'Nenhum componente encontrado', sub: 'Digite um caractere (ex.: 木) ou um significado (ex.: água).' };
    }
    return Object.assign(base, det, {
      ready: true, groups, shown: list.length, total: K.length, empty: list.length === 0, radOpts, strokeOpts,
      modes: seg('mode', [['all', 'Tudo'], ['meaning', 'Significado'], ['comp', 'Componente']]),
      jlpts: seg('jlpt', [[null, 'Todos'], ['N5', 'N5'], ['N4', 'N4'], ['N3', 'N3'], ['N2', 'N2'], ['N1', 'N1']]),
      placeholder: st.mode === 'comp' ? 'Componente: 木, 氵, água, pessoa…' : (st.mode === 'meaning' ? 'Significado: árvore, water, falar…' : 'Kanji, leitura, romaji ou significado'),
      onQuery: (ev) => this.setState({ query: ev.target.value }),
      onRad: (ev) => this.setState({ rad: ev.target.value }),
      onStrokes: (ev) => this.setState({ strokes: ev.target.value }),
      comp: st.comp || '', hasComp: !!st.comp, clearComp: () => this.setState({ comp: null }),
      filterBySelf: () => this.setState({ mdetail: false, comp: e.char, mode: 'all', query: '', jlpt: null, rad: '', strokes: '' }),
      showAllUsed: () => this.setState({ mdetail: false, comp: e.char, mode: 'all', query: '', jlpt: null, rad: '', strokes: '' }),
      anyFilter: !!(st.jlpt || st.rad || st.strokes || st.comp || st.query),
      clearFilters: () => this.setState({ mode: 'all', query: '', jlpt: null, rad: '', strokes: '', comp: null }),
      hasBanner: !!banner, banner: banner || { c: '', title: '', sub: '' },
      mOpen: !!st.mdetail, mList: !st.mdetail, mClose: () => this.setState({ mdetail: false })
    });
  }
}''')

if __name__ == '__main__':
    open('project/Kanji.dc.html', 'w').write(page('Kaku — Kanji', 'pt-BR', body, script, 1440, 1400, DATA_HEAD))
