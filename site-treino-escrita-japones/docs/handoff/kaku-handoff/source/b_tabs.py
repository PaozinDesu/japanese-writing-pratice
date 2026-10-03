from common import *
from ds import c

def mode_tabs(active, mobile=False):
    """Abas Escrita | Leitura (componente Tabs), compartilhadas com a tela Praticar."""
    items = [('escrita', 'Escrita', 'PraticarMobile.dc.html' if mobile else 'Praticar.dc.html', 'brush'), ('leitura', 'Leitura', 'LeituraMobile.dc.html' if mobile else 'Leitura.dc.html', 'book')]
    out = '<nav aria-label="Modo de prática" style="display:flex;gap:4px;padding:4px;background:%s;border-radius:9999px;align-self:flex-start;">' % c('border')
    for k, label, href, icon in items:
        on = k == active
        out += ('<a href="' + href + '"' + (' aria-current="page"' if on else '') + ' style="height:36px;padding:0 16px;border-radius:9999px;display:flex;align-items:center;gap:8px;text-decoration:none;font-size:14px;'
                + ('background:#ffffff;color:%s;font-weight:700;box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05);' % c('text-primary') if on else 'color:%s;font-weight:500;' % c('text-secondary'))
                + '">' + ic(icon, 16) + label + '</a>')
    return out + '</nav>'

