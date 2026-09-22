// Prova do passo 11 (21/09): formulário "personalized price by text" nas páginas de serviço.
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import { join, extname } from 'node:path';

const ROOT = new URL('./site/', import.meta.url).pathname;
const MIME = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon' };
const server = createServer(async (req, res) => {
  try {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (p.endsWith('/')) p += 'index.html';
    if (!extname(p)) p += '/index.html';
    const buf = await readFile(join(ROOT, p));
    res.writeHead(200, { 'content-type': MIME[extname(p)] || 'application/octet-stream' });
    res.end(buf);
  } catch { res.writeHead(404); res.end('nf'); }
});
await new Promise(r => server.listen(8790, r));
await mkdir('shots', { recursive: true });

const API = 'https://slc-app-worker.booking-f8e.workers.dev/api/site/quote-request';
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
let failures = 0;
const check = (cond, msg) => { console.log((cond ? '  ✓ ' : '  ✗ ') + msg); if (!cond) failures++; };

async function newCtx(mobile = true) {
  const ctx = await browser.newContext(mobile
    ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
    : { viewport: { width: 1450, height: 900 } });
  await ctx.route('**/googletagmanager.com/**', r => r.fulfill({ status: 200, contentType: 'text/javascript', body: '' }));
  return ctx;
}

// ── 1) celular, página deep-cleaning, chegando de anúncio ──────────────────
{
  const ctx = await newCtx(true);
  const posted = [];
  await ctx.route(API, async route => {
    posted.push(JSON.parse(route.request().postData() || '{}'));
    await route.fulfill({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify({ ok: true, firstName: 'Sofya', phoneDisplay: '(650) 772-0207' }) });
  });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.log('  pageerror:', e.message));
  await page.goto('http://localhost:8790/services/deep-cleaning/?gclid=GCLIDTEST&utm_campaign=peninsula', { waitUntil: 'load' });
  await page.waitForTimeout(400);

  check(await page.locator('#quote-form').count() === 1, 'seção do formulário existe uma vez');
  const secTop = await page.locator('#quote-form').evaluate(el => el.getBoundingClientRect().top + window.scrollY);
  check(secTop < 1800, `formulário logo abaixo do hero no celular (topo em ${Math.round(secTop)}px)`);
  check(await page.locator('#qfForm [name="service"]').inputValue() === 'deep', 'serviço pré-selecionado: Deep');
  check(await page.locator('#qfForm [name="frequency"]').inputValue() === 'onetime', 'frequência pré-selecionada: one-time');
  const secText = await page.locator('#quote-form').innerText();
  check(!/\$\s?\d/.test(secText), 'nenhum preço aparece na seção do formulário');
  const hp = await page.locator('#qfForm [name="website"]').evaluate(el => { const r = el.getBoundingClientRect(); return { right: r.right, tabindex: el.getAttribute('tabindex') }; });
  check(hp.right < 0 && hp.tabindex === '-1', `honeypot fora da tela e fora do tab (right=${Math.round(hp.right)})`);

  // vitrine do app dentro do bloco
  const appBtn = page.locator('#quote-form .qf-app-btn');
  check(await appBtn.count() === 1 && /app\.signatureluxurycleaning\.com\/\?src=site-quote-deep-cleaning/.test(await appBtn.getAttribute('href') || ''), 'vitrine do app: botão leva ao app com ?src=site-quote-deep-cleaning');
  check(await page.locator('#quote-form .qf-app-steps li').count() === 3, 'vitrine do app: 3 passos (preço, dia, agendar)');
  const appBox = await appBtn.evaluate(el => el.getBoundingClientRect().top + window.scrollY);
  const formBox = await page.locator('#qfForm').evaluate(el => el.getBoundingClientRect().top + window.scrollY);
  check(appBox < formBox, 'no celular a vitrine do app aparece ANTES do formulário');
  check(await page.locator('#qfForm .qf-applink').count() === 1, 'link "skip the wait" para o app também embaixo do formulário');

  await page.locator('#quote-form').scrollIntoViewIfNeeded();
  await page.screenshot({ path: 'shots/qf_m1_form.png' });
  await page.locator('#qfForm').scrollIntoViewIfNeeded();
  await page.screenshot({ path: 'shots/qf_m1b_form.png' });

  // envio sem consentimento → erro local, nada enviado
  await page.fill('#qfForm [name="name"]', 'Sofya Test');
  await page.fill('#qfForm [name="phone"]', '650-772-0207');
  await page.fill('#qfForm [name="zip"]', '94028');
  await page.selectOption('#qfForm [name="bedrooms"]', '4');
  await page.selectOption('#qfForm [name="bathrooms"]', '2');
  await page.fill('#qfForm [name="sqft"]', '4,000');
  await page.fill('#qfForm [name="notes"]', 'Two dogs');
  await page.click('#qfForm .qf-btn');
  await page.waitForTimeout(300);
  check(posted.length === 0 && await page.locator('#qfForm .qf-error').isVisible(), 'sem consentimento: erro local e nada enviado');

  // com consentimento → POST com tudo, sucesso, evento GA4
  await page.check('#qfForm [name="consent"]');
  await page.waitForTimeout(2600); // acima do MIN_FILL_MS do servidor (aqui só documenta o startedAt)
  await page.click('#qfForm .qf-btn');
  await page.waitForSelector('#qfSuccess:not([hidden])', { timeout: 5000 });
  const body = posted[0] || {};
  check(posted.length === 1, 'um POST ao Worker');
  check(body.name === 'Sofya Test' && body.zip === '94028' && body.service === 'deep' && body.frequency === 'onetime', `payload básico correto (${JSON.stringify({ name: body.name, zip: body.zip, service: body.service, frequency: body.frequency })})`);
  check(body.propertyType === 'house' && body.bedrooms === '4' && body.bathrooms === '2' && body.sqft === '4000', 'casa 4/2 e metragem sem vírgula');
  check(body.consent === true && body.website === '' && typeof body.startedAt === 'number', 'consentimento, honeypot vazio e startedAt presentes');
  check(body.gclid === 'GCLIDTEST' && body.utm_campaign === 'peninsula' && body.page === '/services/deep-cleaning/', 'gclid/utm/página seguem no payload');
  check(body.notes === 'Two dogs', 'observações enviadas');
  const successText = await page.locator('#qfSuccess').innerText();
  check(successText.includes('Sofya') && successText.includes('(650) 772-0207'), 'tela de sucesso com nome e telefone');
  check(!(await page.locator('#qfForm').isVisible()), 'formulário some após o sucesso');
  const events = await page.evaluate(() => Array.from(window.dataLayer || []).map(a => Array.from(a)));
  check(events.some(e => e[1] === 'generate_lead'), 'evento GA4 generate_lead disparado');
  check(!events.some(e => e[1] === 'conversion' && String(e[2] && e[2].send_to).endsWith('/')), 'sem conversão do Ads com rótulo vazio (placeholder respeitado)');
  await page.screenshot({ path: 'shots/qf_m2_success.png' });
  await ctx.close();
}

// ── 2) 429 e falha de rede → mensagens certas, formulário continua utilizável ─
{
  const ctx = await newCtx(true);
  let mode = '429';
  await ctx.route(API, async route => {
    if (mode === '429') return route.fulfill({ status: 429, contentType: 'application/json', body: JSON.stringify({ ok: false, error: 'RATE_LIMITED' }) });
    return route.abort('failed');
  });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8790/services/regular-cleaning/', { waitUntil: 'load' });
  check(await page.locator('#qfForm [name="service"]').inputValue() === 'regular' && await page.locator('#qfForm [name="frequency"]').inputValue() === 'biweekly', 'regular-cleaning pré-seleciona Regular / every 2 weeks');
  await page.fill('#qfForm [name="name"]', 'Ana Test');
  await page.fill('#qfForm [name="phone"]', '(650) 555-0301');
  await page.fill('#qfForm [name="zip"]', '94301');
  await page.check('#qfForm [name="consent"]');
  await page.click('#qfForm .qf-btn');
  await page.waitForTimeout(500);
  let err = await page.locator('#qfForm .qf-error').innerText();
  check(/already have your request/i.test(err), '429: avisa que o pedido já existe (sem duplicar)');
  mode = 'fail';
  await page.click('#qfForm .qf-btn');
  await page.waitForTimeout(500);
  err = await page.locator('#qfForm .qf-error').innerText();
  const smsHref = await page.locator('#qfForm .qf-error a').getAttribute('href');
  check(/Text us directly/i.test(err) && String(smsHref).startsWith('sms:+16506193504'), 'falha de rede: fallback com link de SMS para o número da empresa');
  check(!(await page.locator('#qfForm .qf-btn').isDisabled()), 'botão volta a ficar clicável após erro');
  await ctx.close();
}

// ── 3) desktop: layout em duas colunas + home tem o formulário ───────────────
{
  const ctx = await newCtx(false);
  const page = await ctx.newPage();
  await page.goto('http://localhost:8790/services/regular-cleaning/', { waitUntil: 'load' });
  await page.locator('#quote-form').scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  const cols = await page.locator('.qf-wrap').evaluate(el => getComputedStyle(el).gridTemplateColumns.split(' ').length);
  check(cols === 2, `desktop: duas colunas (${cols})`);
  await page.screenshot({ path: 'shots/qf_d1_form.png' });
  await page.goto('http://localhost:8790/', { waitUntil: 'load' });
  check(await page.locator('#quote-form').count() === 1 && await page.locator('#qfForm [name="service"]').inputValue() === 'regular', 'home: formulário presente, Regular por padrão');
  const homeText = await page.locator('#quote-form').innerText();
  check(!/\$\s?\d/.test(homeText), 'home: seção do formulário sem preço');
  await ctx.close();
}

await browser.close();
server.close();
console.log(failures ? `FALHOU: ${failures}` : 'PROVA OK');
process.exit(failures ? 1 : 0);
