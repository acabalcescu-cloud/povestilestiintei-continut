// Coperta unui articol din rubrica „Penalty cu George”, 1200×630 JPG.
// Rulare: node unelte/coperta-george.js <date.json> <iesire.jpg>   date: { titlu, data: "AAAA-LL-ZZ hh:mm" }
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [, , dataFile, outFile] = process.argv;
if (!dataFile || !outFile) {
	console.error('Rulare: node unelte/coperta-george.js <date.json> <iesire.jpg>');
	process.exit(1);
}

const LUNI = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie'];
const d = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const [an, luna, zi] = d.data.slice(0, 10).split('-').map(Number);
const dir = __dirname;
const uri = (f, t) => `data:${t};base64,${fs.readFileSync(path.join(dir, f)).toString('base64')}`;
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const titleSize = d.titlu.length > 70 ? 58 : d.titlu.length > 45 ? 66 : 76;

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Sofia; font-weight: 800; src: url(${uri('fonturi/sofia-sans-extra-condensed-latin-800-normal.woff2', 'font/woff2')}); }
@font-face { font-family: Sofia; font-weight: 800; src: url(${uri('fonturi/sofia-sans-extra-condensed-latin-ext-800-normal.woff2', 'font/woff2')}); unicode-range: U+0100-024F, U+0218-021B; }
* { margin: 0; box-sizing: border-box; }
body { width: 1200px; height: 630px; overflow: hidden; font-family: Inter, sans-serif; color: #fff;
	background: radial-gradient(ellipse 70% 80% at 85% 30%, rgba(255,255,255,.18), transparent 60%), linear-gradient(120deg, #0058B0 0%, #003F80 60%, #071A33 100%); }
.teren { position: absolute; inset: 0; }
.foto { position: absolute; right: 10px; bottom: 0; height: 600px; filter: drop-shadow(0 10px 30px rgba(0,0,0,.35)); }
.text { position: absolute; left: 70px; top: 70px; width: 600px; height: 490px; display: flex; flex-direction: column; }
.rubrica { display: flex; align-items: center; gap: 16px; }
.rubrica img { width: 64px; height: 64px; object-fit: contain; }
.rubrica span { font-family: Sofia; font-weight: 800; font-size: 30px; letter-spacing: 1px; text-transform: uppercase; color: #9CCBFF; }
h1 { font-family: Sofia; font-weight: 800; font-size: ${titleSize}px; line-height: 1; margin-top: 34px; text-shadow: 0 3px 14px rgba(0,0,0,.3); }
.motto { font-family: Sofia; font-weight: 800; font-size: 24px; letter-spacing: 1px; text-transform: uppercase; color: #fff; opacity: .75; margin-top: auto; margin-bottom: 10px; }
.autor { font-size: 22px; } .autor b { font-weight: 700; }
.site { font-family: Sofia; font-weight: 800; font-size: 22px; letter-spacing: 1px; opacity: .85; margin-top: 6px; }
</style></head><body>
<svg class="teren" viewBox="0 0 1200 630" fill="none" stroke="rgba(255,255,255,.13)" stroke-width="4">
	<rect x="650" y="-4" width="570" height="250"/><rect x="820" y="-4" width="240" height="90"/>
	<path d="M820 246 A120 120 0 0 0 1060 246"/><circle cx="940" cy="180" r="9" fill="rgba(255,255,255,.35)" stroke="none"/>
</svg>
<img class="foto" src="${uri('george.png', 'image/png')}">
<div class="text">
	<div class="rubrica"><img src="${uri('logo.png', 'image/png')}"><span>Penalty cu George</span></div>
	<h1>${esc(d.titlu)}</h1>
	<div class="motto">Fără ezitare, de partea Științei</div>
	<div class="autor">de <b>George</b> · ${zi} ${LUNI[luna - 1]} ${an}</div>
	<div class="site">POVESTILESTIINTEI.RO</div>
</div>
</body></html>`;

(async () => {
	const browser = await chromium.launch();
	const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
	await page.setContent(html, { waitUntil: 'load' });
	await page.evaluate(() => document.fonts.ready);
	// Titlul începe de la mărimea calculată și scade până încape în cel mult 5 rânduri, deasupra autorului.
	await page.evaluate(() => {
		const h1 = document.querySelector('h1');
		const autor = document.querySelector('.autor');
		for (let px = parseInt(getComputedStyle(h1).fontSize, 10); px >= 36; px -= 2) {
			h1.style.fontSize = px + 'px';
			if (Math.round(h1.getBoundingClientRect().height / px) <= 5 && h1.getBoundingClientRect().bottom <= autor.getBoundingClientRect().top - 24) break;
		}
	});
	await page.screenshot({ path: outFile, type: 'jpeg', quality: 88 });
	await browser.close();
	console.log('Coperta: ' + outFile);
})();
