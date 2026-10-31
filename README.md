# PizarraPad

Free online whiteboard, blackboard and greenboard for teachers, by Telar Labs.

- `public/board/index.html` – the board app (single file, works offline via `public/sw.js`)
- `tools/build.py` – builds the home, help, FAQ, about, privacy, terms and contact pages
- `site.config.json` – site address, contact email, AdSense IDs

## Cloudflare Pages settings
- Framework preset: None
- Build command: `python3 tools/build.py`
- Build output directory: `public`

AdSense: put your `ca-pub-…` ID in `adsense_client` and an ad unit number in `ad_slots.home`. Ads only appear on the information pages, never on the board.
