// Prova do passo 10 (21/09): conversão em página de serviço, gclid encaminhado ao app, âncora na carga.
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
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
await new Promise(r => server.listen(8789, r));

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
// bloqueia gtag real e grava as chamadas
await ctx.route('**/googletagmanager.com/**', r => r.fulfill({ status: 200, contentType: 'text/javascript', body: '' }));
// a página define gtag(){dataLayer.push(arguments)} — lemos o dataLayer
const CALLS = 'Array.from(window.dataLayer || []).map(a => Array.from(a))';
let failures = 0;
const check = (cond, msg) => { console.log((cond ? '  ✓ ' : '  ✗ ') + msg); if (!cond) failures++; };

// 1) página de serviço com gclid — onde caem 100% dos cliques pagos
const page = await ctx.newPage();
page.on('pageerror', e => console.log('  pageerror:', e.message));
await page.goto('http://localhost:8789/services/regular-cleaning/?gclid=TESTGCLID123&utm_campaign=peninsula', { waitUntil: 'load' });
await page.waitForTimeout(500);
const hrefs = await page.$$eval('a[href*="app.signatureluxurycleaning.com"]', as => as.map(a => a.getAttribute('href')));
check(hrefs.length >= 3, `página de serviço tem links para o app (${hrefs.length})`);
check(hrefs.every(h => h.includes('gclid=TESTGCLID123')), 'TODOS os links do app levam o gclid');
check(hrefs.every(h => h.includes('src=site-svc-regular-cleaning')), 'o ?src original foi preservado');
check(hrefs.every(h => h.includes('utm_campaign=peninsula')), 'utm_campaign também viaja');
// clique no primeiro link do app sem sair da página
await page.$eval('a[href*="app.signatureluxurycleaning.com"]', a => { a.addEventListener('click', e => e.preventDefault()); a.click(); });
let calls = await page.evaluate(CALLS);
const conv = calls.filter(c => c[0] === 'event' && c[1] === 'conversion').map(c => c[2] && c[2].send_to);
check(conv.includes('AW-17096585184/RBjKCM2TsfkcEODfpNg_'), `clique no app dispara a conversão "Site - clique para o app" (${JSON.stringify(conv)})`);
check(conv.filter(x => x === 'AW-17096585184/RBjKCM2TsfkcEODfpNg_').length === 1, 'dispara UMA vez (sem bloco duplicado)');
// tel:
await page.$eval('a[href^="tel:"]', a => { a.addEventListener('click', e => e.preventDefault()); a.click(); });
calls = await page.evaluate(CALLS);
check(calls.some(c => c[1] === 'conversion' && c[2].send_to === 'AW-17096585184/KbSHCOeFsPkcEODfpNg_'), 'clique em ligar dispara "Site - clique ligar/SMS"');

// 2) navegação site→site mantém o gclid (sessionStorage) e a home continua disparando uma vez só
await page.goto('http://localhost:8789/', { waitUntil: 'load' });
await page.waitForTimeout(500);
const homeHrefs = await page.$$eval('a[href*="app.signatureluxurycleaning.com"]', as => as.map(a => a.getAttribute('href')));
check(homeHrefs.length > 10 && homeHrefs.every(h => h.includes('gclid=TESTGCLID123')), `home (2ª página da visita) ainda leva o gclid em todos os ${homeHrefs.length} links`);
await page.$eval('a.btn-download-hero[href*="app.signatureluxurycleaning.com"], a[href*="app.signatureluxurycleaning.com"]', a => { a.addEventListener('click', e => e.preventDefault()); a.click(); });
calls = await page.evaluate(CALLS);
check(calls.filter(c => c[1] === 'conversion' && c[2].send_to === 'AW-17096585184/RBjKCM2TsfkcEODfpNg_').length === 1, 'home: conversão dispara UMA vez (bloco antigo, sem duplicar)');

// 3) âncora na carga (sitelinks /#reviews e /#areas)
const p2 = await ctx.newPage();
await p2.goto('http://localhost:8789/#areas', { waitUntil: 'load' });
await p2.waitForTimeout(1600);
const y = await p2.evaluate(() => Math.round(window.scrollY));
const top = await p2.evaluate(() => Math.round(document.getElementById('areas').getBoundingClientRect().top));
check(y > 500 && Math.abs(top) < 120, `/#areas rola até a seção na carga (scrollY=${y}, topo da seção=${top}px)`);
await p2.goto('http://localhost:8789/#reviews', { waitUntil: 'load' });
await p2.waitForTimeout(1600);
const y2 = await p2.evaluate(() => Math.round(window.scrollY));
check(y2 > 500, `/#reviews rola até a seção na carga (scrollY=${y2})`);

// 4) sem parâmetros: nenhum link é alterado
const p3 = await ctx.newPage();
await p3.goto('http://localhost:8789/services/deep-cleaning/', { waitUntil: 'load' });
await p3.waitForTimeout(400);
const clean = await p3.$$eval('a[href*="app.signatureluxurycleaning.com"]', as => as.map(a => a.getAttribute('href')));
check(clean.every(h => !h.includes('gclid') && h.includes('?src=site-svc-deep-cleaning')), 'visita sem anúncio: links intactos');

await browser.close();
server.close();
console.log(failures ? `FALHOU: ${failures}` : 'PROVA OK');
process.exit(failures ? 1 : 0);
