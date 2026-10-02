from common import *
from b_chars import DBJS, DATA_HEAD

from ui import OVERLINE as LBL, CARD, BTN_O, BTN_R, INPUT
from b_tabs import mode_tabs

def practice_script(cs, page_name):
    return acctify(DBJS + js('account.js') + 'const CS = %d;\nconst PAGE = %r;\n' % (cs, page_name) + js('rec.js') + js('practice.js'))

def chips(lst, extra=''):
    return ('<sc-for list="{{' + lst + '}}" as="o" hint-placeholder-count="3"><button class="btn" onClick="{{o.pick}}" aria-pressed="{{o.pressed}}" style="height:40px;padding:0 14px;border-radius:999px;border:1px solid {{o.bd}};background-color:{{o.bg}};color:{{o.fg}};font-size:14px;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:8px;' + extra + '">{{o.label}}<span style="font-size:12px;opacity:.7;">{{o.count}}</span></button></sc-for>')

def seg(lst, h=40):
    return ('<div role="group" style="display:flex;gap:4px;padding:4px;background:#F2EEE6;border-radius:999px;align-self:flex-start;">'
            '<sc-for list="{{' + lst + '}}" as="s" hint-placeholder-count="2"><button onClick="{{s.pick}}" aria-pressed="{{s.pressed}}" style="height:%dpx;padding:0 16px;border:none;border-radius:999px;background-color:{{s.bg}};color:{{s.fg}};font-weight:{{s.fw}};box-shadow:{{s.sh}};font-size:14px;cursor:pointer;">{{s.label}}</button></sc-for></div>' % h)

def login_prompt(title, text, compact=False):
    return ('''<div style="display:flex;gap:14px;align-items:flex-start;padding:18px;border-radius:16px;background:#F7F4EE;">
<span style="width:40px;height:40px;flex-shrink:0;border-radius:12px;background:#FFFFFF;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic('lock', 20) + '''</span>
<div style="display:flex;flex-direction:column;gap:10px;min-width:0;">
<div style="display:flex;flex-direction:column;gap:2px;"><strong style="font-size:15px;">''' + title + '''</strong><span style="font-size:14px;line-height:1.5;color:#5E5850;">''' + text + '''</span></div>
<div style="display:flex;gap:8px;flex-wrap:wrap;">
<a href="Login.dc.html" onClick="{{toLogin}}" class="btn" style="height:40px;padding:0 16px;font-size:14px;''' + BTN_R + '''">Entrar</a>
<a href="Cadastro.dc.html" class="btn soft" style="height:40px;padding:0 16px;font-size:14px;''' + BTN_O + '''">Criar conta</a>
</div></div></div>''')

def glyph_tile(size, font_hole, extra=''):
    return ('<span class="jp pop" style="width:%dpx;height:%dpx;flex-shrink:0;border-radius:16px;border:1px solid #E6E0D6;background:#FBF9F5;display:flex;align-items:center;justify-content:center;font-size:{{%s}};line-height:1;%s">' % (size, size, font_hole, extra))

def canvas_area(cs):
    return ('''<div style="position:relative;width:%dpx;height:%dpx;border-radius:16px;background:#FFFEFB;box-shadow:inset 0 0 0 1px #EFEAE1;overflow:hidden;flex-shrink:0;">
<sc-if value="{{guide}}" hint-placeholder-val="{{true}}">''' % (cs, cs) + grid_svg(cs) + '''</sc-if>
<sc-if value="{{ghost}}" hint-placeholder-val="{{false}}"><span aria-hidden="true" class="jp fade" style="position:absolute;left:0;top:0;width:%dpx;height:%dpx;display:flex;align-items:center;justify-content:center;font-size:{{t.gsG}};line-height:1;color:#F0D3CD;pointer-events:none;">{{t.c}}</span></sc-if>
<canvas ref="{{setCanvas}}" onPointerDown="{{onDown}}" onPointerMove="{{onMove}}" onPointerUp="{{onUp}}" onPointerCancel="{{onUp}}" onPointerLeave="{{onUp}}" aria-label="Quadro de desenho: escreva o caractere com o mouse ou o dedo" style="position:absolute;left:0;top:0;width:%dpx;height:%dpx;touch-action:none;cursor:crosshair;"></canvas>
<sc-if value="{{emptyHint}}" hint-placeholder-val="{{true}}"><span aria-hidden="true" style="position:absolute;left:0;right:0;bottom:16px;text-align:center;font-size:14px;color:#8A8278;pointer-events:none;">Escreva aqui com o mouse ou o dedo</span></sc-if>
<sc-if value="{{busy}}" hint-placeholder-val="{{false}}"><div class="fade" role="status" style="position:absolute;left:0;top:0;width:%dpx;height:%dpx;background:rgba(255,254,251,.72);display:flex;align-items:center;justify-content:center;gap:8px;font-size:15px;font-weight:700;color:#5E5850;">@@SPIN@@Analisando o desenho…</div></sc-if>
</div>''' % (cs, cs, cs, cs, cs, cs)).replace('@@SPIN@@', spinner(20))

def toggles(h=36):
    return ('''<div style="display:flex;gap:8px;">
<button class="btn" onClick="{{toggleGuide}}" aria-pressed="{{guideP}}" style="height:%dpx;padding:0 14px;border-radius:999px;border:1px solid {{guideBd}};background-color:{{guideBg}};color:{{guideFg}};font-size:13px;font-weight:500;cursor:pointer;">Grade</button>
<button class="btn" onClick="{{toggleGhost}}" aria-pressed="{{ghostP}}" style="height:%dpx;padding:0 14px;border-radius:999px;border:1px solid {{ghostBd}};background-color:{{ghostBg}};color:{{ghostFg}};font-size:13px;font-weight:500;cursor:pointer;">Contorno</button>
</div>''' % (h, h))

def draw_controls():
    return ('''<div style="display:flex;align-items:center;gap:10px;width:100%;">
<button class="btn soft" onClick="{{undo}}" aria-label="Desfazer último traço" style="width:52px;height:52px;''' + BTN_O + '''">''' + ic('undo', 20) + '''</button>
<button class="btn soft" onClick="{{clear}}" style="height:52px;padding:0 20px;font-size:15px;''' + BTN_O + '''">''' + ic('eraser', 20) + '''Limpar</button>
<span style="flex-grow:1;"></span>
<sc-if value="{{noResult}}" hint-placeholder-val="{{true}}"><button class="btn" onClick="{{done}}" style="height:52px;padding:0 34px;font-size:16px;box-shadow:0 8px 18px -10px ''' + ACC + ''';''' + BTN_R + '''">''' + ic('check', 20, 2.2) + '''Pronto</button></sc-if>
<sc-if value="{{hasResult}}" hint-placeholder-val="{{false}}"><button class="btn" onClick="{{next}}" style="height:52px;padding:0 30px;font-size:16px;''' + BTN_R + '''">{{nextLabel}}''' + ic('arrow', 20, 2) + '''</button></sc-if>
</div>''')

def answer_block(kind):
    # kind: rd | mn
    title = '{{rdTitle}}' if kind == 'rd' else 'Significado'
    shown = ('<span style="display:flex;flex-direction:column;gap:2px;"><span class="jp" style="font-size:18px;font-weight:600;">{{t.r}}</span><span style="font-size:13px;color:#5E5850;">{{t.ro}}</span></span>'
             if kind == 'rd' else '<span style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:16px;font-weight:500;">{{t.pt}}</span><span style="font-size:13px;color:#726B61;">{{t.en}}</span></span>')
    ph = 'Romaji ou kana' if kind == 'rd' else 'Em português ou inglês'
    chip = kind + 'Chip'
    return ('''<div style="display:flex;flex-direction:column;gap:10px;padding-top:14px;border-top:1px solid #EFEAE1;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
<h3 style="''' + LBL + '''">''' + title + '''</h3>
<sc-if value="{{''' + kind + '''Hide}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{show''' + kind.capitalize() + '''}}" style="height:32px;padding:0 12px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:13px;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('eye', 15) + '''Mostrar</button></sc-if>
</div>
<sc-if value="{{''' + kind + '''Show}}" hint-placeholder-val="{{false}}"><div class="fade">''' + shown + '''</div></sc-if>
<form onSubmit="{{check''' + kind.capitalize() + '''}}" style="display:flex;gap:8px;margin:0;">
<label style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);" for="ans-''' + kind + '''">''' + ph + '''</label>
<input id="ans-''' + kind + '''" type="text" autocomplete="off" value="{{''' + kind + '''Ans}}" onChange="{{on''' + kind.capitalize() + '''}}" placeholder="''' + ph + '''" style="flex-grow:1;''' + INPUT + '''">
<button type="submit" class="btn soft" style="height:44px;padding:0 14px;font-size:14px;''' + BTN_O + '''">Verificar</button>
</form>
<sc-if value="{{''' + chip + '''.on}}" hint-placeholder-val="{{false}}"><span role="status" class="pop" style="align-self:flex-start;display:flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:999px;background-color:{{''' + chip + '''.bg}};color:{{''' + chip + '''.fg}};font-size:13px;font-weight:700;"><sc-if value="{{''' + chip + '''.ok}}" hint-placeholder-val="{{true}}">''' + ic('check', 16, 2.4) + '''</sc-if><sc-if value="{{''' + chip + '''.no}}" hint-placeholder-val="{{false}}">''' + ic('x', 16, 2.4) + '''</sc-if>{{''' + chip + '''.label}}</span></sc-if>
</div>''')

def verdict_banner():
    return '''<div class="pop" role="status" style="display:flex;gap:12px;align-items:center;padding:14px 16px;border-radius:16px;background-color:{{v.bg}};">
<span style="width:38px;height:38px;flex-shrink:0;border-radius:999px;background-color:{{v.fg}};color:#FFFFFF;display:flex;align-items:center;justify-content:center;">
<sc-if value="{{vOk}}" hint-placeholder-val="{{true}}">''' + ic('check', 22, 2.4) + '''</sc-if>
<sc-if value="{{vAl}}" hint-placeholder-val="{{false}}">''' + ic('alert', 22, 2.6) + '''</sc-if>
<sc-if value="{{vNo}}" hint-placeholder-val="{{false}}">''' + ic('x', 22, 2.4) + '''</sc-if>
</span>
<span style="display:flex;flex-direction:column;gap:2px;"><strong style="font-size:17px;color:{{v.fg}};">{{v.label}}</strong><span style="font-size:13px;line-height:1.45;color:#3B3630;">{{v.sub}}</span></span>
</div>'''

def final_box():
    return '''<div style="display:flex;flex-direction:column;gap:10px;padding:14px 16px;border-radius:16px;border:1px solid #E6E0D6;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
<span style="font-size:14px;font-weight:700;">Resultado deste caractere</span>
<span style="height:28px;padding:0 12px;border-radius:999px;display:flex;align-items:center;font-size:13px;font-weight:700;background-color:{{finBg}};color:{{finFg}};">{{finLabel}}</span>
</div>
<span style="font-size:13px;color:#5E5850;line-height:1.45;">{{finWhy}}</span>
<div style="display:flex;align-items:center;gap:10px;"><span style="font-size:13px;color:#726B61;">Contar como</span>''' + seg('overs', 34) + '''</div>
</div>'''

# ======================= DESKTOP =======================
setup_d = '''<sc-if value="{{vSetup}}" hint-placeholder-val="{{true}}">
<main class="rise" style="display:flex;flex-direction:column;gap:24px;padding:40px 64px 48px;">
''' + mode_tabs('escrita') + '''
<div style="display:flex;flex-direction:column;gap:8px;">
<h1 class="disp" style="margin:0;font-size:44px;font-weight:700;">Pratica - Escrita</h1>
<p style="margin:0;font-size:16px;color:#5E5850;">Escolha o que praticar. Todo caractere do Kaku — hiragana, katakana e os 2.136 kanji — pode entrar numa sessão.</p>
</div>
<div style="display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:24px;align-items:start;">
<section aria-labelledby="nova" style="''' + CARD + '''padding:28px;display:flex;flex-direction:column;gap:24px;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:16px;">
<h2 id="nova" style="margin:0;font-size:20px;font-weight:700;">Nova sessão</h2>
''' + seg('srcs') + '''
</div>
<sc-if value="{{srcFilters}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:20px;">
<div style="display:flex;flex-direction:column;gap:10px;">
<h3 style="''' + LBL + '''">Sistema de escrita</h3>
<div role="group" aria-label="Sistema de escrita" style="display:flex;gap:8px;flex-wrap:wrap;">
<button class="btn" onClick="{{pickAll}}" aria-pressed="{{allChip.pressed}}" style="height:40px;padding:0 16px;border-radius:999px;border:1px solid {{allChip.bd}};background-color:{{allChip.bg}};color:{{allChip.fg}};font-size:14px;font-weight:500;cursor:pointer;">Todos</button>
''' + chips('cats') + '''
</div>
</div>
<div style="display:flex;flex-direction:column;gap:10px;">
<h3 style="''' + LBL + '''">Nível JLPT <span style="text-transform:none;letter-spacing:0;font-weight:500;">· vale para os kanji</span></h3>
<div role="group" aria-label="Nível JLPT" style="display:flex;gap:8px;flex-wrap:wrap;">''' + chips('jlpts') + '''</div>
</div>
<sc-if value="{{jlptNote}}" hint-placeholder-val="{{false}}"><p role="note" style="margin:0;font-size:13px;color:#7A5210;background:#F4EAD6;padding:10px 12px;border-radius:12px;">O nível JLPT só se aplica a kanji. Marque também “Kanji” para incluí-los.</p></sc-if>
</div>
</sc-if>
<sc-if value="{{srcList}}" hint-placeholder-val="{{false}}">
<div style="display:flex;flex-direction:column;gap:12px;">
<sc-if value="{{guest}}" hint-placeholder-val="{{false}}">''' + login_prompt('Entre para usar suas listas', 'As listas de estudo ficam salvas na sua conta. Com elas você pratica exatamente os caracteres que escolheu.') + '''</sc-if>
<sc-if value="{{noListsU}}" hint-placeholder-val="{{false}}"><div style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:18px;border-radius:16px;background:#F7F4EE;"><span style="font-size:15px;color:#3B3630;">Você ainda não tem listas de prática.</span><a href="Listas.dc.html" class="btn" style="height:40px;padding:0 16px;font-size:14px;''' + BTN_R + '''">''' + ic('plus', 18, 2) + '''Criar lista</a></div></sc-if>
<sc-if value="{{hasListsU}}" hint-placeholder-val="{{false}}">
<div role="radiogroup" aria-label="Escolher lista" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;">
<sc-for list="{{lists}}" as="l" hint-placeholder-count="2"><button class="card" role="radio" aria-checked="{{l.pressed}}" onClick="{{l.pick}}" style="display:flex;flex-direction:column;gap:6px;align-items:flex-start;text-align:left;padding:14px 16px;border-radius:16px;border:1px solid {{l.bd}};background-color:{{l.bg}};cursor:pointer;color:#1F1C18;min-width:0;">
<strong style="font-size:15px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{l.name}}</strong><span style="font-size:13px;color:#726B61;">{{l.count}}</span><span class="jp" style="font-size:17px;color:#3B3630;max-width:100%;overflow:hidden;white-space:nowrap;">{{l.preview}}</span></button></sc-for>
</div>
<a href="Listas.dc.html" style="align-self:flex-start;font-size:14px;font-weight:700;text-decoration:none;display:flex;align-items:center;gap:6px;">Gerenciar listas''' + ic('arrow', 16, 2) + '''</a>
</sc-if>
</div>
</sc-if>
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 18px;border-radius:16px;background:#F7F4EE;">
<span style="display:flex;flex-direction:column;gap:2px;"><strong style="font-size:16px;">{{poolLabel}}</strong><span style="font-size:14px;color:#5E5850;">{{poolCount}} {{poolWord}}</span></span>
<sc-if value="{{poolEmpty}}" hint-placeholder-val="{{false}}"><span style="font-size:13px;color:#A8292A;font-weight:700;">Nada para praticar com esta combinação</span></sc-if>
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;">
<div style="display:flex;flex-direction:column;gap:10px;"><h3 style="''' + LBL + '''">Quantidade</h3>''' + seg('sizes') + '''</div>
<div style="display:flex;flex-direction:column;gap:10px;">
<h3 style="''' + LBL + '''">Dificuldades</h3>
<button role="switch" aria-checked="{{prioAttr}}" onClick="{{togglePrio}}" style="display:flex;align-items:center;gap:12px;padding:0;border:none;background:transparent;cursor:pointer;text-align:left;color:#1F1C18;">
<span aria-hidden="true" style="position:relative;width:46px;height:26px;flex-shrink:0;border-radius:999px;background-color:{{prioBg}};transition:background-color .2s ease;"><span style="position:absolute;top:2px;left:{{prioX}};width:22px;height:22px;border-radius:999px;background:#FFFFFF;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:left .2s ease;"></span></span>
<span style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:14px;font-weight:500;">Priorizar os que mais errei</span><sc-if value="{{guest}}" hint-placeholder-val="{{false}}"><span style="font-size:12px;color:#726B61;">Disponível ao entrar na conta</span></sc-if></span>
</button>
</div>
</div>
<div style="display:flex;flex-direction:column;gap:10px;">
<h3 style="''' + LBL + '''">Como praticar</h3>
<div role="radiogroup" aria-label="Como praticar" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;">
<sc-for list="{{modes}}" as="m" hint-placeholder-count="2"><button role="radio" aria-checked="{{m.pressed}}" onClick="{{m.pick}}" style="display:flex;gap:12px;align-items:flex-start;text-align:left;padding:14px 16px;border-radius:16px;border:1px solid {{m.ring}};background-color:{{m.rbg}};cursor:pointer;color:#1F1C18;">
<span aria-hidden="true" style="width:18px;height:18px;flex-shrink:0;margin-top:2px;border-radius:999px;border:2px solid {{m.dotBd}};box-sizing:border-box;display:flex;align-items:center;justify-content:center;"><span style="width:8px;height:8px;border-radius:999px;background-color:{{m.dot}};"></span></span>
<span style="display:flex;flex-direction:column;gap:2px;"><strong style="font-size:15px;">{{m.label}}</strong><span style="font-size:13px;color:#5E5850;">{{m.sub}}</span></span></button></sc-for>
</div>
</div>
<sc-if value="{{canStart}}" hint-placeholder-val="{{true}}"><button class="btn" onClick="{{start}}" style="height:58px;font-size:17px;box-shadow:0 10px 22px -12px ''' + ACC + ''';''' + BTN_R + '''">''' + ic('brush', 20) + '''{{startLabel}}</button></sc-if>
<sc-if value="{{poolEmpty}}" hint-placeholder-val="{{false}}"><button disabled style="height:58px;font-size:17px;border-radius:14px;border:none;background:#E6E0D6;color:#726B61;font-weight:700;">Escolha o que praticar</button></sc-if>
</section>

<div style="display:flex;flex-direction:column;gap:20px;">
<sc-if value="{{guest}}" hint-placeholder-val="{{false}}"><section style="''' + CARD + '''padding:22px;">''' + login_prompt('Salve seu progresso', 'Você pode praticar sem conta, mas o histórico, as estatísticas e as listas só ficam salvos quando você entra.') + '''</section></sc-if>
<sc-if value="{{logged}}" hint-placeholder-val="{{true}}">
<section aria-labelledby="minhas" style="''' + CARD + '''padding:22px;display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><h2 id="minhas" style="margin:0;font-size:17px;font-weight:700;">Minhas listas</h2><a href="Listas.dc.html" style="font-size:14px;font-weight:700;text-decoration:none;">Gerenciar</a></div>
<sc-if value="{{noListsU}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;color:#5E5850;line-height:1.5;">Monte listas como “Kanji N5 — Semana 1” e pratique só esses caracteres.</p><a href="Listas.dc.html" class="btn soft" style="align-self:flex-start;height:40px;padding:0 14px;font-size:14px;''' + BTN_O + '''">''' + ic('plus', 18, 2) + '''Nova lista</a></sc-if>
<sc-for list="{{lists}}" as="l" hint-placeholder-count="2">
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-top:1px solid #EFEAE1;">
<div style="flex-grow:1;min-width:0;display:flex;flex-direction:column;gap:2px;"><span style="font-size:15px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{l.name}}</span><span style="font-size:13px;color:#726B61;">{{l.count}}</span></div>
<sc-if value="{{l.has}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{l.play}}" style="height:38px;padding:0 14px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:14px;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:6px;">''' + ic('brush', 16) + '''Praticar</button></sc-if>
<sc-if value="{{l.empty}}" hint-placeholder-val="{{false}}"><span style="font-size:13px;color:#726B61;">vazia</span></sc-if>
</div>
</sc-for>
</section>
</sc-if>
<section aria-labelledby="revisar" style="''' + CARD + '''padding:22px;display:flex;flex-direction:column;gap:14px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><h2 id="revisar" style="margin:0;font-size:17px;font-weight:700;">Para revisar</h2><span style="font-size:13px;color:#726B61;">mais erros</span></div>
<sc-if value="{{noHard}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;color:#5E5850;line-height:1.5;">Os caracteres em que você errar aparecem aqui — e ganham prioridade nas próximas sessões.</p></sc-if>
<sc-if value="{{hasHard}}" hint-placeholder-val="{{true}}">
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;">
<sc-for list="{{hard}}" as="h" hint-placeholder-count="5"><span data-tip="{{h.sub}}" tabindex="0" style="display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 4px;border-radius:12px;background:#F7F4EE;"><span class="jp" style="font-size:26px;line-height:1.1;">{{h.c}}</span><span style="font-size:11px;color:#726B61;white-space:nowrap;">{{h.sub}}</span></span></sc-for>
</div>
<button class="btn soft" onClick="{{reviewHard}}" style="height:44px;font-size:14px;''' + BTN_O + '''">''' + ic('target', 18) + '''Revisar estes caracteres</button>
</sc-if>
</section>
<sc-if value="{{hasLast}}" hint-placeholder-val="{{false}}">
<section style="''' + CARD + '''padding:20px 22px;display:flex;align-items:center;gap:14px;">
<span style="width:40px;height:40px;flex-shrink:0;border-radius:12px;background:#FBEDEA;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic('history', 20) + '''</span>
<div style="flex-grow:1;min-width:0;display:flex;flex-direction:column;gap:2px;"><span style="font-size:13px;color:#726B61;">Última sessão · {{last.when}}</span><span style="font-size:15px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{last.label}}</span></div>
<span style="display:flex;flex-direction:column;align-items:flex-end;gap:2px;"><strong style="font-size:17px;">{{last.acc}}</strong><span style="font-size:12px;color:#726B61;">{{last.n}} caract.</span></span>
</section>
</sc-if>
</div>
</div>
</main>
</sc-if>'''

session_d = '''<sc-if value="{{vSession}}" hint-placeholder-val="{{false}}">
<main style="display:flex;flex-direction:column;gap:20px;padding:28px 64px 40px;">
<div style="''' + CARD + '''padding:16px 22px;display:flex;align-items:center;gap:24px;">
<div style="display:flex;flex-direction:column;gap:2px;min-width:240px;max-width:320px;"><span style="font-size:13px;color:#726B61;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{label}}</span><strong style="font-size:18px;">{{numLabel}}</strong></div>
<div role="progressbar" aria-label="Progresso da sessão" aria-valuetext="{{numLabel}}" style="flex-grow:1;height:10px;border-radius:999px;background:#EFEAE1;overflow:hidden;"><div style="height:10px;border-radius:999px;width:{{progW}};background-color:''' + ACC + ''';transition:width .4s ease;"></div></div>
<span style="display:flex;align-items:center;gap:6px;height:34px;padding:0 12px;border-radius:999px;background:#E7EEDF;color:#4E6E3A;font-size:14px;font-weight:700;">''' + ic('check', 16, 2.4) + '''{{okN}}<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">acertos</span></span>
<span style="display:flex;align-items:center;gap:6px;height:34px;padding:0 12px;border-radius:999px;background:#F8E4E0;color:#A8292A;font-size:14px;font-weight:700;">''' + ic('x', 16, 2.4) + '''{{failN}}<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">erros</span></span>
<button class="btn soft" onClick="{{endSession}}" style="height:40px;padding:0 16px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:14px;cursor:pointer;">Encerrar sessão</button>
</div>
<div style="display:grid;grid-template-columns:330px minmax(0,1fr) 370px;gap:20px;align-items:start;">
<section aria-label="Caractere" style="''' + CARD + '''padding:22px;display:flex;flex-direction:column;gap:16px;">
<div style="display:flex;gap:8px;align-items:center;">
<span style="font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:4px 10px;border-radius:999px;background-color:{{t.tb}};color:{{t.tf}};">{{t.tl}}</span>
<sc-if value="{{t.hasJlpt}}" hint-placeholder-val="{{false}}"><span style="font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;border:1px solid #E6E0D6;">{{t.jlpt}}</span></sc-if>
<span style="flex-grow:1;"></span>
<button class="btn soft" onClick="{{speak}}" aria-label="Ouvir pronúncia" style="width:38px;height:38px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('speaker', 18) + '''</button>
</div>
<sc-if value="{{memPrompt}}" hint-placeholder-val="{{false}}"><div style="display:flex;flex-direction:column;gap:4px;"><span style="font-size:14px;color:#5E5850;">{{lead}}</span><span class="disp" style="font-size:28px;font-weight:700;line-height:1.2;">{{main}}</span><span style="font-size:14px;color:#726B61;">{{mainSub}}</span></div></sc-if>
<sc-if value="{{copyPrompt}}" hint-placeholder-val="{{true}}"><span style="font-size:14px;color:#5E5850;">Escreva este caractere no quadro:</span></sc-if>
<div style="position:relative;height:210px;border-radius:18px;background:#FBF9F5;border:1px solid #EFEAE1;display:flex;align-items:center;justify-content:center;">
<sc-if value="{{showChar}}" hint-placeholder-val="{{true}}"><span class="jp fade" style="font-size:{{t.gs}};line-height:1;">{{t.c}}</span></sc-if>
<sc-if value="{{hideChar}}" hint-placeholder-val="{{false}}"><span class="disp" style="font-size:56px;color:#C9C1B5;">?</span></sc-if>
</div>
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:13px;color:#726B61;">{{t.n}} traços</span>
<button class="btn soft" onClick="{{toggleChar}}" style="height:34px;padding:0 12px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;font-size:13px;cursor:pointer;display:flex;align-items:center;gap:6px;"><sc-if value="{{showChar}}" hint-placeholder-val="{{true}}">''' + ic('eyeoff', 15) + '''</sc-if><sc-if value="{{hideChar}}" hint-placeholder-val="{{false}}">''' + ic('eye', 15) + '''</sc-if>{{charBtn}}</button>
</div>
<sc-if value="{{askRd}}" hint-placeholder-val="{{true}}">''' + answer_block('rd') + '''</sc-if>
<sc-if value="{{askMn}}" hint-placeholder-val="{{true}}">''' + answer_block('mn') + '''</sc-if>
</section>

<section aria-label="Área de escrita" class="{{shakeCls}}" style="''' + CARD + '''border-radius:24px;padding:20px 22px 22px;display:flex;flex-direction:column;gap:16px;align-items:center;">
<div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
<div style="display:flex;align-items:center;gap:10px;"><h2 style="margin:0;font-size:17px;font-weight:700;">Área de escrita</h2><span style="font-size:13px;color:#5E5850;background:#F7F4EE;padding:5px 11px;border-radius:999px;">Traços: {{count}} / {{t.n}}</span></div>
''' + toggles() + '''
</div>
''' + canvas_area(540) + '''
<sc-if value="{{warnOn}}" hint-placeholder-val="{{false}}"><p role="alert" style="margin:0;width:100%;font-size:14px;color:''' + ACC + ''';">Escreva o caractere antes de clicar em Pronto.</p></sc-if>
''' + draw_controls() + '''
</section>

<aside aria-label="Resultado" style="''' + CARD + '''border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:16px;min-height:700px;">
<sc-if value="{{noResult}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:18px;">
<h2 style="margin:0;font-size:17px;font-weight:700;">Resultado</h2>
<div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px;padding:28px 8px 16px;">
<span style="width:80px;height:80px;border-radius:999px;background:#F7F4EE;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic('brush', 34, 1.6) + '''</span>
<p style="margin:0;font-size:16px;font-weight:500;line-height:1.4;">Escreva o caractere e clique em <strong>Pronto</strong></p>
<p style="margin:0;font-size:14px;color:#726B61;line-height:1.55;">O Kaku compara seu desenho com o caractere e mostra o que reconheceu.</p>
</div>
<div style="display:flex;flex-direction:column;gap:10px;padding:16px;border-radius:16px;background:#F7F4EE;">
<h3 style="''' + LBL + '''">Dicas</h3>
<p style="margin:0;display:flex;gap:10px;font-size:14px;line-height:1.5;"><span style="color:''' + ACC + ''';font-weight:700;">1</span>De cima para baixo, da esquerda para a direita.</p>
<p style="margin:0;display:flex;gap:10px;font-size:14px;line-height:1.5;"><span style="color:''' + ACC + ''';font-weight:700;">2</span>Use o número de traços indicado.</p>
<p style="margin:0;display:flex;gap:10px;font-size:14px;line-height:1.5;"><span style="color:''' + ACC + ''';font-weight:700;">3</span>“Contorno” mostra o caractere por baixo do quadro.</p>
</div>
<sc-if value="{{hasUpcoming}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:10px;"><h3 style="''' + LBL + '''">A seguir</h3><div style="display:flex;gap:8px;flex-wrap:wrap;"><sc-for list="{{upcoming}}" as="q" hint-placeholder-count="5"><span class="jp" style="width:44px;height:44px;border-radius:12px;border:1px solid #E6E0D6;display:flex;align-items:center;justify-content:center;font-size:22px;color:#5E5850;">{{q.c}}</span></sc-for></div></div></sc-if>
<sc-if value="{{unsaved}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:13px;color:#7A5210;background:#F4EAD6;padding:10px 12px;border-radius:12px;line-height:1.45;">Você está praticando sem conta: o resultado não será salvo no seu histórico.</p></sc-if>
</div>
</sc-if>
<sc-if value="{{hasResult}}" hint-placeholder-val="{{false}}">
<div class="rise" style="display:flex;flex-direction:column;gap:16px;">
''' + verdict_banner() + '''
<div style="display:flex;gap:14px;align-items:center;">
''' + glyph_tile(88, 'rid.gsS') + '''{{rid.c}}</span>
<div style="display:flex;flex-direction:column;gap:4px;min-width:0;">
<span style="''' + LBL + '''font-size:11px;">Caractere identificado</span>
<sc-if value="{{hasRid}}" hint-placeholder-val="{{true}}"><span class="jp" style="font-size:15px;font-weight:600;">{{rid.r}}</span><span style="font-size:13px;color:#5E5850;">{{rid.ro}}</span><span style="font-size:14px;">{{rid.pt}}</span></sc-if>
<sc-if value="{{noRid}}" hint-placeholder-val="{{false}}"><span style="font-size:14px;color:#5E5850;line-height:1.45;">Não reconhecemos o desenho como nenhum caractere.</span></sc-if>
</div>
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;">
<figure style="margin:0;display:flex;flex-direction:column;gap:6px;">
<div style="position:relative;width:148px;height:148px;border-radius:12px;border:1px solid #E6E0D6;background:#FFFEFB;overflow:hidden;">''' + grid_svg(148) + '''<img src="{{r.img}}" alt="Seu desenho" style="position:absolute;left:0;top:0;width:148px;height:148px;"></div>
<figcaption style="font-size:12px;color:#726B61;">Seu desenho</figcaption>
</figure>
<figure style="margin:0;display:flex;flex-direction:column;gap:6px;">
<div style="position:relative;width:148px;height:148px;border-radius:12px;border:1px solid #E6E0D6;background:#FFFEFB;overflow:hidden;display:flex;align-items:center;justify-content:center;">''' + grid_svg(148) + '''<span class="jp" style="position:relative;font-size:{{t.gsM}};line-height:1;">{{t.c}}</span></div>
<figcaption style="font-size:12px;color:#726B61;">Modelo · {{t.c}}</figcaption>
</figure>
</div>
<div style="display:flex;flex-direction:column;gap:8px;">
<div style="display:flex;justify-content:space-between;font-size:14px;"><span style="color:#5E5850;">Semelhança da forma</span><strong>{{r.sim}}%</strong></div>
<div style="height:8px;border-radius:999px;background:#EFEAE1;overflow:hidden;"><div style="height:8px;border-radius:999px;width:{{simW}};background-color:{{v.fg}};transition:width .6s ease;"></div></div>
<div style="display:flex;justify-content:space-between;font-size:14px;"><span style="color:#5E5850;">Número de traços</span><strong>{{r.user}} / {{r.exp}}</strong></div>
</div>
''' + final_box() + '''
<button class="btn soft" onClick="{{clear}}" style="height:46px;font-size:15px;''' + BTN_O + '''">''' + ic('replay', 18) + '''Tentar de novo</button>
</div>
</sc-if>
</aside>
</div>
</main>
</sc-if>'''

summary_d = '''<sc-if value="{{vSummary}}" hint-placeholder-val="{{false}}">
<main class="rise" style="display:flex;justify-content:center;padding:40px 64px 48px;">
<section aria-labelledby="resumo" style="''' + CARD + '''width:980px;border-radius:28px;padding:36px;display:flex;flex-direction:column;gap:26px;">
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;">
<div style="display:flex;flex-direction:column;gap:6px;"><span style="font-size:14px;color:#726B61;">Resumo da sessão · {{sLabel}}</span><h1 id="resumo" class="disp" style="margin:0;font-size:40px;font-weight:700;">{{sHead}}</h1></div>
<span class="disp" style="font-size:56px;font-weight:700;color:''' + ACC + ''';line-height:1;">{{sRate}}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;">
<div style="padding:16px;border-radius:16px;background:#F7F4EE;display:flex;flex-direction:column;gap:4px;"><span style="font-size:13px;color:#5E5850;">Praticados</span><strong class="disp" style="font-size:30px;">{{sN}}</strong></div>
<div style="padding:16px;border-radius:16px;background:#E7EEDF;display:flex;flex-direction:column;gap:4px;"><span style="font-size:13px;color:#4E6E3A;">Acertos</span><strong class="disp" style="font-size:30px;color:#3F5A2F;">{{sOk}}</strong></div>
<div style="padding:16px;border-radius:16px;background:#F8E4E0;display:flex;flex-direction:column;gap:4px;"><span style="font-size:13px;color:#A8292A;">Erros</span><strong class="disp" style="font-size:30px;color:#8E2324;">{{sFail}}</strong></div>
<div style="padding:16px;border-radius:16px;background:#F7F4EE;display:flex;flex-direction:column;gap:4px;"><span style="font-size:13px;color:#5E5850;">Taxa de acerto</span><strong class="disp" style="font-size:30px;">{{sRate}}</strong></div>
<div style="padding:16px;border-radius:16px;background:#F7F4EE;display:flex;flex-direction:column;gap:4px;"><span style="font-size:13px;color:#5E5850;">Tempo</span><strong class="disp" style="font-size:30px;">{{sTime}}</strong></div>
</div>
<div style="height:12px;border-radius:999px;background:#F1C7C0;overflow:hidden;" aria-hidden="true"><div style="height:12px;width:{{barOk}};background:#6E8F58;border-radius:999px;"></div></div>
<div style="display:flex;flex-direction:column;gap:12px;">
<h2 style="''' + LBL + '''">Caracteres desta sessão</h2>
<div style="display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:8px;">
<sc-for list="{{results}}" as="x" hint-placeholder-count="10"><div style="position:relative;display:flex;flex-direction:column;align-items:center;gap:2px;padding:10px 4px 8px;border-radius:14px;border:1px solid {{x.bd}};background-color:{{x.bg}};min-width:0;">
<span class="jp" style="font-size:28px;line-height:1.1;">{{x.c}}</span><span style="font-size:11px;color:#5E5850;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{x.sub}}</span>
<sc-if value="{{x.ok}}" hint-placeholder-val="{{true}}"><span aria-label="acerto" style="position:absolute;top:4px;right:4px;display:flex;color:#4E6E3A;">''' + ic('check', 14, 2.6) + '''</span></sc-if>
<sc-if value="{{x.no}}" hint-placeholder-val="{{false}}"><span aria-label="erro" style="position:absolute;top:4px;right:4px;display:flex;color:#A8292A;">''' + ic('x', 14, 2.6) + '''</span></sc-if>
</div></sc-for>
</div>
</div>
<sc-if value="{{unsaved}}" hint-placeholder-val="{{false}}">''' + login_prompt('Esta sessão não foi salva', 'Entre ou crie uma conta para guardar o histórico e ver sua evolução no Progresso.') + '''</sc-if>
<div style="display:flex;gap:12px;flex-wrap:wrap;">
<sc-if value="{{hasWrong}}" hint-placeholder-val="{{true}}"><button class="btn" onClick="{{retryWrong}}" style="height:52px;padding:0 24px;font-size:15px;''' + BTN_R + '''">''' + ic('target', 18) + '''{{wrongLabel}}</button></sc-if>
<button class="btn soft" onClick="{{again}}" style="height:52px;padding:0 22px;font-size:15px;''' + BTN_O + '''">''' + ic('replay', 18) + '''Repetir sessão</button>
<button class="btn soft" onClick="{{newSession}}" style="height:52px;padding:0 22px;font-size:15px;''' + BTN_O + '''">''' + ic('plus', 18, 2) + '''Nova sessão</button>
<span style="flex-grow:1;"></span>
<sc-if value="{{saved}}" hint-placeholder-val="{{true}}"><a href="Progresso.dc.html" style="align-self:center;font-size:15px;font-weight:700;text-decoration:none;display:flex;align-items:center;gap:6px;">Ver progresso''' + ic('arrow', 16, 2) + '''</a></sc-if>
</div>
</section>
</main>
</sc-if>'''

body_d = ('<div style="width:1440px;height:1100px;box-sizing:border-box;background:#F7F4EE;display:flex;flex-direction:column;overflow:hidden;">\n'
          + nav('praticar') + '''
<sc-if value="{{loading}}" hint-placeholder-val="{{false}}"><p style="margin:80px 0;text-align:center;color:#726B61;">Carregando caracteres…</p></sc-if>
''' + setup_d + session_d + summary_d + '\n</div>')

# ======================= CELULAR =======================
MROOT = 'width:390px;height:844px;box-sizing:border-box;background:#F7F4EE;position:relative;overflow:hidden;'
from b_mobile_common import mheader, tabbar_m

setup_m = '''<sc-if value="{{vSetup}}" hint-placeholder-val="{{true}}">
<main style="position:absolute;left:0;top:72px;width:390px;height:692px;box-sizing:border-box;padding:4px 20px 24px;overflow-y:auto;scrollbar-width:none;display:flex;flex-direction:column;gap:18px;">
''' + mode_tabs('escrita', True) + seg('srcs', 36) + '''
<sc-if value="{{srcFilters}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:14px;">
<div style="display:flex;flex-direction:column;gap:8px;"><h2 style="''' + LBL + '''">Sistema de escrita</h2>
<div style="display:flex;gap:6px;flex-wrap:wrap;"><button class="btn" onClick="{{pickAll}}" aria-pressed="{{allChip.pressed}}" style="height:38px;padding:0 14px;border-radius:999px;border:1px solid {{allChip.bd}};background-color:{{allChip.bg}};color:{{allChip.fg}};font-size:14px;cursor:pointer;">Todos</button>''' + chips('cats', 'height:38px;padding:0 12px;') + '''</div></div>
<div style="display:flex;flex-direction:column;gap:8px;"><h2 style="''' + LBL + '''">JLPT (kanji)</h2><div style="display:flex;gap:6px;flex-wrap:wrap;">''' + chips('jlpts', 'height:38px;padding:0 12px;') + '''</div></div>
<sc-if value="{{jlptNote}}" hint-placeholder-val="{{false}}"><p role="note" style="margin:0;font-size:13px;color:#7A5210;background:#F4EAD6;padding:10px 12px;border-radius:12px;">O nível JLPT só se aplica a kanji. Marque também “Kanji”.</p></sc-if>
</div>
</sc-if>
<sc-if value="{{srcList}}" hint-placeholder-val="{{false}}">
<div style="display:flex;flex-direction:column;gap:10px;">
<sc-if value="{{guest}}" hint-placeholder-val="{{false}}">''' + login_prompt('Entre para usar suas listas', 'As listas ficam salvas na sua conta.') + '''</sc-if>
<sc-if value="{{noListsU}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;color:#5E5850;">Você ainda não tem listas. Crie uma na versão para computador ou no detalhe de um caractere.</p></sc-if>
<sc-for list="{{lists}}" as="l" hint-placeholder-count="2"><button role="radio" aria-checked="{{l.pressed}}" onClick="{{l.pick}}" style="display:flex;flex-direction:column;gap:4px;align-items:flex-start;text-align:left;padding:12px 14px;border-radius:14px;border:1px solid {{l.bd}};background-color:{{l.bg}};cursor:pointer;color:#1F1C18;">
<strong style="font-size:15px;">{{l.name}}</strong><span style="font-size:13px;color:#726B61;">{{l.count}} · <span class="jp">{{l.preview}}</span></span></button></sc-for>
</div>
</sc-if>
<div style="display:flex;flex-direction:column;gap:2px;padding:12px 14px;border-radius:14px;background:#FFFFFF;border:1px solid #E6E0D6;"><strong style="font-size:15px;">{{poolLabel}}</strong><span style="font-size:13px;color:#5E5850;">{{poolCount}} {{poolWord}}</span></div>
<div style="display:flex;flex-direction:column;gap:8px;"><h2 style="''' + LBL + '''">Quantidade</h2>''' + seg('sizes', 34) + '''</div>
<div style="display:flex;flex-direction:column;gap:8px;"><h2 style="''' + LBL + '''">Como praticar</h2>
<div role="radiogroup" aria-label="Como praticar" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;"><sc-for list="{{modes}}" as="m" hint-placeholder-count="2"><button role="radio" aria-checked="{{m.pressed}}" onClick="{{m.pick}}" style="display:flex;flex-direction:column;gap:2px;align-items:flex-start;text-align:left;padding:12px;border-radius:14px;border:1px solid {{m.ring}};background-color:{{m.rbg}};cursor:pointer;color:#1F1C18;"><strong style="font-size:14px;">{{m.label}}</strong><span style="font-size:12px;color:#5E5850;">{{m.sub}}</span></button></sc-for></div></div>
<button role="switch" aria-checked="{{prioAttr}}" onClick="{{togglePrio}}" style="display:flex;align-items:center;gap:12px;padding:0;border:none;background:transparent;cursor:pointer;text-align:left;color:#1F1C18;">
<span aria-hidden="true" style="position:relative;width:46px;height:26px;flex-shrink:0;border-radius:999px;background-color:{{prioBg}};"><span style="position:absolute;top:2px;left:{{prioX}};width:22px;height:22px;border-radius:999px;background:#FFFFFF;box-shadow:0 1px 3px rgba(0,0,0,.2);"></span></span>
<span style="font-size:14px;">Priorizar os que mais errei<sc-if value="{{guest}}" hint-placeholder-val="{{false}}"><span style="display:block;font-size:12px;color:#726B61;">Disponível ao entrar</span></sc-if></span></button>
<sc-if value="{{canStart}}" hint-placeholder-val="{{true}}"><button class="btn" onClick="{{start}}" style="flex-shrink:0;height:54px;font-size:16px;''' + BTN_R + '''">''' + ic('brush', 20) + '''{{startLabel}}</button></sc-if>
<sc-if value="{{poolEmpty}}" hint-placeholder-val="{{false}}"><button disabled style="flex-shrink:0;height:54px;font-size:16px;border-radius:14px;border:none;background:#E6E0D6;color:#726B61;font-weight:700;">Escolha o que praticar</button></sc-if>
</main>
</sc-if>'''

session_m = '''<sc-if value="{{vSession}}" hint-placeholder-val="{{false}}">
<main style="position:absolute;left:0;top:72px;width:390px;height:692px;box-sizing:border-box;padding:0 24px 16px;overflow-y:auto;scrollbar-width:none;display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;align-items:center;gap:10px;">
<strong style="font-size:15px;white-space:nowrap;">{{numLabel}}</strong>
<div role="progressbar" aria-label="Progresso da sessão" aria-valuetext="{{numLabel}}" style="flex-grow:1;height:8px;border-radius:999px;background:#E6E0D6;overflow:hidden;"><div style="height:8px;border-radius:999px;width:{{progW}};background-color:''' + ACC + ''';"></div></div>
<button class="btn soft" onClick="{{endSession}}" aria-label="Encerrar sessão" style="width:40px;height:40px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('x', 18, 2) + '''</button>
</div>
<div style="display:flex;gap:14px;align-items:center;padding:12px;border-radius:18px;background:#FFFFFF;border:1px solid #E6E0D6;">
<div style="width:76px;height:76px;flex-shrink:0;border-radius:12px;background:#F7F4EE;display:flex;align-items:center;justify-content:center;">
<sc-if value="{{showChar}}" hint-placeholder-val="{{true}}"><span class="jp fade" style="font-size:{{t.gsS}};line-height:1;">{{t.c}}</span></sc-if>
<sc-if value="{{hideChar}}" hint-placeholder-val="{{false}}"><span class="disp" style="font-size:30px;color:#C9C1B5;">?</span></sc-if>
</div>
<div style="display:flex;flex-direction:column;gap:2px;flex-grow:1;min-width:0;">
<sc-if value="{{memPrompt}}" hint-placeholder-val="{{false}}"><span style="font-size:12px;color:#5E5850;">{{lead}}</span><span class="disp" style="font-size:20px;font-weight:700;line-height:1.2;">{{main}}</span></sc-if>
<sc-if value="{{copyPrompt}}" hint-placeholder-val="{{true}}"><span style="font-size:12px;color:#5E5850;">{{t.tl}} · {{t.n}} traços</span><span style="font-size:15px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{t.pt}}</span></sc-if>
</div>
<button class="btn soft" onClick="{{toggleChar}}" aria-label="{{charBtn}}" style="width:44px;height:44px;flex-shrink:0;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;"><sc-if value="{{showChar}}" hint-placeholder-val="{{true}}">''' + ic('eyeoff', 20) + '''</sc-if><sc-if value="{{hideChar}}" hint-placeholder-val="{{false}}">''' + ic('eye', 20) + '''</sc-if></button>
</div>
<section aria-label="Área de escrita" class="{{shakeCls}}" style="display:flex;flex-direction:column;gap:8px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><span style="font-size:13px;color:#5E5850;">Traços: {{count}} / {{t.n}}</span>''' + toggles(32) + '''</div>
''' + canvas_area(342) + '''
</section>
<sc-if value="{{warnOn}}" hint-placeholder-val="{{false}}"><p role="alert" style="margin:0;font-size:13px;color:''' + ACC + ''';">Escreva o caractere antes de clicar em Pronto.</p></sc-if>
''' + draw_controls().replace('padding:0 34px', 'padding:0 20px;flex-grow:1').replace('padding:0 30px', 'padding:0 20px;flex-grow:1').replace('height:52px;padding:0 20px;font-size:15px', 'height:52px;padding:0 14px;font-size:15px') + '''
<sc-if value="{{askRd}}" hint-placeholder-val="{{true}}"><div style="padding:0 2px;">''' + answer_block('rd') + '''</div></sc-if>
<sc-if value="{{askMn}}" hint-placeholder-val="{{true}}"><div style="padding:0 2px;">''' + answer_block('mn') + '''</div></sc-if>
</main>
<sc-if value="{{hasResult}}" hint-placeholder-val="{{false}}">
<div class="fade" aria-hidden="true" style="position:absolute;left:0;top:0;width:390px;height:844px;background:rgba(31,28,24,.32);"></div>
<section aria-label="Resultado" class="sheet" style="position:absolute;left:0;bottom:0;width:390px;box-sizing:border-box;padding:12px 22px 26px;background:#FFFFFF;border-radius:28px 28px 0 0;box-shadow:0 -12px 40px -12px rgba(31,28,24,.3);display:flex;flex-direction:column;gap:14px;">
<div aria-hidden="true" style="width:40px;height:4px;border-radius:999px;background:#E0D9CD;align-self:center;"></div>
''' + verdict_banner() + '''
<div style="display:flex;gap:12px;align-items:center;padding:12px;border-radius:16px;background:#F7F4EE;">
<div style="position:relative;width:64px;height:64px;flex-shrink:0;border-radius:10px;background:#FFFFFF;border:1px solid #E6E0D6;overflow:hidden;"><img src="{{r.img}}" alt="Seu desenho" style="width:64px;height:64px;"></div>
<span class="jp" style="width:64px;height:64px;flex-shrink:0;border-radius:10px;background:#FFFFFF;border:1px solid #E6E0D6;display:flex;align-items:center;justify-content:center;font-size:44px;line-height:1;">{{t.c}}</span>
<div style="display:flex;flex-direction:column;gap:4px;flex-grow:1;min-width:0;">
<div style="display:flex;justify-content:space-between;font-size:13px;"><span style="color:#5E5850;">Semelhança</span><strong>{{r.sim}}%</strong></div>
<div style="height:6px;border-radius:999px;background:#E6E0D6;overflow:hidden;"><div style="height:6px;border-radius:999px;width:{{simW}};background-color:{{v.fg}};"></div></div>
<div style="display:flex;justify-content:space-between;font-size:13px;"><span style="color:#5E5850;">Traços</span><strong>{{r.user}} / {{r.exp}}</strong></div>
</div>
</div>
<div style="display:flex;flex-direction:column;gap:2px;"><span class="jp" style="font-size:16px;font-weight:600;">{{t.r}}</span><span style="font-size:13px;color:#5E5850;">{{t.ro}} · {{t.pt}}</span></div>
''' + final_box() + '''
<div style="display:flex;gap:10px;">
<button class="btn soft" onClick="{{clear}}" style="flex-grow:1;height:50px;font-size:15px;''' + BTN_O + '''">''' + ic('replay', 18) + '''Tentar de novo</button>
<button class="btn" onClick="{{next}}" style="flex-grow:1;height:50px;font-size:15px;''' + BTN_R + '''">{{nextLabel}}''' + ic('arrow', 18, 2) + '''</button>
</div>
</section>
</sc-if>
</sc-if>'''

summary_m = '''<sc-if value="{{vSummary}}" hint-placeholder-val="{{false}}">
<main class="rise" style="position:absolute;left:0;top:72px;width:390px;height:692px;box-sizing:border-box;padding:4px 20px 24px;overflow-y:auto;scrollbar-width:none;display:flex;flex-direction:column;gap:16px;">
<div style="display:flex;justify-content:space-between;align-items:flex-end;"><div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:13px;color:#726B61;">{{sLabel}}</span><h2 class="disp" style="margin:0;font-size:26px;font-weight:700;">{{sHead}}</h2></div><span class="disp" style="font-size:38px;font-weight:700;color:''' + ACC + ''';line-height:1;">{{sRate}}</span></div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;">
<div style="padding:12px;border-radius:14px;background:#FFFFFF;border:1px solid #E6E0D6;display:flex;flex-direction:column;gap:2px;"><span style="font-size:12px;color:#5E5850;">Praticados</span><strong class="disp" style="font-size:24px;">{{sN}}</strong></div>
<div style="padding:12px;border-radius:14px;background:#E7EEDF;display:flex;flex-direction:column;gap:2px;"><span style="font-size:12px;color:#4E6E3A;">Acertos</span><strong class="disp" style="font-size:24px;color:#3F5A2F;">{{sOk}}</strong></div>
<div style="padding:12px;border-radius:14px;background:#F8E4E0;display:flex;flex-direction:column;gap:2px;"><span style="font-size:12px;color:#A8292A;">Erros</span><strong class="disp" style="font-size:24px;color:#8E2324;">{{sFail}}</strong></div>
</div>
<span style="font-size:13px;color:#5E5850;">Tempo de estudo: {{sTime}}</span>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;">
<sc-for list="{{results}}" as="x" hint-placeholder-count="10"><div style="position:relative;display:flex;align-items:center;justify-content:center;height:56px;border-radius:12px;border:1px solid {{x.bd}};background-color:{{x.bg}};">
<span class="jp" style="font-size:24px;">{{x.c}}</span>
<sc-if value="{{x.ok}}" hint-placeholder-val="{{true}}"><span aria-label="acerto" style="position:absolute;top:3px;right:3px;display:flex;color:#4E6E3A;">''' + ic('check', 12, 2.6) + '''</span></sc-if>
<sc-if value="{{x.no}}" hint-placeholder-val="{{false}}"><span aria-label="erro" style="position:absolute;top:3px;right:3px;display:flex;color:#A8292A;">''' + ic('x', 12, 2.6) + '''</span></sc-if>
</div></sc-for>
</div>
<sc-if value="{{unsaved}}" hint-placeholder-val="{{false}}">''' + login_prompt('Esta sessão não foi salva', 'Entre para guardar seu histórico.') + '''</sc-if>
<sc-if value="{{hasWrong}}" hint-placeholder-val="{{true}}"><button class="btn" onClick="{{retryWrong}}" style="flex-shrink:0;height:50px;font-size:15px;''' + BTN_R + '''">{{wrongLabel}}</button></sc-if>
<div style="display:flex;gap:8px;">
<button class="btn soft" onClick="{{again}}" style="flex-grow:1;height:48px;font-size:14px;''' + BTN_O + '''">Repetir</button>
<button class="btn soft" onClick="{{newSession}}" style="flex-grow:1;height:48px;font-size:14px;''' + BTN_O + '''">Nova sessão</button>
</div>
</main>
</sc-if>'''

body_m = ('<div style="' + MROOT + '">\n' + mheader('Praticar') + tabbar_m('praticar') + '''
<sc-if value="{{loading}}" hint-placeholder-val="{{false}}"><p style="margin:80px 0;text-align:center;color:#726B61;">Carregando…</p></sc-if>
''' + setup_m + session_m + summary_m + '\n</div>')

if __name__ == '__main__':
    open('project/Praticar.dc.html', 'w').write(page('Kaku — Praticar', 'pt-BR', body_d, practice_script(540, 'Praticar.dc.html'), 1440, 1100, DATA_HEAD))
    open('project/PraticarMobile.dc.html', 'w').write(page('Kaku — Praticar (celular)', 'pt-BR', body_m, practice_script(342, 'PraticarMobile.dc.html'), 390, 844, DATA_HEAD))
