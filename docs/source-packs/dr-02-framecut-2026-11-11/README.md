# DR-02 — profesjonalny montaż / FrameCut

Badanie wykonane **2026-11-11**. Resolve jest głównym punktem odniesienia; raport obejmuje także Premiere Pro, Final Cut Pro, Avid Media Composer, Pro Tools, Nuke, Baselight oraz narzędzia kodowe i wymianę timeline.

**Najważniejsza decyzja:** rozwijać istniejący FrameCut project v1 i jego właścicieli. Nowy schemat w pakiecie badawczym jest zewnętrznym RFC intencji, a nie zamiennikiem natywnego projektu ani wdrożoną funkcją.

## Czytanie

| Plik | Zawartość |
|---|---|
| [COMPREHENSIVE-REPORT](COMPREHENSIVE-REPORT.md) | Synteza całego badania i kolejność korzystania z części |
| [CRAFT](specialists/craft/CRAFT.md) | Dramaturgia, selekcja, rytm, gatunki, kontrprzykłady i granice automatyzacji |
| [GLOSSARY](specialists/craft/GLOSSARY.md) | **100 pojęć PL/EN**: definicja, przykład, zastosowanie i błąd |
| [RECIPES](specialists/craft/RECIPES.md) | **18 receptur**, każda z 11 wymaganymi polami; mapa dalszej nauki |
| [NLE-WORKFLOWS](specialists/nle/NLE-WORKFLOWS.md) | Cztery NLE, audio/kolor/finishing, scripting, post-lock changes i mapa szkoleń |
| [CODE-AND-CONTRACTS](CODE-AND-CONTRACTS.md) | Czas/PTS, przed–po, operacja→backend→ograniczenie→test, rewizje/cache i współpraca |
| [CURRENT-STUDIO](specialists/repo/CURRENT-STUDIO.md) | Stan publicznego kodu, installed-cache sample i macierz funkcji/luk/Unknown |
| [CONTRACT-FINDINGS](specialists/repo/CONTRACT-FINDINGS.md) | Kontrakty, których migracja musi dochować; ograniczenia interchange |
| [REPOSITORIES](specialists/repo/REPOSITORIES.md) | **10 wybranych repozytoriów narzędziowych**, konkretne pliki/piny/API/licencje i odroczenia |
| [QA-BENCHMARKS](specialists/nle/QA-BENCHMARKS.md) | **5 benchmarków**, tolerancje, round-trip i osobna ocena redakcyjna/percepcyjna |
| [IMPLEMENTATION_HANDOFF](IMPLEMENTATION_HANDOFF.md) | **10 zadań P0/P1/P2** z właścicielem, wejściem/wyjściem, plikami, ograniczeniem/fallbackiem i testem |
| [COVERAGE-MATRIX](COVERAGE-MATRIX.md) | Każda grupa wymagań promptu → artefakt → dowód → luka |
| [REVIEW](REVIEW.md) / [VERIFICATION](VERIFICATION.md) | Niezależna recenzja, poprawki i rzeczywisty zakres sprawdzeń |

## Źródła i przykłady

[SOURCE-LEDGER.json](SOURCE-LEDGER.json) i [CSV](SOURCE-LEDGER.csv): **88 rekordów, 86 różnych adresów** — 85 adresów web i jeden lokalny dokument oficjalnego SDK. Metody: 62 odczyty dokumentacji, 19 inspekcji kodu, 7 tekstów praktyków. Klasy: 81 SOURCED, 7 PRACTITIONER; synteza i propozycje w raportach są jawnie DERIVED, luki Unknown.

Dwa dokumenty mają po dwa rekordy użycia w różnych domenach: C01/N02 (training page) i C02/N03 (Editor’s Guide). Różne pliki tego samego repo i różne wersje tej samej dokumentacji nie są niezależnymi potwierdzeniami. Nie zaliczamy opisów kursów jako obejrzanych kursów.

Ponowny [link check](LINK-CHECK.json): **81 rekordów HTTP_OK, 6 HTTP403, 1 lokalny**. 403 dotyczą C07, C09, C10, C11, N11, N12; wcześniejszy odczyt treści jest opisany w ledgerze, lecz ponowna dostępność tym klientem nie została potwierdzona. Nie obchodzono ograniczeń ani logowania. Zero odpowiedzi 404 w tej próbie.

- [editorial-intent.schema.json](editorial-intent.schema.json): proponowany sidecar RFC 0.1; native project nadal schema_version1.
- [14 rodzin intencji](examples/editorial-intents.json): trim/split/insert/overwrite/ripple/roll/slip/slide, ramp/freeze, transforms, transition, gain/ducking, subtitles.
- [11 niezależnych przykładów native-shaped](examples/native-operations.json): do porównania z istniejącym API; wykonanie w silniku **NOT_RUN**.
- [Motion envelope RFC](examples/motion-handoff-rfc.json): body/handles, jeden master clock, provenance/locks i niezwiązane jeszcze hashe/fonty.
- [Projekcja napisów](examples/subtitle-time-map.json): własny rachunek przed/po ripple trim, bez sfabrykowanego source hash.

## Wersje i granice

Publiczny main odczytany w badaniu: [`4611c9c4ed44579b8a2c0224c9276d955fccd8d6`](https://github.com/FrameCoreWorks/framecore-works-creative-studio/commit/4611c9c4ed44579b8a2c0224c9276d955fccd8d6), commit 2026-11-11T07:20:22Z. Creative Studio package1.174.1, runtime FrameCut1.1.0, project schema1. **14/14 wybranych plików** cache zgodnych bajtowo z przypiętymi źródłami. Nie oznacza to sprawdzenia całej instalacji ani działania hosta.

Osobne repo FrameCut/FrameMotion: **Unknown**. Claude nie został wywołany i nie zatwierdził architektury. To badanie i handoff, bez zmian kodu produktów, instalacji, uploadów, płatnych usług, publikacji ani pushu.

Pięć benchmarków, rendery, testy native NLE/FrameCut, pomiary mediów, ogląd i odsłuch: **NOT_RUN**. Własne testy obejmują strukturę raportu, odwołania, ograniczony shape RFC oraz rachunek czasu; pełny zewnętrzny JSON Schema validator również NOT_RUN. Wynik maszyny: [VERIFICATION-RESULT.json](VERIFICATION-RESULT.json). Polecenie do powtórzenia: `python3 verify_research.py` uruchomione z katalogu tego badania lub z absolutną ścieżką do skryptu.

## Organizacja i dowód pracy

Hipson: **T-0004**, project = ten katalog; przypisania A-0017 craft, A-0018 NLE/QA, A-0019 repo/contracts, A-0027 niezależna recenzja. Rejestr Hipsona przechowuje końcowy status nadany po świeżym uruchomieniu zadeklarowanego checku. Działano według Superpowers planning/delegation/verification i Studio research/workflow, z trzema równoległymi specjalistami oraz świeżym recenzentem.

`PROMPT.md` zachowano bez zmian; doprecyzowanie zapisano osobno. Datowane kopie przed zmianami są w `backups/` i przy własnych plikach specjalistów. Duże PDF pozostały w prywatnym temp poza snapshotem Hipsona. Niczego nie archiwizowano ani nie usuwano.
