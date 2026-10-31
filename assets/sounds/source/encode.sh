#!/usr/bin/env bash
# Encode the WAVs from make_sounds.py to the published MP3s.
# Music is loudness-normalized to -16 LUFS integrated, -1.5 dBTP (two-pass ffmpeg loudnorm);
# effects keep their synthesized peak level. Usage: encode.sh WAV_DIR OUT_DIR
set -euo pipefail
src=$1; out=$2; mkdir -p "$out"
for wav in "$src"/*.wav; do
  name=$(basename "$wav" .wav)
  if [[ $name == *music* ]]; then
    stats=$(ffmpeg -hide_banner -nostats -i "$wav" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
    get() { python3 -c "import json,sys; print(json.loads(sys.stdin.read())['$1'])" <<<"$stats"; }
    af="loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=44100"
    ffmpeg -hide_banner -loglevel error -y -i "$wav" -af "$af" -c:a libmp3lame -b:a 160k "$out/$name.mp3"
  else
    ffmpeg -hide_banner -loglevel error -y -i "$wav" -c:a libmp3lame -b:a 192k "$out/$name.mp3"
  fi
  echo "$name.mp3"
done
