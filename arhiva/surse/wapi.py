import json,urllib.parse,subprocess,time
UA='PovestileStiinteiArhiva/1.0 (https://povestilestiintei.ro)'
def api(host,params):
    q=urllib.parse.urlencode({**params,'format':'json'})
    for i in range(5):
        r=subprocess.run(['curl','-s','--max-time','90','-A',UA,f'https://{host}/w/api.php?{q}'],capture_output=True,text=True).stdout
        try: return json.loads(r)
        except Exception: time.sleep(3+i*3)
    raise RuntimeError(r[:200])
def cat(host,title):
    out=[];cont={}
    while True:
        d=api(host,{'action':'query','list':'categorymembers','cmtitle':title,'cmlimit':'500','cmtype':'page',**cont})
        out+=[m['title'] for m in d['query']['categorymembers']]
        if 'continue' in d: cont=d['continue']
        else: return out
def wikitext(host,titles):
    """titles: list (<=50) -> {title: wikitext}"""
    d=api(host,{'action':'query','prop':'revisions','rvprop':'content','rvslots':'main','titles':'|'.join(titles),'redirects':1})
    out={}
    for p in d['query']['pages'].values():
        if 'revisions' in p: out[p['title']]=p['revisions'][0]['slots']['main']['*']
    return out,d['query'].get('redirects',[])
