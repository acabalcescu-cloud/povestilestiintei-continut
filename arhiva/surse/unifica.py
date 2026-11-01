import json,re,unicodedata
d=json.load(open('date.json'))
def cheie(t):
    t=re.sub(r'\s*\(.*?\)','',t)
    t=''.join(c for c in unicodedata.normalize('NFD',t.lower()) if unicodedata.category(c)!='Mn')
    t=t.replace('ion ionut','ionut').replace('stinga','stanga')
    return re.sub(r'[^a-z ]','',t).strip()
grup={}
for t,v in d.items():
    k=cheie(t); g=grup.setdefault(k,{'titluri':[],'ro':None,'en':None})
    g['titluri'].append(t)
    for l in ('ro','en'):
        if l in v:
            if g[l] is None or (not g[l]['craiova'] and v[l]['craiova']): g[l]=v[l]
json.dump(grup,open('unificat.json','w'),ensure_ascii=False,indent=0)
print(len(d),'->',len(grup))
