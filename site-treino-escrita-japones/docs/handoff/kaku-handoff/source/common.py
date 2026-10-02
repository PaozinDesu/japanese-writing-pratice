ACC = '{{accent}}'

HELMET = r'''<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&amp;family=Shippori+Mincho:wght@500;700&amp;family=Zen+Kaku+Gothic+New:wght@400;500;700&amp;display=swap">
<style>
body{margin:0;background:#F7F4EE;color:#1F1C18;font-family:'Zen Kaku Gothic New',ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:#C8322F}a:hover{color:#9E2521}
button,input,select,textarea{font-family:inherit}
.jp{font-family:'Klee One','Hiragino Mincho ProN','Yu Mincho',serif}
.disp{font-family:'Shippori Mincho','Hiragino Mincho ProN','Yu Mincho',ui-serif,serif}
/* estados — Design System Kaku (Tailwind) */
.nl{transition:background-color .15s ease,color .15s ease}.nl:hover{background-color:#E6E0D6!important;color:#1F1C18!important}
.card{transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}.card:hover{transform:translateY(-2px);box-shadow:0 10px 15px -3px rgba(31,28,24,.1),0 4px 6px -4px rgba(31,28,24,.1)}
.btn{transition:transform .15s ease,filter .15s ease,background-color .15s ease,border-color .15s ease}.btn:hover{filter:brightness(.92)}.btn:active{transform:scale(.98);filter:brightness(.85)}
.soft:hover{background-color:#F7F4EE!important;filter:none}.soft:active{background-color:#E6E0D6!important}
button:disabled,.btn[aria-disabled="true"]{opacity:.5;cursor:not-allowed!important;filter:none!important;transform:none!important}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:2px solid #C8322F;outline-offset:2px}
input,select,textarea{transition:border-color .15s ease,box-shadow .15s ease}
input:hover,select:hover,textarea:hover{border-color:#D9D1C4}
input:focus,select:focus,textarea:focus{border-color:#C8322F!important;box-shadow:0 0 0 4px #F8E4E0;outline:none}
input[aria-invalid="true"]{border-color:#C8322F!important;background-color:#FDF3F1!important}
input:disabled,select:disabled,textarea:disabled{background-color:#F7F4EE!important;color:#B5ADA2!important;cursor:not-allowed}
input::placeholder,textarea::placeholder{color:#8A8278}
[data-tip]{position:relative}
[data-tip]:hover::after,[data-tip]:focus-visible::after{content:attr(data-tip);position:absolute;left:50%;bottom:calc(100% + 8px);transform:translateX(-50%);width:max-content;max-width:240px;padding:6px 8px;border-radius:6px;background:#1F1C18;color:#FFFFFF;font-size:12px;line-height:16px;font-weight:500;white-space:normal;text-align:center;z-index:50;pointer-events:none;box-shadow:0 4px 6px -1px rgba(31,28,24,.1)}
[data-page-scroll="flow"] main,[data-page-scroll="flow"] footer{flex-shrink:0}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{animation:spin .8s linear infinite}
@keyframes draw{to{stroke-dashoffset:0}}
.stk{animation:draw .6s cubic-bezier(.45,0,.25,1) both}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.rise{animation:rise .4s cubic-bezier(.2,.7,.2,1) both}
@keyframes pop{0%{transform:scale(.7);opacity:0}70%{transform:scale(1.05);opacity:1}100%{transform:scale(1)}}
.pop{animation:pop .45s ease both}
@keyframes shakeA{0%,100%{transform:none}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
@keyframes shakeB{0%,100%{transform:none}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
.shakeA{animation:shakeA .4s ease}.shakeB{animation:shakeB .4s ease}
@keyframes sheet{from{transform:translateY(100%)}to{transform:none}}
.sheet{animation:sheet .38s cubic-bezier(.2,.8,.2,1) both}
@keyframes fade{from{opacity:0}to{opacity:1}}
.fade{animation:fade .3s ease both}
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;animation-delay:0s!important;transition:none!important}}
</style>
</helmet>'''

ICONS = {
 'home': '<path d="M3.5 10.5 12 3.5l8.5 7"></path><path d="M5.5 9v11h13V9"></path><path d="M10 20v-5h4v5"></path>',
 'grid': '<rect x="3.5" y="3.5" width="7" height="7" rx="1.8"></rect><rect x="13.5" y="3.5" width="7" height="7" rx="1.8"></rect><rect x="3.5" y="13.5" width="7" height="7" rx="1.8"></rect><rect x="13.5" y="13.5" width="7" height="7" rx="1.8"></rect>',
 'brush': '<path d="M14.5 4.5l5 5L10 19l-5.5 1 1-5.5z"></path><path d="M12.5 6.5l5 5"></path>',
 'chart': '<path d="M3.5 20h17"></path><path d="M6.5 16v-5"></path><path d="M11.5 16V6"></path><path d="M16.5 16v-8"></path>',
 'search': '<circle cx="11" cy="11" r="6.5"></circle><path d="m20 20-4.2-4.2"></path>',
 'speaker': '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"></path><path d="M15.5 9a4 4 0 0 1 0 6"></path><path d="M18 6.5a7.5 7.5 0 0 1 0 11"></path>',
 'replay': '<path d="M4.5 12a7.5 7.5 0 1 0 2.3-5.4"></path><path d="M4.5 4v4.5H9"></path>',
 'undo': '<path d="M9 14 4 9l5-5"></path><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"></path>',
 'eraser': '<path d="M8 20h12"></path><path d="m4.6 15.4 8.8-8.8a2 2 0 0 1 2.8 0l2.2 2.2a2 2 0 0 1 0 2.8L11.5 18.5H7.7z"></path>',
 'check': '<path d="m5 12.5 4.5 4.5L19 7.5"></path>',
 'x': '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"></path>',
 'alert': '<path d="M12 7.5v5.5"></path><path d="M12 16.5v.5"></path>',
 'flame': '<path d="M12 21c-3.9 0-6.5-2.6-6.5-6.2 0-3.3 2.4-5.4 3.8-8.3.5 1.8 1.6 3 2.7 3.4.3-2.6 1.6-5 3.8-6.9.3 2.6 2.7 4.8 2.7 9 0 5.9-2.6 9-6.5 9z"></path>',
 'eye': '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"></path><circle cx="12" cy="12" r="3"></circle>',
 'eyeoff': '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"></path><path d="M4 4l16 16"></path>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"></path>',
 'back': '<path d="M19 12H5M11 6l-6 6 6 6"></path>',
 'user': '<circle cx="12" cy="8.5" r="3.8"></circle><path d="M4.5 20c1.2-3.6 4-5.5 7.5-5.5s6.3 1.9 7.5 5.5"></path>',
 'clock': '<circle cx="12" cy="12" r="8.5"></circle><path d="M12 7.5V12l3 2"></path>',
 'bulb': '<path d="M9.5 18h5M10.5 21h3"></path><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"></path>',
 'target': '<circle cx="12" cy="12" r="8.5"></circle><circle cx="12" cy="12" r="4.5"></circle><circle cx="12" cy="12" r="1"></circle>',
 'chev': '<path d="m6 9 6 6 6-6"></path>',
 'list': '<path d="M9 6h11M9 12h11M9 18h11"></path><path d="M4.5 6h.01M4.5 12h.01M4.5 18h.01"></path>',
 'logout': '<path d="M15 4.5h3.5a1.5 1.5 0 0 1 1.5 1.5v12a1.5 1.5 0 0 1-1.5 1.5H15"></path><path d="M10 16.5 5.5 12 10 7.5"></path><path d="M5.5 12H15"></path>',
 'plus': '<path d="M12 5v14M5 12h14"></path>',
 'trash': '<path d="M4.5 7h15"></path><path d="M9.5 7V4.5h5V7"></path><path d="M6.5 7l1 13h9l1-13"></path>',
 'pencil': '<path d="M4 20h4L19 9l-4-4L4 16z"></path>',
 'lock': '<rect x="5" y="10.5" width="14" height="10" rx="2"></rect><path d="M8.5 10.5V7.5a3.5 3.5 0 0 1 7 0v3"></path>',
 'history': '<path d="M4.5 12a7.5 7.5 0 1 0 2.3-5.4"></path><path d="M4.5 4v4.5H9"></path><path d="M12 8v4l3 2"></path>',
 'book': '<path d="M4 5.5A2 2 0 0 1 6 3.5h13v15H6a2 2 0 0 0-2 2z"></path><path d="M4 20.5V5.5"></path><path d="M8.5 8h6"></path>',
}

def ic(name, size=20, sw=1.8):
    return ('<svg aria-hidden="true" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
            % (size, size, sw, ICONS[name]))

MENU_ITEM = 'display:flex;align-items:center;gap:10px;height:44px;padding:0 12px;border-radius:10px;text-decoration:none;color:#1F1C18;font-size:15px;font-weight:500;'
def acct_area():
    return ('''<sc-if value="{{acct.in}}" hint-placeholder-val="{{false}}">
<sc-if value="{{acct.hasStreak}}" hint-placeholder-val="{{false}}"><span title="Dias seguidos com prática" style="display:flex;align-items:center;gap:6px;height:40px;padding:0 14px;border-radius:999px;background:#FFFFFF;border:1px solid #E6E0D6;font-size:14px;font-weight:700;color:#1F1C18;"><span style="display:flex;color:''' + ACC + ''';">''' + ic('flame', 18) + '''</span>{{acct.streakLabel}}</span></sc-if>
<button class="btn soft" onClick="{{acct.toggle}}" aria-haspopup="menu" aria-expanded="{{acct.openAttr}}" style="height:44px;padding:0 12px 0 4px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;gap:8px;cursor:pointer;font-size:14px;font-weight:700;">
<span aria-hidden="true" style="width:36px;height:36px;border-radius:999px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;">{{acct.initials}}</span>{{acct.name}}<span style="display:flex;color:#726B61;">''' + ic('chev', 16, 2) + '''</span></button>
<sc-if value="{{acct.open}}" hint-placeholder-val="{{false}}">
<div class="rise" role="menu" aria-label="Conta" style="position:absolute;right:0;top:52px;width:256px;box-sizing:border-box;padding:8px;background:#FFFFFF;border:1px solid #E6E0D6;border-radius:18px;box-shadow:0 22px 44px -22px rgba(31,28,24,.45);display:flex;flex-direction:column;gap:2px;z-index:40;">
<div style="padding:10px 12px 12px;border-bottom:1px solid #EFEAE1;margin-bottom:4px;display:flex;flex-direction:column;gap:2px;"><strong style="font-size:15px;">{{acct.full}}</strong><span style="font-size:13px;color:#726B61;overflow:hidden;text-overflow:ellipsis;">{{acct.email}}</span></div>
<a role="menuitem" href="Perfil.dc.html" onClick="{{acct.close}}" class="soft" style="''' + MENU_ITEM + '''"><span style="display:flex;color:#726B61;">''' + ic('user', 18) + '''</span>Perfil</a>
<a role="menuitem" href="Listas.dc.html" onClick="{{acct.close}}" class="soft" style="''' + MENU_ITEM + '''"><span style="display:flex;color:#726B61;">''' + ic('list', 18) + '''</span>Minhas listas</a>
<a role="menuitem" href="Progresso.dc.html" onClick="{{acct.close}}" class="soft" style="''' + MENU_ITEM + '''"><span style="display:flex;color:#726B61;">''' + ic('history', 18) + '''</span>Histórico</a>
<a role="menuitem" href="Main.dc.html" onClick="{{acct.logout}}" class="soft" style="''' + MENU_ITEM + '''border-top:1px solid #EFEAE1;border-radius:0 0 10px 10px;margin-top:4px;color:#A8292A;"><span style="display:flex;">''' + ic('logout', 18) + '''</span>Sair</a>
</div>
</sc-if>
</sc-if>
<sc-if value="{{acct.out}}" hint-placeholder-val="{{true}}">
<a href="Login.dc.html" onClick="{{acct.toLogin}}" class="btn soft" style="height:44px;padding:0 18px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;gap:8px;text-decoration:none;font-size:15px;font-weight:500;">''' + ic('user', 18) + '''Entrar</a>
<a href="Cadastro.dc.html" class="btn" style="height:44px;padding:0 18px;border-radius:999px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;text-decoration:none;font-size:15px;font-weight:700;">Criar conta</a>
</sc-if>''')

def macct():
    return ('''<sc-if value="{{acct.in}}" hint-placeholder-val="{{false}}"><a href="Perfil.dc.html" aria-label="Perfil de {{acct.full}}" style="display:flex;align-items:center;gap:6px;height:40px;padding:0 4px 0 12px;border-radius:999px;background:#FFFFFF;border:1px solid #E6E0D6;text-decoration:none;color:#1F1C18;font-size:13px;font-weight:700;"><span style="display:flex;color:''' + ACC + ''';">''' + ic('flame', 16) + '''</span>{{acct.streak}}<span aria-hidden="true" style="width:32px;height:32px;border-radius:999px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:12px;">{{acct.initials}}</span></a></sc-if>
<sc-if value="{{acct.out}}" hint-placeholder-val="{{true}}"><a href="Login.dc.html" onClick="{{acct.toLogin}}" style="display:flex;align-items:center;gap:6px;height:40px;padding:0 14px;border-radius:999px;background:#FFFFFF;border:1px solid #E6E0D6;text-decoration:none;color:#1F1C18;font-size:14px;font-weight:500;">''' + ic('user', 16) + '''Entrar</a></sc-if>''')

def nav(active):
    items = [('inicio', 'Início', 'Main.dc.html'), ('caracteres', 'Caracteres', 'Caracteres.dc.html'),
             ('praticar', 'Praticar', 'Praticar.dc.html'), ('progresso', 'Progresso', 'Progresso.dc.html')]
    links = ''
    for k, l, h in items:
        base = 'display:flex;align-items:center;height:36px;padding:0 16px;border-radius:999px;text-decoration:none;font-size:15px;'
        if k == active:
            links += '<a href="' + h + '" aria-current="page" class="nl" style="' + base + 'font-weight:700;color:' + ACC + ';background-color:#FFFFFF;box-shadow:inset 0 0 0 1px #E6E0D6;">' + l + '</a>\n'
        else:
            links += '<a href="' + h + '" class="nl" style="' + base + 'font-weight:500;color:#5E5850;">' + l + '</a>\n'
    return ('''<header style="height:64px;flex-shrink:0;position:relative;z-index:30;display:flex;align-items:center;justify-content:space-between;padding:0 64px;border-bottom:1px solid #E6E0D6;background:#F7F4EE;box-sizing:border-box;">
<a href="Main.dc.html" aria-label="Kaku, página inicial" style="display:flex;align-items:center;gap:12px;text-decoration:none;color:#1F1C18;">
<span class="jp" style="width:38px;height:38px;border-radius:9px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:600;">書</span>
<span class="disp" style="font-size:23px;font-weight:700;letter-spacing:.02em;">Kaku</span>
</a>
<nav aria-label="Principal" style="display:flex;gap:4px;padding:4px;border-radius:999px;background:#F2EEE6;">
''' + links + '''</nav>
<div style="display:flex;align-items:center;gap:10px;position:relative;">''' + acct_area() + '''
</div>
</header>''')

def tabbar(active):
    items = [('inicio', 'Início', 'Main.dc.html', 'home'), ('caracteres', 'Caracteres', 'CaracteresMobile.dc.html', 'grid'),
             ('praticar', 'Praticar', 'PraticarMobile.dc.html', 'brush'), ('progresso', 'Progresso', 'Progresso.dc.html', 'chart')]
    out = '<nav aria-label="Principal" style="position:absolute;left:0;bottom:0;width:390px;height:80px;box-sizing:border-box;padding:8px 8px 16px;background:#FFFFFF;border-top:1px solid #E6E0D6;display:flex;">\n'
    for k, l, h, i in items:
        col = ACC if k == active else '#726B61'
        cur = ' aria-current="page"' if k == active else ''
        fw = '700' if k == active else '500'
        out += '<a href="' + h + '"' + cur + ' style="flex-grow:1;flex-basis:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;text-decoration:none;color:' + col + ';font-size:11px;font-weight:' + fw + ';">' + ic(i, 22) + l + '</a>\n'
    return out + '</nav>'

def grid_svg(size, extra=''):
    return ('<svg aria-hidden="true" viewBox="0 0 100 100" style="position:absolute;left:0;top:0;width:%dpx;height:%dpx;%s">'
            '<line x1="50" y1="0" x2="50" y2="100" stroke="#E4DCCF" stroke-width="0.5" stroke-dasharray="2 2"></line>'
            '<line x1="0" y1="50" x2="100" y2="50" stroke="#E4DCCF" stroke-width="0.5" stroke-dasharray="2 2"></line>'
            '<line x1="0" y1="0" x2="100" y2="100" stroke="#EFE9DF" stroke-width="0.4" stroke-dasharray="1.5 2.5"></line>'
            '<line x1="100" y1="0" x2="0" y2="100" stroke="#EFE9DF" stroke-width="0.4" stroke-dasharray="1.5 2.5"></line>'
            '</svg>') % (size, size, extra)

def animbox(size, lst='strokes', ghost='#EDE7DD', sw=7):
    return ('<div style="position:relative;width:%dpx;height:%dpx;">' % (size, size) + grid_svg(size) +
     '<sc-for list="{{' + lst + '}}" as="g" hint-placeholder-count="3"><svg aria-hidden="true" viewBox="0 0 100 100" style="position:absolute;left:0;top:0;width:%dpx;height:%dpx;"><path d="{{g.d}}" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round"></path></svg></sc-for>' % (size, size, ghost, sw) +
     '<sc-for list="{{' + lst + '}}" as="s" hint-placeholder-count="3"><svg aria-hidden="true" viewBox="0 0 100 100" style="position:absolute;left:0;top:0;width:%dpx;height:%dpx;"><path class="stk" d="{{s.d}}" fill="none" stroke="#1F1C18" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:{{s.len}};stroke-dashoffset:{{s.len}};animation-delay:{{s.delay}};"></path></svg></sc-for>' % (size, size, sw) +
     '</div>')

def anim_pair(size, lst='strokes', sw=7):
    return ('<sc-if value="{{animA}}" hint-placeholder-val="{{true}}">' + animbox(size, lst, sw=sw) + '</sc-if>'
            '<sc-if value="{{animB}}" hint-placeholder-val="{{false}}">' + animbox(size, lst, sw=sw) + '</sc-if>')

def frames(lst='frames', box=60):
    inner = box - 8
    return ('<div style="display:flex;flex-wrap:wrap;gap:10px;"><sc-for list="{{' + lst + '}}" as="fr" hint-placeholder-count="3">'
     '<div style="display:flex;flex-direction:column;align-items:center;gap:4px;">'
     '<div style="position:relative;width:%dpx;height:%dpx;border:1px solid #E6E0D6;border-radius:10px;background:#FFFFFF;box-sizing:border-box;">' % (box, box) +
     '<sc-for list="{{fr.layers}}" as="ly" hint-placeholder-count="3"><svg aria-hidden="true" viewBox="0 0 100 100" style="position:absolute;left:3px;top:3px;width:%dpx;height:%dpx;"><path d="{{ly.d}}" fill="none" stroke="{{ly.c}}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"></path></svg></sc-for>' % (inner, inner) +
     '<svg aria-hidden="true" viewBox="0 0 100 100" style="position:absolute;left:3px;top:3px;width:%dpx;height:%dpx;"><circle cx="{{fr.sx}}" cy="{{fr.sy}}" r="7" fill="{{accent}}"></circle></svg>' % (inner, inner) +
     '</div><span style="font-size:12px;color:#726B61;">{{fr.n}}</span></div></sc-for></div>')

def fix_forms(body):
    """Formulários sem envio nativo (o iframe do canvas bloqueia submit): Enter e botão chamam o handler."""
    import re
    def one(m):
        h, inner = m.group(1), m.group(3)
        inner = inner.replace('type="submit"', 'type="button" onClick="{{' + h + '}}"')
        return '<form onKeyDown="{{' + h + 'Key}}"' + m.group(2) + inner + '</form>'
    return re.sub(r'<form onSubmit="\{\{([\w.]+)\}\}"([^>]*>)(.*?)</form>', one, body, flags=re.S)

# Quadro padrão das páginas desktop: 1920 × 1080 (16:9).
# O layout é desenhado em 1440 px de largura e ampliado uniformemente (×4/3) para 1920 px, então todos os
# elementos mantêm tamanho, espaçamento e posição relativos. 1080 / (4/3) = 810 px de altura lógica.
FRAME_W, FRAME_H, SCALE = 1920, 1080, 4 / 3
PAGE_H = round(FRAME_H / SCALE)   # 810

def standard_frame(body, w, h):
    """Páginas desktop com cabeçalho: quadro 1920×1080 (layout de 1440 ampliado ×4/3) e conteúdo rolando abaixo do cabeçalho."""
    import re
    b = body.strip()
    if w != 1440 or 'aria-label="Principal"' not in b or not b.startswith('<div style="width:1440px;height:'):
        return body, w, h
    b = re.sub(r'^<div style="width:1440px;height:\d+px;', '<div style="width:1440px;height:%dpx;transform:scale(%.7f);transform-origin:0 0;' % (PAGE_H, SCALE), b, count=1)
    i = b.index('</header>') + len('</header>')
    assert b.endswith('</div>')
    mode = 'fill' if re.search(r'<main style="[^"]*min-height:0', b[i:]) else 'flow'   # fill = colunas com rolagem própria
    b = (b[:i] + '\n<div data-page-scroll="' + mode + '" style="flex:1 1 0;min-height:0;overflow-y:auto;scrollbar-width:thin;display:flex;flex-direction:column;">'
         + b[i:-len('</div>')] + '</div>\n</div>')
    bg = re.search(r'background:([^;]+);', b).group(1)
    b = '<div style="width:%dpx;height:%dpx;overflow:hidden;background:%s;">\n' % (FRAME_W, FRAME_H, bg) + b + '\n</div>'
    return b, FRAME_W, FRAME_H

MOBILE_OF = {'Main': 'MainMobile', 'Caracteres': 'CaracteresMobile', 'Kanji': 'KanjiMobile', 'Praticar': 'PraticarMobile', 'Leitura': 'LeituraMobile',
             'Progresso': 'ProgressoMobile', 'Login': 'LoginMobile', 'Cadastro': 'CadastroMobile', 'Listas': 'ListasMobile', 'Perfil': 'PerfilMobile'}
def to_mobile_links(text):
    import re
    return re.sub(r'(?<![A-Za-z])(' + '|'.join(MOBILE_OF) + r')\.dc\.html', lambda m: MOBILE_OF[m.group(1)] + '.dc.html', text)

def page(title, lang, body, script, w, h, extra_head=''):
    import ds
    if w <= 480:
        body, script = to_mobile_links(body), to_mobile_links(script)
    body, w, h = standard_frame(body, w, h)
    body = fix_forms(body)
    props = '{"accent":{"editor":"color","default":"#C8322F","options":["#C8322F","#B3282D","#D4533F","#1F1C18"]},"$preview":{"width":%d,"height":%d}}' % (w, h)
    return ds.normalize('<!doctype html>\n<html lang="' + lang + '">\n<head>\n<meta charset="utf-8">\n<title>' + title + '</title>\n<script src="./support.js"></script>\n' + extra_head + '</head>\n<body>\n<x-dc>\n'
            + HELMET + '\n' + body + '\n</x-dc>\n<script type="text/x-dc" data-dc-script data-props=\'' + props + '\'>\n' + script + '\n</script>\n</body>\n</html>\n', mobile=(w <= 480))

JSDATA = r'''
const TYPES = { h: { label: 'Hiragana', fg: '#2E4C6E', bg: '#E3EAF2' }, k: { label: 'Katakana', fg: '#7A5210', bg: '#F4EAD6' }, j: { label: 'Kanji', fg: '#A8292A', bg: '#F8E4E0' } };
const DATA = [
  { c: 'い', t: 'h', r: 'い', ro: 'i', pt: 'sílaba “i”', en: 'syllable “i”', ex: 'いぬ', exk: '', exr: 'inu', expt: 'cão', exen: 'dog', orig: '以', p: ['M26 26 Q20 60 30 74 Q34 78 38 68', 'M68 34 Q80 50 78 66'] },
  { c: 'う', t: 'h', r: 'う', ro: 'u', pt: 'sílaba “u”', en: 'syllable “u”', ex: 'うみ', exk: '', exr: 'umi', expt: 'mar', exen: 'sea', orig: '宇', p: ['M40 14 Q52 18 60 22', 'M30 44 Q50 32 66 42 Q76 56 62 72 Q52 82 40 88'] },
  { c: 'く', t: 'h', r: 'く', ro: 'ku', pt: 'sílaba “ku”', en: 'syllable “ku”', ex: 'くも', exk: '', exr: 'kumo', expt: 'nuvem', exen: 'cloud', orig: '久', p: ['M64 14 Q40 36 30 50 Q42 64 64 86'] },
  { c: 'こ', t: 'h', r: 'こ', ro: 'ko', pt: 'sílaba “ko”', en: 'syllable “ko”', ex: 'こども', exk: '', exr: 'kodomo', expt: 'criança', exen: 'child', orig: '己', p: ['M30 30 Q52 26 68 30 Q64 34 60 38', 'M26 66 Q30 76 50 76 Q66 76 76 72'] },
  { c: 'し', t: 'h', r: 'し', ro: 'shi', pt: 'sílaba “shi”', en: 'syllable “shi”', ex: 'しお', exk: '', exr: 'shio', expt: 'sal', exen: 'salt', orig: '之', p: ['M36 14 L36 66 Q38 84 56 82 Q70 78 78 64'] },
  { c: 'つ', t: 'h', r: 'つ', ro: 'tsu', pt: 'sílaba “tsu”', en: 'syllable “tsu”', ex: 'つき', exk: '', exr: 'tsuki', expt: 'lua', exen: 'moon', orig: '川', p: ['M16 44 Q52 26 76 36 Q88 48 72 64 Q60 74 42 78'] },
  { c: 'て', t: 'h', r: 'て', ro: 'te', pt: 'sílaba “te”', en: 'syllable “te”', ex: 'て', exk: '', exr: 'te', expt: 'mão', exen: 'hand', orig: '天', p: ['M16 30 Q50 26 84 22 Q56 34 46 52 Q42 70 56 84 Q62 88 68 86'] },
  { c: 'へ', t: 'h', r: 'へ', ro: 'he', pt: 'sílaba “he”', en: 'syllable “he”', ex: 'へや', exk: '', exr: 'heya', expt: 'quarto', exen: 'room', orig: '部', p: ['M12 60 Q24 40 34 36 Q42 36 52 48 Q70 68 88 76'] },
  { c: 'り', t: 'h', r: 'り', ro: 'ri', pt: 'sílaba “ri”', en: 'syllable “ri”', ex: 'りんご', exk: '', exr: 'ringo', expt: 'maçã', exen: 'apple', orig: '利', p: ['M34 20 Q30 44 34 58 Q36 62 40 52', 'M64 18 Q72 40 68 62 Q62 80 44 90'] },
  { c: 'イ', t: 'k', r: 'イ', ro: 'i', pt: 'sílaba “i”', en: 'syllable “i”', ex: 'イルカ', exk: '', exr: 'iruka', expt: 'golfinho', exen: 'dolphin', orig: '伊', p: ['M64 12 Q50 40 16 62', 'M44 40 L44 90'] },
  { c: 'エ', t: 'k', r: 'エ', ro: 'e', pt: 'sílaba “e”', en: 'syllable “e”', ex: 'エレベーター', exk: '', exr: 'erebētā', expt: 'elevador', exen: 'elevator', orig: '江', p: ['M24 26 L76 26', 'M50 26 L50 78', 'M14 80 L86 80'] },
  { c: 'カ', t: 'k', r: 'カ', ro: 'ka', pt: 'sílaba “ka”', en: 'syllable “ka”', ex: 'カメラ', exk: '', exr: 'kamera', expt: 'câmera', exen: 'camera', orig: '加', p: ['M20 34 L76 34 Q76 70 66 84 Q62 88 56 84', 'M48 12 Q46 58 20 88'] },
  { c: 'コ', t: 'k', r: 'コ', ro: 'ko', pt: 'sílaba “ko”', en: 'syllable “ko”', ex: 'コーヒー', exk: '', exr: 'kōhī', expt: 'café', exen: 'coffee', orig: '己', p: ['M22 26 L76 26 L76 76', 'M22 76 L76 76'] },
  { c: 'ニ', t: 'k', r: 'ニ', ro: 'ni', pt: 'sílaba “ni”', en: 'syllable “ni”', ex: 'ニュース', exk: '', exr: 'nyūsu', expt: 'notícias', exen: 'news', orig: '二', p: ['M28 32 L72 32', 'M14 72 L86 72'] },
  { c: 'ト', t: 'k', r: 'ト', ro: 'to', pt: 'sílaba “to”', en: 'syllable “to”', ex: 'トマト', exk: '', exr: 'tomato', expt: 'tomate', exen: 'tomato', orig: '止', p: ['M40 12 L40 90', 'M42 44 Q60 50 72 60'] },
  { c: 'ハ', t: 'k', r: 'ハ', ro: 'ha', pt: 'sílaba “ha”', en: 'syllable “ha”', ex: 'ハンバーガー', exk: '', exr: 'hanbāgā', expt: 'hambúrguer', exen: 'hamburger', orig: '八', p: ['M38 28 Q34 58 14 78', 'M60 26 Q74 50 88 76'] },
  { c: 'ロ', t: 'k', r: 'ロ', ro: 'ro', pt: 'sílaba “ro”', en: 'syllable “ro”', ex: 'ロボット', exk: '', exr: 'robotto', expt: 'robô', exen: 'robot', orig: '呂', p: ['M26 24 L26 80', 'M26 24 L76 24 L76 80', 'M26 78 L76 78'] },
  { c: 'ミ', t: 'k', r: 'ミ', ro: 'mi', pt: 'sílaba “mi”', en: 'syllable “mi”', ex: 'ミルク', exk: '', exr: 'miruku', expt: 'leite', exen: 'milk', orig: '三', p: ['M28 18 Q50 22 68 32', 'M32 44 Q52 48 66 56', 'M22 68 Q50 74 74 86'] },
  { c: '一', t: 'j', r: 'ひと(つ)', ro: 'hito(tsu)', pt: 'um', en: 'one', on: [['イチ', 'ichi'], ['イツ', 'itsu']], kun: [['ひと(つ)', 'hito(tsu)']], ex: '一月', exk: 'いちがつ', exr: 'ichigatsu', expt: 'janeiro', exen: 'January', tip: 'Um único traço horizontal representa o número um.', p: ['M14 51 Q50 48 86 50'] },
  { c: '二', t: 'j', r: 'ふた(つ)', ro: 'futa(tsu)', pt: 'dois', en: 'two', on: [['ニ', 'ni']], kun: [['ふた(つ)', 'futa(tsu)']], ex: '二月', exk: 'にがつ', exr: 'nigatsu', expt: 'fevereiro', exen: 'February', tip: 'Dois traços horizontais; o de baixo é mais longo.', p: ['M28 32 L72 31', 'M14 70 L86 68'] },
  { c: '三', t: 'j', r: 'み(っつ)', ro: 'mi(ttsu)', pt: 'três', en: 'three', on: [['サン', 'san']], kun: [['み(っつ)', 'mi(ttsu)']], ex: '三月', exk: 'さんがつ', exr: 'sangatsu', expt: 'março', exen: 'March', tip: 'Três traços; o do meio é o mais curto.', p: ['M24 24 L76 23', 'M30 50 L70 49', 'M14 78 L86 77'] },
  { c: '十', t: 'j', r: 'とお', ro: 'tō', pt: 'dez', en: 'ten', on: [['ジュウ', 'jū']], kun: [['とお', 'tō']], ex: '十月', exk: 'じゅうがつ', exr: 'jūgatsu', expt: 'outubro', exen: 'October', tip: 'Uma cruz: o traço horizontal vem primeiro.', p: ['M14 48 L86 47', 'M50 12 L50 90'] },
  { c: '人', t: 'j', r: 'ひと', ro: 'hito', pt: 'pessoa', en: 'person', on: [['ジン', 'jin'], ['ニン', 'nin']], kun: [['ひと', 'hito']], ex: '日本人', exk: 'にほんじん', exr: 'nihonjin', expt: 'japonês (pessoa)', exen: 'Japanese person', tip: 'Uma pessoa de pé, vista de lado.', p: ['M52 12 Q50 55 14 86', 'M50 44 Q62 72 88 86'] },
  { c: '大', t: 'j', r: 'おお(きい)', ro: 'ō(kii)', pt: 'grande', en: 'big', on: [['ダイ', 'dai'], ['タイ', 'tai']], kun: [['おお(きい)', 'ō(kii)']], ex: '大人', exk: 'おとな', exr: 'otona', expt: 'adulto', exen: 'adult', tip: 'Uma pessoa de braços abertos: “grande”.', p: ['M16 38 L84 37', 'M50 10 Q50 60 16 88', 'M52 50 Q64 74 88 88'] },
  { c: '口', t: 'j', r: 'くち', ro: 'kuchi', pt: 'boca', en: 'mouth', on: [['コウ', 'kō'], ['ク', 'ku']], kun: [['くち', 'kuchi']], ex: '出口', exk: 'でぐち', exr: 'deguchi', expt: 'saída', exen: 'exit', tip: 'Uma boca aberta, em forma de quadrado.', p: ['M24 26 L26 80', 'M24 26 L76 25 L74 80', 'M26 76 L74 76'] },
  { c: '日', t: 'j', r: 'ひ', ro: 'hi', pt: 'sol, dia', en: 'sun, day', on: [['ニチ', 'nichi'], ['ジツ', 'jitsu']], kun: [['ひ', 'hi'], ['か', 'ka']], ex: '日本', exk: 'にほん', exr: 'nihon', expt: 'Japão', exen: 'Japan', tip: 'Originalmente, um desenho do sol.', p: ['M28 14 L29 88', 'M28 14 L72 13 L71 88', 'M29 50 L71 50', 'M29 84 L71 84'] },
  { c: '中', t: 'j', r: 'なか', ro: 'naka', pt: 'meio, dentro', en: 'middle, inside', on: [['チュウ', 'chū']], kun: [['なか', 'naka']], ex: '中国', exk: 'ちゅうごく', exr: 'chūgoku', expt: 'China', exen: 'China', tip: 'Uma linha que atravessa o centro de uma caixa.', p: ['M20 32 L22 66', 'M20 32 L80 31 L78 66', 'M22 62 L78 62', 'M50 10 L50 92'] },
  { c: '山', t: 'j', r: 'やま', ro: 'yama', pt: 'montanha', en: 'mountain', on: [['サン', 'san']], kun: [['やま', 'yama']], ex: '富士山', exk: 'ふじさん', exr: 'fujisan', expt: 'Monte Fuji', exen: 'Mount Fuji', tip: 'Três picos de uma montanha.', p: ['M50 12 L50 80', 'M20 36 L20 80 L80 80', 'M80 34 L80 88'] },
  { c: '川', t: 'j', r: 'かわ', ro: 'kawa', pt: 'rio', en: 'river', on: [['セン', 'sen']], kun: [['かわ', 'kawa']], ex: '小川', exk: 'おがわ', exr: 'ogawa', expt: 'riacho', exen: 'stream', tip: 'Água correndo entre duas margens.', p: ['M28 16 Q28 60 16 88', 'M50 22 L50 72', 'M78 12 L78 90'] },
  { c: '木', t: 'j', r: 'き', ro: 'ki', pt: 'árvore, madeira', en: 'tree, wood', on: [['モク', 'moku'], ['ボク', 'boku']], kun: [['き', 'ki']], ex: '木曜日', exk: 'もくようび', exr: 'mokuyōbi', expt: 'quinta-feira', exen: 'Thursday', tip: 'Uma árvore com galhos e raízes.', p: ['M14 36 L86 35', 'M50 10 L50 92', 'M48 38 Q36 64 14 80', 'M52 38 Q66 62 88 78'] }
];
function nums(d) { return (d.match(/-?\d+(\.\d+)?/g) || []).map(Number); }
function plen(d) { const n = nums(d); let L = 0; for (let i = 2; i + 1 < n.length; i += 2) L += Math.hypot(n[i] - n[i - 2], n[i + 1] - n[i - 1]); return Math.ceil(L) + 6; }
function startPt(d) { const n = nums(d); return { x: n[0], y: n[1] }; }
function norm(s) { return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
function strokesOf(d, gap) { return d.p.map((p, i) => ({ d: p, len: plen(p), delay: (i * (gap || 0.7)).toFixed(2) + 's' })); }
function framesOf(d, accent) { return d.p.map((_, i) => { const s = startPt(d.p[i]); return { n: i + 1, sx: s.x, sy: s.y, layers: d.p.map((p, j) => ({ d: p, c: j < i ? '#1F1C18' : (j === i ? accent : '#E6E0D6') })) }; }); }
function decorate(d) { const T = TYPES[d.t]; return Object.assign({}, d, { tl: T.label, tf: T.fg, tb: T.bg, n: d.p.length }); }
function speakText(d) { return d.t === 'j' ? d.r.replace(/[()]/g, '') : d.c; }
function say(text) { try { const u = new SpeechSynthesisUtterance(text); u.lang = 'ja-JP'; u.rate = 0.85; window.speechSynthesis.cancel(); window.speechSynthesis.speak(u); } catch (e) {} }
'''

# Drawing + recognition engine, parameterised by canvas size CS
def engine(cs):
    return r'''
const CS = ''' + str(cs) + r''', RES = 2, N = 100;
function bboxOf(paths) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; paths.forEach((p) => { const n = nums(p); for (let i = 0; i + 1 < n.length; i += 2) { x0 = Math.min(x0, n[i]); x1 = Math.max(x1, n[i]); y0 = Math.min(y0, n[i + 1]); y1 = Math.max(y1, n[i + 1]); } }); return { x0, y0, x1, y1 }; }
const Ink = {
  init(self) {
    self.strokes = []; self.cur = null; self.cv = null; self.ctx = null;
    self.setCanvas = (el) => { if (!el || el === self.cv) return; self.cv = el; el.width = CS * RES; el.height = CS * RES; self.ctx = el.getContext('2d'); Ink.redraw(self); };
    self.onDown = (e) => { if (self.state.result || !self.ctx) return; e.preventDefault(); try { self.cv.setPointerCapture(e.pointerId); } catch (_) {} const p = Ink.pt(self, e); p.w = 22; self.cur = [p]; Ink.dot(self, p); };
    self.onMove = (e) => { if (!self.cur) return; e.preventDefault(); const p = Ink.pt(self, e); const a = self.cur[self.cur.length - 1]; const dist = Math.hypot(p.x - a.x, p.y - a.y); if (dist < 2) return; const v = dist / Math.max(1, p.t - a.t); const tw = Math.max(13, Math.min(28, 30 - v * 5)); p.w = a.w * 0.65 + tw * 0.35; self.cur.push(p); Ink.seg(self, a, p); };
    self.onUp = () => { if (!self.cur) return; self.strokes.push(self.cur); self.cur = null; self.setState({ count: self.strokes.length, warn: 0 }); };
    self.wipe = () => { self.strokes = []; self.cur = null; Ink.redraw(self); };
  },
  pt(self, e) { const r = self.cv.getBoundingClientRect(); return { x: (e.clientX - r.left) * (CS * RES / r.width), y: (e.clientY - r.top) * (CS * RES / r.height), t: e.timeStamp || Date.now() }; },
  seg(self, a, b) { const c = self.ctx; c.strokeStyle = '#1F1C18'; c.lineCap = 'round'; c.lineJoin = 'round'; c.lineWidth = (a.w + b.w) / 2 * (CS / 560 + 0.3); c.beginPath(); c.moveTo(a.x, a.y); c.lineTo(b.x, b.y); c.stroke(); },
  dot(self, p) { const c = self.ctx; c.fillStyle = '#1F1C18'; c.beginPath(); c.arc(p.x, p.y, p.w / 2 * (CS / 560 + 0.3), 0, Math.PI * 2); c.fill(); },
  redraw(self) { if (!self.ctx) return; self.ctx.clearRect(0, 0, CS * RES, CS * RES); self.strokes.forEach((s) => { Ink.dot(self, s[0]); for (let i = 1; i < s.length; i++) Ink.seg(self, s[i - 1], s[i]); }); },
  mask(self, fn) { const c = self.off || (self.off = document.createElement('canvas')); c.width = N; c.height = N; const x = c.getContext('2d'); x.lineCap = 'round'; x.lineJoin = 'round'; x.strokeStyle = '#000'; fn(x); const d = x.getImageData(0, 0, N, N).data; const m = new Uint8Array(N * N); for (let i = 0; i < N * N; i++) m[i] = d[i * 4 + 3] > 40 ? 1 : 0; return m; },
  userBox(self) { const k = N / (CS * RES); let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; self.strokes.forEach((s) => s.forEach((p) => { x0 = Math.min(x0, p.x * k); x1 = Math.max(x1, p.x * k); y0 = Math.min(y0, p.y * k); y1 = Math.max(y1, p.y * k); })); return { x0, y0, x1, y1 }; },
  score(self, d) {
    const tb = bboxOf(d.p), ub = Ink.userBox(self), k = N / (CS * RES);
    const us = Math.max(ub.x1 - ub.x0, ub.y1 - ub.y0, 1), ts = Math.max(tb.x1 - tb.x0, tb.y1 - tb.y0, 1);
    const s = Math.max(0.5, Math.min(2.5, ts / us));
    const ucx = (ub.x0 + ub.x1) / 2, ucy = (ub.y0 + ub.y1) / 2, tcx = (tb.x0 + tb.x1) / 2, tcy = (tb.y0 + tb.y1) / 2;
    const map = (p) => [(p.x * k - ucx) * s + tcx, (p.y * k - ucy) * s + tcy];
    const um = (lw) => Ink.mask(self, (x) => { x.lineWidth = lw; self.strokes.forEach((st) => { x.beginPath(); const a = map(st[0]); x.moveTo(a[0], a[1]); if (st.length === 1) x.lineTo(a[0] + 0.1, a[1]); for (let i = 1; i < st.length; i++) { const b = map(st[i]); x.lineTo(b[0], b[1]); } x.stroke(); }); });
    const tm = (lw) => Ink.mask(self, (x) => { x.lineWidth = lw; d.p.forEach((p) => x.stroke(new Path2D(p))); });
    const U4 = um(4), U16 = um(16), T4 = tm(4), T16 = tm(16);
    let a = 0, ab = 0, b = 0, bb = 0;
    for (let i = 0; i < N * N; i++) { if (U4[i]) { a++; if (T16[i]) ab++; } if (T4[i]) { b++; if (U16[i]) bb++; } }
    const P = a ? ab / a : 0, R = b ? bb / b : 0, f = P + R ? 2 * P * R / (P + R) : 0, sd = Math.abs(self.strokes.length - d.p.length);
    return { f, sd, total: f - 0.06 * sd };
  },
  evaluate(self, target) {
    let best = null, bs = null;
    DATA.forEach((d) => { const s = Ink.score(self, d); if (!bs || s.total > bs.total) { best = d; bs = s; } });
    const ts = Ink.score(self, target);
    let id = ts.total >= bs.total - 0.05 ? target : best;
    const idf = id === target ? ts.f : bs.f;
    if (idf < 0.45) id = null;
    const shapeOk = ts.f >= 0.68, strokesOk = ts.sd === 0;
    const verdict = id === target && shapeOk && strokesOk ? 'ok' : (id === target ? 'almost' : 'no');
    let img = '';
    try { img = self.cv.toDataURL('image/png'); } catch (e) {}
    return { id: id ? id.c : null, verdict, sim: Math.round(ts.f * 100), user: self.strokes.length, exp: target.p.length, shapeOk, img };
  }
};
function verdictView(r, target, accent) {
  if (!r) return null;
  const idc = r.id ? DATA.find((x) => x.c === r.id) : null;
  const tr = (n) => n + (n === 1 ? ' traço' : ' traços');
  if (r.verdict === 'ok') return { label: 'Correto!', sub: 'Seu desenho corresponde ao caractere pedido.', fg: '#4E6E3A', bg: '#E7EEDF', ok: true, al: false, no: false, idc };
  if (r.verdict === 'almost') return { label: 'Quase lá', sub: r.shapeOk ? 'Forma reconhecida, mas você usou ' + tr(r.user) + ' — o esperado são ' + tr(r.exp) + '.' : 'Reconhecemos o caractere, mas a forma ainda pode ficar mais precisa.', fg: '#7A5210', bg: '#F4EAD6', ok: false, al: true, no: false, idc };
  return { label: 'Não corresponde', sub: idc ? 'Identificamos “' + idc.c + '” em vez de “' + target.c + '”. Observe a referência e tente de novo.' : 'Não conseguimos reconhecer o desenho. Tente de novo com calma.', fg: '#A8292A', bg: '#F8E4E0', ok: false, al: false, no: true, idc };
}
'''


import os as _os
_JS = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'js')
def js(name):
    return open(_os.path.join(_JS, name)).read()

def acctify(script):
    """Faz o renderVals de qualquer página devolver também a área do usuário (cabeçalho)."""
    assert script.count('renderVals() {') == 1, 'renderVals must appear once'
    return script.replace('renderVals() {', 'renderVals() { return withAcct(this, this._rv()); }\n  _rv() {', 1)

def spinner(size=18, color='currentColor'):
    """Loading state padrão (Tailwind: animate-spin)."""
    return ('<svg class="spin" aria-hidden="true" width="%d" height="%d" viewBox="0 0 24 24" fill="none">'
            '<circle cx="12" cy="12" r="9" stroke="%s" stroke-opacity=".25" stroke-width="3"></circle>'
            '<path d="M21 12a9 9 0 0 0-9-9" stroke="%s" stroke-width="3" stroke-linecap="round"></path></svg>') % (size, size, color, color)
