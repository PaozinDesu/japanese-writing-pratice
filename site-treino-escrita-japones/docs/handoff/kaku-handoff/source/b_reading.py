"""Prática de leitura — nova tela, montada só com componentes do Design System (ui.py)."""
from common import *
from b_chars import DBJS, DATA_HEAD
from ui import T, CARD, btn, INPUT, INPUT_BLOCK, badge, alert, OVERLINE
from ds import c
from b_mobile_common import mheader, tabbar_m
from b_tabs import mode_tabs

def chips(lst, h=36):
    return ('<sc-for list="{{' + lst + '}}" as="o" hint-placeholder-count="3"><button class="btn" onClick="{{o.pick}}" aria-pressed="{{o.pressed}}" style="height:%dpx;padding:0 12px;border-radius:9999px;border:1px solid {{o.bd}};background-color:{{o.bg}};color:{{o.fg}};font-size:14px;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:8px;">{{o.label}}<span style="font-size:12px;opacity:.7;">{{o.count}}</span></button></sc-for>' % h)

def seg(lst):
    return ('<div role="group" style="display:flex;gap:4px;padding:4px;background:%s;border-radius:9999px;align-self:flex-start;">' % c('border')
            + '<sc-for list="{{' + lst + '}}" as="s" hint-placeholder-count="2"><button onClick="{{s.pick}}" aria-pressed="{{s.pressed}}" style="height:36px;padding:0 16px;border:none;border-radius:9999px;background-color:{{s.bg}};color:{{s.fg}};font-weight:{{s.fw}};box-shadow:{{s.sh}};font-size:14px;cursor:pointer;">{{s.label}}</button></sc-for></div>')

def setup(mobile=False):
    pad = 'padding:20px;' if mobile else 'padding:32px;'
    return ('''<sc-if value="{{vSetup}}" hint-placeholder-val="{{true}}">
<section aria-labelledby="t-setup" class="rise" style="''' + CARD + pad + '''display:flex;flex-direction:column;gap:24px;">
<div style="display:flex;flex-direction:column;gap:8px;">
<h''' + ('2' if mobile else '1') + ''' id="t-setup" style="''' + (T['h3'] if mobile else T['h2']) + '''">Prática de leitura</h''' + ('2' if mobile else '1') + '''>
<p style="''' + T['body'] + '''">Veja um caractere e digite como ele se lê. Escolha o que entra na prática.</p>
</div>
<div style="display:flex;flex-direction:column;gap:12px;">
<h3 style="''' + OVERLINE + '''">Tipos de caracteres</h3>
<div role="group" aria-label="Tipos de caracteres" style="display:flex;gap:8px;flex-wrap:wrap;">''' + chips('cats') + '''</div>
<sc-if value="{{noCats}}" hint-placeholder-val="{{false}}"><p role="alert" style="''' + alert('warning') + '''margin:0;">Escolha pelo menos um tipo de caractere.</p></sc-if>
</div>
<sc-if value="{{kanjiOn}}" hint-placeholder-val="{{false}}">
<div class="fade" style="display:flex;flex-direction:column;gap:12px;">
<h3 style="''' + OVERLINE + '''">Níveis JLPT dos kanji</h3>
<div role="group" aria-label="Níveis JLPT" style="display:flex;gap:8px;flex-wrap:wrap;">
<button class="btn" onClick="{{pickAllLevels}}" aria-pressed="{{allLevels.pressed}}" style="height:36px;padding:0 12px;border-radius:9999px;border:1px solid {{allLevels.bd}};background-color:{{allLevels.bg}};color:{{allLevels.fg}};font-size:14px;font-weight:500;cursor:pointer;">Todos os níveis</button>
''' + chips('jlpts') + '''</div>
</div>
</sc-if>
<div style="display:flex;flex-direction:column;gap:12px;"><h3 style="''' + OVERLINE + '''">Quantidade</h3>''' + seg('sizes') + '''</div>
<div style="display:flex;flex-direction:column;gap:4px;padding:16px;border-radius:12px;background:''' + c('surface-muted') + ''';"><strong style="''' + T['label'] + '''">{{poolLabel}}</strong><span style="''' + T['small'] + '''">{{poolCount}}</span></div>
<button class="btn" onClick="{{start}}" disabled="{{cantStart}}" style="''' + btn('primary', 'lg') + '''width:100%;">''' + ic('book', 20) + '''{{startLabel}}</button>
</section>
</sc-if>''')

def quiz(mobile=False):
    big = '{{c.fsM}}' if mobile else '{{c.fs}}'
    box = '220px' if mobile else '288px'
    return ('''<sc-if value="{{vQuiz}}" hint-placeholder-val="{{false}}">
<div style="display:flex;flex-direction:column;gap:''' + ('16' if mobile else '24') + '''px;">
<section aria-label="Progresso da sessão" style="''' + CARD + ('padding:16px;' if mobile else 'padding:16px 24px;') + '''display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:16px;">
<div style="display:flex;flex-direction:column;gap:4px;min-width:0;">
<strong role="status" style="''' + T['h4'] + '''">{{qLabel}}</strong>
<span style="''' + T['small'] + '''">{{scoreLabel}}<span style="color:''' + c('text-muted') + ''';"> · {{rateLabel}}</span></span>
</div>
<button class="btn soft" onClick="{{end}}" style="''' + btn('outline', 'sm') + '''">Encerrar prática</button>
</div>
<div role="progressbar" aria-label="Progresso" aria-valuetext="{{qLabel}}" style="height:8px;border-radius:9999px;background:''' + c('border') + ''';overflow:hidden;"><div style="height:8px;border-radius:9999px;width:{{progW}};background-color:''' + ACC + ''';transition:width .3s ease;"></div></div>
</section>
<section aria-label="Caractere" style="''' + CARD + ('padding:20px;' if mobile else 'padding:32px;') + '''display:flex;flex-direction:column;align-items:center;gap:24px;">
<div style="display:flex;gap:8px;"><span style="''' + badge('neutral') + '''background-color:{{c.tb}};color:{{c.tf}};">{{c.tl}}</span><sc-if value="{{c.hasJlpt}}" hint-placeholder-val="{{false}}"><span style="''' + badge('neutral') + '''background:''' + c('secondary') + ''';color:#ffffff;">{{c.jlpt}}</span></sc-if></div>
<div style="width:''' + box + ''';height:''' + box + ''';border-radius:12px;background:''' + c('background-subtle') + ''';border:1px solid ''' + c('border') + ''';display:flex;align-items:center;justify-content:center;">
<span class="jp pop" lang="ja" style="font-size:''' + big + ''';line-height:1;color:''' + c('text-primary') + ''';">{{c.ch}}</span>
</div>
<form onSubmit="{{submit}}" style="width:100%;max-width:448px;display:flex;flex-direction:column;gap:12px;margin:0;">
<label for="leitura" style="''' + T['label'] + '''text-align:center;">Como se lê?</label>
<input id="leitura" ref="{{setInput}}" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" value="{{ans}}" onChange="{{onAns}}" readOnly="{{locked}}" placeholder="Digite em romaji ou kana — ex.: ka" style="''' + INPUT_BLOCK + '''text-align:center;border-color:{{inputBd}};background-color:{{inputBg}};">
<sc-if value="{{asking}}" hint-placeholder-val="{{true}}">
<div style="display:flex;gap:8px;">
<button type="button" class="btn soft" onClick="{{skip}}" style="''' + btn('ghost', 'md') + '''flex:1;">Pular</button>
<button type="submit" class="btn" disabled="{{cannotSubmit}}" style="''' + btn('primary', 'md') + '''flex:2;">Responder</button>
</div>
<span style="''' + T['caption'] + '''text-align:center;">Pressione Enter para responder</span>
</sc-if>
</form>
<sc-if value="{{answered}}" hint-placeholder-val="{{false}}">
<div class="rise" style="width:100%;max-width:448px;display:flex;flex-direction:column;gap:12px;">
<sc-if value="{{isOk}}" hint-placeholder-val="{{true}}"><div role="status" style="''' + alert('success') + '''"><span style="display:flex;flex-shrink:0;">''' + ic('check', 20, 2.4) + '''</span><div style="display:flex;flex-direction:column;gap:4px;"><strong>Correto!</strong><span>Leituras aceitas: <strong>{{c.main}}</strong></span></div></div></sc-if>
<sc-if value="{{isWrong}}" hint-placeholder-val="{{false}}"><div role="alert" style="''' + alert('error') + '''"><span style="display:flex;flex-shrink:0;">''' + ic('x', 20, 2.4) + '''</span><div style="display:flex;flex-direction:column;gap:4px;"><strong>Não foi dessa vez</strong><span>Sua resposta: “{{given}}” · Resposta correta: <strong>{{c.main}}</strong></span></div></div></sc-if>
<dl style="margin:0;display:grid;grid-template-columns:96px minmax(0,1fr);gap:8px 12px;padding:16px;border-radius:12px;background:''' + c('surface-muted') + ''';">
<dt style="''' + T['caption'] + '''">Leitura</dt><dd class="jp" lang="ja" style="margin:0;''' + T['small'] + '''color:''' + c('text-primary') + ''';">{{c.kana}}</dd>
<dt style="''' + T['caption'] + '''">Romaji</dt><dd style="margin:0;''' + T['small'] + '''color:''' + c('text-primary') + ''';">{{c.main}}</dd>
<sc-if value="{{c.hasMeaning}}" hint-placeholder-val="{{false}}"><dt style="''' + T['caption'] + '''">Significado</dt><dd style="margin:0;''' + T['small'] + '''color:''' + c('text-primary') + ''';">{{c.meaning}}</dd></sc-if>
</dl>
<button class="btn" ref="{{setNext}}" onClick="{{next}}" style="''' + btn('primary', 'lg') + '''width:100%;">{{nextLabel}}''' + ic('arrow', 18, 2) + '''</button>
</div>
</sc-if>
</section>
</div>
</sc-if>''')

def result(mobile=False):
    cols = 3 if mobile else 4
    stat = lambda label, hole, tone='': ('<div style="' + CARD + 'padding:16px;display:flex;flex-direction:column;gap:4px;' + tone + '"><span style="' + T['caption'] + '">' + label + '</span><strong style="' + T['h2'] + '">{{' + hole + '}}</strong></div>')
    stats = stat('Questões', 'rTotal') + stat('Acertos', 'rOk', 'background:%s;border-color:%s;' % (c('success-subtle'), c('success-border'))) + stat('Erros', 'rFail', 'background:%s;border-color:%s;' % (c('error-subtle'), c('error-border'))) + ('' if mobile else stat('Acerto', 'rRate'))
    wrong_rows = ('<table style="width:100%;border-collapse:collapse;font-size:14px;line-height:20px;"><thead><tr>'
                  + ''.join('<th scope="col" style="padding:12px 8px 12px 0;text-align:left;' + OVERLINE + '">' + h + '</th>' for h in (['Caractere', 'Sua resposta', 'Correta'] if mobile else ['Caractere', 'Sua resposta', 'Resposta correta', 'Leitura', 'Significado']))
                  + '</tr></thead><tbody><sc-for list="{{wrongList}}" as="w" hint-placeholder-count="3"><tr>'
                  + '<td style="padding:12px 8px 12px 0;border-top:1px solid %s;"><span class="jp" lang="ja" style="font-size:30px;line-height:1;">{{w.ch}}</span></td>' % c('border')
                  + '<td style="padding:12px 8px 12px 0;border-top:1px solid %s;"><sc-if value="{{w.answered}}" hint-placeholder-val="{{true}}"><span style="color:%s;text-decoration:line-through;">{{w.given}}</span></sc-if><sc-if value="{{w.skipped}}" hint-placeholder-val="{{false}}"><span style="%s">Pulado</span></sc-if></td>' % (c('border'), c('error'), badge('neutral'))
                  + '<td style="padding:12px 8px 12px 0;border-top:1px solid %s;font-weight:700;color:%s;">{{w.correct}}</td>' % (c('border'), c('success'))
                  + ('' if mobile else '<td class="jp" lang="ja" style="padding:12px 8px 12px 0;border-top:1px solid %s;">{{w.kana}}</td><td style="padding:12px 0;border-top:1px solid %s;color:%s;">{{w.meaning}}</td>' % (c('border'), c('border'), c('text-secondary')))
                  + '</tr></sc-for></tbody></table>')
    return ('''<sc-if value="{{vResult}}" hint-placeholder-val="{{false}}">
<div class="rise" style="display:flex;flex-direction:column;gap:24px;">
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:16px;">
<div style="display:flex;flex-direction:column;gap:8px;min-width:0;"><span style="''' + T['caption'] + '''">Resultado · {{rLabel}}</span><h1 style="''' + (T['h3'] if mobile else T['h2']) + '''">{{rHead}}</h1></div>
<span style="font-family:'Shippori Mincho',serif;font-size:''' + ('30' if mobile else '48') + '''px;line-height:1;font-weight:700;color:''' + ACC + ''';">{{rRate}}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(''' + str(cols) + ''',minmax(0,1fr));gap:''' + ('8' if mobile else '16') + '''px;">''' + stats + '''</div>
<div aria-hidden="true" style="height:8px;border-radius:9999px;background:''' + c('red-200') + ''';overflow:hidden;"><div style="height:8px;width:{{barOk}};border-radius:9999px;background:''' + c('success-solid') + ''';"></div></div>
<section aria-labelledby="t-err" style="''' + CARD + ('padding:16px;' if mobile else 'padding:24px;') + '''display:flex;flex-direction:column;gap:12px;">
<h2 id="t-err" style="''' + T['h4'] + '''">Caracteres errados</h2>
<sc-if value="{{noWrong}}" hint-placeholder-val="{{false}}"><p style="''' + T['small'] + '''">Nenhum erro nesta sessão.</p></sc-if>
<sc-if value="{{hasWrong}}" hint-placeholder-val="{{true}}">''' + wrong_rows + '''</sc-if>
</section>
<section aria-labelledby="t-ok" style="''' + CARD + ('padding:16px;' if mobile else 'padding:24px;') + '''display:flex;flex-direction:column;gap:12px;">
<h2 id="t-ok" style="''' + T['h4'] + '''">Caracteres acertados</h2>
<sc-if value="{{noRight}}" hint-placeholder-val="{{false}}"><p style="''' + T['small'] + '''">Nenhum acerto nesta sessão.</p></sc-if>
<div style="display:flex;flex-wrap:wrap;gap:8px;"><sc-for list="{{rightList}}" as="k" hint-placeholder-count="6"><span style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:56px;height:56px;padding:0 8px;box-sizing:border-box;border-radius:8px;border:1px solid ''' + c('success-border') + ''';background:''' + c('success-subtle') + ''';"><span class="jp" lang="ja" style="font-size:24px;line-height:1;">{{k.ch}}</span><span style="font-size:12px;line-height:16px;color:''' + c('success') + ''';">{{k.sub}}</span></span></sc-for></div>
</section>
<div style="display:flex;gap:8px;flex-wrap:wrap;">
<button class="btn" onClick="{{again}}" style="''' + btn('primary', 'md') + ('flex:1;' if mobile else '') + '''">''' + ic('replay', 18) + '''Praticar novamente</button>
<button class="btn soft" onClick="{{onlyWrong}}" disabled="{{noWrong}}" style="''' + btn('outline', 'md') + ('flex:1;' if mobile else '') + '''">''' + ic('target', 18) + '''Praticar somente os erros</button>
<button class="btn soft" onClick="{{backSetup}}" style="''' + btn('ghost', 'md') + ('flex:1;' if mobile else '') + '''">Voltar para seleção</button>
</div>
</div>
</sc-if>''')

def script(page_name):
    helpers = js('practice.js').split('class Component')[0]   # poolOf, poolLabel, chips… (mesmo modelo da Escrita)
    return acctify(DBJS + js('account.js') + 'const CS = 0;\nconst PAGE = %r;\n' % page_name + js('rec.js') + helpers + js('reading.js'))

def from_escrita(src, mobile=False):
    """Reaproveita a configuração da tela Escrita (mesmo layout e componentes), adaptada para Leitura."""
    import re
    if mobile:
        src = re.sub(r'<div style="display:flex;flex-direction:column;gap:8px;"><h2 style="[^"]*">Como praticar</h2>.*?(?=\n<button role="switch")', '', src, flags=re.S)
        src = src.replace(mode_tabs('escrita', True), mode_tabs('leitura', True))
    else:
        src = re.sub(r'<div style="display:flex;flex-direction:column;gap:10px;">\n<h3 style="[^"]*">Como praticar</h3>.*?</div>\n</div>\n(?=<sc-if value="\{\{canStart\}\}")', '', src, flags=re.S)
        src = src.replace(mode_tabs('escrita'), mode_tabs('leitura'))
        src = src.replace('>Pratica - Escrita</h1>', '>Pratica - Leitura</h1>')
        src = src.replace('Escolha o que praticar. Todo caractere do Kaku — hiragana, katakana e os 2.136 kanji — pode entrar numa sessão.', 'Veja um caractere e digite como ele se lê. Todo caractere do Kaku — hiragana, katakana e os 2.136 kanji — pode entrar numa sessão.')
    src = src.replace(ic('brush', 20) + '{{startLabel}}', ic('book', 20) + '{{startLabel}}')
    assert 'Como praticar' not in src and 'aria-current="page" style' in src
    return src

import b_practice as _esc

LOADING = ('<sc-if value="{{loading}}" hint-placeholder-val="{{false}}"><p role="status" style="' + T['small']
           + 'display:flex;align-items:center;gap:8px;padding:40px 80px;">' + spinner(18, c('primary')) + 'Carregando caracteres…</p></sc-if>')

body_d = ('<div style="width:1440px;height:1400px;box-sizing:border-box;background:' + c('background') + ';display:flex;flex-direction:column;overflow:hidden;">\n'
          + nav('praticar') + LOADING + from_escrita(_esc.setup_d)
          + '<sc-if value="{{inSession}}" hint-placeholder-val="{{false}}">'
          + '<main style="width:100%;max-width:896px;box-sizing:border-box;margin:0 auto;padding:32px 0 48px;display:flex;flex-direction:column;gap:24px;">'
          + quiz() + result() + '</main></sc-if></div>')

body_m = ('<div style="width:390px;height:844px;box-sizing:border-box;background:' + c('background') + ';position:relative;overflow:hidden;">\n'
          + mheader('Leitura') + tabbar_m('praticar') + LOADING.replace('padding:40px 80px', 'padding:0 20px') + from_escrita(_esc.setup_m, True)
          + '<sc-if value="{{inSession}}" hint-placeholder-val="{{false}}">'
          + '<main style="position:absolute;left:0;top:72px;width:390px;height:692px;box-sizing:border-box;padding:0 20px 24px;overflow-y:auto;scrollbar-width:none;display:flex;flex-direction:column;gap:16px;">'
          + quiz(True) + result(True) + '</main></sc-if></div>')

if __name__ == '__main__':
    open('project/Leitura.dc.html', 'w').write(page('Kaku — Prática de leitura', 'pt-BR', body_d, script('Leitura.dc.html'), 1440, 1400, DATA_HEAD))
    open('project/LeituraMobile.dc.html', 'w').write(page('Kaku — Leitura (celular)', 'pt-BR', body_m, script('LeituraMobile.dc.html'), 390, 844, DATA_HEAD))
