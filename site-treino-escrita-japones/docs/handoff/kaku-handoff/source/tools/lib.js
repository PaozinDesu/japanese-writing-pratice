const S = 'http://127.0.0.1:8765/';
async function signupLogin(page, email = 'ana@exemplo.com', name = 'Ana Souza') {
  await page.goto(S + 'Cadastro.dc.html'); await page.waitForTimeout(700);
  await page.fill('#name', name); await page.fill('#email', email); await page.fill('#age', '31'); await page.fill('#pw', 'segredo1'); await page.fill('#pw2', 'segredo1');
  await page.getByRole('button', { name: 'Criar conta', exact: true }).last().click(); await page.waitForTimeout(700);
  await page.goto(S + 'Login.dc.html'); await page.waitForTimeout(700);
  await page.fill('#email', email); await page.fill('#pw', 'segredo1'); await page.getByRole('button', { name: 'Entrar', exact: true }).last().click(); await page.waitForTimeout(700);
}
module.exports = { S, signupLogin };
