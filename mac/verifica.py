#!/usr/bin/env python3
"""Verificarea orară a știrilor, pe Mac, fără inteligență artificială.

1. Aduce ultimele modificări din depozit (git pull).
2. Citește Google News și fluxurile RSS ale publicațiilor sportive.
3. Păstrează doar titlurile despre Știința apărute în ultimele ore,
   pe care nu le-am mai văzut (nici local, nici în presa/vazute.json).
4. Numai dacă rămâne ceva nou, pornește Claude Code (claude -p) cu mac/prompt.md.

Rulare manuală:  python3 mac/verifica.py            (verificare + Claude dacă e cazul)
                 python3 mac/verifica.py --doar-lista (arată candidații, fără Claude)
"""
import datetime as dt
import email.utils
import fcntl
import html
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET

DEPOZIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STARE = os.path.join(DEPOZIT, '.stare-mac')
VAZUTE_LOCAL = os.path.join(STARE, 'vazute-local.json')
CANDIDATI = os.path.join(STARE, 'candidati.json')
JURNAL = os.path.join(STARE, 'jurnal.log')
ORE = 4  # cât de vechi poate fi un articol ca să fie luat în calcul
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'

CAUTARI_GN = ['Universitatea Craiova', 'Coelho Craiova', 'Stiinta Craiova']
FLUXURI = [
    'https://www.gsp.ro/rss.xml', 'https://www.sport.ro/rss', 'https://www.prosport.ro/feed',
    'https://www.fanatik.ro/feed', 'https://www.digisport.ro/rss', 'https://www.digi24.ro/rss/stiri/sport',
    'https://www.gandul.ro/sport/feed',
]
# Cuvinte care leagă un titlu de Știința (fără diacritice, litere mici).
CHEI = ['craiova', 'coelho', 'oblemenco', 'rotaru', 'bancu', 'baiaram', 'hamlawi', 'elisor', 'nsimba',
        'cicaldau', 'screciu', 'romanchuk', 'stevanovic', 'lameira', 'felgueiras', 'baluta', 'mekvabishvili']


def jurnal(msg):
    os.makedirs(STARE, exist_ok=True)
    rand = f"{dt.datetime.now():%Y-%m-%d %H:%M} {msg}"
    print(rand)
    with open(JURNAL, 'a', encoding='utf-8') as f:
        f.write(rand + '\n')


def fara_diacritice(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


def curl(url):
    r = subprocess.run(['curl', '-s', '-L', '--max-time', '30', '-A', UA, url], capture_output=True, text=True, errors='ignore')
    return r.stdout


def citeste_flux(url):
    try:
        root = ET.fromstring(curl(url).encode('utf-8', 'ignore'))
    except ET.ParseError:
        return []
    out = []
    for it in root.iter('item'):
        titlu = html.unescape((it.findtext('title') or '').strip())
        link = (it.findtext('link') or '').strip()
        data = it.findtext('pubDate') or ''
        try:
            cand = email.utils.parsedate_to_datetime(data)
            if cand.tzinfo is None:
                cand = cand.replace(tzinfo=dt.timezone.utc)
        except (TypeError, ValueError):
            cand = None
        sursa = it.findtext('source') or urllib.parse.urlparse(url).netloc
        out.append({'titlu': titlu, 'link': link, 'data': cand, 'sursa': sursa})
    return out


def incarca(cale, implicit):
    try:
        with open(cale, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return implicit


def salveaza(cale, obiect):
    os.makedirs(os.path.dirname(cale), exist_ok=True)
    with open(cale, 'w', encoding='utf-8') as f:
        json.dump(obiect, f, ensure_ascii=False, indent=1)


def decodeaza(link):
    sys.path.insert(0, os.path.join(DEPOZIT, 'unelte'))
    from gndecode import decode
    try:
        return decode(link)
    except Exception:
        return None


def candidati():
    limita = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=ORE)
    vazute_local = set(incarca(VAZUTE_LOCAL, []))
    vazute_depozit = incarca(os.path.join(DEPOZIT, 'presa', 'vazute.json'), {})
    articole = []
    for q in CAUTARI_GN:
        articole += citeste_flux('https://news.google.com/rss/search?q=' + urllib.parse.quote(q + ' when:1d') + '&hl=ro&gl=RO&ceid=RO:ro')
    for f in FLUXURI:
        articole += citeste_flux(f)
    articole = [a for a in articole if any(k in fara_diacritice(a['titlu']) for k in CHEI)]
    noi, vazute_titluri, vazute_url = [], set(), set()
    for a in articole:
        if not a['link'] or a['link'] in vazute_local or (a['data'] and a['data'] < limita):
            continue
        cheie_titlu = fara_diacritice(re.sub(r'\s+-\s+[^-]+$', '', a['titlu']))[:70]
        if cheie_titlu in vazute_titluri:
            continue
        vazute_titluri.add(cheie_titlu)
        url = decodeaza(a['link']) if 'news.google.com' in a['link'] else a['link']
        if url:
            url = url.replace('\\u003d', '=').replace('\\u0026', '&')
        if url in vazute_url:
            continue
        vazute_url.add(url)
        if url and url in vazute_depozit:
            vazute_local.add(a['link'])
            continue
        noi.append({'titlu': a['titlu'], 'sursa': a['sursa'], 'url': url or a['link'], 'link_original': a['link'],
                    'data': a['data'].isoformat() if a['data'] else ''})
    salveaza(VAZUTE_LOCAL, sorted(vazute_local)[-5000:])
    return noi


def notifica(text):
    text = text.replace('"', "'")[:200]
    subprocess.run(['osascript', '-e', f'display notification "{text}" with title "Poveștile Științei"'], capture_output=True)


def main():
    os.makedirs(STARE, exist_ok=True)
    blocare = open(os.path.join(STARE, '.blocare'), 'w')
    try:
        fcntl.flock(blocare, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        jurnal('O verificare anterioară încă rulează, ies.')
        return
    subprocess.run(['git', '-C', DEPOZIT, 'pull', '-q', '--rebase', 'origin', 'main'], capture_output=True)
    noi = candidati()
    if '--doar-lista' in sys.argv:
        for c in noi:
            print('-', c['titlu'], '|', c['url'])
        return
    if not noi:
        jurnal('Nimic nou.')
        return
    salveaza(CANDIDATI, noi)
    jurnal(f'{len(noi)} articole noi, pornesc Claude.')
    with open(os.path.join(DEPOZIT, 'mac', 'prompt.md'), encoding='utf-8') as f:
        prompt = f.read()
    unelte = ['Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash(git:*)', 'Bash(python3:*)', 'Bash(node:*)', 'Bash(curl:*)',
              'Bash(ls:*)', 'Bash(cat:*)', 'Bash(head:*)', 'Bash(grep:*)', 'Bash(wc:*)', 'Bash(date:*)']
    start = time.time()
    r = subprocess.run(['claude', '-p', prompt, '--allowedTools', *unelte, '--max-turns', '60', '--output-format', 'text'],
                       cwd=DEPOZIT, capture_output=True, text=True, timeout=3600)
    raport = (r.stdout or r.stderr or '').strip()
    prima = raport.splitlines()[0] if raport else 'Fără raport'
    jurnal(f'Claude a terminat în {int(time.time() - start)}s: {prima}')
    with open(os.path.join(STARE, 'ultimul-raport.txt'), 'w', encoding='utf-8') as f:
        f.write(raport)
    vazute_local = set(incarca(VAZUTE_LOCAL, []))
    vazute_local.update(c['link_original'] for c in noi)
    salveaza(VAZUTE_LOCAL, sorted(vazute_local)[-5000:])
    if not prima.lower().startswith('nimic nou'):
        notifica(prima)


if __name__ == '__main__':
    main()
