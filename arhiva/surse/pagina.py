import json,html
D=json.load(open('out/legende.json',encoding='utf-8'))
e=lambda s: html.escape(s or '',quote=True)
nf=sum(len(x['legende']) for x in D); nj=len({j['nume'] for x in D for j in x['jucatori']}|{n for x in D for l in x['loturi'] for n in l['nume']})
def init(n):
    p=[w for w in n.replace('și','').split() if w[0].isupper()]
    return (p[0][0]+p[-1][0]) if len(p)>1 else n[:2]
o=[]
o.append(f'''<div class="ps-leg">
<header class="ps-leg-hero">
<span class="ps-leg-ani">1948 – 2026</span>
<h1>Legendele Științei</h1>
<p class="ps-leg-sub">Arhiva istorică a Universității Craiova</p>
<p class="ps-leg-intro">Nu un clasament al celor mai cunoscuți fotbaliști, ci povestea completă a clubului, epocă după epocă: pionierii din 1948, campionii din 1974, Craiova Maxima, generația eventului, anii ’90, deceniul greu de după 2000 și echipa modernă. Pentru fiecare perioadă găsești contextul, momentele care au contat, loturile istorice, fișele jucătorilor-cheie și lista tuturor celor care au purtat tricoul alb-albastru.</p>
<div class="ps-leg-stat"><div><b>8</b><span>epoci</span></div><div><b>{nf}</b><span>fișe de legendă</span></div><div><b>{nj}</b><span>nume în arhivă</span></div></div>
</header>
<nav class="ps-leg-nav" id="ps-leg-nav" aria-label="Epoci">''')
for x in D: o.append(f'<a href="#epoca-{x["nr"]}"><b>{x["nr"]}</b><span>{e(x["titlu"])}</span><small>{e(x["ani"])}</small></a>')
o.append('</nav>')
for x in D:
    n=x['nr']
    o.append(f'<section class="ps-leg-epoca" id="epoca-{n}">')
    o.append(f'<div class="ps-leg-head"><span class="ps-leg-nr">Epoca {n}</span><h2>{e(x["titlu"])}</h2><span class="ps-leg-perioada">{e(x["ani"])}</span><p>{e(x["subtitlu"])}</p></div>')
    o.append('<div class="ps-leg-cols"><div class="ps-leg-text">'+''.join(f'<p>{e(p)}</p>' for p in x['intro'])+'</div>')
    if x['momente']:
        o.append('<aside class="ps-leg-momente"><h3>Momente</h3><ul>'+''.join(f'<li>{e(m)}</li>' for m in x['momente'])+'</ul></aside>')
    o.append('</div>')
    if x['loturi']:
        o.append('<h3 class="ps-leg-h3">Loturi istorice</h3><div class="ps-leg-loturi">')
        for l in x['loturi']:
            a=f'<small>Antrenor: {e(l["antrenor"])}</small>' if l.get('antrenor') else ''
            o.append(f'<div class="ps-leg-lot"><h4>{e(l["titlu"])}</h4><p>{" · ".join(e(k) for k in l["nume"])}</p>{a}</div>')
        o.append('</div>')
    o.append('<h3 class="ps-leg-h3">Fișele epocii</h3><div class="ps-leg-carduri">')
    for l in x['legende']:
        cls=' ps-leg-antrenor' if l['rol']=='antrenor' else ''
        por=f'<em>„{e(l["porecla"])}”</em>' if l['porecla'] else ''
        cif=f'<footer>{e(l["cifre"])}</footer>' if l['cifre'] else ''
        o.append(f'<article class="ps-leg-card{cls}"><div class="ps-leg-card-top"><span class="ps-leg-ini">{e(init(l["nume"]))}</span><div><h4>{e(l["nume"])}</h4><span class="ps-leg-meta">{e(l["post"])} · {e(l["ani"])}</span>{por}</div></div><p>{e(l["text"])}</p>{cif}</article>')
    o.append('</div>')
    if len(x['jucatori'])>3:
        o.append(f'<details class="ps-leg-toti"><summary>Toți jucătorii epocii din arhivă ({len(x["jucatori"])})</summary><ul>')
        for j in x['jucatori']:
            meta=' · '.join(t for t in (j['post'],j['ani']) if t)
            o.append(f'<li><b>{e(j["nume"])}</b><span>{e(meta)}</span></li>')
        o.append('</ul><p class="ps-leg-nota">Lista include jucătorii pentru care perioada petrecută la Craiova apare în fișele publice. Arhiva se completează pe măsură ce verificăm alte nume.</p></details>')
    o.append('<p class="ps-leg-surse">Surse: '+'; '.join(e(s) for s in x['surse'])+'.</p><a class="ps-leg-sus" href="#ps-leg-nav">↑ Înapoi la epoci</a></section>')
o.append('<footer class="ps-leg-metoda"><h3>Cum am construit arhiva</h3><p>Textele sunt scrise de redacție pe baza istoricului oficial al clubului, a paginilor de legende ale clubului și a edițiilor română și engleză ale Wikipedia. Am trecut cifre (meciuri, goluri, selecții) doar acolo unde cel puțin două surse se potrivesc; unde sursele diferă, am preferat să nu dăm un număr. Perioadele petrecute la Craiova provin din fișele publice ale jucătorilor. Dacă ai fotografii, documente sau corecturi pentru arhivă, scrie-ne.</p></footer></div>')
open('out/legende.html','w',encoding='utf-8').write('\n'.join(o))
print(nf,nj,len(''.join(o)))
