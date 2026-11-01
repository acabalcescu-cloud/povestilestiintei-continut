#!/usr/bin/env python3
"""Meciul în direct, pe Mac: echipele de start, golurile Științei și finalul, din Sofascore.

Rulează la fiecare 2 minute (launchd), fără inteligență artificială. Lucrează doar în ziua
meciului, de la 90 de minute înainte de start până la final (cel mult 3 ore și jumătate după start).

  - Echipele de start: când Sofascore le marchează „confirmate”, publică știrea cu formațiile.
  - Fiecare gol al Științei: o știre scurtă cu marcatorul, minutul, pasa decisivă, scorul și
    video-ul jucătorului din fișa lui ([ps_jucator_video]). Un gol se publică abia când apare la
    două verificări la rând (2–4 minute după gol), ca să nu publicăm goluri anulate la VAR.
  - Finalul: pornește imediat cronica (mac/meci.py --acum).

Lucrează într-o copie separată a depozitului (.stare-mac/live-depozit), ca să nu încurce Claude,
care poate scrie în același timp în depozitul principal.

Rulare manuală:  python3 mac/live.py              (o verificare, ca launchd)
                 python3 mac/live.py --test       (arată ce vede acum în Sofascore, fără să publice nimic)
                 python3 mac/live.py --test 16403928   (același lucru, pentru un anumit meci Sofascore)
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
API = 'https://api.sofascore.com/api/v1'
SLUG = 'universitatea-craiova'            # echipa noastră pe Sofascore (nu „fc-u-craiova-1948”)
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
INAINTE, DUPA = 90, 210                   # fereastra de lucru, în minute față de start
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


def get(url):
    r = subprocess.run(['curl', '-s', '-L', '--max-time', '25', '-A', UA, '-H', 'Accept: application/json',
                        '-H', 'Referer: https://www.sofascore.com/', url], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {}


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


def eveniment(start):
    """Meciul din Sofascore: în programul zilei, echipa cu slug-ul nostru."""
    d = get(f'{API}/sport/football/scheduled-events/{start:%Y-%m-%d}')
    for e in d.get('events', []):
        if SLUG in (e.get('homeTeam', {}).get('slug'), e.get('awayTeam', {}).get('slug')):
            return e
    return None


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

def nume_jucator(p):
    return html.unescape((p.get('player') or {}).get('name', '')).strip()


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
    B.append(f'<p><em>Surse:</em> <a href="https://www.sofascore.com/event/{ev["id"]}">Sofascore</a> (formații confirmate)</p>')
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
    B.append(f'<p><em>Sursa:</em> <a href="https://www.sofascore.com/event/{ev["id"]}">Sofascore</a></p>')
    ide = f'{zi}-stire-gol-{slug(marcator or "autogol")}-{slug(m)}'
    return {
        'id': ide, 'titlu': titlu,
        'rezumat': f'{marcator or "Autogol"}, minutul {m}: {gazde} – {oaspeti} {scor}.',
        'continut': '\n'.join(B), 'categorie': 'Știri',
        'etichete': ['Universitatea Craiova', adv, 'Gol'] + ([marcator] if marcator and not autogol else []),
        'imagine': ide + '.jpg', 'data_publicare': f'{acum:%Y-%m-%d %H:%M}', 'anunt': False,
    }


def goluri_noastre(ev, incidente):
    """Golurile Științei din lista Sofascore, inclusiv autogolurile adversarilor.
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
    if test_id:
        ev = get(f'{API}/event/{test_id}').get('event')
        start = dt.datetime.fromtimestamp(ev['startTimestamp']) if ev else acum
    else:
        m, start = meci_azi(acum)
        if not m:
            return
        ev = eveniment(start)
    if not ev:
        jurnal('Nu găsesc meciul în Sofascore (sau Sofascore nu răspunde).')
        return
    stare = incarca(LIVE, {})
    s = stare.setdefault(str(ev['id']), {'echipe': False, 'goluri': [], 'vazute': [], 'final': False})

    # 1. echipele de start
    lu = get(f"{API}/event/{ev['id']}/lineups")
    if test_id:
        print('Meci:', ev['homeTeam']['name'], '–', ev['awayTeam']['name'], '| stare:', ev.get('status', {}).get('type'))
        print('Formații confirmate:', lu.get('confirmed'))
    if lu.get('confirmed') and not s['echipe']:
        a = articol_echipe(ev, lu, start, acum)
        # Dacă știrea cu echipele există deja pentru ziua asta (scrisă de mână sau de rutina de știri), n-o dublăm.
        clona()
        if not test_id and [f for f in os.listdir(os.path.join(CLONA, 'cronici')) if f.startswith(f'{start:%Y-%m-%d}-stire-echipele-de-start') and f.endswith('.json') and not f.endswith('.coperta.json')]:
            s['echipe'] = True
            jurnal('Știrea cu echipele de start există deja; n-o mai public.')
        if test_id:
            print('\nȘtirea cu echipele:\n', a['titlu'], '\n', re.sub('<[^>]+>', '', a['continut']))
        elif s['echipe']:
            pass
        elif publica(a, 'SuperLiga', f"Live: echipele de start {ev['homeTeam']['name']} - {ev['awayTeam']['name']}"):
            s['echipe'] = True
            jurnal(f"Publicat: {a['titlu']}")
            notifica(a['titlu'])

    # 2. golurile Științei (publicate doar dacă apar la două verificări la rând)
    inc = get(f"{API}/event/{ev['id']}/incidents").get('incidents', [])
    goluri = goluri_noastre(ev, inc)
    acum_vazute = [cheie_gol(g) for g in goluri]
    for g in sorted(goluri, key=lambda x: (x.get('time') or 0, x.get('addedTime') or 0)):
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
    s['vazute'] = acum_vazute

    # 3. finalul: cronica imediat
    stat = (get(f"{API}/event/{ev['id']}").get('event') or ev).get('status', {}).get('type')
    if test_id:
        print('\nStare meci:', stat)
        return
    if stat == 'finished' and not s['final']:
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
            ev = eveniment(start) if m else None
            if not ev:
                print('Niciun meci al Științei în fereastra de acum (sau Sofascore nu răspunde de pe acest calculator).')
            else:
                verifica(test_id=ev['id'])
    else:
        verifica()
