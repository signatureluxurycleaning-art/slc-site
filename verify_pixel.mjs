// Prova do passo 17 em navegador real: Meta Pixel carregado, fbclid viajando
// site→app, Lead no envio do formulário e Contact no clique de ligar/SMS —
// com o gtag do Google intocado. Roda: node verify_pixel.mjs
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { join, extname } from 'node:path';

const ROOT = new URL('./site/', import.meta.url).pathname;
const MIME = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.xml': 'application/xml', '.txt': 'text/plain' };

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
await new Promise(r => server.listen(8791, r));

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
// Sem rede externa: o fbevents.js real não carrega, então o fbq fica no modo
// "stub com fila" do snippet oficial — a fila (fbq.queue) é a prova dos eventos.
const ctx = await browser.newContext();
await ctx.route('https://connect.facebook.net/**', r => r.fulfill({ status: 200, contentType: 'text/javascript', body: '/* fbevents mock */' }));
await ctx.route('https://www.googletagmanager.com/**', r => r.fulfill({ status: 200, contentType: 'text/javascript', body: '/* gtag mock */' }));
await ctx.route('https://ipapi.co/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '{}' }));
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', e => errors.push('pageerror: ' + e.message));

let pass = 0, failCount = 0;
const check = (cond, msg) => { if (cond) { pass++; console.log('  ✓ ' + msg); } else { failCount++; console.log('  ✗ ' + msg); } };
const queue = () => page.evaluate(() => (window.fbq && window.fbq.queue ? window.fbq.queue.map(a => Array.prototype.slice.call(a)) : null));

// ── 1. Home com fbclid: pixel + PageView + encaminhamento ao app ────────────
await page.goto('http://localhost:8791/?fbclid=TESTE123&utm_source=facebook', { waitUntil: 'load' });
await page.waitForTimeout(900);
let q = await queue();
check(Array.isArray(q), 'fbq existe na home (snippet oficial carregou)');
check(q.some(c => c[0] === 'init' && c[1] === '2304367959989921'), "fbq('init') com o pixel novo 2304367959989921");
check(q.some(c => c[0] === 'track' && c[1] === 'PageView'), 'PageView disparado no carregamento');
const appHref = await page.evaluate(() => { const a = document.querySelector('a[href*="app.signatureluxurycleaning.com"]'); return a ? a.getAttribute('href') : ''; });
check(appHref.includes('fbclid=TESTE123'), `fbclid viaja site→app no link do app (${appHref.slice(0, 80)}…)`);
check(appHref.includes('utm_source=facebook'), 'utm_source continua viajando junto');

// ── 2. Contact: clique em link de SMS ───────────────────────────────────────
await page.evaluate(() => { const a = document.querySelector('a[href^="sms:"], a[href^="tel:"]'); a.addEventListener('click', e => e.preventDefault()); a.click(); });
q = await queue();
check(q.some(c => c[0] === 'track' && c[1] === 'Contact'), 'Contact disparado no clique de ligar/SMS');

// ── 3. Lead: formulário de cotação enviado com sucesso ──────────────────────
await ctx.route('https://slc-app-worker.booking-f8e.workers.dev/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, firstName: 'Test', phoneDisplay: '(650) 555-0100' }) }));
await page.goto('http://localhost:8791/?fbclid=TESTE123', { waitUntil: 'load' });
await page.waitForTimeout(2600); // > MIN_FILL_MS do anti-robô
await page.evaluate(() => {
  const f = document.getElementById('qfForm');
  f.querySelector('[name="name"]').value = 'Pixel Teste';
  f.querySelector('[name="phone"]').value = '(650) 555-0100';
  f.querySelector('[name="zip"]').value = '94002';
  f.querySelector('[name="consent"]').checked = true;
});
await page.click('#qfForm .qf-btn');
await page.waitForTimeout(900);
const okShown = await page.evaluate(() => !document.getElementById('qfSuccess').hidden);
check(okShown, 'formulário confirmou o envio (tela de sucesso)');
q = await queue();
check(q.some(c => c[0] === 'track' && c[1] === 'Lead'), 'Lead da Meta disparado no sucesso do formulário');

// ── 4. Google intocado: gtag segue definido e com os mesmos eventos ─────────
const gtagOk = await page.evaluate(() => typeof window.gtag === 'function' && Array.isArray(window.dataLayer));
check(gtagOk, 'gtag do Google continua funcionando na mesma página');
const genLead = await page.evaluate(() => window.dataLayer.some(a => Array.prototype.slice.call(a).join('|').includes('generate_lead')));
check(genLead, 'generate_lead do Google continua disparando no mesmo envio');

// ── 5. Página de serviço e de cidade também têm o pixel ─────────────────────
for (const path of ['/services/deep-cleaning/', '/locations/palo-alto/']) {
  await page.goto('http://localhost:8791' + path, { waitUntil: 'load' });
  await page.waitForTimeout(500);
  q = await queue();
  check(q && q.some(c => c[0] === 'init'), `pixel ativo em ${path}`);
}

check(errors.length === 0, `nenhum erro de JavaScript nas páginas (${errors.length ? errors.join(' | ') : 'limpo'})`);

await browser.close();
server.close();
console.log(`\n${pass} ✓ · ${failCount} ✗`);
process.exit(failCount ? 1 : 0);
