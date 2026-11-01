import json,re,sys,unicodedata
P=json.load(open('pagini.json')); F=json.load(open('fise.json'))
exec(open('fise.py').read().split('def apropiat')[0].split('club={}')[0])
C=json.load(open('ucv/texte.json')); club={}
for k,t in C.items():
    if k in ('istoric','palmares'): continue
    t=t[t.rfind('Galerie foto ')+13:]
    m=re.search(r'^(.+?) (Portar|Apărător|Mijlocaș|Atacant|Antrenor[^N]*|Președinte[^N]*) Născut pe (.+?) Biografie (.+)',t)
    if m: club[fara(m.group(1)).lower()]=m.group(4)
def lead(w,n=700):
    w=re.sub(r'<ref[^>]*/>|<ref[^>]*>.*?</ref>','',w,flags=re.S)
    for _ in range(5): w=re.sub(r'\{\{[^{}]*\}\}','',w)
    w=re.sub(r'\[\[(?:Fișier|File|Imagine|Categorie|Category)[^\]]*\]\]','',w)
    w=re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]',r'\1',w); w=re.sub(r"'''?|<[^>]+>",'',w)
    return re.sub(r'\s+',' ',w.split('\n==')[0]).strip()[:n]
def gas(lim,n):
    for t in P[lim]:
        if fara(t.split(' (')[0]).lower()==fara(n).lower() and len(P[lim][t])>300: return P[lim][t]
for n in sys.argv[1:]:
    f=F.get(n,{}); print('##',n,'|',f.get('post'),f.get('perioade'),'m',f.get('meciuri'),'g',f.get('goluri'),'nat',f.get('nat'),'|',f.get('porecla'))
    c=club.get(fara(n).lower())
    if c: print(' CLUB:',c[:900])
    for l in ('ro','en'):
        w=gas(l,n)
        if w: print(' '+l.upper()+':',lead(w))
