"""Versões de celular (390 × 844) das páginas que só existiam no desktop.
Usam exatamente a mesma lógica (scripts) das páginas desktop — nenhuma funcionalidade é removida."""
from common import *
from ds import c
from ui import T, CARD, btn, INPUT, INPUT_BLOCK, badge, alert, OVERLINE
from b_chars import DBJS, DATA_HEAD, glyph_box, BACK_BTN, detail_block
from b_mobile_common import mheader, tabbar_m
from b_listpick import list_picker
from b_practice import login_prompt
import b_pages, b_progress, b_auth, b_lists, b_kanji
from b_comp import comp_section

MROOT = 'width:390px;height:844px;box-sizing:border-box;background:' + c('background') + ';position:relative;overflow:hidden;'
def screen(title, inner, tab, gap=16, header_right=None):
    return ('<div style="' + MROOT + '">\n' + mheader(title, header_right) + tabbar_m(tab)
            + '<main style="position:absolute;left:0;top:72px;width:390px;height:692px;box-sizing:border-box;padding:0 20px 24px;overflow-y:auto;scrollbar-width:none;display:flex;flex-direction:column;gap:%dpx;">' % gap
            + inner + '</main>\n</div>')

def hscroll(inner):
    return '<div style="display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:0 -20px;padding:0 20px;flex-shrink:0;">' + inner + '</div>'

def segm(lst, var='f'):
    return ('<div role="group" style="display:flex;gap:4px;padding:4px;background:' + c('border') + ';border-radius:9999px;flex-shrink:0;">'
            '<sc-for list="{{' + lst + '}}" as="' + var + '" hint-placeholder-count="3"><button onClick="{{' + var + '.pick}}" aria-pressed="{{' + var + '.pressed}}" style="height:36px;padding:0 14px;border:none;border-radius:9999px;background-color:{{' + var + '.bg}};color:{{' + var + '.fg}};font-weight:{{' + var + '.fw}};box-shadow:{{' + var + '.sh}};font-size:14px;cursor:pointer;white-space:nowrap;">{{' + var + '.label}}</button></sc-for></div>')

SELECT = 'width:100%;height:44px;padding:0 12px;border-radius:8px;border:1px solid ' + c('border-strong') + ';background:#ffffff;font-size:16px;color:' + c('text-primary') + ';'

# =============================================================== Início
main_m = screen('Kaku', '''
<section style="display:flex;flex-direction:column;gap:16px;padding-top:8px;">
<span style="''' + badge('primary') + '''align-self:flex-start;"><span class="jp">書く</span>kaku · escrever</span>
<h2 style="''' + T['h2'] + '''">Aprenda a escrever japonês, traço a traço.</h2>
<p style="''' + T['body'] + '''">Explore Hiragana, Katakana e Kanji, pratique à mão livre no quadro e receba feedback imediato sobre cada caractere que você escreve.</p>
<div style="display:flex;flex-direction:column;gap:8px;">
<a href="Praticar.dc.html" class="btn" style="''' + btn('primary', 'lg') + '''">''' + ic('brush', 20) + '''Começar a praticar</a>
<a href="Caracteres.dc.html" class="btn soft" style="''' + btn('outline', 'lg') + '''">''' + ic('grid', 20) + '''Explorar caracteres</a>
</div>
</section>
<section style="''' + CARD + '''padding:20px;display:flex;flex-direction:column;gap:16px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><span style="''' + OVERLINE + '''">Caractere do dia</span><span style="''' + badge('primary') + '''">Kanji</span></div>
<div style="display:flex;justify-content:center;padding:16px 0;background:''' + c('background-subtle') + ''';border-radius:12px;border:1px solid ''' + c('border') + ''';">''' + anim_pair(200) + '''</div>
<div style="display:flex;align-items:flex-end;justify-content:space-between;">
<div style="display:flex;flex-direction:column;gap:4px;"><span style="display:flex;align-items:baseline;gap:8px;"><span class="jp" style="font-size:24px;font-weight:600;">やま</span><span style="''' + T['small'] + '''">yama</span></span><span style="''' + T['small'] + '''">montanha · mountain</span></div>
<div style="display:flex;gap:8px;">
<button class="btn soft" onClick="{{replay}}" aria-label="Repetir animação da escrita" style="''' + btn('outline') + '''width:44px;height:44px;">''' + ic('replay', 20) + '''</button>
<button class="btn soft" onClick="{{speak}}" aria-label="Ouvir pronúncia" style="''' + btn('outline') + '''width:44px;height:44px;">''' + ic('speaker', 20) + '''</button>
</div></div>
<a href="Praticar.dc.html" onClick="{{practiceYama}}" class="btn" style="''' + btn('secondary', 'md') + '''">Praticar 山 agora''' + ic('arrow', 18, 2) + '''</a>
</section>
<section style="display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><h2 style="''' + T['h3'] + '''">{{contTitle}}</h2><a href="Progresso.dc.html" style="font-size:14px;font-weight:700;text-decoration:none;">Ver progresso</a></div>
''' + b_pages.script_card('あ', 'Hiragana', '#E3EAF2', '#2E4C6E', 'hiragana', 'Silabário fonético') + b_pages.script_card('ア', 'Katakana', '#F4EAD6', '#7A5210', 'katakana', 'Palavras estrangeiras') + b_pages.script_card('字', 'Kanji', '#F8E4E0', '#A8292A', 'kanji', 'Os 2.136 de uso comum') + '''
</section>
<section style="display:flex;flex-direction:column;gap:12px;">
<h2 style="''' + T['h3'] + '''">Como funciona</h2>
''' + b_pages.step('一', 'book', 'Explore', 'Conheça cada caractere: leitura, romaji, significado em português e inglês e a ordem correta dos traços.') + b_pages.step('二', 'brush', 'Pratique', 'Escreva no quadro com o dedo. Ao tocar em Pronto, o Kaku identifica o caractere e compara com o exercício.') + b_pages.step('三', 'chart', 'Acompanhe', 'Veja sua sequência de estudos, a precisão por caractere e o que vale revisar na próxima sessão.') + '''
</section>
<p style="''' + T['caption'] + '''text-align:center;padding-top:8px;">Kaku · 書く — feito para quem está aprendendo a escrever em japonês.</p>
''', 'inicio', 24)

# =============================================================== Kanji
S = comp_section(56, full=True)
kanji_list = '''
<sc-if value="{{mList}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:12px;">
<a href="Caracteres.dc.html" style="font-size:14px;text-decoration:none;display:flex;align-items:center;gap:4px;">''' + ic('back', 16) + '''Caracteres</a>
<label style="position:relative;display:flex;align-items:center;"><span style="position:absolute;left:12px;display:flex;color:''' + c('text-muted') + ''';">''' + ic('search', 18) + '''</span><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Pesquisar kanji</span>
<input type="search" value="{{query}}" onChange="{{onQuery}}" placeholder="{{placeholder}}" style="''' + INPUT_BLOCK + '''padding-left:40px;"></label>
''' + hscroll(segm('modes')) + hscroll(segm('jlpts')) + '''
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;">
<label style="display:flex;flex-direction:column;gap:4px;''' + T['label'] + '''font-size:12px;">Radical<select value="{{rad}}" onChange="{{onRad}}" style="''' + SELECT + '''"><sc-for list="{{radOpts}}" as="o" hint-placeholder-count="5"><option value="{{o.v}}">{{o.label}}</option></sc-for></select></label>
<label style="display:flex;flex-direction:column;gap:4px;''' + T['label'] + '''font-size:12px;">Traços<select value="{{strokes}}" onChange="{{onStrokes}}" style="''' + SELECT + '''"><sc-for list="{{strokeOpts}}" as="o" hint-placeholder-count="5"><option value="{{o.v}}">{{o.label}}</option></sc-for></select></label>
</div>
<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
<sc-if value="{{hasComp}}" hint-placeholder-val="{{false}}"><span style="display:flex;align-items:center;gap:8px;height:36px;padding:0 4px 0 12px;border-radius:9999px;background:''' + c('secondary') + ''';color:#ffffff;font-size:14px;">Componente <span class="jp">{{comp}}</span><button onClick="{{clearComp}}" aria-label="Remover filtro de componente" style="width:28px;height:28px;border:none;border-radius:9999px;background:rgb(255 255 255 / 0.15);color:#ffffff;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('x', 14, 2.4) + '''</button></span></sc-if>
<sc-if value="{{anyFilter}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{clearFilters}}" style="''' + btn('ghost', 'sm') + '''color:''' + ACC + ''';">Limpar filtros</button></sc-if>
<span role="status" style="''' + T['caption'] + '''margin-left:auto;">{{shown}} de {{total}} kanji</span>
</div>
<sc-if value="{{hasBanner}}" hint-placeholder-val="{{false}}"><div style="display:flex;align-items:center;gap:12px;padding:12px;border-radius:12px;background:#ffffff;border:1px solid ''' + c('border') + ''';"><span class="jp" style="width:44px;height:44px;flex-shrink:0;border-radius:8px;background:''' + c('accent-subtle') + ''';display:flex;align-items:center;justify-content:center;font-size:24px;">{{banner.c}}</span><div style="display:flex;flex-direction:column;gap:2px;min-width:0;"><strong style="''' + T['label'] + '''">{{banner.title}}</strong><span style="''' + T['caption'] + '''">{{banner.sub}}</span></div></div></sc-if>
<sc-if value="{{loading}}" hint-placeholder-val="{{false}}"><p style="''' + T['small'] + '''">Carregando kanji…</p></sc-if>
<sc-if value="{{empty}}" hint-placeholder-val="{{false}}"><p style="''' + T['small'] + '''text-align:center;padding:24px;border:1px dashed ''' + c('border-strong') + ''';border-radius:12px;">Nenhum kanji encontrado.</p></sc-if>
<sc-for list="{{groups}}" as="g" hint-placeholder-count="2">
<div style="display:flex;flex-direction:column;gap:8px;margin-bottom:8px;">
<h2 style="''' + OVERLINE + '''display:flex;align-items:center;gap:8px;"><span style="''' + badge('neutral') + '''background:''' + c('secondary') + ''';color:#ffffff;">{{g.level}}</span>{{g.count}} kanji</h2>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;">
<sc-for list="{{g.items}}" as="it" hint-placeholder-count="10"><button class="card" onClick="{{it.pick}}" aria-label="{{it.c}}, {{it.pt}}" style="display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 2px 6px;border-radius:8px;border:1px solid #e7e5e4;background:#ffffff;cursor:pointer;color:#1c1917;min-width:0;"><span class="jp" style="font-size:30px;line-height:1.1;">{{it.c}}</span><span style="font-size:10px;color:#57534e;width:100%;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{it.pt}}</span></button></sc-for>
</div>
<sc-if value="{{g.hasMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{g.more}}" style="''' + btn('outline', 'sm') + '''">{{g.moreLabel}}</button></sc-if>
</div>
</sc-for>
</div>
</sc-if>'''
kanji_detail = '''
<sc-if value="{{mOpen}}" hint-placeholder-val="{{false}}">
<div class="rise" style="display:flex;flex-direction:column;gap:16px;">
<button class="btn soft" onClick="{{mClose}}" style="''' + btn('ghost', 'sm') + '''align-self:flex-start;padding:0 8px;">''' + ic('back', 16) + '''Lista de kanji</button>
<sc-if value="{{ready}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:16px;">
''' + BACK_BTN + glyph_box(180) + '''
<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;"><span style="''' + badge('neutral') + '''background:''' + c('secondary') + ''';color:#ffffff;">{{d.jlpt}}</span><span style="''' + T['caption'] + '''">{{metaLine}}</span><sc-if value="{{d.essential}}" hint-placeholder-val="{{false}}"><span style="''' + badge('warning') + '''">Ficha essencial</span></sc-if></div>
<div style="display:flex;flex-direction:column;gap:2px;"><span style="''' + T['h2'] + '''">{{d.pt}}</span><span style="''' + T['body'] + '''">{{d.en}}</span></div>
''' + b_kanji.reading_rows + '''
<div style="display:flex;gap:8px;flex-wrap:wrap;">
<button class="btn soft" onClick="{{speak}}" style="''' + btn('outline', 'sm') + '''">''' + ic('speaker', 16) + '''Ouvir</button>
<sc-if value="{{hasOrder}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{replay}}" style="''' + btn('outline', 'sm') + '''">''' + ic('replay', 16) + '''Ver traços</button></sc-if>
<a href="Praticar.dc.html" onClick="{{practiceThis}}" class="btn" style="''' + btn('primary', 'sm') + '''">''' + ic('brush', 16) + '''Praticar</a>
</div>
''' + list_picker(compact=True, show_practice=False) + '''
<h2 style="''' + T['h3'] + '''">Componentes do Kanji</h2>
''' + S['decomp'] + S['formation'] + '''
<div style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:12px;">''' + S['used'] + '''
<sc-if value="{{cx.usedMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{showAllUsed}}" style="''' + btn('outline', 'sm') + '''">Ver todos na lista</button></sc-if>
<sc-if value="{{cx.hasUsed}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{filterBySelf}}" style="''' + btn('outline', 'sm') + '''">''' + ic('search', 14, 2) + '''Filtrar a lista por <span class="jp">{{d.c}}</span></button></sc-if>
</div>
<div style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:16px;">''' + S['rel'] + S['same'] + '''</div>
''' + b_kanji.examples + b_kanji.sentence_order + '''
</div>
</sc-if>
</div>
</sc-if>'''
kanji_m = screen('Kanji', kanji_list + kanji_detail, 'caracteres')

# =============================================================== Progresso
kpi_m = lambda icon, label, val, sub: ('<div style="' + CARD + 'padding:12px;display:flex;flex-direction:column;gap:4px;"><div style="display:flex;align-items:center;gap:8px;color:' + c('text-secondary') + ';"><span style="display:flex;color:' + ACC + ';">' + ic(icon, 16) + '</span><span style="font-size:12px;">' + label + '</span></div><span style="' + T['h2'] + 'font-size:24px;line-height:32px;">{{k.' + val + '}}</span><span style="' + T['caption'] + '">{{k.' + sub + '}}</span></div>')
prog_m = screen('Progresso', '''
''' + hscroll('<div role="group" aria-label="Período" style="display:flex;gap:4px;padding:4px;background:' + c('border') + ';border-radius:9999px;flex-shrink:0;"><sc-for list="{{periods}}" as="p" hint-placeholder-count="4"><button onClick="{{p.pick}}" aria-pressed="{{p.pressed}}" style="height:36px;padding:0 14px;border:none;border-radius:9999px;background-color:{{p.bg}};color:{{p.fg}};font-weight:{{p.fw}};box-shadow:{{p.sh}};font-size:14px;cursor:pointer;white-space:nowrap;">{{p.label}}</button></sc-for></div>') + '''
<p style="''' + T['small'] + '''">{{periodText}}</p>
<sc-if value="{{acct.out}}" hint-placeholder-val="{{false}}"><div style="''' + CARD + '''padding:16px;">''' + login_prompt('Entre para ver seu histórico', 'Seu progresso e suas sessões ficam salvos na sua conta.') + '''</div></sc-if>
<sc-if value="{{acct.in}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:16px;">
<sc-if value="{{noData}}" hint-placeholder-val="{{false}}"><div style="display:flex;flex-direction:column;gap:12px;padding:16px;border-radius:12px;background:#ffffff;border:1px dashed ''' + c('border-strong') + ''';"><span style="''' + T['small'] + '''">{{emptyText}}</span><div style="display:flex;gap:8px;flex-wrap:wrap;"><a href="Praticar.dc.html" class="btn" style="''' + btn('primary', 'sm') + '''">Praticar agora</a><sc-if value="{{canDemo}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{addDemo}}" style="''' + btn('outline', 'sm') + '''">Ver com dados de exemplo</button></sc-if></div></div></sc-if>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;">''' + kpi_m('grid', 'Praticados', 'n', 'nSub') + kpi_m('check', 'Acertos', 'ok', 'okSub') + kpi_m('x', 'Erros', 'fail', 'failSub') + kpi_m('target', 'Taxa de acerto', 'rate', 'rateSub') + kpi_m('clock', 'Tempo de estudo', 'time', 'timeSub') + kpi_m('history', 'Sessões', 'sessions', 'sessionsSub') + '''</div>
<section style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;"><div style="display:flex;flex-direction:column;gap:2px;"><h2 style="''' + T['h4'] + '''">Evolução</h2><span style="''' + T['caption'] + '''">{{evoSub}}</span></div>
<div style="display:flex;flex-direction:column;gap:4px;font-size:12px;"><span style="display:flex;align-items:center;gap:6px;"><span style="width:10px;height:10px;border-radius:2px;background:#16a34a;"></span>Acertos</span><span style="display:flex;align-items:center;gap:6px;"><span style="width:10px;height:10px;border-radius:2px;background:#fca5a5;"></span>Erros</span></div></div>
<div style="position:relative;height:170px;">
<span style="position:absolute;right:0;top:-4px;font-size:11px;color:''' + c('text-muted') + ''';">{{yMax}}</span>
<div role="img" aria-label="{{evoAria}}" style="position:absolute;left:0;right:0;top:12px;height:136px;display:flex;align-items:flex-end;gap:2px;border-bottom:1px solid ''' + c('border-strong') + ''';">
<sc-for list="{{series}}" as="b" hint-placeholder-count="7"><div data-tip="{{b.tip}}" style="flex-grow:1;flex-basis:0;height:136px;display:flex;flex-direction:column;justify-content:flex-end;gap:{{b.gap}};min-width:0;"><div style="height:{{b.hFailM}};background:#fca5a5;border-radius:{{b.rFail}};"></div><div style="height:{{b.hOkM}};background:#16a34a;border-radius:{{b.rOk}};"></div></div></sc-for>
</div>
<div aria-hidden="true" style="position:absolute;left:0;right:0;top:152px;display:flex;gap:2px;"><sc-for list="{{series}}" as="b" hint-placeholder-count="7"><span style="flex-grow:1;flex-basis:0;text-align:center;font-size:10px;color:{{b.lc}};font-weight:{{b.fw}};white-space:nowrap;min-width:0;overflow:visible;">{{b.label}}</span></sc-for></div>
</div>
</section>
<section style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:16px;">
<div style="display:flex;flex-direction:column;gap:2px;"><h2 style="''' + T['h4'] + '''">Caracteres estudados</h2><span style="''' + T['caption'] + '''">diferentes, no período · acertados pelo menos uma vez</span></div>
<sc-for list="{{systems}}" as="s" hint-placeholder-count="3"><div style="display:flex;align-items:center;gap:12px;"><span class="jp" style="width:40px;height:40px;flex-shrink:0;border-radius:8px;background-color:{{s.tb}};color:{{s.tf}};display:flex;align-items:center;justify-content:center;font-size:24px;">{{s.g}}</span><div style="flex-grow:1;display:flex;flex-direction:column;gap:6px;min-width:0;"><div style="display:flex;justify-content:space-between;gap:8px;font-size:14px;"><strong>{{s.name}}</strong><span style="color:''' + c('text-secondary') + ''';font-size:12px;">{{s.label}}</span></div><div aria-hidden="true" style="position:relative;height:8px;border-radius:9999px;background:''' + c('border') + ''';overflow:hidden;"><div style="position:absolute;left:0;top:0;height:8px;border-radius:9999px;width:{{s.seenW}};background:#fecaca;"></div><div style="position:absolute;left:0;top:0;height:8px;border-radius:9999px;width:{{s.okW}};background-color:''' + ACC + ''';"></div></div></div></div></sc-for>
</section>
''' + b_progress.rank('top', 'Mais praticados', 'no período', 'mtop', 'Nenhum caractere praticado neste período.').replace('padding:24px;', 'padding:16px;') + '''
''' + b_progress.rank('hard', 'Mais erros', 'no período', 'mhard', 'Nenhum erro neste período.').replace('padding:24px;', 'padding:16px;') + '''
<sc-if value="{{hasHard}}" hint-placeholder-val="{{false}}"><a href="Praticar.dc.html" onClick="{{reviewHard}}" class="btn soft" style="''' + btn('outline', 'md') + '''">''' + ic('target', 18) + '''Praticar os com mais erros</a></sc-if>
<section style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:8px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><h2 style="''' + T['h4'] + '''">Histórico de sessões</h2><span style="''' + T['caption'] + '''">{{histSub}}</span></div>
<sc-if value="{{sessEmpty}}" hint-placeholder-val="{{false}}"><p style="''' + T['small'] + '''">Nenhuma sessão neste período.</p></sc-if>
<sc-for list="{{sessions}}" as="s" hint-placeholder-count="3"><div style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 0;border-top:1px solid ''' + c('border') + ''';"><div style="display:flex;flex-direction:column;gap:2px;min-width:0;"><span style="''' + T['label'] + '''font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{s.label}}<sc-if value="{{s.demo}}" hint-placeholder-val="{{false}}"><span style="''' + badge('warning') + '''margin-left:8px;">exemplo</span></sc-if></span><span style="''' + T['caption'] + '''">{{s.when}} · {{s.n}} caract. · {{s.dur}}</span></div><strong style="''' + T['h4'] + '''">{{s.acc}}</strong></div></sc-for>
<sc-if value="{{sessMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{moreSess}}" style="''' + btn('outline', 'sm') + '''">{{sessMoreLabel}}</button></sc-if>
</section>
</div>
</sc-if>''', 'progresso')

# =============================================================== Login / Cadastro
def auth_screen(title, card_inner):
    return screen(title, '<section style="' + CARD + 'padding:20px;display:flex;flex-direction:column;gap:20px;margin-top:8px;">' + card_inner + '</section>', 'inicio')

def _auth_inner(body_desktop):
    s = body_desktop
    a = s.index('<sc-if value="{{form}}"'); b = s.rindex('</section>')
    inner = s[a:b]
    inner = inner.replace("style=\"" + T['h2'], "style=\"" + T['h2'])
    return inner.replace('font-size:34px', 'font-size:30px').replace('font-size:32px', 'font-size:30px')

login_m = auth_screen('Entrar', _auth_inner(b_auth.login_body))
signup_m = auth_screen('Criar conta', _auth_inner(b_auth.signup_body).replace('grid-template-columns:minmax(0,1fr) 150px;', 'grid-template-columns:minmax(0,1fr);'))

# =============================================================== Perfil
profile_m = screen('Perfil', '''
<sc-if value="{{acct.out}}" hint-placeholder-val="{{false}}"><div style="''' + CARD + '''padding:16px;">''' + login_prompt('Entre para ver seu perfil', 'Seu perfil reúne seus dados, estatísticas e listas.') + '''</div></sc-if>
<sc-if value="{{acct.in}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:16px;">
<section style="''' + CARD + '''padding:20px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px;">
<span aria-hidden="true" class="disp" style="width:80px;height:80px;border-radius:9999px;background-color:''' + ACC + ''';color:#ffffff;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:700;">{{acct.initials}}</span>
<h2 style="''' + T['h2'] + '''">{{acct.full}}</h2>
<dl style="margin:0;display:flex;flex-direction:column;gap:4px;''' + T['small'] + '''"><div><dt style="display:inline;">Email </dt><dd style="display:inline;margin:0;color:''' + c('text-primary') + ''';font-weight:500;">{{acct.email}}</dd></div><div><dt style="display:inline;">Idade </dt><dd style="display:inline;margin:0;color:''' + c('text-primary') + ''';font-weight:500;">{{age}}</dd></div><div><dt style="display:inline;">Membro desde </dt><dd style="display:inline;margin:0;color:''' + c('text-primary') + ''';font-weight:500;">{{since}}</dd></div></dl>
<a href="Main.dc.html" onClick="{{acct.logout}}" class="btn soft" style="''' + btn('outline', 'md') + '''color:''' + c('error') + ''';align-self:stretch;">''' + ic('logout', 18) + '''Sair</a>
</section>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;">
''' + ''.join('<div style="' + CARD + 'padding:12px;display:flex;flex-direction:column;gap:2px;"><span style="' + T['caption'] + '">' + l + '</span><strong style="' + T['h2'] + 'font-size:24px;line-height:32px;">{{' + h + '}}</strong></div>' for l, h in [('Sessões', 's.sessions'), ('Praticados', 's.n'), ('Diferentes', 's.unique'), ('Taxa de acerto', 's.rate'), ('Tempo de estudo', 's.time'), ('Sequência', 'acct.streakLabel')]) + '''
</div>
''' + ''.join('<a href="' + href + '" class="card" style="' + CARD + 'padding:16px;display:flex;align-items:center;gap:12px;text-decoration:none;color:' + c('text-primary') + ';"><span style="width:40px;height:40px;flex-shrink:0;border-radius:8px;background:' + c('accent-subtle') + ';color:' + ACC + ';display:flex;align-items:center;justify-content:center;">' + ic(icon, 20) + '</span><span style="display:flex;flex-direction:column;gap:2px;min-width:0;"><strong style="' + T['label'] + '">' + t + '</strong><span style="' + T['caption'] + '">' + sub + '</span></span></a>' for href, icon, t, sub in [('Listas.dc.html', 'list', 'Minhas listas', '{{listsLabel}}'), ('Progresso.dc.html', 'history', 'Histórico e estatísticas', 'Hoje, semana, mês ou todo o período.'), ('Praticar.dc.html', 'brush', 'Praticar', 'Hiragana, katakana, kanji ou suas listas.')]) + '''
<section style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:12px;">
<h2 style="''' + T['h4'] + '''">Dados de exemplo</h2><p style="''' + T['small'] + '''">Gere um histórico fictício de 4 meses nesta conta para experimentar os gráficos e filtros do Progresso. Ele pode ser removido quando quiser.</p>
<sc-if value="{{demoMsgOn}}" hint-placeholder-val="{{false}}"><span role="status" style="font-size:14px;font-weight:700;color:''' + c('success') + ''';">{{demoMsg}}</span></sc-if>
<sc-if value="{{noDemo}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{addDemo}}" style="''' + btn('outline', 'md') + '''">Gerar histórico de exemplo</button></sc-if>
<sc-if value="{{hasDemo}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{removeDemo}}" style="''' + btn('outline', 'md') + '''">Remover dados de exemplo</button></sc-if>
</section>
</div>
</sc-if>''', 'inicio')

# =============================================================== Minhas listas
pill_m = lambda lst: ('<sc-for list="{{' + lst + '}}" as="p" hint-placeholder-count="3"><button class="btn" onClick="{{p.pick}}" aria-pressed="{{p.pressed}}" style="height:36px;padding:0 12px;border-radius:9999px;border:1px solid {{p.bd}};background-color:{{p.bg}};color:{{p.fg}};font-size:14px;font-weight:500;cursor:pointer;white-space:nowrap;flex-shrink:0;">{{p.label}}</button></sc-for>')
lists_m = screen('Minhas listas', '''
<sc-if value="{{acct.out}}" hint-placeholder-val="{{false}}"><div style="''' + CARD + '''padding:16px;">''' + login_prompt('Entre para criar listas', 'Suas listas ficam salvas na sua conta e aparecem em Praticar e Leitura.') + '''</div></sc-if>
<sc-if value="{{ready}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:16px;">
<sc-if value="{{mList}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:16px;">
<form onSubmit="{{create}}" style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:8px;margin:0;">
<label for="nova-lista-m" style="''' + T['label'] + '''">Nova lista</label>
<div style="display:flex;gap:8px;"><input id="nova-lista-m" type="text" value="{{newName}}" onChange="{{onNewName}}" placeholder="Ex.: Kanji N5 — Semana 1" maxlength="60" style="flex-grow:1;''' + INPUT + '''"><button type="submit" class="btn" aria-label="Criar lista" style="''' + btn('primary') + '''width:44px;height:44px;">''' + ic('plus', 20, 2.2) + '''</button></div>
<sc-if value="{{newErrOn}}" hint-placeholder-val="{{false}}"><span role="alert" style="font-size:12px;color:''' + c('error') + ''';">{{newErr}}</span></sc-if>
</form>
<sc-if value="{{noLists}}" hint-placeholder-val="{{false}}"><div style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:12px;"><h2 style="''' + T['h4'] + '''">Crie sua primeira lista</h2><p style="''' + T['small'] + '''">Dê um nome à lista e adicione os caracteres que quiser — kanji de qualquer nível, hiragana ou katakana.</p><button class="btn soft" onClick="{{example}}" style="''' + btn('outline', 'md') + '''white-space:normal;height:auto;min-height:44px;padding:8px 16px;">Criar a lista de exemplo “Kanji N5 — Semana 1”</button></div></sc-if>
<div role="listbox" aria-label="Suas listas" style="display:flex;flex-direction:column;gap:8px;">
<sc-for list="{{lists}}" as="l" hint-placeholder-count="3"><button role="option" aria-selected="false" onClick="{{l.pick}}" class="soft" style="display:flex;align-items:center;gap:12px;padding:12px;border-radius:12px;border:1px solid #e7e5e4;background-color:#ffffff;cursor:pointer;text-align:left;color:#1c1917;">
<span class="jp" style="width:40px;height:40px;flex-shrink:0;border-radius:8px;background:''' + c('surface-muted') + ''';display:flex;align-items:center;justify-content:center;font-size:24px;">{{l.first}}</span>
<span style="flex-grow:1;min-width:0;display:flex;flex-direction:column;gap:2px;"><strong style="font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{l.name}}</strong><span style="font-size:12px;color:''' + c('text-muted') + ''';">{{l.count}} · {{l.when}}</span></span><span style="display:flex;color:''' + c('text-muted') + ''';transform:rotate(-90deg);">''' + ic('chev', 18, 2) + '''</span></button></sc-for>
</div>
</div>
</sc-if>
<sc-if value="{{mOpen}}" hint-placeholder-val="{{false}}">
<div class="rise" style="display:flex;flex-direction:column;gap:16px;">
<button class="btn soft" onClick="{{mClose}}" style="''' + btn('ghost', 'sm') + '''align-self:flex-start;padding:0 8px;">''' + ic('back', 16) + '''Todas as listas</button>
<section style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:12px;">
<sc-if value="{{notRenaming}}" hint-placeholder-val="{{true}}"><div style="display:flex;flex-direction:column;gap:4px;"><h2 style="''' + T['h3'] + '''">{{sel.name}}</h2><span style="''' + T['caption'] + '''">{{sel.count}} · atualizada {{sel.when}}</span></div></sc-if>
<sc-if value="{{renaming}}" hint-placeholder-val="{{false}}"><form onSubmit="{{saveRename}}" style="display:flex;flex-direction:column;gap:8px;margin:0;"><label for="ren-m" style="''' + T['label'] + '''">Nome da lista</label><input id="ren-m" type="text" value="{{renameVal}}" onChange="{{onRename}}" maxlength="60" style="''' + INPUT_BLOCK + '''"><div style="display:flex;gap:8px;"><button type="submit" class="btn" style="''' + btn('primary', 'md') + '''flex:1;">Salvar</button><button type="button" onClick="{{cancelRename}}" class="btn soft" style="''' + btn('outline', 'md') + '''flex:1;">Cancelar</button></div><sc-if value="{{renameErrOn}}" hint-placeholder-val="{{false}}"><span role="alert" style="font-size:12px;color:''' + c('error') + ''';">{{renameErr}}</span></sc-if></form></sc-if>
<div style="display:flex;gap:8px;flex-wrap:wrap;">
<button class="btn soft" onClick="{{startRename}}" style="''' + btn('outline', 'sm') + '''">''' + ic('pencil', 16) + '''Renomear</button>
<button class="btn soft" onClick="{{askDelete}}" style="''' + btn('outline', 'sm') + '''color:''' + c('error') + ''';">''' + ic('trash', 16) + '''Excluir</button>
<sc-if value="{{sel.has}}" hint-placeholder-val="{{true}}"><a href="Praticar.dc.html" onClick="{{practice}}" class="btn" style="''' + btn('primary', 'sm') + '''">''' + ic('brush', 16) + '''Praticar</a></sc-if>
</div>
<sc-if value="{{confirmDel}}" hint-placeholder-val="{{false}}"><div role="alertdialog" aria-label="Confirmar exclusão" style="''' + alert('error') + '''flex-direction:column;"><span>Excluir a lista <strong>“{{sel.name}}”</strong>? Os caracteres continuam no site.</span><div style="display:flex;gap:8px;"><button onClick="{{doDelete}}" class="btn" style="''' + btn('danger', 'sm') + '''">Excluir lista</button><button onClick="{{cancelDelete}}" class="btn soft" style="''' + btn('outline', 'sm') + '''">Cancelar</button></div></div></sc-if>
<sc-if value="{{sel.empty}}" hint-placeholder-val="{{false}}"><p style="''' + T['small'] + '''text-align:center;padding:16px;border:1px dashed ''' + c('border-strong') + ''';border-radius:12px;">Lista vazia — adicione caracteres abaixo.</p></sc-if>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;">
<sc-for list="{{items}}" as="it" hint-placeholder-count="10"><div style="position:relative;display:flex;flex-direction:column;align-items:center;padding:8px 2px 6px;border-radius:8px;border:1px solid #e7e5e4;background:#ffffff;min-width:0;"><span class="jp" style="font-size:{{it.fs}};line-height:1.15;">{{it.c}}</span><span style="font-size:10px;color:#57534e;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{it.sub}}</span><button onClick="{{it.remove}}" aria-label="Remover {{it.c}} da lista" style="position:absolute;top:0;right:0;width:24px;height:24px;border:none;background:transparent;color:#78716c;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('x', 12, 2.4) + '''</button></div></sc-for>
</div>
<sc-if value="{{msgOn}}" hint-placeholder-val="{{false}}"><span role="status" style="font-size:14px;font-weight:700;color:''' + c('success') + ''';">{{msg}}</span></sc-if>
</section>
<section style="''' + CARD + '''padding:16px;display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><h2 style="''' + T['h4'] + '''">Adicionar caracteres</h2><span style="''' + T['caption'] + '''">{{found}}</span></div>
<label style="position:relative;display:flex;align-items:center;"><span style="position:absolute;left:12px;display:flex;color:''' + c('text-muted') + ''';">''' + ic('search', 18) + '''</span><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Buscar caracteres</span><input type="search" value="{{q}}" onChange="{{onQ}}" placeholder="Caractere, leitura ou significado" style="''' + INPUT_BLOCK + '''padding-left:40px;"></label>
''' + hscroll(pill_m('cats')) + hscroll(pill_m('jlpts')) + '''
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;">
<sc-for list="{{results}}" as="r" hint-placeholder-count="15"><button onClick="{{r.toggle}}" aria-pressed="{{r.pressed}}" aria-label="{{r.title}}" style="position:relative;height:56px;border-radius:8px;border:1px solid {{r.bd}};background-color:{{r.bg}};cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#1c1917;min-width:0;"><span class="jp" style="font-size:{{r.fs}};line-height:1.1;">{{r.c}}</span><span style="font-size:10px;color:#57534e;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:0 2px;">{{r.sub}}</span><sc-if value="{{r.in}}" hint-placeholder-val="{{false}}"><span aria-hidden="true" style="position:absolute;top:2px;right:2px;width:14px;height:14px;border-radius:9999px;background-color:''' + ACC + ''';color:#ffffff;display:flex;align-items:center;justify-content:center;">''' + ic('check', 10, 3) + '''</span></sc-if></button></sc-for>
</div>
<span style="''' + T['caption'] + '''">Toque num caractere para adicionar ou remover.</span>
<div style="display:flex;gap:8px;flex-wrap:wrap;">
<sc-if value="{{hasMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{more}}" style="''' + btn('outline', 'sm') + '''">{{moreLabel}}</button></sc-if>
<sc-if value="{{canAddAll}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{addAll}}" style="''' + btn('outline', 'sm') + '''">''' + ic('plus', 16, 2) + '''{{addAllLabel}}</button></sc-if>
</div>
</section>
</div>
</sc-if>
</div>
</sc-if>''', 'praticar')

if __name__ == '__main__':
    W, H = 390, 844
    open('project/MainMobile.dc.html', 'w').write(page('Kaku — Início (celular)', 'pt-BR', main_m, b_pages.script_m, W, H, DATA_HEAD))
    open('project/KanjiMobile.dc.html', 'w').write(page('Kaku — Kanji (celular)', 'pt-BR', kanji_m, b_kanji.script, W, H, DATA_HEAD))
    open('project/ProgressoMobile.dc.html', 'w').write(page('Kaku — Progresso (celular)', 'pt-BR', prog_m, b_progress.script, W, H, DATA_HEAD))
    open('project/LoginMobile.dc.html', 'w').write(page('Kaku — Entrar (celular)', 'pt-BR', login_m, b_auth.login_script, W, H))
    open('project/CadastroMobile.dc.html', 'w').write(page('Kaku — Criar conta (celular)', 'pt-BR', signup_m, b_auth.signup_script, W, H))
    open('project/PerfilMobile.dc.html', 'w').write(page('Kaku — Perfil (celular)', 'pt-BR', profile_m, b_auth.profile_script, W, H, DATA_HEAD))
    open('project/ListasMobile.dc.html', 'w').write(page('Kaku — Minhas listas (celular)', 'pt-BR', lists_m, b_lists.script, W, H, DATA_HEAD))
