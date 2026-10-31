# Știrile pe Mac Studio

O verificare automată rulează pe Mac în fiecare oră, la minutul 47. Nu folosește inteligență artificială: citește Google News și fluxurile RSS și se uită dacă a apărut ceva nou despre Știința. Numai atunci pornește Claude Code, care scrie știrea, o salvează în depozit și o trimite pe GitHub. Site-ul o preia singur, în cel mult 15 minute, și o publică.

Așa, Claude rulează doar în orele în care chiar există ceva de scris, nu de 24 de ori pe zi.

## Ziua meciului: cronica și rezumatul video

`mac/meci.py` rulează la fiecare 5 minute, tot fără AI. Ia ora de start din lista meciurilor de pe site (`/wp-json/ps/v1/meciuri`) și, dacă Știința joacă azi, pornește Claude la 2 ore după start, apoi la 150, 180, 210... minute, din 30 în 30, cel mult până la 23:55 în ziua meciului. Se oprește mai devreme, imediat ce în depozit există și cronica, și rezumatul video.

Exemplu: start 17:30 → verificări la 19:30, 20:00, 20:30 ... 23:30.

Meciurile care încep târziu (după 21:55, când prima verificare ar cădea după 23:55) nu au limita de 23:55: verificările încep la start + 2 ore, chiar după miezul nopții, și continuă din 30 în 30 de minute până apar cronica și video-ul, dar cel mult 24 de ore de la start. Exemplu: start 22:00 → 00:00, 00:30, 01:00 ... până la cronică și video.

`python3 mac/meci.py --program` arată orele verificărilor de azi.

## Ce trebuie pe Mac (o singură dată)

1. **Programele.** În Terminal:
   - Homebrew, dacă nu e instalat: vezi https://brew.sh
   - `brew install git node gh`
   - Claude Code: `npm install -g @anthropic-ai/claude-code`, apoi rulează o dată `claude` și loghează-te cu contul tău.
2. **Accesul la GitHub.** `gh auth login` (alege GitHub.com, HTTPS, login din browser). Contul trebuie să aibă drept de scriere în `acabalcescu-cloud/povestilestiintei-continut`.
3. **Depozitul.**
   ```
   cd ~
   gh repo clone acabalcescu-cloud/povestilestiintei-continut
   cd povestilestiintei-continut
   ```
4. **Instalarea.** `bash mac/instaleaza.sh`

## Verificare

- `python3 mac/verifica.py --doar-lista` arată ce articole noi ar fi găsit acum, fără să pornească Claude.
- `python3 mac/verifica.py` face o rundă completă imediat.
- `cat .stare-mac/jurnal.log` arată ce s-a întâmplat la fiecare oră.
- `cat .stare-mac/ultimul-raport.txt` arată raportul ultimei rulări Claude.

Când se publică o știre, apare o notificare pe Mac cu titlul ei.

## De știut

- Mac-ul trebuie să fie pornit. Dacă doarme, verificarea se face la trezire.
- Nu e nevoie de parola WordPress pe Mac: publicarea trece prin GitHub.
- Oprire: `bash mac/instaleaza.sh --sterge`.
- Rutina de noapte din cloud (23:43) rămâne ca plasă de siguranță pentru cronici și video.
