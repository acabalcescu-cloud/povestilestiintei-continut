# Cronica automată după meci – instrucțiuni pentru sesiunea programată

Rulează zilnic seara. Scopul: dacă Universitatea Craiova a jucat azi un meci oficial, scrie cronica, coperta și scorul în acest depozit. Site-ul povestilestiintei.ro le preia singur (cronica ca ciornă, scorul direct în meci).

## Pași
1. **A jucat Craiova azi?** Caută pe web (ora României) meciul de azi al Universității Craiova (Sofascore, LPF, GSP). Fără meci terminat azi → oprește-te, nu scrie nimic.
2. **Există deja?** Dacă `cronici/<AAAA-LL-ZZ>-*.json` există pentru data de azi → oprește-te.
3. **Strânge faptele** din cel puțin două surse: scor final și la pauză, competiție și etapă, marcatori cu minute (autogol/penalty), echipa de start a Craiovei, momente-cheie, arbitru, clasament și următorul meci. La loviturile de departajare: scorul de la final de prelungiri + „(x-y d.l.l.)”.
4. **Scrie cronica** după `STIL.md`.
5. **Fișierele**, cu `<id>` = `AAAA-LL-ZZ-gazde-oaspeti` (fără diacritice, cu cratime), ex. `2026-10-29-voluntari-craiova`:
   - `cronici/<id>.json`:
     ```json
     {
       "id": "<id>",
       "titlu": "…",
       "rezumat": "1-2 fraze pentru lista de articole",
       "continut": "<p>…</p>",
       "categorie": "SuperLiga | Cupa României | Supercupa României | Liga Campionilor | Europa League | Conference League",
       "etichete": ["Universitatea Craiova", "<adversar>", "<sezon, ex. 2026/2027>"],
       "imagine": "<id>.jpg",
       "meci": { "data": "AAAA-LL-ZZ", "scor": [goluri_gazde, goluri_oaspeti] }
     }
     ```
     `scor` e în ordinea gazde–oaspeți, la fel ca pe site. Fără departajare în `scor`.
   - `cronici/<id>.coperta.json` – datele copertei (vezi `unelte/coperta.js`); `sofa_id` din `unelte/cluburi.tsv`.
   - `cronici/<id>.jpg` – `node unelte/coperta.js cronici/<id>.coperta.json cronici/<id>.jpg`. Uită-te la imagine înainte de commit.
6. **`index.json`** – adaugă `"cronici/<id>.json"` la începutul listei `cronici` (păstrează maximum 30).
7. **Commit și push** pe `main`, mesaj: `Cronica: <gazde> – <oaspeti> <scor>`.
8. **Raport** scurt: scorul, titlul, sursele. Dacă faptele n-au putut fi confirmate din două surse, spune-o și nu face commit.
