from common import *
from b_comp import COMPJS, comp_block_compact
from b_listpick import list_picker

from ui import OVERLINE as LBL
DATA_HEAD = '<script src="./data/kaku-data.js"></script>\n'
HELPERS = JSDATA[JSDATA.index('function nums'):]

DBJS = HELPERS + r'''
const KTYPES = { hiragana: { label: 'Hiragana', fg: '#2E4C6E', bg: '#E3EAF2' }, katakana: { label: 'Katakana', fg: '#7A5210', bg: '#F4EAD6' }, kanji: { label: 'Kanji', fg: '#A8292A', bg: '#F8E4E0' } };
const GROUP_LABEL = { basico: 'Básico', dakuten: 'Dakuten', handakuten: 'Handakuten', pequeno: 'Pequeno', combinacao: 'Combinação', estrangeiro: 'Som estrangeiro', joyo: 'Jōyō' };
const DIFF_LABEL = { iniciante: 'Iniciante', intermediario: 'Intermediário', avancado: 'Avançado' };
function hydrate(D) {
  if (!D.compact || D._hydrated) return;
  const USAGE = { N5: [5, 'muito alto'], N4: [4, 'alto'], N3: [3, 'médio'], N2: [2, 'moderado'], N1: [1, 'baixo'] };
  const DIFF = { N5: 'iniciante', N4: 'iniciante', N3: 'intermediario', N2: 'avancado', N1: 'avancado' };
  const comp = (k) => {
    const i = k.lastIndexOf('|'); const c = k.slice(0, i), f = k.slice(i + 1);
    if (f === '!') return { c, form: 'grafico', lookalike: true, meaning: 'forma parecida com ' + c + ', mas com outra origem', ref: null };
    const v = D.comps[k] || [f, '', null, null]; const o = { c, form: v[0], meaning: v[1], ref: v[2] };
    if (v[3]) o.standard = v[3];
    return o;
  };
  D.characters = D.characters.map((z) => {
    if (z.char) { z.examples = z.examples || []; z.jlpt = z.jlpt || null; z.strokeOrder = z.strokeOrder || null; return z; }
    const on = z.on.map((k, i) => ({ kana: k, romaji: z.rj[i] }));
    const kun = z.kun.map((k, i) => { const p = k.split('.'); const st = p[0], ok = p[1] || ''; return { kana: st + ok, display: st + (ok ? '(' + ok + ')' : ''), okurigana: ok || null, romaji: z.rj[z.on.length + i] }; });
    const prim = kun[0]; const rad = D.rads[z.r[1]] || [0, '', ''];
    const f = z.f ? { type: z.f[0], label: D.ftypes[z.f[0]][0], description: D.ftypes[z.f[0]][1], note: z.f[1] || null,
      parts: z.f[2].map((q) => { const cc = comp(q[0]); const p = { c: cc.c, role: q[1] === 's' ? 'semantico' : 'fonetico', meaning: cc.meaning, ref: cc.ref, form: cc.form }; if (q[2]) p.reading = q[2]; return p; }) } : null;
    return {
      id: 'kanji:' + z.c, char: z.c, category: 'kanji', group: 'joyo', romaji: prim ? prim.romaji : on[0].romaji, reading: prim ? prim.display : on[0].kana,
      meaning: { pt: z.pt, en: z.en }, jlpt: z.j, difficulty: DIFF[z.j], strokes: z.n,
      strokeOrder: z.so ? { source: 'kaku-simplificado', viewBox: '0 0 100 100', paths: z.so } : null,
      examples: z.ex.map((x) => ({ word: x[0], reading: x[1], romaji: x[2], pt: x[3], en: x[4] })),
      readings: { on, kun }, readingsRomaji: z.rj, grade: z.g || 0,
      gradeLabel: z.g ? (z.g <= 6 ? z.g + 'º ano (primário)' : 'ensino secundário') : '',
      usage: { level: USAGE[z.j][0], label: USAGE[z.j][1] }, sentence: z.s ? { ja: z.s[0], pt: z.s[1], en: z.s[2] } : null,
      detail: z.s ? 'completo' : 'essencial',
      radical: { char: z.r[0], standard: z.r[1], number: rad[0], meaning: { pt: rad[1], en: rad[2] }, name: z.r[2] || null, ref: null },
      decomposition: z.d.map(comp), formation: f, containsComponents: z.cc, usedIn: z.u, related: z.rel
    };
  });
  D._hydrated = true;
}
function kdb() {
  const D = window.KAKU_DATA;
  if (!D) return null;
  hydrate(D);
  if (!D._idx) {
    D._idx = {};
    D.characters.forEach((e) => {
      D._idx[e.id] = e;
      const r = e.readings ? e.readings.on.map((o) => o.kana).concat(e.readings.kun.map((k) => k.kana)).join(' ') : '';
      e._hay = norm([e.char, e.reading, e.romaji, (e.readingsRomaji || []).join(' '), r, e.meaning.pt.join(' '), e.meaning.en.join(' ')].join(' '));
    });
    D.characters.forEach((e) => { if (e.radical && !e.radical.ref && D._idx['kanji:' + e.radical.standard]) e.radical.ref = 'kanji:' + e.radical.standard; });
  }
  return D;
}
function waitForData(self) { if (kdb()) return; let n = 0; const t = setInterval(() => { n++; if (kdb() || n > 60) { clearInterval(t); self.forceUpdate(); } }, 150); }
function cardOf(e, accent, selId, pick) {
  const T = KTYPES[e.category], on = e.id === selId, two = Array.from(e.char).length > 1;
  return {
    id: e.id, c: e.char, tl: T.label, tf: T.fg, tb: T.bg, n: e.strokes, jlpt: e.jlpt || '', hasJlpt: !!e.jlpt,
    sub: e.category === 'kanji' ? e.reading + ' · ' + e.romaji : e.romaji, subJp: e.category === 'kanji',
    pt: e.meaning.pt.join('; '), en: e.meaning.en.join('; '), gs: two ? '46px' : '64px',
    cur: on ? 'true' : 'false', bd: on ? accent : '#E6E0D6', sh: on ? '0 0 0 3px ' + accent + '2E' : 'none', pick
  };
}
function detailOf(self, e, accent) {
  const T = KTYPES[e.category], isKanji = e.category === 'kanji', two = Array.from(e.char).length > 1;
  const order = e.strokeOrder ? e.strokeOrder.paths : null;
  return {
    d: {
      c: e.char, tl: T.label, tf: T.fg, tb: T.bg, n: e.strokes, jlpt: e.jlpt || '—', group: GROUP_LABEL[e.group] || e.group,
      diff: DIFF_LABEL[e.difficulty], r: e.reading, ro: e.romaji, pt: e.meaning.pt.join('; '), en: e.meaning.en.join('; '),
      note: e.note || '', grade: e.gradeLabel || '—', essential: e.detail === 'essencial', usage: e.usage ? e.usage.label : '', gs: two ? '104px' : '150px',
      sja: e.sentence ? e.sentence.ja : '', spt: e.sentence ? e.sentence.pt : '', sen: e.sentence ? e.sentence.en : ''
    },
    hasJlpt: !!e.jlpt, hasOrder: !!order, noOrder: !order, isKanji, isKana: !isKanji,
    hasNote: !!e.note, hasExamples: e.examples.length > 0, hasSentence: !!e.sentence,
    strokes: order ? order.map((p, i) => ({ d: p, len: plen(p), delay: (i * 0.7).toFixed(2) + 's' })) : [],
    frames: order ? order.map((_, i) => { const s = startPt(order[i]); return { n: i + 1, sx: s.x, sy: s.y, layers: order.map((p, j) => ({ d: p, c: j < i ? '#1F1C18' : (j === i ? accent : '#E6E0D6') })) }; }) : [],
    animA: self.state.anim % 2 === 0, animB: self.state.anim % 2 === 1,
    onR: isKanji ? e.readings.on.map((o) => ({ k: o.kana, r: o.romaji })) : [],
    kunR: isKanji ? e.readings.kun.map((k) => ({ k: k.display, r: k.romaji })) : [],
    hasOn: isKanji && e.readings.on.length > 0, hasKun: isKanji && e.readings.kun.length > 0,
    examples: e.examples.map((x) => ({ w: x.word, r: x.reading === x.word ? '' : x.reading, ro: x.romaji, pt: x.pt, en: x.en })),
    cx: isKanji && e.radical ? compOf(self, e, null) : EMPTY_CX, hasHist: (self.state.hist || []).length > 0, back: () => goBack(self),
    replay: () => self.setState({ anim: self.state.anim + 1 }),
    speak: () => say(isKanji ? (e.readings.kun[0] ? e.readings.kun[0].kana : e.readings.on[0].kana) : e.char)
  };
}
''' + COMPJS

def chip(bg='#FFFFFF', fg='#1F1C18'):
    return 'font-size:11px;font-weight:700;letter-spacing:.04em;padding:4px 9px;border-radius:999px;'

def glyph_box(size):
    return ('''<div style="display:flex;justify-content:center;padding:18px 0;background:#FBF9F5;border-radius:18px;border:1px solid #EFEAE1;">
<sc-if value="{{hasOrder}}" hint-placeholder-val="{{true}}">''' + anim_pair(size) + '''</sc-if>
<sc-if value="{{noOrder}}" hint-placeholder-val="{{false}}"><div style="position:relative;width:%dpx;height:%dpx;display:flex;align-items:center;justify-content:center;">''' % (size, size) + grid_svg(size) + '''<span class="jp fade" style="position:relative;font-size:{{d.gs}};line-height:1;">{{d.c}}</span></div></sc-if>
</div>''')

def info_cell(label, val):
    return '<div style="padding:12px 14px;border-radius:12px;background:#F7F4EE;display:flex;flex-direction:column;gap:2px;"><span style="font-size:11px;color:#726B61;font-weight:700;letter-spacing:.06em;text-transform:uppercase;">' + label + '</span><span style="font-size:15px;font-weight:500;">' + val + '</span></div>'

BACK_BTN = '''<sc-if value="{{hasHist}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{back}}" style="align-self:flex-start;height:34px;padding:0 12px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:13px;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('back', 16, 2) + '''Voltar</button></sc-if>'''

def detail_block(glyph_size=220, compact=False):
    return BACK_BTN + glyph_box(glyph_size) + '''
<div style="display:flex;align-items:baseline;justify-content:center;gap:12px;">
<span class="jp" style="font-size:28px;font-weight:600;">{{d.r}}</span>
<span style="font-size:18px;color:#5E5850;">{{d.ro}}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;">
<div style="padding:14px 16px;border-radius:14px;background:#F7F4EE;display:flex;flex-direction:column;gap:4px;"><span style="''' + LBL + '''font-size:11px;">Português</span><span style="font-size:16px;font-weight:500;line-height:1.35;">{{d.pt}}</span></div>
<div style="padding:14px 16px;border-radius:14px;background:#F7F4EE;display:flex;flex-direction:column;gap:4px;"><span style="''' + LBL + '''font-size:11px;">Inglês</span><span style="font-size:16px;font-weight:500;line-height:1.35;">{{d.en}}</span></div>
</div>
<sc-if value="{{isKanji}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:12px;">
<h3 style="''' + LBL + '''">Leituras</h3>
<sc-if value="{{hasOn}}" hint-placeholder-val="{{true}}"><div style="display:flex;align-items:flex-start;gap:12px;"><span style="width:78px;flex-shrink:0;font-size:14px;color:#5E5850;padding-top:7px;">On'yomi</span><div style="display:flex;flex-wrap:wrap;gap:8px;"><sc-for list="{{onR}}" as="o" hint-placeholder-count="2"><span style="display:flex;align-items:baseline;gap:6px;padding:6px 11px;border-radius:10px;border:1px solid #E6E0D6;"><span class="jp" style="font-size:16px;">{{o.k}}</span><span style="font-size:13px;color:#726B61;">{{o.r}}</span></span></sc-for></div></div></sc-if>
<sc-if value="{{hasKun}}" hint-placeholder-val="{{true}}"><div style="display:flex;align-items:flex-start;gap:12px;"><span style="width:78px;flex-shrink:0;font-size:14px;color:#5E5850;padding-top:7px;">Kun'yomi</span><div style="display:flex;flex-wrap:wrap;gap:8px;"><sc-for list="{{kunR}}" as="o" hint-placeholder-count="2"><span style="display:flex;align-items:baseline;gap:6px;padding:6px 11px;border-radius:10px;border:1px solid #E6E0D6;"><span class="jp" style="font-size:16px;">{{o.k}}</span><span style="font-size:13px;color:#726B61;">{{o.r}}</span></span></sc-for></div></div></sc-if>
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;">
''' + info_cell('Traços', '{{d.n}}') + info_cell('JLPT (aprox.)', '{{d.jlpt}}') + info_cell('Série escolar', '{{d.grade}}') + info_cell('Nível de uso', '{{d.usage}}') + '''
</div>
''' + comp_block_compact(56 if compact else 60) + '''
<a href="Kanji.dc.html" style="display:flex;align-items:center;gap:6px;font-size:14px;font-weight:700;text-decoration:none;">Explorar kanji por componentes''' + ic('arrow', 16, 2) + '''</a>
</sc-if>
<sc-if value="{{isKana}}" hint-placeholder-val="{{false}}">
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;">
''' + info_cell('Traços', '{{d.n}}') + info_cell('Tipo', '{{d.group}}') + info_cell('Nível', '{{d.diff}}') + '''
</div>
</sc-if>
<sc-if value="{{hasNote}}" hint-placeholder-val="{{false}}">
<div style="display:flex;gap:10px;align-items:flex-start;padding:14px 16px;border-radius:14px;background:#FBEDEA;">
<span style="display:flex;color:''' + ACC + ''';">''' + ic('bulb', 20) + '''</span>
<span style="font-size:14px;line-height:1.5;">{{d.note}}</span>
</div>
</sc-if>
<sc-if value="{{hasExamples}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:4px;">
<h3 style="''' + LBL + '''margin-bottom:6px;">Exemplos</h3>
<sc-for list="{{examples}}" as="x" hint-placeholder-count="3">
<div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-top:1px solid #EFEAE1;">
<span class="jp" style="font-size:22px;min-width:64px;">{{x.w}}</span>
<div style="display:flex;flex-direction:column;gap:2px;min-width:0;"><span style="font-size:13px;color:#5E5850;"><span class="jp">{{x.r}}</span> {{x.ro}}</span><span style="font-size:14px;font-weight:500;">{{x.pt}} <span style="color:#726B61;font-weight:400;">· {{x.en}}</span></span></div>
</div>
</sc-for>
</div>
</sc-if>
<sc-if value="{{hasSentence}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:8px;padding:16px 18px;border-radius:14px;border:1px solid #E6E0D6;">
<h3 style="''' + LBL + '''">Frase</h3>
<span class="jp" style="font-size:18px;line-height:1.5;">{{d.sja}}</span>
<span style="font-size:14px;line-height:1.45;">{{d.spt}}</span>
<span style="font-size:13px;line-height:1.45;color:#726B61;">{{d.sen}}</span>
</div>
</sc-if>
<div style="display:flex;flex-direction:column;gap:12px;">
<h3 style="''' + LBL + '''">Ordem dos traços</h3>
<sc-if value="{{hasOrder}}" hint-placeholder-val="{{true}}">''' + frames('frames', 56 if compact else 60) + '''</sc-if>
<sc-if value="{{noOrder}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;line-height:1.5;color:#5E5850;">Animação ainda não disponível para este caractere ({{d.n}} traços).</p></sc-if>
</div>
'''

# kept for DetalheMobile
DETAIL_JS = r'''
    const DD = kdb();
    const e = DD ? (DD._idx[this.state.sel] || DD.characters[0]) : null;
    const detail = e ? Object.assign({ ready: true, loading: false }, detailOf(this, e, accent), listPickerVals(this, e.id, accent)) : { ready: false, loading: true, al: { lists: [] } };
'''

PILL = 'height:40px;padding:0 16px;border-radius:999px;border:1px solid {{%s.bd}};background-color:{{%s.bg}};color:{{%s.fg}};font-size:14px;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:6px;'

def pill_group(lst, label, var='p'):
    return ('<div role="group" aria-label="' + label + '" style="display:flex;gap:6px;align-items:center;">'
            '<span style="font-size:13px;color:#726B61;font-weight:700;margin-right:4px;">' + label + '</span>'
            '<sc-for list="{{' + lst + '}}" as="' + var + '" hint-placeholder-count="3"><button class="btn" onClick="{{' + var + '.pick}}" aria-pressed="{{' + var + '.pressed}}" style="' + (PILL.replace('%s', var)).replace('height:40px', 'height:36px').replace('padding:0 16px', 'padding:0 12px').replace('font-size:14px', 'font-size:13px') + '">{{' + var + '.label}}</button></sc-for></div>')

body = '''<div style="width:1440px;height:1180px;box-sizing:border-box;background:#F7F4EE;display:flex;flex-direction:column;overflow:hidden;">
''' + nav('caracteres') + '''
<main style="display:flex;flex-direction:column;min-height:0;flex-grow:1;">
<section style="padding:36px 64px 20px;display:flex;flex-direction:column;gap:18px;">
<div style="display:flex;align-items:flex-end;justify-content:space-between;gap:24px;">
<div style="display:flex;flex-direction:column;gap:6px;">
<h1 class="disp" style="margin:0;font-size:44px;font-weight:700;letter-spacing:.01em;">Caracteres</h1>
<p style="margin:0;font-size:16px;color:#5E5850;">Hiragana, katakana e kanji em um só lugar — pesquise, filtre e estude cada caractere.</p>
</div>
<div style="display:flex;align-items:center;gap:18px;"><a href="Kanji.dc.html" class="btn soft" style="height:40px;padding:0 14px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;gap:8px;text-decoration:none;font-size:14px;font-weight:500;"><span class="jp" style="font-size:18px;color:''' + ACC + ''';">字</span>Explorar kanji por componentes''' + ic('arrow', 16, 2) + '''</a><p role="status" style="margin:0;font-size:14px;color:#726B61;">Mostrando <strong style="color:#1F1C18;">{{shown}}</strong> de {{total}}</p></div>
</div>
<div style="display:flex;align-items:center;gap:16px;">
<label style="position:relative;display:flex;align-items:center;width:440px;height:50px;flex-shrink:0;">
<span style="position:absolute;left:16px;display:flex;color:#726B61;">''' + ic('search', 20) + '''</span>
<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Pesquisar caracteres</span>
<input type="search" value="{{query}}" onChange="{{onQuery}}" placeholder="Caractere, romaji, leitura ou significado" style="width:100%;height:50px;box-sizing:border-box;padding:0 16px 0 48px;border:1px solid #E6E0D6;border-radius:14px;background:#FFFFFF;font-size:15px;color:#1F1C18;outline:none;">
</label>
<div role="group" aria-label="Categoria" style="display:flex;gap:4px;padding:4px;background:#F2EEE6;border-radius:999px;">
<sc-for list="{{cats}}" as="f" hint-placeholder-count="4"><button onClick="{{f.pick}}" aria-pressed="{{f.pressed}}" style="height:40px;padding:0 16px;border:none;border-radius:999px;background-color:{{f.bg}};color:{{f.fg}};font-weight:{{f.fw}};box-shadow:{{f.sh}};font-size:14px;cursor:pointer;display:flex;align-items:center;gap:8px;transition:background-color .2s ease;">{{f.label}}<span style="font-size:12px;opacity:.7;">{{f.count}}</span></button></sc-for>
</div>
</div>
<div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;min-height:36px;">
''' + pill_group('jlpts', 'JLPT') + '''
<span aria-hidden="true" style="width:1px;height:24px;background:#E0D9CD;"></span>
''' + pill_group('diffs', 'Nível') + '''
<sc-if value="{{showGroups}}" hint-placeholder-val="{{false}}"><span aria-hidden="true" style="width:1px;height:24px;background:#E0D9CD;"></span>''' + pill_group('groups', 'Tipo') + '''</sc-if>
<sc-if value="{{anyFilter}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{clearFilters}}" style="height:36px;padding:0 12px;border:none;border-radius:999px;background:transparent;color:''' + ACC + ''';font-size:13px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('x', 16, 2) + '''Limpar filtros</button></sc-if>
</div>
</section>
<div style="display:flex;gap:28px;padding:0 64px 32px;min-height:0;flex-grow:1;">
<div style="flex-grow:1;min-width:0;overflow-y:auto;scrollbar-width:thin;padding:4px 8px 24px 4px;">
<sc-if value="{{loading}}" hint-placeholder-val="{{false}}"><p style="margin:40px 0;text-align:center;color:#726B61;">Carregando caracteres…</p></sc-if>
<sc-if value="{{empty}}" hint-placeholder-val="{{false}}">
<div style="padding:64px 24px;border:1px dashed #D9D1C4;border-radius:20px;text-align:center;display:flex;flex-direction:column;gap:8px;align-items:center;">
<span class="jp" style="font-size:48px;color:#B5ADA2;">？</span>
<p style="margin:0;font-size:16px;font-weight:500;">Nenhum caractere encontrado</p>
<p style="margin:0;font-size:14px;color:#726B61;">Tente outro termo ou limpe os filtros.</p>
</div>
</sc-if>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;">
<sc-for list="{{cards}}" as="it" hint-placeholder-count="15">
<button class="card" onClick="{{it.pick}}" aria-pressed="{{it.cur}}" style="display:flex;flex-direction:column;gap:8px;padding:14px;border-radius:18px;border:1px solid {{it.bd}};box-shadow:{{it.sh}};background:#FFFFFF;cursor:pointer;text-align:left;color:#1F1C18;min-width:0;">
<span style="display:flex;justify-content:space-between;align-items:center;width:100%;gap:6px;">
<span style="font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:4px 8px;border-radius:999px;background-color:{{it.tb}};color:{{it.tf}};">{{it.tl}}</span>
<sc-if value="{{it.hasJlpt}}" hint-placeholder-val="{{false}}"><span style="font-size:11px;font-weight:700;color:#5E5850;border:1px solid #E6E0D6;padding:2px 7px;border-radius:999px;">{{it.jlpt}}</span></sc-if>
</span>
<span class="jp" style="height:76px;display:flex;align-items:center;justify-content:center;font-size:{{it.gs}};line-height:1;width:100%;">{{it.c}}</span>
<span style="text-align:center;width:100%;font-size:14px;color:#5E5850;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.sub}}</span>
<span style="border-top:1px solid #EFEAE1;padding-top:8px;display:flex;flex-direction:column;gap:1px;width:100%;min-width:0;">
<span style="font-size:14px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.pt}}</span>
<span style="font-size:12px;color:#726B61;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.en}}</span>
</span>
</button>
</sc-for>
</div>
<sc-if value="{{hasMore}}" hint-placeholder-val="{{false}}"><div style="display:flex;justify-content:center;padding:20px 0 8px;"><button class="btn soft" onClick="{{loadMore}}" style="height:44px;padding:0 20px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:14px;font-weight:500;cursor:pointer;">{{moreLabel}}</button></div></sc-if>
</div>
<aside aria-label="Detalhes do caractere" style="width:420px;flex-shrink:0;box-sizing:border-box;background:#FFFFFF;border:1px solid #E6E0D6;border-radius:24px;overflow-y:auto;scrollbar-width:thin;">
<sc-if value="{{ready}}" hint-placeholder-val="{{true}}">
<div style="padding:24px 26px 28px;display:flex;flex-direction:column;gap:20px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
<span style="font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:4px 10px;border-radius:999px;background-color:{{d.tb}};color:{{d.tf}};">{{d.tl}}</span>
<sc-if value="{{hasJlpt}}" hint-placeholder-val="{{true}}"><span style="font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;border:1px solid #E6E0D6;">{{d.jlpt}}</span></sc-if>
<span style="font-size:13px;color:#726B61;">{{d.diff}}</span>
</div>
<div style="display:flex;gap:8px;">
<sc-if value="{{hasOrder}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{replay}}" aria-label="Repetir animação da escrita" style="width:44px;height:44px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('replay', 20) + '''</button></sc-if>
<button class="btn soft" onClick="{{speak}}" aria-label="Ouvir pronúncia" style="width:44px;height:44px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('speaker', 20) + '''</button>
</div>
</div>
''' + detail_block(220) + '''
''' + list_picker() + '''
</div>
</sc-if>
</aside>
</div>
</main>
</div>'''

FILTER_JS = r'''
function filterList(D, st) {
  const q = norm(st.query).trim();
  return D.characters.filter((e) =>
    (st.cat === 'todos' || e.category === st.cat) && (!st.jlpt || e.jlpt === st.jlpt) &&
    (!st.diff || e.difficulty === st.diff) && (!st.group || e.group === st.group) && (!q || e._hay.includes(q)));
}
function toggleList(self, key, items, labels) {
  const cur = self.state[key];
  return items.map((id, i) => {
    const on = cur === id;
    return { label: labels[i], pressed: on ? 'true' : 'false', bg: on ? '#1F1C18' : '#FFFFFF', fg: on ? '#FFFFFF' : '#5E5850', bd: on ? '#1F1C18' : '#E6E0D6', pick: () => self.setState({ [key]: on ? null : id }) };
  });
}
function catList(self, D) {
  const st = self.state;
  return [['todos', 'Todos'], ['hiragana', 'Hiragana'], ['katakana', 'Katakana'], ['kanji', 'Kanji']].map(([id, label]) => {
    const on = st.cat === id;
    const count = D ? filterList(D, Object.assign({}, st, { cat: id, group: null })).length : 0;
    return { label, count, pressed: on ? 'true' : 'false', bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F1C18' : '#5E5850', fw: on ? '700' : '500', sh: on ? '0 1px 3px rgba(31,28,24,.12)' : 'none', pick: () => self.setState({ cat: id, group: null }) };
  });
}
'''

script = acctify(DBJS + js('account.js') + FILTER_JS + r'''
class Component extends DCLogic {
  constructor(...a) {
    super(...a);
    this._page = 'Caracteres.dc.html';
    this.state = { cat: 'todos', jlpt: null, diff: null, group: null, query: '', sel: 'kanji:日', anim: 0 };
  }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
    const st = this.state;
    const D = kdb();
    const list = D ? filterList(D, st) : [];
    const key = JSON.stringify([st.cat, st.jlpt, st.diff, st.group, st.query]);
    const lim = this._lim && this._lim.key === key ? this._lim.n : 60;
    const cards = list.slice(0, lim).map((e) => cardOf(e, accent, st.sel, () => this.setState({ sel: e.id, anim: st.anim + 1 })));
    const kanaCat = st.cat === 'hiragana' || st.cat === 'katakana';
    const gIds = st.cat === 'katakana' ? ['basico', 'dakuten', 'handakuten', 'pequeno', 'combinacao', 'estrangeiro'] : ['basico', 'dakuten', 'handakuten', 'pequeno', 'combinacao'];
    const gLabels = st.cat === 'katakana' ? ['Básicos', 'Dakuten', 'Handakuten', 'Pequenos', 'Combinações', 'Estrangeiros'] : ['Básicos', 'Dakuten', 'Handakuten', 'Pequenos', 'Combinações'];
''' + DETAIL_JS + r'''
    return Object.assign({
      accent, query: st.query, cards, shown: list.length, total: D ? D.characters.length : 0,
      hasMore: list.length > lim, moreLabel: 'Mostrar mais (' + (list.length - lim) + ' restantes)', loadMore: () => { this._lim = { key, n: lim + 60 }; this.forceUpdate(); },
      empty: !!D && cards.length === 0, loading: !D,
      cats: catList(this, D),
      jlpts: toggleList(this, 'jlpt', ['N5', 'N4', 'N3', 'N2', 'N1'], ['N5', 'N4', 'N3', 'N2', 'N1']),
      diffs: toggleList(this, 'diff', ['iniciante', 'intermediario', 'avancado'], ['Iniciante', 'Intermediário', 'Avançado']),
      groups: toggleList(this, 'group', gIds, gLabels), showGroups: kanaCat,
      anyFilter: !!(st.jlpt || st.diff || st.group || st.query || st.cat !== 'todos'),
      clearFilters: () => this.setState({ cat: 'todos', jlpt: null, diff: null, group: null, query: '' }),
      onQuery: (ev) => this.setState({ query: ev.target.value })
    }, detail);
  }
}''')

if __name__ == '__main__':
    open('project/Caracteres.dc.html', 'w').write(page('Kaku — Caracteres', 'pt-BR', body, script, 1440, 1180, DATA_HEAD))
