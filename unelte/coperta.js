// Coperta unei cronici, 1200×630 JPG, în albastrul blogului.
// Rulare: node unelte/coperta.js cronici/<id>.coperta.json cronici/<id>.jpg
// Datele: { titlu, competitie, data, gazde: { nume, sofa_id }, oaspeti: { nume, sofa_id }, scor: [g, o], marcatori }
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [, , dataFile, outFile] = process.argv;
if (!dataFile || !outFile) {
	console.error('Rulare: node unelte/coperta.js <date.json> <iesire.jpg>');
	process.exit(1);
}

const d = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const dir = __dirname;
const dataUri = (file, type) => `data:${type};base64,${fs.readFileSync(file).toString('base64')}`;
const sigla = (team) => {
	const file = path.join(dir, 'sigle', `${team.sofa_id}.png`);
	return fs.existsSync(file) ? `<img class="sigla" src="${dataUri(file, 'image/png')}">` : '<div class="sigla"></div>';
};
const logoFile = path.join(dir, 'logo.png');
const logo = fs.existsSync(logoFile)
	? `<img class="logo" src="${dataUri(logoFile, 'image/png')}">`
	: '<div class="logo-text">Poveștile<br>Științei</div>';
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const font = (f) => dataUri(path.join(dir, 'fonturi', f), 'font/woff2');

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Sofia; font-weight: 800; src: url(${font('sofia-sans-extra-condensed-latin-800-normal.woff2')}); }
@font-face { font-family: Sofia; font-weight: 800; src: url(${font('sofia-sans-extra-condensed-latin-ext-800-normal.woff2')}); unicode-range: U+0100-024F, U+0218-021B; }
* { margin: 0; box-sizing: border-box; }
body { width: 1200px; height: 630px; overflow: hidden; font-family: Inter, sans-serif; color: #fff;
	background:
		radial-gradient(ellipse 60% 45% at 15% 0%, rgba(255,255,255,.28), transparent 70%),
		radial-gradient(ellipse 60% 45% at 85% 0%, rgba(255,255,255,.22), transparent 70%),
		linear-gradient(180deg, #0058B0 0%, #003F80 45%, #071A33 100%); }
.gazon { position: absolute; left: 0; right: 0; bottom: 0; height: 150px;
	background: repeating-linear-gradient(90deg, rgba(255,255,255,.05) 0 80px, transparent 80px 160px), linear-gradient(180deg, #0b3a24, #06261a); }
.gazon::before { content: ''; position: absolute; left: 0; right: 0; top: 0; height: 3px; background: rgba(255,255,255,.35); }
.wrap { position: absolute; inset: 0; padding: 48px 60px; display: grid; grid-template-columns: 220px 1fr; gap: 50px; align-items: center; }
.logo { width: 220px; height: 220px; object-fit: contain; filter: drop-shadow(0 6px 18px rgba(0,0,0,.45)); }
.logo-text { font-family: Sofia; font-weight: 800; font-size: 64px; line-height: .95; text-transform: uppercase; }
.competitie { display: inline-block; background: #fff; color: #0058B0; font-family: Sofia; font-weight: 800; font-size: 26px;
	text-transform: uppercase; padding: 4px 14px; letter-spacing: .5px; }
.data { display: inline-block; margin-left: 12px; font-size: 18px; opacity: .85; }
h1 { font-family: Sofia; font-weight: 800; font-size: 64px; line-height: .98; text-transform: uppercase; margin: 18px 0 22px; text-shadow: 0 3px 12px rgba(0,0,0,.35); }
.tabela { display: flex; align-items: center; gap: 18px; }
.sigla { width: 64px; height: 64px; object-fit: contain; }
.echipa { font-family: Sofia; font-weight: 800; font-size: 30px; text-transform: uppercase; max-width: 230px; line-height: 1; }
.scor { display: flex; gap: 6px; font-family: Sofia; font-weight: 800; font-size: 56px; }
.scor span { background: #071A33; padding: 0 16px; border: 2px solid rgba(255,255,255,.25); }
.marcatori { margin-top: 14px; font-size: 18px; opacity: .9; }
.site { position: absolute; right: 60px; bottom: 26px; font-family: Sofia; font-weight: 800; font-size: 24px; letter-spacing: 1px; opacity: .9; }
</style></head><body>
<div class="gazon"></div>
<div class="wrap">
	<div>${logo}</div>
	<div>
		<span class="competitie">${esc(d.competitie)}</span><span class="data">${esc(d.data)}</span>
		<h1>${esc(d.titlu)}</h1>
		<div class="tabela">
			${sigla(d.gazde)}<div class="echipa">${esc(d.gazde.nume)}</div>
			<div class="scor"><span>${esc(d.scor[0])}</span><span>${esc(d.scor[1])}</span></div>
			<div class="echipa">${esc(d.oaspeti.nume)}</div>${sigla(d.oaspeti)}
		</div>
		<div class="marcatori">${esc(d.marcatori)}</div>
	</div>
</div>
<div class="site">POVESTILESTIINTEI.RO</div>
</body></html>`;

(async () => {
	const browser = await chromium.launch();
	const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
	await page.setContent(html, { waitUntil: 'load' });
	await page.evaluate(() => document.fonts.ready);
	await page.screenshot({ path: outFile, type: 'jpeg', quality: 88 });
	await browser.close();
	console.log('Coperta: ' + outFile);
})();
