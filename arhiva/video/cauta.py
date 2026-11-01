import json,re,subprocess,sys,urllib.parse,time
def cauta(q):
    u='https://www.youtube.com/results?hl=ro&gl=RO&search_query='+urllib.parse.quote(q)
    h=subprocess.run(['curl','-s','-m','30','-H','Accept-Language: ro-RO,ro;q=0.9',u],capture_output=True,text=True).stdout
    m=re.search(r'var ytInitialData = (\{.*?\});</script>',h)
    if not m: return []
    d=json.loads(m.group(1)); out=[]
    def walk(x):
        if isinstance(x,dict):
            if 'videoRenderer' in x:
                v=x['videoRenderer']
                t=''.join(r.get('text','') for r in v.get('title',{}).get('runs',[]))
                ch=''.join(r.get('text','') for r in v.get('ownerText',{}).get('runs',[]))
                out.append({'id':v['videoId'],'titlu':t,'canal':ch,'durata':v.get('lengthText',{}).get('simpleText',''),'vizualizari':v.get('viewCountText',{}).get('simpleText',''),'publicat':v.get('publishedTimeText',{}).get('simpleText','')})
            for y in x.values(): walk(y)
        elif isinstance(x,list):
            for y in x: walk(y)
    walk(d); return out
Q=sys.argv[1:]
R={}
for q in Q:
    R[q]=cauta(q)[:12]; time.sleep(2)
json.dump(R,open('rez-%d.json'%int(time.time()),'w'),ensure_ascii=False,indent=1)
for q,L in R.items():
    print('\n##',q)
    for v in L: print(f"  {v['id']} | {v['durata']:>8} | {v['vizualizari'][:22]:22} | {v['canal'][:28]:28} | {v['titlu'][:95]}")
