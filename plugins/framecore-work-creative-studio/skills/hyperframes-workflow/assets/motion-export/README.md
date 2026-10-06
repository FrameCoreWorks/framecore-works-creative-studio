# Browser video export

Turns a motion contract into a video file in the user's own browser, without installing anything and without uploading anything. It is the video route for hosts with no shell or renderer; where Node.js and Remotion are available, the [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md) remains the full render path with audio.

## How it works

[`video-export.mjs`](video-export.mjs) draws every frame of the [single-file preview](../single-file-preview/README.md) stage into a canvas through an SVG `foreignObject` image, encodes it with the browser's WebCodecs `VideoEncoder` and writes the file with its own dependency-free muxers:

- **MP4 with H.264** when the browser can encode H.264 (High profile; level 4.0 up to 1920 × 1080 or 1080 × 1920, 5.1 above). This is the file most social platforms and editors accept.
- **WebM with VP9 or VP8** otherwise. Some platforms do not accept WebM; convert it or render with Remotion when MP4 is required.

Frames come from the shared [scene engine](../motion-scenes/README.md), one at a time from the master frame number, so the export does not depend on playback speed. Captions are included. The export is **video only**: music and voice-over are not mixed in; add them in an editor or render with Remotion. Keyframes fall every two seconds; the bitrate is 8 Mbit/s at 1920 × 1080 and 30 FPS, scaled with frame size and rate.

The single-file preview embeds `video-export.mjs` (without `export` keywords) and the toolkit validation keeps the copies identical.

## Using it

- **In the preview.** Choose the format, press **Export video**, wait for the progress to finish, then save the file from the link. The file is named after the contract and format, such as `kinetic-type-starter-9x16.mp4`.
- **From a shell** with Node.js 20 and a local Chrome or Chromium, through the same code:

```sh
node export-video.mjs motion-score.json --out film.mp4 [--format 9x16] [--container mp4|webm] [--browser /path/to/chrome]
```

[`export-video.mjs`](export-video.mjs) is dependency-free and drives the browser over its DevTools pipe. It refuses to overwrite a file; when the browser cannot write the requested container it writes the other one and says so.

## Browser support

The browser needs WebCodecs video encoding and must allow reading back a canvas that drew an SVG `foreignObject` image. When either is missing, the export stops with a message and nothing is written. Fonts must be system fonts or embedded in the page; images must be inline data URIs, as the preview already requires.

| Browser | Status |
| --- | --- |
| Chromium 1194 (Linux, development container) | Verified: WebM VP9 and VP8; H.264 encoding not offered by this build |
| Chrome or Edge on Windows or macOS | Expected to offer H.264, not verified |
| Firefox | Not verified |
| Safari | Not verified; drawing `foreignObject` may block reading the canvas |

## Verification boundary

During package preparation, in a Linux development container with Chromium 1194: drawn frames matched the Remotion still of the same frame pixel for pixel; the captioned starter exported in 16:9 and 9:16 as VP9 WebM files with 300 frames and 10.00 s that ffprobe read, at about 42 dB PSNR against the reference screenshots, in about 2.5 seconds each; the preview's button produced a download named per format. The MP4 writer was verified with an H.264 stream from libx264 instead of a browser encoder: ffprobe reported High profile, 300 frames and 10.00 s, and all frames decoded in order. Browser H.264 encoding, other browsers and host behavior are not verified.
