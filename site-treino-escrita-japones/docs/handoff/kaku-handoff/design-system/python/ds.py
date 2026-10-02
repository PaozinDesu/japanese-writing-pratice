"""Kaku Design System — tokens baseados exclusivamente na escala do Tailwind CSS (v3).

Tudo o que é visual passa por aqui:
  * TW: a paleta do Tailwind usada pelo produto (só os tons que usamos);
  * SEM: tokens semânticos (primary, secondary, accent, background, surface, border, text-*, status);
  * SPACE / RADIUS / TYPE / SHADOW / BREAKPOINTS: escalas;
  * normalize(): garante que nenhum valor fora da escala Tailwind chegue às telas.
"""
import re

# ---------------------------------------------------------------- paleta Tailwind
TW = {
    'white': '#ffffff', 'black': '#000000',
    'stone-50': '#fafaf9', 'stone-100': '#f5f5f4', 'stone-200': '#e7e5e4', 'stone-300': '#d6d3d1', 'stone-400': '#a8a29e',
    'stone-500': '#78716c', 'stone-600': '#57534e', 'stone-700': '#44403c', 'stone-800': '#292524', 'stone-900': '#1c1917', 'stone-950': '#0c0a09',
    'red-50': '#fef2f2', 'red-100': '#fee2e2', 'red-200': '#fecaca', 'red-300': '#fca5a5', 'red-400': '#f87171', 'red-500': '#ef4444',
    'red-600': '#dc2626', 'red-700': '#b91c1c', 'red-800': '#991b1b', 'red-900': '#7f1d1d',
    'green-50': '#f0fdf4', 'green-100': '#dcfce7', 'green-200': '#bbf7d0', 'green-600': '#16a34a', 'green-700': '#15803d', 'green-800': '#166534',
    'amber-50': '#fffbeb', 'amber-100': '#fef3c7', 'amber-200': '#fde68a', 'amber-600': '#d97706', 'amber-700': '#b45309', 'amber-800': '#92400e',
    'blue-50': '#eff6ff', 'blue-100': '#dbeafe', 'blue-200': '#bfdbfe', 'blue-600': '#2563eb', 'blue-700': '#1d4ed8', 'blue-800': '#1e40af',
}

# ---------------------------------------------------------------- semânticos (60 / 30 / 10)
# 60% dominante  -> background (stone-100) e superfícies claras
# 30% secundária -> surface branca, bordas, navegação, texto e ações secundárias (escala stone)
# 10% destaque   -> primary/accent vermelho: CTAs, links, estados ativos, indicadores
SEM = {
    'background': 'stone-100', 'background-subtle': 'stone-50',
    'surface': 'white', 'surface-muted': 'stone-100', 'surface-sunken': 'stone-50', 'surface-inverse': 'stone-900',
    'border': 'stone-200', 'border-strong': 'stone-300', 'divider': 'stone-200',
    'text-primary': 'stone-900', 'text-secondary': 'stone-700', 'text-muted': 'stone-600', 'text-placeholder': 'stone-500', 'text-disabled': 'stone-400', 'text-inverse': 'white',
    'primary': 'red-600', 'primary-hover': 'red-700', 'primary-active': 'red-800', 'primary-subtle': 'red-50', 'primary-muted': 'red-100', 'primary-focus-ring': 'red-100', 'primary-disabled': 'red-300',
    'secondary': 'stone-900', 'secondary-hover': 'stone-800', 'secondary-active': 'stone-700', 'secondary-subtle': 'stone-100', 'secondary-disabled': 'stone-300',
    'accent': 'red-600', 'accent-subtle': 'red-50', 'accent-muted': 'red-100', 'accent-border': 'red-200',
    'success': 'green-700', 'success-bg': 'green-100', 'success-subtle': 'green-50', 'success-border': 'green-200', 'success-solid': 'green-600',
    'warning': 'amber-800', 'warning-bg': 'amber-100', 'warning-subtle': 'amber-50', 'warning-border': 'amber-200', 'warning-solid': 'amber-600',
    'error': 'red-700', 'error-bg': 'red-100', 'error-subtle': 'red-50', 'error-border': 'red-200', 'error-solid': 'red-600',
    'info': 'blue-800', 'info-bg': 'blue-100', 'info-subtle': 'blue-50', 'info-border': 'blue-200', 'info-solid': 'blue-600',
    # sistemas de escrita (identidade de categoria, sempre com rótulo de texto)
    'hiragana-fg': 'blue-800', 'hiragana-bg': 'blue-100', 'katakana-fg': 'amber-800', 'katakana-bg': 'amber-100', 'kanji-fg': 'red-700', 'kanji-bg': 'red-100',
}
def c(token):
    """Hex de um token semântico ou de um tom Tailwind."""
    return TW[SEM.get(token, token)]

# ---------------------------------------------------------------- escalas
SPACE = {'0': 0, 'px': 1, '0.5': 2, '1': 4, '1.5': 6, '2': 8, '2.5': 10, '3': 12, '3.5': 14, '4': 16, '5': 20, '6': 24, '7': 28, '8': 32,
         '9': 36, '10': 40, '11': 44, '12': 48, '14': 56, '16': 64, '20': 80, '24': 96, '28': 112, '32': 128, '36': 144, '40': 160,
         '44': 176, '48': 192, '52': 208, '56': 224, '60': 240, '64': 256, '72': 288, '80': 320, '96': 384}
# Escala reduzida usada para gap/padding/margin: cria a hierarquia (2/4/8/12/16/20/24/32/40/48/64/80/96)
SPACING_STEPS = [0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96]
SPACING_ROLES = {
    'related (ícone+texto, rótulo+campo)': 'gap-2 (8px)',
    'itens de um grupo (chips, botões lado a lado)': 'gap-2 / gap-3 (8–12px)',
    'entre componentes dentro de um card': 'gap-4 (16px)',
    'padding de card': 'p-6 (24px) · compacto p-4/p-5',
    'entre cards / colunas': 'gap-6 (24px)',
    'entre seções da página': 'gap-8 → gap-12 (32–48px)',
    'página (desktop)': 'px-20 py-10 · conteúdo max-w-7xl (1280px)',
    'página (celular)': 'px-5 py-4',
    'campos de formulário': 'gap-4 (16px); rótulo→campo gap-2',
    'título → texto': 'gap-2 (8px); texto → conteúdo gap-4/6',
}
SIZE_STEPS = sorted(set(SPACE.values()))
RADIUS = {'none': 0, 'sm': 2, 'DEFAULT': 4, 'md': 6, 'lg': 8, 'xl': 12, 'full': 9999}
RADIUS_ROLES = {'rounded-md (6px)': 'badges, chips pequenos, tooltips, checkboxes', 'rounded-lg (8px)': 'botões, inputs, selects, tiles, menus', 'rounded-xl (12px)': 'cards, painéis, modais, containers', 'rounded-full': 'pílulas, avatares, abas segmentadas, barras de progresso'}
TYPE = [  # nome, classes, px, line-height, weight, família
    ('Display', 'font-serif text-6xl leading-none font-bold', 60, '1', 700, 'serif'),
    ('H1', 'font-serif text-5xl leading-none font-bold', 48, '1', 700, 'serif'),
    ('H2', 'font-serif text-3xl leading-9 font-bold', 30, '36px', 700, 'serif'),
    ('H3', 'text-xl leading-7 font-bold', 20, '28px', 700, 'sans'),
    ('H4', 'text-lg leading-7 font-bold', 18, '28px', 700, 'sans'),
    ('Body', 'text-base leading-6', 16, '24px', 400, 'sans'),
    ('Body Small', 'text-sm leading-5', 14, '20px', 400, 'sans'),
    ('Label', 'text-sm leading-5 font-bold', 14, '20px', 700, 'sans'),
    ('Caption', 'text-xs leading-4', 12, '16px', 400, 'sans'),
    ('Overline', 'text-xs leading-4 font-bold uppercase tracking-widest', 12, '16px', 700, 'sans'),
]
FONT_STEPS = [12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72, 96, 128]   # escala completa (glifos japoneses)
TEXT_STEPS = [12, 14, 16, 18, 20, 30, 48, 60]                     # papéis tipográficos (Caption…Display)
LEADING = [1, 1.25, 1.375, 1.5, 1.625, 2]
TRACKING = [('-0.025em', -0.025), ('0', 0), ('0.025em', 0.025), ('0.05em', 0.05), ('0.1em', 0.1)]
SHADOW = {
    'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    'DEFAULT': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    'up': '0 -10px 15px -3px rgb(0 0 0 / 0.1), 0 -4px 6px -4px rgb(0 0 0 / 0.1)',
}
BREAKPOINTS = {'sm': 640, 'md': 768, 'lg': 1024, 'xl': 1280, '2xl': 1536}
FONTS = {'sans': "'Zen Kaku Gothic New',ui-sans-serif,system-ui,sans-serif", 'serif': "'Shippori Mincho',ui-serif,Georgia,serif", 'jp': "'Klee One','Hiragino Mincho ProN','Yu Mincho',serif"}

# ---------------------------------------------------------------- migração das cores antigas
COLOR_MAP = {
    'FFFFFF': 'white', '000': 'black', '000000': 'black',
    '1F1C18': 'stone-900', '3B3630': 'stone-800', '2C2823': 'stone-800', '5E5850': 'stone-700', '726B61': 'stone-600', '8A8278': 'stone-500',
    'B5ADA2': 'stone-400', 'C9C1B5': 'stone-300', 'D9D1C4': 'stone-300', 'E0D9CD': 'stone-300', 'E6E0D6': 'stone-200', 'EFEAE1': 'stone-200',
    'E4DCCF': 'stone-200', 'EDE7DD': 'stone-200', 'F2EEE6': 'stone-200', 'EFE9DF': 'stone-100', 'F7F4EE': 'stone-100', 'FBF9F5': 'stone-50', 'FFFEFB': 'white',
    'C8322F': 'red-600', 'D4533F': 'red-500', 'B3282D': 'red-700', '9E2521': 'red-700', 'A8292A': 'red-700', '8E2324': 'red-800', '6E1C1D': 'red-900',
    'FBEDEA': 'red-50', 'FDF3F1': 'red-50', 'F8E4E0': 'red-100', 'F0D3CD': 'red-100', 'EBC9C2': 'red-200', 'F1C7C0': 'red-200', 'E3A99F': 'red-300',
    '4E6E3A': 'green-700', '3F5A2F': 'green-800', '5E7F4A': 'green-600', '6E8F58': 'green-600', 'E7EEDF': 'green-100', 'F4F8F0': 'green-50', 'CFE0C3': 'green-200',
    '7A5210': 'amber-800', 'F4EAD6': 'amber-100',
    '2E4C6E': 'blue-800', 'E3EAF2': 'blue-100', 'EEF2F7': 'blue-50',
}
RGBA_MAP = [  # sombras/overlays antigos -> Tailwind
    ('rgba(31,28,24,.32)', 'rgb(12 10 9 / 0.4)'), ('rgba(31,28,24,.3)', 'rgb(12 10 9 / 0.4)'),
    ('rgba(255,254,251,.72)', 'rgb(255 255 255 / 0.75)'), ('rgba(0,0,0,.2)', 'rgb(0 0 0 / 0.1)'), ('rgba(255,255,255,.15)', 'rgb(255 255 255 / 0.15)'),
]

def _snap(v, steps, tie_small_below=12):
    a = abs(v); best = None
    for s in steps:
        d = abs(s - a)
        if best is None or d < best[0] - 1e-9 or (abs(d - best[0]) < 1e-9 and (s > best[1] if a < tie_small_below else s < best[1])):
            best = (d, s)
    return best[1] if v >= 0 else -best[1]

def _fmt(n):
    return ('%g' % n)

def _px(value, fn):
    return re.sub(r'(-?\d+(?:\.\d+)?)px', lambda m: _fmt(fn(float(m.group(1)))) + 'px', value)

def _shadow(value):
    v = value.strip()
    if v in SHADOW.values():
        return v
    if v == 'none' or '{{' in v or 'inset' in v:
        return v
    if v.startswith('0 0 0 3px'):
        return '0 0 0 2px' + v[len('0 0 0 3px'):]
    if v.startswith('0 0 0 '):
        return v
    nums = [float(x) for x in re.findall(r'(-?\d+(?:\.\d+)?)px', v)]
    if len(nums) < 3:
        return SHADOW['sm']
    y, blur = nums[1], nums[2]
    if y < 0: return SHADOW['up']
    if blur <= 3: return SHADOW['sm']
    if blur <= 20: return SHADOW['md']
    if blur <= 30: return SHADOW['lg']
    return SHADOW['xl']

def _radius(v):
    if v >= 99: return 9999
    if v <= 0: return 0
    if v <= 3: return 2 if v <= 2 else 4
    if v <= 5: return 4
    if v <= 7: return 6
    if v <= 14: return 8
    return 12

def _font(v, glyph=False):
    if v > 128: return v
    return _snap(v, FONT_STEPS if glyph else TEXT_STEPS, tie_small_below=16)

def _lead(num):
    x = float(num)
    return min(LEADING, key=lambda s: (abs(s - x), s))

GRID_W = [224, 256, 288, 320, 384, 448, 512]

DECL = re.compile(r'(?<![\w-])(gap|row-gap|column-gap|padding(?:-top|-right|-bottom|-left|-inline|-block)?|margin(?:-top|-right|-bottom|-left)?|border-radius|font-size|line-height|letter-spacing|box-shadow|width|height|min-width|min-height|max-width|max-height|grid-template-columns|top|bottom)\s*:\s*([^;"{}\n]+)')

_GLYPH = [False]
def _decl(m):
    prop, val = m.group(1), m.group(2)
    if '{{' in val and prop not in ('box-shadow',):
        return m.group(0)
    if prop in ('gap', 'row-gap', 'column-gap') or prop.startswith('padding') or prop.startswith('margin'):
        nv = _px(val, lambda n: _snap(n, SPACING_STEPS))
    elif prop == 'border-radius':
        nv = _px(val, _radius)
    elif prop == 'font-size':
        nv = _px(val, lambda n: _font(n, _GLYPH[0]))
    elif prop == 'line-height':
        mm = re.fullmatch(r'\s*(\d*\.?\d+)\s*', val)
        nv = _fmt(_lead(mm.group(1))) if mm else val
    elif prop == 'letter-spacing':
        mm = re.fullmatch(r'\s*(-?\d*\.?\d+)em\s*', val)
        nv = min(TRACKING, key=lambda t: abs(t[1] - float(mm.group(1))))[0] if mm else val
    elif prop == 'box-shadow':
        nv = _shadow(val)
    elif prop in ('width', 'height', 'min-width', 'min-height', 'max-width', 'max-height'):
        nv = _px(val, lambda n: _snap(n, SIZE_STEPS) if n <= 160 else n)
    elif prop in ('top', 'bottom'):
        return m.group(0)
    elif prop == 'grid-template-columns':
        nv = _px(val, lambda n: min(GRID_W, key=lambda s: abs(s - n)) if n >= 200 else _snap(n, SIZE_STEPS))
    else:
        nv = val
    return prop + ':' + nv

CONTROL_H = [36, 44, 48]      # botões: sm h-9 · md h-11 · lg h-12  (inputs/selects: h-11)
def _ctrl(n):
    return 36 if n <= 38 else (44 if n <= 45 else 48)

def _parse(style):
    out = []
    for part in style.split(';'):
        if ':' in part:
            k, v = part.split(':', 1); out.append([k.strip(), v.strip()])
    return out

def _get(d, k):
    for kk, v in d:
        if kk == k: return v
    return None

def _set(d, k, v):
    for it in d:
        if it[0] == k: it[1] = v; return
    d.append([k, v])

def _drop(d, *ks):
    d[:] = [it for it in d if it[0] not in ks]

def _ser(d):
    return ';'.join(k + ':' + v for k, v in d) + ';'

SOLID_BG = {TW['red-600'], TW['red-700'], TW['stone-900'], '{{accent}}', TW['green-700']}

def control(t):
    """Passo de componentes: reescreve cada elemento com o padrão documentado em Componentes.

    button / a.btn  -> Button (primary · secondary · outline · ghost × sm/md/lg/ícone), Chip ou Tab
    input / select  -> Input (h-11, px-4, text-base, rounded-lg, border-stone-300)
    span/p/div      -> Badge (h-6, px-2, rounded-md, text-xs bold) e Alert (warning / error)
    """
    m = re.match(r'<(\w+)', t); name = m.group(1).lower()
    sm = re.search(r'\bstyle="([^"]*)"', t)
    if not sm:
        return t
    d = _parse(sm.group(1))
    is_btn = name == 'button' or (name == 'a' and re.search(r'class="[^"]*\bbtn\b', t))
    bg = (_get(d, 'background-color') or _get(d, 'background') or '').lower()
    rad = _get(d, 'border-radius') or ''
    if name in ('input', 'select') and 'type="checkbox"' not in t and 'type="radio"' not in t:
        h = _get(d, 'height')
        if h and '{{' not in h and int(float(h[:-2])) >= 32: _set(d, 'height', '44px')
        _set(d, 'border-radius', '8px'); _set(d, 'font-size', '16px')
        if _get(d, 'padding') in ('0 12px', '0 14px', '0 16px'): _set(d, 'padding', '0 16px')
    elif is_btn:
        pressed = re.search(r'aria-pressed=|role="(radio|switch|checkbox|option)"', t)
        h = _get(d, 'height'); w = _get(d, 'width')
        hv = int(float(h[:-2])) if h and h.endswith('px') and '{{' not in h else None
        wv = int(float(w[:-2])) if w and w.endswith('px') and '{{' not in w else None
        square = hv is not None and hv == wv
        if pressed and rad == '9999px' and hv:
            # Chip (com borda) ou Tab segmentada (sem borda)
            _set(d, 'height', '36px'); _set(d, 'font-size', '14px')
            _set(d, 'padding', '0 12px' if 'solid' in (_get(d, 'border') or '') else '0 16px')
        elif hv and hv >= 30 and not pressed:
            size = 'sm' if hv <= 38 else ('md' if hv <= 45 else 'lg')
            nh = {'sm': 36, 'md': 44, 'lg': 48}[size]
            _set(d, 'height', '%dpx' % nh)
            if square: _set(d, 'width', '%dpx' % nh)
            _set(d, 'border-radius', '8px')
            fs = _get(d, 'font-size')
            if fs and '{{' not in fs: _set(d, 'font-size', '16px' if size == 'lg' else '14px')
            pad = _get(d, 'padding')
            if pad and re.fullmatch(r'0 \d+px', pad) and not square:
                _set(d, 'padding', '0 %dpx' % {'sm': 12, 'md': 16, 'lg': 24}[size])
            solid = any(x in bg for x in SOLID_BG)
            if _get(d, 'font-weight') or fs:
                _set(d, 'font-weight', '700' if solid else '500')
    elif name in ('span', 'strong'):
        fs = _get(d, 'font-size'); fw = _get(d, 'font-weight'); pad = _get(d, 'padding')
        if fs == '12px' and fw == '700' and rad and pad and not _get(d, 'width'):
            # Badge
            _drop(d, 'text-transform', 'letter-spacing', 'padding')
            _set(d, 'display', 'inline-flex'); _set(d, 'align-items', 'center'); _set(d, 'height', '24px')
            _set(d, 'padding', '0 8px'); _set(d, 'border-radius', '6px'); _set(d, 'line-height', '16px')
            if 'flex-shrink' not in dict(d): _set(d, 'flex-shrink', '0')
    if name in ('p', 'div'):
        col = (_get(d, 'color') or '').lower()
        if bg == TW['amber-100'] and col == TW['amber-800'] and _get(d, 'padding'):
            # Alert · warning
            _set(d, 'background', TW['amber-50']); _drop(d, 'background-color')
            _set(d, 'border', '1px solid ' + TW['amber-200']); _set(d, 'border-radius', '8px'); _set(d, 'padding', '12px 16px')
            _set(d, 'font-size', '14px'); _set(d, 'line-height', '20px')
        elif 'alertdialog' in t and bg == TW['red-100']:
            _set(d, 'background', TW['red-50']); _drop(d, 'background-color')
            _set(d, 'border', '1px solid ' + TW['red-200']); _set(d, 'border-radius', '8px'); _set(d, 'padding', '12px 16px')
    return t[:sm.start(1)] + _ser(d) + t[sm.end(1):]

def normalize(text, mobile=False):
    """Aplica os tokens a um artboard inteiro (HTML + CSS + JS)."""
    for old, tok in COLOR_MAP.items():
        text = re.sub('#' + old + r'(?![0-9A-Fa-f])', TW[tok], text, flags=re.I)
    for old, new in RGBA_MAP:
        text = text.replace(old, new)
    # sombras definidas em JS (valores de holes)
    text = text.replace("'0 1px 3px rgba(31,28,24,.12)'", "'" + SHADOW['sm'] + "'").replace("'0 0 0 3px ' + accent", "'0 0 0 2px ' + accent")
    text = re.sub(r'rgba\(31,28,24,\.\d+\)', 'rgb(0 0 0 / 0.1)', text)
    # página: conteúdo com max-w-7xl (1280) => respiro lateral de 80px (px-20) num quadro de 1440
    if not mobile:
        text = re.sub(r'padding:(\d+)px 64px(?=[;" ])', r'padding:\1px 80px', text)
        text = re.sub(r'padding:(\d+)px 64px (\d+)px', r'padding:\1px 80px \2px', text)
    else:
        text = re.sub(r'padding:(\d+)px 2[24]px(?=[;"])', r'padding:\1px 20px', text)
        text = re.sub(r'padding:(\d+)px 2[24]px (\d+)px', r'padding:\1px 20px \2px', text)
    # tags com class "jp" são glifos (caracteres japoneses em destaque): usam a escala completa;
    # todo o resto é texto e fica preso aos papéis tipográficos.
    def tag(m):
        t = m.group(0)
        _GLYPH[0] = bool(re.search(r'class="[^"]*\bjp\b', t))
        r = DECL.sub(_decl, t)
        _GLYPH[0] = False
        return control(r)
    held = []
    def hold(m):
        held.append(tag(m)); return '\x00%d\x00' % (len(held) - 1)
    text = re.sub(r'<[a-zA-Z][^<>]*\bstyle="[^"]*"[^<>]*>', hold, text)
    text = DECL.sub(_decl, text)
    return re.sub(r'\x00(\d+)\x00', lambda m: held[int(m.group(1))], text)
