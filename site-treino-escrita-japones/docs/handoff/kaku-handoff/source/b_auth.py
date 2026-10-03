from common import *
from b_chars import DBJS, DATA_HEAD
from b_practice import BTN_O, BTN_R, LBL, CARD, login_prompt

from ui import INPUT_BLOCK as INPUT

def field(fid, label, typ='text', auto='', pw=False, hint=''):
    """Campo com rótulo, mensagem de erro e (para senhas) botão de olho."""
    f = 'f.' + fid
    inp = ('<input id="' + fid + '" name="' + fid + '" type="{{' + f + '.type}}" autocomplete="' + auto + '" value="{{' + f + '.value}}" onChange="{{' + f + '.onChange}}" onBlur="{{' + f + '.onBlur}}" '
           'aria-invalid="{{' + f + '.invalid}}" aria-describedby="' + fid + '-msg" '
           'style="' + INPUT + 'border-color:{{' + f + '.bd}};' + ('padding-right:52px;' if pw else '') + '">')
    eye = ''
    if pw:
        eye = ('<button type="button" onClick="{{' + f + '.toggle}}" aria-label="{{' + f + '.eyeLabel}}" aria-pressed="{{' + f + '.shown}}" '
               'style="position:absolute;right:4px;top:4px;width:42px;height:42px;border:none;border-radius:10px;background:transparent;color:#5E5850;display:flex;align-items:center;justify-content:center;cursor:pointer;">'
               '<sc-if value="{{' + f + '.isShown}}" hint-placeholder-val="{{false}}">' + ic('eyeoff', 20) + '</sc-if>'
               '<sc-if value="{{' + f + '.isHidden}}" hint-placeholder-val="{{true}}">' + ic('eye', 20) + '</sc-if></button>')
    return ('<div style="display:flex;flex-direction:column;gap:6px;">'
            '<label for="' + fid + '" style="font-size:14px;font-weight:700;">' + label + '</label>'
            '<div style="position:relative;">' + inp + eye + '</div>'
            '<sc-if value="{{' + f + '.hasErr}}" hint-placeholder-val="{{false}}"><span id="' + fid + '-msg" role="alert" style="display:flex;align-items:flex-start;gap:6px;font-size:13px;line-height:1.4;color:#A8292A;"><span style="display:flex;flex-shrink:0;margin-top:1px;">' + ic('alert', 16, 2.4) + '</span>{{' + f + '.err}}</span></sc-if>'
            + ('<sc-if value="{{' + f + '.noErr}}" hint-placeholder-val="{{true}}"><span id="' + fid + '-msg" style="font-size:13px;color:#726B61;">' + hint + '</span></sc-if>' if hint else '')
            + '</div>')

FORM_JS = r'''
// Campos controlados com validação ao sair do campo e ao enviar.
function fieldVals(self, id, opts) {
  const st = self.state, err = st.errors[id] || '';
  const pw = !!(opts && opts.pw), shown = !!st.show[id];
  return {
    value: st.v[id] || '', err, hasErr: !!err, noErr: !err, invalid: err ? 'true' : 'false', bd: err ? '#C8322F' : '#D9D1C4',
    type: pw ? (shown ? 'text' : 'password') : ((opts && opts.type) || 'text'),
    isShown: shown, isHidden: !shown, shown: shown ? 'true' : 'false', eyeLabel: shown ? 'Ocultar senha' : 'Mostrar senha',
    toggle: () => self.setState({ show: Object.assign({}, st.show, { [id]: !shown }) }),
    onChange: (ev) => { const v = Object.assign({}, self.state.v, { [id]: ev.target.value }); const errors = Object.assign({}, self.state.errors); if (errors[id]) { const again = self.check(v)[id]; if (again) errors[id] = again; else delete errors[id]; } self.setState({ v, errors, formErr: '' }); },
    onBlur: () => { const v = self.state.v; if (!v[id]) return; const e = self.check(v)[id]; const errors = Object.assign({}, self.state.errors); if (e) errors[id] = e; else delete errors[id]; self.setState({ errors }); }
  };
}
const RETURN_LABEL = { 'Praticar.dc.html': 'Continuar para Praticar', 'PraticarMobile.dc.html': 'Continuar para Praticar', 'Progresso.dc.html': 'Ver meu progresso', 'Listas.dc.html': 'Ir para Minhas listas', 'Caracteres.dc.html': 'Voltar para Caracteres', 'Kanji.dc.html': 'Voltar para Kanji', 'Perfil.dc.html': 'Ir para o Perfil', 'DetalheMobile.dc.html': 'Voltar', 'CaracteresMobile.dc.html': 'Voltar', 'MainMobile.dc.html': 'Ir para o início', 'KanjiMobile.dc.html': 'Voltar para Kanji', 'LeituraMobile.dc.html': 'Continuar para Leitura', 'Leitura.dc.html': 'Continuar para Leitura', 'ProgressoMobile.dc.html': 'Ver meu progresso', 'ListasMobile.dc.html': 'Ir para Minhas listas', 'PerfilMobile.dc.html': 'Ir para o Perfil' };
function returnTo() { const r = KS.get('returnTo', 'Praticar.dc.html'); return RETURN_LABEL[r] ? r : 'Praticar.dc.html'; }
'''

def aside_brand(title, text):
    return ('''<section aria-hidden="true" style="position:relative;border-radius:32px;background:#1F1C18;color:#F7F4EE;padding:48px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;">
<span class="jp" style="position:absolute;right:-30px;bottom:-80px;font-size:420px;line-height:1;color:#2C2823;">書</span>
<span style="position:relative;display:flex;align-items:center;gap:10px;font-size:14px;font-weight:700;color:#EBC9C2;"><span class="jp" style="font-size:18px;">書く</span>kaku · escrever</span>
<div style="position:relative;display:flex;flex-direction:column;gap:16px;max-width:420px;">
<h2 class="disp" style="margin:0;font-size:44px;line-height:1.15;font-weight:700;">''' + title + '''</h2>
<p style="margin:0;font-size:17px;line-height:1.6;color:#D9D1C4;">''' + text + '''</p>
</div>
<div style="position:relative;display:flex;gap:10px;">
<span class="jp" style="width:56px;height:56px;border-radius:14px;background:#2C2823;display:flex;align-items:center;justify-content:center;font-size:30px;">あ</span>
<span class="jp" style="width:56px;height:56px;border-radius:14px;background:#2C2823;display:flex;align-items:center;justify-content:center;font-size:30px;">ア</span>
<span class="jp" style="width:56px;height:56px;border-radius:14px;background-color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;font-size:30px;">字</span>
</div>
</section>''')

def shell(inner, h):
    return ('<div style="width:1440px;height:' + str(h) + 'px;box-sizing:border-box;background:#F7F4EE;display:flex;flex-direction:column;overflow:hidden;">\n' + nav('') + '\n' + inner + '\n</div>')

VOLATILE = '''<sc-if value="{{acct.volatile}}" hint-placeholder-val="{{false}}"><p role="note" style="margin:0;font-size:13px;color:#7A5210;background:#F4EAD6;padding:10px 12px;border-radius:12px;">Este navegador bloqueou o armazenamento local: a conta vale só enquanto a página estiver aberta.</p></sc-if>'''

# ---------------- Login ----------------
login_body = shell('''<main style="flex-grow:1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;padding:48px 64px 56px;">
''' + aside_brand('Seu progresso, suas listas.', 'Entre para salvar cada sessão de prática, montar listas de estudo e acompanhar sua evolução.') + '''
<div style="display:flex;align-items:center;justify-content:center;">
<section aria-labelledby="t-login" style="''' + CARD + '''width:460px;border-radius:28px;padding:40px;display:flex;flex-direction:column;gap:24px;">
<sc-if value="{{form}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:6px;"><h1 id="t-login" class="disp" style="margin:0;font-size:34px;font-weight:700;">Entrar</h1><p style="margin:0;font-size:15px;color:#5E5850;">Que bom ver você de novo.</p></div>
<form onSubmit="{{submit}}" novalidate style="display:flex;flex-direction:column;gap:18px;margin:0;">
''' + field('email', 'Email', 'email', 'email') + '''
''' + field('pw', 'Senha', auto='current-password', pw=True) + '''
<button type="submit" class="btn" style="height:54px;font-size:16px;''' + BTN_R + '''"><sc-if value="{{busy}}" hint-placeholder-val="{{false}}">''' + spinner(18) + '''</sc-if>{{submitLabel}}</button>
</form>
''' + VOLATILE + '''
<p style="margin:0;font-size:15px;color:#5E5850;text-align:center;">Ainda não tem conta? <a href="Cadastro.dc.html" style="font-weight:700;">Criar conta</a></p>
</sc-if>
<sc-if value="{{done}}" hint-placeholder-val="{{false}}">
<div class="rise" style="display:flex;flex-direction:column;gap:18px;align-items:flex-start;">
<span style="width:56px;height:56px;border-radius:999px;background:#E7EEDF;color:#4E6E3A;display:flex;align-items:center;justify-content:center;">''' + ic('check', 28, 2.4) + '''</span>
<div style="display:flex;flex-direction:column;gap:6px;"><h1 class="disp" style="margin:0;font-size:32px;font-weight:700;">{{hello}}</h1><p style="margin:0;font-size:15px;color:#5E5850;">Você entrou como {{acct.email}}.</p></div>
<a href="{{next}}" class="btn" style="align-self:stretch;height:54px;font-size:16px;''' + BTN_R + '''">{{nextLabel}}''' + ic('arrow', 18, 2) + '''</a>
<div style="display:flex;gap:16px;"><a href="Listas.dc.html" style="font-size:14px;font-weight:700;text-decoration:none;">Minhas listas</a><a href="Progresso.dc.html" style="font-size:14px;font-weight:700;text-decoration:none;">Progresso</a><button onClick="{{logout}}" style="padding:0;border:none;background:none;font-size:14px;font-weight:700;color:#5E5850;cursor:pointer;">Sair</button></div>
</div>
</sc-if>
</section>
</div>
</main>''', 900)

login_script = acctify(DBJS[:DBJS.index('const KTYPES')] + js('account.js') + FORM_JS + r'''
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'Login.dc.html'; this.state = { v: { email: KS.get('lastEmail', '') || '', pw: '' }, errors: {}, show: {}, busy: false }; }
  check(v) { return Auth.checkLogin(v); }
  renderVals() {
    const st = this.state, u = Auth.current();
    const submit = async (ev) => {
      if (ev && ev.preventDefault) ev.preventDefault();
      if (st.busy) return;
      const pre = this.check(st.v); if (Object.keys(pre).length) { this.setState({ errors: pre }); return; }
      this.setState({ busy: true });
      const r = await Auth.login(st.v);
      this.setState({ busy: false, errors: r.ok ? {} : r.errors, v: r.ok ? Object.assign({}, st.v, { pw: '' }) : st.v });
    };
    return {
      accent: this.props.accent ?? '#C8322F', form: !u, done: !!u, submit, busy: st.busy, submitLabel: st.busy ? 'Entrando…' : 'Entrar',
      f: { email: fieldVals(this, 'email', { type: 'email' }), pw: fieldVals(this, 'pw', { pw: true }) },
      hello: u ? 'Olá, ' + u.name.split(/\s+/)[0] + '!' : '', next: returnTo(), nextLabel: RETURN_LABEL[returnTo()] || 'Continuar',
      logout: () => { Auth.logout(); this.setState({ v: Object.assign({}, st.v, { pw: '' }) }); }
    };
  }
}''')

# ---------------- Cadastro ----------------
signup_body = shell('''<main style="flex-grow:1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;padding:40px 64px 48px;">
''' + aside_brand('Comece a escrever em japonês.', 'Crie sua conta para guardar listas de estudo, histórico de prática e estatísticas — tudo separado por usuário.') + '''
<div style="display:flex;align-items:center;justify-content:center;">
<section aria-labelledby="t-cad" style="''' + CARD + '''width:500px;border-radius:28px;padding:36px 40px;display:flex;flex-direction:column;gap:20px;">
<sc-if value="{{form}}" hint-placeholder-val="{{true}}">
<div style="display:flex;flex-direction:column;gap:6px;"><h1 id="t-cad" class="disp" style="margin:0;font-size:34px;font-weight:700;">Criar conta</h1><p style="margin:0;font-size:15px;color:#5E5850;">Leva menos de um minuto.</p></div>
<form onSubmit="{{submit}}" novalidate style="display:flex;flex-direction:column;gap:14px;margin:0;">
''' + field('name', 'Nome', auto='name') + '''
<div style="display:grid;grid-template-columns:minmax(0,1fr) 150px;gap:12px;align-items:start;">
''' + field('email', 'Email', 'email', 'email') + '''
''' + field('age', 'Idade', auto='off') + '''
</div>
''' + field('pw', 'Senha', auto='new-password', pw=True, hint='Pelo menos 6 caracteres.') + '''
''' + field('pw2', 'Confirmar senha', auto='new-password', pw=True) + '''
<button type="submit" class="btn" style="height:54px;margin-top:4px;font-size:16px;''' + BTN_R + '''"><sc-if value="{{busy}}" hint-placeholder-val="{{false}}">''' + spinner(18) + '''</sc-if>{{submitLabel}}</button>
</form>
''' + VOLATILE + '''
<p style="margin:0;font-size:15px;color:#5E5850;text-align:center;">Já tem conta? <a href="Login.dc.html" style="font-weight:700;">Entrar</a></p>
</sc-if>
<sc-if value="{{created}}" hint-placeholder-val="{{false}}">
<div class="rise" style="display:flex;flex-direction:column;gap:18px;align-items:flex-start;">
<span style="width:56px;height:56px;border-radius:999px;background:#E7EEDF;color:#4E6E3A;display:flex;align-items:center;justify-content:center;">''' + ic('check', 28, 2.4) + '''</span>
<div style="display:flex;flex-direction:column;gap:6px;"><h1 class="disp" style="margin:0;font-size:32px;font-weight:700;">Conta criada!</h1><p style="margin:0;font-size:15px;line-height:1.55;color:#5E5850;">Agora entre com <strong style="color:#1F1C18;">{{createdEmail}}</strong> e a senha que você acabou de criar.</p></div>
<a href="Login.dc.html" class="btn" style="align-self:stretch;height:54px;font-size:16px;''' + BTN_R + '''">Entrar''' + ic('arrow', 18, 2) + '''</a>
</div>
</sc-if>
<sc-if value="{{already}}" hint-placeholder-val="{{false}}">
<div style="display:flex;flex-direction:column;gap:16px;"><h1 class="disp" style="margin:0;font-size:30px;font-weight:700;">Você já está conectado</h1><p style="margin:0;font-size:15px;color:#5E5850;">Conta atual: {{acct.email}}. Para criar outra conta, saia primeiro.</p>
<div style="display:flex;gap:10px;"><a href="Praticar.dc.html" class="btn" style="height:48px;padding:0 20px;font-size:15px;''' + BTN_R + '''">Ir para Praticar</a><button onClick="{{logout}}" class="btn soft" style="height:48px;padding:0 20px;font-size:15px;''' + BTN_O + '''">Sair</button></div></div>
</sc-if>
</section>
</div>
</main>''', 960)

signup_script = acctify(DBJS[:DBJS.index('const KTYPES')] + js('account.js') + FORM_JS + r'''
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'Cadastro.dc.html'; this.state = { v: {}, errors: {}, show: {}, busy: false, created: null }; }
  check(v) { return Auth.checkRegister(v); }
  renderVals() {
    const st = this.state, u = Auth.current();
    const submit = async (ev) => {
      if (ev && ev.preventDefault) ev.preventDefault();
      if (st.busy) return;
      const pre = this.check(st.v); if (Object.keys(pre).length) { this.setState({ errors: pre }); return; }
      this.setState({ busy: true });
      const r = await Auth.register(st.v);
      if (r.ok) this.setState({ busy: false, created: r.user.email, v: {}, errors: {} }); else this.setState({ busy: false, errors: r.errors });
    };
    return {
      accent: this.props.accent ?? '#C8322F', form: !u && !st.created, created: !u && !!st.created, already: !!u, createdEmail: st.created || '',
      submit, busy: st.busy, submitLabel: st.busy ? 'Criando conta…' : 'Criar conta',
      f: { name: fieldVals(this, 'name'), email: fieldVals(this, 'email', { type: 'email' }), age: fieldVals(this, 'age', { type: 'number' }), pw: fieldVals(this, 'pw', { pw: true }), pw2: fieldVals(this, 'pw2', { pw: true }) },
      logout: () => { Auth.logout(); this.forceUpdate(); }
    };
  }
}''')

# ---------------- Perfil ----------------
def pstat(label, hole, sub=''):
    return ('<div style="padding:18px;border-radius:18px;background:#FFFFFF;border:1px solid #E6E0D6;display:flex;flex-direction:column;gap:4px;"><span style="font-size:13px;color:#5E5850;">' + label + '</span><strong class="disp" style="font-size:30px;line-height:1.1;">{{' + hole + '}}</strong>' + ('<span style="font-size:12px;color:#726B61;">' + sub + '</span>' if sub else '') + '</div>')

profile_body = shell('''<main style="display:flex;flex-direction:column;gap:24px;padding:44px 64px 48px;">
<sc-if value="{{acct.out}}" hint-placeholder-val="{{false}}"><section style="''' + CARD + '''max-width:640px;padding:28px;display:flex;flex-direction:column;gap:16px;"><h1 class="disp" style="margin:0;font-size:34px;font-weight:700;">Perfil</h1>''' + login_prompt('Entre para ver seu perfil', 'Seu perfil reúne seus dados, estatísticas e listas.') + '''</section></sc-if>
<sc-if value="{{acct.in}}" hint-placeholder-val="{{true}}">
<section style="''' + CARD + '''border-radius:28px;padding:32px;display:flex;align-items:center;gap:28px;">
<span aria-hidden="true" class="disp" style="width:104px;height:104px;flex-shrink:0;border-radius:999px;background-color:''' + ACC + ''';color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:700;">{{acct.initials}}</span>
<div style="flex-grow:1;display:flex;flex-direction:column;gap:6px;min-width:0;">
<h1 class="disp" style="margin:0;font-size:38px;font-weight:700;">{{acct.full}}</h1>
<dl style="margin:0;display:flex;gap:28px;font-size:15px;color:#5E5850;flex-wrap:wrap;">
<div style="display:flex;gap:6px;"><dt>Email</dt><dd style="margin:0;color:#1F1C18;font-weight:500;">{{acct.email}}</dd></div>
<div style="display:flex;gap:6px;"><dt>Idade</dt><dd style="margin:0;color:#1F1C18;font-weight:500;">{{age}}</dd></div>
<div style="display:flex;gap:6px;"><dt>Membro desde</dt><dd style="margin:0;color:#1F1C18;font-weight:500;">{{since}}</dd></div>
</dl>
</div>
<a href="Main.dc.html" onClick="{{acct.logout}}" class="btn soft" style="height:48px;padding:0 20px;font-size:15px;''' + BTN_O + '''color:#A8292A;">''' + ic('logout', 18) + '''Sair</a>
</section>
<div style="display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;">
''' + pstat('Sessões', 's.sessions') + pstat('Caracteres praticados', 's.n', 'tentativas') + pstat('Caracteres diferentes', 's.unique') + pstat('Taxa de acerto', 's.rate') + pstat('Tempo de estudo', 's.time') + pstat('Sequência', 'acct.streakLabel') + '''
</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;">
<a href="Listas.dc.html" class="card" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:10px;text-decoration:none;color:#1F1C18;"><span style="width:44px;height:44px;border-radius:12px;background:#FBEDEA;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic('list', 22) + '''</span><strong style="font-size:18px;">Minhas listas</strong><span style="font-size:14px;color:#5E5850;">{{listsLabel}}</span></a>
<a href="Progresso.dc.html" class="card" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:10px;text-decoration:none;color:#1F1C18;"><span style="width:44px;height:44px;border-radius:12px;background:#FBEDEA;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic('history', 22) + '''</span><strong style="font-size:18px;">Histórico e estatísticas</strong><span style="font-size:14px;color:#5E5850;">Filtre por hoje, semana, mês ou todo o período.</span></a>
<a href="Praticar.dc.html" class="card" style="''' + CARD + '''padding:24px;display:flex;flex-direction:column;gap:10px;text-decoration:none;color:#1F1C18;"><span style="width:44px;height:44px;border-radius:12px;background:#FBEDEA;color:''' + ACC + ''';display:flex;align-items:center;justify-content:center;">''' + ic('brush', 22) + '''</span><strong style="font-size:18px;">Praticar</strong><span style="font-size:14px;color:#5E5850;">Hiragana, katakana, kanji por JLPT ou suas listas.</span></a>
</div>
<section aria-labelledby="demo" style="''' + CARD + '''padding:24px;display:flex;align-items:center;gap:20px;">
<div style="flex-grow:1;display:flex;flex-direction:column;gap:4px;"><h2 id="demo" style="margin:0;font-size:17px;font-weight:700;">Dados de exemplo</h2><p style="margin:0;font-size:14px;line-height:1.5;color:#5E5850;">Para experimentar os gráficos e filtros do Progresso, gere um histórico fictício de 4 meses nesta conta. Ele fica marcado como exemplo e pode ser removido quando quiser.</p>
<sc-if value="{{demoMsgOn}}" hint-placeholder-val="{{false}}"><span role="status" style="font-size:13px;font-weight:700;color:#4E6E3A;">{{demoMsg}}</span></sc-if></div>
<sc-if value="{{noDemo}}" hint-placeholder-val="{{true}}"><button class="btn soft" onClick="{{addDemo}}" style="height:44px;padding:0 18px;font-size:14px;white-space:nowrap;flex-shrink:0;''' + BTN_O + '''">Gerar histórico de exemplo</button></sc-if>
<sc-if value="{{hasDemo}}" hint-placeholder-val="{{false}}"><button class="btn soft" onClick="{{removeDemo}}" style="height:44px;padding:0 18px;font-size:14px;white-space:nowrap;flex-shrink:0;''' + BTN_O + '''">Remover dados de exemplo</button></sc-if>
</section>
</sc-if>
</main>''', 900)

profile_script = acctify(DBJS + js('account.js') + r'''
class Component extends DCLogic {
  constructor(...a) { super(...a); this._page = 'Perfil.dc.html'; this.state = { msg: '' }; }
  componentDidMount() { waitForData(this); }
  renderVals() {
    const u = Auth.current(), d = u ? UD.load(u) : null, s = computeStats(d, 'tudo');
    const D = kdb();
    const hasDemo = !!d && d.sessions.some((x) => x.demo);
    return {
      accent: this.props.accent ?? '#C8322F',
      age: u ? u.age + ' anos' : '', since: u ? fmtDate(u.created) : '',
      s: { sessions: fmtInt(s.sessions.length), n: fmtInt(s.n), unique: fmtInt(s.unique), rate: pct(s.rate), time: fmtDur(s.ms) },
      listsLabel: d ? (d.lists.length ? d.lists.length + (d.lists.length === 1 ? ' lista de estudo' : ' listas de estudo') : 'Nenhuma lista ainda — crie a primeira.') : '',
      hasDemo, noDemo: !hasDemo, demoMsg: this.state.msg, demoMsgOn: !!this.state.msg,
      addDemo: () => { if (!D) return; UD.mut((x) => { x.sessions = x.sessions.concat(demoHistory(D)).sort((a, b) => a.start - b.start); }); this.setState({ msg: 'Histórico de exemplo criado. Veja em Progresso.' }); },
      removeDemo: () => { UD.mut((x) => { x.sessions = x.sessions.filter((z) => !z.demo); }); this.setState({ msg: 'Dados de exemplo removidos.' }); },
      toLogin: () => KS.set('returnTo', 'Perfil.dc.html')
    };
  }
}''')

if __name__ == '__main__':
    open('project/Login.dc.html', 'w').write(page('Kaku — Entrar', 'pt-BR', login_body, login_script, 1440, 900))
    open('project/Cadastro.dc.html', 'w').write(page('Kaku — Criar conta', 'pt-BR', signup_body, signup_script, 1440, 960))
    open('project/Perfil.dc.html', 'w').write(page('Kaku — Perfil', 'pt-BR', profile_body, profile_script, 1440, 900, DATA_HEAD))
