import json,html,subprocess
exec(open('date_video.py',encoding='utf-8').read())
E=json.load(open('/home/user/povestilestiintei-continut/arhiva/epoci.json',encoding='utf-8'))
ver={x['id']:x for x in json.load(open('verificat.json'))}
ver['YRcvIDgIF8E']={'canal':'Orange Sport Romania'}
e=lambda s: html.escape(s or '',quote=True)
def card(v):
    ep,i,t,d,desc=v; c=ver[i]['canal']
    return (f'<article class="ps-vid-card"><button type="button" class="ps-vid-play" data-id="{i}" aria-label="Pornește: {e(t)}">'
            f'<img src="https://i.ytimg.com/vi/{i}/hqdefault.jpg" alt="" loading="lazy"><span class="ps-vid-btn" aria-hidden="true"></span></button>'
            f'<div class="ps-vid-text"><span class="ps-vid-data">{e(d)}</span><h4>{e(t)}</h4><p>{e(desc)}</p>'
            f'<a class="ps-vid-sursa" href="https://www.youtube.com/watch?v={i}" target="_blank" rel="noopener">YouTube · {e(c)}</a></div></article>')
o=['<div class="ps-leg ps-vid">','''<header class="ps-leg-hero"><span class="ps-leg-ani">1948 – 2026</span><h1>Arhiva video</h1><p class="ps-leg-sub">Istoria Științei, în imagini</p>
<p class="ps-leg-intro">Golurile, serile europene, finalele și oamenii care au făcut istoria Universității Craiova, așa cum au rămas în înregistrările publicate pe YouTube. De la interviul cu Ion Oblemenco din sezonul primului titlu la Leeds, Bayern, Kaiserslautern și Benfica, de la eventul din 1991 la tripla internă din 2026.</p>''']
o.append(f'<div class="ps-leg-stat"><div><b>{len(V)}</b><span>înregistrări</span></div><div><b>8</b><span>epoci</span></div></div></header>')
o.append('<nav class="ps-leg-nav" id="ps-leg-nav" aria-label="Epoci"><a href="#video-documentare"><b>★</b><span>Documentare</span><small>povești și portrete</small></a>')
for x in E[1:]: o.append(f'<a href="#video-{x["nr"]}"><b>{x["nr"]}</b><span>{e(x["titlu"])}</span><small>{e(x["ani"])}</small></a>')
o.append('</nav>')
def sectiune(ide,eticheta,titlu,ani,sub,lst,nota=''):
    o.append(f'<section class="ps-leg-epoca" id="{ide}"><div class="ps-leg-head"><span class="ps-leg-nr">{e(eticheta)}</span><h2>{e(titlu)}</h2>'+(f'<span class="ps-leg-perioada">{e(ani)}</span>' if ani else '')+f'<p>{e(sub)}</p></div>')
    if nota: o.append(f'<p class="ps-vid-nota">{e(nota)}</p>')
    o.append('<div class="ps-vid-grid">'+''.join(card(v) for v in lst)+'</div><a class="ps-leg-sus" href="#ps-leg-nav">↑ Înapoi la epoci</a></section>')
sectiune('video-documentare','Documentare','Povești și portrete','', 'Filme și reportaje despre marile generații ale Științei.',[v for v in V if v[0]=='D'])
for x in E:
    lst=[v for v in V if v[0]==str(x['nr'])]
    nota='' if lst else 'Din primii ani ai clubului nu au rămas înregistrări video publice. Povestea pionierilor o găsești în arhiva „Legendele Științei”.'
    sectiune(f'video-{x["nr"]}',f'Epoca {x["nr"]}',x['titlu'],x['ani'],x['subtitlu'],lst,nota)
o.append('<p class="ps-vid-legal">Înregistrările aparțin canalelor care le-au publicat pe YouTube și sunt redate prin playerul YouTube. Fiecare card are legătura spre videoclipul original.</p></div>')
o.append('''<script>document.querySelectorAll('.ps-vid-play').forEach(function(b){b.addEventListener('click',function(){var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1&rel=0';f.title=b.getAttribute('aria-label');f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;f.className='ps-vid-frame';b.replaceWith(f);});});</script>''')
open('arhiva-video.html','w',encoding='utf-8').write('\n'.join(o)); print(len('\n'.join(o)))
json.dump([dict(epoca=v[0],id=v[1],titlu=v[2],data=v[3],descriere=v[4],canal=ver[v[1]]['canal']) for v in V],open('/home/user/povestilestiintei-continut/arhiva/video/video.json','w'),ensure_ascii=False,indent=1)
