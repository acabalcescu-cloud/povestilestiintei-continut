# Vocea cronicilor – Poveștile Științei

Blogul suporterilor Universității Craiova: „din tribună, cu inima”. Cronicile sunt scrise de un suporter, nu de o agenție.

## Ton
- Optimist și cald, ca suporter al Științei. „Noi”, „ai noștri”, „băieții noștri”, „echipa noastră”, „Știința”, „Craiova”, „alb-albaștrii” – niciodată ton neutru de agenție.
- **Nu folosim „oltenii”** (nici „oltenilor”) pentru jucători sau echipă: sună ca și cum am scrie despre alții. Cititorul e suporter și face parte din familia clubului, așa că scriem la persoana întâi plural: „am câștigat”, „băieții noștri”, „echipa noastră”, „tribuna noastră”. „Oltenia” (regiunea) rămâne.
- Optimismul nu ascunde faptele: o înfrângere sau o seară slabă se spune limpede, apoi se caută ce rămâne bun și ce urmează.
- Fără atacuri la adversari, arbitri sau jucători. Fără limbaj vulgar. Respect pentru adversar.
- Finalul privește înainte (următorul meci, clasamentul, ce e în joc) și se încheie cu „Hai Știința!”.

## Structură
1. **Titlu** – scurt, cu emoție, fără clickbait. Ex.: „Știința nu cedează niciodată: un punct smuls cu inima la Voluntari”.
2. **Linia de rezultat** (paragraf separat, bold): `Gazde – Oaspeți X-Y (pauză), Competiție, faza/etapa`.
3. **Deschidere** – 1-2 fraze despre ce a însemnat seara.
4. **Echipa de start** a Craiovei și contextul (rotații, absenți, poziția în clasament).
5. **Prima repriză** – ocazii, goluri, cu minute.
6. **A doua repriză** – schimbări importante, goluri, momente-cheie (VAR, bare, roșii).
7. **„De ce zâmbim totuși”** sau **„Ce înseamnă rezultatul”** – clasament, calcule, următorul meci.
8. **Încheiere** – o frază de tribună + „Hai Știința!”.

Lungime: 350–550 de cuvinte. Diacritice corecte (ș, ț cu virgulă).

## Fapte
- Scorul, marcatorii, minutele, echipele de start și arbitrul se verifică în cel puțin două surse (Sofascore, LPF, GSP, ProSport, Digi Sport, Jurnalul Olteniei, Gazeta de Sud, news.ro).
- Când sursele se contrazic, se scrie varianta sigură sau se omite detaliul. Nimic inventat.
- Textul e scris de la zero, cu cuvintele noastre – fără fraze copiate din articole.
- La final, în HTML, o listă scurtă „Surse” cu linkuri.

## Format HTML (`continut`)
Doar `<p>`, `<strong>`, `<em>`, `<h3>`, `<ul>/<li>`, `<a>`. Fără stiluri inline, fără imagini în text.

## Știri

Aceeași voce de suporter ca în cronici, dar despre ce se întâmplă între meciuri: transferuri, accidentări, jucători, staff, academie, Europa.

- **Scrise de la zero.** Faptele (nume, cifre, date, citate scurte și atribuite) se iau din surse; textul, ordinea ideilor și titlul sunt ale noastre. Nu se reformulează frază cu frază un articol-sursă și nu i se păstrează structura. Când mai multe surse tratează același subiect, le adunăm într-un singur articol.
- **Lungime: ținta e în jur de 1.000 de cuvinte (minimum 700), chiar mai mult dacă sursele o permit.** Lungimea vine numai din fapte verificabile (declarații complete, cifre, istoric, reacții din mai multe surse, context din cronicile noastre), niciodată din umplutură sau repetiții. Dacă subiectul e subțire, mai bine 700 de cuvinte solide decât 1.000 diluate. Pe lângă știrea propriu-zisă, articolul aduce context din ce știm deja: drumul jucătorului la Craiova, golurile și meciurile lui din sezon (din cronicile noastre), ce înseamnă vestea pentru echipă și ce urmează în calendar.
- **Structură:** titlu cu emoție, fără clickbait · 1–2 fraze de deschidere cu vestea · 2–4 secțiuni cu `<h3>` (ce s-a întâmplat, cine e omul/contextul, ce înseamnă pentru Știința) · încheiere care privește înainte și „Hai Știința!”.
- **Zvonuri:** se scriu doar dacă vin din cel puțin două surse serioase și se prezintă ca atare („potrivit presei”, „ar fi”), fără sume sau detalii neconfirmate.
- **Fără** atacuri la persoane, fără dispute personale sau juridice detaliate, fără referiri la disputa privind identitatea clubului.
- La final, `<p><em>Surse:</em> …</p>` cu linkuri la articolele folosite.

## Reguli comune (cronici și știri)

- **Titlurile de secțiune (`<h3>`)** sunt urmate întotdeauna de cel puțin un paragraf de text. Nu pune un titlu direct deasupra unei liste: introduci lista cu o frază sau renunți la titlu.
- **Cuvintele potrivite:** jucătorii noi sunt „veniri” sau „sosiri” (nu „venituri”); un atac cu mai mulți marcatori are „guri de foc” (nu „capete”). Recitește titlurile cu voce tare înainte de commit.
- **Legături interne.** Când revii pe un subiect deja tratat pe site, pune o legătură spre articolul nostru: `<a href="ps:<id>">text</a>`, unde `<id>` e numele fișierului din `cronici/` fără `.json` (ex.: `ps:2026-07-08-vitebsk-craiova`). Pentru pagina unui meci: `<a href="ps:meci:AAAA-LL-ZZ">text</a>`. Site-ul transformă singur aceste adrese în linkuri reale și le ignoră pe cele spre articole încă nepublicate. Verifică întâi că fișierul există.
- **Numele jucătorilor și ale staff-ului** nu se pun în legături de mână: site-ul leagă automat prima apariție a numelui complet („Prenume Nume” sau „Nume Prenume”) de pagina persoanei. De aceea, la prima pomenire a unui jucător scrie-i numele complet (ex.: „Simon Elisor”), apoi poți folosi doar numele de familie.
