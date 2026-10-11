"""Generate a portable, static research website from content.json."""
from pathlib import Path
from html import escape as esc
import json

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text())
topics = data['topics']

def source_html(fig):
    text = esc(fig['credit'])
    if fig.get('source'):
        text = f'<a href="{esc(fig["source"])}" target="_blank" rel="noopener noreferrer">{text}</a>'
    if fig.get('license'):
        text += f' · <a href="{esc(fig["license"])}" target="_blank" rel="noopener noreferrer">License</a>'
    return text

def figure_html(fig, group, number, hidden=False):
    return f'''<figure class="research-figure" id="{group}-figure-{number}" {'hidden' if hidden else ''}>
      <div class="figure-image"><img src="assets/{esc(fig['src'])}" alt="{esc(fig['alt'])}" loading="lazy" decoding="async"></div>
      <figcaption><div class="figure-title-row"><h4>{esc(fig['title'])}</h4><button class="expand-figure" type="button" aria-label="Expand {esc(fig['title'])}">Expand <span aria-hidden="true">↗</span></button></div>
      <p>{esc(fig['caption'])}</p><small>{source_html(fig)}</small></figcaption>
    </figure>'''

sections = []
for topic in topics:
    figure_controls = ''.join(f'<button type="button" class="figure-choice" aria-pressed="{str(i == 0).lower()}" aria-controls="{topic["id"]}-figure-{i}">{esc(f["short"])}</button>' for i, f in enumerate(topic['figures']))
    figures = ''.join(figure_html(f, topic['id'], i, i != 0) for i, f in enumerate(topic['figures']))
    links = ''.join(f'<a class="text-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>' for label, url in topic['links'])
    tags = ''.join(f'<li>{esc(tag)}</li>' for tag in topic['tags'])
    status = f'<span class="research-status">{esc(topic["status"])}</span>' if topic.get('status') else ''
    sections.append(f'''<section class="topic-section" id="{topic['id']}" aria-labelledby="{topic['id']}-title">
      <div class="topic-copy"><p class="eyebrow">Research focus {status}</p><h3 id="{topic['id']}-title">{esc(topic['name'])}</h3>
      <p class="topic-subtitle">{esc(topic['subtitle'])}</p><p>{esc(topic['body'])}</p><p>{esc(topic['detail'])}</p>
      <ul class="research-tags" aria-label="Methods and interests">{tags}</ul><div class="topic-links">{links}</div></div>
      <div class="figure-gallery"><div class="gallery-controls" aria-label="Choose a {esc(topic['name'])} figure">{figure_controls}</div>{figures}</div>
    </section>''')

nav = ''.join(f'<a href="#{t["id"]}">{esc(t["name"])}</a>' for t in topics)
works = ''.join(f'''<li><a href="{esc(w[4])}" target="_blank" rel="noopener noreferrer"><div><span class="work-type">{esc(w[3])}</span><h3>{esc(w[0])}</h3><p>{esc(w[1])} <span aria-hidden="true">·</span> {esc(w[2])}</p></div><span class="work-arrow" aria-hidden="true">↗</span></a></li>''' for w in data['works'])
hero = next(t for t in topics if t['id'] == 'contact-networks')['figures'][1]

html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Khaled M. Elokely, PhD | Research</title>
  <meta name="description" content="Khaled M. Elokely's research at the University of Wyoming: medicinal chemistry, data curation, protein contact networks, molecular kinetics, FragFlow, and KChiro.">
  <meta name="theme-color" content="#173f36">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="styles.css"><script src="site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="#home" aria-label="Khaled M. Elokely, home"><span class="brand-mark">KE</span><span>Elokely <b>Research</b></span></a>
  <nav aria-label="Main navigation"><a href="#research">Research</a><a href="#selected-work">Selected work</a><a href="#contact">Contact <span aria-hidden="true">↗</span></a></nav>
</header>
<main id="main">
  <section class="hero page-width" id="home" aria-labelledby="name">
    <div class="hero-copy"><p class="eyebrow"><span class="small-rule"></span> University of Wyoming</p>
    <h1 id="name">Khaled M.<br>Elokely<span class="degree">, PhD</span></h1>
    <h2>From molecular recognition<br>to <em>drug discovery.</em></h2>
    <p class="hero-intro">I bring computational and medicinal chemistry together to understand how molecules interact with biological targets—and use that understanding to guide the design of bioactive compounds.</p>
    <a class="primary-link" href="#research">Explore my research <span aria-hidden="true">↓</span></a>
    <p class="hero-affiliation">Division of Pharmaceutical Sciences<br>School of Pharmacy · College of Health Sciences</p></div>
    <div class="hero-art"><div class="hero-figure-label"><span class="eyebrow">Molecular recognition</span><span class="figure-dot" aria-hidden="true"></span></div>
      {figure_html(hero, 'hero', 0)}
    </div>
  </section>
  <section class="research-intro page-width" id="research" aria-labelledby="research-title"><div><p class="eyebrow">Research interests</p><h2 id="research-title">Six connected perspectives<br>on molecular discovery.</h2></div><p>Reliable data, protein structure, molecular timing, and stereochemistry each reveal a different part of the drug-discovery problem. My research connects these perspectives through reproducible computational methods and medicinal chemistry.</p></section>
  <nav class="topic-nav" aria-label="Research topics"><div class="page-width">{nav}</div></nav>
  <div class="research-sections page-width">{''.join(sections)}</div>
  <section class="work-section page-width" id="selected-work" aria-labelledby="work-title"><div class="section-heading"><div><p class="eyebrow">Publications & resources</p><h2 id="work-title">Selected work</h2></div><a class="text-link" href="https://orcid.org/0000-0002-2394-021X" target="_blank" rel="noopener noreferrer">ORCID profile <span aria-hidden="true">↗</span></a></div><ul class="work-list">{works}</ul>
  <div class="resource-strip"><p>Explore the methods and data behind the research.</p><div><a href="https://github.com/kelokely" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="https://doi.org/10.5281/zenodo.22736366" target="_blank" rel="noopener noreferrer">FragFlow data ↗</a><a href="https://doi.org/10.5281/zenodo.22760975" target="_blank" rel="noopener noreferrer">CURATO-OPIOID data ↗</a></div></div>
  </section>
  <section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="page-width contact-layout"><div><p class="eyebrow">Get in touch</p><h2 id="contact-title">Let’s connect.</h2><a class="contact-email" href="mailto:kelokely@uwyo.edu">kelokely@uwyo.edu <span aria-hidden="true">↗</span></a></div>
  <div class="contact-details"><h3>Khaled M. Elokely, PhD</h3><p>Division of Pharmaceutical Sciences<br>School of Pharmacy, College of Health Sciences<br>University of Wyoming<br>Laramie, WY 82071</p><div class="rooms"><div><span>Office</span><p>Room 398<br><a href="tel:+13077666136">307-766-6136</a></p></div><div><span>Lab</span><p>Room 396<br><a href="tel:+13077662954">307-766-2954</a></p></div></div></div></div></section>
</main>
<footer class="page-width"><span>© 2026 Khaled M. Elokely</span><span>Research figures are credited individually.</span><a href="#home">Back to top ↑</a></footer>
<dialog id="figure-dialog" aria-labelledby="dialog-title"><div class="dialog-header"><div><p class="eyebrow">Research figure</p><h2 id="dialog-title"></h2></div><button type="button" class="dialog-close" aria-label="Close figure">Close <span aria-hidden="true">×</span></button></div><div class="dialog-image-wrap"><img id="dialog-image" alt=""></div><div class="dialog-caption"><p id="dialog-caption-text"></p><small id="dialog-credit"></small><a id="dialog-original" target="_blank" rel="noopener noreferrer">Open image at full size ↗</a></div></dialog>
</body></html>'''
(ROOT.parent / 'index.html').write_text(html)
print(f'Generated {len(topics)} research sections, {sum(len(t["figures"]) for t in topics)} gallery figures, and {len(data["works"])} selected works.')
