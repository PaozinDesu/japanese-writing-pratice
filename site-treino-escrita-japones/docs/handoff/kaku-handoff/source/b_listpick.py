from common import *

def list_picker(compact=False, show_practice=True, practice_href='Praticar.dc.html'):
    """Ações do detalhe: praticar o caractere e 'Adicionar à lista de prática' (com criação rápida de lista)."""
    h = '46px' if compact else '50px'
    prac = ('<a href="' + practice_href + '" onClick="{{practiceThis}}" class="btn" style="' + ('flex:0 0 auto;padding:0 18px;' if compact else 'flex-grow:1;') + 'height:' + h + ';border-radius:14px;background-color:' + ACC + ';color:#FFFFFF;display:flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;font-weight:700;font-size:15px;white-space:nowrap;">' + ic('brush', 18) + 'Praticar</a>') if show_practice else ''
    return ('''<div style="display:flex;flex-direction:column;gap:10px;">
<div style="display:flex;gap:8px;">''' + prac + '''
<button class="btn soft" onClick="{{al.toggle}}" aria-expanded="{{al.openAttr}}" style="flex-grow:1;min-width:0;overflow:hidden;height:''' + h + ''';padding:0 14px;border-radius:14px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;gap:8px;font-size:15px;font-weight:500;cursor:pointer;white-space:nowrap;">''' + ic('list', 18) + '''{{al.''' + ('short' if compact else 'label') + '''}}</button>
</div>
<sc-if value="{{al.open}}" hint-placeholder-val="{{false}}">
<div class="rise" role="group" aria-label="Adicionar à lista de prática" style="display:flex;flex-direction:column;gap:12px;padding:16px;border-radius:16px;border:1px solid #E6E0D6;background:#FBF9F5;">
<sc-if value="{{al.out}}" hint-placeholder-val="{{false}}">
<p style="margin:0;font-size:14px;line-height:1.5;color:#3B3630;">Entre na sua conta para criar listas de prática e guardar este caractere.</p>
<div style="display:flex;gap:8px;"><a href="Login.dc.html" onClick="{{al.toLogin}}" class="btn" style="height:40px;padding:0 16px;border-radius:12px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;text-decoration:none;font-size:14px;font-weight:700;">Entrar</a><a href="Cadastro.dc.html" class="btn soft" style="height:40px;padding:0 16px;border-radius:12px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;text-decoration:none;font-size:14px;">Criar conta</a></div>
</sc-if>
<sc-if value="{{al.in}}" hint-placeholder-val="{{true}}">
<sc-if value="{{al.hasLists}}" hint-placeholder-val="{{true}}"><span style="font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#726B61;">Suas listas</span>
<div style="display:flex;flex-direction:column;gap:6px;max-height:190px;overflow-y:auto;scrollbar-width:thin;">
<sc-for list="{{al.lists}}" as="l" hint-placeholder-count="2"><button role="checkbox" aria-checked="{{l.pressed}}" onClick="{{l.pick}}" style="display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:12px;border:1px solid {{l.bd}};background-color:{{l.bg}};cursor:pointer;text-align:left;color:#1F1C18;">
<span aria-hidden="true" style="width:20px;height:20px;flex-shrink:0;border-radius:6px;border:2px solid {{l.bd}};background-color:{{l.bd}};color:#FFFFFF;display:flex;align-items:center;justify-content:center;box-sizing:border-box;"><sc-if value="{{l.has}}" hint-placeholder-val="{{false}}">''' + ic('check', 13, 3) + '''</sc-if></span>
<span style="flex-grow:1;min-width:0;display:flex;flex-direction:column;"><span style="font-size:14px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{l.name}}</span><span style="font-size:12px;color:#726B61;">{{l.count}}</span></span></button></sc-for>
</div></sc-if>
<form onSubmit="{{al.create}}" style="display:flex;flex-direction:column;gap:6px;margin:0;">
<label for="al-nova" style="font-size:13px;font-weight:700;color:#5E5850;">Nova lista</label>
<div style="display:flex;gap:8px;"><input id="al-nova" type="text" value="{{al.name}}" onChange="{{al.onName}}" placeholder="Ex.: Kanji N5 — Semana 1" maxlength="60" style="flex-grow:1;min-width:0;height:42px;box-sizing:border-box;padding:0 12px;border:1px solid #D9D1C4;border-radius:10px;background:#FFFFFF;font-size:14px;color:#1F1C18;outline:none;">
<button type="submit" class="btn" style="height:42px;padding:0 12px;border-radius:10px;border:none;background-color:#1F1C18;color:#FFFFFF;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap;">Criar e adicionar</button></div>
<sc-if value="{{al.hasErr}}" hint-placeholder-val="{{false}}"><span role="alert" style="font-size:13px;color:#A8292A;">{{al.err}}</span></sc-if>
</form>
<sc-if value="{{al.hasMsg}}" hint-placeholder-val="{{false}}"><span role="status" style="font-size:13px;font-weight:700;color:#4E6E3A;">{{al.msg}}</span></sc-if>
<a href="Listas.dc.html" style="font-size:13px;font-weight:700;text-decoration:none;">Gerenciar minhas listas</a>
</sc-if>
</div>
</sc-if>
</div>''')
