import sys,json,time,os; sys.path.insert(0,'/tmp/claude-0/arhiva')
from wapi import wikitext
c=json.load(open('categorii.json'))
f='pagini.json'
res=json.load(open(f)) if os.path.exists(f) else {'ro':{},'en':{}}
jobs=[('ro.wikipedia.org','ro',c['ro']),('en.wikipedia.org','en',sorted(set(c['en1948']+c['encs'])-{'List of FC U Craiova 1948 players'}))]
for host,key,lst in jobs:
    lst=[t for t in lst if t not in res[key]]
    for i in range(0,len(lst),20):
        for incercare in range(6):
            try:
                w,red=wikitext(host,lst[i:i+20]); break
            except Exception as e:
                time.sleep(30*(incercare+1))
        else: continue
        res[key].update(w)
        for r in red: res[key].setdefault(r['from'],w.get(r['to'],''))
        json.dump(res,open(f,'w'),ensure_ascii=False)
        time.sleep(4)
    print(key,len(res[key]),flush=True)
