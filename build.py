"""Build the single-page portfolio from the approved copy and supplied photos."""
from pathlib import Path
from html import escape as esc
import json

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
projects=json.loads((ROOT/'content.json').read_text())
photos=json.loads((ROOT/'photos.json').read_text())
intro=json.loads((ROOT/'intro.json').read_text())
favicon=(ROOT/'favicon-data.txt').read_text()

def document(title,body,extra=''):
    desc='Woodworking and design by Ishan Gokhale. Furniture, tableware, and handmade objects.'
    return f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#000000"><title>{esc(title)}</title><meta name="description" content="{desc}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><link rel="icon" type="image/svg+xml" href="{favicon}"><link rel="stylesheet" href="/style.css?v=6">{extra}</head><body>{body}</body></html>\n'

header='<a class="skip" href="#main">Skip to content</a><header class="header shell"><a class="brand" href="/">Ishan Gokhale</a></header>'
footer='<footer id="contact" class="footer shell"><div class="footer-top"><div class="contact-links"><a href="mailto:idgokhale@gmail.com">idgokhale@gmail.com</a></div></div><div class="footer-bottom"><span>© 2026 Ishan Gokhale</span><a href="https://www.linkedin.com/in/ishan-gokhale" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="#top">Back to top ↑</a></div></footer>'
# The introduction and portfolio now share one page.
lead='<section id="about" class="welcome shell" aria-label="Introduction"><h1 class="name-slot"><a class="hero-name" href="#top">Ishan Gokhale</a></h1><div class="welcome-content"><p class="welcome-role">Product designer &amp; woodworker</p><div class="welcome-bio"><p class="bio-heading">'+esc(intro['heading'])+'</p>'
for paragraph in intro['paragraphs']:
    lead+='<p>'+esc(paragraph).replace('say hi','<a href="mailto:idgokhale@gmail.com?subject=hi">say hi</a>')+'</p>'
lead+='</div><a class="scroll-cue" href="#work">Scroll down to see my work <span aria-hidden="true">↓</span></a></div></section>'
home_header='<a class="skip" href="#work">Skip to work</a><header class="site-header"><div class="shell"></div></header>'
body=home_header+'<main id="main">'+lead+'<section id="work" class="projects shell" aria-label="Woodworking projects">'
assert len(projects)==len(photos)==30
for number,(p,photo) in enumerate(zip(projects,photos),1):
    assert photo['number']==number
    ratio=photo['width']/photo['height'];shape='portrait' if ratio<.9 else 'square' if ratio<1.1 else 'landscape'
    sizes='(max-width: 600px) calc(100vw - 40px), (max-width: 900px) 55vw, '+('480px' if shape=='portrait' else '620px' if shape=='square' else '720px')
    srcset=', '.join(f'{v["path"]} {v["width"]}w' for v in photo['variants'])
    loading='loading="eager" fetchpriority="high"' if number==1 else 'loading="lazy"'
    body+=f'<article id="{p["id"]}" class="project {shape}" aria-labelledby="title-{number}"><figure><img src="{photo["variants"][-2]["path"]}" srcset="{srcset}" sizes="{sizes}" width="{photo["width"]}" height="{photo["height"]}" alt="{esc(p["title"])} — {esc(p["wood"])}" {loading} decoding="async"></figure><div class="description"><h2 id="title-{number}">{esc(p["title"])}</h2><p class="wood">{esc(p["wood"])}</p><p class="sentence">{esc(p["sentence"])}</p></div></article>'
body+='</section></main>'+footer+'<script src="/intro.js?v=6" defer></script>'
(OUT/'index.html').write_text(document('Ishan Gokhale — Design & Woodworking',body.replace('<body>','<body id="top">')).replace('<body>','<body id="top">'))

# Retain old incoming links, but lead them to their place in the one-page portfolio.
aliases={p['id']:p['id'] for p in projects}
aliases.update({'about':'about','contact':'contact','cutting-boards':'checkered-cutting-board','small-objects':'dragonfly-tableware'})
for route,anchor in aliases.items():
    target='/#'+anchor;folder=OUT/route;folder.mkdir(exist_ok=True)
    content=f'<main class="shell error"><p>This project is now part of the main portfolio.</p><a href="{target}">View the portfolio</a></main>'
    (folder/'index.html').write_text(document('Ishan Gokhale — Portfolio',content,f'<meta http-equiv="refresh" content="0;url={target}">'))
error=header+'<main id="main" class="shell error"><h1>Page not found.</h1><p><a href="/">Return to the portfolio</a></p></main>'
(OUT/'404.html').write_text(document('Page not found — Ishan Gokhale',error))
(OUT/'404').mkdir(exist_ok=True);(OUT/'404/index.html').write_text((OUT/'404.html').read_text())
print('Built single-page introduction and portfolio; retained 30 ordered projects.')
