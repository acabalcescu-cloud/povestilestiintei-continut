// Infografica statisticilor unui meci (PNG, 1200 px lățime): scor, teren cu primul 11 și notele,
// inele (posesie, dueluri), bare de comparație, precizii și schimbări.
// Rulare: node unelte/statistici-meci.js <date.json> <iesire.png>
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [, , dataFile, outFile] = process.argv;
if (!dataFile || !outFile) {
	console.error('Rulare: node unelte/statistici-meci.js <date.json> <iesire.png>');
	process.exit(1);
}
const d = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const dir = __dirname;
const uri = (f, t) => `data:${t};base64,${fs.readFileSync(path.join(dir, f)).toString('base64')}`;
const font = (f) => uri(path.join('fonturi', f), 'font/woff2');
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const sigla = (id) => (fs.existsSync(path.join(dir, 'sigle', `${id}.png`)) ? uri(`sigle/${id}.png`, 'image/png') : '');
const nota = (n) => (n >= 7 ? '#21a35a' : n >= 6.5 ? '#c9a227' : n >= 6 ? '#e08a2a' : '#d6403a');
const NOI = '#2b8af7';
const EI = '#e2463b';

// Inel cu două valori (procente)
function inel(titlu, a, b, sub = '') {
	const r = 54;
	const c = 2 * Math.PI * r;
	const pa = a / (a + b);
	return `<div class="inel"><svg viewBox="0 0 140 140" width="150" height="150">
		<circle cx="70" cy="70" r="${r}" fill="none" stroke="${EI}" stroke-width="18"/>
		<circle cx="70" cy="70" r="${r}" fill="none" stroke="${NOI}" stroke-width="18" stroke-dasharray="${c * pa} ${c}" transform="rotate(-90 70 70)"/>
		<text x="70" y="66" text-anchor="middle" class="ival">${esc(a)}%</text>
		<text x="70" y="92" text-anchor="middle" class="ival2">${esc(b)}%</text></svg>
		<b>${esc(titlu)}</b>${sub ? `<small>${esc(sub)}</small>` : ''}</div>`;
}
// Bară dublă (valori absolute)
function bara(titlu, a, b) {
	const t = (+a) + (+b) || 1;
	return `<div class="bara"><span class="bv ${+a >= +b ? 'top' : ''}">${esc(a)}</span><div class="bt"><i>${esc(titlu)}</i>
		<div class="bl"><em style="width:${(a / t) * 100}%;background:${NOI}"></em></div><div class="br"><em style="width:${(b / t) * 100}%;background:${EI}"></em></div></div>
		<span class="bv r ${+b >= +a ? 'top' : ''}">${esc(b)}</span></div>`;
}
// Precizie (reușite/total)
function precizie(titlu, [a1, a2], [b1, b2]) {
	const pa = Math.round((a1 / a2) * 100);
	const pb = Math.round((b1 / b2) * 100);
	return `<div class="prec"><div><b style="color:${NOI}">${pa}%</b><small>${a1}/${a2}</small></div><span>${esc(titlu)}</span><div><b style="color:${EI}">${pb}%</b><small>${b1}/${b2}</small></div></div>`;
}

// Terenul: primul 11 al Științei, pe linii (portar în stânga)
const linii = {};
for (const j of d.primul11) (linii[j.linie] = linii[j.linie] || []).push(j);
const nLinii = Object.keys(linii).length;
let jucatori = '';
Object.keys(linii).sort().forEach((l, i) => {
	const lst = linii[l];
	const x = 7 + (i * 86) / (nLinii - 1);
	lst.forEach((j, k) => {
		const y = ((k + 1) * 100) / (lst.length + 1);
		const ic = [];
		for (let g = 0; g < (j.goluri || 0); g++) ic.push('<span class="ic">⚽</span>');
		if (j.pase) ic.push('<span class="ic">👟</span>');
		if (j.galben) ic.push('<span class="ic gal"></span>');
		if (j.schimbat) ic.push(`<span class="ic sch">${esc(j.schimbat)}'</span>`);
		jucatori += `<div class="jj" style="left:${x}%;top:${y}%"><div class="nr">${esc(j.nr)}${j.capitan ? '<sup>C</sup>' : ''}</div>
			<div class="nt" style="background:${nota(j.nota)}">${j.nota.toFixed(1)}</div><div class="nm">${esc(j.nume)}</div><div class="ics">${ic.join('')}</div></div>`;
	});
});
const zone = d.zone_pase ? `<div class="zone">${d.zone_pase.map((z) => `<div><b>${z}%</b></div>`).join('')}</div>` : '';

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Sofia; font-weight: 800; src: url(${font('sofia-sans-extra-condensed-latin-800-normal.woff2')}); }
@font-face { font-family: Sofia; font-weight: 800; src: url(${font('sofia-sans-extra-condensed-latin-ext-800-normal.woff2')}); unicode-range: U+0100-024F, U+0218-021B; }
* { margin: 0; box-sizing: border-box; }
body { width: 1200px; font-family: Inter, 'Helvetica Neue', Arial, sans-serif; color: #fff; background: linear-gradient(180deg, #0a2a55 0%, #071a33 60%, #050f1f 100%); padding: 40px 50px 30px; }
.sof { font-family: Sofia; font-weight: 800; text-transform: uppercase; }
.cap { display: flex; align-items: center; justify-content: space-between; }
.rub { font-family: Sofia; font-weight: 800; font-size: 22px; letter-spacing: 2px; color: #9CCBFF; text-transform: uppercase; }
.logo { height: 58px; }
.scor { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; margin: 24px 0 8px; }
.ech { display: flex; align-items: center; gap: 18px; font-family: Sofia; font-weight: 800; font-size: 40px; text-transform: uppercase; line-height: 1; }
.ech.r { justify-content: flex-end; text-align: right; }
.ech img { width: 96px; height: 96px; object-fit: contain; }
.rez { font-family: Sofia; font-weight: 800; font-size: 104px; line-height: 1; padding: 0 30px; letter-spacing: 4px; }
.marc { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; font-size: 18px; color: #cfe0f5; margin-bottom: 6px; }
.marc div:last-child { text-align: right; }
.info { text-align: center; color: #8fb0d6; font-size: 16px; margin: 6px 0 26px; }
h2 { font-family: Sofia; font-weight: 800; font-size: 30px; text-transform: uppercase; margin: 30px 0 14px; letter-spacing: 1px; }
h2 span { color: #9CCBFF; }
.teren { position: relative; height: 720px; border-radius: 22px; overflow: hidden; background: repeating-linear-gradient(90deg, #1f7a43 0 90px, #23894b 90px 180px); border: 3px solid rgba(255,255,255,.55); }
.teren .l { position: absolute; border: 3px solid rgba(255,255,255,.55); }
.zone { position: absolute; inset: 0; display: grid; grid-template-columns: 1fr 1fr 1fr; pointer-events: none; }
.zone div { display: flex; align-items: flex-end; justify-content: center; padding-bottom: 12px; border-right: 2px dashed rgba(255,255,255,.18); }
.zone b { font-family: Sofia; font-size: 22px; color: rgba(255,255,255,.65); }
.jj { position: absolute; transform: translate(-50%, -50%); text-align: center; width: 150px; }
.nr { width: 64px; height: 64px; margin: 0 auto; border-radius: 50%; background: #fff; color: #0a2a55; font-family: Sofia; font-weight: 800; font-size: 30px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 16px rgba(0,0,0,.35); border: 4px solid ${NOI}; position: relative; }
.nr sup { position: absolute; top: -6px; right: -8px; background: #c9a227; color: #fff; font-size: 14px; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.nt { display: inline-block; margin-top: -10px; position: relative; padding: 2px 8px; border-radius: 6px; font-weight: 800; font-size: 16px; }
.nm { font-family: Sofia; font-weight: 800; font-size: 20px; text-transform: uppercase; margin-top: 4px; text-shadow: 0 2px 6px rgba(0,0,0,.6); }
.ics { display: flex; gap: 4px; justify-content: center; margin-top: 3px; height: 22px; }
.ic { font-size: 15px; line-height: 22px; }
.ic.gal { width: 12px; height: 17px; background: #f5c518; border-radius: 2px; margin-top: 2px; }
.ic.sch { font-size: 13px; background: rgba(0,0,0,.45); border-radius: 10px; padding: 0 7px; color: #ffb3ad; }
.legenda { display: flex; gap: 22px; color: #8fb0d6; font-size: 14px; margin-top: 10px; }
.inele { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center; }
.inel b { display: block; font-family: Sofia; font-size: 22px; text-transform: uppercase; margin-top: 4px; }
.inel small { display: block; color: #8fb0d6; font-size: 13px; }
.ival { font-family: Sofia; font-weight: 800; font-size: 30px; fill: ${NOI}; }
.ival2 { font-family: Sofia; font-weight: 800; font-size: 20px; fill: ${EI}; }
.bare { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 50px; }
.bara { display: grid; grid-template-columns: 56px 1fr 56px; align-items: center; gap: 12px; padding: 8px 0; }
.bv { font-family: Sofia; font-weight: 800; font-size: 26px; color: #9fb6d3; }
.bv.top { color: #fff; }
.bv.r { text-align: right; }
.bt i { display: block; font-style: normal; text-align: center; font-size: 15px; color: #cfe0f5; margin-bottom: 6px; }
.bt { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }
.bt i { grid-column: 1 / 3; }
.bl, .br { height: 10px; background: rgba(255,255,255,.08); border-radius: 6px; overflow: hidden; display: flex; }
.bl { justify-content: flex-end; }
.bl em, .br em { display: block; height: 100%; border-radius: 6px; }
.precizii { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.prec { background: rgba(255,255,255,.06); border-radius: 16px; padding: 16px 18px; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 8px; }
.prec b { font-family: Sofia; font-size: 34px; display: block; line-height: 1; }
.prec small { color: #8fb0d6; font-size: 13px; }
.prec div:last-child { text-align: right; }
.prec span { font-size: 14px; color: #cfe0f5; text-align: center; max-width: 110px; }
.sch-list { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.sch-list div { background: rgba(255,255,255,.06); border-radius: 14px; padding: 12px 14px; }
.sch-list b { font-family: Sofia; font-size: 22px; text-transform: uppercase; display: block; }
.sch-list small { color: #8fb0d6; font-size: 13px; }
.sch-list em { font-style: normal; color: #6fe39b; font-weight: 800; }
.leg { display: flex; justify-content: center; gap: 30px; margin: 4px 0 0; font-size: 15px; color: #cfe0f5; }
.leg i { display: inline-block; width: 14px; height: 14px; border-radius: 4px; margin-right: 8px; vertical-align: -2px; }
.sub { display: flex; justify-content: space-between; color: #6f8fb8; font-size: 14px; margin-top: 30px; border-top: 1px solid rgba(255,255,255,.1); padding-top: 14px; }
.sub b { font-family: Sofia; font-size: 20px; color: #fff; letter-spacing: 1px; }
</style></head><body>
<div class="cap"><span class="rub">${esc(d.competitie)} · statisticile meciului</span><img class="logo" src="${uri('logo.png', 'image/png')}"></div>
<div class="scor">
	<div class="ech"><img src="${sigla(d.gazde.sofa_id)}">${esc(d.gazde.nume)}</div>
	<div class="rez">${d.scor[0]}-${d.scor[1]}</div>
	<div class="ech r">${esc(d.oaspeti.nume)}<img src="${sigla(d.oaspeti.sofa_id)}"></div>
</div>
<div class="marc"><div>${esc(d.marcatori_gazde || '')}</div><div>${esc(d.marcatori_oaspeti || '')}</div></div>
<div class="info">${esc(d.info)}</div>
<div class="leg"><span><i style="background:${NOI}"></i>${esc(d.noi)}</span><span><i style="background:${EI}"></i>${esc(d.ei)}</span></div>

<h2>Primul 11 <span>· ${esc(d.sistem)} · note ${esc(d.sursa_note)}</span></h2>
<div class="teren">
	<div class="l" style="left:50%;top:-3px;bottom:-3px;width:0"></div>
	<div class="l" style="left:calc(50% - 70px);top:calc(50% - 70px);width:140px;height:140px;border-radius:50%"></div>
	<div class="l" style="left:-3px;top:25%;width:150px;height:50%"></div>
	<div class="l" style="right:-3px;top:25%;width:150px;height:50%"></div>
	${zone}${jucatori}
</div>
<div class="legenda"><span>⚽ gol</span><span>👟 pasă decisivă</span><span><i class="ic gal" style="display:inline-block;vertical-align:-3px"></i> cartonaș galben</span><span>minutul schimbării</span>${d.zone_pase ? '<span>procentele: zona în care s-a jucat mingea</span>' : ''}</div>

<h2>Controlul jocului</h2>
<div class="inele">${d.inele.map((x) => inel(x[0], x[1], x[2], x[3])).join('')}</div>

<h2>Cifrele meciului</h2>
<div class="bare">${d.bare.map((x) => bara(x[0], x[1], x[2])).join('')}</div>

<h2>Precizie</h2>
<div class="precizii">${d.precizii.map((x) => precizie(x[0], x[1], x[2])).join('')}</div>

<h2>Schimbările Științei</h2>
<div class="sch-list">${d.schimbari.map((s) => `<div><b>${esc(s.intra)}</b><small><em>${esc(s.minut)}'</em> în locul lui ${esc(s.iese)}${s.nota ? ' · nota ' + s.nota.toFixed(1) : ''}</small></div>`).join('')}</div>

<div class="sub"><span>Sursa datelor: ${esc(d.sursa)}</span><b>POVESTILESTIINTEI.RO</b></div>
</body></html>`;

(async () => {
	const browser = await chromium.launch();
	const page = await browser.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
	await page.setContent(html, { waitUntil: 'load' });
	await page.evaluate(() => document.fonts.ready);
	await page.screenshot({ path: outFile, fullPage: true });
	await browser.close();
	console.log('Statistici: ' + outFile);
})();
