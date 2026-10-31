# Cronica automată după meci – instrucțiuni pentru sesiunea programată

Rulează zilnic la 23:43 (ora României). În zilele cu meci, cronica și rezumatul video se verifică și pe Mac Studio (`mac/meci.py`): la 2 ore după start, apoi din 30 în 30 de minute, până la 23:55. Scopul: dacă Universitatea Craiova a jucat azi sau ieri un meci oficial fără cronică, scrie cronica, coperta și scorul în acest depozit. Site-ul povestilestiintei.ro le preia singur (cronica ca ciornă, scorul direct în meci).

## Pași
1. **A jucat Craiova?** Caută pe web (ora României) meciurile oficiale ale Universității Craiova de azi și de ieri (Sofascore, LPF, GSP). Amicalele nu contează.
2. **Există deja?** Pentru fiecare meci terminat, dacă `cronici/<AAAA-LL-ZZ>-*.json` există pentru data lui → sari peste el. Dacă meciul de azi s-a terminat prea târziu și sursele sunt încă sărace, lasă-l pe mâine-seară (va fi „ieri”). Nicio cronică de scris → treci direct la pasul 6 (rezumatele video), apoi la pasul 7 (știrile).
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
     Doar la meciurile de **SuperLiga**, adaugă în `meci` și `"statistici"`, luate de la LPF: pe `https://lpf.ro/cluburi/universitatea-craiova/9/rezultate` găsește butonul „Statistici” al meciului (`https://lpf.ro/statistici/<nr>`) și copiază toate rândurile, ca `[["Posesia mingii", "54%", "46%"], ["Șuturi", "17", "8"], …]`, gazdele primele (cum le dă LPF). Dacă pagina nu există încă, lasă câmpul deoparte.
     La meciurile din **cupele europene**, statisticile vin de la UEFA: găsește id-ul meciului în `https://match.uefa.com/v5/matches?seasonYear=<anul de final al sezonului, ex. 2027>&competitionId=<1 Liga Campionilor | 14 Europa League | 2019 Conference League>&limit=100&offset=0&order=ASC`, apoi ia valorile din `https://matchstats.uefa.com/v2/team-statistics/<id>` (gazdele = `homeTeam.id` din `https://match.uefa.com/v5/matches/<id>`). Folosește aceleași denumiri: Posesia mingii (`ball_possession` + „%”), Șuturi (`attempts`), Șuturi pe poartă (`attempts_on_target`), Atacuri (`attacks`), Total pase (`passes_attempted`), Pase precise (`passes_completed`), Cornere (`corners`), Ofsaiduri (`offsides`), Parade (`saves`), Faulturi (`fouls_committed`), Cartonașe galbene (`yellow_cards`), Cartonașe roșii (`red_cards`), și pune `"sursa_statistici": "UEFA"` (la LPF: `"LPF"`). Verifică întâi că `goals` din statistici dă scorul.
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
7. **Știrile zilei.** Prima sursă e Google News, care adună toate publicațiile (GSP, Fanatik, Golazo, ProSport, Digi Sport, Antena Sport, Gazeta de Sud etc.): `curl -s "https://news.google.com/rss/search?q=Universitatea+Craiova+when:3d&hl=ro&gl=RO&ceid=RO:ro"` (repetă cu `Coelho+Craiova`, numele jucătorilor din știrile zilei). Linkurile `news.google.com/rss/articles/...` se transformă în adresa reală cu `python3 -I unelte/gndecode.py <link>`, iar textul articolului se scoate cu `python3 -I unelte/citeste.py <url>`. Apoi completează cu fluxurile RSS (GSP `https://www.gsp.ro/rss.xml`, Sport.ro `https://www.sport.ro/rss`, ProSport `https://www.prosport.ro/feed`, Fanatik `https://www.fanatik.ro/feed`, Digi Sport `https://www.digisport.ro/rss`, Digi24 `https://www.digi24.ro/rss/stiri/sport`, Gândul `https://www.gandul.ro/sport/feed`): filtrează titlurile despre Craiova, jucătorii, staff-ul și conducerea, apoi citește articolele cu `curl`. Include declarațiile de după meciuri, opiniile conducerii și ale foștilor jucători sau comentatorilor (rezumate, cu numele autorului, citate scurte). Caută apoi și pe web știrile despre Universitatea Craiova apărute în ultimele 48 de ore (GSP, ProSport, Sport.ro, Digi Sport, Fanatik, Flashscore/Soccerway, Gazeta de Sud, Jurnalul Olteniei, site-ul clubului ucv1948.ro, LPF, UEFA): transferuri, accidentări, declarații, jucători, staff, academie, suporteri, programul următoarelor meciuri.
   - **Grupează pe subiecte.** Mai multe articole despre același lucru → un singur articol al nostru, care le adună.
   - **Scrie un articol pentru fiecare subiect** care are fapte confirmate în cel puțin două surse, după secțiunea „Știri” din `STIL.md`: câte subiecte reale există (la rutina orară, de obicei 0–2). Zvonurile nesigure, meciurile deja acoperite de cronică și subiectele fără două surse nu se scriu.
   - **Evidența surselor:** `presa/vazute.json` = `{ "<url sursa>": "<id-ul stirii noastre sau „ignorat”>" }`. Înainte de a citi un articol, verifică dacă URL-ul e deja acolo; după ce l-ai folosit sau ai decis să-l ignori, adaugă-l. Așa rutina orară nu tratează de două ori același articol.
   - **Nu repeta.** Citește titlurile și rezumatele știrilor noastre din ultimele 10 zile (`cronici/*-stire-*.json`). Dacă subiectul a fost deja tratat, scrii doar dacă există o noutate reală și o spui clar în titlu.
   - **Fișierele:** `cronici/<AAAA-LL-ZZ>-stire-<subiect-fara-diacritice>.json` cu `id`, `titlu`, `rezumat`, `continut` (HTML, cu „Surse” la final), `"categorie": "Știri"`, `etichete`, `"imagine": "<id>.jpg"`, `"data_publicare": "AAAA-LL-ZZ hh:mm"` (ora evenimentului sau a primei surse, niciodată în viitor), `"anunt": false`. Coperta: `cronici/<id>.coperta.json` = `{ "titlu", "rubrica", "data" }` (rubrica: Știri din club, Transferuri, Jucătorii noștri, Academie, Conference League, SuperLiga, Cupa României…), apoi `node unelte/coperta-stire.js cronici/<id>.coperta.json cronici/<id>.jpg`. Uită-te la copertă înainte de commit.
8. **`index.json`** – adaugă fiecare fișier nou (`cronici/<id>.json`, `cronici/<id>-video.json`, știrile) la începutul listei `cronici` (păstrează maximum 120). Dacă n-ai scris nimic nou (nici cronică, nici video, nici știre) → oprește-te fără commit.
9. **Commit și push** pe `main`, mesaj: `Cronica: <gazde> – <oaspeti> <scor>` (sau `Rezumat video: …` / `Stiri: <subiecte>` dacă e doar video sau doar știri).
10. **Raport** scurt: scorul, titlul, știrile scrise, sursele. Dacă faptele n-au putut fi confirmate din două surse, spune-o și nu face commit.


## Rutina orară de știri

Rutina rulează pe Mac Studio (vezi `mac/README.md`): `mac/verifica.py` verifică fără AI, în fiecare oră, dacă au apărut articole noi și pornește Claude Code numai atunci, cu lista în `.stare-mac/candidati.json`. O sesiune pornește doar pentru știri (pasul 7), fără cronici și video (acelea rămân la rutina de noapte):

1. Google News cu `when:1d` pentru `Universitatea+Craiova`, `Coelho+Craiova`, `Stiinta+Craiova`, plus fluxurile RSS. Păstrează doar articolele din ultimele 3 ore care nu sunt în `presa/vazute.json`.
2. Dacă nu există nimic nou despre Craiova → adaugă URL-urile verificate în `presa/vazute.json` doar dacă ai decis ceva despre ele, altfel oprește-te fără commit.
3. Dacă există un subiect nou confirmat de două surse (sau o declarație oficială a clubului, a antrenorului ori a unui jucător, apărută în două publicații) → scrie știrea după `STIL.md`, cu textul construit de la zero: altă structură, alt unghi, alt titlu decât sursele, faptele reformulate, doar citate scurte și atribuite. Nu copia fraze din surse.
4. Articolele se publică direct pe site (importul rulează la 15 minute), deci verifică încă o dată numele, cifrele, datele și zilele săptămânii înainte de commit.
5. Raportul de final începe cu titlul știrii publicate (pentru notificare), sau cu „Nimic nou” dacă n-ai scris nimic.
