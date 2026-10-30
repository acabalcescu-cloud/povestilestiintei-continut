# Cronica automată după meci – instrucțiuni pentru sesiunea programată

Rulează zilnic la 23:43 (ora României). Scopul: dacă Universitatea Craiova a jucat azi sau ieri un meci oficial fără cronică, scrie cronica, coperta și scorul în acest depozit. Site-ul povestilestiintei.ro le preia singur (cronica ca ciornă, scorul direct în meci).

## Pași
1. **A jucat Craiova?** Caută pe web (ora României) meciurile oficiale ale Universității Craiova de azi și de ieri (Sofascore, LPF, GSP). Amicalele nu contează.
2. **Există deja?** Pentru fiecare meci terminat, dacă `cronici/<AAAA-LL-ZZ>-*.json` există pentru data lui → sari peste el. Dacă meciul de azi s-a terminat prea târziu și sursele sunt încă sărace, lasă-l pe mâine-seară (va fi „ieri”). Niciun meci de scris → oprește-te fără commit.
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
6. **`index.json`** – adaugă `"cronici/<id>.json"` la începutul listei `cronici` (păstrează maximum 60).
7. **Commit și push** pe `main`, mesaj: `Cronica: <gazde> – <oaspeti> <scor>`.
8. **Raport** scurt: scorul, titlul, sursele. Dacă faptele n-au putut fi confirmate din două surse, spune-o și nu face commit.
