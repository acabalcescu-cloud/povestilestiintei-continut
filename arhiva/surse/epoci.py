import json,re
d=json.load(open('date.json'))
EPOCI=[(1,'Pionierii Științei',1948,1964),(2,'Generația primului titlu',1964,1974),(3,'Craiova Maxima',1975,1985),(4,'Generația de tranziție',1985,1990),(5,'Generația eventului',1990,1991),(6,'Generația anilor ’90',1992,2000),(7,'Generația 2000–2010',2000,2011),(8,'Generația modernă',2014,2026)]
def merge(v):
    # preferă ro, completează cu en; marchează confirmarea dublă
    ro=v.get('ro',{}).get('craiova',[]); en=v.get('en',{}).get('craiova',[])
    sp=[]
    for s in (ro or en):
        if not s['ani']: continue
        alt=[e for e in (en if ro else ro) if e['ani'] and abs(e['ani'][0]-s['ani'][0])<=1]
        s=dict(s); s['confirmat']=bool(alt); s['alt']=alt[0] if alt else None; sp.append(s)
    return sp
rez={}
for nume,v in d.items():
    sp=merge(v)
    if not sp: continue
    meciuri=sum(s['meciuri'] or 0 for s in sp)
    best=None;bo=-1
    for nr,_,a,b in EPOCI:
        o=sum(max(0,min(b,s['ani'][1])-max(a,s['ani'][0])+(1 if s['ani'][1]>=a and s['ani'][0]<=b else 0)) for s in sp)
        if o>bo: bo,best=o,nr
    if bo<=0: continue
    info=v.get('ro') or v.get('en')
    rez[nume]={'epoca':best,'spells':sp,'meciuri':meciuri,'goluri':sum(s['goluri'] or 0 for s in sp),'pozitie':(v.get('ro',{}).get('pozitie') or v.get('en',{}).get('pozitie')),'nascut':info.get('nascut'),'nat':max([x.get('nat_meciuri') or 0 for x in v.values()]),'porecla':(v.get('ro',{}).get('porecla') or '')}
json.dump(rez,open('candidati.json','w'),ensure_ascii=False,indent=1)
for nr,t,a,b in EPOCI:
    L=sorted([(x['meciuri'],n) for n,x in rez.items() if x['epoca']==nr],reverse=True)
    print(f'\n## {nr}. {t} ({a}-{b}): {len(L)}'); print(', '.join(f'{n} ({m})' for m,n in L))
