# Cronica automată după meci – instrucțiuni pentru sesiunea programată

Rulează zilnic la 23:43 (ora României). Scopul: dacă Universitatea Craiova a jucat azi sau ieri un meci oficial fără cronică, scrie cronica, coperta și scorul în acest depozit. Site-ul povestilestiintei.ro le preia singur (cronica ca ciornă, scorul direct în meci).

## Pași
1. **A jucat Craiova?** Caută pe web (ora României) meciurile oficiale ale Universității Craiova de azi și de ieri (Sofascore, LPF, GSP). Amicalele nu contează.
2. **Există deja?** Pentru fiecare meci terminat, dacă `cronici/<AAAA-LL-ZZ>-*.json` există pentru data lui → sari peste el. Dacă meciul de azi s-a terminat prea târziu și sursele sunt încă sărace, lasă-l pe mâine-seară (va fi „ieri”). Nicio cronică de scris → treci direct la pasul 6 (rezumatele video).
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
       "meci": {
         "data": "AAAA-LL-ZZ", "scor": [goluri_gazde, goluri_oaspeti],
         "marcatori": {
           "gazde":   [{ "nume": "Nsimba", "minut": "45+3' (pen.)" }],
           "oaspeti": [{ "nume": "Guțea", "minut": "90+3' (pen.)" }]
         }
       }
     }
     ```
     `scor` e în ordinea gazde–oaspeți, la fel ca pe site. Fără departajare în `scor`.
     `marcatori` apar pe pagina meciului, sub sigla fiecărei echipe: numele de familie și minutul, cu „(pen.)” sau „(autogol)”. Autogolul stă la echipa care a beneficiat de el. Mai multe goluri ale aceluiași jucător merg pe un rând: `"24' (pen.), 44'"`. Numărul de goluri trebuie să dea exact scorul.
   - `cronici/<id>.coperta.json` – datele copertei (vezi `unelte/coperta.js`); `sofa_id` din `unelte/cluburi.tsv`.
   - `cronici/<id>.jpg` – `node unelte/coperta.js cronici/<id>.coperta.json cronici/<id>.jpg`. Uită-te la imagine înainte de commit.
6. **Rezumatul video.** Pentru fiecare meci cu cronică (cel nou și cele din ultimele 3 zile) care nu are încă `cronici/<id>-video.json`:
   - caută pe YouTube rezumatul oficial, de preferință de la Orange Sport Romania, apoi Prima Sport, Digi Sport, Superliga România, SPORT.RO sau Gazeta Sporturilor;
   - verifică-l prin oEmbed (`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json`): titlul trebuie să conțină ambele echipe și scorul meciului, iar canalul să fie unul dintre cele de mai sus. Atenție la meciuri mai vechi între aceleași echipe, cu același scor;
   - dacă nu găsești un rezumat sigur, nu pune nimic: încerci din nou mâine-seară;
   - dacă îl găsești, scrie `cronici/<id>-video.json`:
     ```json
     {
       "id": "<id>-video", "tip": "video",
       "titlu": "Rezumat video: <Gazde> – <Oaspeți> <scor>",
       "rezumat": "Golurile și fazele importante din <Gazde> – <Oaspeți>, <competiție>. Rezumat <canal>.",
       "video_url": "https://www.youtube.com/watch?v=<ID>",
       "imagine_url": "https://img.youtube.com/vi/<ID>/maxresdefault.jpg",
       "categorie": "Rezumate video",
       "etichete": ["Universitatea Craiova", "<adversar>", "<sezon>"]
     }
     ```
     (dacă `maxresdefault.jpg` nu există, folosește `hqdefault.jpg`).
7. **`index.json`** – adaugă fiecare fișier nou (`cronici/<id>.json`, `cronici/<id>-video.json`) la începutul listei `cronici` (păstrează maximum 80). Dacă n-ai scris nimic nou (nici cronică, nici video) → oprește-te fără commit.
8. **Commit și push** pe `main`, mesaj: `Cronica: <gazde> – <oaspeti> <scor>` (sau `Rezumat video: …` dacă e doar video).
9. **Raport** scurt: scorul, titlul, sursele. Dacă faptele n-au putut fi confirmate din două surse, spune-o și nu face commit.
