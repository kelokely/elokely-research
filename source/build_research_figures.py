"""Build structure-free reaction schemes and a conformational-search schematic."""
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / 'assets'


def text(x, y, label, size=21, color='#3f5149', weight=400, anchor='middle'):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(label)}</text>')


def rect(x, y, w, h, fill='#f6f7f2', stroke='#d8ddd3', radius=10):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')


def arrow(x1, y1, x2, y2):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" '
            'stroke="#8d6b35" stroke-width="2.5" marker-end="url(#arrow)"/>')


def write_svg(name, height, title, desc, elements, width=640):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#8d6b35"/></marker></defs>
<style>text{{font-family:Arial,Helvetica,sans-serif}}</style>
<rect width="{width}" height="{height}" fill="#fff"/>
{''.join(elements)}
</svg>'''
    (ASSETS / name).write_text(svg)


assembly = [
    rect(20, 20, 380, 60), text(210, 58, 'Core scaffold', 26, '#183b32'),
    arrow(45, 87, 45, 210),
    text(83, 111, 'N-alkylation /', 24, '#183b32', 700, 'start'),
    text(83, 139, 'N-benzylation', 24, '#183b32', 700, 'start'),
    text(83, 166, 'Alkyl / benzyl bromide', 21, anchor='start'),
    text(83, 193, 'NaH · DMF · 0 °C to RT', 21, anchor='start'),
    rect(20, 220, 380, 60),
    text(210, 246, 'N-substituted', 25, '#183b32'), text(210, 273, 'intermediate', 25, '#183b32'),
    arrow(45, 289, 45, 398),
    text(83, 314, 'Pd-catalyzed C–N coupling', 23, '#183b32', 700, 'start'),
    text(83, 342, 'Amine coupling partner', 21, anchor='start'),
    text(83, 370, 'Brett-Phos Pd G3 · Cs₂CO₃', 20, anchor='start'),
    text(83, 398, '1,4-dioxane · N₂ · 100 °C', 20, anchor='start'),
    rect(20, 408, 380, 60),
    text(210, 434, 'Boc-protected', 25, '#183b32'), text(210, 461, 'derivatives', 25, '#183b32'),
    arrow(45, 477, 45, 563),
    text(83, 502, 'Boc deprotection', 24, '#183b32', 700, 'start'),
    text(83, 536, 'Then KOH free-base workup', 21, anchor='start'),
    rect(20, 573, 380, 60),
    text(210, 599, 'Free-amine', 25, '#183b32'), text(210, 626, 'derivatives', 25, '#183b32'),
    text(210, 665, 'Representative reaction classes · Generic labels', 16, '#66756c'),
]
write_svg('cdk5-generic-assembly.svg', 685, 'CDK5 series assembly and deprotection',
          'Generic scaffold labels show N-substitution, protected-amine coupling, and deprotection. Named reagents describe the reaction classes; no molecular structures are included.', assembly, width=420)


diversification = [
    text(20, 31, 'Imine formation', 27, '#183b32', 700, 'start'),
    rect(20, 50, 380, 75),
    text(210, 82, 'Free-amine intermediate', 25, '#183b32'),
    text(210, 111, '+ aromatic aldehyde', 22),
    arrow(45, 134, 45, 266),
    text(83, 159, 'Condensation', 24, '#183b32', 700, 'start'),
    text(83, 187, '4 Å molecular sieves', 22, anchor='start'),
    text(83, 215, 'DCM / MeOH or', 21, anchor='start'),
    text(83, 243, 'DCE / MeCN (series-dependent)', 21, anchor='start'),
    rect(20, 276, 380, 60), text(210, 314, 'Imine derivatives', 26, '#183b32'),
    text(20, 386, 'Amide formation', 27, '#183b32', 700, 'start'),
    rect(20, 405, 380, 75),
    text(210, 437, 'Free-amine intermediate', 25, '#183b32'),
    text(210, 466, '+ carboxylic acid', 22),
    arrow(45, 489, 45, 595),
    text(83, 516, 'Amide coupling', 24, '#183b32', 700, 'start'),
    text(83, 545, 'HATU · DIPEA · DMF', 22, anchor='start'),
    text(83, 574, '0 °C to room temperature', 21, anchor='start'),
    rect(20, 605, 380, 60), text(210, 643, 'Amide derivatives', 26, '#183b32'),
    text(210, 702, 'Shared amine intermediate · Complementary routes', 16, '#66756c'),
]
write_svg('cdk5-generic-diversification.svg', 720, 'Diversifying CDK5 amine intermediates',
          'Two generic reaction routes show amine condensation with aromatic aldehydes to form imines and HATU-mediated amide coupling with carboxylic acids. No molecular structures are included.', diversification, width=420)


conformers = []
stages = [
    ('Define the search scope', 'Method and energy window', 'Solvent and stereochemistry'),
    ('Repeat the searches', 'Independent search replicas', 'Matched search conditions'),
    ('Compare conformers', 'Cluster distinct families', 'Re-rank relative energies'),
    ('Assess sampling evidence', 'Estimate search coverage', 'Population uncertainty'),
    ('Choose the next step', 'Bounded ensemble result', 'or additional sampling'),
]
for i, (heading, line1, line2) in enumerate(stages):
    y = 24 + i * 121
    conformers += [rect(20, y, 380, 104),
                  f'<circle cx="55" cy="{y + 52}" r="20" fill="#183b32"/>',
                  text(55, y + 60, str(i + 1), 22, '#fff', 700),
                  text(92, y + 35, heading, 23, '#183b32', 700, 'start'),
                  text(92, y + 64, line1, 20, anchor='start'),
                  text(92, y + 90, line2, 20, anchor='start')]
    if i < len(stages) - 1:
        conformers += [arrow(55, y + 108, 55, y + 117)]
conformers += [text(210, 647, 'CertCrest · Sampling and uncertainty', 17, '#66756c')]
write_svg('conformational-search-workflow.svg', 670, 'Conformational search with explicit uncertainty',
          'CertCrest concept workflow connects a declared search scope, repeated searches, clustering and energy re-ranking, statistical evidence, and a bounded result or further sampling.', conformers, width=420)
print('Generated two generic CDK5 reaction schemes and a conformational-search schematic.')
