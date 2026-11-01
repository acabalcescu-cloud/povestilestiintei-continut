import json,re
CRA=re.compile(r'Universitatea Craiova|U Craiova|FCU Craiova|CSU Craiova|Știința Craiova|Stiinta Craiova|ClubFotbal\|Craiova\b|Universitatea\]\]',re.I)
NOT=re.compile(r'Electroputere|Extensiv|FC Craiova|Craiova 1948 II|Universitatea II|Universitatea Craiova II|U Craiova II|Gloria|Sporting|Viitorul|Pandurii|Atletic|tineret|U-19|U19|U-21|U21|youth|\bB\b',re.I)
def curat(s):
    s=re.sub(r'<ref[^>]*/>|<ref[^>]*>.*?</ref>','',s,flags=re.S)
    s=re.sub(r'\{\{(?:nowrap|small)\|([^{}]*)\}\}',r'\1',s)
    return s
def campuri(t):
    i=-1
    for k in ('{{Infobox','{{infobox','{{Infocaseta Fotbalist','{{Infocaseta fotbalist','{{Cutie fotbalist'):
        i=t.find(k)
        if i>=0: break
    if i<0: return {}
    # până la închiderea infobox-ului
    d=0;j=i
    while j<len(t):
        if t.startswith('{{',j): d+=1;j+=2;continue
        if t.startswith('}}',j):
            d-=1;j+=2
            if d==0: break
            continue
        j+=1
    box=curat(t[i:j]); f={}
    for m in re.finditer(r'\n\s*\|\s*([\w ()ăâîșțĂÂÎȘȚ]+?)\s*=\s*(.*?)(?=\n\s*\||\n\}\}|\Z)',box,re.S): f[m.group(1).strip()]=m.group(2).strip()
    if 'echipe' in f and 'ani' in f:   # format ro vechi: liste separate prin <br>
        sp=lambda v: [x.strip() for x in re.split(r'<br\s*/?>',v)]
        A=sp(f['ani']); E=sp(f['echipe']); G=sp(f.get('apariții(goluri)',''))
        for n,(a,e) in enumerate(zip(A,E),1):
            f['years%d'%n]=a; f['clubs%d'%n]=e
            g=re.sub(r'\{\{0\}\}','',G[n-1]) if n-1<len(G) else ''
            m=re.match(r"\s*'*\s*(\d+)\s*\((\d+)\)",g)
            if m: f['caps%d'%n]=m.group(1); f['goals%d'%n]=m.group(2)
        f.setdefault('position',f.get('post',''))
        f.setdefault('birth_date',f.get('datanașterii',''))
        g=re.sub(r'\{\{0\}\}','',f.get('aparițiilanațională(goluri)',''))
        m=re.match(r"\s*(\d+)",g)
        if m: f['nationalcaps1']=m.group(1)
        f.setdefault('nationalteam1',f.get('echipănațională',''))
    return f
def num(s):
    m=re.search(r'\d+',re.sub(r'\(.*?\)','',s or '')); return int(m.group()) if m else None
def ani(s):
    y=[int(x) for x in re.findall(r'(?:19|20)\d\d',s or '')]
    if not y: return None
    a=y[0]; b=y[-1] if len(y)>1 else (2026 if re.search(r'[–-]\s*$|prezent|present',s) else a)
    return [a,b]
def spells(f):
    out=[]
    for k,v in f.items():
        m=re.fullmatch(r'clubs(\d+)',k)
        if not m: continue
        n=m.group(1)
        if CRA.search(v) and not NOT.search(v):
            a=ani(f.get('years'+n,''))
            if a and a[0]>=2012 and re.search(r'1948|FCU|FC U Craiova|FC Universitatea',v): continue
            out.append({'club':re.sub(r'\s+',' ',v)[:80],'ani':a,'ani_txt':re.sub(r'\s+',' ',f.get('years'+n,'')),'meciuri':num(f.get('caps'+n)),'goluri':num(f.get('goals'+n)),'imprumut':'→' in v or 'loan' in v.lower() or 'împrumut' in v.lower()})
    return out
def info(t):
    f=campuri(t)
    pos=re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]',r'\1',f.get('position',f.get('poziție',''))); pos=re.sub(r'<.*?>|\{\{.*?\}\}','',pos).strip()
    bd=re.findall(r'(?:19|20)\d\d',f.get('birth_date',f.get('data_nașterii','')))
    nat=num(f.get('nationalcaps1')); natt=f.get('nationalteam1','')
    return {'pozitie':pos[:60],'nascut':int(bd[0]) if bd else None,'craiova':spells(f),'nat_meciuri':nat,'nat_echipa':re.sub(r'\{\{|\}\}|\[\[|\]\]','',natt)[:60],'porecla':re.sub(r"''|<.*?>",'',f.get('poreclă',f.get('nickname','')))[:80]}
if __name__=='__main__':
    P=json.load(open('pagini.json'))
    out={}
    for lim in ['ro','en']:
        for t,w in P[lim].items():
            out.setdefault(t,{})[lim]=info(w)
    json.dump(out,open('date.json','w'),ensure_ascii=False,indent=0)
    ok=[(t,d['ro']['craiova']) for t,d in out.items() if 'ro' in d]
    print(len(out), sum(1 for _,c in ok if c))
    for t,c in ok[:25]: print(t,c)
