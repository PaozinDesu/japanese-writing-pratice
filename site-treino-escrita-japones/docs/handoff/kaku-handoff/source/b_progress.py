from common import *
from b_chars import DBJS, DATA_HEAD
from b_practice import BTN_O, BTN_R, LBL, CARD, login_prompt

OKC, FAILC = '#5E7F4A', '#E3A99F'

def kpi(icon, label, val, sub):
    return ('<div style="' + CARD + 'border-radius:20px;padding:20px;display:flex;flex-direction:column;gap:10px;">'
            '<div style="display:flex;align-items:center;gap:10px;color:#5E5850;"><span style="width:34px;height:34px;border-radius:10px;background:#FBEDEA;color:' + ACC + ';display:flex;align-items:center;justify-content:center;">' + ic(icon, 18) + '</span><span style="font-size:14px;">' + label + '</span></div>'
            '<span class="disp" style="font-size:34px;font-weight:700;line-height:1;">{{k.' + val + '}}</span>'
            '<span style="font-size:13px;color:#726B61;">{{k.' + sub + '}}</span></div>')

def rank(lst, title, sub, hid, empty):
    return ('''<section aria-labelledby="''' + hid + '''" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><h2 id="''' + hid + '''" style="margin:0;font-size:18px;font-weight:700;">''' + title + '''</h2><span style="font-size:13px;color:#726B61;">''' + sub + '''</span></div>
<sc-if value="{{''' + lst + '''Empty}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;color:#5E5850;">''' + empty + '''</p></sc-if>
<sc-for list="{{''' + lst + '''}}" as="r" hint-placeholder-count="5">
<div style="display:flex;align-items:center;gap:14px;padding:8px 0;border-top:1px solid #EFEAE1;">
<span class="jp" style="width:44px;height:44px;flex-shrink:0;border-radius:12px;background:#F7F4EE;display:flex;align-items:center;justify-content:center;font-size:{{r.fs}};">{{r.c}}</span>
<div style="flex-grow:1;min-width:0;display:flex;flex-direction:column;gap:6px;">
<div style="display:flex;justify-content:space-between;gap:8px;font-size:14px;"><span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{r.label}}</span><strong style="white-space:nowrap;">{{r.value}}</strong></div>
<div aria-hidden="true" style="display:flex;gap:2px;height:6px;"><div style="height:6px;border-radius:3px;background:''' + OKC + ''';width:{{r.okW}};"></div><div style="height:6px;border-radius:3px;background:''' + FAILC + ''';width:{{r.failW}};"></div></div>
</div>
</div>
</sc-for>
</section>''')

body = ('<div style="width:1440px;height:2000px;box-sizing:border-box;background:#F7F4EE;display:flex;flex-direction:column;overflow:hidden;">\n' + nav('progresso') + '''
<main style="display:flex;flex-direction:column;gap:22px;padding:44px 64px 56px;">
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;">
<div style="display:flex;flex-direction:column;gap:8px;">
<h1 class="disp" style="margin:0;font-size:46px;font-weight:700;">Seu progresso</h1>
<p style="margin:0;font-size:17px;color:#5E5850;">{{periodText}}</p>
</div>
<div role="group" aria-label="Período" style="display:flex;gap:4px;padding:4px;background:#EFEAE1;border-radius:999px;">
<sc-for list="{{periods}}" as="p" hint-placeholder-count="4"><button onClick="{{p.pick}}" aria-pressed="{{p.pressed}}" style="height:42px;padding:0 18px;border:none;border-radius:999px;background-color:{{p.bg}};color:{{p.fg}};font-weight:{{p.fw}};box-shadow:{{p.sh}};font-size:14px;cursor:pointer;">{{p.label}}</button></sc-for>
</div>
</div>
<sc-if value="{{acct.out}}" hint-placeholder-val="{{false}}"><section style="''' + CARD + '''max-width:720px;padding:24px;">''' + login_prompt('Entre para ver seu histórico', 'Seu progresso, estatísticas e sessões ficam salvos na sua conta. Sem entrar, você ainda pode praticar livremente.') + '''</section></sc-if>
<sc-if value="{{acct.in}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:22px;">
<sc-if value="{{noData}}" hint-placeholder-val="{{false}}"><div style="display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 20px;border-radius:16px;background:#FFFFFF;border:1px dashed #D9D1C4;">
<span style="font-size:15px;color:#3B3630;">{{emptyText}}</span>
<span style="display:flex;gap:8px;flex-shrink:0;"><a href="Praticar.dc.html" class="btn" style="height:42px;padding:0 16px;font-size:14px;''' + BTN_R + '''">''' + ic('brush', 16) + '''Praticar agora</a><sc-if value="{{canDemo}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{addDemo}}" style="height:42px;padding:0 16px;font-size:14px;''' + BTN_O + '''">Ver com dados de exemplo</button></sc-if></span>
</div></sc-if>
<div style="display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;">
''' + kpi('grid', 'Praticados', 'n', 'nSub') + kpi('check', 'Acertos', 'ok', 'okSub') + kpi('x', 'Erros', 'fail', 'failSub') + kpi('target', 'Taxa de acerto', 'rate', 'rateSub') + kpi('clock', 'Tempo de estudo', 'time', 'timeSub') + kpi('history', 'Sessões', 'sessions', 'sessionsSub') + '''
</div>
<div style="display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:20px;">
<section aria-labelledby="evo" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:16px;">
<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
<div style="display:flex;flex-direction:column;gap:2px;"><h2 id="evo" style="margin:0;font-size:18px;font-weight:700;">Evolução</h2><span style="font-size:13px;color:#726B61;">{{evoSub}}</span></div>
<div style="display:flex;gap:14px;font-size:13px;color:#3B3630;"><span style="display:flex;align-items:center;gap:6px;"><span style="width:12px;height:12px;border-radius:3px;background:''' + OKC + ''';"></span>Acertos</span><span style="display:flex;align-items:center;gap:6px;"><span style="width:12px;height:12px;border-radius:3px;background:''' + FAILC + ''';"></span>Erros</span></div>
</div>
<div style="position:relative;height:230px;">
<div aria-hidden="true" style="position:absolute;left:0;right:0;top:0;border-top:1px dashed #E6E0D6;"></div>
<div aria-hidden="true" style="position:absolute;left:0;right:0;top:100px;border-top:1px dashed #EFEAE1;"></div>
<span style="position:absolute;right:0;top:-18px;font-size:11px;color:#726B61;">{{yMax}}</span>
<div role="img" aria-label="{{evoAria}}" style="position:absolute;left:0;right:0;top:0;height:200px;display:flex;align-items:flex-end;gap:{{barGap}};border-bottom:1px solid #D9D1C4;">
<sc-for list="{{series}}" as="b" hint-placeholder-count="7"><div data-tip="{{b.tip}}" style="flex-grow:1;flex-basis:0;height:200px;display:flex;flex-direction:column;justify-content:flex-end;align-items:stretch;gap:{{b.gap}};cursor:default;min-width:0;">
<div style="height:{{b.hFail}};background:''' + FAILC + ''';border-radius:{{b.rFail}};"></div>
<div style="height:{{b.hOk}};background:''' + OKC + ''';border-radius:{{b.rOk}};"></div>
</div></sc-for>
</div>
<div aria-hidden="true" style="position:absolute;left:0;right:0;top:206px;display:flex;gap:{{barGap}};">
<sc-for list="{{series}}" as="b" hint-placeholder-count="7"><span style="flex-grow:1;flex-basis:0;text-align:center;font-size:11px;color:{{b.lc}};font-weight:{{b.fw}};white-space:nowrap;min-width:0;">{{b.label}}</span></sc-for>
</div>
</div>
<span style="font-size:12px;color:#726B61;">Passe o mouse sobre as barras para ver os números de cada {{unit}}.</span>
</section>
<section aria-labelledby="sis" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:20px;">
<div style="display:flex;flex-direction:column;gap:2px;"><h2 id="sis" style="margin:0;font-size:18px;font-weight:700;">Caracteres estudados</h2><span style="font-size:13px;color:#726B61;">diferentes, no período · acertados pelo menos uma vez</span></div>
<sc-for list="{{systems}}" as="s" hint-placeholder-count="3">
<div style="display:flex;align-items:center;gap:16px;">
<span class="jp" style="width:50px;height:50px;flex-shrink:0;border-radius:14px;background-color:{{s.tb}};color:{{s.tf}};display:flex;align-items:center;justify-content:center;font-size:28px;">{{s.g}}</span>
<div style="flex-grow:1;display:flex;flex-direction:column;gap:8px;min-width:0;">
<div style="display:flex;justify-content:space-between;font-size:15px;"><strong>{{s.name}}</strong><span style="color:#5E5850;">{{s.label}}</span></div>
<div aria-hidden="true" style="position:relative;height:10px;border-radius:999px;background:#EFEAE1;overflow:hidden;"><div style="position:absolute;left:0;top:0;height:10px;border-radius:999px;width:{{s.seenW}};background:#EBC9C2;"></div><div style="position:absolute;left:0;top:0;height:10px;border-radius:999px;width:{{s.okW}};background-color:''' + ACC + ''';"></div></div>
</div>
</div>
</sc-for>
<div style="display:flex;gap:14px;font-size:12px;color:#5E5850;"><span style="display:flex;align-items:center;gap:6px;"><span style="width:12px;height:12px;border-radius:3px;background-color:''' + ACC + ''';"></span>Acertados</span><span style="display:flex;align-items:center;gap:6px;"><span style="width:12px;height:12px;border-radius:3px;background:#EBC9C2;"></span>Praticados</span></div>
</section>
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;">
''' + rank('top', 'Mais praticados', 'tentativas no período', 'top', 'Nenhum caractere praticado neste período.') + '''
''' + rank('hard', 'Mais erros', 'erros no período', 'hard', 'Nenhum erro neste período.') + '''
</div>
<sc-if value="{{hasHard}}" hint-placeholder-val="{{false}}"><div style="display:flex;justify-content:flex-end;margin-top:-8px;"><a href="Praticar.dc.html" onClick="{{reviewHard}}" style="font-size:14px;font-weight:700;text-decoration:none;display:flex;align-items:center;gap:6px;">Praticar os caracteres com mais erros''' + ic('arrow', 16, 2) + '''</a></div></sc-if>
<section id="historico" aria-labelledby="hist" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;"><h2 id="hist" style="margin:0;font-size:18px;font-weight:700;">Histórico de sessões</h2><span style="font-size:13px;color:#726B61;">{{histSub}}</span></div>
<sc-if value="{{sessEmpty}}" hint-placeholder-val="{{false}}"><p style="margin:0;font-size:14px;color:#5E5850;">Nenhuma sessão neste período.</p></sc-if>
<sc-if value="{{sessAny}}" hint-placeholder-val="{{true}}">
<table style="width:100%;border-collapse:collapse;font-size:14px;">
<thead><tr style="text-align:left;color:#726B61;font-size:12px;letter-spacing:.06em;text-transform:uppercase;"><th scope="col" style="padding:8px 0;font-weight:700;">Data</th><th scope="col" style="padding:8px 0;font-weight:700;">Sessão</th><th scope="col" style="padding:8px 0;font-weight:700;text-align:right;">Caracteres</th><th scope="col" style="padding:8px 0;font-weight:700;text-align:right;">Acertos</th><th scope="col" style="padding:8px 0;font-weight:700;text-align:right;">Taxa</th><th scope="col" style="padding:8px 0;font-weight:700;text-align:right;">Duração</th></tr></thead>
<tbody><sc-for list="{{sessions}}" as="s" hint-placeholder-count="5"><tr style="border-top:1px solid #EFEAE1;"><td style="padding:10px 0;color:#5E5850;white-space:nowrap;">{{s.when}}</td><td style="padding:10px 12px 10px 0;">{{s.label}}<sc-if value="{{s.demo}}" hint-placeholder-val="{{false}}"><span style="margin-left:8px;font-size:11px;font-weight:700;padding:2px 7px;border-radius:999px;background:#F4EAD6;color:#7A5210;">exemplo</span></sc-if></td><td style="padding:10px 0;text-align:right;">{{s.n}}</td><td style="padding:10px 0;text-align:right;">{{s.ok}}</td><td style="padding:10px 0;text-align:right;font-weight:700;">{{s.acc}}</td><td style="padding:10px 0;text-align:right;color:#5E5850;">{{s.dur}}</td></tr></sc-for></tbody>
</table>
<sc-if value="{{sessMore}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{moreSess}}" style="align-self:center;height:40px;padding:0 16px;font-size:14px;''' + BTN_O + '''border-radius:999px;">{{sessMoreLabel}}</button></sc-if>
</sc-if>
</section>
</div>
</sc-if>
</main>
</div>''')

script = acctify(DBJS + js('account.js') + r'''
const PERIOD_TEXT = { hoje: 'Hoje', semana: 'Esta semana (desde segunda-feira)', mes: 'Este mês', tudo: 'Todo o período' };
const UNIT = { hoje: 'hora', semana: 'dia', mes: 'dia', tudo: 'mês' };
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'Progresso.dc.html'; this.state = { period: 'semana', lim: 10 }; }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const accent = this.props.accent ?? '#C8322F';
    const st = this.state, u = Auth.current(), d = u ? UD.load(u) : null, D = kdb();
    const s = computeStats(d, st.period);
    const periods = PERIODS.map(([id, label]) => { const on = st.period === id; return { label, pressed: on ? 'true' : 'false', bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F1C18' : '#5E5850', fw: on ? '700' : '500', sh: on ? '0 1px 3px rgba(31,28,24,.12)' : 'none', pick: () => this.setState({ period: id, lim: 10 }) }; });
    const plural = (n, a, b) => fmtInt(n) + ' ' + (n === 1 ? a : b);
    const k = {
      n: fmtInt(s.n), nSub: plural(s.unique, 'caractere diferente', 'caracteres diferentes'),
      ok: fmtInt(s.ok), okSub: s.n ? pct(s.ok / s.n) + ' das tentativas' : 'nenhuma tentativa',
      fail: fmtInt(s.fail), failSub: s.fail ? plural(s.chars.filter((c) => c.fail).length, 'caractere com erro', 'caracteres com erro') : 'nenhum erro',
      rate: pct(s.rate), rateSub: 'acertos ÷ praticados',
      time: fmtDur(s.ms), timeSub: s.sessions.length ? 'média de ' + fmtDur(s.ms / s.sessions.length) + ' por sessão' : 'sem sessões',
      sessions: fmtInt(s.sessions.length), sessionsSub: s.sessions.length ? 'última: ' + fmtDate(s.sessions[0].start, true) : 'nenhuma no período'
    };
    const max = Math.max(1, ...s.series.map((b) => b.n));
    const nice = max <= 5 ? 5 : max <= 10 ? 10 : Math.ceil(max / 10) * 10;
    const series = s.series.map((b) => {
      const hOk = Math.round(b.ok / nice * 200), hFail = Math.round(b.fail / nice * 200);
      return { label: b.label, lc: b.cur ? '#1F1C18' : '#726B61', fw: b.cur ? '700' : '400',
        hOk: (b.ok ? Math.max(2, hOk) : 0) + 'px', hFail: (b.fail ? Math.max(2, hFail) : 0) + 'px', hOkM: (b.ok ? Math.max(2, Math.round(b.ok / nice * 136)) : 0) + 'px', hFailM: (b.fail ? Math.max(2, Math.round(b.fail / nice * 136)) : 0) + 'px', gap: b.ok && b.fail ? '2px' : '0px',
        rOk: b.fail ? '0 0 2px 2px' : '4px 4px 2px 2px', rFail: '4px 4px 0 0',
        tip: b.full + ' — ' + (b.n ? b.n + ' praticados · ' + b.ok + ' acertos · ' + b.fail + ' erros · ' + pct(b.acc) : 'sem prática') };
    });
    const tile = (id) => { const e = D && D._idx[id]; const c = e ? e.char : id.split(':')[1]; return { c, fs: Array.from(c).length > 1 ? '18px' : '26px', name: e ? (e.category === 'kanji' ? e.meaning.pt[0] : e.romaji) : '' }; };
    const top = s.top.map((p) => { const t = tile(p.id); return Object.assign(t, { label: t.name, value: p.n + (p.n === 1 ? ' vez' : ' vezes') + ' · ' + pct(p.ok / p.n), okW: (p.ok / s.top[0].n * 100) + '%', failW: (p.fail / s.top[0].n * 100) + '%' }); });
    const hmax = s.hard.length ? Math.max(...s.hard.map((p) => p.n)) : 1;
    const hard = s.hard.map((p) => { const t = tile(p.id); return Object.assign(t, { label: t.name, value: p.fail + (p.fail === 1 ? ' erro' : ' erros') + ' em ' + p.n, okW: (p.ok / hmax * 100) + '%', failW: (p.fail / hmax * 100) + '%' }); });
    const tot = { hiragana: 0, katakana: 0, kanji: 0 };
    if (D) D.characters.forEach((e) => { tot[e.category]++; });
    const systems = [['あ', 'Hiragana', 'hiragana', '#E3EAF2', '#2E4C6E'], ['ア', 'Katakana', 'katakana', '#F4EAD6', '#7A5210'], ['字', 'Kanji', 'kanji', '#F8E4E0', '#A8292A']].map(([g, name, id, tb, tf]) => {
      const c = s.byCat[id], T = tot[id] || 1;
      return { g, name, tb, tf, label: fmtInt(c.ok) + ' acertados · ' + fmtInt(c.seen) + ' de ' + fmtInt(tot[id]), seenW: Math.max(c.seen ? 1 : 0, c.seen / T * 100) + '%', okW: Math.max(c.ok ? 1 : 0, c.ok / T * 100) + '%' };
    });
    const sessions = s.sessions.slice(0, st.lim).map((x) => ({ when: fmtDate(x.start, true), label: x.label || 'Sessão', n: x.n, ok: x.ok, acc: pct(x.acc), dur: fmtDur(x.ms), demo: x.demo }));
    const everything = d && d.sessions.some((x) => x.items.length);
    return {
      accent, periods, periodText: PERIOD_TEXT[st.period] + (s.n ? ' · ' + plural(s.n, 'caractere praticado', 'caracteres praticados') : ''),
      k, series, yMax: 'máx. ' + nice, barGap: s.series.length > 20 ? '3px' : '10px', unit: UNIT[st.period],
      evoSub: { hoje: 'caracteres praticados por hora, hoje', semana: 'caracteres praticados por dia, nesta semana', mes: 'caracteres praticados por dia, neste mês', tudo: 'caracteres praticados por mês' }[st.period],
      evoAria: 'Gráfico de barras: ' + s.series.filter((b) => b.n).map((b) => b.full + ' ' + b.n + ' praticados, ' + b.ok + ' acertos').join('; '),
      systems, top, topEmpty: !top.length, hard, hardEmpty: !hard.length, hasHard: hard.length > 0,
      reviewHard: () => Intent.set({ kind: 'chars', chars: s.hard.map((p) => p.id), label: 'Revisão: mais erros' }),
      sessions, sessEmpty: !s.sessions.length, sessAny: s.sessions.length > 0, histSub: plural(s.sessions.length, 'sessão', 'sessões') + ' no período',
      sessMore: s.sessions.length > st.lim, sessMoreLabel: 'Mostrar mais (' + (s.sessions.length - st.lim) + ')', moreSess: () => this.setState({ lim: st.lim + 20 }),
      noData: !!u && s.n === 0, emptyText: everything ? 'Nenhuma prática em “' + PERIOD_TEXT[st.period].toLowerCase() + '”. Escolha outro período ou pratique agora.' : 'Você ainda não praticou. Suas sessões aparecem aqui assim que terminar a primeira.',
      canDemo: !everything && !!D, addDemo: () => { UD.mut((x) => { x.sessions = x.sessions.concat(demoHistory(D)).sort((a, b) => a.start - b.start); }); this.forceUpdate(); },
      toLogin: () => KS.set('returnTo', 'Progresso.dc.html')
    };
  }
}''')

if __name__ == '__main__':
    open('project/Progresso.dc.html', 'w').write(page("Kaku — Progresso", "pt-BR", body, script, 1440, 2000, DATA_HEAD))
