// Coperta unei știri, 1200×630 JPG.
// Rulare: node unelte/coperta-stire.js <date.json> <iesire.jpg>   date: { titlu, rubrica?, data: "AAAA-LL-ZZ hh:mm" }
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [, , dataFile, outFile] = process.argv;
if (!dataFile || !outFile) {
	console.error('Rulare: node unelte/coperta-stire.js <date.json> <iesire.jpg>');
	process.exit(1);
}

const LUNI = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie'];
const d = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const [an, luna, zi] = d.data.slice(0, 10).split('-').map(Number);
const dir = __dirname;
const uri = (f, t) => `data:${t};base64,${fs.readFileSync(path.join(dir, f)).toString('base64')}`;
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
// Titlul stă în coloana din stânga (cel mult 5 rânduri); dreapta rămâne liberă pentru fotografiile jucătorilor.

// Coperți pe competiții: rubrica „SuperLiga”, „Cupa României” sau „Conference League” (ori câmpul „competitie”)
// schimbă fundalul și emblema. Imaginile oficiale stau în unelte/competitii/.
const COMPETITII = {
	superliga: {
		fundal: 'radial-gradient(ellipse 60% 80% at 82% 40%, rgba(255,255,255,.16), transparent 60%), linear-gradient(120deg, #E30613 0%, #A3000E 55%, #3A0006 100%)',
		icon: 'competitii/superliga-logo.png', iconRadius: '12px',
		emblema: 'competitii/superliga-trofeu.png', emblemaStil: 'right: 70px; height: 500px; opacity: .55; filter: drop-shadow(0 20px 40px rgba(0,0,0,.45));',
		culoare: '#FFD1D4',
	},
	cupa: {
		fundal: 'radial-gradient(circle at 1px 1px, rgba(255,255,255,.18) 1px, transparent 0) 0 0/26px 26px, linear-gradient(120deg, #E0101E 0%, #8E1340 45%, #2A1660 80%, #120B3A 100%)',
		icon: 'competitii/cupa-logo.png',
		emblema: 'competitii/cupa-logo.png', emblemaStil: 'right: 80px; height: 460px; opacity: .5; filter: drop-shadow(0 20px 40px rgba(0,0,0,.4));',
		culoare: '#FFE27A',
	},
	conference: {
		fundal: 'linear-gradient(90deg, #020805 0%, #031109 45%, rgba(3,17,9,0) 70%), url(__CONFERENCE_FUNDAL__) right center/auto 100% no-repeat, #020805',
		icon: 'competitii/conference-logo.png',
		emblema: '', emblemaStil: '',
		culoare: '#3BE37A',
	},
};
const cheieCompetitie = (() => {
	const t = String(d.competitie || d.rubrica || '').toLowerCase();
	if (/superliga|liga 1|liga i\b/.test(t)) return 'superliga';
	if (/cupa rom/.test(t)) return 'cupa';
	if (/conference|uecl/.test(t)) return 'conference';
	return '';
})();
const comp = COMPETITII[cheieCompetitie];
if (comp && cheieCompetitie === 'conference') comp.fundal = comp.fundal.replace('__CONFERENCE_FUNDAL__', uri('competitii/conference-fundal.jpg', 'image/jpeg'));
const mime = (f) => (f.endsWith('.png') ? 'image/png' : 'image/jpeg');

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Sofia; font-weight: 800; src: url(${uri('fonturi/sofia-sans-extra-condensed-latin-800-normal.woff2', 'font/woff2')}); }
@font-face { font-family: Sofia; font-weight: 800; src: url(${uri('fonturi/sofia-sans-extra-condensed-latin-ext-800-normal.woff2', 'font/woff2')}); unicode-range: U+0100-024F, U+0218-021B; }
* { margin: 0; box-sizing: border-box; }
body { width: 1200px; height: 630px; overflow: hidden; font-family: Inter, sans-serif; color: #fff;
	background: radial-gradient(ellipse 70% 80% at 85% 30%, rgba(255,255,255,.18), transparent 60%), linear-gradient(120deg, #0058B0 0%, #003F80 60%, #071A33 100%); }
.stema { position: absolute; right: 60px; top: 50%; height: 470px; transform: translateY(-50%) rotate(-6deg); opacity: .16; }
.text { position: absolute; left: 70px; top: 70px; width: 640px; height: 490px; display: flex; flex-direction: column; }
.rubrica { display: flex; align-items: center; gap: 16px; }
.rubrica img { width: 64px; height: 64px; object-fit: contain; }
.rubrica span { font-family: Sofia; font-weight: 800; font-size: 30px; letter-spacing: 1px; text-transform: uppercase; color: #9CCBFF; }
h1 { font-family: Sofia; font-weight: 800; font-size: 80px; line-height: 1; margin-top: 30px; text-shadow: 0 3px 14px rgba(0,0,0,.3); overflow-wrap: break-word; }
.autor { margin-top: auto; font-size: 22px; } .autor b { font-weight: 700; }
.emblema { position: absolute; top: 50%; transform: translateY(-50%); }
${comp ? `body { background: ${comp.fundal}; }` : ''}
.site { font-family: Sofia; font-weight: 800; font-size: 22px; letter-spacing: 1px; opacity: .85; margin-top: 6px; }
</style></head><body>
${comp ? (comp.emblema ? `<img class="emblema" style="${comp.emblemaStil}" src="${uri(comp.emblema, mime(comp.emblema))}">` : '') : `<img class="stema" src="${uri('logo.png', 'image/png')}">`}
<div class="text">
	<div class="rubrica">${comp ? `<img src="${uri(comp.icon, mime(comp.icon))}" style="${comp.iconRadius ? 'border-radius:' + comp.iconRadius : ''}">` : ''}<img src="${uri('logo.png', 'image/png')}"><span${comp ? ` style="color:${comp.culoare}"` : ''}>${esc(d.rubrica || 'Știri')}</span></div>
	<h1>${esc(d.titlu)}</h1>
	<div class="autor">de <b>George Fedorovici</b> · ${zi} ${LUNI[luna - 1]} ${an}</div>
	<div class="site">POVESTILESTIINTEI.RO</div>
</div>
</body></html>`;

(async () => {
	const browser = await chromium.launch();
	const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
	await page.setContent(html, { waitUntil: 'load' });
	await page.evaluate(() => document.fonts.ready);
	// Cea mai mare mărime la care titlul încape în cel mult 5 rânduri și nu atinge autorul.
	await page.evaluate(() => {
		const h1 = document.querySelector('h1');
		const autor = document.querySelector('.autor');
		for (let px = 80; px >= 36; px -= 2) {
			h1.style.fontSize = px + 'px';
			const randuri = Math.round(h1.getBoundingClientRect().height / px);
			if (randuri <= 5 && h1.getBoundingClientRect().bottom <= autor.getBoundingClientRect().top - 24) break;
		}
	});
	await page.screenshot({ path: outFile, type: 'jpeg', quality: 88 });
	await browser.close();
	console.log('Coperta: ' + outFile);
})();
