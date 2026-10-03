from common import *
from b_chars import detail_block, DETAIL_JS
from b_listpick import list_picker
from b_mobile_common import mheader

MROOT = 'width:390px;height:844px;box-sizing:border-box;background:#F7F4EE;position:relative;overflow:hidden;'
STREAK = None

# ---------- Caracteres (mobile) ----------
from b_chars import DBJS, FILTER_JS, DATA_HEAD

MCHIP = 'flex-shrink:0;height:34px;padding:0 12px;border-radius:999px;border:1px solid {{%s.bd}};background-color:{{%s.bg}};color:{{%s.fg}};font-size:13px;font-weight:500;cursor:pointer;'
body_c = '<div style="' + MROOT + '">\n' + mheader('Caracteres') + '''
<div style="display:flex;flex-direction:column;gap:10px;padding:0 24px;">
<label style="position:relative;display:flex;align-items:center;height:48px;">
<span style="position:absolute;left:14px;display:flex;color:#726B61;">''' + ic('search', 18) + '''</span>
<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Pesquisar caracteres</span>
<input type="search" value="{{query}}" onChange="{{onQuery}}" placeholder="Caractere, romaji ou significado" style="width:100%;height:48px;box-sizing:border-box;padding:0 14px 0 42px;border:1px solid #E6E0D6;border-radius:14px;background:#FFFFFF;font-size:15px;color:#1F1C18;outline:none;">
</label>
<div role="group" aria-label="Categoria" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;padding:4px;background:#F2EEE6;border-radius:14px;">
<sc-for list="{{cats}}" as="f" hint-placeholder-count="4"><button onClick="{{f.pick}}" aria-pressed="{{f.pressed}}" style="height:36px;border:none;border-radius:10px;background-color:{{f.bg}};color:{{f.fg}};font-weight:{{f.fw}};box-shadow:{{f.sh}};font-size:13px;cursor:pointer;">{{f.label}}</button></sc-for>
</div>
</div>
<div role="group" aria-label="Filtros" style="display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding:10px 24px 0;">
<sc-for list="{{jlpts}}" as="p" hint-placeholder-count="5"><button class="btn" onClick="{{p.pick}}" aria-pressed="{{p.pressed}}" style="''' + MCHIP.replace('%s', 'p') + '''">{{p.label}}</button></sc-for>
<span aria-hidden="true" style="flex-shrink:0;width:1px;height:22px;align-self:center;background:#E0D9CD;"></span>
<sc-for list="{{diffs}}" as="p" hint-placeholder-count="3"><button class="btn" onClick="{{p.pick}}" aria-pressed="{{p.pressed}}" style="''' + MCHIP.replace('%s', 'p') + '''">{{p.label}}</button></sc-for>
</div>
<div style="position:absolute;left:0;top:236px;width:390px;height:528px;overflow-y:auto;box-sizing:border-box;padding:6px 24px 24px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin:0 0 10px;"><p role="status" style="margin:0;font-size:13px;color:#726B61;">{{shown}} caracteres</p><a href="Kanji.dc.html" style="font-size:14px;font-weight:700;text-decoration:none;display:flex;align-items:center;gap:4px;">Kanji por componentes''' + ic('arrow', 14, 2) + '''</a></div>
<sc-if value="{{empty}}" hint-placeholder-val="{{false}}"><p style="margin:24px 0;text-align:center;font-size:15px;color:#726B61;">Nenhum caractere encontrado.</p></sc-if>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;">
<sc-for list="{{cards}}" as="it" hint-placeholder-count="6">
<a href="DetalheMobile.dc.html" class="card" style="display:flex;flex-direction:column;gap:6px;padding:12px;border-radius:18px;border:1px solid #E6E0D6;background:#FFFFFF;text-decoration:none;color:#1F1C18;min-width:0;">
<span style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background-color:{{it.tb}};color:{{it.tf}};">{{it.tl}}</span>
<sc-if value="{{it.hasJlpt}}" hint-placeholder-val="{{false}}"><span style="font-size:10px;font-weight:700;color:#5E5850;border:1px solid #E6E0D6;padding:2px 6px;border-radius:999px;">{{it.jlpt}}</span></sc-if>
</span>
<span class="jp" style="height:64px;display:flex;align-items:center;justify-content:center;font-size:{{it.gs}};line-height:1;">{{it.c}}</span>
<span style="text-align:center;font-size:13px;color:#5E5850;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.sub}}</span>
<span style="border-top:1px solid #EFEAE1;padding-top:6px;display:flex;flex-direction:column;gap:1px;min-width:0;">
<span style="font-size:14px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.pt}}</span>
<span style="font-size:12px;color:#726B61;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.en}}</span>
</span>
</a>
</sc-for>
</div>
<sc-if value="{{hasMore}}" hint-placeholder-val="{{false}}"><div style="display:flex;justify-content:center;padding:20px 0 8px;"><button class="btn soft" onClick="{{loadMore}}" style="height:44px;padding:0 20px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:14px;font-weight:500;cursor:pointer;">{{moreLabel}}</button></div></sc-if>
</div>
''' + tabbar('caracteres') + '''
</div>'''

script_c = acctify(DBJS + js('account.js') + FILTER_JS + r'''
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'CaracteresMobile.dc.html'; this.state = { cat: 'kanji', jlpt: 'N5', diff: null, group: null, query: '', anim: 0 }; }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
    const st = this.state;
    const D = kdb();
    const list = D ? filterList(D, st) : [];
    const key = JSON.stringify([st.cat, st.jlpt, st.diff, st.group, st.query]);
    const lim = this._lim && this._lim.key === key ? this._lim.n : 40;
    const cards = list.slice(0, lim).map((e) => cardOf(e, accent, null, null)).map((c) => Object.assign(c, { gs: c.gs === '64px' ? '52px' : '38px' }));
    return {
      accent, query: st.query, cards, shown: list.length, empty: !!D && list.length === 0,
      hasMore: list.length > lim, moreLabel: 'Mostrar mais (' + (list.length - lim) + ')', loadMore: () => { this._lim = { key, n: lim + 40 }; this.forceUpdate(); },
      cats: catList(this, D).map((c) => Object.assign(c, { label: c.label === 'Todos' ? 'Todos' : c.label })),
      jlpts: toggleList(this, 'jlpt', ['N5', 'N4', 'N3', 'N2', 'N1'], ['N5', 'N4', 'N3', 'N2', 'N1']),
      diffs: toggleList(this, 'diff', ['iniciante', 'intermediario', 'avancado'], ['Iniciante', 'Intermediário', 'Avançado']),
      onQuery: (ev) => this.setState({ query: ev.target.value })
    };
  }
}''')
open('project/CaracteresMobile.dc.html', 'w').write(page('Kaku — Caracteres (celular)', 'pt-BR', body_c, script_c, 390, 844, DATA_HEAD))

# ---------- Detalhe (mobile) ----------
body_d = '<div style="' + MROOT + '">\n' + '''<header style="display:flex;align-items:center;justify-content:space-between;padding:16px 16px 8px;">
<a href="CaracteresMobile.dc.html" aria-label="Voltar para caracteres" class="soft" style="width:44px;height:44px;border-radius:999px;display:flex;align-items:center;justify-content:center;color:#1F1C18;">''' + ic('back', 22) + '''</a>
<sc-if value="{{ready}}" hint-placeholder-val="{{true}}"><div style="display:flex;gap:8px;align-items:center;">
<span style="font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:4px 10px;border-radius:999px;background-color:{{d.tb}};color:{{d.tf}};">{{d.tl}}</span>
<sc-if value="{{hasJlpt}}" hint-placeholder-val="{{true}}"><span style="font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;border:1px solid #E6E0D6;">{{d.jlpt}}</span></sc-if>
</div></sc-if>
<div style="display:flex;gap:4px;">
<sc-if value="{{hasOrder}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{replay}}" aria-label="Repetir animação da escrita" style="width:44px;height:44px;border-radius:999px;border:none;background:transparent;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('replay', 20) + '''</button></sc-if>
<button class="btn soft" onClick="{{speak}}" aria-label="Ouvir pronúncia" style="width:44px;height:44px;border-radius:999px;border:none;background:transparent;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('speaker', 20) + '''</button>
</div>
</header>
<main style="position:absolute;left:0;top:68px;width:390px;height:680px;overflow-y:auto;box-sizing:border-box;padding:4px 24px 32px;">
<sc-if value="{{ready}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:20px;">
''' + detail_block(200, compact=True) + '''
</div></sc-if>
</main>
<div style="position:absolute;left:0;bottom:0;width:390px;box-sizing:border-box;padding:14px 24px 24px;background:#F7F4EE;border-top:1px solid #E6E0D6;">
''' + list_picker(compact=True, practice_href='PraticarMobile.dc.html') + '''
</div>
</div>'''

script_d = acctify(DBJS + js('account.js') + r'''
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'DetalheMobile.dc.html'; this.state = { sel: 'kanji:木', anim: 0 }; }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
''' + DETAIL_JS + r'''
    return Object.assign({ accent }, detail);
  }
}''')
open('project/DetalheMobile.dc.html', 'w').write(page('Kaku — Detalhe do caractere (celular)', 'pt-BR', body_d, script_d, 390, 844, DATA_HEAD))
