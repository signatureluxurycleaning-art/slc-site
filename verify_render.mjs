// Prova visual do pacote v1: renderiza o site patcheado em celular e desktop.
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
await new Promise(r => server.listen(8788, r));

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const errors = [];
const shot = async (page, name, opts = {}) => page.screenshot({ path: `shots/${name}.png`, ...opts });

// ── CELULAR 390×844 ─────────────────────────────────────────────
const m = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
const mp = await m.newPage();
mp.on('pageerror', e => errors.push('mobile pageerror: ' + e.message));
await mp.goto('http://localhost:8788/', { waitUntil: 'networkidle' }).catch(() => {});
await mp.waitForTimeout(600);

// 1. faixa de preços visível no primeiro scroll?
const strip = await mp.locator('.hero-prices').first();
const stripVisible = await strip.isVisible().catch(() => false);
const stripBox = stripVisible ? await strip.boundingBox() : null;
console.log('MOBILE hero-prices visible:', stripVisible, 'top:', stripBox && Math.round(stripBox.y));
await shot(mp, 'm1_hero');

// 2. hero-visual (mockup) escondido no mobile?
console.log('MOBILE hero-visual hidden:', !(await mp.locator('.hero-visual').first().isVisible().catch(() => true)));

// 3. cards com preço
await mp.locator('#services').scrollIntoViewIfNeeded();
await mp.waitForTimeout(700);
const priceCount = await mp.locator('.service-card .service-price').count();
console.log('MOBILE service-price count:', priceCount);
await shot(mp, 'm2_services_card');

// 4. before/after
await mp.locator('.ba-strip').scrollIntoViewIfNeeded();
await mp.waitForTimeout(700);
console.log('MOBILE BA pairs:', await mp.locator('.ba-pair').count());
await shot(mp, 'm3_before_after');

// 5. rodapé: email + © 2026
await mp.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
await mp.waitForTimeout(500);
const footTxt = await mp.locator('.footer').innerText();
console.log('MOBILE footer email ok:', footTxt.includes('booking@signatureluxurycleaning.com'), '| © 2026:', footTxt.includes('© 2026'), '| 22:', footTxt.includes('22'));
await shot(mp, 'm4_footer');

// 6. japonês
await mp.evaluate(() => { localStorage.setItem('slc_lang', 'ja'); });
await mp.goto('http://localhost:8788/', { waitUntil: 'networkidle' }).catch(() => {});
await mp.waitForTimeout(600);
const heroJa = await mp.locator('.hero-title').innerText();
console.log('MOBILE ja hero title:', JSON.stringify(heroJa.slice(0, 30)));
await shot(mp, 'm5_japanese');
await mp.evaluate(() => localStorage.removeItem('slc_lang'));

// 7. cidade: reviews reais
await mp.goto('http://localhost:8788/locations/palo-alto/', { waitUntil: 'networkidle' }).catch(() => {});
const revTxt = await mp.locator('.reviews-grid').first().innerText().catch(() => '');
console.log('CITY reviews real:', revTxt.includes('Google review') && !revTxt.includes('Jennifer'), '| authors:', (revTxt.match(/— ([^,\n]+)/g) || []).join(' / '));

// 8. 404
await mp.goto('http://localhost:8788/404.html', { waitUntil: 'networkidle' }).catch(() => {});
await shot(mp, 'm6_404');

// ── DESKTOP 1450×900 ────────────────────────────────────────────
const d = await browser.newContext({ viewport: { width: 1450, height: 900 }, deviceScaleFactor: 1 });
const dp = await d.newPage();
dp.on('pageerror', e => errors.push('desktop pageerror: ' + e.message));
await dp.goto('http://localhost:8788/', { waitUntil: 'networkidle' }).catch(() => {});
await dp.waitForTimeout(800);
console.log('DESKTOP hero-prices hidden:', !(await dp.locator('.hero-prices').first().isVisible().catch(() => true)));
// badge não sobrepõe o greeting?
const b1 = await dp.locator('.badge-rating').boundingBox();
const g1 = await dp.locator('.phone-greeting').boundingBox();
const overlap = b1 && g1 && !(b1.y > g1.y + g1.height || g1.y > b1.y + b1.height || b1.x > g1.x + g1.width || g1.x > b1.x + b1.width);
console.log('DESKTOP badge overlaps greeting:', overlap === true);
await shot(dp, 'd1_hero');
await dp.locator('#services').scrollIntoViewIfNeeded();
await dp.waitForTimeout(900);
await shot(dp, 'd2_services');
await dp.locator('.ba-strip').scrollIntoViewIfNeeded();
await dp.waitForTimeout(900);
await shot(dp, 'd3_before_after');

console.log('PAGE ERRORS:', errors.length ? errors : 'none');
await browser.close();
server.close();
