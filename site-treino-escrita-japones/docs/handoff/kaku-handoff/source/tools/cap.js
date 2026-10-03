const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const fs = require('fs'); const path = require('path');
const { S, signupLogin } = require('./lib');
const OUT = process.argv[2];
const SHOT = path.join(OUT, 'screenshots'), STAT = path.join(OUT, 'screens-static');
const DESK = ['Main','Caracteres','Kanji','Praticar','Leitura','Progresso','Login','Cadastro','Listas','Perfil'];
const MOB = ['MainMobile','CaracteresMobile','DetalheMobile','KanjiMobile','PraticarMobile','LeituraMobile','ProgressoMobile','ResultadoMobile','LoginMobile','CadastroMobile','ListasMobile','PerfilMobile'];
const DS = ['DesignSystem','Componentes'];
const log = [];
async function snap(page, dir, name, full) {
  fs.mkdirSync(path.join(SHOT, dir), { recursive: true }); fs.mkdirSync(path.join(STAT, dir), { recursive: true });
  await page.screenshot({ path: path.join(SHOT, dir, name + '.png'), fullPage: !!full });
  const html = await page.evaluate(() => {
    const d = document.documentElement.cloneNode(true);
    d.querySelectorAll('script').forEach(s => s.remove());
    d.querySelectorAll('canvas').forEach(c => { const r = document.createElement('div'); r.setAttribute('data-canvas-placeholder',''); r.style.cssText = c.getAttribute('style') || ''; r.style.width = (c.clientWidth||c.width)+'px'; r.style.height=(c.clientHeight||c.height)+'px'; r.style.background = r.style.background || '#fff'; c.replaceWith(r); });
    return '<!doctype html>\n' + d.outerHTML;
  });
  fs.writeFileSync(path.join(STAT, dir, name + '.html'), html.replace('<head>', '<head>\n<!-- Snapshot estático gerado do protótipo Kaku (sem scripts). Referência visual/estrutural apenas. -->'));
  log.push(dir + '/' + name);
}
async function visit(page, f, w, h) { await page.setViewportSize({ width: w, height: h }); await page.goto(S + f + '.dc.html'); await page.waitForTimeout(1800); }
async function step(label, fn) { try { await fn(); } catch (e) { console.log('FAIL', label, e.message.split('\n')[0]); } }
(async () => {
  const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('PAGEERR', e.message));
  // visitante
  for (const f of DESK) await step(f, async () => { await visit(page, f, 1920, 1080); await snap(page, 'desktop/visitante', f); });
  for (const f of MOB) await step(f, async () => { await visit(page, f, 390, 844); await snap(page, 'mobile/visitante', f); });
  for (const f of DS) await step(f, async () => { await visit(page, f, 1440, 1000); await snap(page, 'design-system', f, true); });
  // logado + dados de exemplo
  await page.setViewportSize({ width: 1920, height: 1080 });
  await signupLogin(page);
  await step('demo', async () => { await visit(page, 'Perfil', 1920, 1080); await page.getByRole('button', { name: 'Gerar histórico de exemplo' }).click(); await page.waitForTimeout(400); });
  await step('lista', async () => { await visit(page, 'Listas', 1920, 1080); await page.getByRole('button', { name: /Criar a lista de exemplo/ }).click(); await page.waitForTimeout(400); });
  for (const f of DESK.filter(x => x !== 'Login' && x !== 'Cadastro')) await step(f, async () => { await visit(page, f, 1920, 1080); await snap(page, 'desktop/logado', f); });
  for (const f of MOB.filter(x => x !== 'LoginMobile' && x !== 'CadastroMobile')) await step(f, async () => { await visit(page, f, 390, 844); await snap(page, 'mobile/logado', f); });
  // estados-chave
  await step('menu', async () => { await visit(page, 'Main', 1920, 1080); await page.getByRole('button', { name: /Ana/ }).first().click(); await page.waitForTimeout(300); await snap(page, 'estados', 'desktop-menu-usuario'); });
  await step('escrita', async () => {
    await visit(page, 'Praticar', 1920, 1080); await page.getByRole('button', { name: '10', exact: true }).first().click(); await page.getByRole('button', { name: /Começar/ }).first().click(); await page.waitForSelector('canvas'); await page.waitForTimeout(400);
    await snap(page, 'estados', 'desktop-escrita-1-sessao');
    const box = await page.locator('canvas').boundingBox();
    await page.mouse.move(box.x + 150, box.y + 150); await page.mouse.down(); await page.mouse.move(box.x + 400, box.y + 400, { steps: 12 }); await page.mouse.up();
    await page.getByRole('button', { name: 'Pronto' }).click(); await page.waitForSelector('text=Resultado deste caractere'); await page.waitForTimeout(300);
    await snap(page, 'estados', 'desktop-escrita-2-feedback');
    for (let k = 0; k < 40; k++) {
      const vr = page.getByRole('button', { name: 'Ver resumo' });
      if (await vr.count()) { await vr.first().click(); break; }
      await page.getByRole('button', { name: /^Próximo/ }).first().click(); await page.waitForTimeout(150);
      const bx = await page.locator('canvas').boundingBox();
      await page.mouse.move(bx.x + 120, bx.y + 200); await page.mouse.down(); await page.mouse.move(bx.x + 420, bx.y + 210, { steps: 8 }); await page.mouse.up();
      await page.getByRole('button', { name: 'Pronto' }).click(); await page.waitForTimeout(150);
    }
    await page.waitForTimeout(500);
    await snap(page, 'estados', 'desktop-escrita-3-resumo');
  });
  await step('leitura', async () => {
    await visit(page, 'Leitura', 1920, 1080);
    await page.getByRole('button', { name: /^Kanji/ }).click(); await page.getByRole('button', { name: /^N5/ }).click(); await page.getByRole('button', { name: '10', exact: true }).click();
    await page.getByRole('button', { name: /Iniciar prática/ }).click(); await page.waitForTimeout(400);
    await snap(page, 'estados', 'desktop-leitura-1-pergunta');
    await page.fill('#leitura', 'xx'); await page.press('#leitura', 'Enter'); await page.waitForTimeout(300);
    await snap(page, 'estados', 'desktop-leitura-2-feedback');
    await page.keyboard.press('Enter'); await page.waitForTimeout(150);
    for (let k = 0; k < 3; k++) { await page.fill('#leitura', 'xx'); await page.press('#leitura', 'Enter'); await page.waitForTimeout(120); await page.keyboard.press('Enter'); await page.waitForTimeout(120); }
    await page.getByRole('button', { name: 'Encerrar prática' }).click(); await page.waitForTimeout(400);
    await snap(page, 'estados', 'desktop-leitura-3-resultado');
  });
  await step('leitura-mob', async () => {
    await visit(page, 'LeituraMobile', 390, 844);
    await page.getByRole('button', { name: /Iniciar prática/ }).click(); await page.waitForTimeout(400);
    await snap(page, 'estados', 'mobile-leitura-pergunta');
  });
  await step('escrita-mob', async () => {
    await visit(page, 'PraticarMobile', 390, 844); await page.getByRole('button', { name: /Começar/ }).first().click(); await page.waitForTimeout(500);
    await snap(page, 'estados', 'mobile-escrita-sessao');
  });
  await step('kanji-mob', async () => {
    await visit(page, 'KanjiMobile', 390, 844); await page.locator('button.card', { hasText: '木' }).first().click(); await page.waitForTimeout(400);
    await snap(page, 'estados', 'mobile-kanji-detalhe');
  });
  await step('listas-mob', async () => {
    await visit(page, 'ListasMobile', 390, 844); await page.locator('[role=option], button.card').first().click(); await page.waitForTimeout(400);
    await snap(page, 'estados', 'mobile-lista-detalhe');
  });
  await step('login-err', async () => {
    await page.getByRole('button', { name: /Ana/ }).first().click().catch(()=>{});
    await page.evaluate(() => { Object.keys(localStorage).filter(k => k.indexOf('kaku.v1.session') === 0 || k === 'kaku.v1.sess').forEach(k => localStorage.removeItem(k)); });
    await visit(page, 'Login', 1920, 1080); await page.getByRole('button', { name: 'Entrar', exact: true }).last().click(); await page.waitForTimeout(300);
    await snap(page, 'estados', 'desktop-login-validacao');
    await visit(page, 'Cadastro', 1920, 1080); await page.fill('#email', 'x'); await page.fill('#pw', '1'); await page.fill('#pw2', '2'); await page.getByRole('button', { name: 'Criar conta', exact: true }).last().click(); await page.waitForTimeout(300);
    await snap(page, 'estados', 'desktop-cadastro-validacao');
  });
  fs.writeFileSync(path.join(OUT, 'capture-log.txt'), log.join('\n'));
  console.log('captured', log.length);
  await b.close();
})();
