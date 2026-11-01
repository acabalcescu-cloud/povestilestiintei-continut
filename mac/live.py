#!/usr/bin/env python3
"""Meciul în direct, pe Mac: echipele de start, golurile Științei și finalul, din API-Football.

Rulează la fiecare 2 minute (launchd), fără inteligență artificială, dar întreabă API-Football cel mult
o dată la 3 minute (varianta gratuită are 100 de cereri pe zi). Lucrează doar în ziua meciului,
de la 60 de minute înainte de start până la final.

  - Echipele de start: când apar în API-Football, publică știrea cu formațiile
    (dacă nu există deja una pentru ziua respectivă).
  - Fiecare gol al Științei: o știre scurtă cu marcatorul, minutul, pasa decisivă, scorul și
    video-ul jucătorului din fișa lui ([ps_jucator_video]). Un gol se publică abia când apare la
    două verificări la rând (3–6 minute după gol), ca să nu publicăm goluri anulate la VAR.
  - Finalul: pornește imediat cronica (mac/meci.py --acum).

Cheia API stă doar pe Mac, în .stare-mac/api-football.env:  API_FOOTBALL_KEY=...
Lucrează într-o copie separată a depozitului (.stare-mac/live-depozit), ca să nu încurce Claude.

Rulare manuală:  python3 mac/live.py              (o verificare, ca launchd)
                 python3 mac/live.py --test       (meciul de azi: ce vede acum în API-Football, fără să publice)
                 python3 mac/live.py --test 1234567   (același lucru, pentru un meci anume, după id-ul API-Football)
"""
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import time
import unicodedata

DEPOZIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STARE = os.path.join(DEPOZIT, '.stare-mac')
CLONA = os.path.join(STARE, 'live-depozit')
LIVE = os.path.join(STARE, 'live.json')
JURNAL = os.path.join(STARE, 'jurnal.log')
URL_MECIURI = 'https://povestilestiintei.ro/wp-json/ps/v1/meciuri'
API = 'https://v3.football.api-sports.io'
CHEIE = os.path.join(STARE, 'api-football.env')
SLUG = 'universitatea-craiova'            # marcajul intern al echipei noastre în structurile de mai jos
PAUZA = 180                               # secunde între două cereri către API-Football
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
INAINTE, DUPA = 60, 210                   # fereastra de lucru, în minute față de start
POST = {'G': 'Portar', 'D': 'Fundaș', 'M': 'Mijlocaș', 'F': 'Atacant'}


def jurnal(msg):
    os.makedirs(STARE, exist_ok=True)
    rand = f"{dt.datetime.now():%Y-%m-%d %H:%M} [live] {msg}"
    print(rand)
    with open(JURNAL, 'a', encoding='utf-8') as f:
        f.write(rand + '\n')


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


def cheie_api():
    try:
        with open(CHEIE, encoding='utf-8') as f:
            for rand in f:
                if rand.strip().startswith('API_FOOTBALL_KEY='):
                    return rand.split('=', 1)[1].strip()
    except OSError:
        pass
    return os.environ.get('API_FOOTBALL_KEY', '')


def api(cale):
    """O cerere către API-Football; întoarce câmpul „response” (listă) sau None."""
    k = cheie_api()
    if not k:
        jurnal('Lipsește cheia API-Football (.stare-mac/api-football.env).')
        return None
    r = subprocess.run(['curl', '-s', '--max-time', '25', '-H', f'x-apisports-key: {k}', API + cale], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        return None
    if d.get('errors'):
        jurnal(f"API-Football: {d['errors']}")
        return None
    return d.get('response')


def slug(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def notifica(text):
    text = text.replace('"', "'")[:200]
    subprocess.run(['osascript', '-e', f'display notification "{text}" with title "Poveștile Științei – live"'], capture_output=True)


# ---------- meciul de azi ----------

def meci_azi(acum):
    """Meciul Științei din lista site-ului aflat acum în fereastra de lucru."""
    r = subprocess.run(['curl', '-s', '-L', '--max-time', '30', '-A', UA, URL_MECIURI], capture_output=True, text=True)
    try:
        lista = json.loads(r.stdout)
    except ValueError:
        lista = incarca(os.path.join(STARE, 'meciuri.json'), [])
    for m in lista:
        try:
            start = dt.datetime.strptime(m['data'], '%Y/%m/%d %H:%M')
        except (KeyError, ValueError):
            continue
        if start - dt.timedelta(minutes=INAINTE) <= acum <= start + dt.timedelta(minutes=DUPA):
            return m, start
    return None, None


def echipa_noastra():
    """Id-ul Universității Craiova în API-Football (nu FC U Craiova 1948), păstrat local după prima căutare."""
    st = incarca(LIVE, {})
    if st.get('_echipa'):
        return st['_echipa']
    for t in api('/teams?search=Craiova&country=Romania') or []:
        nume = t.get('team', {}).get('name', '')
        if 'Universitatea Craiova' in nume or nume in ('U Craiova', 'Univ. Craiova', 'CS Universitatea Craiova'):
            if '1948' not in nume:
                st['_echipa'] = t['team']['id']
                salveaza(LIVE, st)
                return st['_echipa']
    return None


def meci_api(start=None, fid=None):
    """Meciul complet (stare, scor, goluri, echipe) dintr-o singură cerere."""
    if not fid:
        st = incarca(LIVE, {})
        fid = st.get('_meciuri', {}).get(f'{start:%Y-%m-%d}')
        if not fid:
            noi = echipa_noastra()
            lst = api(f'/fixtures?team={noi}&date={start:%Y-%m-%d}&timezone=Europe/Bucharest') if noi else None
            if not lst:
                return None
            fid = lst[0]['fixture']['id']
            st.setdefault('_meciuri', {})[f'{start:%Y-%m-%d}'] = fid
            salveaza(LIVE, st)
    r = api(f'/fixtures?id={fid}&timezone=Europe/Bucharest')
    return r[0] if r else None


def adapteaza(f):
    """Datele API-Football în structura folosită de texte: ev, echipe, goluri (cu scorul după fiecare gol)."""
    noi = incarca(LIVE, {}).get('_echipa')
    h, a = f['teams']['home'], f['teams']['away']
    def echipa(t):
        return {'id': t['id'], 'name': t['name'], 'slug': SLUG if t['id'] == noi else slug(t['name'])}
    ev = {'id': f['fixture']['id'], 'homeTeam': echipa(h), 'awayTeam': echipa(a), 'status': f['fixture']['status']['short']}
    lineups = {}
    jucatori = {}
    for l in f.get('lineups') or []:
        latura = 'home' if l['team']['id'] == h['id'] else 'away'
        pl = [{'player': {'name': x['player']['name']}, 'position': x['player'].get('pos') or '', 'substitute': False} for x in l.get('startXI') or []]
        pl += [{'player': {'name': x['player']['name']}, 'position': x['player'].get('pos') or '', 'substitute': True} for x in l.get('substitutes') or []]
        lineups[latura] = {'formation': l.get('formation') or '', 'players': pl}
        for x in pl:
            jucatori[x['player']['name']] = latura
    if len(lineups) == 2:
        lineups['confirmed'] = True
    goluri, gh, ga = [], 0, 0
    evs = [e for e in f.get('events') or [] if e.get('type') == 'Goal' and e.get('detail') != 'Missed Penalty']
    evs.sort(key=lambda e: ((e['time'].get('elapsed') or 0), (e['time'].get('extra') or 0)))
    for e in evs:
        echipa_ev = 'home' if e['team']['id'] == h['id'] else 'away'
        autogol = e.get('detail') == 'Own Goal'
        beneficiar = echipa_ev
        if autogol and jucatori.get(e['player'].get('name')) == echipa_ev:
            # jucătorul care a marcat în propria poartă e din echipa indicată: golul e al celeilalte
            beneficiar = 'away' if echipa_ev == 'home' else 'home'
        if beneficiar == 'home':
            gh += 1
        else:
            ga += 1
        goluri.append({'incidentType': 'goal', 'time': e['time'].get('elapsed'), 'addedTime': e['time'].get('extra'),
                       'homeScore': gh, 'awayScore': ga, 'isHome': beneficiar == 'home',
                       'incidentClass': 'ownGoal' if autogol else ('penalty' if e.get('detail') == 'Penalty' else 'regular'),
                       'player': {'name': (e.get('player') or {}).get('name') or ''},
                       'assist1': {'name': (e.get('assist') or {}).get('name') or ''},
                       'id': f"{e['time'].get('elapsed')}-{(e.get('player') or {}).get('id')}"})
    return ev, lineups, goluri


# ---------- depozitul separat și publicarea ----------

def clona():
    if not os.path.isdir(os.path.join(CLONA, '.git')):
        url = subprocess.run(['git', '-C', DEPOZIT, 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout.strip()
        subprocess.run(['git', 'clone', '-q', '--depth', '50', url, CLONA], check=True)
    subprocess.run(['git', '-C', CLONA, 'fetch', '-q', 'origin', 'main'], check=True)
    subprocess.run(['git', '-C', CLONA, 'reset', '-q', '--hard', 'origin/main'], check=True)


def publica(articol, rubrica, mesaj):
    """Scrie articolul și coperta în copia separată, îl adaugă în index și îl trimite pe GitHub (cu reîncercări)."""
    for incercare in range(4):
        clona()
        cr = os.path.join(CLONA, 'cronici')
        if os.path.exists(os.path.join(cr, articol['id'] + '.json')):
            return True  # există deja (publicat de altcineva sau de o rulare anterioară)
        salveaza(os.path.join(cr, articol['id'] + '.json'), articol)
        salveaza(os.path.join(cr, articol['id'] + '.coperta.json'), {'titlu': articol['titlu'], 'rubrica': rubrica, 'data': articol['data_publicare']})
        subprocess.run(['node', os.path.join(DEPOZIT, 'unelte', 'coperta-stire.js'), os.path.join(cr, articol['id'] + '.coperta.json'),
                        os.path.join(cr, articol['id'] + '.jpg')], cwd=DEPOZIT, capture_output=True, timeout=120)
        idx_cale = os.path.join(CLONA, 'index.json')
        idx = incarca(idx_cale, {'cronici': []})
        f = f"cronici/{articol['id']}.json"
        idx['cronici'] = [f] + [x for x in idx['cronici'] if x != f]
        with open(idx_cale, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(idx, ensure_ascii=False, indent=2))
        subprocess.run(['git', '-C', CLONA, 'add', '-A', 'cronici', 'index.json'], check=True)
        subprocess.run(['git', '-C', CLONA, 'commit', '-q', '-m', mesaj], check=True)
        if subprocess.run(['git', '-C', CLONA, 'push', '-q', 'origin', 'HEAD:main'], capture_output=True).returncode == 0:
            return True
        time.sleep(5 * (incercare + 1))
    return False


# ---------- textele ----------

_LOT = None


def lot():
    """Numele complete ale jucătorilor noștri, de pe site (/ps/v1/jucatori)."""
    global _LOT
    if _LOT is None:
        r = subprocess.run(['curl', '-s', '--max-time', '20', '-A', UA, 'https://povestilestiintei.ro/wp-json/ps/v1/jucatori'], capture_output=True, text=True)
        try:
            _LOT = [html.unescape(j['nume']) for j in json.loads(r.stdout)]
        except (ValueError, KeyError, TypeError):
            _LOT = []
    return _LOT


def complet(nume):
    """„A. Al Hamlawi” → „Assad Al Hamlawi”, „N. Stevanović” → „Nikola Stevanovic”, dacă se potrivește unic în lot."""
    n = slug(nume).replace('-', ' ')
    if not n:
        return nume
    for j in lot():
        if slug(j).replace('-', ' ') == n:
            return j
    parti = n.split(' ')
    fam = ' '.join(parti[1:]) if len(parti) > 1 and len(parti[0]) <= 2 else n
    gasiti = [j for j in lot() if slug(j).replace('-', ' ').endswith(' ' + fam)]
    if len(gasiti) == 1 and (len(parti[0]) > 2 or slug(gasiti[0])[0] == parti[0][0]):
        return gasiti[0]
    return nume


def nume_jucator(p):
    n = html.unescape((p.get('player') or {}).get('name', '')).strip()
    return complet(n) if p.get('_noi') else n


def formatie(echipa):
    """„Popescu – Romanchuk, Stevanović, Screciu – ...” după poziții, plus rezervele."""
    titulari = [p for p in echipa.get('players', []) if not p.get('substitute')]
    rezerve = [p for p in echipa.get('players', []) if p.get('substitute')]
    linii = []
    for poz in 'GDMF':
        grup = [nume_jucator(p) + (' (căpitan)' if p.get('captain') else '') for p in titulari if p.get('position') == poz]
        if grup:
            linii.append(', '.join(grup))
    return ' – '.join(linii), ', '.join(nume_jucator(p) for p in rezerve)


def articol_echipe(ev, lineups, start, acum):
    noi_acasa = ev['homeTeam']['slug'] == SLUG
    gazde, oaspeti = html.unescape(ev['homeTeam']['name']), html.unescape(ev['awayTeam']['name'])
    noi = lineups['home' if noi_acasa else 'away']
    for x in noi.get('players', []):
        x['_noi'] = True
    ei = lineups['away' if noi_acasa else 'home']
    adv = oaspeti if noi_acasa else gazde
    t_noi, r_noi = formatie(noi)
    t_ei, r_ei = formatie(ei)
    f_noi, f_ei = noi.get('formation', ''), ei.get('formation', '')
    zi = f'{start:%Y-%m-%d}'
    B = [
        f'<p>Echipele de start pentru meciul Universitatea Craiova – {adv}, de la ora {start:%H:%M}, au fost anunțate. Știința intră în teren'
        + (f' în sistemul {f_noi}' if f_noi else '') + '.</p>',
        f'<h3>Universitatea Craiova' + (f' ({f_noi})' if f_noi else '') + '</h3>',
        f'<p>{t_noi}.</p>',
    ]
    if r_noi:
        B.append(f'<p><em>Rezerve:</em> {r_noi}.</p>')
    B += [f'<h3>{adv}' + (f' ({f_ei})' if f_ei else '') + '</h3>', f'<p>{t_ei}.</p>']
    if r_ei:
        B.append(f'<p><em>Rezerve:</em> {r_ei}.</p>')
    B.append('<p>Revenim cu golurile și cu cronica meciului. Hai Știința!</p>')
    B.append('<p><em>Sursa:</em> datele oficiale ale meciului (API-Football).</p>')
    return {
        'id': f'{zi}-stire-echipele-de-start-{slug(adv)}',
        'titlu': f'Echipele de start: Universitatea Craiova – {adv}',
        'rezumat': f'Primul 11 al Științei pentru meciul cu {adv}' + (f', în sistemul {f_noi}' if f_noi else '') + '.',
        'continut': '\n'.join(B), 'categorie': 'Știri',
        'etichete': ['Universitatea Craiova', adv, 'Echipe de start'],
        'imagine': f'{zi}-stire-echipele-de-start-{slug(adv)}.jpg',
        'data_publicare': f'{acum:%Y-%m-%d %H:%M}', 'anunt': False,
    }


def minut(inc):
    t = inc.get('time')
    plus = inc.get('addedTime')
    return f'{t}+{plus}' if plus and plus != 999 else str(t)


def articol_gol(ev, inc, start, acum):
    noi_acasa = ev['homeTeam']['slug'] == SLUG
    gazde, oaspeti = html.unescape(ev['homeTeam']['name']), html.unescape(ev['awayTeam']['name'])
    adv = oaspeti if noi_acasa else gazde
    scor = f"{inc.get('homeScore')}-{inc.get('awayScore')}"
    autogol = inc.get('incidentClass') == 'ownGoal'
    penalty = inc.get('incidentClass') == 'penalty'
    marcator = html.unescape((inc.get('player') or {}).get('name', '') or inc.get('playerName', '')).strip()
    pasa = html.unescape((inc.get('assist1') or {}).get('name', '')).strip()
    if not autogol:
        marcator, pasa = complet(marcator), (complet(pasa) if pasa else pasa)
    m = minut(inc)
    zi = f'{start:%Y-%m-%d}'
    if autogol:
        titlu = f'GOL! Autogol în minutul {m}: {gazde} – {oaspeti} {scor}'
        B = [f'<p>Știința marchează în minutul {m}: {marcator or "un jucător advers"} își învinge propriul portar. {gazde} – {oaspeti} {scor}.</p>']
    else:
        titlu = f'GOL! {marcator} marchează în minutul {m}: {gazde} – {oaspeti} {scor}'
        B = [f'<p>{marcator} a marcat în minutul {m}' + (' din penalty' if penalty else '') + (f', după pasa lui {pasa}' if pasa else '')
             + f'. Scorul pe „Ion Oblemenco”: {gazde} – {oaspeti} {scor}.</p>' if noi_acasa else
             f'<p>{marcator} a marcat în minutul {m}' + (' din penalty' if penalty else '') + (f', după pasa lui {pasa}' if pasa else '')
             + f'. Scorul: {gazde} – {oaspeti} {scor}.</p>']
        B.append(f'[ps_jucator_video nume="{marcator}"]')
    B.append(f'<p>Meciul continuă. Revenim cu cronica după fluierul final. Hai Știința!</p>')
    B.append('<p><em>Sursa:</em> datele oficiale ale meciului (API-Football).</p>')
    ide = f'{zi}-stire-gol-{slug(marcator or "autogol")}-{slug(m)}'
    return {
        'id': ide, 'titlu': titlu,
        'rezumat': f'{marcator or "Autogol"}, minutul {m}: {gazde} – {oaspeti} {scor}.',
        'continut': '\n'.join(B), 'categorie': 'Știri',
        'etichete': ['Universitatea Craiova', adv, 'Gol'] + ([marcator] if marcator and not autogol else []),
        'imagine': ide + '.jpg', 'data_publicare': f'{acum:%Y-%m-%d %H:%M}', 'anunt': False,
    }


def goluri_noastre(ev, incidente):
    """Golurile Științei, inclusiv autogolurile adversarilor.
    Echipa care a marcat se deduce din scorul care crește de la un gol la altul."""
    noi_acasa = ev['homeTeam']['slug'] == SLUG
    goluri = [i for i in incidente if i.get('incidentType') == 'goal' and i.get('homeScore') is not None]
    goluri.sort(key=lambda x: ((x.get('time') or 0), (x.get('addedTime') or 0) if x.get('addedTime') != 999 else 0, (x.get('homeScore') or 0) + (x.get('awayScore') or 0)))
    out, gazde, oaspeti = [], 0, 0
    for g in goluri:
        h, a = g.get('homeScore') or 0, g.get('awayScore') or 0
        if (h > gazde) if noi_acasa else (a > oaspeti):
            out.append(g)
        gazde, oaspeti = h, a
    return out


def cheie_gol(inc):
    return f"{inc.get('id') or ''}-{inc.get('time')}-{inc.get('homeScore')}-{inc.get('awayScore')}"


# ---------- bucla ----------

def verifica(test_id=None):
    acum = dt.datetime.now()
    stare = incarca(LIVE, {})
    if test_id:
        f = meci_api(fid=test_id)
        start = dt.datetime.fromtimestamp(f['fixture']['timestamp']) if f else acum
    else:
        m, start = meci_azi(acum)
        if not m:
            return
        if time.time() - stare.get('_ultima', 0) < PAUZA - 10:
            return  # cel mult o cerere la 3 minute (limita variantei gratuite)
        stare['_ultima'] = time.time()
        salveaza(LIVE, stare)
        f = meci_api(start=start)
    if not f:
        jurnal('Nu găsesc meciul în API-Football (sau lipsește cheia).')
        return
    ev, lu, goluri = adapteaza(f)
    stare = incarca(LIVE, {})
    s = stare.setdefault(str(ev['id']), {'echipe': False, 'goluri': [], 'vazute': [], 'final': False})
    if test_id:
        print('Meci:', ev['homeTeam']['name'], '–', ev['awayTeam']['name'], '| stare:', ev['status'], '| echipa noastră găsită:', SLUG in (ev['homeTeam']['slug'], ev['awayTeam']['slug']))
        print('Echipe de start disponibile:', bool(lu.get('confirmed')))

    # 1. echipele de start
    if lu.get('confirmed') and not s['echipe']:
        a = articol_echipe(ev, lu, start, acum)
        if test_id:
            print('\nȘtirea cu echipele:\n', a['titlu'], '\n', re.sub('<[^>]+>', '', a['continut']))
        else:
            clona()
            deja = [x for x in os.listdir(os.path.join(CLONA, 'cronici')) if x.startswith(f'{start:%Y-%m-%d}-stire-echipele-de-start') and x.endswith('.json') and not x.endswith('.coperta.json')]
            if deja:
                s['echipe'] = True
                jurnal('Știrea cu echipele de start există deja; n-o mai public.')
            elif publica(a, 'SuperLiga', f"Live: echipele de start {ev['homeTeam']['name']} - {ev['awayTeam']['name']}"):
                s['echipe'] = True
                jurnal(f"Publicat: {a['titlu']}")
                notifica(a['titlu'])

    # 2. golurile Științei (publicate doar dacă apar la două verificări la rând)
    ale_noastre = goluri_noastre(ev, goluri)
    for g in ale_noastre:
        k = cheie_gol(g)
        a = articol_gol(ev, g, start, acum)
        if test_id:
            print('\nGol:', a['titlu'])
            continue
        if k in s['goluri'] or k not in s['vazute']:
            continue
        if publica(a, 'SuperLiga', f"Live: {a['titlu']}"):
            s['goluri'].append(k)
            jurnal(f"Publicat: {a['titlu']}")
            notifica(a['titlu'])
    s['vazute'] = [cheie_gol(g) for g in ale_noastre]

    # 3. finalul: cronica imediat
    if test_id:
        return
    if ev['status'] in ('FT', 'AET', 'PEN') and not s['final']:
        s['final'] = True
        salveaza(LIVE, stare)
        jurnal('Final de meci: pornesc cronica.')
        subprocess.run([sys.executable, os.path.join(DEPOZIT, 'mac', 'meci.py'), '--acum'], cwd=DEPOZIT)
    salveaza(LIVE, stare)


if __name__ == '__main__':
    if '--test' in sys.argv:
        rest = [a for a in sys.argv[1:] if a != '--test']
        if rest:
            verifica(test_id=rest[0])
        else:
            m, start = meci_azi(dt.datetime.now())
            if not m:
                print('Niciun meci al Științei în fereastra de acum (cu o oră înainte de start, până la final).')
            else:
                f = meci_api(start=start)
                if not f:
                    print('Nu găsesc meciul în API-Football (sau lipsește cheia).')
                else:
                    verifica(test_id=f['fixture']['id'])
    else:
        verifica()
