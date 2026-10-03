"""Artboards de documentação do Design System (gerados a partir de ds.py/ui.py — a mesma fonte das telas)."""
from common import *
import ds
from ds import c, TW, SEM, SHADOW, TYPE, SPACING_ROLES, RADIUS_ROLES, BREAKPOINTS
from ui import T, CARD, BTN_VARIANT, BTN_SIZE, btn, INPUT, INPUT_BLOCK, badge, alert, OVERLINE

W = 1440
def sec(title, sub, inner, cols=None):
    return ('<section style="display:flex;flex-direction:column;gap:24px;flex-shrink:0;">'
            '<div style="display:flex;flex-direction:column;gap:8px;"><h2 style="' + T['h2'] + '">' + title + '</h2><p style="' + T['body'] + 'max-width:768px;">' + sub + '</p></div>'
            + inner + '</section>')

def box(inner, pad=24, extra=''):
    return '<div style="' + CARD + 'padding:%dpx;display:flex;flex-direction:column;gap:16px;%s">' % (pad, extra) + inner + '</div>'

def code(t):
    return '<code style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;line-height:16px;color:%s;background:%s;padding:2px 6px;border-radius:6px;">%s</code>' % (c('text-secondary'), c('surface-muted'), t)

def swatch(name, tw, big=False):
    hexv = TW[tw]; dark = tw in ('black',) or any(tw.endswith('-' + k) for k in ('600', '700', '800', '900', '950'))
    return ('<div style="display:flex;flex-direction:column;gap:8px;min-width:0;">'
            '<div style="height:%dpx;border-radius:8px;background:%s;border:1px solid %s;"></div>' % (64 if big else 48, hexv, c('border'))
            + '<div style="display:flex;flex-direction:column;gap:2px;min-width:0;"><span style="' + T['label'] + 'font-size:12px;line-height:16px;">' + name + '</span><span style="' + T['caption'] + '">' + tw + ' · ' + hexv + '</span></div></div>')

def grid(n, inner, gap=16):
    return '<div style="display:grid;grid-template-columns:repeat(%d,minmax(0,1fr));gap:%dpx;">' % (n, gap) + inner + '</div>'

def state_label(t):
    return '<span style="' + T['caption'] + 'text-align:center;">' + t + '</span>'

HEAD = lambda title, sub: ('<header style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;padding-bottom:32px;border-bottom:1px solid %s;">' % c('border')
    + '<div style="display:flex;flex-direction:column;gap:8px;"><span style="' + OVERLINE + 'color:' + c('primary') + ';">Kaku Design System · Tailwind CSS</span><h1 style="' + T['h1'] + '">' + title + '</h1><p style="' + T['body'] + 'max-width:768px;">' + sub + '</p></div>'
    + '<span class="jp" style="width:64px;height:64px;border-radius:12px;background:' + c('primary') + ';color:#ffffff;display:flex;align-items:center;justify-content:center;font-size:36px;">書</span></header>')

# =================================================================== FUNDAMENTOS
def ratio_bar():
    return ('<div style="display:flex;height:96px;border-radius:12px;overflow:hidden;border:1px solid %s;">' % c('border')
        + '<div style="flex:60;background:%s;padding:16px;display:flex;flex-direction:column;justify-content:flex-end;"><strong style="%s">60%% · Dominante</strong><span style="%s">background · stone-100</span></div>' % (c('background'), T['label'], T['caption'])
        + '<div style="flex:30;background:%s;border-left:1px solid %s;padding:16px;display:flex;flex-direction:column;justify-content:flex-end;"><strong style="%s">30%% · Secundária</strong><span style="%s">surface white · stone-200/900</span></div>' % (c('surface'), c('border'), T['label'], T['caption'])
        + '<div style="flex:10;background:%s;padding:16px;display:flex;flex-direction:column;justify-content:flex-end;"><strong style="%scolor:#ffffff;">10%%</strong><span style="%scolor:%s;">red-600</span></div>' % (c('primary'), T['label'], T['caption'], c('red-100'))
        + '</div>')

def token_table():
    groups = [
        ('primary', [('primary', 'red-600'), ('hover', 'red-700'), ('active', 'red-800'), ('subtle', 'red-50'), ('muted / focus', 'red-100'), ('disabled', 'red-300')]),
        ('secondary', [('secondary', 'stone-900'), ('hover', 'stone-800'), ('active', 'stone-700'), ('subtle', 'stone-100'), ('disabled', 'stone-300')]),
        ('accent', [('accent', 'red-600'), ('subtle', 'red-50'), ('muted', 'red-100'), ('border', 'red-200')]),
        ('background · surface', [('background', 'stone-100'), ('background-subtle', 'stone-50'), ('surface', 'white'), ('surface-muted', 'stone-100'), ('surface-inverse', 'stone-900')]),
        ('border', [('border', 'stone-200'), ('border-strong', 'stone-300'), ('divider', 'stone-200')]),
        ('texto', [('text-primary', 'stone-900'), ('text-secondary', 'stone-700'), ('text-muted', 'stone-600'), ('placeholder', 'stone-500'), ('disabled', 'stone-400')]),
        ('success', [('texto/ícone', 'green-700'), ('fundo', 'green-100'), ('sutil', 'green-50'), ('borda', 'green-200'), ('sólido', 'green-600')]),
        ('warning', [('texto/ícone', 'amber-800'), ('fundo', 'amber-100'), ('sutil', 'amber-50'), ('borda', 'amber-200'), ('sólido', 'amber-600')]),
        ('error', [('texto/ícone', 'red-700'), ('fundo', 'red-100'), ('sutil', 'red-50'), ('borda', 'red-200'), ('sólido', 'red-600')]),
        ('info', [('texto/ícone', 'blue-800'), ('fundo', 'blue-100'), ('sutil', 'blue-50'), ('borda', 'blue-200'), ('sólido', 'blue-600')]),
    ]
    out = ''
    for g, items in groups:
        out += ('<div style="display:grid;grid-template-columns:192px minmax(0,1fr);gap:24px;align-items:start;padding:16px 0;border-top:1px solid %s;">' % c('divider')
                + '<div style="display:flex;flex-direction:column;gap:4px;"><strong style="' + T['h4'] + '">' + g + '</strong>' + code(g.split(' ')[0]) + '</div>'
                + grid(6, ''.join(swatch(n, t) for n, t in items)) + '</div>')
    return out

def palettes():
    rows = ''
    for fam, steps in [('stone', [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]), ('red', [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]),
                       ('green', [50, 100, 200, 600, 700, 800]), ('amber', [50, 100, 200, 600, 700, 800]), ('blue', [50, 100, 200, 600, 700, 800])]:
        cells = ''.join('<div style="flex:1;display:flex;flex-direction:column;gap:4px;min-width:0;"><div style="height:40px;border-radius:6px;background:%s;border:1px solid %s;"></div><span style="%s">%d</span></div>' % (TW['%s-%d' % (fam, s)], c('border'), T['caption'], s) for s in steps)
        rows += '<div style="display:flex;align-items:center;gap:16px;"><span style="' + T['label'] + 'width:64px;">' + fam + '</span><div style="flex:1;display:flex;gap:8px;">' + cells + '</div></div>'
    return rows

def type_scale():
    out = ''
    for name, cls, px, lh, wt, fam in TYPE:
        style = ("font-family:'Shippori Mincho',serif;" if fam == 'serif' else '') + 'font-size:%dpx;line-height:%s;font-weight:%d;color:%s;margin:0;' % (px, lh, wt, c('text-primary'))
        if name == 'Overline': style += 'letter-spacing:0.1em;text-transform:uppercase;color:%s;' % c('text-muted')
        if name in ('Body', 'Body Small'): style = style.replace(c('text-primary'), c('text-secondary'))
        if name == 'Caption': style = style.replace(c('text-primary'), c('text-muted'))
        sample = {'Display': 'Aprenda a escrever', 'H1': 'Seu progresso', 'H2': 'Componentes do Kanji', 'H3': 'Nova sessão', 'H4': 'Mais praticados',
                  'Body': 'Escreva no quadro com o mouse ou o dedo.', 'Body Small': 'O Kaku compara seu desenho com o caractere.', 'Label': 'Email', 'Caption': '12 caracteres diferentes', 'Overline': 'Sistema de escrita'}[name]
        out += ('<div style="display:grid;grid-template-columns:160px minmax(0,1fr) 320px;gap:24px;align-items:center;padding:16px 0;border-top:1px solid %s;">' % c('divider')
                + '<div style="display:flex;flex-direction:column;gap:4px;"><strong style="' + T['label'] + '">' + name + '</strong><span style="' + T['caption'] + '">%dpx / %s · %d</span></div>' % (px, lh, wt)
                + '<p style="' + style + '">' + sample + '</p><div>' + code(cls) + '</div></div>')
    out += ('<div style="' + alert('info') + 'margin-top:8px;"><span>Famílias: <strong>font-serif</strong> Shippori Mincho (títulos Display–H2) · <strong>font-sans</strong> Zen Kaku Gothic New (texto e interface) · <strong>font-jp</strong> Klee One (caracteres japoneses em destaque). Título → texto: <strong>gap-2</strong>; texto → conteúdo: <strong>gap-4</strong> a <strong>gap-6</strong>.</span></div>')
    return out

def spacing():
    bars = ''.join('<div style="display:flex;align-items:center;gap:16px;"><span style="' + T['label'] + 'width:48px;">' + k + '</span><div style="height:16px;width:%dpx;background:%s;border-radius:4px;"></div><span style="%s">%dpx</span></div>' % (v, c('red-200'), T['caption'], v)
                   for k, v in [('0.5', 2), ('1', 4), ('2', 8), ('3', 12), ('4', 16), ('5', 20), ('6', 24), ('8', 32), ('10', 40), ('12', 48), ('16', 64), ('20', 80), ('24', 96)])
    roles = ''.join('<div style="display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-top:1px solid %s;"><span style="%s">%s</span>%s</div>' % (c('divider'), T['small'], k, code(v)) for k, v in SPACING_ROLES.items())
    return grid(2, box('<h3 style="' + T['h4'] + '">Escala (Tailwind spacing)</h3><div style="display:flex;flex-direction:column;gap:8px;">' + bars + '</div>')
                + box('<h3 style="' + T['h4'] + '">Hierarquia</h3><div>' + roles + '</div>'), 24)

def radius_shadow():
    rad = ''.join('<div style="display:flex;flex-direction:column;gap:8px;"><div style="height:80px;border:2px solid %s;background:%s;border-radius:%s;"></div><strong style="%s">%s</strong><span style="%s">%s</span></div>' % (c('border-strong'), c('surface-muted'), r, T['label'], k, T['caption'], u)
                  for (k, u), r in zip(RADIUS_ROLES.items(), ['6px', '8px', '12px', '9999px']))
    sh = ''.join('<div style="display:flex;flex-direction:column;gap:12px;"><div style="height:80px;border-radius:12px;background:#ffffff;box-shadow:%s;"></div><strong style="%s">%s</strong><span style="%s">%s</span></div>' % (SHADOW[k], T['label'], 'shadow' if k == 'DEFAULT' else 'shadow-' + k, T['caption'], u)
                 for k, u in [('sm', 'segmentos ativos, cards elevados'), ('DEFAULT', 'botões flutuantes'), ('md', 'hover de cards, tooltips'), ('lg', 'dropdowns e menus'), ('xl', 'modais e bottom sheets')])
    bd = ('<div style="display:flex;flex-direction:column;gap:12px;">'
          + '<div style="display:flex;align-items:center;gap:16px;"><div style="flex:1;height:0;border-top:1px solid %s;"></div>%s</div>' % (c('border'), code('border · border-stone-200 (padrão)'))
          + '<div style="display:flex;align-items:center;gap:16px;"><div style="flex:1;height:0;border-top:1px solid %s;"></div>%s</div>' % (c('border-strong'), code('border-stone-300 (inputs)'))
          + '<div style="display:flex;align-items:center;gap:16px;"><div style="flex:1;height:0;border-top:2px solid %s;"></div>%s</div>' % (c('primary'), code('border-2 border-red-600 (seleção, foco)'))
          + '<div style="display:flex;align-items:center;gap:16px;"><div style="flex:1;height:0;border-top:1px dashed %s;"></div>%s</div>' % (c('border-strong'), code('border-dashed (vazios, guias)')) + '</div>')
    return (grid(4, rad, 24) + '<div style="height:8px;"></div>' + grid(5, sh, 24) + box('<h3 style="' + T['h4'] + '">Bordas e divisores</h3>' + bd))

def layout():
    bp = ''.join('<div style="display:flex;justify-content:space-between;padding:12px 0;border-top:1px solid %s;"><span style="%s">%s</span><span style="%s">≥ %dpx</span></div>' % (c('divider'), T['label'], k, T['small'], v) for k, v in BREAKPOINTS.items())
    rules = ''.join('<div style="display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-top:1px solid %s;"><span style="%s">%s</span>%s</div>' % (c('divider'), T['small'], k, code(v)) for k, v in [
        ('Container', 'mx-auto w-full max-w-7xl'), ('Padding lateral', 'px-5 sm:px-6 lg:px-12 xl:px-20'), ('Topo da página', 'pt-10 pb-12'),
        ('Entre seções', 'space-y-8 lg:space-y-12'), ('Grid de cards', 'grid gap-6 sm:grid-cols-2 lg:grid-cols-3'), ('Grid de caracteres', 'grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-4'),
        ('Prática (3 colunas)', 'grid gap-6 lg:grid-cols-12 · col-span-3 / 5 / 4'), ('Navegação', 'barra superior ≥ md · barra inferior < md')])
    cols = ''.join('<div style="height:96px;background:%s;border-radius:4px;"></div>' % c('red-100') for _ in range(12))
    return (grid(2, box('<h3 style="' + T['h4'] + '">Breakpoints (padrão Tailwind)</h3><div>' + bp + '</div>') + box('<h3 style="' + T['h4'] + '">Regras de página</h3><div>' + rules + '</div>'), 24)
            + box('<h3 style="' + T['h4'] + '">Grid de 12 colunas · max-w-7xl (1280px) · gap-6</h3>' + grid(12, cols, 24)))

body_f = ('<div style="width:1440px;height:5760px;box-sizing:border-box;background:%s;padding:48px 80px 80px;display:flex;flex-direction:column;gap:48px;overflow:hidden;">' % c('background')
    + HEAD('Fundamentos', 'Cores, tipografia, espaçamento, bordas e layout. Todos os valores vêm da escala padrão do Tailwind CSS — as telas do Kaku são geradas a partir destes mesmos tokens.')
    + sec('Cores · regra 60/30/10', 'Neutros quentes (stone) dominam fundos e superfícies; a escala stone também estrutura cards, navegação, bordas e texto; o vermelho aparece só onde precisa chamar atenção: CTAs, links, estados ativos e indicadores.', ratio_bar() + box(token_table(), 24, 'gap:0;'))
    + sec('Paletas do Tailwind em uso', 'Somente estas famílias. Status nunca é comunicado só por cor: sempre com ícone e rótulo.', box(palettes()))
    + sec('Tipografia', 'Um tamanho por função. Elementos com o mesmo papel usam sempre o mesmo estilo.', box(type_scale(), 24, 'gap:0;'))
    + sec('Espaçamento', 'Apenas a escala do Tailwind, com uma hierarquia fixa para cada relação.', spacing())
    + sec('Raios, sombras e bordas', 'Pequenos: rounded-md · botões e campos: rounded-lg · cards e containers: rounded-xl · pílulas: rounded-full.', radius_shadow())
    + sec('Layout e responsividade', 'Mesma estrutura em todas as páginas. Os quadros do canvas mostram os breakpoints xl (1440) e celular (390).', layout())
    + '</div>')

# =================================================================== COMPONENTES
STATES = ['Padrão', 'Hover', 'Focus', 'Active', 'Disabled', 'Loading']
FOCUS = 'outline:2px solid %s;outline-offset:2px;' % c('primary')
def button_states(variant, label):
    hover = {'primary': 'background-color:%s;' % c('primary-hover'), 'secondary': 'background-color:%s;' % c('secondary-hover'), 'outline': 'background:%s;' % c('background-subtle'),
             'ghost': 'background:%s;' % c('surface-muted'), 'danger': 'background-color:%s;' % c('red-800'), 'link': 'color:%s;text-decoration:underline;' % c('primary-hover')}[variant]
    active = {'primary': 'background-color:%s;' % c('primary-active'), 'secondary': 'background-color:%s;' % c('secondary-active'), 'outline': 'background:%s;' % c('surface-muted'),
              'ghost': 'background:%s;' % c('border'), 'danger': 'background-color:%s;' % c('red-900'), 'link': 'color:%s;' % c('primary-active')}[variant]
    base = btn(variant, 'md').replace('{{accent}}', c('primary'))
    cells = [base, base + hover, base + FOCUS, base + active, base + 'opacity:.5;cursor:not-allowed;', base]
    out = ''
    for i, st in enumerate(cells):
        inner = (spinner(16) + 'Salvando…') if i == 5 else label
        out += '<div style="display:flex;flex-direction:column;align-items:center;gap:8px;"><button style="' + st + '"' + (' disabled' if i == 4 else '') + '>' + inner + '</button>' + state_label(STATES[i]) + '</div>'
    return ('<div style="display:grid;grid-template-columns:160px repeat(6,minmax(0,1fr));gap:16px;align-items:center;padding:12px 0;border-top:1px solid %s;"><div style="display:flex;flex-direction:column;gap:4px;"><strong style="%s">%s</strong>%s</div>' % (c('divider'), T['label'], variant, code("button({ variant: '%s' })" % variant)) + out + '</div>')

def field_states():
    lab = lambda t: '<label style="' + T['label'] + '">' + t + '</label>'
    def f(label, style, value='', ph='nome@exemplo.com', msg='', tone='muted', extra=''):
        mcol = c('error') if tone == 'error' else c('text-muted')
        return ('<div style="display:flex;flex-direction:column;gap:8px;">' + lab(label)
                + '<input readonly value="' + value + '" placeholder="' + ph + '" style="' + INPUT_BLOCK + style + '"' + extra + '>'
                + ('<span style="font-size:12px;line-height:16px;color:' + mcol + ';">' + msg + '</span>' if msg else '') + '</div>')
    cells = [f('Padrão', '', msg='Texto de ajuda'), f('Hover', 'border-color:%s;' % c('stone-400')), f('Focus', 'border-color:%s;box-shadow:0 0 0 4px %s;' % (c('primary'), c('primary-muted')), 'ana@'),
             f('Erro', 'border-color:%s;background:%s;' % (c('primary'), c('error-subtle')), 'ana@exemplo', msg='Digite um email válido.', tone='error', extra=' aria-invalid="true"'),
             f('Disabled', 'background:%s;color:%s;' % (c('surface-muted'), c('text-disabled')), 'ana@exemplo.com', extra=' disabled')]
    sel = ('<div style="display:flex;flex-direction:column;gap:8px;">' + lab('Select') + '<select style="' + INPUT_BLOCK + 'appearance:auto;"><option>Todos os radicais</option></select></div>')
    ta = ('<div style="display:flex;flex-direction:column;gap:8px;">' + lab('Textarea') + '<textarea readonly placeholder="Anotações sobre este kanji…" style="' + INPUT_BLOCK + 'height:96px;padding:12px 16px;resize:vertical;line-height:24px;"></textarea></div>')
    pw = ('<div style="display:flex;flex-direction:column;gap:8px;">' + lab('Senha (com olho)') + '<div style="position:relative;"><input readonly type="password" value="segredo1" style="' + INPUT_BLOCK + 'padding-right:48px;"><button aria-label="Mostrar senha" style="position:absolute;right:4px;top:4px;width:36px;height:36px;border:none;border-radius:8px;background:transparent;color:' + c('text-muted') + ';display:flex;align-items:center;justify-content:center;">' + ic('eye', 20) + '</button></div></div>')
    return grid(5, ''.join(cells), 24) + grid(3, sel + ta + pw, 24)

def choice_controls():
    def cb(checked, label, dis=False, focus=False):
        bd = c('primary') if checked else c('border-strong')
        return ('<label style="display:flex;align-items:center;gap:8px;%s"><span style="width:20px;height:20px;border-radius:6px;border:2px solid %s;background:%s;color:#ffffff;display:flex;align-items:center;justify-content:center;box-sizing:border-box;%s">%s</span><span style="%s">%s</span></label>'
                % ('opacity:.5;' if dis else '', bd, bd if checked else '#ffffff', FOCUS if focus else '', ic('check', 13, 3) if checked else '', T['small'], label))
    def rd(checked, label, dis=False, focus=False):
        return ('<label style="display:flex;align-items:center;gap:8px;%s"><span style="width:20px;height:20px;border-radius:9999px;border:2px solid %s;display:flex;align-items:center;justify-content:center;box-sizing:border-box;%s"><span style="width:8px;height:8px;border-radius:9999px;background:%s;"></span></span><span style="%s">%s</span></label>'
                % ('opacity:.5;' if dis else '', c('primary') if checked else c('border-strong'), FOCUS if focus else '', c('primary') if checked else 'transparent', T['small'], label))
    def sw(on, label, dis=False):
        return ('<label style="display:flex;align-items:center;gap:8px;%s"><span style="position:relative;width:44px;height:24px;border-radius:9999px;background:%s;"><span style="position:absolute;top:2px;left:%s;width:20px;height:20px;border-radius:9999px;background:#ffffff;box-shadow:%s;"></span></span><span style="%s">%s</span></label>'
                % ('opacity:.5;' if dis else '', c('primary') if on else c('border-strong'), '22px' if on else '2px', SHADOW['sm'], T['small'], label))
    col = lambda t, items: box('<h3 style="' + T['h4'] + '">' + t + '</h3><div style="display:flex;flex-direction:column;gap:12px;">' + items + '</div>')
    return grid(3, col('Checkbox', cb(False, 'Padrão') + cb(True, 'Marcado') + cb(False, 'Focus', focus=True) + cb(True, 'Disabled', dis=True))
                + col('Radio', rd(False, 'Com modelo') + rd(True, 'De memória (selecionado)') + rd(False, 'Focus', focus=True) + rd(False, 'Disabled', dis=True))
                + col('Switch', sw(False, 'Desligado') + sw(True, 'Priorizar os que mais errei') + sw(True, 'Disabled', dis=True)), 24)

def tabs_badges_alerts():
    seg = ('<div style="display:flex;gap:4px;padding:4px;background:%s;border-radius:9999px;align-self:flex-start;">' % c('border')
           + ''.join('<button aria-pressed="false" style="height:36px;padding:0 16px;border:none;border-radius:9999px;font-size:14px;%s">%s</button>' % (('background:#ffffff;color:%s;font-weight:700;box-shadow:%s;' % (c('text-primary'), SHADOW['sm'])) if i == 1 else 'background:transparent;color:%s;font-weight:500;' % c('text-secondary'), t) for i, t in enumerate(['Hoje', 'Esta semana', 'Este mês', 'Todo o período'])) + '</div>')
    chips = ('<div style="display:flex;gap:8px;flex-wrap:wrap;">' + ''.join('<button aria-pressed="false" style="height:36px;padding:0 12px;border-radius:9999px;font-size:14px;border:1px solid %s;background:%s;color:%s;%s">%s</button>' % (bd, bg, fg, ex, t) for t, bd, bg, fg, ex in [
        ('Todos', c('secondary'), c('secondary'), '#ffffff', ''), ('Kanji', c('border'), '#ffffff', c('text-secondary'), ''), ('N5 · hover', c('border'), c('background-subtle'), c('text-secondary'), ''), ('N4 · focus', c('border'), '#ffffff', c('text-secondary'), FOCUS), ('N1 · disabled', c('border'), '#ffffff', c('text-secondary'), 'opacity:.5;')]) + '</div>')
    under = ('<div style="display:flex;gap:24px;border-bottom:1px solid %s;">' % c('border') + ''.join('<span style="padding:0 0 12px;font-size:14px;%s">%s</span>' % (('font-weight:700;color:%s;border-bottom:2px solid %s;' % (c('text-primary'), c('primary'))) if i == 0 else 'color:%s;' % c('text-muted'), t) for i, t in enumerate(['Decomposição', 'Formação', 'Exemplos'])) + '</div>')
    badges = '<div style="display:flex;gap:8px;flex-wrap:wrap;">' + ''.join('<span style="%s">%s</span>' % (badge(t), l) for t, l in [('neutral', 'Neutro'), ('primary', 'Kanji'), ('info', 'Hiragana'), ('warning', 'Katakana'), ('success', 'Acerto'), ('error', 'Erro')]) + '<span style="' + badge('neutral') + 'background:' + c('secondary') + ';color:#ffffff;">N5</span></div>'
    al = ''.join('<div style="%s"><span style="display:flex;flex-shrink:0;">%s</span><span><strong>%s</strong> %s</span></div>' % (alert(t), ic(i, 18, 2.2), h, m) for t, i, h, m in [
        ('info', 'bulb', 'Dica.', '“Contorno” mostra o caractere por baixo do quadro.'), ('success', 'check', 'Lista criada.', 'Agora adicione caracteres.'),
        ('warning', 'alert', 'Sem conta.', 'O resultado desta sessão não será salvo.'), ('error', 'x', 'Senha incorreta.', 'Tente novamente.')])
    tip = ('<div style="position:relative;display:flex;flex-direction:column;align-items:center;gap:8px;padding-top:48px;"><span style="position:absolute;top:0;width:max-content;max-width:240px;padding:8px;border-radius:6px;background:%s;color:#ffffff;font-size:12px;line-height:16px;box-shadow:%s;">Qui, 24 set — 12 praticados · 83%%</span><span style="width:40px;height:64px;border-radius:4px;background:%s;"></span></div>' % (c('secondary'), SHADOW['md'], c('green-600')))
    return grid(2, box('<h3 style="' + T['h4'] + '">Tabs</h3>' + seg + under + '<h3 style="' + T['h4'] + '">Chips de filtro</h3>' + chips)
                + box('<h3 style="' + T['h4'] + '">Badges</h3>' + badges + '<h3 style="' + T['h4'] + '">Tooltip</h3>' + tip), 24) + box('<h3 style="' + T['h4'] + '">Alerts</h3>' + grid(2, al, 16))

def overlays():
    menu = ('<div style="width:256px;box-sizing:border-box;padding:8px;background:#ffffff;border:1px solid %s;border-radius:12px;box-shadow:%s;display:flex;flex-direction:column;gap:2px;">' % (c('border'), SHADOW['lg'])
            + '<div style="padding:8px 12px 12px;border-bottom:1px solid %s;margin-bottom:4px;display:flex;flex-direction:column;"><strong style="%s">Ana Souza</strong><span style="%s">ana@exemplo.com</span></div>' % (c('divider'), T['label'], T['caption'])
            + ''.join('<span style="display:flex;align-items:center;gap:12px;height:44px;padding:0 12px;border-radius:8px;font-size:14px;%s">%s%s</span>' % (('background:%s;' % c('surface-muted')) if i == 1 else '', '<span style="display:flex;color:%s;">%s</span>' % (c('text-muted'), ic(icn, 18)), t) for i, (icn, t) in enumerate([('user', 'Perfil'), ('list', 'Minhas listas · hover'), ('history', 'Histórico')]))
            + '<span style="display:flex;align-items:center;gap:12px;height:44px;padding:0 12px;border-top:1px solid %s;margin-top:4px;font-size:14px;color:%s;">%sSair</span></div>' % (c('divider'), c('error'), ic('logout', 18)))
    modal = ('<div style="position:relative;height:320px;border-radius:12px;overflow:hidden;background:%s;">' % c('stone-300')
             + '<div style="position:absolute;inset:0;background:rgb(12 10 9 / 0.4);"></div>'
             + '<div role="dialog" style="position:absolute;left:50%%;top:50%%;transform:translate(-50%%,-50%%);width:448px;box-sizing:border-box;padding:24px;background:#ffffff;border-radius:12px;box-shadow:%s;display:flex;flex-direction:column;gap:16px;">' % SHADOW['xl']
             + '<h3 style="' + T['h3'] + '">Excluir lista?</h3><p style="' + T['small'] + '">A lista “Kanji N5 — Semana 1” será apagada. Os caracteres continuam no site.</p>'
             + '<div style="display:flex;justify-content:flex-end;gap:8px;"><button style="' + btn('outline', 'md') + '">Cancelar</button><button style="' + btn('danger', 'md') + '">Excluir lista</button></div></div></div>')
    return grid(2, box('<h3 style="' + T['h4'] + '">Dropdown / menu de usuário</h3>' + menu) + box('<h3 style="' + T['h4'] + '">Modal · max-w-md, rounded-xl, shadow-xl, overlay stone-950/40</h3>' + modal), 24)

def data_nav():
    th = 'padding:12px 0;text-align:left;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;color:%s;' % c('text-muted')
    td = 'padding:12px 0;border-top:1px solid %s;font-size:14px;line-height:20px;color:%s;' % (c('divider'), c('text-primary'))
    table = ('<table style="width:100%;border-collapse:collapse;"><thead><tr><th style="' + th + '">Data</th><th style="' + th + '">Sessão</th><th style="' + th + 'text-align:right;">Caracteres</th><th style="' + th + 'text-align:right;">Taxa</th></tr></thead><tbody>'
             + ''.join('<tr style="%s"><td style="%s">%s</td><td style="%s">%s</td><td style="%stext-align:right;">%s</td><td style="%stext-align:right;font-weight:700;">%s</td></tr>' % (('background:%s;' % c('background-subtle')) if i == 1 else '', td, d, td, s, td, n, td, r) for i, (d, s, n, r) in enumerate([('24 set, 15:14', 'Kanji · N5', '20', '75%'), ('23 set, 09:02', 'Lista: Semana 1 (hover)', '10', '90%'), ('22 set, 21:40', 'Hiragana', '30', '83%')]))
             + '</tbody></table>')
    pg = lambda t, on=False, dis=False: '<button style="min-width:36px;height:36px;padding:0 8px;border-radius:8px;font-size:14px;border:1px solid %s;background:%s;color:%s;font-weight:%s;%s">%s</button>' % (c('secondary') if on else c('border'), c('secondary') if on else '#ffffff', '#ffffff' if on else c('text-secondary'), 700 if on else 500, 'opacity:.5;' if dis else '', t)
    pager = '<div style="display:flex;gap:8px;align-items:center;">' + pg('‹', dis=True) + pg('1', on=True) + pg('2') + pg('3') + '<span style="' + T['caption'] + '">…</span>' + pg('40') + pg('›') + '</div>'
    more = '<button style="' + btn('outline', 'sm') + 'align-self:flex-start;">Mostrar mais (2.076 restantes)</button>'
    crumbs = ('<nav style="display:flex;align-items:center;gap:8px;font-size:14px;"><a style="color:%s;text-decoration:none;font-weight:500;">Caracteres</a><span style="color:%s;">/</span><a style="color:%s;text-decoration:none;font-weight:500;">Kanji</a><span style="color:%s;">/</span><span style="color:%s;font-weight:700;">明</span></nav>' % (c('primary'), c('text-disabled'), c('primary'), c('text-disabled'), c('text-primary')))
    navbar = ('<div style="display:flex;align-items:center;justify-content:space-between;height:64px;padding:0 20px;border:1px solid %s;border-radius:12px;background:%s;">' % (c('border'), c('background'))
              + '<span style="display:flex;align-items:center;gap:8px;"><span class="jp" style="width:36px;height:36px;border-radius:8px;background:%s;color:#ffffff;display:flex;align-items:center;justify-content:center;font-size:20px;">書</span><strong style="font-family:\'Shippori Mincho\',serif;font-size:20px;">Kaku</strong></span>' % c('primary')
              + '<span style="display:flex;gap:4px;padding:4px;border-radius:9999px;background:%s;">' % c('border') + ''.join('<span style="height:36px;padding:0 16px;border-radius:9999px;display:flex;align-items:center;font-size:14px;%s">%s</span>' % (('background:#ffffff;color:%s;font-weight:700;' % c('primary')) if i == 2 else 'color:%s;' % c('text-secondary'), t) for i, t in enumerate(['Início', 'Caracteres', 'Praticar', 'Progresso'])) + '</span>'
              + '<span style="display:flex;align-items:center;gap:8px;"><span style="width:36px;height:36px;border-radius:9999px;background:%s;color:#ffffff;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;">AS</span></span></div>' % c('primary'))
    side = ('<div style="width:256px;box-sizing:border-box;padding:12px;border:1px solid %s;border-radius:12px;background:#ffffff;display:flex;flex-direction:column;gap:4px;">' % c('border')
            + '<span style="' + OVERLINE + 'padding:8px 12px;">Conta</span>'
            + ''.join('<span style="display:flex;align-items:center;gap:12px;height:40px;padding:0 12px;border-radius:8px;font-size:14px;%s">%s%s</span>' % (('background:%s;color:%s;font-weight:700;' % (c('accent-subtle'), c('error'))) if i == 1 else 'color:%s;' % c('text-secondary'), ic(icn, 18), t) for i, (icn, t) in enumerate([('user', 'Perfil'), ('list', 'Minhas listas'), ('history', 'Histórico'), ('logout', 'Sair')])) + '</div>')
    return (box('<h3 style="' + T['h4'] + '">Tabela</h3>' + table)
            + grid(2, box('<h3 style="' + T['h4'] + '">Paginação</h3>' + pager + '<span style="' + T['caption'] + '">Listas longas usam “Mostrar mais” (carregamento incremental):</span>' + more)
                   + box('<h3 style="' + T['h4'] + '">Breadcrumbs</h3>' + crumbs + '<h3 style="' + T['h4'] + '">Sidebar</h3>' + side), 24)
            + box('<h3 style="' + T['h4'] + '">Navbar (≥ md) · barra inferior no celular</h3>' + navbar))

def cards_states():
    k = lambda title, extra, sub: ('<div style="' + CARD + 'padding:24px;display:flex;flex-direction:column;gap:8px;' + extra + '"><strong style="' + T['h4'] + '">' + title + '</strong><span style="' + T['small'] + '">' + sub + '</span></div>')
    skel = lambda w, h=12: '<div style="height:%dpx;width:%s;border-radius:6px;background:%s;"></div>' % (h, w, c('border'))
    loading = box('<h3 style="' + T['h4'] + '">Loading</h3><div style="display:flex;align-items:center;gap:8px;' + T['small'] + '">' + spinner(20, c('primary')) + 'Carregando caracteres…</div><div style="display:flex;flex-direction:column;gap:8px;">' + skel('60%', 16) + skel('100%') + skel('80%') + '</div>')
    empty = box('<h3 style="' + T['h4'] + '">Empty state</h3><div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;padding:24px;border:1px dashed %s;border-radius:12px;"><span class="jp" style="font-size:48px;color:%s;">？</span><strong style="%s">Nenhum caractere encontrado</strong><span style="%s">Tente outro termo ou limpe os filtros.</span><button style="%s">Limpar filtros</button></div>' % (c('border-strong'), c('text-disabled'), T['label'], T['small'], btn('outline', 'sm')))
    return grid(4, k('Card', '', 'rounded-xl · p-6 · border-stone-200') + k('Hover', 'box-shadow:%s;transform:translateY(-2px);' % SHADOW['lg'], 'shadow-lg · -translate-y-0.5')
                + k('Selecionado', 'border-color:%s;box-shadow:0 0 0 2px %s;background:%s;' % (c('primary'), c('primary-muted'), c('accent-subtle')), 'border-red-600 · ring-2 ring-red-100') + k('Disabled', 'opacity:.5;', 'opacity-50'), 24) + grid(2, loading + empty, 24)

buttons = ''.join(button_states(v, l) for v, l in [('primary', 'Começar'), ('secondary', 'Todos'), ('outline', 'Limpar'), ('ghost', 'Mostrar'), ('danger', 'Excluir'), ('link', 'Ver progresso')])
sizes = ('<div style="display:flex;align-items:center;gap:16px;">' + ''.join('<div style="display:flex;flex-direction:column;align-items:center;gap:8px;"><button style="%s">%s</button>%s</div>' % (btn('primary', s).replace('{{accent}}', c('primary')), l, state_label(d)) for s, l, d in [('sm', 'Pequeno', 'sm · h-9 · px-3 · text-sm'), ('md', 'Médio', 'md · h-11 · px-4 · text-sm'), ('lg', 'Grande', 'lg · h-12 · px-6 · text-base')])
         + '<div style="display:flex;flex-direction:column;align-items:center;gap:8px;"><button aria-label="Desfazer" style="' + btn('outline') + 'width:44px;height:44px;">' + ic('undo', 20) + '</button>' + state_label('ícone · size-11') + '</div></div>')

body_c = ('<div style="width:1440px;height:4880px;box-sizing:border-box;background:%s;padding:48px 80px 80px;display:flex;flex-direction:column;gap:48px;overflow:hidden;">' % c('background')
    + HEAD('Componentes', 'Um padrão por função, com os mesmos estados em toda a aplicação: padrão, hover, focus, active, disabled, loading e erro. As variantes existem como funções em ui.py e como CVA em design-system/components.ts.')
    + sec('Botões', 'Variantes × estados. Foco sempre com outline-2 red-600 e offset-2; disabled = opacity-50 + cursor-not-allowed; loading = spinner + rótulo no gerúndio.', box(buttons + '<div style="height:8px;"></div>' + sizes, 24, 'gap:0;'))
    + sec('Campos de formulário', 'Inputs, selects e textareas: h-11, px-4, rounded-lg, border-stone-300. Rótulo acima (gap-2), mensagem abaixo. Erro: borda red-600, fundo red-50 e texto com ícone.', box(field_states(), 24))
    + sec('Seleção', 'Checkbox rounded-md, radio e switch rounded-full, sempre com rótulo clicável.', choice_controls())
    + sec('Tabs, chips, badges, tooltips e alerts', 'Tabs segmentadas para alternar visões; chips para filtros combináveis; badges rounded-md; alerts com ícone + texto (nunca só cor).', tabs_badges_alerts())
    + sec('Menus, dropdowns e modais', 'Superfícies flutuantes: branco, border-stone-200, rounded-xl; dropdown shadow-lg, modal shadow-xl.', overlays())
    + sec('Dados e navegação', 'Tabelas com cabeçalho em overline e divisores stone-200; paginação, breadcrumbs, navbar e sidebar.', data_nav())
    + sec('Cards, loading e empty states', 'Cards com os mesmos estados; carregamento com spinner/skeleton; vazios com ícone, título, explicação e uma ação.', cards_states())
    + '</div>')

SCRIPT = "class Component extends DCLogic {\n  renderVals() { return { accent: this.props.accent ?? '#dc2626' }; }\n}"

if __name__ == '__main__':
    open('project/DesignSystem.dc.html', 'w').write(page('Kaku — Design System · Fundamentos', 'pt-BR', body_f, SCRIPT, 1440, 5760))
    open('project/Componentes.dc.html', 'w').write(page('Kaku — Design System · Componentes', 'pt-BR', body_c, SCRIPT, 1440, 4880))
