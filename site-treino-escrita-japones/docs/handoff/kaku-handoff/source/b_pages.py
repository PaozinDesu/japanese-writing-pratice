from common import *
from b_chars import DBJS, DATA_HEAD

from ui import OVERLINE as LBL
from ui import CARD

def script_card(glyph, name, tb, tf, key, note):
    h = 'sc.' + key + '.'
    return '''<div class="card" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:18px;color:#1F1C18;">
<div style="display:flex;align-items:center;gap:16px;">
<span class="jp" style="width:64px;height:64px;border-radius:16px;background:''' + tb + ''';color:''' + tf + ''';display:flex;align-items:center;justify-content:center;font-size:38px;">''' + glyph + '''</span>
<div style="display:flex;flex-direction:column;gap:2px;"><span style="font-size:19px;font-weight:700;">''' + name + '''</span><span style="font-size:14px;color:#726B61;">''' + note + '''</span></div>
</div>
<div style="display:flex;flex-direction:column;gap:8px;">
<div style="display:flex;justify-content:space-between;font-size:14px;"><span style="color:#5E5850;">{{''' + h + '''line}}</span><strong>{{''' + h + '''pct}}</strong></div>
<div style="height:8px;border-radius:999px;background:#EFEAE1;overflow:hidden;"><div style="height:8px;width:{{''' + h + '''w}};border-radius:999px;background-color:''' + ACC + ''';"></div></div>
</div>
<a href="Praticar.dc.html" onClick="{{''' + h + '''go}}" style="display:flex;align-items:center;gap:6px;font-size:15px;font-weight:700;text-decoration:none;">Praticar ''' + name + ic('arrow', 18, 2) + '''</a>
</div>'''

def step(n, icon, title, text):
    return '''<div style="display:flex;flex-direction:column;gap:14px;padding:28px;border-radius:24px;background:#FFFFFF;border:1px solid #E6E0D6;">
<div style="display:flex;align-items:center;justify-content:space-between;">
<span style="width:48px;height:48px;border-radius:14px;background:#FBEDEA;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic(icon, 24) + '''</span>
<span class="disp" style="font-size:40px;font-weight:700;color:#E6E0D6;line-height:1;">''' + n + '''</span>
</div>
<h3 style="margin:0;font-size:20px;font-weight:700;">''' + title + '''</h3>
<p style="margin:0;font-size:15px;line-height:1.6;color:#5E5850;">''' + text + '''</p>
</div>'''

body_m = '''<div style="width:1440px;height:1580px;box-sizing:border-box;background:#F7F4EE;display:flex;flex-direction:column;overflow:hidden;">
''' + nav('inicio') + '''
<main style="display:flex;flex-direction:column;gap:72px;padding:72px 64px 56px;">
<section style="display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:72px;align-items:center;">
<div style="display:flex;flex-direction:column;gap:28px;">
<span style="align-self:flex-start;display:flex;align-items:center;gap:8px;height:34px;padding:0 14px;border-radius:999px;background:#FBEDEA;color:#A8292A;font-size:14px;font-weight:700;"><span class="jp" style="font-size:16px;">書く</span>kaku · escrever</span>
<h1 class="disp" style="margin:0;font-size:66px;line-height:1.12;font-weight:700;letter-spacing:-.005em;">Aprenda a escrever japonês, traço a traço.</h1>
<p style="margin:0;font-size:19px;line-height:1.65;color:#5E5850;max-width:560px;">Explore Hiragana, Katakana e Kanji, pratique à mão livre no quadro e receba feedback imediato sobre cada caractere que você escreve.</p>
<div style="display:flex;gap:12px;">
<a href="Praticar.dc.html" class="btn" style="height:56px;padding:0 28px;border-radius:14px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;gap:10px;text-decoration:none;font-size:16px;font-weight:700;box-shadow:0 10px 22px -12px ''' + ACC + ''';">''' + ic('brush', 20) + '''Começar a praticar</a>
<a href="Caracteres.dc.html" class="btn soft" style="height:56px;padding:0 26px;border-radius:14px;border:1px solid #D9D1C4;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;gap:10px;text-decoration:none;font-size:16px;font-weight:500;">''' + ic('grid', 20) + '''Explorar caracteres</a>
</div>
<div style="display:flex;gap:28px;padding-top:8px;">
<div style="display:flex;align-items:center;gap:10px;"><span class="jp" style="font-size:30px;color:#2E4C6E;">あ</span><span style="display:flex;flex-direction:column;"><strong style="font-size:15px;">Hiragana</strong><span style="font-size:13px;color:#726B61;">46 básicos</span></span></div>
<div style="display:flex;align-items:center;gap:10px;"><span class="jp" style="font-size:30px;color:#7A5210;">ア</span><span style="display:flex;flex-direction:column;"><strong style="font-size:15px;">Katakana</strong><span style="font-size:13px;color:#726B61;">46 básicos</span></span></div>
<div style="display:flex;align-items:center;gap:10px;"><span class="jp" style="font-size:30px;color:#A8292A;">字</span><span style="display:flex;flex-direction:column;"><strong style="font-size:15px;">Kanji</strong><span style="font-size:13px;color:#726B61;">2.136 de uso comum</span></span></div>
</div>
</div>
<div style="''' + CARD + '''border-radius:28px;padding:28px;display:flex;flex-direction:column;gap:20px;box-shadow:0 30px 60px -40px rgba(31,28,24,.35);">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="''' + LBL + '''">Caractere do dia</span>
<span style="font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:4px 10px;border-radius:999px;background:#F8E4E0;color:#A8292A;">Kanji</span>
</div>
<div style="display:flex;justify-content:center;padding:20px 0;background:#FBF9F5;border-radius:20px;border:1px solid #EFEAE1;">
''' + anim_pair(260) + '''
</div>
<div style="display:flex;align-items:flex-end;justify-content:space-between;">
<div style="display:flex;flex-direction:column;gap:4px;">
<span style="display:flex;align-items:baseline;gap:10px;"><span class="jp" style="font-size:28px;font-weight:600;">やま</span><span style="font-size:17px;color:#5E5850;">yama</span></span>
<span style="font-size:16px;">montanha <span style="color:#726B61;">· mountain</span></span>
</div>
<div style="display:flex;gap:8px;">
<button class="btn soft" onClick="{{replay}}" aria-label="Repetir animação da escrita" style="width:48px;height:48px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('replay', 20) + '''</button>
<button class="btn soft" onClick="{{speak}}" aria-label="Ouvir pronúncia" style="width:48px;height:48px;border-radius:999px;border:1px solid #E6E0D6;background:#FFFFFF;color:#1F1C18;display:flex;align-items:center;justify-content:center;cursor:pointer;">''' + ic('speaker', 20) + '''</button>
</div>
</div>
<a href="Praticar.dc.html" onClick="{{practiceYama}}" class="btn" style="height:52px;border-radius:14px;background-color:#1F1C18;color:#FFFFFF;display:flex;align-items:center;justify-content:center;gap:10px;text-decoration:none;font-size:15px;font-weight:700;">Praticar 山 agora''' + ic('arrow', 18, 2) + '''</a>
</div>
</section>

<section aria-labelledby="cont" style="display:flex;flex-direction:column;gap:24px;">
<div style="display:flex;justify-content:space-between;align-items:flex-end;">
<h2 id="cont" class="disp" style="margin:0;font-size:32px;font-weight:700;">{{contTitle}}</h2>
<a href="Progresso.dc.html" style="font-size:15px;font-weight:700;text-decoration:none;display:flex;align-items:center;gap:6px;">Ver progresso''' + ic('arrow', 16, 2) + '''</a>
</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;">
''' + script_card('あ', 'Hiragana', '#E3EAF2', '#2E4C6E', 'hiragana', 'Silabário fonético') + '''
''' + script_card('ア', 'Katakana', '#F4EAD6', '#7A5210', 'katakana', 'Palavras estrangeiras') + '''
''' + script_card('字', 'Kanji', '#F8E4E0', '#A8292A', 'kanji', 'Os 2.136 de uso comum') + '''
</div>
</section>

<section aria-labelledby="como" style="display:flex;flex-direction:column;gap:24px;">
<h2 id="como" class="disp" style="margin:0;font-size:32px;font-weight:700;">Como funciona</h2>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;">
''' + step('一', 'book', 'Explore', 'Conheça cada caractere: leitura, romaji, significado em português e inglês e a ordem correta dos traços.') + '''
''' + step('二', 'brush', 'Pratique', 'Escreva no quadro com o mouse ou o dedo. Ao clicar em Pronto, o Kaku identifica o caractere e compara com o exercício.') + '''
''' + step('三', 'chart', 'Acompanhe', 'Veja sua sequência de estudos, a precisão por caractere e o que vale revisar na próxima sessão.') + '''
</div>
</section>
</main>
<footer style="margin-top:auto;display:flex;justify-content:space-between;align-items:center;padding:24px 64px;border-top:1px solid #E6E0D6;font-size:14px;color:#726B61;">
<span><span class="disp" style="font-weight:700;color:#1F1C18;">Kaku</span> · 書く</span>
<span>Feito para quem está aprendendo a escrever em japonês.</span>
</footer>
</div>'''

script_m = acctify(JSDATA + DBJS[DBJS.index('const KTYPES'):] + js('account.js') + r'''
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'Main.dc.html'; this.state = { anim: 0 }; }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
    const d = DATA.find((x) => x.c === '山');
    const D = kdb(), u = Auth.current(), data = u ? UD.load(u) : null;
    const hist = data ? charHistory(data) : {};
    const sc = {};
    ['hiragana', 'katakana', 'kanji'].forEach((cat) => {
      const total = D ? D.characters.filter((e) => e.category === cat).length : ({ hiragana: 115, katakana: 139, kanji: 2136 })[cat];
      const ok = Object.keys(hist).filter((id) => catOf(id) === cat && hist[id].ok > 0).length;
      const p = total ? ok / total : 0;
      sc[cat] = { line: u ? fmtInt(ok) + ' de ' + fmtInt(total) + ' já acertados' : fmtInt(total) + ' caracteres', pct: u ? (p > 0 && p < 0.01 ? '<1%' : Math.round(p * 100) + '%') : '', w: (u ? Math.max(ok ? 1 : 0, p * 100) : 0) + '%', go: () => Intent.set({ kind: 'filters', cats: [cat] }) };
    });
    return {
      accent, strokes: strokesOf(d, 0.8), animA: this.state.anim % 2 === 0, animB: this.state.anim % 2 === 1,
      replay: () => this.setState({ anim: this.state.anim + 1 }), speak: () => say('やま'),
      sc, contTitle: u && data.sessions.length ? 'Continue de onde parou' : 'Por onde começar',
      practiceYama: () => Intent.set({ kind: 'chars', chars: ['kanji:山'], label: 'Caractere 山' })
    };
  }
}''')
open('project/Main.dc.html', 'w').write(page('Kaku — Início', 'pt-BR', body_m, script_m, 1440, 1580, DATA_HEAD))

