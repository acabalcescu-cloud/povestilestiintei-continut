import json,re,unicodedata,html
exec(open('legende_text.py',encoding='utf-8').read())
E=json.load(open('/home/user/povestilestiintei-continut/arhiva/epoci.json',encoding='utf-8'))
F=json.load(open('fise.json',encoding='utf-8'))
EXCL={'Cătălin Crăciun','Ionuț Stancu','Vukašin Tomić','Nicolae Zamfir'}
def fara(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').lower()
def ani(per):
    per=sorted(per); m=[]
    for a,b in per:
        if m and a<=m[-1][1]+1: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    return ', '.join(f'{a}' if a==b else f'{a}–{"prezent" if b>=2026 else b}' for a,b in m)
# jucători cunoscuți doar din pagina clubului / loturi (fără infobox complet)
EXTRA={'Aurică Beldeanu':(3,'Mijlocaș',[[1976,1985]]),'Costică Donose':(3,'Mijlocaș',[[1977,1983]]),'Gabriel Boldici':(3,'Portar',[[1977,1985],[1988,1993]]),
 'Nicolae Tilihoi':(3,'Fundaș',[[1976,1987]]),'Zoltan Crișan':(3,'Atacant',[[1974,1984]]),'Petre Deselnicu':(2,'Fundaș',[[1964,1976]]),
 'Theodor Țarălungă':(2,'Extremă',[[1970,1974]]),'Emil Săndoi':(4,'Fundaș',[[1983,1999]]),'Ovidiu Stângă':(6,'Mijlocaș',[[1990,1995],[2002,2004],[2005,2007]]),
 'Silvian Cristescu':(5,'Mijlocaș',[[1990,1998],[1999,2000]]),'Ion Niță':(2,'Atacant',[[1973,1974]]),'Dragu Bădin':(2,'Fundaș',[[1973,1974]]),'Dănuț Bică':(4,'Mijlocaș',[[1989,1991]])}
EP={1:(1948,1964),2:(1964,1974),3:(1975,1985),4:(1985,1990),5:(1990,1991),6:(1992,2000),7:(2000,2011),8:(2014,2026)}
toti={e:{} for e in EP}
for n,f in F.items():
    if n in EXCL: continue
    for e in f['epoci']: toti[e][n]={'nume':n,'post':f['post'],'ani':ani(f['perioade']),'m':f.get('meciuri')}
for n,(e0,post,per) in EXTRA.items():
    for e,(a,b) in EP.items():
        if any(p[0]<=b and p[1]>=a for p in per): toti[e].setdefault(n,{'nume':n,'post':post,'ani':ani(per),'m':None})
def nume_fam(n): return fara(n.split()[-1] if not n.endswith('Jr.') else n.split()[-2])
out=[]
for x in E:
    e=x['nr']
    leg=[l for l in L if l['epoca']==e]
    lst=sorted(toti[e].values(),key=lambda j:(nume_fam(j['nume']),fara(j['nume'])))
    out.append({**x,'legende':leg,'jucatori':lst})
json.dump(out,open('out/legende.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print({x['nr']:(len(x['legende']),len(x['jucatori'])) for x in out})
