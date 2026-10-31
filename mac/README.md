# Știrile pe Mac Studio

O verificare automată rulează pe Mac în fiecare oră, la minutul 47. Nu folosește inteligență artificială: citește Google News și fluxurile RSS și se uită dacă a apărut ceva nou despre Știința. Numai atunci pornește Claude Code, care scrie știrea, o salvează în depozit și o trimite pe GitHub. Site-ul o preia singur, în cel mult 15 minute, și o publică.

Așa, Claude rulează doar în orele în care chiar există ceva de scris, nu de 24 de ori pe zi.

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
- Cronicile și video-urile rămân la rutina de noapte din cloud.
