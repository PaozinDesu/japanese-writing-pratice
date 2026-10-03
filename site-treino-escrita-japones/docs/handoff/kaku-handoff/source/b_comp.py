"""Bloco “Componentes do Kanji” + “Origem / formação” + relações (compartilhado)."""
from common import ic, ACC

from ui import OVERLINE as LBL

COMPJS = r'''
const FORM_STYLE = {
  kanji: { full: 'Kanji independente', short: 'Kanji', bg: '#F8E4E0', fg: '#A8292A' },
  radical: { full: 'Radical', short: 'Radical', bg: '#E3EAF2', fg: '#2E4C6E' },
  grafico: { full: 'Componente gráfico', short: 'Gráfico', bg: '#EFEAE1', fg: '#5E5850' }
};
function goTo(self, id) {
  if (!id || id === self.state.sel) return;
  self.setState({ sel: id, anim: self.state.anim + 1, hist: (self.state.hist || []).concat([self.state.sel]).slice(-30) });
}
function goBack(self) {
  const h = (self.state.hist || []).slice(); const prev = h.pop();
  if (prev) self.setState({ sel: prev, anim: self.state.anim + 1, hist: h });
}
const EMPTY_CX = { hasDecomp: false, noDecomp: false, eqItems: [], compRows: [], rad: {}, radVariant: false, hasFormation: false, noFormation: false, fParts: [], hasFParts: false, hasFNote: false, usedTiles: [], hasUsed: false, noUsed: false, relTiles: [], hasRel: false, sameRad: [], hasSameRad: false, usedMore: false };
function compOf(self, e, onComp) {
  const D = kdb(); const idx = D._idx;
  const act = (c, ref) => ref ? () => goTo(self, ref) : (onComp ? () => onComp(c) : null);
  const dec = e.decomposition || [];
  const eqItems = dec.map((d, i) => {
    const st = FORM_STYLE[d.form] || FORM_STYLE.grafico; const a = act(d.c, d.ref);
    return {
      c: d.c, badge: d.lookalike ? 'Parecido com ' + d.c : st.full, short: d.lookalike ? 'Parecido' : st.short, bg: st.bg, fg: st.fg,
      meaning: d.meaning || '—', plus: i > 0, pick: a || (() => {}), cursor: a ? 'pointer' : 'default', isLink: !!d.ref, isFilter: !d.ref && !!a,
      mainRad: d.c === e.radical.char, hint: d.ref ? 'Abrir ' + (d.standard || d.c) : (a ? 'Ver kanji com ' + d.c : '')
    };
  });
  const f = e.formation;
  const fParts = f ? f.parts.map((p, i) => {
    const a = act(p.c, p.ref); const sem = p.role === 'semantico';
    return { c: p.c, role: sem ? 'Semântico' : 'Fonético', reading: p.reading || '', hasReading: !!p.reading, bg: sem ? '#E7EEDF' : '#F4EAD6', fg: sem ? '#4E6E3A' : '#7A5210', meaning: p.meaning || '—', plus: i > 0, pick: a || (() => {}), cursor: a ? 'pointer' : 'default' };
  }) : [];
  const toTile = (ch) => { const o = idx['kanji:' + ch]; return { c: ch, pt: o ? o.meaning.pt[0] : '', jlpt: o ? o.jlpt : '', pick: () => goTo(self, 'kanji:' + ch) }; };
  const r = e.radical;
  const sameRad = D.characters.filter((o) => o.category === 'kanji' && o.id !== e.id && o.radical && o.radical.standard === r.standard).slice(0, 12).map((o) => toTile(o.char));
  const used = e.usedIn || [];
  return {
    hasDecomp: dec.length > 0, noDecomp: dec.length === 0, eqItems, compRows: eqItems, self: e.char,
    rad: { c: r.char, std: r.standard, num: r.number, pt: r.meaning.pt, name: r.name || '', pick: r.ref ? () => goTo(self, r.ref) : (() => {}), cursor: r.ref && r.ref !== e.id ? 'pointer' : 'default' },
    radVariant: r.char !== r.standard,
    hasFormation: !!f, noFormation: !f, fLabel: f ? f.label : '', fDesc: f ? f.description : '', fParts, hasFParts: fParts.length > 0,
    fNote: f && f.note ? f.note : '', hasFNote: !!(f && f.note),
    usedTiles: used.slice(0, 24).map(toTile), usedCount: used.length, hasUsed: used.length > 0, noUsed: used.length === 0, usedMore: used.length > 24,
    relTiles: (e.related || []).map(toTile), hasRel: (e.related || []).length > 0,
    sameRad, hasSameRad: sameRad.length > 0
  };
}
'''

def legend():
    item = lambda label, bg, fg: '<span style="display:flex;align-items:center;gap:6px;"><span style="width:10px;height:10px;border-radius:3px;background:%s;border:1.5px solid %s;"></span>%s</span>' % (bg, fg, label)
    return ('<div style="display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:#5E5850;">'
            + item('Kanji independente', '#F8E4E0', '#A8292A') + item('Radical', '#E3EAF2', '#2E4C6E') + item('Componente gráfico', '#EFEAE1', '#5E5850') + '</div>')

def tiles(lst, size=48, fs=26, with_meaning=False):
    inner = ('<span class="jp" style="font-size:%dpx;line-height:1;">{{k.c}}</span>' % fs)
    if with_meaning:
        inner += '<span style="font-size:10px;color:#726B61;max-width:%dpx;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{k.pt}}</span>' % (size + 8)
    return ('<div style="display:flex;flex-wrap:wrap;gap:8px;"><sc-for list="{{' + lst + '}}" as="k" hint-placeholder-count="6">'
            '<button class="btn soft" onClick="{{k.pick}}" aria-label="Abrir {{k.c}} ({{k.pt}})" title="{{k.pt}}" style="min-width:%dpx;height:%dpx;padding:4px 6px;box-sizing:border-box;border-radius:12px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;">' % (size, size + (16 if with_meaning else 0))
            + inner + '</button></sc-for></div>')

def comp_section(tile=72, full=True):
    fs = int(tile * 0.55)
    eq = ('''<div style="display:flex;align-items:flex-start;flex-wrap:wrap;gap:8px;">
<sc-for list="{{cx.eqItems}}" as="t" hint-placeholder-count="2">
<sc-if value="{{t.plus}}" hint-placeholder-val="{{false}}"><span aria-hidden="true" style="font-size:22px;color:#B5ADA2;height:%dpx;display:flex;align-items:center;">+</span></sc-if>
<button onClick="{{t.pick}}" title="{{t.hint}}" aria-label="{{t.c}}: {{t.badge}}, {{t.meaning}}" style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:0;border:none;background:transparent;cursor:{{t.cursor}};font-family:inherit;">
<span class="jp card" style="width:%dpx;height:%dpx;box-sizing:border-box;border-radius:14px;border:2px solid {{t.fg}};background:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:%dpx;color:#1F1C18;">{{t.c}}</span>
<span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:999px;background-color:{{t.bg}};color:{{t.fg}};">{{t.short}}</span>
</button>
</sc-for>
<span aria-hidden="true" style="font-size:22px;color:#B5ADA2;height:%dpx;display:flex;align-items:center;">→</span>
<div style="display:flex;flex-direction:column;align-items:center;gap:6px;"><span class="jp pop" style="width:%dpx;height:%dpx;box-sizing:border-box;border-radius:14px;background:#FBEDEA;border:2px solid ''' % (tile, tile, tile, fs, tile, tile, tile) + ACC + ''';display:flex;align-items:center;justify-content:center;font-size:%dpx;color:#1F1C18;">{{cx.self}}</span><span style="font-size:10px;font-weight:700;color:''' % fs + ACC + ''';">Resultado</span></div>
</div>''')

    rows = '''<div style="display:flex;flex-direction:column;">
<sc-for list="{{cx.compRows}}" as="t" hint-placeholder-count="2">
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-top:1px solid #EFEAE1;">
<span class="jp" style="width:40px;height:40px;flex-shrink:0;border-radius:10px;background-color:{{t.bg}};color:#1F1C18;display:flex;align-items:center;justify-content:center;font-size:24px;">{{t.c}}</span>
<div style="display:flex;flex-direction:column;gap:3px;flex-grow:1;min-width:0;">
<span style="font-size:15px;font-weight:500;">{{t.meaning}}</span>
<span style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;"><span style="font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;background-color:{{t.bg}};color:{{t.fg}};">{{t.badge}}</span><sc-if value="{{t.mainRad}}" hint-placeholder-val="{{false}}"><span style="font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;border:1px solid #2E4C6E;color:#2E4C6E;">Radical principal</span></sc-if></span>
</div>
<sc-if value="{{t.isLink}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{t.pick}}" style="flex-shrink:0;height:34px;padding:0 12px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:13px;cursor:pointer;display:flex;align-items:center;gap:4px;">Abrir''' + ic('arrow', 14, 2) + '''</button></sc-if>
<sc-if value="{{t.isFilter}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{t.pick}}" style="flex-shrink:0;height:34px;padding:0 12px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:13px;cursor:pointer;">Ver kanji com {{t.c}}</button></sc-if>
</div>
</sc-for>
</div>'''

    radical = '''<div style="display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:#EEF2F7;">
<button onClick="{{cx.rad.pick}}" aria-label="Radical {{cx.rad.c}}" class="jp" style="width:44px;height:44px;flex-shrink:0;border-radius:10px;border:2px solid #2E4C6E;background:#FFFFFF;color:#1F1C18;font-size:26px;cursor:{{cx.rad.cursor}};padding:0;">{{cx.rad.c}}</button>
<div style="display:flex;flex-direction:column;gap:2px;">
<span style="font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#2E4C6E;">Radical principal · nº {{cx.rad.num}}</span>
<span style="font-size:15px;font-weight:500;">{{cx.rad.pt}}<sc-if value="{{cx.radVariant}}" hint-placeholder-val="{{false}}"><span style="color:#5E5850;font-weight:400;"> — forma de <span class="jp">{{cx.rad.std}}</span> ({{cx.rad.name}})</span></sc-if></span>
</div>
</div>'''

    formation = '''<div style="display:flex;flex-direction:column;gap:12px;padding:18px;border-radius:16px;border:1px solid #E6E0D6;background:#FFFFFF;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;"><h3 style="''' + LBL + '''">Origem / formação do kanji</h3><span style="font-size:11px;color:#726B61;">histórico</span></div>
<sc-if value="{{cx.hasFormation}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;flex-direction:column;gap:4px;"><span style="font-size:16px;font-weight:700;">{{cx.fLabel}}</span><span style="font-size:13px;color:#5E5850;">{{cx.fDesc}}</span></div>
<sc-if value="{{cx.hasFParts}}" hint-placeholder-val="{{true}}"><div style="display:flex;align-items:flex-start;flex-wrap:wrap;gap:8px;">
<sc-for list="{{cx.fParts}}" as="p" hint-placeholder-count="2">
<sc-if value="{{p.plus}}" hint-placeholder-val="{{false}}"><span aria-hidden="true" style="font-size:20px;color:#B5ADA2;height:52px;display:flex;align-items:center;">+</span></sc-if>
<button onClick="{{p.pick}}" aria-label="{{p.c}}: {{p.role}}, {{p.meaning}}" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:0;border:none;background:transparent;cursor:{{p.cursor}};font-family:inherit;max-width:112px;">
<span class="jp" style="width:52px;height:52px;box-sizing:border-box;border-radius:12px;border:2px solid {{p.fg}};background:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:28px;color:#1F1C18;">{{p.c}}</span>
<span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:999px;background-color:{{p.bg}};color:{{p.fg}};">{{p.role}}<sc-if value="{{p.hasReading}}" hint-placeholder-val="{{false}}"> · <span class="jp">{{p.reading}}</span></sc-if></span>
<span style="font-size:11px;color:#5E5850;text-align:center;line-height:1.3;">{{p.meaning}}</span>
</button>
</sc-for>
</div></sc-if>
<sc-if value="{{cx.hasFNote}}" hint-placeholder-val="{{true}}"><p style="margin:0;font-size:14px;line-height:1.55;">{{cx.fNote}}</p></sc-if>
</div>
</sc-if>
<sc-if value="{{cx.noFormation}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;line-height:1.55;color:#5E5850;">Ainda não temos uma explicação histórica confiável para este kanji. A decomposição acima é apenas visual — ela não indica a origem.</p></sc-if>
<p style="margin:0;font-size:12px;line-height:1.5;color:#726B61;">Segue a classificação tradicional (象形, 指事, 会意, 形声). Não usamos mnemônicos modernos como origem.</p>
</div>'''

    decomp_block = '''<div style="display:flex;flex-direction:column;gap:14px;padding:18px;border-radius:16px;background:#FBF9F5;border:1px solid #EFEAE1;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;"><h3 style="''' + LBL + '''">Decomposição gráfica</h3><span style="font-size:11px;color:#726B61;">visual</span></div>
<sc-if value="{{cx.hasDecomp}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:14px;">''' + eq + legend() + rows + '''</div></sc-if>
<sc-if value="{{cx.noDecomp}}" hint-placeholder-val="{{false}}"><div style="display:flex;align-items:center;gap:14px;"><span class="jp" style="width:%dpx;height:%dpx;flex-shrink:0;border-radius:14px;background:#FFFFFF;border:2px solid #1F1C18;display:flex;align-items:center;justify-content:center;font-size:%dpx;">{{cx.self}}</span><p style="margin:0;font-size:14px;line-height:1.5;color:#5E5850;">Caractere básico: não se divide em partes com significado próprio. Ele mesmo funciona como componente de outros kanji.</p></div></sc-if>
''' % (tile, tile, fs) + radical + '''
</div>'''

    used = '''<div style="display:flex;flex-direction:column;gap:10px;">
<h3 style="''' + LBL + '''">Kanji que utilizam este componente <span style="color:#1F1C18;">({{cx.usedCount}})</span></h3>
<sc-if value="{{cx.hasUsed}}" hint-placeholder-val="{{true}}">''' + tiles('cx.usedTiles', 48, 26, full) + '''</sc-if>
<sc-if value="{{cx.noUsed}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;color:#5E5850;">Nenhum kanji da base usa este caractere como componente (ainda).</p></sc-if>
</div>'''
    rel = '''<sc-if value="{{cx.hasRel}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:10px;">
<h3 style="''' + LBL + '''">Kanji relacionados</h3>
''' + tiles('cx.relTiles', 48, 26, full) + '''
</div></sc-if>'''
    same = '''<sc-if value="{{cx.hasSameRad}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:10px;">
<h3 style="''' + LBL + '''">Mesmo radical <span class="jp" style="color:#1F1C18;">{{cx.rad.c}}</span></h3>
''' + tiles('cx.sameRad', 44, 24, False) + '''
</div></sc-if>'''
    return {'decomp': decomp_block, 'formation': formation, 'used': used, 'rel': rel, 'same': same}

def comp_block_compact(tile=60):
    s = comp_section(tile, full=False)
    return ('<div style="display:flex;flex-direction:column;gap:14px;"><h2 class="disp" style="margin:4px 0 0;font-size:22px;font-weight:700;">Componentes do Kanji</h2>'
            + s['decomp'] + s['formation'] + s['used'] + s['rel'] + '</div>')
