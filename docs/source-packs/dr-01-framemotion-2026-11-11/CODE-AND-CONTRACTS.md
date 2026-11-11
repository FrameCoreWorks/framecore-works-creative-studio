# Od warsztatu do kontraktu i danych

Data badania: 2026-11-11. **DERIVED:** wszystkie proponowane struktury poniżej są materiałem projektowym, nie wdrożoną funkcją FrameMotion. Pełna inspekcja publicznego Studio: `specialists/backends/STUDIO-AUDIT.md`. Runtime testy repozytorium: **NOT_RUN**. Żadnego kodu pobranego z repozytoriów nie uruchamiano.

## Pierwszeństwo istniejących kontraktów

**SOURCED, inspekcja dokumentu i kodu:** publiczny main Studio przypięto do `4611c9c4ed44579b8a2c0224c9276d955fccd8d6` (2026-11-11). Istnieje [motion-contract-json.md](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-contract-json.md) oraz [score.mjs](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-quality/score.mjs). `motion-score.json` łączy storyboard, approval i techniczny timeline; używa `fps:{num,den}`, `totalFrames`, scen `start/end` i holds. Nie projektujemy zamiennika tylko dlatego, że nowa wtyczka nosi inną nazwę.

FrameCut ma odrębne projekcje żądań oraz wiązania wyników w [fc_render.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py); ścisła walidacja projektu znajduje się w [fc_core.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_core.py). Żądanie wskazuje owner `hyperframes-workflow`, projekt/rewizję, event, globalny start, lokalny start=0, długość, FPS, wymiary, alpha/color i hashe. Inspekcja `bind_motion` ujawnia węższą kontrolę niż pełny test alfa/koloru: przy żądaniu straight sprawdza obecność kanału (`has_alpha`), nie dowodzi straight versus premultiplied; nie waliduje transformu koloru z tekstowego pola requestu. Potrzebny osobny test pikselowy/conform. Dodanie nieznanych kluczy do FrameCut v1 może zostać odrzucone. Adapter ma zachować te nazwy i właścicieli, dopóki właściciel architektury nie zatwierdzi migracji. Lista pól odczytanych: `specialists/backends/request.fields.json` — jest opisem kształtu, nie rzeczywistym requestem.

**Granica dowodu:** odczytany kod publiczny ≠ stan działającej instalacji ≠ przetestowany wynik. Dokładny stan nowej wtyczki FrameMotion i repozytorium FrameCut pozostaje Unknown; ich adresów nie dostarczono. Lokalny odczyt skilla Studio wskazuje pakiet 1.174.1, ale nie dowodzi aktywacji całego runtime ani zgodności z publicznym commitem.

## Trzy poziomy danych i jeden owner

1. **Specyfikacja kreatywna:** istniejący score — cel, kopia, kompozycja, impacty, holds, akceptacja, locked assets. Opisuje *dlaczego i kiedy*.
2. **Proponowany sidecar FrameMotion:** typed scene graph + jawne capability requirements + referencja do score/request. Opisuje *co ma zostać wyliczone*. To osobny, wersjonowany dokument, którego istniejący renderer nie musi znać.
3. **Adapter:** kompiluje sidecar do konkretnego backendu i raportuje mapowania wierne/przybliżone/hybrydowe/unsupported. Opisuje *jak*. Nie interpretuje ponownie hasła ani nie ustala montażu.

Standalone: FrameMotion może być ownerem własnej osi. Zlecenie ze Studio: owner wynika z project state. Zlecenie od FrameCut: FrameCut jest właścicielem globalnej osi; FrameMotion działa w przydzielonym lokalnym zakresie i zwraca wynik, nie przesuwa sąsiednich scen. W istniejącym motion score `start/end` nazywane są master frames; w projekcji sceny ze zlecenia master score jest **lokalną osią otrzymanej sceny**, a mapowanie do master filmu pozostaje w żądaniu FrameCut. Nie wolno dodać globalnego startu dwukrotnie.

## Pola wspólne: obecne, projektowane i mapowanie

| Wymaganie | Obecna reprezentacja | Propozycja dla sidecar / reguła |
|---|---|---|
| project_id | FrameCut request `project_id` | Kopiuj, nie generuj nowego dla tej samej pracy |
| schema_version, revision | Obecne score; request schema_version/project_revision | Sidecar ma własną `schema_version`; bazowe rewizje przypięte w `bindings` |
| timeline_owner | Owner route/request, bez uniwersalnego top-level pola w v1 | Sidecar `timeline_owner`; kontrola zgodności z ownerem requestu, nie dowód przejęcia własności |
| asset_id/hash | Score `assets.id/file/revision`; hash w FrameCut binding | Sidecar dependencies z sha256; nie zmieniaj formatu upstream w ciszy |
| fps_num/fps_den | `fps.num/den` | Adapter mapuje 1:1; nie trzyma dwóch edytowalnych wartości |
| czas [in,out) | Sceny `start/end`, request duration | `assignment.in_frame/out_frame` globalnie; `scene_graph` lokalnie |
| source/timeline time | FrameCut source-to-sequence | Jawna funkcja source(local), jednostki; origin nie wynika z nazwy pliku |
| handles | Zależy od event/request | Sidecar deklaruje dostępny pre/post range; nie renderuje poza zakresem bez zlecenia |
| retiming | Istniejący montaż FrameCut | Proponowane segmenty affine albo tabela mapowania; żadne ukryte stretch |
| width/height | Oba kontrakty | Warianty kompozycji w score.formats; adapter ma znać viewport |
| color space / alpha | Request `color`, `alpha` | Rozdziel input/work/output/display i premult domain; mapuj dopiero wspierane możliwości |
| audio sample rate | Runtime/spec audio, nie zakładaj uniwersalnego pola v1 | `audio.sample_rate_hz`; cues z deklaracją source/local/global time |
| fonty | Score `fonts` | Manifest plików/hashów/licencji i glyph coverage; niedostępne = blocked |
| seed | Część soundDesign, brak wspólnego seed całej sceny potwierdzonego | Sidecar `random.seed` i jawny algorytm dla danej wersji adaptera |
| provenance | Rewizje, hashe, evidence w różnych ownerach | Graf zależności i źródła; wzorowany na H06 PROV, nie pełna zgodność PROV |
| accepted locks | Copy/assets/approval | Mapuj istniejące locks; nie deklaruj nowego approval za użytkownika |

## Przykład spójnego pakietu badawczego

`examples/motion-score.example.json` to oryginalny score demonstracyjny, a `examples/framemotion-sidecar.example.json` jest **proponowaną specyfikacją rozszerzenia**, nie aktualnym API. W przykładzie scenie przydzielono globalnie [900,1140), lokalnie [0,240), FPS 30000/1001. Długość to 8.008 s. Asset SVG istnieje w `examples/assets/mark.svg` i ma obliczony hash; jest sztucznym znakiem testowym, nie logo klienta. Font ma status `NOT_PROVIDED`; cały preflight do produkcji jest `blocked`, co jest zamierzonym wynikiem. Nie ma prawdziwych hashów projektu FrameCut ani zgody klienta.

Sidecar trzyma hash score, więc zmiana tekstu musi unieważnić binding. Przykład pokazuje warstwę, maskę, kamerę ortograficzną, typed keyframes oraz cue audio w próbkach. Nie wymaga przedstawienia finalnego filmu. Weryfikator odtwarza tylko referencje i arytmetykę.

## Scene graph ≠ dependency graph ≠ timeline

**Scene graph:** hierarchia transformacji. Propozycja używa kolumnowych wektorów i lokalnego `M=T(position)·R(rotation)·S(scale)·T(−anchor)`, zaś `M_world=M_parent·M_local`. Jednostka 2D px, kąty deg, skala bezwymiarowa. Grupowanie nie musi oznaczać dziedziczenia opacity — reguła jest jawna. Zamiana kolejności R i T zmienia ruch. AE parenting lub collapse transformations nie może być odtworzone samym CSS `transform` bez sprawdzenia modelu.

**Dependency graph:** renderowane powierzchnie, maski, kamery, matte, expression inputs i assety. To DAG wymagający sortowania topologicznego; self-reference i cykle A→B→A są błędem, nie dowolną kolejnością. Kolejność musi wskazywać przestrzeń maski: maska local może działać przed transformacją, maska composition po transformacji celu. W naszym przykładzie: load asset → local shape → target world transform → composition-space alpha mask → composite → output transform. `mask1` nie jest widoczną warstwą (`renderable:false`), tylko wejściem alpha; jego przestrzeń jest jawnie `composition-px`. Zmiana miejsca rasteryzacji wpływa na rozdzielczość efektów i crop. Obsługa precomp/collapse to osobna capability.

**Timeline:** widoczność i kanały parametrów w lokalnej osi. Klucz może leżeć na granicy out do określenia interpolacji, lecz ostatni renderowany sample to out−1; validator oddziela granice segmentu od próbek obrazu. W fixture kanały przed pierwszym kluczem trzymają pierwszą wartość (`hold-first`), po ostatnim ostatnią (`hold-last`); mark jest visible [0,240), lecz na f0–18 pozostaje poza kadrem, tekst visible [45,240). To ustala jednoznaczny stan dla f0/18/30/239; nie zakładamy automatycznego wejścia/wyjścia. Spatial path i temporal progress są osobne. Ease nie musi zachowywać prędkości w px/s, jeśli długość ścieżki jest nieregularna.

## Krótkie przykłady — oryginalny pseudokod DERIVED

### Klatka i próbka audio bez narastającego błędu

```python
from fractions import Fraction
fps = Fraction(30000, 1001)
t = Fraction(frame, 1) / fps             # sekundy od local zero
sample_time = Fraction(sample, 48000)   # oddzielny zegar audio
exact_frame = sample_time * fps
# nearest, ties away from zero dla dodatniego czasu:
rounded = (2*exact_frame.numerator + exact_frame.denominator) // (2*exact_frame.denominator)
```

To przeliczenie nie identyfikuje beatu — bierze już opisane zdarzenie. H04 beat tracker estymuje rytm, H05 onset detector atak; jednostka analysis frame jest inna niż video frame. Dla cue 48048 próbek: 1.001 s, klatka30. Jeżeli wejście ma 12 klatek do impactu, start=18. Próba startowania na30 daje impact42, czyli pomylenie startu z akcentem.

### Prosty ease jako kontrast do prędkości

```text
u = clamp((f-a)/(b-a), 0, 1)
p = 3*u*u - 2*u*u*u
x = x0 + (x1-x0)*p
v_px_per_s = (x1-x0)*(6*u-6*u*u) / ((b-a)/fps)
```

To gładki punkt startowy bez overshoot, nie uniwersalny „dobry easing”. Value graph to x(t); speed graph w ruchu 1D to |dx/dt|, a signed velocity zachowuje kierunek. Dla 2D speed to norma wektora pochodnej. Zmiana dystansu przy tym samym duration zmienia prędkość; nie należy kopiować jedynie kształtu krzywej. Przy temporal cubic Bézier należy rozwiązać x(s)=u, a potem odczytać y(s); bez tego obliczenie y(u) nie jest CSS cubic-bezier.

### Deterministyczne cząstki i procedural noise

```text
birth = particle_id * stagger_frames
age_seconds = (frame - birth) * fps_den / fps_num
r = hash32(seed, particle_id, channel) / 2^32
position = p0 + velocity(r)*age_seconds + 0.5*gravity*age_seconds^2
visible = 0 <= age_seconds < life_seconds
```

Hash musi mieć określony algorytm, kodowanie i integer overflow; samo „seed=42” nie standaryzuje wielu generatorów. Wyrażenie analityczne jest seekable. Kolizje z historycznym solverem wymagają stałego kroku i cache/checkpoint. Noise do swobodnego ruchu interpolować między stałymi próbkami czasowymi; niezależny random każdej klatki daje migotanie, co może być poprawne dla grain, lecz błędne dla płynnego driftu.

### Font preflight bez fałszywego PASS

```text
verify local bytes hash and licence record
load each required FontFace; fail on load rejection
await document.fonts.ready after placing final strings
inspect glyph coverage and expected line breaks
capture only after stable layout; reject fallback where exact font is locked
```

H01: `document.fonts.check` może zwrócić true dla nieistniejącej rodziny, a `ready` samo się nie odrzuca. Z tego wynika, że czekanie nie zastępuje kontroli konkretnego fontu. Tekst dzielić po grapheme clusters; zachować ligatury/kerning na etapie shaping albo świadomie wybrać słowa jako jednostkę animacji. Kodową serializację UTF-16 odróżnić od glifu.

## Retiming i zmiana długości

**DERIVED:** `source_frame(local)=source_in + local*speed` przy jednakowych jednostkach FPS; przy innych najpierw przejść przez czas rational. Dla ramp potrzebna funkcja całki prędkości lub jawna tabela mapowania, nie pojedynczy mnożnik. Ujemna prędkość wymaga określonego kierunku i bounds źródła. Quantize dotyczy pobrania próbki, nie definicji wszystkich zegarów.

Jeśli scena potrzebuje 300 zamiast przydzielonych 240 klatek, FrameMotion zwraca `duration_change_request` z powodem i zakresem, którego nie może spełnić. Owner wybiera: skrócenie wyrazu, zmiana hold, retime lub wydłużenie filmu. Dopiero nowa revision/request umożliwia render. Bez zgody nie przesuwa montażu, VO ani końcówki. Istniejący helper rewizji score potrafi przesunąć dalsze sceny — w delegowanym zadaniu jego użycie trzeba ograniczyć do lokalnego scope, nie całego filmu.

## Wersjonowanie, błędy i brak cichej utraty danych

- Sidecar `schema_version` dotyczy sidecar, nie zmienia FrameCut v1. `adapter_version`, `source_contract_schema`, `source_revision` i `compiled_from_sha256` przechowywać osobno.
- Nieznana wersja major → fail; nowy opcjonalny klucz minor zachować losslessly w round-trip, ale nie twierdzić, że renderer go wykonał. Required capability unknown/unsupported → fail.
- Migracja jest czystą funkcją tworzącą nowy plik, z diffem znaczenia, manifestem pól odrzuconych (domyślnie pustym), kopią oryginału i testem round-trip tam, gdzie odwracalna. Nie nadpisywać automatycznie jedynego projektu.
- Missing asset/hash mismatch/font missing: lokalny blocker z identyfikatorem; nie sieciowy zamiennik. Unsupported effect: explicit fallback do native RGBA, prostszej zaakceptowanej techniki albo STOP.
- Stale request z niezgodnym kontekstem (brief/sequence/deliverable): odświeżyć projekcję od ownera; nie retry samego attach. Sam wzrost numeru revision, np. przez ingest wyniku przy niezmienionych hashach kontekstu, nie oznacza automatycznej niezgodności. Zachować semantykę istniejącego bind_motion. Decode failure: jednokrotne ponowienie po diagnostyce wejścia, bez zmiany parametrów. Out-of-memory: zmniejszyć concurrency lub rozbić na chunk, zachowując jakość; zmiana quality settings wymaga jawnej nowej specyfikacji.
- Idempotency key: hash score + deps + adapter/build + output settings + range. Zapis atomowy wynik.tmp → wynik; ukończenie wyłącznie po checksum i probe, nie po samym wyjściu procesu.
- Koszt planowany: lokalny CPU/GPU/dysk; w tym researchu brak wywołań paid/cloud. Licencja backendu jest osobnym warunkiem, szczególnie Remotion/GSAP; zmiana wtyczki w narzędzie authoring może zmienić zastosowanie licencji.

## Preview/export parity i wznowienie

Specyfikacja jest wspólna, ale identyczność implementacji nie wynika z identycznego JSON. Przypiąć browser build, fonty, DPR, viewport, backend, shader precision, output color, GPU/driver i seed. CPU 2D i WebGL mogą mieć różny antyaliasing, blend i raster tekstu. Testy porównują najpierw semantykę/transformacje/tekst, potem obrazy w jawnej tolerancji; bit-identical wolno obiecać wyłącznie w przetestowanym pinned środowisku.

Render po numerze klatki powinien być funkcją `render(frame, immutableSpec, dependencies)` albo odczytem bake. Wall-clock, Date.now, sieć, zmienny RNG i ukryte poprzednie klatki są zależnościami wymagającymi usunięcia lub ujawnienia. Dla blur oceniać scenę w subframes względem shutter center/phase, nie tylko rozmywać gotowy obraz. Cache kluczuje quality i color settings. Granice chunków muszą uwzględniać tails efektów i potrzebne wcześniejsze stany solvera. Wznowienie nie oznacza dalszego użycia częściowo zapisanej klatki.
