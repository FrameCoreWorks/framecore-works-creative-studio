# DR-02 — Katalog repozytoriów i decyzji integracyjnych

Data: 2026-11-11. Publiczne źródła pierwotne i wskazane pliki zostały odczytane. **Nie instalowano bibliotek, nie uruchamiano pobranego kodu i nie wykonywano benchmarków.** Wszystkie testy poniżej to NOT_RUN. SOURCED opisuje dokumentację/kod; DERIVED oznacza rekomendację do późniejszego wdrożenia.

„Wybrane” nie znaczy automatycznie dodane do Studio/Toolbox. Metoda, instrukcja, runtime dependency i kopiowanie kodu to cztery osobne decyzje. Preferencja: oryginalny adapter wykorzystujący publiczne API; bez vendoringu całych repozytoriów. FFmpeg/ffprobe opisuje główny raport, więc ten katalog ich nie dubluje.

## 1. Piny i utrzymanie

Daty w tabeli to data **commitu z default branch**, nie obietnica najnowszego stabilnego wydania. Pushed_at nie został podmieniony za datę commitu. Żadne z badanych repozytoriów nie miało flagi archived=true w odczytanej metadanej; aktywność nie dowodzi jakości.

| Repo/pin (skrót) | Odczytana wersja | Commit UTC | Licencja główna | Decyzja DERIVED |
|---|---|---|---|---|
| [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/tree/bad7ab5a40ac1a95d9d78a87c95a688d8b57cf28) bad7ab5a | OTIO_VERSION.json=0.19.0; latest docs banner0.19.0.dev1 | 2026-11-10 | Apache-2.0 | Preferowany IR/adapter interchange, już opcjonalnie obecny w FrameCut. |
| [otio-fcp-adapter](https://github.com/OpenTimelineIO/otio-fcp-adapter/tree/63824d5ca04dbda81bcced89c9fde6ab0b7e6e36) 63824d5c | pyproject1.1.0 | 2026-04-08 | Apache-2.0 | Bounded FCP7 XML; nie mylić z FCPXML. |
| [otio-fcpx-xml-adapter](https://github.com/OpenTimelineIO/otio-fcpx-xml-adapter/tree/c61839e105fb035589d3ec704b1266a22089b425) c61839e1 | package1.1.0; emitter FCPXML1.8 | 2024-06-25 | Apache-2.0 | Opcjonalny adapter legacy; ostrożnie z obecnym FCP. |
| [otio-aaf-adapter](https://github.com/OpenTimelineIO/otio-aaf-adapter/tree/47886982d67c00573ad4a565ae51ad0e73f4caff) 47886982 | pyproject2.0.0 | 2026-09-22 | Apache-2.0 | Bounded AAF turnover z loss report. |
| [MLT](https://github.com/mltframework/mlt/tree/2a51ed9cca0b7edca5f1c34749bad67b76b0051a) 2a51ed9c | CMake7.43.0, development tree | 2026-11-07 | LGPL-2.1 core; moduły/build osobno | Pilot backend dopiero przy udowodnionej potrzebie multitrack. |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect/tree/c0d48701fad42e9a8a7af0790f58d9645a211490) c0d48701 | main0.8-dev0; stable docs0.7.3 | 2026-11-10 | BSD-3-Clause | Najsilniejszy kandydat do jawnych cut candidates i metrics. |
| [Whisper](https://github.com/openai/whisper/tree/86098128c0b4f24f0e2aa2994de830614b474227) 86098128 | commit pin; model family oddzielnie | 2026-08-31 | MIT code i oficjalne weights | ASR evidence, nie decision engine; najpierw istniejący lokalny route. |
| [PyAV](https://github.com/PyAV-Org/PyAV/tree/38df009989caf976ce24feaa794882effd63c850) 38df0099 | commit pin; nie przyjęto numeru release | 2026-11-08 | BSD-3-Clause + FFmpeg build | Optional decode/PTS/QC helper; nie kolejny NLE renderer. |
| [MediaInfoLib](https://github.com/MediaArea/MediaInfoLib/tree/24a58322113a884654bca463ae68f1e3a4165a06) 24a58322 | version string26.10 | 2026-11-11 | BSD-2-Clause + dependencies | Metadata cross-check tam, gdzie ffprobe nie wystarcza. |
| [libebur128](https://github.com/jiixyj/libebur128/tree/67b33abe1558160ed76ada1322329b0e9e058b02) 67b33abe | 1.2.6 | 2021-02-14 | MIT | Optional independent meter; nie nowa default dependency. |

Źródła: [R14][R15][R16][R17][R18][R19][R20][R21][R22][R23][R24][R25][R27][R29]. Commit pin jest odtwarzalnym punktem inspekcji. Production pin powinien zostać wybrany po fixture i host compatibility check, nie na zasadzie „main jest nowe”.

## 2. Karty modułów, wejść i wyjść

### OpenTimelineIO — format wymiany, nie pełny renderer

**SOURCED:** docs/tutorials/otio-timeline-structure.md (R14), time-ranges.md (R28) i src/py-opentimelineio/opentimelineio/adapters/__init__.py (R15) rozdzielają Timeline/Stack/Track/Clip/Gap/Transition oraz MediaReference. API: read_from_file/read_from_string, write_to_file/write_to_string, available_adapter_names. Wejście: OTIO/native lub format konkretnego adaptera; wyjście: obiekty timeline/serialization. C++ core z Python API, osobno instalowane plugins dla większości zewnętrznych formatów.

**Transfer:** własny mapper Native FrameCut↔OTIO i semantic comparison. Zachować source PTS/hash/revision w metadata, ale nie zakładać, że każdy NLE zachowa custom metadata. OTIO nie waliduje dostępności media handles i nie definiuje pełnej semantyki dowolnego effect. Transition nie zmienia długości track. [R14][R15][R28]

**Counterexample/test:** poprawnie zserializowany clip wskazuje poza available_range albo imported effect jest ignorowany. Fixture nonzero source start, long rational duration, nested stack, asymmetric handles i trailing gap; porównać całe ranges, nie tylko total duration. NOT_RUN.

### FCP7 XML adapter — weryfikować kod i kierunek

**SOURCED:** src/otio_fcp_adapter/fcp_xml.py ma read_from_string (L2003), write_to_string (L2020), FCP7XMLParser, transition_for_element (L1116) oraz _build_transition_item (L1548). Wejście/wyjście: Final Cut Pro7 XML i OTIO, zależność opentimelineio, package1.1.0. [R16]

**Rozbieżność:** README feature matrix oznacza transitions jako niewspierane, ale kod posiada ścieżki read/write przejść, a badany commit naprawia ich rate. Nie wolno z tego zrobić ani „żadne przejście nie działa”, ani „round-trip jest pełny”. Przyjąć per-feature status Unknown/needs fixture; basic cuts/gaps są niższym ryzykiem niż efekty.

**Transfer/test:** FCP7 XML turnover dla NLE obsługującego ten dialekt; compare source/record intervals, actual dissolve handles i 30000/1001 vs24. Nie deklarować zgodności z obecnym Final Cut Pro na podstawie historycznej nazwy formatu. NOT_RUN.

### FCPXML adapter — wersja emitowanego dokumentu jest kontraktem

**SOURCED:** src/otio_fcpx_xml_adapter/fcpx_xml.py ma rational-time conversion L79–123, tworzy fcpxml version1.8 w L134, API read_from_string/write_to_string L1133–end. [R17] README wymienia brak transitions/effects/retiming; to ograniczenie adaptera, nie całego formatu FCPXML.

**Transfer:** osobny adapter qualified dla konkretnego FCP. Data commitu2024-06-25 i emitowanie1.8 wymagają próby importu w wersji używanej do projektu. Nie zakładać zachowania roles, captions, nested/connected clips i modern metadata bez fixture.

**Fallback/test:** native project + source map + rendered effects/graphics + explicit loss report, gdy struktur nie da się przenieść. A/B imported timeline i reference render, auditory check; NOT_RUN.

### AAF adapter — read i write nie są symetryczne

**SOURCED:** src/otio_aaf_adapter/adapters/advanced_authoring_format.py używa pyaaf2 i typed AAF objects, transkrybuje media/source ranges i timewarp; README deklaruje linear-speed read, ale nie write; effects/fancy retime nie są wspierane. API adaptera: read_from_file/write_to_file. [R18]

**Transfer:** bounded turnover do postprodukcji, osobno audio/video channels, source mob/reel/timecode i relink. pyaaf2 jest dodatkową zależnością; jego wybrany release/licencję trzeba potwierdzić przed bundlingiem — nie zaliczono go tu jako oddzielnie zakwalifikowanego repo.

**Counterexample/test:** AAF import rozpoznaje constant speed, re-export gubi to samo przekształcenie. Test markers, stereo/mono channel mapping, linked audio, overlaps, source ranges i actual NLE reimport. NOT_RUN.

### MLT — silnik timeline z konkretnym kosztem integracji

**SOURCED:** src/framework/mlt_playlist.h L85–145 udostępnia append_io, insert, remove, move, resize_clip, split/split_at, join, blanks i remove_region; mlt_tractor.h łączy tracks. XML dokumentuje producers→playlists→multitrack/tractor→consumer. Parser XML opisany jest jako non-validating. [R19][R26]

Wejście: MLT XML albo C/C++ service graph, profile/frame rate, media sources. Wyjście: frame/audio stream, XML serialization lub plik przez wybrany consumer. Zależności i codecs zależą od wybranych build modules; Python binding nie jest automatycznie obecny. Framework LGPL nie oznacza, że cały wybrany build i jego dodatkowe moduły mają tę samą licencję.

**Transfer:** przejęcie metody producer/source vs playlist event; optional compiler backend dopiero, gdy uzasadnia go multitrack/performance. Nie usuwać istniejącego FrameCut/Pillow/FFmpeg route dla samej popularności MLT.

**Test:** konwersja półotwartego [in,out) na model endpointów backendu, pojedyncza klatka, blanks, seeking, transition duration, audio mapping, missing service, headless macOS. NOT_RUN. Fallback: native FrameCut render lub human NLE.

### PySceneDetect — analiza nie jest decyzją montażową

**SOURCED:** adaptive_detector.py procesuje adjacent HSV changes i rolling average, emituje kandydackie cięcia. SceneManager daje scene lists/statistics; Python detect/open_video i CLI detect-adaptive/list-scenes/split-video to różne poziomy działania. Core dependencies: Python≥3.10, NumPy/OpenCV; CLI click/platformdirs/tqdm. Opcjonalny PyAV backend. [R20][R27]

**Version hazard:** inspected main0.8-dev0 nie jest stable docs0.7.3. Stable docs mówią min_scene_len Python15frames vs CLI0.6s, więc niezapisane defaults mogą dać różne wyniki. Adapter ma serializować realne parametry, jednostki, source hash i detector version.

**Transfer:** zaproponować review windows wokół wykrytych zmian, wyszukać hard cuts/fades; nie wybierać najlepszego dubla ani nie skracać „nudnych” fragmentów. Fast pan/flash/dissolve to kontrprzykłady dla naiwnego cut score.

**Test:** annotowane source boundaries z hard cut/pan/flash/fade/similar framing; precision/recall i timestamp tolerance podane jako projektowe. VFR backend musi zachować rzeczywiste timestampy. NOT_RUN.

### Whisper — ASR jako wersjonowany dowód

**SOURCED:** whisper/transcribe.py L38–125 przyjmuje file path, waveform NumPy albo Tensor i zwraca text/segments/language. word_timestamps korzysta z cross-attention+DTW; nie jest gwarancją forced alignment. Model card ostrzega o hallucinations, repetitions i różnicach językowych; diarization nie staje się potwierdzoną funkcją przez samo ASR. Code i oficjalne weights MIT. [R21][R22][R29]

Zależności obejmują PyTorch/Python stack/FFmpeg, wybrany model i dostępne device resources. Model weights/version/hash należy zapisać oddzielnie od engine commit. Read-only research niczego nie pobrał. Studio ma już lokalną opcjonalną trasę PyWhisperCpp z jawnym modelem; nowy engine wymaga porównania wartości, nie duplikacji instalacji. [R31]

**Transfer:** draft words/segments z source hash, timing method i flags do odsłuchu. Nie poprawiać sensu z samego language model confidence. Nie generować równomiernych sztucznych word times.

**Test:** polskie nazwy, liczby, code switching, szum, muzyka, cisza, overlap speakers; porównanie z odsłuchanym reference transcript i ręcznie ustalonymi boundary times. Transkrypcja nie ocenia tonu, ironii i dramaturgii. NOT_RUN.

### PyAV — dokładny dostęp do dekodowania, ale nie magiczny seek

**SOURCED:** av/container/input.py L319–375 przyjmuje integer seek offset w stream.time_base; zwykle seek do poprzedniego keyframe, potem decode forward. docs/api/time.rst rozróżnia stream/codec time bases i wymaga rescale przed mux. W bieżącym main dokumentacja mówi AVRational oraz falsy unset, więc starsze przykłady Fraction/None mogą nie pasować. [R23]

Wejście: container bytes/file, streams, packet/frame PTS. Wyjście: decoded frames/audio samples lub muxed packets. Zależności: compiled extension/FFmpeg; build dependencies Cython/setuptools. Licencja PyAV BSD-3-Clause nie zastępuje licencji dołączonego FFmpeg.

**Transfer/test:** optional frame extractor i sequential-vs-random-decode oracle. Long-GOP/B-frames/VFR/nonzeroPTS i frame hash po decode forward. Nie używać packet index jako display frame index. NOT_RUN.

### MediaInfoLib — dodatkowy odczyt metadanych

**SOURCED:** Source/MediaInfoDLL/MediaInfoDLL.h L566–588 pokazuje Open/Get/Inform/Option; version string26.10 w MediaInfo_Config.cpp L141. Wejście: media file/buffer; wyjście: stream/container metadata i reports. Licencja BSD-2-Clause; ZenLib/zlib/inne opcjonalne biblioteki zachowują własne warunki. [R24]

**Transfer:** cross-check codec/color/channel metadata, gdy istotne pola ffprobe są niepełne lub sprzeczne. Nie tworzyć drugiego master clock; rozbieżność zapisać i rozstrzygnąć przez source/decode evidence.

**Counterexample/test:** kontener deklaruje poprawną długość/kolor, ale dekodowanie się kończy błędem albo obraz jest przekształcony błędnie. Fixture known CFR/VFR/rotation/SAR/audio/color; NOT_RUN. Metadata inspection nie zastępuje QC.

### libebur128 — niezależny meter, nie ocena miksu

**SOURCED:** ebur128.h L119–127 tworzy state dla channels/sample rate/modes; add_frames_* L217–227 przyjmuje PCM, L240–378 zwraca integrated/momentary/short-term LUFS, LRA i true peak. Wersja1.2.6/MIT. [R25]

**Transfer:** optional independent numeric verification tam, gdzie uzasadnia to test. Kanały i sample count muszą mieć właściwe jednostki. cisza→negative infinity jest wynikiem pomiaru, nie osiągniętym target LUFS.

**Maintenance:** default-branch commit z2021 jest sygnałem do kontroli compatibility; nie dowodzi porzucenia ani wad. Ponieważ FrameCut już mierzy FFmpeg loudnorm, dodatkowy C meter potrzebuje mierzalnej wartości.

**Test:** referencyjne sygnały, kanały, cisza, post-encode true peak; odsłuch oddzielnie. NOT_RUN.

## 3. Odrzucenia i odroczenia

| Kandydatura / pomysł | Decyzja | Powód i warunek powrotu |
|---|---|---|
| Nowy master timeline w OTIO obok native FrameCut | Odrzucone | Dwie authority i rewizje. OTIO ma być projekcją interchange; native pozostaje master. [R04][R14] |
| Zastąpienie rendererów Studio przez MLT od razu | Odroczone | Brak benchmarku korzyści i host build/licence qualification. Pilot tylko przy konkretnym multitrack problemie. [R19][R26] |
| Auto-cut z PySceneDetect/Whisper | Odrzucone jako decyzja kreatywna | Cut detection/ASR nie wyznacza intencji, tonu ani najlepszego dubla. Candidate evidence jest użyteczne. [R20][R22] |
| FCPXML adapter jako pełne współczesne FCP round-trip | Odrzucone jako promise | Emitter1.8, stary commit, niepotwierdzone efekty/roles. Potrzebny named-version fixture. [R17] |
| Jeden bool „AAF/OTIO supported” | Odrzucone | Feature×direction×adapter×version; read≠write, format≠implementation. [R15][R18] |
| Nowy WhisperX/diarization/model stack | Nie zakwalifikowano w tym podzakresie | Nie badano tu konkretnego engine/weights/model licence chain; brak podstaw do auto-install. Wrócić przy rzeczywistej potrzebie alignment/diarization. |
| Kopiowanie skilli/parserów z repo jako domyślny transfer | Odrzucone | Preferować metodę/API i własny adapter; kopiowanie wymaga oddzielnego licence/provenance review. |

## 4. Priorytet praktyczny

**DERIVED:** P0 zachowuje native project, ops/revision/hash i rozszerza semantic QA. P1 rozwija OTIO z wybieranymi adapterami oraz jawne cut/ASR evidence, gdy obecne analizy nie wystarczają. P2 rozważa alternatywny backend/independent meters po benchmarku. Żadna biblioteka nie zastępuje rzeczywistego oglądu/odsłuchu i redakcyjnego uzasadnienia cięcia.

Dla każdej instalowanej później zależności acceptance obejmuje: commit/package/model pin, API fixture, offline/local behavior, brak niejawnego download/upload, resource timeout, output provenance i loss report. To wymagania projektu, nie wyniki niniejszego badania. Wszystkie benchmarki **NOT_RUN**.

