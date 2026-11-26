#!/usr/bin/env python3
"""Builds PizarraPad's information pages into public/. The board app itself is public/board/index.html.
Run: python3 tools/build.py   (standard library only)"""
import json, os, html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
CFG = json.load(open(os.path.join(ROOT, 'site.config.json')))
E = lambda s: html.escape(str(s), quote=True)
URL = CFG['site_url'].rstrip('/')
NAME = CFG['site_name']; ST = CFG['studio']; MAIL = CFG['contact_email']

LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#203A2F"/>'
        '<path d="M8 21c3-6 5-9 7-9s1 7 3 7 3-5 6-8" fill="none" stroke="#F2F0E4" stroke-width="2.4" stroke-linecap="round"/></svg>')


import hashlib as _h
CSSV = _h.md5(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', 'assets', 'site.css'), 'rb').read()).hexdigest()[:8]

# ---------------------------------------------------------------- Telar Labs family links
FAMILY = [f for f in CFG.get('family', []) if f['name'] != CFG['site_name']]
HUB = CFG.get('studio_url', '')

def slug_app(n): return ''.join(ch for ch in n.lower() if ch.isalnum())

def family_row():
    if not FAMILY: return ''
    head = f'<a href="{E(HUB)}">More from {E(CFG["studio"])}</a>' if HUB else f'More from {E(CFG["studio"])}'
    links = ''.join(f'<a class="app-{slug_app(f["name"])}" href="{E(f["url"])}" title="{E(f["blurb"])}">{E(f["name"])}</a>' for f in FAMILY)
    return f'<div class="wrap family"><span class="family-h">{head}:</span>{links}</div>'

def family_promo(title):
    if not FAMILY: return ''
    links = ''.join(f'<a class="app-{slug_app(f["name"])}" href="{E(f["url"])}"><b>{E(f["name"])}</b><span>{E(f["blurb"])}</span></a>' for f in FAMILY)
    return f'<section class="wrap section family-promo"><h2>{title}</h2><div class="family-links">{links}</div></section>'

def ad(key):
    slot = CFG['ad_slots'].get(key, '')
    if not (CFG['adsense_client'] and slot): return ''
    return (f'<div class="ad"><span class="ad-label">Advertisement</span><ins class="adsbygoogle" style="display:block" data-ad-client="{E(CFG["adsense_client"])}" '
            f'data-ad-slot="{E(slot)}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')

def page(path, title, desc, body):
    full = title if NAME in title else f'{title} | {NAME}'
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={E(CFG["adsense_client"])}" crossorigin="anonymous"></script>'
           if CFG['adsense_client'] else '')
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(URL + path)}">
<meta property="og:title" content="{E(full)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{E(URL + path)}">
<meta property="og:image" content="{E(URL)}/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#1D7A50">
<link rel="preload" href="/assets/fonts/atkinson-hyperlegible-400.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/site.css?v={CSSV}">
{ads}
</head>
<body>
<header class="top"><div class="wrap top-in">
  <span class="tl-wrap"><a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a><a class="tl-by" href="https://telarlabs.net" title="Telar Labs home"><span>by </span>Telar Labs</a><style>.tl-wrap{{display:flex;align-items:center;min-width:0}}.tl-by{{margin-left:10px;font-size:13px;font-weight:500;line-height:1;color:inherit;opacity:.65;text-decoration:none;white-space:nowrap;flex:none}}.tl-by:hover{{opacity:1;text-decoration:underline}}@media(max-width:560px){{.tl-wrap{{flex-direction:column;align-items:flex-start}}.tl-by{{margin:3px 0 0;font-size:11.5px}}}}</style></span>
  <nav class="nav"><a href="/tools/">Classroom tools</a><a href="/how-to-use/">How to use</a><a href="/projector/">Use with a projector</a><a href="/guides/">Guides</a><a href="/about/">About</a></nav>
  <a class="btn btn-sm" href="/board/">Open the board</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
  <div><a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a>
  <p class="muted">A free whiteboard, blackboard and greenboard for teachers. Part of the {E(ST)} teacher tools.</p></div>
  <div class="foot-cols">
    <div><h4>Use it</h4><a href="/board/">Open the board</a><a href="/tools/">Classroom tools</a><a href="/tools/timer/">Classroom timer</a><a href="/tools/random-name-picker/">Random name picker</a><a href="/tools/spinner-wheel/">Spinner wheel</a><a href="/tools/pomodoro-timer/">Pomodoro timer</a><a href="/how-to-use/">How to use</a><a href="/projector/">Use with a projector</a><a href="/guides/">Guides</a><a href="/faq/">FAQ</a></div>
    <div><h4><a href="https://telarlabs.net" style="color:inherit;margin:0">{E(ST)}</a></h4><a href="https://telarlabs.net">Telar Labs home</a><a href="https://telarlabs.net/guides/">Telar Labs guides</a><a href="/about/">About</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="/contact/">Contact</a></div>
  </div>
</div>{family_row()}<div class="wrap fine">&copy; {date.today().year} {E(ST)}.</div></footer>
</body>
</html>'''
    out = os.path.join(PUB, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(PUB, path.strip('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)

def prose(path, title, desc, inner):
    page(path, title, desc, f'<article class="wrap prose">{inner}</article>')

FEATURES = [
    ('Three boards', 'Switch between a clean whiteboard, a classic charcoal blackboard and a green chalkboard, with backgrounds for handwriting, math and music: lines, graph paper, dots, music staff, a number line and a 1–100 chart.'),
    ('Any pen, finger or mouse', 'Works with a Samsung S Pen, Apple Pencil, Surface Pen and other styluses (with pressure), your finger, a mouse, or the keyboard.'),
    ('Pen-only mode', 'Turn it on and your palm and fingers stop drawing. Fingers scroll and zoom instead, so you can rest your hand on the screen.'),
    ('Type when you prefer', 'Tap with the Text tool and type. Change the size, color or bold, and drag text to move it.'),
    ('Shapes, highlighter, laser', 'Straight lines, arrows, boxes and circles; a see-through highlighter; and a laser pointer that fades away.'),
    ('Add pictures', 'Insert a photo, diagram or worksheet picture, or snap one with your phone camera. Move and resize it, then write on top.'),
    ('Pages and saving', 'Add as many pages as your lesson needs. Everything saves on your device automatically. Save any page as an image, or the whole lesson as a PDF.'),
    ('Works offline', 'Once opened, the board keeps working even when the school Wi-Fi drops.'),
    ('English, Español, 中文, 日本語, 한국어, Русский', 'The board speaks English, Spanish, Simplified Chinese, Japanese, Korean and Russian, and picks your device language automatically.'),
    ('Free, no account', 'No sign-up, no limits on pages, no watermark. Open it and teach.'),
]

def home():
    feats = ''.join(f'<div class="feat"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in FEATURES)
    body = f'''
<section class="hero"><div class="wrap hero-in">
  <div class="hero-text">
    <p class="eyebrow">Free · No sign-up · Works offline</p>
    <h1>The free online board for teachers</h1>
    <p class="hero-sub">Whiteboard, blackboard or greenboard. Write with a stylus, your finger or a mouse, or just type, then show it on your projector or TV.</p>
    <div class="cta"><a class="btn btn-big" href="/board/">Open the board</a><a class="btn btn-ghost" href="/tools/">⏱ Classroom tools</a><a class="btn btn-ghost" href="/how-to-use/">See how it works</a></div>
  </div>
  <div class="hero-shot" aria-hidden="true">
    <div class="mock mock-green"><span class="chalk t1">Lesson 3: Adding Fractions</span><span class="chalk t2">½ + ¼ = ¾</span><svg viewBox="0 0 200 120"><circle cx="60" cy="60" r="40" fill="none" stroke="#9CCBFF" stroke-width="3"/><path d="M60 20v80M60 60h40" stroke="#9CCBFF" stroke-width="3"/><path d="M120 60h50m-12-10l12 10-12 10" fill="none" stroke="#FFB26B" stroke-width="3" stroke-linecap="round"/></svg></div>
    <div class="mock mock-white"><span class="ink">Photosynthesis</span><svg viewBox="0 0 200 60"><path d="M10 40c30-30 60 20 90-10s60 10 90-5" fill="none" stroke="#D7263D" stroke-width="3" stroke-linecap="round"/></svg></div>
  </div>
</div></section>
<section class="wrap section"><h2>Free classroom tools</h2><div class="feats">
<a class="feat" href="/tools/timer/" style="text-decoration:none;color:inherit"><h3>⏱ Classroom timer</h3><p>A big countdown for the projector, with color warnings and a gentle chime.</p></a>
<a class="feat" href="/tools/random-name-picker/" style="text-decoration:none;color:inherit"><h3>🎯 Random name picker</h3><p>Pick a student fairly, or make random groups.</p></a>
<a class="feat" href="/tools/dice/" style="text-decoration:none;color:inherit"><h3>🎲 Dice</h3><p>Roll up to six dice on the big screen for games and math.</p></a>
<a class="feat" href="/tools/noise-meter/" style="text-decoration:none;color:inherit"><h3>🔊 Noise meter</h3><p>Shows how loud the room is, so the class can keep it down.</p></a>
<a class="feat" href="/tools/pomodoro-timer/" style="text-decoration:none;color:inherit"><h3>🍅 Pomodoro timer</h3><p>Focus and break intervals, or your own steps and stations.</p></a>
<a class="feat" href="/tools/spinner-wheel/" style="text-decoration:none;color:inherit"><h3>🎡 Spinner wheel</h3><p>Spin a wheel of names, prizes or topics.</p></a>
<a class="feat" href="/tools/animal-race/" style="text-decoration:none;color:inherit"><h3>🐢 Animal race</h3><p>Cute animals race to the finish to pick a winner.</p></a>
<a class="feat" href="/tools/icebreaker-cards/" style="text-decoration:none;color:inherit"><h3>💬 Icebreaker cards</h3><p>Would you rather, this or that, quick draw and more.</p></a></div>
<p><a href="/tools/">All classroom tools →</a></p></section>
<section class="wrap section"><h2>Everything you need at the front of the class</h2><div class="feats">{feats}</div></section>
{ad("home")}
<section class="wrap section steps-sec"><h2>Start in three steps</h2>
<ol class="steps"><li><h3>Open the board</h3><p>Go to <a href="/board/">the board</a> on your laptop, tablet or phone. To use it like an app, tap ⋯ and <b>Install PizarraPad as an app</b>, or add it to your home screen.</p></li>
<li><h3>Pick your board and tools</h3><p>Tap ⋯ to choose whiteboard, blackboard or greenboard and plain, lined or grid. Pick the pen, color and thickness in the tool bar.</p></li>
<li><h3>Show it to the class</h3><p>Connect your laptop to the projector or TV, or mirror your tablet. <a href="/projector/">See the options</a>.</p></li></ol></section>
<section class="wrap section"><h2>Coming next</h2><div class="feats">
<div class="feat"><h3>Maps and worksheets library</h3><p>Ready-made maps, graphs and worksheet pages you can drop onto the board and write on.</p></div>
<div class="feat"><h3>Phone-to-projector sync</h3><p>Write on your phone or tablet anywhere in the room while the board appears on the projector computer. No cables.</p></div></div></section>
<section class="wrap section"><div class="callout"><h2>Built for real classrooms</h2><p>Big buttons for tablets, readable from the back row, and it keeps working when the internet doesn't. PizarraPad is free because the information pages show a few ads; the board itself never shows ads while you teach.</p><a class="btn" href="/board/">Open the board</a></div></section>'''
    body += ('<section class="wrap section"><h2>Guides for teachers</h2><ul class="glist" style="list-style:none;padding:0;display:grid;gap:12px">' + ''.join(f'<li style="border:1px solid var(--line);border-radius:12px;padding:14px 16px"><a href="/guides/{g["slug"]}/" style="font-weight:700">{E(g["title"])}</a></li>' for g in GUIDES) + '</ul><p><a href="/guides/">All guides →</a></p></section>')
    body += family_promo('More free tools for teachers')
    page('/', f'{NAME} – Free Online Whiteboard, Blackboard & Greenboard for Teachers',
         'Free online whiteboard, blackboard and greenboard for teachers. Write with a stylus, finger or mouse, or type. Works offline, no sign-up.', body)

def pages():
    prose('/how-to-use/', 'How to Use PizarraPad', 'Step-by-step guide to the PizarraPad tools: pen, highlighter, eraser, text, shapes, laser, pages and saving.', f'''
<h1>How to use {E(NAME)}</h1>
<p class="lead">A quick tour of every tool. It takes about two minutes to learn.</p>
<h2>The tool bar</h2>
<ul>
<li><b>Pen:</b> write and draw. With a stylus, lines get thicker when you press harder. Tap Pen again to change color and thickness.</li>
<li><b>Highlight:</b> a see-through marker for underlining or shading.</li>
<li><b>Eraser:</b> drag over any stroke, shape or text to remove it.</li>
<li><b>Text:</b> tap anywhere and type. Tap existing text to edit it, or drag it to move it. Choose size and bold in the Color panel.</li>
<li><b>Shape:</b> drag to draw a line, arrow, box or circle. Pick which one in the Color panel.</li>
<li><b>Image:</b> add a picture from your device (on a phone or tablet you can also take a photo). Drag it to move it, drag the round corner to resize, and tap × to remove it. Your writing always stays on top. You can also paste an image or drag one onto the board.</li>
<li><b>Laser:</b> point at things for the class; the trail fades after a second.</li>
<li><b>Undo / Redo:</b> step back or forward. Keyboard: Ctrl+Z and Ctrl+Y (⌘ on Mac).</li>
<li><b>Hide:</b> tucks the tool bar away for a clean screen. Tap <b>Tools</b> to bring it back.</li>
</ul>
<h2>Board and background</h2>
<p>Tap <b>⋯</b> at the top right to choose <b>Whiteboard</b>, <b>Blackboard</b> or <b>Greenboard</b>; a <b>Plain</b>, <b>Lines</b> (handwriting guide) or <b>Grid</b> background. Pen colors adjust automatically so they're easy to see on each board.</p>
<h2>Language</h2>
<p>The board's buttons and menus come in <b>English</b>, <b>Español</b>, <b>中文</b> (Simplified Chinese), <b>日本語</b> (Japanese), <b>한국어</b> (Korean) and <b>Русский</b> (Russian). It follows your device language at first; change it any time under <b>⋯ → Language</b>.</p>
<h2>Writing with a stylus (Pen only)</h2>
<p>Turn on <b>Pen only</b> at the top. Your stylus draws, while fingers scroll and pinch-zoom, so resting your palm on a tablet won't leave marks. Turn it off if you want to draw with your finger.</p>
<h2>Moving around</h2>
<ul><li><b>Tablet or phone:</b> two fingers to scroll and pinch to zoom (one finger too, when Pen only is on).</li>
<li><b>Computer:</b> scroll with the mouse wheel or trackpad; hold Ctrl (⌘ on Mac) and scroll to zoom; drag with the middle or right mouse button to move.</li>
<li><b>Fit button</b> (four corners): shows everything on the page at once.</li></ul>
<h2>Pages</h2>
<p>Use <b>+</b> to add a page after the current one, and the arrows to move between pages. Each page has its own undo history.</p>
<h2>Saving your work</h2>
<p>Everything saves on your device automatically, so you can close the tab and come back later. To keep a copy or share it, choose <b>⋯ → Save page as image</b>. <b>Clear page</b> empties the current page (Undo brings it back); <b>Start a new board</b> erases all pages.</p>
<h2>Keyboard shortcuts</h2>
<p><b>P</b> pen · <b>H</b> highlight · <b>E</b> eraser · <b>T</b> text · <b>S</b> shape · <b>I</b> image · <b>L</b> laser · <b>Esc</b> close menus</p>
<p><a class="btn" href="/board/">Open the board</a></p>''')
    prose('/projector/', 'Use PizarraPad with a Projector or TV', 'How to show PizarraPad on a classroom projector, TV or smart board from a laptop, tablet or phone.', f'''
<h1>Use {E(NAME)} with a projector or TV</h1>
<p class="lead">{E(NAME)} runs in the browser, so it shows on any screen your device can connect to. Pick the setup that matches your classroom.</p>
<h2>1. Laptop connected to the projector (easiest)</h2>
<ol><li>Connect the laptop with an HDMI or VGA cable.</li><li>On Windows press <b>Windows + P</b> and choose <b>Duplicate</b>; on a Mac open <b>Displays</b> and choose <b>Mirror</b>.</li>
<li>Open {E(NAME)} and choose <b>⋯ → Full screen</b>.</li><li>Write with the mouse, a touchpad, or a cheap drawing tablet, or type.</li></ol>
<h2>2. Tablet or phone mirrored to the screen</h2>
<p>Write by hand on a tablet while the class watches the big screen.</p>
<ul><li><b>Android (Samsung and others):</b> use <b>Smart View</b> or <b>Cast</b> to a smart TV or a Chromecast; or use a USB-C to HDMI adapter (most Samsung Galaxy Tab S models support this).</li>
<li><b>iPad / iPhone:</b> use <b>Screen Mirroring</b> to an Apple TV or AirPlay TV, or a Lightning/USB-C to HDMI adapter.</li>
<li><b>Windows tablets:</b> press <b>Windows + K</b> to connect to a Miracast display.</li></ul>
<h2>3. Interactive board or smart TV with a browser</h2>
<p>Open {E(NAME)} in the board's built-in browser and write with its pen or your finger.</p>
<h2>Tips for the back row</h2>
<ul><li>Use the <b>Thick</b> pen and <b>Large</b> text.</li><li>On bright projectors, the <b>Blackboard</b> or <b>Greenboard</b> with yellow or white chalk is easiest to read.</li>
<li>Hide the tool bar for a clean screen while you explain.</li>
<li>Write in the middle of the page. The edges of a projected image are often cut off or blurry, especially on older projectors.</li>
<li>Use color with a purpose: one color for the main idea, a second for examples, red only for corrections. Too many colors are harder to read from far away.</li>
<li>Pale colors like yellow look great on the blackboard but almost disappear on the whiteboard. Switch boards rather than fighting the projector.</li></ul>

<h2>Before the lesson: a 3-minute check</h2>
<ol><li>Open {E(NAME)} on the device you will teach with, once, while you have internet. After that it keeps working if the Wi-Fi drops.</li>
<li>Connect to the projector or TV and switch to full screen.</li>
<li>Walk to the back of the room and look. Write one line with the pen size and color you plan to use.</li>
<li>Turn off sleep for the lesson: set the screen timeout to 30 minutes or more, and plug the device in.</li>
<li>Turn off notifications, or use Do Not Disturb, so messages don’t pop up on the big screen.</li></ol>

<h2>Common problems and fixes</h2>
<table class="tbl"><thead><tr><th>Problem</th><th>Try this</th></tr></thead><tbody>
<tr><td>The projector shows “No signal”.</td><td>Check that the cable is pushed in firmly at both ends, then choose the right input on the projector (HDMI 1, HDMI 2 or VGA). On Windows, press Windows + P again and choose Duplicate.</td></tr>
<tr><td>The picture is cut off at the edges.</td><td>Look for <b>Aspect ratio</b> or <b>Zoom</b> in the projector menu and choose 16:9 or Auto. On a laptop, try a lower screen resolution, like 1280 × 720.</td></tr>
<tr><td>Everything looks tiny.</td><td>Use full screen, the Thick pen and Large text. Zoom in on the board with two fingers or Ctrl and the mouse wheel.</td></tr>
<tr><td>Casting is slow or lags behind my pen.</td><td>Move closer to the TV or Wi-Fi router, close other apps, or use a cable. Cables never lag.</td></tr>
<tr><td>My hand draws lines while I write on the tablet.</td><td>Turn on <b>Pen only</b>. Your palm and fingers stop drawing, and fingers scroll and zoom instead.</td></tr>
<tr><td>The colors look washed out.</td><td>Close the curtains or turn off the lights near the screen, and use the Blackboard or Greenboard.</td></tr></tbody></table>

<h2>After class</h2>
<p>Your pages are saved on your device automatically. Use <b>Save page as image</b> to keep a copy or to share a page with students who were absent, for example in your class group chat or learning system.</p>
<p>For lesson ideas, see our guides on <a href="https://telarlabs.net/guides/projector-tv-classroom-whiteboard/">using a projector or TV as a classroom whiteboard</a> and <a href="https://telarlabs.net/guides/whiteboard-activities-projector-classroom/">whiteboard activities for the projector classroom</a>.</p>
<p class="muted">Coming soon: write on your phone or tablet and have it appear on the projector computer automatically, without cables, plus a library of maps and worksheets.</p>''')
    faq = [('Is PizarraPad really free?', 'Yes. There is no paid plan, no sign-up and no page limit. The information pages show a few ads to cover costs; the board itself never shows ads.'),
           ('Do I need to create an account?', 'No. Open the board and start teaching.'),
           ('Where is my work saved?', 'In your browser on your own device. Nothing is uploaded to our servers. Clearing your browser data will remove saved boards, so save important pages as images.'),
           ('Does it work without internet?', 'Yes. After you open the board once while online, it keeps working offline in the same browser.'),
           ('Which styluses work?', 'Any stylus your device supports as a pen: Samsung S Pen, Apple Pencil, Surface Pen, Wacom and others. Pressure sensitivity works where the device provides it.'),
           ('Can students use it?', 'Yes, it works on any device with a browser. Each device keeps its own boards.'),
           ('Can I install it like an app?', 'Yes. In Chrome or Edge choose "Install app" or "Add to home screen"; on iPad/iPhone use Share → Add to Home Screen.'),
           ('Can I add pictures?', 'Yes. Use the Image tool to add a photo, diagram or worksheet picture, then write on top of it. Pictures are saved on your device with the board.'),
           ('Which languages does the board support?', 'English, Spanish (Español), Simplified Chinese (中文), Japanese (日本語), Korean (한국어) and Russian (Русский). Change it under ⋯ → Language.'),
           ('How do I undo a mistake?', 'Tap Undo, or press Ctrl+Z on a keyboard. Redo brings it back. Even Clear page can be undone.'),
           ('What is Pen only mode?', 'With Pen only turned on, only a stylus draws. Your palm and fingers scroll and zoom instead, so you can rest your hand on the screen while you write, like on paper.'),
           ('Which backgrounds are there?', 'Three boards (whiteboard, blackboard and greenboard), each with a plain, lined or grid background. Lines help with handwriting and grids with math, graphs and tables.'),
           ('How many pages can I make?', 'As many as your lesson needs. Use the arrows to move between pages. Pages are saved on your device until you start a new board.'),
           ('How do I share a page with students?', 'Use Save page as image, then send the picture in your class chat, email or learning system. Students who were absent can see exactly what was on the board.'),
           ('How do I start fresh for the next class?', 'Choose Start a new board. It erases all pages on this device, so save any page you need as an image first. To clear just one page, use Clear page.'),
           ('Can I show it on a projector or TV?', 'Yes. Connect your laptop with a cable, or mirror a tablet or phone to a TV. See Use with a projector for step-by-step setups and fixes for common problems.'),
           ('Does it work on cheap tablets and older laptops?', 'Usually, yes. It runs in any modern browser (Chrome, Edge, Safari, Samsung Internet or Firefox) and doesn’t need a fast connection after the first visit.'),
           ('Can I use my phone with the projector computer?', 'Not yet. Writing on your phone or tablet while the board shows on the projector computer is coming soon, along with a library of maps and worksheets.')]
    prose('/faq/', 'Frequently Asked Questions', f'Answers to common questions about {NAME}.', '<h1>Frequently asked questions</h1>' + ''.join(f'<h2>{E(q)}</h2><p>{E(a)}</p>' for q, a in faq))
    prose('/about/', 'About', f'About {NAME}, the free online board for teachers, by {ST}.', f"""
<h1>About {E(NAME)}</h1>
<p class="lead">{E(NAME)} is a free online board for teachers, made by {E(ST)}, a small independent studio.</p>
<p>Many classrooms have a projector or TV but no expensive interactive board. Teachers end up using slides that can't be written on, or apps with sign-ups, page limits and watermarks. {E(NAME)} gives every teacher a board they can write on with whatever they have: a laptop and mouse, a tablet and stylus, or a phone.</p>
<p>The name comes from <i>pizarra</i>, the Spanish word for blackboard.</p>

<h2>Who it’s for</h2>
<ul><li><b>Teachers with a projector or TV</b> who want to write and draw during the lesson, not just show slides.</li>
<li><b>Teachers with a tablet and stylus</b> who want to write by hand while the class watches the big screen.</li>
<li><b>Tutors and online teachers</b> who share their screen in a video call and need a quick board.</li>
<li><b>Students</b> who want to work out a problem or practice handwriting on lined or grid pages.</li></ul>

<h2>How it’s designed</h2>
<ul><li><b>Familiar boards.</b> Whiteboard, blackboard and greenboard, with plain, lined or grid backgrounds, so it feels like the board you already know.</li>
<li><b>Easy to read from the back row.</b> Thick pens, large text, a highlighter and a laser pointer are one tap away.</li>
<li><b>Made for real hands.</b> Pen-only mode lets you rest your palm on the screen. Pressure works with styluses that support it.</li>
<li><b>Keeps working when the Wi-Fi drops.</b> After the first visit, the board works offline in the same browser.</li>
<li><b>Three languages.</b> English, Spanish and Simplified Chinese, chosen automatically from your device.</li></ul>

<h2>Your work stays with you</h2>
<p>Boards are saved in your browser on your own device, not on our servers. There’s nothing to sign up for and nothing to delete later. To keep a page, save it as an image. Details are in our <a href="/privacy/">privacy policy</a>.</p>

<h2>Our promises</h2>
<ul><li>The board stays free, with no sign-up.</li><li>Your boards stay on your device.</li><li>No ads on the board while you teach.</li></ul>

<h2>Get started</h2>
<p><a href="/board/">Open the board</a>, read <a href="/how-to-use/">how to use it</a>, or set it up with <a href="/projector/">a projector or TV</a>.</p>

<h2>Other {E(ST)} tools</h2>
<p>{E(ST)} also makes <a href="https://quizpolice.telarlabs.net">QuizPolice</a> for monitored online quizzes, <a href="https://drafttrail.telarlabs.net">DraftTrail</a>, a writing-process recorder, <a href="https://clips.telarlabs.net">Telar Clips</a>, free motion backgrounds for videos, and <a href="https://tixward.telarlabs.net">Tixward</a>, event tickets and bookings for school events.</p>
<p>Questions or ideas? <a href="/contact/">Contact us</a>.</p>""")
    ads_p = ('<p>Some information pages show ads from Google AdSense. Google and its partners use cookies to show ads based on your visits to this and other websites. You can turn off personalized ads in '
             '<a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>, and learn more at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites that use its services</a>. '
             'Visitors in the EEA, the UK and Switzerland are asked for consent first. The board page itself shows no ads.</p>')
    prose('/privacy/', 'Privacy Policy', f'Privacy policy for {NAME}.', f'''
<h1>Privacy policy</h1>
<p class="lead">{E(NAME)} is run by {E(ST)}. In short: your boards stay on your device, and we don't ask who you are.</p>
<h2>Your boards</h2><p>Everything you write is saved in your own browser's storage on your device. It is not sent to us. If you clear your browser data, your saved boards are deleted.</p>
<h2>No accounts</h2><p>We don't ask for your name, email or school to use the board.</p>
<h2>Advertising</h2>{ads_p}
<h2>Analytics</h2><p>We use Cloudflare Web Analytics to count page visits. It does not use cookies and does not track you across websites.</p>
<h2>Hosting</h2><p>The site is hosted on Cloudflare, whose servers may record basic technical information (such as IP address and browser type) to keep the service secure and working.</p>
<h2>Children</h2><p>Teachers and students of all ages can use the board. We don't knowingly collect personal information from children, and the board page doesn't show ads.</p>
<h2>Contact</h2><p><a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated {E(CFG["launch_date"])}.</p>''')
    prose('/terms/', 'Terms of Use', f'Terms of use for {NAME}.', f'''
<h1>Terms of use</h1>
<p class="lead">{E(NAME)} is free to use for teaching, studying, meetings and personal projects.</p>
<ul><li>What you create on the board belongs to you.</li><li>Please don't use the service for anything illegal or to harm others.</li>
<li>The board is provided as it is, without warranty. Keep copies of important work by saving pages as images; {E(ST)} isn't responsible for lost boards (for example, after clearing browser data).</li>
<li>We may update features or these terms; the date below shows the latest version.</li></ul>
<p>Questions: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated {E(CFG["launch_date"])}.</p>''')
    prose('/contact/', 'Contact', f'Contact {NAME}.', f'''
<h1>Contact us</h1><p class="lead">Ideas, problems or a feature your classroom needs? We'd like to hear it.</p>
<p>Email: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p>Tell us your device (for example "Samsung Tab S6 Lite, Chrome") if something isn't working.</p>''')

def extras():
    open(os.path.join(PUB, 'favicon.svg'), 'w').write(LOGO.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" '))
    urls = ['/', '/board/', '/how-to-use/', '/projector/', '/faq/', '/guides/'] + [f'/guides/{g["slug"]}/' for g in GUIDES] + ['/tools/', '/tools/whiteboard-backgrounds/'] + [t[0] for t in TOOLS] + ['/about/', '/privacy/', '/terms/', '/contact/']
    open(os.path.join(PUB, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{URL}{u}</loc></url>\n' for u in urls if u != '/board/') + '</urlset>\n')
    open(os.path.join(PUB, 'robots.txt'), 'w').write(f'User-agent: *\nDisallow: /cdn-cgi/\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n')
    if CFG['adsense_client']:
        open(os.path.join(PUB, 'ads.txt'), 'w').write(f'google.com, {CFG["adsense_client"].replace("ca-", "")}, DIRECT, f08c47fec0942fa0\n')
    page('/404.html', 'Page not found', 'Page not found.', '<section class="wrap prose"><h1>Page not found</h1><p><a class="btn" href="/board/">Open the board</a></p></section>')


# ---------------------------------------------------------------- help guides (content pages)
import sys as _sys; _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides_content import GUIDES, LEAD as GUIDES_LEAD
GUIDE_STYLE = ('<style>.glist{list-style:none;padding:0;display:flex;flex-direction:column;gap:14px}.glist li{border:1px solid var(--line);border-radius:12px;padding:14px 16px}'
               '.glist a{font-weight:700}.glist p{margin:6px 0 0}.gmeta{font-size:14px;margin:0 0 6px}</style>')
def guides():
    items = ''.join(f'<li><a href="/guides/{g["slug"]}/">{E(g["title"])}</a><p class="muted">{E(g["desc"])}</p></li>' for g in GUIDES)
    prose('/guides/', f'{NAME} Guides for Teachers', f'{GUIDES_LEAD}', f'{GUIDE_STYLE}<h1>Guides</h1><p class="lead">{E(GUIDES_LEAD)}</p><ul class="glist">{items}</ul>'
          f'<p>More guides for teachers and organizers: <a href="https://telarlabs.net/guides/">Telar Labs guides</a>.</p>')
    for g in GUIDES:
        more = ''.join(f'<li><a href="/guides/{o["slug"]}/">{E(o["title"])}</a></li>' for o in GUIDES if o is not g)
        prose(f'/guides/{g["slug"]}/', g['title'], g['desc'],
              f'{GUIDE_STYLE}<p class="gmeta muted"><a href="/guides/">Guides</a> · Updated {E(g["updated"])}</p><h1>{E(g["title"])}</h1>{g["body"]}'
              f'<h2>More guides</h2><ul>{more}<li><a href="https://telarlabs.net/guides/">Telar Labs guides for teachers and organizers</a></li></ul>')

# ---------------------------------------------------------------- classroom tools
from tools_content import TOOLS, HUB as TOOLS_HUB, CSS as TOOLS_CSS, BG_PAGE
from tools_more import TOOLS_MORE
TOOLS = TOOLS + TOOLS_MORE
TOOLS_HUB = TOOLS_HUB.replace('<a href="/tools/whiteboard-backgrounds/">', ''.join(f'<a href="{t[0]}"><b>{t[2]}</b>{t[6]}</a>' for t in TOOLS_MORE) + '<a href="/tools/whiteboard-backgrounds/">', 1)
def tools():
    prose('/tools/', 'Free Classroom Tools: Timer, Pomodoro, Spinner Wheel, Name Picker, Icebreakers', 'Free classroom tools for the projector: a countdown timer, Pomodoro timer, spinner wheel, animal race, random name picker with groups, icebreaker cards, dice and a noise meter. No sign-up, private, works offline.',
          f'{TOOLS_CSS}<h1>Classroom tools</h1>{TOOLS_HUB}')
    for path, title, short, desc, tool, text, _ in TOOLS:
        more = ''.join(f'<li><a href="{p}">{E(s)}</a></li>' for p, _, s, _, _, _, _ in TOOLS if p != path)
        prose(path, title, desc, f'{TOOLS_CSS}<p class="muted" style="font-size:14px;margin:0 0 6px"><a href="/tools/">Classroom tools</a></p><h1>{E(short)}</h1>{tool}{text}'
              f'<h2>More classroom tools</h2><ul>{more}<li><a href="/board/">The PizarraPad whiteboard</a></li></ul>')
    prose(BG_PAGE[0], BG_PAGE[1], BG_PAGE[2], f'<p class="muted" style="font-size:14px;margin:0 0 6px"><a href="/tools/">Classroom tools</a></p><h1>Whiteboard backgrounds</h1>{BG_PAGE[3]}')

if __name__ == '__main__':
    home(); pages(); guides(); tools(); extras(); print('Built PizarraPad pages')

    # AdSense: no ad code on error, contact and legal pages (no publisher content)
    import re as _re
    for _p in ('404.html', 'contact/index.html', 'privacy/index.html', 'terms/index.html'):
        _f = os.path.join(PUB, _p)
        if os.path.exists(_f):
            _s = open(_f).read()
            _s = _re.sub(r'<script async src="https://pagead2\.googlesyndication\.com[^>]*></script>', '', _s)
            _s = _re.sub(r'<div class="ad">.*?</ins>(<script>.*?</script>)?</div>', '', _s, flags=_re.S)
            open(_f, 'w').write(_s)

    # old *.pages.dev address: send fresh visitors to the real domain (tools/home_domain.py)
    import home_domain as _hd; _hd.inject(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public'))
    import sitemap_lastmod as _sl; _sl.stamp(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public'))
