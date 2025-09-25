# MI-támogatott Sudoku-megoldó specifikáció

## 1. Projektáttekintés
- **Kontextus:** 2025 őszi vállalati csapatépítő, amely az MI-vel támogatott programozásra fókuszál.
- **Cél:** Olyan alkalmazás vagy algoritmus szállítása, amely bármilyen szabványos 9×9-es Sudoku táblát gyorsan és hibátlanul megold.
- **Csapatösszetétel:** 3–4 fő, akik elsődlegesen MI-eszközökre támaszkodnak a fejlesztés során.
- **Elsődleges sikerkritériumok:** Működő megoldó demonstrációja, MI-first munkafolyamat betartása, tanulságok és eredmények professzionális bemutatása.

## 2. Terjedelem
- **Terjedelembe tartozik:**
  - Sudoku-feldolgozó mag (input validáció, megoldás, opcionális egyértelműség-ellenőrzés).
  - Felhasználói felület (CLI és/vagy web UI) a feladványok betöltésére és a megoldások megjelenítésére.
  - REST API végpont a programozott puzzle-megoldáshoz (opcionális, de ajánlott a demó rugalmassága érdekében).
  - Fejlesztési feladatok MI-asszisztensekkel történő automatizálása (kódgenerálás, refaktorálás, dokumentálás).
  - A délután érkező változtatási igény lekezelése és integrálása.
  - Architektúra, MI-használat és visszatekintés dokumentálása a záró prezentációhoz.
- **Terjedelmen kívül esik:**
  - Nem Sudoku jellegű rejtvények.
  - Többjátékos vagy verseny jellegű funkciók.
  - Tartós adattárolás az ideiglenes memórián vagy lokális fájlokon túl.
  - Fejlett felhasználókezelés vagy autentikáció.

## 3. Érintettek
- **Csapattagok:** Fejlesztők, akik MI-eszközökkel terveznek, kódolnak és tesztelnek.
- **Facilitátorok:** Szervezők, akik figyelik a státuszjelentéseket és kiadják a változtatási igényt.
- **Hallgatóság:** Kollégák, akik részt vesznek a záró bemutatón.

## 4. Funkcionális követelmények
1. **Feladvány-beolvasás:**
   - Fogadjon 9×9-es Sudoku táblákat fájlfeltöltésből, beillesztett szövegből vagy kézi űrlapkitöltésből.
   - Ellenőrizze, hogy minden sor, oszlop és 3×3-as blokk csak 1–9 számjegyeket vagy üres mezőket tartalmazzon.
2. **Feladvány megoldása:**
   - Bármely megoldható feladványra másodperceken belül adjon ki legalább egy helyes megoldást standard laptopon.
   - Hibás vagy megoldhatatlan feladvány esetén adjon vissza magyarázó hibaüzenetet.
3. **Opcionális egyértelműség-vizsgálat:** Kérésre jelezze, hogy a feladványnak van-e egyedi megoldása.
4. **Interfészek:**
   - **CLI:** Parancsok fájlból/stdinből való megoldáshoz és a megoldások többféle formátumban való megjelenítéséhez.
   - **Web UI:** Reszponzív rácsos űrlap validációval, Solve/Reset gombokkal és példafeladvány betöltésével.
   - **API (opcionális):** `POST /api/solve` végpont, amely JSON mátrixot fogad és megoldást, valamint egyértelműségi zászlót ad vissza.
5. **Változtatási igény kezelése:** A nap folyamán érkező módosítást rövid időn belül elemezni, megvalósítani és bemutatni.
6. **Státuszjelentés:** Minden műhelyszakasz végén (pl. specifikáció, MVP, változtatás utáni állapot) megosztani az aktuális állapotot.

## 5. Nem-funkcionális követelmények
- **Teljesítmény:** Átlagos megoldási idő <500 ms tipikus feladványokra; legfeljebb 2 s a legnehezebb esetekre.
- **Megbízhatóság:** Determinisztikus működés helyes Sudoku rácsokkal; automatizált tesztek a magfunkciókra és interfészekre.
- **Használhatóság:** Egyszerű, érthető felület és hibaüzenetek.
- **Karbantarthatóság:** Moduláris kód, MI által generált dokumentáció, automatizált lint és teszt futtatás.
- **Megfelelés:** MI-first fejlesztési elv követése és az MI-hozzájárulások dokumentálása.

## 6. Korlátok és feltételezések
- Elsődlegesen MI-asszisztenseket (chat, IDE plugin) kell használni ötletelésre, kódolásra, hibakeresésre.
- Lehetőség van kevésbé ismert technológiák kipróbálására (pl. Python, alternatív JS keretrendszer), ha az MI támogatja.
- A fejlesztési idő a meghatározott idősávokra korlátozódik: 10:30–12:00, 13:00–14:00, 16:30–17:30, majd záró demó.
- Elérhető internet az MI-eszközökhöz és a közös tárhelyekhez (Google Drive, GitHub, GitLab).

## 7. Megoldás architektúrája
- **Magmodul:** Feldolgozás, validáció és megoldó algoritmus (pl. backtracking heurisztikákkal vagy constraint propagationnal).
- **Interfész réteg:**
  - CLI szkript a magmodul köré építve.
  - Webszerver (Flask/FastAPI/Node) API végponttal és felületkiszolgálással.
- **Frontend:** HTML/CSS/JS vagy választott keretrendszer a rácskezeléshez és API-hívásokhoz.
- **Tesztelés:** Automata unit- és integrációs tesztek a megoldóhoz, parserhez, API-hoz.
- **MI-munkafolyamat:** Dokumentált promptok, generált kódrészletek, felülvizsgálati pontok.
- **Változáskezelés:** Branch-ek vagy konfigurációk a késői igény integrálására regressziók nélkül.

## 8. MI-használati terv
1. **Ismeretszerzés:** Sudoku algoritmusok, technológiák, új fogalmak tisztázása MI segítségével.
2. **Tervezés:** Architektúra, adatáramlás, user storyk közös kidolgozása MI-vel.
3. **Implementáció:** Boilerplate, megoldó logika, UI komponensek és tesztek generáltatása MI-eszközökkel.
4. **Hibakeresés:** MI bevonása hibák azonosításához, javításokhoz, teljesítmény-tuninghoz.
5. **Dokumentáció & prezentáció:** Felhasználói útmutató, telepítési lépések, záró prezentáció tartalmának megíratása MI-vel.
6. **Változtatási igény:** MI bevonása a követelmény értelmezésébe, a design frissítésébe és a gyors implementációba.

## 9. Megvalósítási ütemterv
| Fázis | Idősáv | Tevékenységek | Eredmények |
|-------|--------|---------------|------------|
| Indítás | 10:30–11:00 | Scope egyeztetés, MI-források összegyűjtése, kollaborációs eszközök beállítása | Megosztott repo/drive, prompt sablonok |
| Tervezés | 11:00–12:00 | Architektúra, adatfolyam, UI vázlatok kidolgozása MI-vel | Specifikáció (jelen dokumentum), backlog |
| Építés 1 | 13:00–14:00 | Megoldó mag + alap interfész implementálása MI támogatással | Futó MVP, kezdeti tesztek |
| Építés 2 | 16:30–17:00 | Funkciók erősítése, UX javítása, tesztek bővítése, változtatásra készülés | Fejlettebb alkalmazás, tesztlefedettség |
| Változtatási igény | 17:00–17:20 | Új követelmény elemzése és implementálása | Frissített alkalmazás, módosítási jegyzet |
| Zárás | 17:20–17:30 | Demóanyagok előkészítése, próba, tanulságok összegyűjtése | Demóforgatókönyv, prezentáció |
| Demó & retro | 17:30–19:00 | Megoldás bemutatása, MI-élmények megosztása, visszajelzések gyűjtése | Élő demó, összegzés |

## 10. Tesztelés és validáció
- Unit tesztek a megoldó helyességére és a validációra.
- Integrációs tesztek a CLI, API és UI folyamatokra.
- Benchmark szkript a különböző nehézségi szintek futási idejének méréséhez.
- Manuális teszt a változtatási igényre és a hibakezelésre.
- Folyamatos tesztelés `make` vagy CI folyamaton keresztül a regressziók elkerülésére.

## 11. Telepítés és eszközök
- Lokális futtatás Python virtuális környezetben vagy a választott stack futtatókörnyezetében.
- Opcionális konténerizáció a konzisztens demó érdekében.
- Verziókezelés Git-tel; branch-ek és pull requestek használata a változtatás integrálásához.
- Megosztott artefaktumok tárolása Google Drive-on/GitHubon a facilitátorok iránymutatása szerint.

## 12. Jelentések és dokumentáció
- Minden idősáv végén friss állapot, akadályok és következő lépések rögzítése közös csatornán vagy dokumentumban.
- Changelog vezetése az MI által létrehozott főbb hozzájárulásokról és a manuális korrekciókról.
- Záró prezentáció előkészítése, amely összefoglalja a célt, a megoldást, az MI-ből származó tanulságokat és a jövőbeli ötleteket.

## 13. Kockázatok és mitigáció
| Kockázat | Hatás | Mitigáció |
|---------|-------|-----------|
| Ismeretlen technológia túlzott használata | Késések beállítási problémák miatt | MI-vel előzetesen validálni a megvalósíthatóságot, tartalék stack készenlétben |
| MI által generált kód minőségi hibái | Bugok, nehezen karbantartható kód | MI kimenetek review-ja, tesztek és lint futtatása |
| Változtatási igény túlnövése | Határidő csúszása | Elemzés időkeretezése, minimálisan szükséges megoldás egyeztetése |
| Korlátozott MI-hozzáférés | Produktivitás visszaesése | Több MI-eszköz, alternatív hozzáférések előkészítése |
| Csapatkoordináció hiányosságai | Dupla munka vagy merge konfliktus | Gyakori szinkron, egyértelmű felelősségek, közös backlog |

## 14. Átadás-átvételi feltételek
- Sudoku feladványok helyes megoldása a teljesítménykövetelmények mellett.
- Interfészek zökkenőmentes bevitel-ellenőrzést és megoldás-megjelenítést nyújtanak.
- A változtatási igény implementálva és bemutatva a demón.
- MI-használat és projektkimenetek dokumentálva.
- Pozitív visszajelzés a záró prezentáción (átláthatóság, funkcionalitás, tanulságok).

