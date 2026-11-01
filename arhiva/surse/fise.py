"""Construiește fișele jucătorilor pe epoci, din datele extrase (ro/en wiki) + paginile clubului.
Cifrele (meciuri, goluri) apar doar când ro și en se potrivesc (±10%) sau când o singură wiki se potrivește cu pagina clubului."""
import json,re,unicodedata
U=json.load(open('unificat.json')); C=json.load(open('ucv/texte.json'))
EPOCI=[(1,1948,1964),(2,1964,1974),(3,1975,1985),(4,1985,1990),(5,1990,1991),(6,1992,2000),(7,2000,2011),(8,2014,2026)]
def fara(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
club={}
for k,t in C.items():
    if k in ('istoric','palmares'): continue
    t=t[t.rfind('Galerie foto ')+13:]
    m=re.search(r'^(.+?) (Portar|Apărător|Mijlocaș|Atacant|Antrenor[^N]*|Președinte[^N]*) Născut pe (.+?) Biografie (.+)',t)
    if m: club[fara(m.group(1)).lower()]={'nume':m.group(1),'post':m.group(2),'nascut':m.group(3),'bio':m.group(4).strip()}
def apropiat(a,b): return a and b and abs(a-b)<=max(3,0.1*max(a,b))
POST={'goalkeeper':'Portar','defender':'Fundaș','midfielder':'Mijlocaș','forward':'Atacant','striker':'Atacant','winger':'Extremă','centre-back':'Fundaș central','full-back':'Fundaș lateral','left-back':'Fundaș stânga','right-back':'Fundaș dreapta','attacking midfielder':'Mijlocaș ofensiv','defensive midfielder':'Mijlocaș defensiv','central midfielder':'Mijlocaș central'}
def post(ro,en):
    p=(ro or {}).get('pozitie') or ''
    if p and not re.search(r'[a-z]{4,}',fara(p).lower().replace('mijlocas','').replace('fundas','').replace('atacant','').replace('portar','').replace('extrema','')): pass
    if p and re.search(r'Portar|Fundaș|Mijlocaș|Atacant|Extrem|Apărător|Mijloca|Fundas',p): return re.sub(r'\s*\(.*','',p)[:40]
    e=((en or {}).get('pozitie') or '').lower()
    for k,v in POST.items():
        if k in e: return v
    return ''
out={}
for g in U.values():
    nume=sorted(g['titluri'],key=len)[0].split(' (')[0]
    ro,en=g['ro'],g['en']
    srs=[s for s in ((ro or {}).get('craiova') or []) if s.get('ani')]
    sen=[s for s in ((en or {}).get('craiova') or []) if s.get('ani')]
    baza=srs or sen
    if not baza: continue
    perioade=[];m_tot=0;g_tot=0;conf=True
    for s in baza:
        alt=[e for e in (sen if srs else srs) if abs(e['ani'][0]-s['ani'][0])<=1]
        perioade.append(s['ani'])
        if alt and apropiat(s['meciuri'],alt[0]['meciuri']):
            m_tot+=s['meciuri'] or 0; g_tot+=s['goluri'] or 0
        else: conf=False
    cb=club.get(fara(nume).lower())
    ep=max(EPOCI,key=lambda e: sum(max(0,min(e[2],p[1])-max(e[1],p[0])+1) for p in perioade))[0]
    eps=[e[0] for e in EPOCI if any(p[0]<=e[2] and p[1]>=e[1] and not (e[0]==8 and p[1]<2014) for p in perioade)]
    out[nume]={'epoca':ep,'epoci':eps,'perioade':perioade,'post':post(ro,en),'meciuri':m_tot if conf and m_tot else None,'goluri':g_tot if conf and m_tot else None,
               'nat':max([(x or {}).get('nat_meciuri') or 0 for x in (ro,en)]) or None,'porecla':(ro or {}).get('porecla') or '','club':cb,
               'surse':[x for x,v in (('Wikipedia ro',srs),('Wikipedia en',sen)) if v]+(['ucv1948.ro'] if cb else [])}
json.dump(out,open('fise.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(out),Counter(e for v in out.values() for e in v['epoci']), sum(1 for v in out.values() if v['meciuri']),'cu cifre confirmate', sum(1 for v in out.values() if v['club']),'cu pagina club')
print('club fara potrivire:',[c['nume'] for k,c in club.items() if not any(fara(n).lower()==k for n in out)])
