# Fișele jucătorilor-cheie, scrise de la zero din cel puțin două surse
# (pagina de legende/istoric a clubului, Wikipedia ro/en, loturile oficiale).
# Cifrele apar doar când sursele se potrivesc.
L = []
def f(ep, nume, post, ani, text, cifre='', porecla='', rol='jucător'):
    L.append(dict(epoca=ep, nume=nume, post=post, ani=ani, text=text, cifre=cifre, porecla=porecla, rol=rol))

# 1. PIONIERII (1948–1964)
f(1,'N. Polojinski','Antrenor','1948',
  'Primul antrenor din istoria clubului. A condus echipa studenților în primul meci oficial, pe 5 septembrie 1948, la Filiași. Știința a pierdut cu 6-3, dar în acea zi tricoul alb-albastru a intrat pentru prima dată pe un teren de fotbal.', rol='antrenor')
f(1,'Nicolae Oțeleanu','Antrenor','1954, 1963–1964',
  'Antrenorul celor două promovări care au construit drumul clubului. În 1954, la turneul de baraj de la Arad, a dus Știința din Divizia C în B. Un deceniu mai târziu a revenit pe bancă și a obținut, în sezonul 1963–1964, promovarea în prima divizie, unde echipa avea să rămână 41 de ani la rând. Înainte de a fi antrenor, fusese unul dintre fotbaliștii valoroși ai anilor interbelici, la Sparta, Sportul Studențesc și Sporting Chișinău.', rol='antrenor')
f(1,'Ionescu Crum','Antrenor','1958',
  'Antrenorul care a readus Știința în Divizia B, pe 6 iulie 1958. Promovarea s-a decis la mustață, după o luptă cu Unirea Râmnicu Vâlcea, încheiată la egalitate de puncte și tranșată de rezultatele directe.', rol='antrenor')
f(1,'Constantin Deliu','Jucător, apoi antrenor','1963–1964 (jucător)',
  'Component al lotului care a urcat Știința în Divizia A în 1964. Legătura lui cu clubul n-a încetat odată cu retragerea: în 1978, alături de Ilie Oană, a pregătit echipa care a câștigat a doua Cupă a României din istorie, 3-1 în finala cu Olimpia Satu Mare.')
f(1,'Ion Papuc','Portar','anii ’60',
  'Portarul lotului promovării din 1964, primul nume trecut în lista „actului istoric” care a dus Știința în prima divizie. Apare în galeria portarilor importanți ai clubului, alături de nume precum Silviu Lung și Gabriel Boldici.')

# 2. GENERAȚIA PRIMULUI TITLU (1964–1974)
f(2,'Ion Oblemenco','Atacant','1966–1977',
  'Omul al cărui nume îl poartă astăzi stadionul. Născut la Corabia, a fost de patru ori golgheterul campionatului, cu un șut atât de puternic încât tribuna l-a numit „Tunarul din Bănie”. A câștigat cu Știința titlul din 1974 și Cupa României din 1977, iar ca antrenor a fost pe banca titlurilor din 1980 și 1981. Paradoxul carierei lui: deși a fost unul dintre cei mai prolifici marcatori din istoria primei divizii, nu a primit niciodată o selecție în echipa națională. A murit în 1996.',
  cifre='264 de meciuri și 167 de goluri în Divizia A pentru Știința', porecla='Tunarul din Bănie')
f(2,'Petre Deselnicu','Fundaș','1964–1976',
  'Craiovean din Mofleni, format la CS Craiova, a fost unul dintre stâlpii echipei construite de Constantin Cernăianu. A jucat 12 ani pentru Știința, a fost campion al României în 1974 și campion mondial universitar. Prieten nedespărțit al lui Oblemenco, după retragere a rămas în fotbalul craiovean ca oficial. A murit în 2003.',
  cifre='246 de meciuri și 12 goluri în Divizia A')
f(2,'Theodor Țarălungă','Extremă','din 1970',
  'Venit la Craiova în 1970, convins de prietenul lui, Ion Oblemenco, a devenit repede unul dintre idolii tribunei. Mulți dintre cei care l-au văzut jucând îl consideră una dintre cele mai bune extreme din fotbalul românesc. A fost campion în 1974 și a jucat pentru echipa națională.')
f(2,'Dumitru Marcu','Extremă stânga','1972–1980',
  'Supranumit „Motoreta” pentru viteza lui, a închis atacul de legendă Țarălungă – Oblemenco – Bălan – Marcu. Venit de la Steaua în 1972, a câștigat cu Știința titlurile din 1974 și 1980 și două Cupe ale României, fiind și internațional.',
  porecla='Motoreta')
f(2,'Ion Niță','Atacant / mijlocaș ofensiv','anii ’70',
  'Născut în 1948, chiar în anul înființării clubului, a făcut parte din echipa care a adus în Bănie primul titlu de campioană, în sezonul 1973–1974. După Craiova a evoluat la Steagul Roșu Brașov.')
f(2,'Dragu Bădin','Fundaș','anii ’70',
  'Unul dintre fundașii echipei campioane din 1974, primul trofeu din istoria clubului. Numele lui apare în lotul „eroilor din teren” trecut de club în istoria oficială a primului titlu.')
f(2,'Alexandru Boc','Fundaș','1973–1976',
  'Fundaș venit cu experiența unui titlu câștigat la Petrolul, a fost campion și cu Știința în 1974. A fost și internațional.')
f(2,'Paul Manta','Portar','1972–1974',
  'Portar format în fotbalul bucureștean, la Sportul Studențesc și Progresul, a apărat poarta Științei în sezonul primului titlu, alături de Oprea.')
f(2,'Constantin Cernăianu și Constantin Oțet','Antrenori','1973–1974',
  'Cuplul de antrenori al primului titlu. Cernăianu a construit echipa în jurul lui Oblemenco și Deselnicu, iar Oțet, secund în acel sezon, avea să devină un deceniu mai târziu antrenorul semifinalei Cupei UEFA. Universitatea a devenit atunci prima echipă studențească din țară campioană națională.', rol='antrenor')

# 3. CRAIOVA MAXIMA (1975–1985)
f(3,'Ilie Balaci','Mijlocaș ofensiv','1973–1984',
  'Pentru mulți, cel mai mare fotbalist român. Născut la Bistreț, a debutat pentru Știința la 16 ani și a devenit creierul Craiovei Maxima, cu o tehnică și o viziune rar întâlnite. A câștigat trei titluri (1974, 1980, 1981) și patru Cupe ale României și a condus echipa în sferturile Cupei Campionilor și în semifinala Cupei UEFA din 1983. Două accidentări grave i-au scurtat cariera. A murit în 2018.',
  cifre='285 de meciuri și 76 de goluri în Divizia A · 65 de selecții', porecla='Minunea Blondă')
f(3,'Rodion Cămătaru','Atacant','1974–1986',
  'Venit de la Progresul Strehaia în 1974, a rămas 12 sezoane la Craiova și a câștigat tot ce se putea câștiga în țară: titlurile din 1980 și 1981 și Cupele din 1977, 1978, 1981 și 1983. A jucat la EURO 1984 și la Mondialul din 1990. Revista franceză Onze l-a trecut în 1983 printre primii zece atacanți ai Europei.',
  cifre='288 de meciuri și 122 de goluri în Divizia A · 75 de selecții', porecla='Cami')
f(3,'Costică Ștefănescu','Fundaș central, căpitan','1973–1986',
  'Venit de la Steaua în 1973, a câștigat titlul chiar din primul sezon. A fost căpitanul Științei mai bine de un deceniu, în anii de vârf ai Maximei, și căpitan al naționalei. Eleganța și calmul lui i-au adus porecla de „Ministrul Apărării”, iar în 1983 a fost nominalizat la Balonul de Aur. Este recordmanul clubului la meciuri jucate. A murit în 2013.',
  cifre='378 de meciuri în Divizia A pentru Știința, record al clubului', porecla='Ministrul Apărării')
f(3,'Silviu Lung','Portar','1974–1988, 1993–1994',
  'Adus de la Victoria Carei, a apărat poarta Științei 14 sezoane, cu două titluri și patru Cupe ale României. A fost portarul naționalei la EURO 1984 și a făcut parte din lotul de la Mondialul din 1990. În 1984 a fost desemnat fotbalistul român al anului. Fiul lui, Silviu Lung Jr., a apărat și el poarta Craiovei.')
f(3,'Gabriel Boldici','Portar','până în 1985, 1988–1993',
  'Crescut la Universitate de la copii la seniori, a debutat în echipa mare la 19 ani. Rivalitatea lui cu Silviu Lung pentru postul de titular a fost una dintre cele mai frumoase din fotbalul românesc. A apărat în finalele de Cupă din 1977 și 1978 și a fost campion atât cu Maxima (1980, 1981), cât și cu generația eventului din 1991.',
  cifre='152 de meciuri în Divizia A pentru Știința (Wikipedia)')
f(3,'Nicolae Negrilă','Fundaș dreapta','1973–1988',
  'A debutat chiar în meciul care a adus primul titlu, 0-0 la Ploiești, în 1974. Pe 16 martie 1983 a marcat golul cu FC Kaiserslautern care a dus Știința, prima echipă românească, în semifinalele Cupei UEFA. A jucat la EURO 1984 și a câștigat trei titluri și patru Cupe; în 1991 a mai adăugat eventul ca antrenor secund.',
  cifre='28 de selecții', porecla='Negoro')
f(3,'Nicolae Tilihoi','Fundaș central','1976–1987',
  'Brăileanul descoperit la un trial în București și adus la Craiova a format, timp de peste un deceniu, cuplul de fundași centrali cu Costică Ștefănescu. A câștigat două titluri și patru Cupe ale României, iar tribuna l-a numit „fundașul de fier” al Craiovei.')
f(3,'Nicolae Ungureanu','Fundaș stânga','1977–1987',
  'Format la CSȘ Craiova, a jucat toate meciurile din cele două sezoane de titlu, 1979–1980 și 1980–1981. Celebrele lui incursiuni din banda stângă spre interior erau cunoscute de toți adversarii, dar puțini le puteau opri. A fost la EURO 1984 cu naționala.', porecla='Roșu')
f(3,'Aurel Țicleanu','Mijlocaș dreapta','1976–1985',
  'A debutat la 17 ani și a devenit rapid un punct fix al Maximei, cu o capacitate de efort ieșită din comun. Practic nu a avut rival pe postul lui. A câștigat două titluri și patru Cupe ale României, a jucat în semifinala Cupei UEFA din 1983 și la EURO 1984.',
  cifre='232 de meciuri și 10 goluri în Divizia A · 44 de selecții')
f(3,'Aurică Beldeanu','Mijlocaș central','1976–1985',
  'Venit de la CSM Reșița în 1976, a jucat nouă ani pentru Știința, cu două titluri și patru Cupe ale României. Numele lui e legat de una dintre cele mai mari victorii românești în Europa, eliminarea lui Leeds United, cu un șut care a intrat la vinclu și a rămas în memoria tribunei.')
f(3,'Costică Donose','Mijlocaș central','anii ’70–’80',
  'Supranumit „Pele al Craiovei”, a fost unul dintre motoarele Maximei: titlurile din 1980 și 1981 și Cupele din 1977, 1978, 1981 și 1983. La fel ca Oblemenco, nu a prins naționala mare, deși a jucat zeci de meciuri la juniori și la olimpică. În 2003 a devenit Cetățean de Onoare al Craiovei.', porecla='Pele al Craiovei')
f(3,'Zoltan Crișan','Atacant','1974–1984',
  'Adus de la Minerul Baia Mare, a debutat în prima ligă la Craiova și a jucat zece sezoane în alb-albastru, cu două titluri și patru Cupe. Cel mai dureros moment al carierei lui a fost și unul dintre cele mai cunoscute: pe 20 aprilie 1983, cu Benfica, șutul lui a lovit bara în minutul 78, la un pas de finala Cupei UEFA. A murit în 2003, la 48 de ani.')
f(3,'Ion Geolgău','Mijlocaș','1976–1990',
  'Golul lui de la Bratislava a calificat România la EURO 1984, într-o grupă cu campioana mondială Italia, iar Centralul l-a cântat ani la rând: „Din Pielești la Bratislava…”. Tot el a marcat în prelungiri golul cu Bordeaux care a dus Știința mai departe în Europa. După retragere a rămas la club ca antrenor secund.')
f(3,'Mircea Irimescu','Mijlocaș / fundaș','1976–1990',
  'Craiovean, „jolly-jokerul” Maximei: putea juca mijlocaș central, fundaș central sau pe toată banda stângă, din apărare până în atac, cu un șut cu stângul de temut. A jucat 14 sezoane pentru Știința și a fost la EURO 1984.',
  cifre='318 de meciuri și 62 de goluri în Divizia A')
f(3,'Sorin Cârțu','Atacant, apoi antrenor','1976–1987',
  'Produs al școlii craiovene, a debutat cu gol pe 22 august 1976, într-un 5-1 cu Progresul. A câștigat ca jucător titluri și Cupe ale României cu Știința, iar în 1991, ca antrenor, a adus eventul. Astăzi este președinte de onoare al clubului.', porecla='Sorinaccio')
f(3,'Adrian Bumbescu','Fundaș central','1978–1980',
  'Craiovean, și-a semnat primul contract cu Universitatea în 1978 și a câștigat aici primul din cele șapte titluri ale carierei. Este singurul fotbalist campion al României cu trei echipe diferite; cu Steaua a câștigat Cupa Campionilor Europeni în 1986.')
f(3,'Constantin Oțet','Antrenor','1981–1984',
  'Antrenorul celei mai mari performanțe europene din istoria clubului: semifinala Cupei UEFA din 1983, cu Benfica. Fusese în staff-ul Științei încă din 1968, secund la primul titlu, în 1974, și secundul lui Ion Oblemenco la titlul din 1981.', rol='antrenor')

# 4. GENERAȚIA DE TRANZIȚIE (1985–1990)
f(4,'Gheorghe Popescu','Fundaș central / mijlocaș','1984–1987, 1988–1990',
  'Născut la Calafat, a făcut primii pași în fotbalul mare la Craiova, a trecut scurt pe la Steaua și s-a întors la Știința înainte de Mondialul din 1990. A urmat o carieră uriașă: PSV, Tottenham, Barcelona, unde a fost căpitan și a câștigat Cupa Cupelor, și Galatasaray, cu care a câștigat Cupa UEFA în 2000.',
  cifre='115 selecții', porecla='Baciul')
f(4,'Pavel Badea','Mijlocaș','1983–1992, 1996, 2002–2004',
  'Unul dintre cele mai mari talente ale școlii craiovene. A debutat la seniori la 16 ani, iar la 20 era deja un om de bază. După Craiova a jucat în Elveția, Coreea de Sud și Japonia, apoi s-a întors acasă și a jucat până la 37 de ani. A fost și antrenor, și președinte al clubului.',
  cifre='258 de meciuri și 52 de goluri în Divizia A', porecla='Bădiță')
f(4,'Emil Săndoi','Fundaș','1983–1999',
  'Produs al școlii craiovene, a debutat în 1983, când în vestiar legea o făceau încă marii jucători ai Maximei, și a rămas legat de Știința până în 1999. A fost în lotul României la Mondialul din 1990 și a câștigat eventul din 1991.')
f(4,'Adrian Popescu','Fundaș dreapta, căpitan','1980–1992, 1995–1996',
  'Craiovean, a debutat la 20 de ani într-un lot dominat de Maxima și și-a câștigat, pas cu pas, locul de titular. A fost căpitanul echipei care a câștigat eventul din 1991 și a jucat la Mondialul din 1990.')
f(4,'Eugen Neagoe','Atacant','1986–1994, 1999–2000',
  'Atacant central masiv, dar cu o tehnică foarte bună, a debutat la 19 ani și a rămas la Știința până în 1994, cu două Cupe ale României câștigate. A jucat apoi în Ungaria, Cipru și Grecia și a revenit acasă spre finalul carierei. Ca antrenor, a pregătit Craiova și a fost secundul lui Victor Pițurcă la națională.', porecla='Geană')
f(4,'Ștefan Stoica','Atacant','1986–1990, 1994',
  'Oltean, a debutat la Universitate în 1986 și a plecat în Grecia la finalul lui 1990, unde a jucat aproape un deceniu, la Larissa și Veria. A avut și selecții în echipa națională, iar după retragere a devenit antrenor.')
f(4,'Vasile Mănăilă','Fundaș','1984–1991',
  'Fundaș de bază al anilor de tranziție, a fost unul dintre jucătorii care au făcut legătura dintre Maxima și generația eventului. Numele lui apare în lotul campion și câștigător al Cupei din 1991.')
f(4,'Dănuț Bică','Mijlocaș','sfârșitul anilor ’80',
  'Mijlocaș al anilor de tranziție, a rămas la Craiova până la marea recoltă din 1991, când a câștigat eventul cu Știința. A mai jucat în prima ligă la Sportul Studențesc.')

# 5. GENERAȚIA EVENTULUI (1990–1991)
f(5,'Florin Prunea','Portar','1990–1991, 1999–2000',
  'Venit de la Dinamo, a fost portarul sezonului perfect: în 1991 a câștigat cu Știința atât campionatul, cât și Cupa României. Mai târziu a jucat la două Campionate Mondiale (1994, 1998) și două Europene (1996, 2000).',
  cifre='40 de selecții')
f(5,'Silvian Cristescu','Mijlocaș, căpitan','1990–1998, 1999–2000',
  'Campion cu Craiova la juniori (1988), tineret (1991) și seniori (1991), a devenit căpitanul echipei din 1994. „Il Capitano” a strâns peste 230 de meciuri pentru Craiova și a rămas apoi aproape de club, ca director sportiv.', porecla='Il Capitano')
f(5,'Gheorghe Craioveanu','Atacant','1991–1995',
  'A venit la mijlocul sezonului 1990–1991, la timp pentru event, și a devenit unul dintre cei mai iubiți jucători ai tribunei. Golurile lui de la Craiova l-au dus în Spania, unde a jucat 11 ani la Real Sociedad, Villarreal și Getafe. A fost la Mondialul din 1998.',
  cifre='25 de selecții')
f(5,'Roland Agalliu','Atacant / mijlocaș ofensiv','1990–1992',
  'Albanezul care a scris o pagină de istorie: a fost unul dintre primii străini din campionatul României după 1989 și a câștigat eventul cu Știința în sezonul 1990–1991.')
f(5,'Dumitru Mitriță','Fundaș','1990, 1994–1997',
  'Campion cu Craiova la juniori, tineret și seniori, a debutat la 18 ani în echipa mare. După ani de rodaj la alte echipe a revenit la Știința, iar între 1997 și 2000 a fost titular la Heerenveen, în Olanda.')
f(5,'Adrian Pigulea','Atacant','1988–1995',
  'Atacant al generației eventului, prezent în lotul care a câștigat campionatul și Cupa României în 1991.')
f(5,'Ion Olaru','Mijlocaș','1988–1993',
  'Mijlocaș cu experiență, a fost unul dintre oamenii de echilibru ai echipei care a făcut eventul în 1991.')
f(5,'Gheorghe Ceaușilă','Atacant','1989–1991',
  'A jucat pentru Steaua, Dinamo și Craiova, unde a fost în lotul campion și câștigător al Cupei din 1991. A jucat și pentru echipa națională.')
f(5,'Sorin Cârțu și Ștefan Cioacă','Antrenori','1990–1991',
  'Antrenorii ultimului event din secolul XX. Cârțu, fost atacant al Maximei, a câștigat cu Știința campionatul și Cupa României în același sezon, la nici patru ani după retragere.', rol='antrenor')

# 6. GENERAȚIA ANILOR ’90 (1992–2000)
f(6,'Ovidiu Stângă','Mijlocaș','1990–1995, 2002–2004, 2005–2007',
  'Produs sută la sută al școlii craiovene, a debutat la 20 de ani și în echipa națională, cu care a jucat la Mondialele din 1994 și 1998 și la EURO 1996. A jucat peste hotare la PSV Eindhoven și Salamanca și s-a întors de două ori acasă. Mai târziu a fost și antrenorul Științei.')
f(6,'Corneliu Papură','Fundaș central / mijlocaș defensiv','1991–1996, 1999–2001, 2002–2004, 2005',
  'Fundaș de mare rafinament, a debutat în 1991, după titlurile câștigate la juniori și tineret. Cariera lui s-a întors mereu la Craiova, în patru perioade diferite, între experiențe la Rennes, Beitar Ierusalim și în China. A jucat la Mondialul din 1994.',
  cifre='226 de meciuri și 13 goluri în Divizia A · 12 selecții')
f(6,'Gabriel Popescu','Mijlocaș ofensiv','1994–1997, 2000–2001',
  'Craiovean, a trecut de la postul de fundaș dreapta la cel de mijlocaș de mare valoare. După Craiova a jucat în Spania, la Salamanca, Valencia și Numancia, și a fost la Mondialul din 1998.',
  cifre='101 meciuri și 16 goluri în Divizia A · 14 selecții', porecla='Gabi')
f(6,'Ionel Gane','Atacant','1988–1996, 2004, 2005–2006',
  'Și-a petrecut cea mai mare parte a carierei la Craiova și a jucat pentru echipa națională. După retragere a devenit antrenor, inclusiv secund la naționala României.', porecla='Jerry')
f(6,'Ionel Ganea','Atacant','1996–1998',
  'Doi ani la Craiova, cu 22 de goluri în 56 de meciuri, înainte de a deveni golgheterul campionatului în sezonul 1998–1999 și internațional la EURO 2000.',
  cifre='56 de meciuri și 22 de goluri în Divizia A')
f(6,'Cristian Chivu','Fundaș central','1998–1999',
  'A venit de la CSM Reșița în 1998 și a jucat un singur sezon la Craiova, suficient ca să fie remarcat de Ajax. A urmat o carieră de căpitan la Ajax, apoi Roma și Inter, cu care a câștigat Liga Campionilor.')
f(6,'Claudiu Niculescu','Atacant','1998–2001',
  'Atacant cu o execuție de temut la loviturile libere, „Lunetistul” a trecut prin Craiova înaintea anilor de glorie de la Dinamo. Este unul dintre cei mai prolifici marcatori din istoria primei ligi.', porecla='Lunetistul')
f(6,'Flavius Stoican','Fundaș dreapta','1995–2002',
  'Fundaș dreapta cu șapte sezoane în alb-albastru, unul dintre jucătorii constanți ai anilor ’90, devenit ulterior antrenor.')
f(6,'Marian Bondrea','Antrenor','1993',
  'Fost mijlocaș al Științei la începutul anilor ’70, a câștigat ca antrenor Cupa României din 1993, după 2-0 în finala cu Dacia Unirea Brăila.', rol='antrenor')

# 7. GENERAȚIA 2000–2010
f(7,'Mihăiță Pleșan','Mijlocaș central','2000–2005, 2013–2014',
  'Mijlocaș central al echipei anilor 2000, a ajuns de la Craiova până la echipa națională. A fost unul dintre jucătorii de bază ai primei jumătăți a deceniului.',
  cifre='95 de meciuri și 17 goluri în prima ligă')
f(7,'Gabriel Velcovici','Fundaș stânga','2003–2004, 2005–2008',
  'Fundaș stânga cu peste o sută de meciuri pentru Craiova în prima ligă, unul dintre jucătorii constanți ai unui deceniu dificil.',
  cifre='112 meciuri și 8 goluri în prima ligă')
f(7,'Robert Săceanu','Mijlocaș dreapta','2005–2009',
  'Născut la Corabia, ca Ion Oblemenco, a fost mijlocașul dreapta al echipei care a revenit în Liga I în 2006 și a luptat pentru Europa în sezonul 2008–2009.',
  cifre='77 de meciuri și 8 goluri în prima ligă')
f(7,'Michael Baird','Atacant','2006–2009',
  'Australianul venit din A-League a petrecut aproape patru ani la Craiova, unul dintre atacanții de bază ai echipei care a revenit în Liga I.',
  cifre='67 de meciuri și 18 goluri în prima ligă')
f(7,'Florin Costea','Atacant','2006–2011',
  'Atacant al Craiovei timp de cinci sezoane, în anii de după revenirea în Liga I din 2006.')
f(7,'Valerică Găman','Fundaș central','2006–2011',
  'Fundaș central al echipei în a doua jumătate a deceniului, a ajuns apoi la echipa națională, pentru care a jucat 15 meciuri.')
f(7,'Dorel Stoica','Mijlocaș, căpitan','2005–2009, 2010–2011',
  'A venit la Craiova odată cu revenirea în Liga I și a fost căpitanul echipei în acei ani. A jucat și pentru echipa națională, debutând într-un 3-0 cu Luxemburg.')
f(7,'Andrei Prepeliță','Mijlocaș defensiv','2007–2011',
  'Mijlocaș defensiv al ultimilor ani din deceniu, jucător de luptă al echipei, devenit ulterior antrenor.')
f(7,'Cosmin Moți','Fundaș central','2003–2005',
  'Și-a început cariera la Craiova, de unde a plecat în 2005 la Dinamo. A urmat o carieră lungă la Ludogoreț, cu șapte titluri consecutive în Bulgaria.')

# 8. GENERAȚIA MODERNĂ (2014–2026)
f(8,'Nicușor Bancu','Fundaș stânga / extremă, căpitan','2014–prezent',
  'Fața generației moderne. A venit în anul revenirii în Liga I și a rămas, devenind căpitanul echipei și internațional. A câștigat toate trofeele noii ere, de la Cupa din 2018 la eventul din 2026, și a jucat pentru România la EURO 2024.',
  cifre='peste 50 de selecții')
f(8,'Alexandru Mitriță','Mijlocaș ofensiv / extremă','2017–2019, 2023–2025',
  'Craiovean, s-a întors acasă din Italia în 2017 și a devenit titular indiscutabil. A câștigat Cupa României în 2018, iar evoluțiile lui l-au dus în MLS, la New York City FC. A revenit la Craiova pentru a doua perioadă.')
f(8,'Andrei Ivan','Atacant','2014–2017, 2019–2025',
  'A debutat la seniori la Craiova în 2014 și, după trei ani și jumătate, a fost transferat la Krasnodar. S-a întors în 2019 și a rămas un om important al echipei, internațional încă de la 18 ani.')
f(8,'Alexandru Cicâldău','Mijlocaș','2018–2021, 2024–prezent',
  'Venit de la Viitorul în 2018, a trecut de o sută de meciuri pentru Craiova și a câștigat două trofee înainte de transferul la Galatasaray, în 2021. Clubul l-a readus acasă în 2024.')
f(8,'Alexandru Mateiu','Mijlocaș','2014–2024',
  'Brașoveanul semnat în 2014 a devenit un simbol al constanței: un deceniu în alb-albastru și peste 270 de meciuri în prima ligă pentru Craiova.')
f(8,'Alexandru Băluță','Mijlocaș ofensiv','2014–2018',
  'Unul dintre tinerii talentați ai anilor revenirii în Liga I, mijlocaș ofensiv care putea juca și ca vârf.')
f(8,'Vladimir Screciu','Mijlocaș defensiv / fundaș central','2016–2018, 2020–prezent',
  'A ajuns la Craiova la 16 ani, iar după revenirea din 2020 a devenit un om de bază al echipei și jucător al naționalei.')
f(8,'Elvir Koljić','Atacant','2018–2025',
  'Bosniacul venit în 2018 a petrecut șapte ani la Craiova, unul dintre atacanții de bază ai perioadei.')
f(8,'Mirko Pigliacelli','Portar','2018, 2019–2022',
  'Portarul italian al perioadei 2019–2022, ani în care Craiova a câștigat Cupa României și Supercupa, în 2021.')
f(8,'Ștefan Baiaram','Extremă','2019–prezent',
  'Extremă adusă la Craiova la 16 ani, a devenit internațional și unul dintre jucătorii eventului din 2026.')
f(8,'Carlos Mora','Extremă / fundaș lateral','2024–prezent',
  'Costaricanul a adus viteză pe benzi și a jucat pentru naționala lui la Gold Cup 2025, ca jucător al Craiovei.')
f(8,'Anzor Mekvabishvili','Mijlocaș','2024–2026',
  'Georgianul a jucat pentru Georgia la EURO 2024 ca jucător al Craiovei și a fost unul dintre mijlocașii sezonului eventului.')
f(8,'Tudor Băluță','Mijlocaș defensiv','2025–prezent',
  'Internațional român, venit în 2025, a întărit mijlocul echipei care a câștigat titlul după 35 de ani.')
