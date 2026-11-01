import sys,json,time,re,os; sys.path.insert(0,'/tmp/claude-0/arhiva')
from wapi import api,wikitext,cat
P=json.load(open('pagini.json'))
time.sleep(20)
csu=cat('ro.wikipedia.org','Categorie:Fotbaliști ai CSU Craiova')
c=json.load(open('categorii.json')); c['ro_csu']=csu; json.dump(c,open('categorii.json','w'),ensure_ascii=False,indent=0)
print('csu',len(csu),flush=True)
a=json.load(open('articole.json'))['ro']['CS Universitatea Craiova (1948)'][57888:61818]
imp=[m.split('|')[0] for m in re.findall(r'\[\[([^\]]+)\]\]',a)]
lst=[t for t in dict.fromkeys(csu+imp) if t not in P['ro'] and t not in ('Romania','Albania')]
print('de descarcat',len(lst),flush=True)
for i in range(0,len(lst),15):
    for k in range(6):
        try: w,red=wikitext('ro.wikipedia.org',lst[i:i+15]); break
        except Exception: time.sleep(40*(k+1))
    else: continue
    P['ro'].update(w)
    for r in red: P['ro'].setdefault(r['from'],w.get(r['to'],''))
    json.dump(P,open('pagini.json','w'),ensure_ascii=False)
    time.sleep(6)
print('gata',len(P['ro']),flush=True)
