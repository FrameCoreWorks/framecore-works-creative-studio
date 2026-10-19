import pathlib,sys
def rep(path, old, new, count=1):
    p=pathlib.Path(path); t=p.read_text()
    n=t.count(old)
    if n!=count: sys.exit(f'{path}: expected {count} got {n}: {old[:70]!r}')
    p.write_text(t.replace(old,new))
A='skills/hyperframes-workflow/assets/motion-sync/audio_envelope.py'
rep(A,"""composition, as `const ENVELOPE = {...};`, so the render needs no network or file reads.""","""composition, as `const ENVELOPE = {...};`, so the render needs no network or file reads, and sets `data-duration` on
the composition root and on a music clip (`data-timeline-role="music"`) to the envelope's length.""")
rep(A,"""    line = f"{BEGIN}\\n      const ENVELOPE = {json.dumps(data, separators=(',', ':'))};\\n      "
    Path(path).write_text(text[:a] + line + text[b:], encoding='utf-8')""","""    line = f"{BEGIN}\\n      const ENVELOPE = {json.dumps(data, separators=(',', ':'))};\\n      "
    text = text[:a] + line + text[b:]

    def set_duration(tag):
        tag = tag.group(0)
        if 'data-composition-id=' in tag or 'data-timeline-role="music"' in tag:
            tag = re.sub(r'data-duration="[^"]*"', f'data-duration="{data["duration"]:g}"', tag)
        return tag
    Path(path).write_text(re.sub(r'<(?:div|audio)\\b[^>]*>', set_duration, text), encoding='utf-8')""")
E='skills/hyperframes-workflow/assets/iso-glow/examples/bass-speaker/index.html'
rep(E,"""      <svg id="art\"""","""      <!-- With the user's track (never committed): copy it next to this file and uncomment the clip; audio_envelope.py --inject sets both durations.
      <audio id="music" class="clip" src="track.m4a" data-start="0" data-duration="8" data-track-index="0" data-timeline-role="music"></audio> -->
      <svg id="art\"""")
rep(E,"""      const D = Math.min(8, ENVELOPE.duration);""","""      const D = ENVELOPE.duration;""")
T='tests/iso_glow_test.py'
rep(T,"""            html.write_text('<script>\\n      /* BEGIN ENVELOPE */\\n      const ENVELOPE = null;\\n      /* END ENVELOPE */\\n</script>\\n')""","""            html.write_text('<div id="root" data-composition-id="main" data-duration="8">\\n'
                            '<audio id="music" data-duration="8" data-timeline-role="music"></audio>\\n'
                            '<div class="scene" data-duration="2"></div>\\n'
                            '<script>\\n      /* BEGIN ENVELOPE */\\n      const ENVELOPE = null;\\n      /* END ENVELOPE */\\n</script>\\n')""")
rep(T,"""            self.assertEqual(body.count('/* END ENVELOPE */'), 1)""","""            self.assertEqual(body.count('/* END ENVELOPE */'), 1)
            self.assertEqual(body.count('data-duration="4"'), 2)
            self.assertIn('class="scene" data-duration="2"', body)""")
R='skills/hyperframes-workflow/assets/iso-glow/README.md'
rep(R,"""5. **Drive it from time.** Copy the example, run `python3 audio_envelope.py track.mp3 --start S --duration D --inject index.html`""","""5. **Drive it from time.** Copy the example, put the user's track beside it and uncomment its music clip, run `python3 <skill>/assets/motion-sync/audio_envelope.py track.m4a --start S --duration D --inject index.html` (it also sets the composition and clip length)""")
rep(R,"""6. **Check** with the usual""","""6. **Render** with `npx hyperframes render --quality draft` in a HyperFrames project, or, without npm, with [`capture-html.mjs`](../motion-export/README.md#hand-written-html-to-mp4-without-npm) and the track muxed in afterwards.
7. **Check** with the usual""")
