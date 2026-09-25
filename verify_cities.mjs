// Prova do passo 12 (25/09/2026): Foster City + Redwood Shores + 23 cidades.
// Sobe site/ num servidor local, abre as páginas tocadas em desktop e celular
// e confere o que o anúncio/sitelink vai mostrar. Sai com código 1 se algo falhar.
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import { join, extname } from 'node:path';

const ROOT = new URL('./site/', import.meta.url).pathname;
const PORT = 8790;
const BASE = `http://localhost:${PORT}`;
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.xml': 'application/xml', '.txt': 'text/plain', '.woff2': 'font/woff2' };

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
await new Promise(r => server.listen(PORT, r));
await mkdir(new URL('./shots/', import.meta.url).pathname, { recursive: true });

let failures = 0;
const check = (cond, msg) => { console.log(`${cond ? '✓' : '✗'} ${msg}`); if (!cond) failures++; };
const status = async (url) => (await fetch(url)).status;

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });

async function openPage(ctx, path) {
  const page = await ctx.newPage();
  const errors = [];
  const missing = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('response', r => { if (r.url().startsWith(BASE) && r.status() >= 400) missing.push(`${r.status()} ${r.url().slice(BASE.length)}`); });
  // rede externa (fontes, gtag, ipapi) não existe aqui — bloqueia para não travar
  await page.route(u => !u.href.startsWith(BASE), r => r.abort());
  await page.goto(BASE + path, { waitUntil: 'load' });
  await page.waitForTimeout(500);
  return { page, errors, missing };
}

async function internalLinksOk(page) {
  const hrefs = await page.$$eval('a[href]', as => as.map(a => a.getAttribute('href')));
  const internal = [...new Set(hrefs.filter(h => h && !h.startsWith('#') && !/^(https?:|tel:|sms:|mailto:|javascript:)/.test(h)))];
  const bad = [];
  for (const h of internal) {
    const url = new URL(h, page.url());
    url.hash = '';
    if (await status(url.href) !== 200) bad.push(h);
  }
  return { count: internal.length, bad };
}

// ── DESKTOP ─────────────────────────────────────────────────────────────────
const desk = await browser.newContext({ viewport: { width: 1366, height: 900 } });

{ // Foster City (página nova — destino do sitelink)
  const { page, errors, missing } = await openPage(desk, '/locations/foster-city/');
  check(await page.title() === 'House Cleaning Foster City CA | Signature Luxury Cleaning', 'Foster City: título da aba');
  check((await page.locator('h1').innerText()).replace(/\s+/g, ' ').trim() === 'House Cleaning Foster City, CA', 'Foster City: H1');
  check((await page.locator('.hero-badge').first().textContent()).includes('Foster City, San Mateo County'), 'Foster City: badge do hero');
  const pills = await page.locator('.neighborhood-pill').allInnerTexts();
  check(JSON.stringify(pills) === JSON.stringify(['Sea Colony', 'Treasure Isle', 'Isle Cove', 'Marina Point', 'Edgewater']), `Foster City: bairros ${JSON.stringify(pills)}`);
  const landmarks = await page.locator('.landmarks-list li').allInnerTexts();
  check(landmarks.includes('Leo J. Ryan Park') && landmarks.includes('Foster City Lagoon'), `Foster City: marcos ${JSON.stringify(landmarks)}`);
  const stats = await page.locator('.city-stat-number').allInnerTexts();
  check(stats.includes('33,805') && stats.includes('$1.8M'), `Foster City: população e valor ${JSON.stringify(stats)}`);
  const authors = await page.locator('.review-author').allInnerTexts();
  check(authors.length === 3 && authors.every(a => a.includes('Google review')) && !authors.some(a => a.includes('Mia')), `Foster City: 3 reviews reais ${JSON.stringify(authors.map(a => a.split(',')[0]))}`);
  const appHref = await page.locator('#btn-pwa-city').getAttribute('href');
  check(appHref === 'https://app.signatureluxurycleaning.com/download?src=site-foster-city', `Foster City: botão do app com origem própria (${appHref})`);
  const bodyText = await page.locator('body').innerText();
  check(!/Hillsdale|Baywood|Fiesta Gardens|94401|Coyote Point/.test(bodyText), 'Foster City: nenhum texto de San Mateo sobrando na tela');
  const ld = await page.$$eval('script[type="application/ld+json"]', ss => ss.map(s => { try { JSON.parse(s.textContent); return true; } catch { return false; } }));
  check(ld.length >= 2 && ld.every(Boolean), `Foster City: ${ld.length} blocos JSON-LD válidos`);
  const links = await internalLinksOk(page);
  check(links.bad.length === 0, `Foster City: ${links.count} links internos, todos 200 (quebrados: ${JSON.stringify(links.bad)})`);
  check(errors.length === 0, `Foster City: sem erro de JS (${errors.join(' | ')})`);
  check(missing.length === 0, `Foster City: nenhum arquivo local faltando (${missing.slice(0, 4).join(', ')})`);
  await page.screenshot({ path: 'shots/fc_desktop_hero.png' });
  await page.locator('.neighborhoods-grid').scrollIntoViewIfNeeded();
  await page.screenshot({ path: 'shots/fc_desktop_neighborhoods.png' });
  await page.close();
}

{ // Redwood City (sitelink "Redwood City Cleaning")
  const { page, errors } = await openPage(desk, '/locations/redwood-city/');
  check((await page.locator('.hero-badge').first().textContent()).includes('Redwood Shores & Emerald Hills'), 'Redwood City: badge cita Redwood Shores & Emerald Hills');
  const pills = await page.locator('.neighborhood-pill').allInnerTexts();
  check(pills[0] === 'Redwood Shores' && pills.includes('Emerald Hills'), `Redwood City: bairros ${JSON.stringify(pills)}`);
  const faq = await page.locator('.faq-item').allTextContents(); // <details> fechado: innerText esconde a resposta
  check(faq.some(f => f.includes('94065')), 'Redwood City: FAQ com ZIP 94065 (Redwood Shores)');
  const desc = await page.locator('meta[name="description"]').getAttribute('content');
  check(desc.includes('Redwood Shores') && desc.includes('Emerald Hills'), 'Redwood City: meta description');
  check(errors.length === 0, `Redwood City: sem erro de JS (${errors.join(' | ')})`);
  await page.screenshot({ path: 'shots/rc_desktop_hero.png' });
  await page.close();
}

{ // San Mateo e Belmont: o link "Foster City" agora abre a página nova
  for (const slug of ['san-mateo', 'belmont']) {
    const { page } = await openPage(desk, `/locations/${slug}/`);
    const fc = await page.$$eval('a', as => as.filter(a => a.textContent.trim().endsWith('Foster City')).map(a => a.getAttribute('href')));
    check(fc.length >= 1 && fc.every(h => h === '/locations/foster-city/'), `${slug}: ${fc.length} link(s) "Foster City" → /locations/foster-city/`);
    const links = await internalLinksOk(page);
    check(links.bad.length === 0, `${slug}: links internos todos 200 (quebrados: ${JSON.stringify(links.bad)})`);
    await page.close();
  }
}

{ // Home: grade de áreas, contagem, FAQ, clique no pill novo
  const { page, errors } = await openPage(desk, '/');
  const pills = await page.locator('#areas .area-pill').allInnerTexts();
  check(pills.length === 23 && pills.includes('Foster City'), `home: ${pills.length} cidades na grade, com Foster City`);
  check((await page.locator('.hero-stat .number').allInnerTexts()).includes('23'), 'home: contador "23 Cities Served"');
  check((await page.locator('#areas .section-subtitle').innerText()).includes('23 cities'), 'home: subtítulo de áreas com 23');
  const faqAreas = await page.locator('.faq-item', { hasText: 'What areas do you serve?' }).first().textContent();
  check(faqAreas.includes('Foster City') && faqAreas.includes('Hillsborough') && !faqAreas.includes('Fremont'), 'home: FAQ de áreas cita a Península (sem Fremont/San Jose)');
  const links = await internalLinksOk(page);
  check(links.bad.length === 0, `home: ${links.count} links internos, todos 200 (quebrados: ${JSON.stringify(links.bad)})`);
  check(errors.length === 0, `home: sem erro de JS (${errors.join(' | ')})`);
  await page.locator('#areas').scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.screenshot({ path: 'shots/home_areas_23.png' });
  await page.locator('#areas a.area-pill', { hasText: 'Foster City' }).click();
  await page.waitForLoadState('load');
  check(page.url() === `${BASE}/locations/foster-city/`, `home: clique no pill abre ${page.url().slice(BASE.length)}`);
  await page.close();
}

{ // traduções: a contagem nova aparece nas 7 línguas
  const want = { en: '23 cities', zh: '23个城市', hi: '23 शहरों', tl: '23 lungsod', vi: '23 thành phố', ko: '23개 도시', ja: '23都市' };
  for (const [lang, token] of Object.entries(want)) {
    const { page } = await openPage(desk, `/?lang=${lang}`);
    const sub = await page.locator('#areas .section-subtitle').innerText();
    check(sub.includes(token) && !/22/.test(sub), `home ?lang=${lang}: "${token}"`);
    await page.close();
  }
}

// ── CELULAR (85% dos cliques pagos vêm do celular) ──────────────────────────
const mob = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
for (const path of ['/locations/foster-city/', '/locations/redwood-city/']) {
  const { page, errors } = await openPage(mob, path);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  check(overflow <= 1, `celular ${path}: sem rolagem horizontal (${overflow}px)`);
  check(errors.length === 0, `celular ${path}: sem erro de JS`);
  const name = path.includes('foster') ? 'fc' : 'rc';
  await page.screenshot({ path: `shots/${name}_mobile_hero.png` });
  await page.close();
}

await browser.close();
server.close();
console.log(failures ? `FALHOU: ${failures} verificação(ões)` : 'OK: passo 12 provado no navegador.');
process.exit(failures ? 1 : 0);
