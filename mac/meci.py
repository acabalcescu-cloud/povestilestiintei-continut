#!/usr/bin/env python3
"""Cronica și rezumatul video în ziua meciului, pe Mac.

Rulează la fiecare 5 minute (launchd), fără inteligență artificială, și verifică
dacă Știința joacă azi. Dacă da, pornește Claude Code la 2 ore după ora de start,
apoi din 30 în 30 de minute (150, 180, 210... minute după start), cel mult până
la 23:55 în ziua meciului. Se oprește mai devreme dacă în depozit există deja
și cronica, și rezumatul video ale meciului.

Meciurile care încep după ora 20:00 nu au limita de 23:55: verificările continuă
din 30 în 30 de minute și după miezul nopții, până apar cronica și video-ul,
dar cel mult 12 ore de la start.

Ora de start vine din lista meciurilor de pe site: /wp-json/ps/v1/meciuri.

Rulare manuală:  python3 mac/meci.py           (o verificare, ca launchd)
                 python3 mac/meci.py --program (arată orele verificărilor de azi)
"""
import datetime as dt
import fcntl
import glob
import html
import json
import os
import subprocess
import sys
import time

DEPOZIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STARE = os.path.join(DEPOZIT, '.stare-mac')
MECIURI = os.path.join(STARE, 'meciuri.json')
FACUTE = os.path.join(STARE, 'meci-verificari.json')
JURNAL = os.path.join(STARE, 'jurnal.log')
URL = 'https://povestilestiintei.ro/wp-json/ps/v1/meciuri'
PRIMA, PAS = 120, 30           # minute după start: prima verificare, apoi pasul
LIMITA = dt.time(23, 55)       # nicio verificare după această oră, în ziua meciului
ORA_TARZIU = dt.time(20, 0)    # meciurile care încep după această oră sunt „târzii”
MAX_TARZIU = dt.timedelta(hours=12)  # meciurile târzii: verificări cel mult 12 ore de la start
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def jurnal(msg):
    os.makedirs(STARE, exist_ok=True)
    rand = f"{dt.datetime.now():%Y-%m-%d %H:%M} [meci] {msg}"
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


def meciuri():
    """Lista de pe site, reîmprospătată cel mult o dată pe oră; altfel copia locală."""
    if os.path.exists(MECIURI) and time.time() - os.path.getmtime(MECIURI) < 3600:
        return incarca(MECIURI, [])
    r = subprocess.run(['curl', '-s', '-L', '--max-time', '30', '-A', UA, URL], capture_output=True, text=True)
    try:
        lista = json.loads(r.stdout)
        assert isinstance(lista, list) and lista
        salveaza(MECIURI, lista)
        return lista
    except (ValueError, AssertionError):
        return incarca(MECIURI, [])


def meciuri_recente(acum):
    """Meciurile începute în ultimele 25 de ore (cel de azi și, eventual, unul târziu de ieri)."""
    out = []
    for m in meciuri():
        try:
            start = dt.datetime.strptime(m['data'], '%Y/%m/%d %H:%M')
        except (KeyError, ValueError):
            continue
        if acum - dt.timedelta(hours=25) <= start <= acum + dt.timedelta(hours=24):
            out.append((m, start))
    return out


def tarziu(start):
    return start.time() > ORA_TARZIU


def verificari(start):
    """Orele verificărilor: start + 120, 150, 180... minute.
    Meci până la 20:00: cel mult 23:55 în aceeași zi. Meci după 20:00: cel mult 12 ore după start."""
    capat = start + MAX_TARZIU if tarziu(start) else dt.datetime.combine(start.date(), LIMITA)
    ore, t = [], start + dt.timedelta(minutes=PRIMA)
    while t <= capat:
        ore.append(t)
        t += dt.timedelta(minutes=PAS)
    return ore


def complet(zi):
    """Cronica și rezumatul video ale meciului din ziua respectivă există în depozit?"""
    fisiere = [os.path.basename(f) for f in glob.glob(os.path.join(DEPOZIT, 'cronici', f'{zi:%Y-%m-%d}-*.json'))]
    cronici = [f for f in fisiere if '-stire-' not in f and 'florin' not in f and not f.endswith(('.coperta.json', '-video.json'))]
    return bool(cronici) and all(os.path.exists(os.path.join(DEPOZIT, 'cronici', c[:-5] + '-video.json')) for c in cronici)


def notifica(text):
    text = text.replace('"', "'")[:200]
    subprocess.run(['osascript', '-e', f'display notification "{text}" with title "Poveștile Științei – meci"'], capture_output=True)


def ruleaza(m, start, acum):
    trecute = [t for t in verificari(start) if t <= acum]
    if not trecute:
        return
    cheie = f'{trecute[-1]:%Y-%m-%d %H:%M}'
    facute = incarca(FACUTE, [])
    if cheie in facute:
        return
    os.makedirs(STARE, exist_ok=True)
    blocare = open(os.path.join(STARE, '.blocare'), 'w')
    try:
        fcntl.flock(blocare, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return  # rulează verificarea de știri; încercăm din nou peste 5 minute
    subprocess.run(['git', '-C', DEPOZIT, 'pull', '-q', '--rebase', 'origin', 'main'], capture_output=True)
    facute.append(cheie)
    salveaza(FACUTE, facute[-300:])
    if complet(start.date()):
        jurnal(f'{cheie}: cronica și video există deja, nimic de făcut.')
        return

    meci = f"{html.unescape(m['gazde'])} – {html.unescape(m['oaspeti'])} ({html.unescape(m.get('competitie', ''))}), {start:%d.%m.%Y}, ora {start:%H:%M}"
    with open(os.path.join(DEPOZIT, 'mac', 'prompt-meci.md'), encoding='utf-8') as f:
        prompt = f.read().replace('{MECI}', meci).replace('{DATA}', f'{start:%Y-%m-%d}')
    jurnal(f'{cheie}: verific cronica și video pentru {meci}.')
    unelte = ['Read', 'Write', 'Edit', 'Glob', 'Grep', 'WebSearch', 'WebFetch', 'Bash(git:*)', 'Bash(python3:*)', 'Bash(node:*)',
              'Bash(curl:*)', 'Bash(ls:*)', 'Bash(cat:*)', 'Bash(head:*)', 'Bash(grep:*)', 'Bash(wc:*)', 'Bash(date:*)']
    pornit = time.time()
    r = subprocess.run(['claude', '-p', prompt, '--allowedTools', *unelte, '--max-turns', '80', '--output-format', 'text'],
                       cwd=DEPOZIT, capture_output=True, text=True, timeout=3000)
    raport = (r.stdout or r.stderr or '').strip()
    prima = raport.splitlines()[0] if raport else 'Fără raport'
    jurnal(f'Claude a terminat în {int(time.time() - pornit)}s: {prima}')
    with open(os.path.join(STARE, 'ultimul-raport-meci.txt'), 'w', encoding='utf-8') as f:
        f.write(raport)
    if not prima.lower().startswith('nimic nou'):
        notifica(prima)


def main():
    acum = dt.datetime.now()
    recente = meciuri_recente(acum)
    if '--program' in sys.argv:
        if not recente:
            print('Nu e niciun meci azi sau în ultimele ore (după lista de pe site).')
        for m, start in recente:
            ore = verificari(start)
            print(f"{html.unescape(m['gazde'])} – {html.unescape(m['oaspeti'])}, start {start:%d.%m %H:%M}"
                  + (' (meci târziu: verificările continuă după miezul nopții, până la cronică și video)' if tarziu(start) else ''))
            arata = [f'{t:%d.%m %H:%M}' for t in ore]
            if len(arata) > 12:
                arata = arata[:10] + ['...', arata[-1]]
            print('Verificări:', ', '.join(arata))
        return
    for m, start in recente:
        ruleaza(m, start, acum)


if __name__ == '__main__':
    main()
