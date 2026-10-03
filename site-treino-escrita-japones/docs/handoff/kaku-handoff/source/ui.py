"""Componentes compartilhados (equivalente em Python às variantes CVA de design-system/components.ts).

Cada constante/função devolve o estilo inline de um componente a partir dos tokens de ds.py.
Os estados (hover, focus, active, disabled, loading, error) ficam centralizados no <helmet> (common.HELMET).
"""
from ds import c, SHADOW

ACCENT = '{{accent}}'   # tweak do canvas; padrão = primary (red-600)

# ---- tipografia (papéis) ----
T = {
    'display': "font-family:'Shippori Mincho',serif;font-size:60px;line-height:1;font-weight:700;color:%s;margin:0;" % c('text-primary'),
    'h1': "font-family:'Shippori Mincho',serif;font-size:48px;line-height:1;font-weight:700;color:%s;margin:0;" % c('text-primary'),
    'h2': "font-family:'Shippori Mincho',serif;font-size:30px;line-height:36px;font-weight:700;color:%s;margin:0;" % c('text-primary'),
    'h3': 'font-size:20px;line-height:28px;font-weight:700;color:%s;margin:0;' % c('text-primary'),
    'h4': 'font-size:18px;line-height:28px;font-weight:700;color:%s;margin:0;' % c('text-primary'),
    'body': 'font-size:16px;line-height:24px;color:%s;margin:0;' % c('text-secondary'),
    'small': 'font-size:14px;line-height:20px;color:%s;margin:0;' % c('text-secondary'),
    'label': 'font-size:14px;line-height:20px;font-weight:700;color:%s;' % c('text-primary'),
    'caption': 'font-size:12px;line-height:16px;color:%s;' % c('text-muted'),
    'overline': 'margin:0;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:%s;' % c('text-muted'),
}
OVERLINE = T['overline']

# ---- superfícies ----
CARD = 'background:%s;border:1px solid %s;border-radius:12px;box-sizing:border-box;' % (c('surface'), c('border'))
CARD_RAISED = CARD + 'box-shadow:%s;' % SHADOW['sm']
PANEL = 'background:%s;border-radius:12px;' % c('surface-muted')

# ---- botões (variant × size) ----
_BTN_BASE = 'border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;white-space:nowrap;'
BTN_VARIANT = {
    'primary': 'border:none;background-color:%s;color:%s;font-weight:700;' % (ACCENT, c('text-inverse')),
    'secondary': 'border:none;background-color:%s;color:%s;font-weight:700;' % (c('secondary'), c('text-inverse')),
    'outline': 'border:1px solid %s;background:%s;color:%s;font-weight:500;' % (c('border'), c('surface'), c('text-primary')),
    'ghost': 'border:none;background:transparent;color:%s;font-weight:500;' % c('text-primary'),
    'danger': 'border:none;background-color:%s;color:%s;font-weight:700;' % (c('error'), c('text-inverse')),
    'link': 'border:none;background:transparent;color:%s;font-weight:700;padding:0;' % ACCENT,
}
BTN_SIZE = {'sm': 'height:36px;padding:0 12px;font-size:14px;', 'md': 'height:44px;padding:0 16px;font-size:14px;', 'lg': 'height:48px;padding:0 24px;font-size:16px;'}
def btn(variant='primary', size=None):
    return _BTN_BASE + BTN_VARIANT[variant] + (BTN_SIZE[size] if size else '')
BTN_R = btn('primary')
BTN_O = btn('outline')
BTN_S = btn('secondary')
BTN_SM_O = btn('outline', 'sm')

# ---- campos ----
INPUT = 'height:44px;box-sizing:border-box;padding:0 16px;border:1px solid %s;border-radius:8px;background:%s;font-size:16px;color:%s;outline:none;min-width:0;' % (c('border-strong'), c('surface'), c('text-primary'))
INPUT_BLOCK = 'width:100%;' + INPUT

# ---- chips / badges ----
def badge(tone='neutral'):
    fg, bg = {'neutral': ('text-secondary', 'surface-muted'), 'primary': ('error', 'primary-muted'), 'success': ('success', 'success-bg'),
              'warning': ('warning', 'warning-bg'), 'error': ('error', 'error-bg'), 'info': ('info', 'info-bg')}[tone]
    return 'display:inline-flex;align-items:center;gap:4px;height:24px;padding:0 8px;border-radius:6px;font-size:12px;line-height:16px;font-weight:700;background:%s;color:%s;' % (c(bg), c(fg))

def alert(tone='info'):
    fg, bg, bd = {'info': ('info', 'info-subtle', 'info-border'), 'success': ('success', 'success-subtle', 'success-border'),
                  'warning': ('warning', 'warning-subtle', 'warning-border'), 'error': ('error', 'error-subtle', 'error-border')}[tone]
    return 'display:flex;gap:12px;align-items:flex-start;padding:12px 16px;border-radius:8px;border:1px solid %s;background:%s;color:%s;font-size:14px;line-height:20px;' % (c(bd), c(bg), c(fg))
