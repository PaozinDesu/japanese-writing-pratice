from common import *
from b_chars import DBJS, DATA_HEAD
from b_practice import BTN_O, BTN_R, LBL, CARD, login_prompt

from ui import INPUT, BTN_SM_O as SMALL_O

def err(hole):
    return '<sc-if value="{{' + hole + 'On}}" hint-placeholder-val="{{false}}"><span role="alert" style="font-size:13px;color:#A8292A;">{{' + hole + '}}</span></sc-if>'

def pills(lst):
    return ('<sc-for list="{{' + lst + '}}" as="p" hint-placeholder-count="3"><button class="btn" onClick="{{p.pick}}" aria-pressed="{{p.pressed}}" style="height:36px;padding:0 12px;border-radius:999px;border:1px solid {{p.bd}};background-color:{{p.bg}};color:{{p.fg}};font-size:13px;font-weight:500;cursor:pointer;">{{p.label}}</button></sc-for>')

body = ('<div style="width:1440px;height:1240px;box-sizing:border-box;background:#F7F4EE;display:flex;flex-direction:column;overflow:hidden;">\n' + nav('') + '''
<main style="display:flex;flex-direction:column;gap:24px;padding:40px 64px 40px;min-height:0;flex-grow:1;">
<div style="display:flex;flex-direction:column;gap:8px;">
<h1 class="disp" style="margin:0;font-size:44px;font-weight:700;">Minhas listas</h1>
<p style="margin:0;font-size:16px;color:#5E5850;">Monte conjuntos de estudo com qualquer caractere do Kaku e pratique só o que você escolheu.</p>
</div>
<sc-if value="{{acct.out}}" hint-placeholder-val="{{false}}"><section style="''' + CARD + '''max-width:640px;padding:24px;">''' + login_prompt('Entre para criar listas', 'Suas listas ficam salvas na sua conta e aparecem na aba Praticar.') + '''</section></sc-if>
<sc-if value="{{ready}}" hint-placeholder-val="{{true}}">
<div style="display:grid;grid-template-columns:360px minmax(0,1fr);gap:24px;align-items:start;min-height:0;">
<section aria-labelledby="t-listas" style="''' + CARD + '''padding:22px;display:flex;flex-direction:column;gap:16px;">
<h2 id="t-listas" style="margin:0;font-size:17px;font-weight:700;">Listas <span style="font-weight:500;color:#726B61;">({{nLists}})</span></h2>
<form onSubmit="{{create}}" style="display:flex;flex-direction:column;gap:6px;margin:0;">
<label for="nova-lista" style="font-size:13px;font-weight:700;color:#5E5850;">Nova lista</label>
<div style="display:flex;gap:8px;"><input id="nova-lista" type="text" value="{{newName}}" onChange="{{onNewName}}" placeholder="Ex.: Kanji N5 — Semana 1" maxlength="60" style="flex-grow:1;''' + INPUT + '''"><button type="submit" class="btn" aria-label="Criar lista" style="width:46px;height:46px;flex-shrink:0;''' + BTN_R + '''">''' + ic('plus', 20, 2.2) + '''</button></div>
''' + err('newErr') + '''
</form>
<div role="listbox" aria-label="Suas listas" style="display:flex;flex-direction:column;gap:6px;">
<sc-for list="{{lists}}" as="l" hint-placeholder-count="3"><button role="option" aria-selected="{{l.sel}}" onClick="{{l.pick}}" class="soft" style="display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;border:1px solid {{l.bd}};background-color:{{l.bg}};cursor:pointer;text-align:left;color:#1F1C18;">
<span class="jp" style="width:40px;height:40px;flex-shrink:0;border-radius:10px;background:#F7F4EE;display:flex;align-items:center;justify-content:center;font-size:22px;">{{l.first}}</span>
<span style="flex-grow:1;min-width:0;display:flex;flex-direction:column;gap:2px;"><strong style="font-size:15px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{l.name}}</strong><span style="font-size:12px;color:#726B61;">{{l.count}} · {{l.when}}</span></span></button></sc-for>
</div>
<sc-if value="{{noLists}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;color:#5E5850;line-height:1.5;">Nenhuma lista ainda.</p></sc-if>
</section>

<div style="display:flex;flex-direction:column;gap:20px;min-width:0;">
<sc-if value="{{noSel}}" hint-placeholder-val="{{false}}">
<section style="''' + CARD + '''padding:40px;display:flex;flex-direction:column;align-items:flex-start;gap:14px;">
<span style="width:56px;height:56px;border-radius:16px;background:#FBEDEA;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic('list', 28) + '''</span>
<h2 class="disp" style="margin:0;font-size:28px;font-weight:700;">Crie sua primeira lista</h2>
<p style="margin:0;font-size:15px;line-height:1.6;color:#5E5850;max-width:560px;">Dê um nome à lista ao lado e adicione os caracteres que quiser — kanji de qualquer nível, hiragana ou katakana. Você também pode adicionar caracteres pelo botão “Adicionar à lista de prática” nos detalhes de cada caractere.</p>
<button class="btn soft" onClick="{{example}}" style="height:46px;padding:0 18px;font-size:15px;''' + BTN_O + '''">Criar a lista de exemplo “Kanji N5 — Semana 1”</button>
</section>
</sc-if>
<sc-if value="{{hasSel}}" hint-placeholder-val="{{true}}">
<section aria-labelledby="t-sel" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:18px;">
<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;">
<sc-if value="{{notRenaming}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:4px;min-width:0;"><h2 id="t-sel" class="disp" style="margin:0;font-size:30px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{sel.name}}</h2><span style="font-size:14px;color:#726B61;">{{sel.count}} · atualizada {{sel.when}}</span></div></sc-if>
<sc-if value="{{renaming}}" hint-placeholder-val="{{false}}"><form onSubmit="{{saveRename}}" style="display:flex;flex-direction:column;gap:6px;margin:0;flex-grow:1;max-width:520px;"><label for="ren" style="font-size:13px;font-weight:700;color:#5E5850;">Nome da lista</label><div style="display:flex;gap:8px;"><input id="ren" type="text" value="{{renameVal}}" onChange="{{onRename}}" maxlength="60" style="flex-grow:1;''' + INPUT + '''"><button type="submit" class="btn" style="height:46px;padding:0 16px;font-size:14px;''' + BTN_R + '''">Salvar</button><button type="button" onClick="{{cancelRename}}" class="btn soft" style="height:46px;padding:0 14px;font-size:14px;''' + BTN_O + '''">Cancelar</button></div>''' + err('renameErr') + '''</form></sc-if>
<div style="display:flex;gap:8px;flex-shrink:0;">
<button class="btn soft" onClick="{{startRename}}" style="''' + SMALL_O + '''">''' + ic('pencil', 16) + '''Renomear</button>
<button class="btn soft" onClick="{{askDelete}}" style="''' + SMALL_O + '''color:#A8292A;">''' + ic('trash', 16) + '''Excluir</button>
<sc-if value="{{sel.has}}" hint-placeholder-val="{{true}}"><a href="Praticar.dc.html" onClick="{{practice}}" class="btn" style="height:40px;padding:0 16px;font-size:14px;''' + BTN_R + '''border-radius:999px;">''' + ic('brush', 16) + '''Praticar esta lista</a></sc-if>
</div>
</div>
<sc-if value="{{confirmDel}}" hint-placeholder-val="{{false}}"><div role="alertdialog" aria-label="Confirmar exclusão" class="rise" style="display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 16px;border-radius:14px;background:#F8E4E0;"><span style="font-size:14px;color:#6E1C1D;">Excluir a lista <strong>“{{sel.name}}”</strong>? Os caracteres continuam no site; só a lista é apagada.</span><span style="display:flex;gap:8px;flex-shrink:0;"><button onClick="{{doDelete}}" class="btn" style="height:40px;padding:0 16px;font-size:14px;border-radius:12px;border:none;background:#A8292A;color:#FFFFFF;font-weight:700;cursor:pointer;">Excluir lista</button><button onClick="{{cancelDelete}}" class="btn soft" style="height:40px;padding:0 14px;font-size:14px;''' + BTN_O + '''">Cancelar</button></span></div></sc-if>
<sc-if value="{{sel.empty}}" hint-placeholder-val="{{false}}"><p style="margin:0;padding:22px;border:1px dashed #D9D1C4;border-radius:16px;text-align:center;font-size:15px;color:#5E5850;">Lista vazia — adicione caracteres na busca abaixo.</p></sc-if>
<div style="display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:8px;max-height:236px;overflow-y:auto;scrollbar-width:thin;padding:2px;">
<sc-for list="{{items}}" as="it" hint-placeholder-count="10"><div style="position:relative;display:flex;flex-direction:column;align-items:center;gap:2px;padding:10px 4px 8px;border-radius:14px;border:1px solid #E6E0D6;background:#FFFFFF;min-width:0;">
<span class="jp" style="font-size:{{it.fs}};line-height:1.15;">{{it.c}}</span><span style="font-size:11px;color:#5E5850;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{it.sub}}</span>
<button onClick="{{it.remove}}" aria-label="Remover {{it.c}} da lista" style="position:absolute;top:2px;right:2px;width:26px;height:26px;border:none;border-radius:999px;background:transparent;color:#8A8278;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('x', 14, 2.2) + '''</button>
</div></sc-for>
</div>
<sc-if value="{{msgOn}}" hint-placeholder-val="{{false}}"><span role="status" style="font-size:13px;font-weight:700;color:#4E6E3A;">{{msg}}</span></sc-if>
</section>

<section aria-labelledby="t-add" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:16px;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:16px;"><h2 id="t-add" style="margin:0;font-size:17px;font-weight:700;">Adicionar caracteres</h2><span style="font-size:13px;color:#726B61;">{{found}}</span></div>
<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
<label style="position:relative;display:flex;align-items:center;width:380px;"><span style="position:absolute;left:14px;display:flex;color:#726B61;">''' + ic('search', 18) + '''</span><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Buscar caracteres</span>
<input type="search" value="{{q}}" onChange="{{onQ}}" placeholder="Caractere, leitura, romaji ou significado" style="width:100%;''' + INPUT + '''padding-left:42px;"></label>
<div role="group" aria-label="Categoria" style="display:flex;gap:6px;">''' + pills('cats') + '''</div>
<div role="group" aria-label="JLPT" style="display:flex;gap:6px;">''' + pills('jlpts') + '''</div>
</div>
<div style="display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:8px;max-height:300px;overflow-y:auto;scrollbar-width:thin;padding:2px;">
<sc-for list="{{results}}" as="r" hint-placeholder-count="24"><button onClick="{{r.toggle}}" aria-pressed="{{r.pressed}}" title="{{r.title}}" style="position:relative;height:64px;border-radius:12px;border:1px solid {{r.bd}};background-color:{{r.bg}};cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;color:#1F1C18;min-width:0;">
<span class="jp" style="font-size:{{r.fs}};line-height:1.1;">{{r.c}}</span><span style="font-size:10px;color:#726B61;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:0 2px;">{{r.sub}}</span>
<sc-if value="{{r.in}}" hint-placeholder-val="{{false}}"><span aria-hidden="true" style="position:absolute;top:3px;right:3px;width:16px;height:16px;border-radius:999px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;justify-content:center;">''' + ic('check', 11, 3) + '''</span></sc-if>
</button></sc-for>
</div>
<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
<span style="font-size:13px;color:#726B61;">Clique num caractere para adicionar ou remover.</span>
<div style="display:flex;gap:8px;">
<sc-if value="{{hasMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{more}}" style="''' + SMALL_O + '''">{{moreLabel}}</button></sc-if>
<sc-if value="{{canAddAll}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{addAll}}" style="''' + SMALL_O + '''">''' + ic('plus', 16, 2) + '''{{addAllLabel}}</button></sc-if>
</div>
</div>
</section>
</sc-if>
</div>
</div>
</sc-if>
</main>
</div>''')

script = acctify(DBJS + js('account.js') + r'''
const CATS = [['todos', 'Todos'], ['hiragana', 'Hiragana'], ['katakana', 'Katakana'], ['kanji', 'Kanji']];
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'Listas.dc.html'; this.state = { sel: null, newName: '', newErr: '', renaming: false, renameVal: '', renameErr: '', confirmDel: false, q: '', cat: 'todos', jlpt: null, lim: 96, msg: '' }; }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
    const st = this.state, D = kdb(), u = Auth.current();
    const lists = u ? UD.load(u).lists : [];
    const selL = lists.find((l) => l.id === st.sel) || lists[0] || null;
    const base = { accent, ready: !!u && !!D, nLists: lists.length };
    if (!u || !D) return Object.assign(base, { lists: [], items: [], results: [], cats: [], jlpts: [] });
    const word = (n) => n + (n === 1 ? ' caractere' : ' caracteres');
    const pick = (id) => this.setState({ sel: id, renaming: false, confirmDel: false, msg: '', mdetail: true });
    const listItems = lists.map((l) => { const on = selL && l.id === selL.id; return { name: l.name, count: word(l.chars.length), when: fmtDate(l.updated), first: l.chars[0] ? l.chars[0].split(':')[1] : '・', sel: on ? 'true' : 'false', bd: on ? accent : '#E6E0D6', bg: on ? '#FBEDEA' : '#FFFFFF', pick: () => pick(l.id) }; });
    const inSel = new Set(selL ? selL.chars : []);
    const items = selL ? selL.chars.map((id) => { const e = D._idx[id]; const c = e ? e.char : id.split(':')[1]; return { c, fs: Array.from(c).length > 1 ? '20px' : '28px', sub: e ? (e.category === 'kanji' ? e.meaning.pt[0] : e.romaji) : '', remove: () => { Lists.removeChar(selL.id, id); this.setState({ msg: 'Removido: ' + c }); } }; }) : [];
    const q = norm(st.q).trim();
    const all = D.characters.filter((e) => (st.cat === 'todos' || e.category === st.cat) && (!st.jlpt || e.jlpt === st.jlpt) && (!q || e._hay.includes(q)));
    const results = all.slice(0, st.lim).map((e) => { const on = inSel.has(e.id); return { c: e.char, fs: Array.from(e.char).length > 1 ? '17px' : '24px', sub: e.category === 'kanji' ? e.meaning.pt[0] : e.romaji, title: e.char + ' — ' + e.meaning.pt.join('; '), in: on, pressed: on ? 'true' : 'false', bd: on ? accent : '#E6E0D6', bg: on ? '#FBEDEA' : '#FFFFFF', toggle: () => { if (!selL) return; Lists.toggle(selL.id, e.id); this.setState({ msg: (on ? 'Removido: ' : 'Adicionado: ') + e.char }); } }; });
    const missing = all.filter((e) => !inSel.has(e.id));
    const pillVals = (on) => ({ pressed: on ? 'true' : 'false', bg: on ? '#1F1C18' : '#FFFFFF', fg: on ? '#FFFFFF' : '#5E5850', bd: on ? '#1F1C18' : '#E6E0D6' });
    const create = (ev) => { if (ev && ev.preventDefault) ev.preventDefault(); const r = Lists.create(st.newName, []); if (r.error) this.setState({ newErr: r.error }); else this.setState({ newName: '', newErr: '', sel: r.id, mdetail: true, msg: 'Lista criada. Agora adicione caracteres.' }); };
    return Object.assign(base, {
      lists: listItems, noLists: !lists.length, hasSel: !!selL, noSel: !selL, mOpen: !!st.mdetail && !!selL, mList: !(st.mdetail && selL), mClose: () => this.setState({ mdetail: false, renaming: false, confirmDel: false }),
      newName: st.newName, onNewName: (ev) => this.setState({ newName: ev.target.value, newErr: '' }), create, newErr: st.newErr, newErrOn: !!st.newErr,
      example: () => { const ids = Array.from('日月火水木金土人山川').map((c) => 'kanji:' + c).filter((id) => D._idx[id]); const r = Lists.create('Kanji N5 — Semana 1', ids); if (r.error) this.setState({ newErr: r.error }); else this.setState({ sel: r.id, mdetail: true, msg: 'Lista de exemplo criada.' }); },
      sel: selL ? { name: selL.name, count: word(selL.chars.length), when: fmtDate(selL.updated, true), has: selL.chars.length > 0, empty: !selL.chars.length } : { name: '', count: '', when: '', has: false, empty: false },
      items, msg: st.msg, msgOn: !!st.msg,
      renaming: st.renaming, notRenaming: !st.renaming, renameVal: st.renameVal, renameErr: st.renameErr, renameErrOn: !!st.renameErr,
      startRename: () => this.setState({ renaming: true, renameVal: selL.name, renameErr: '', confirmDel: false }),
      onRename: (ev) => this.setState({ renameVal: ev.target.value, renameErr: '' }),
      saveRename: (ev) => { if (ev && ev.preventDefault) ev.preventDefault(); const r = Lists.rename(selL.id, st.renameVal); if (r.error) this.setState({ renameErr: r.error }); else this.setState({ renaming: false, msg: 'Nome atualizado.' }); },
      cancelRename: () => this.setState({ renaming: false, renameErr: '' }),
      confirmDel: st.confirmDel, askDelete: () => this.setState({ confirmDel: true, renaming: false }), cancelDelete: () => this.setState({ confirmDel: false }),
      doDelete: () => { const name = selL.name; Lists.remove(selL.id); this.setState({ confirmDel: false, sel: null, msg: '' , newErr: '', mdetail: false }); },
      practice: () => Intent.set({ kind: 'list', listId: selL.id }),
      q: st.q, onQ: (ev) => this.setState({ q: ev.target.value, lim: 96 }),
      cats: CATS.map(([id, label]) => Object.assign({ label, pick: () => this.setState({ cat: id, jlpt: id === 'kanji' || id === 'todos' ? st.jlpt : null, lim: 96 }) }, pillVals(st.cat === id))),
      jlpts: ['N5', 'N4', 'N3', 'N2', 'N1'].map((lv) => Object.assign({ label: lv, pick: () => this.setState({ jlpt: st.jlpt === lv ? null : lv, cat: st.jlpt === lv ? st.cat : 'kanji', lim: 96 }) }, pillVals(st.jlpt === lv))),
      results, found: fmtInt(all.length) + (all.length === 1 ? ' resultado' : ' resultados'),
      hasMore: all.length > st.lim, moreLabel: 'Mostrar mais (' + fmtInt(all.length - st.lim) + ')', more: () => this.setState({ lim: st.lim + 192 }),
      canAddAll: missing.length > 0 && missing.length <= 400, addAllLabel: 'Adicionar ' + (missing.length === all.length ? 'todos os ' : 'os ') + fmtInt(missing.length) + (missing.length === all.length ? '' : ' que faltam'),
      addAll: () => { Lists.add(selL.id, missing.map((e) => e.id)); this.setState({ msg: missing.length + ' caracteres adicionados.' }); }
    });
  }
}''')

if __name__ == '__main__':
    open('project/Listas.dc.html', 'w').write(page('Kaku — Minhas listas', 'pt-BR', body, script, 1440, 1240, DATA_HEAD))
