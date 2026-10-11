# Khaled M. Elokely — Research

Personal research website hosted on GitHub Pages.

## Edit the website

- Research descriptions, figure captions, source credits, and selected works:
  edit `source/content.json`, then run `python3 source/build_site.py`.
- Homepage and affiliation/contact markup: edit `source/build_site.py`, then
  run the same command.
- Design and spacing: edit `styles.css`.
- Figure interactions: edit `site.js`.
- New or replacement figures: add the image to `assets/`, then update its
  entry in `source/content.json`.

Commit and push the updated files to `main`. GitHub Pages automatically
publishes the site from the root of that branch. Keep `.nojekyll` so these
static files are served without an extra build step.

You can also request updates in the original Codex conversation.

## Research content and figure credits

The site covers Data Curation, Contact Networks, Protein Timing (the kinetics
clock), FragFlow, KChiro, and Medicinal Chemistry through the CDK5 project.
Individual figures carry source credits and, where applicable, license links.
Replotted research figures are identified in their captions. Preprints and
methods in development are labeled separately from published papers.

The owner requested omission of compound structures, academic position, and
education history. The hosting repository contains only the website and its
editable content. No private manuscripts, grant documents, data bundles,
credentials, or ChatGPT hosting metadata are included.

GitHub Pages for public repositories is available on GitHub Free:
https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
