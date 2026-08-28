# -*- coding: utf-8 -*-
"""Assemble the Opéra Rembourrage site from shared partials.
Run:  python3 build.py
"""
import json, re, pathlib

S = json.loads(pathlib.Path('content.json').read_text(encoding='utf-8'))

# Contenu modifiable depuis /admin.html — ne jamais écrire ces valeurs
# en dur ici, elles seraient perdues au prochain import.
D  = json.loads(pathlib.Path('data/site.json').read_text(encoding='utf-8'))
BIZ, HERO = D['entreprise'], D['enseigne']

NAV = [
    ('index.html',        'Accueil',      'Home'),
    ('a-propos.html',     'À propos',     'About'),
    ('savoir-faire.html', 'Savoir-faire', 'Craft'),
    ('cannage.html',      'Cannage',      'Caning'),
]

import hashlib

def ver(path):
    """Empreinte courte du contenu, pour casser le cache à chaque mise à jour."""
    return hashlib.sha1(pathlib.Path(path).read_bytes()).hexdigest()[:8]

PREPAINT = """<script>
/* Avant la premiere peinture : on saute l'ouverture si elle a deja
   ete vue dans cette session ou si le mouvement est desactive.
   #intro la rejoue, #introhold la fige pour la revue. */
(function(){
  var replay = location.hash === '#intro' || location.hash === '#introhold';
  var seen;
  try { seen = sessionStorage.getItem('operaIntro'); } catch (e) { seen = null; }
  if (!replay && (seen || matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    document.documentElement.classList.add('intro-skip');
  }
})();
</script>"""

SITE = 'https://operaupholstering.com/'

# Mettre à False avant de publier si la page d'édition ne doit pas
# exister en ligne du tout — c'est la protection la plus sûre, elle ne
# dépend d'aucun réglage d'hébergeur.
BUILD_ADMIN = True
OG_IMAGE = SITE + 'assets/hero.jpg'

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
  "name": "Opera Upholstering",
  "alternateName": "Op\u00e9ra Rembourrage",
  "description": "Atelier de rembourrage, restauration de meubles anciens et cannage tiss\u00e9 \u00e0 la main \u00e0 Montr\u00e9al depuis 1955, aujourd\u2019hui rue Saint-Hubert.",
  "url": "https://operaupholstering.com/",
  "telephone": "+1-514-270-4352",
  "email": "contact@operarembourrage.ca",
  "foundingDate": "1955",
  "priceRange": "$$",
  "image": "https://operaupholstering.com/assets/hero.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "7498 rue Saint-Hubert",
    "addressLocality": "Montr\u00e9al",
    "addressRegion": "QC",
    "postalCode": "H2R 2N3",
    "addressCountry": "CA"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 45.5449, "longitude": -73.6161 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "17:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "17:00" }
  ],
  "availableLanguage": ["fr", "en"],
  "areaServed": ["Montr\u00e9al", "Laval", "Rive-Sud", "Villeray", "Rosemont", "Outremont", "Westmount"],
  "knowsAbout": ["rembourrage", "restauration de meubles anciens", "cannage", "banquettes", "t\u00eates de lit", "finition du bois"]
}
</script>"""

def head(title, desc, page, noindex=False):
    canon = SITE + ('' if page == 'index.html' else page)
    og = OG_IMAGE
    HOURS_JSON = json.dumps(D['heures'])
    ROBOTS = '\n<meta name="robots" content="noindex, nofollow">' if noindex else ''
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">{ROBOTS}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Opera Upholstering">
<meta property="og:locale" content="fr_CA">
<meta property="og:locale:alternate" content="en_CA">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#26282C">
<link rel="icon" href="assets/logo-opera.png">
<link rel="apple-touch-icon" href="assets/logo-opera.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..700&family=Jost:wght@300;400;500&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&display=swap">
<link rel="stylesheet" href="assets/site.css?v={ver('assets/site.css')}">
{SCHEMA}
<script id="opera-hours" type="application/json">{HOURS_JSON}</script>
<script>
/* Avant la première peinture : une adresse de préproduction ne peut pas
   authentifier, Vercel intercepte en amont. On y renvoie tout de suite. */
(function(){{
  var h = location.hostname;
  if(/-git-/.test(h) || /^operaupholstering-[a-z0-9]{{6,}}/.test(h)){{
    location.replace('https://operaupholstering.vercel.app' + location.pathname + location.search);
  }}
}})();
</script>
{{PREPAINT}}
</head>
<body>
'''

def header(current):
    links = []
    for href, fr, en in NAV:
        cur = ' aria-current="page"' if href == current else ''
        links.append(f'      <a href="{href}"{cur} data-en="{en}">{fr}</a>')
    links.append('      <a href="index.html#soumission" data-en="Contact">Contact</a>')
    return '''<div class="splash" id="splash" aria-hidden="true">
  <div class="splash-lock">
    <span class="splash-fr">Rembourrage</span>
    <img class="splash-mark" src="assets/logo-mark.png" alt="" width="511" height="140">
    <span class="splash-rule"></span>
    <img class="splash-sub" src="assets/logo-sub.png" alt="" width="511" height="30">
  </div>
</div>

<a class="skip" href="#contenu" data-en="Skip to content">Aller au contenu</a>

<header class="topbar">
  <div class="wrap bar">
    <a class="logo" href="index.html" aria-label="Opéra Rembourrage — accueil">
      <span class="logo-fr">Rembourrage</span>
      <img src="assets/logo-opera.png" alt="Opéra Rembourrage · Opera Upholstering">
    </a>
    <nav class="navlinks" aria-label="Principal">
''' + '\n'.join(links) + '''
    </nav>
    <div class="navtools">
      <button type="button" class="menubtn" id="menubtn" aria-expanded="false" aria-controls="mobilemenu">
        <span class="bars" aria-hidden="true"><i></i><i></i></span>
        <span class="menubtn-t" data-en="Menu">Menu</span>
      </button>
      <div class="langtog" role="group" aria-label="Langue / Language">
        <button type="button" id="btn-fr" aria-pressed="true">FR</button>
        <button type="button" id="btn-en" aria-pressed="false">EN</button>
      </div>
      <a class="btn" href="index.html#soumission" data-en="Get a quote">Soumission</a>
    </div>
  </div>
  <div class="mobilemenu" id="mobilemenu" hidden>
    <nav aria-label="Menu">
''' + '\n'.join(
      '      <a href="%s"%s data-en="%s">%s</a>' % (h, ' aria-current="page"' if h == current else '', e, f)
      for h, f, e in NAV) + '''
      <a href="tissus.html" data-en="The fabrics">Les tissus</a>
      <a href="index.html#soumission" data-en="Contact">Contact</a>
      <a class="mm-tel" href="tel:{BIZ[telephone_lien]}">{BIZ[telephone]}</a>
    </nav>
  </div>
</header>
'''

STATUSBAR = '''<div class="statusbar">
  <div class="wrap bar">
    <span class="sb-left">{BIZ[adresse]}, {BIZ[ville_courte]}</span>
    <a class="sb-right" href="tel:{BIZ[telephone_lien]}">{BIZ[telephone]}</a>
  </div>
</div>
'''

FOOTER = '''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="flogo"><img src="assets/logo-opera.png" alt="Opera Upholstering"></div>
        <p style="margin-top:16px;max-width:34ch" data-en="Upholstery, antique restoration and hand caning in Montréal since 1955.">Rembourrage, restauration d’antiquités et cannage tissé à la main à Montréal depuis 1955.</p>
        <p style="margin-top:14px"><a href="tel:{BIZ[telephone_lien]}">{BIZ[telephone]}</a><br><a class="mail-swap" data-mail-fr="{BIZ[courriel_fr]}" data-mail-en="{BIZ[courriel_en]}" href="mailto:{BIZ[courriel_fr]}">{BIZ[courriel_fr]}</a><br>7498 rue Saint-Hubert<br>Montréal (Québec) H2R 2N3</p>
      </div>
      <div>
        <p class="flabel" data-en="Services">Services</p>
        <p><a href="index.html#services" data-en="Armchairs &amp; sofas">Fauteuils &amp; sofas</a><br>
        <a href="index.html#services" data-en="Antique restoration">Restauration d’antiquités</a><br>
        <a href="cannage.html" data-en="Cane, rush &amp; wicker">Cannage, jonc &amp; rotin</a><br>
        <a href="index.html#services" data-en="Dining chairs">Chaises de salle à manger</a><br>
        <a href="index.html#services" data-en="Custom headboards">Têtes de lit sur mesure</a><br>
        <a href="index.html#services" data-en="Cushions &amp; outdoor">Coussins &amp; extérieur</a><br>
        <a href="index.html#services" data-en="Banquettes &amp; contract">Banquettes &amp; contrat</a><br>
        <a href="index.html#services" data-en="Frames &amp; springs">Structure &amp; ressorts</a></p>
      </div>
      <div>
        <p class="flabel" data-en="Learn">Comprendre</p>
        <p><a href="tissus.html" data-en="The fabric library">La bibliothèque de tissus</a><br>
        <a href="tissus.html#performance" data-en="Which cloth survives your household">Quel tissu survit à votre maison</a><br>
        <a href="savoir-faire.html" data-en="What is under the fabric">Ce qu’il y a sous le tissu</a><br>
        <a href="savoir-faire.html#prix" data-en="What decides the price">Ce qui décide du prix</a><br>
        <a href="savoir-faire.html#questions" data-en="Questions">Questions</a></p>
      </div>
      <div>
        <p class="flabel" data-en="Served areas">Secteurs desservis</p>
        <p data-en="Villeray · Petite-Patrie · Rosemont · Plateau-Mont-Royal · Outremont · Ahuntsic · Mile End · Saint-Léonard · Westmount · Town of Mount Royal · Laval · South Shore">Villeray · Petite-Patrie · Rosemont · Plateau-Mont-Royal · Outremont · Ahuntsic · Mile End · Saint-Léonard · Westmount · Mont-Royal · Laval · Rive-Sud</p>
      </div>
    </div>
    <div class="colophon">
      <span>© <span id="year">2026</span> Opera Upholstering</span>
      <span data-en="Est. 1955 · Montréal">Depuis 1955 · Montréal</span>
      <span data-en="Service in French and English">Service en français et en anglais</span>
    </div>
  </div>
</footer>

<div class="tray" id="tray" aria-live="polite">
  <div class="wrap bar">
    <span class="lbl" data-en="Your tray">Votre plateau</span>
    <div class="tray-items" id="trayitems"></div>
    <span class="note" id="traynote"></span>
    <a class="btn light" href="index.html#soumission" id="traycta" data-en="Reserve at the counter">Réserver au comptoir</a>
  </div>
</div>

<div class="mobilebar">
  <a class="btn light" href="tel:{BIZ[telephone_lien]}" data-en="Call">Appeler</a>
  <a class="btn outline-light" href="index.html#soumission" data-en="Quote">Soumission</a>
</div>

<script src="assets/site.js?v={JSVER}"></script>
'''



JOURS_FR = ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi']
JOURS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

def hours_rows():
    """Le tableau de la page contact et le bandeau « ouvert / fermé »
       doivent lire la même source, sinon ils se contredisent."""
    out = []
    for d in [1, 2, 3, 4, 5, 6, 0]:
        v = D['heures'].get(str(d))
        if v:
            fr = '%s h – %s h' % (v[0], v[1])
            en = '%s – %s' % (v[0], v[1])
            cell = '<td data-en="%s">%s</td>' % (en, fr)
        else:
            cell = '<td data-en="Closed">Fermé</td>'
        out.append('          <tr data-day="%d"><td data-en="%s">%s</td>%s</tr>'
                   % (d, JOURS_EN[d], JOURS_FR[d], cell))
    return '\n'.join(out)

def fill(html):
    """Les partials (en-tête, bandeau, pied) portent des jetons
       {BIZ[cle]} ; on les remplace ici plutôt qu'avec .format(), qui
       trébucherait sur les accolades du JSON-LD et du CSS."""
    html = html.replace('{HOURS_ROWS}', hours_rows())
    return re.sub(r'\{BIZ\[([a-z_]+)\]\}', lambda m: esc(str(BIZ.get(m.group(1), ''))), html)

def page(filename, title, desc, body, statusbar=False, noindex=False):
    footer = FOOTER.replace('{JSVER}', ver('assets/site.js'))
    html = head(title, desc, filename, noindex).replace('{PREPAINT}', PREPAINT) + '\n' + header(filename) + (STATUSBAR if statusbar else '') + '\n<main id="contenu">\n' + body + '\n</main>\n\n' + footer + '\n</body>\n</html>\n'
    pathlib.Path(filename).write_text(fill(html), encoding='utf-8')
    print('wrote', filename, len(html), 'bytes')


# ── Les textes édités depuis /admin.html recouvrent content.json ────
# L'index ordinal des balises [data-en] est la clé. Si le balisage
# d'une section change ici, régénérer data/textes.json.
_TXT_PATH = pathlib.Path('data/textes.json')
TXT = json.loads(_TXT_PATH.read_text(encoding='utf-8')) if _TXT_PATH.exists() else {}
_TXT_PAT = re.compile(r'<(\w+)([^>]*\sdata-en="([^"]*)"[^>]*)>(.*?)</\1>', re.S)

def apply_textes(key, html):
    edits = TXT.get(key)
    if not edits:
        return html
    # Garde-fou : l'index ordinal n'a de sens que si la structure n'a pas
    # bougé. Si une figure ou un champ a été ajouté au balisage, on refuse
    # d'appliquer plutôt que de décaler tous les textes d'un cran.
    live = [m for m in _TXT_PAT.finditer(html) if '<' not in m.group(4)]
    if len(live) != len(edits):
        print('  ! %s : %d champs dans le balisage, %d dans textes.json — '
              'overlay ignoré, relancer l\'extraction' % (key, len(live), len(edits)))
        return html
    i = [0]
    def swap(m):
        fr = m.group(4)
        if '<' in fr:                 # balisage interne : laissé tel quel
            return m.group(0)
        n = i[0]; i[0] += 1
        if n >= len(edits):
            return m.group(0)
        e = edits[n]
        attrs = m.group(2).replace('data-en="%s"' % m.group(3),
                                   'data-en="%s"' % esc(e.get('en', m.group(3))))
        return '<%s%s>%s</%s>' % (m.group(1), attrs, esc(e.get('fr', fr)), m.group(1))
    return _TXT_PAT.sub(swap, html)

def sec(sid, extra_class='', keep_id=None):
    """Re-wrap an extracted planche body as a plain section."""
    cls = ('section' + (' ' + extra_class if extra_class else '')).replace('section', '').strip()
    attrs = (' class="%s"' % cls) if cls else ''
    return '<section%s id="%s">%s\n</section>' % (attrs, keep_id or sid, apply_textes(sid, S[sid]))

# ── strip the old "Planche N" eyebrow furniture ──────────────────────────
def clean(html):
    html = html.replace('<div class="ph-head rise">', '<div class="sec-head rise">')
    html = re.sub(r'\s*<span class="ph-num"[^>]*>.*?</span>\n', '\n', html)
    html = html.replace('<div class="ph-head rise">\n      \n      <div>', '<div class="sec-head rise">\n      <div>')
    # the old head was a 2-col grid; flatten the inner wrapper
    return html

for k in S: S[k] = clean(S[k])
S['bibliotheque'] = S['bibliotheque'].replace('id="swatchgrid"', 'data-swatchgrid')

# sections lifted onto sub-pages must aim their CTAs at the home page anchor
for k in [k for k in ('cannage','calculateur','prix','questions','anatomie','procede','glossaire','bibliotheque','performance') if k in S]:
    S[k] = S[k].replace('href="#soumission"', 'href="index.html#soumission"')
print('sections loaded')

# ═════════════════════════ ACCUEIL ═════════════════════════
def esc(t):
    """Le contenu vient d'un formulaire : on l'échappe ici plutôt que
       d'obliger l'atelier à taper des entités HTML dans l'éditeur."""
    return (t or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

SERVICES_SHORT = [(esc(x['fr']), esc(x['en']), esc(x['desc_fr']), esc(x['desc_en']),
                   esc(x['meta_fr']), esc(x['meta_en'])) for x in D['services']]


def _svc_card(fr, en, dfr, den, mfr, men):
    """La ligne « meta » ne s'affiche que si le service en a une —
       seul Cueillette & livraison en garde une désormais."""
    meta = ('\n        <div class="meta"><span data-en="On request">Sur demande</span>'
            '<b data-en="%s">%s</b></div>' % (men, mfr)) if mfr else ''
    return ('      <article class="svc rise">\n'
            '        <h3 data-en="%s">%s</h3>\n'
            '        <p data-en="%s">%s</p>%s\n'
            '      </article>' % (en, fr, den, dfr, meta))

svc_cards = '\n'.join(_svc_card(*row) for row in SERVICES_SHORT)

FIGS = '\n'.join(
 '      <div class="fig"><b>%s</b><span data-en="%s">%s</span></div>'
 % (f['valeur'], f['label_en'], f['label_fr']) for f in D['chiffres'])

for _k in HERO: HERO[_k] = esc(HERO[_k])
for _f in D['chiffres']:
    for _k in ('valeur','label_fr','label_en'): _f[_k] = esc(_f[_k])

HOME = ('''<section class="hero" id="haut">
  <div class="hero-media">
    <img class="hero-photo" src="assets/hero.jpg" alt="Un sofa haut de gamme retapissé dans un tissu à motif floral aquarelle, dans une pièce sombre éclairée par un rideau voilé et une lampe sur pied." fetchpriority="high" width="2000" height="1116">
    <span class="hero-scrim"></span>
  </div>
  <div class="hero-type">
    <span class="lbl" data-en="{HERO[surtitre_en]}">{HERO[surtitre_fr]}</span>
    <h1 class="hero-logo">
      <span class="hero-logo-fr">Rembourrage</span>
      <img src="assets/logo-mark.png" alt="Opera" width="511" height="140">
      <span class="hero-logo-en">Upholstering</span>
    </h1>
    <p class="hero-sub" data-en="{HERO[sous_titre_en]}">{HERO[sous_titre_fr]}</p>
    <div class="hero-cta">
      <a class="btn light" href="#soumission" data-en="{HERO[bouton1_en]}">{HERO[bouton1_fr]}</a>
      <a class="btn outline-light" href="#realisations" data-en="{HERO[bouton2_en]}">{HERO[bouton2_fr]}</a>
    </div>
    <div class="hero-figures">
{FIGS}
    </div>
  </div>
</section>

<section id="services">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="lbl" data-en="Services">Services</span>
      <h2 data-en="The work of the shop">Les travaux de l’atelier</h2>
      <p class="kicker" data-en="The delays below are those of an ordinary season. They lengthen between April and June, and vary with what the frame turns out to need once the piece is stripped.">Les délais ci-dessous sont ceux d’une saison ordinaire. Ils s’allongent entre avril et juin, et varient selon ce que la structure révèle une fois la pièce dégarnie.</p>
    </div>
    <div class="cols" data-stagger>
''' + svc_cards + '''
    </div>
    <div class="endcta rise">
      <a class="btn" href="tissus.html" data-en="Discover the fabrics">Découvrir les tissus</a>
      <a class="btn ghost" href="#soumission" data-en="Request an estimate">Demander une estimation</a>
    </div>
  </div>
</section>

<section class="sunk" id="atelier">
  <div class="wrap">
    <div class="cols-2 rise">
      <div>
        <span class="lbl" data-en="The workshop">L’atelier</span>
        <h2 style="margin-top:12px" data-en="What comes before the fabric">Ce qui précède le tissu</h2>
        <p class="muted" style="margin-top:18px" data-en="A piece that arrives is stripped to the frame. Everything beneath the fabric is inspected before a single yard is cut.">Une pièce qui arrive est dégarnie jusqu’à la structure. Tout ce qui se trouve sous le tissu est inspecté avant qu’une seule verge soit coupée.</p>
        <p class="muted" data-en="Loose joints are re-glued and doweled, webbing replaced and stretched by hand, coil springs retied at eight knots each. The fabric goes on only afterwards.">Les joints lâches sont recollés et chevillés, les sangles remplacées et tendues à la main, les ressorts reguindés à huit nœuds chacun. Le tissu ne monte qu’ensuite.</p>
        <p class="muted" data-en="A serious estimate therefore assumes the piece has been seen: the real work only appears once the frame is bare.">Une estimation sérieuse suppose donc d’avoir vu la pièce : le travail réel n’apparaît qu’une fois la structure à nu.</p>
        <div class="endcta">
          <a class="btn ghost" href="savoir-faire.html" data-en="The ten layers of a seat">Les dix couches d’un siège</a>
        </div>
      </div>
      <div class="cols atelier-pair" data-stagger style="gap:16px">
        <figure class="fig-sq rise">
          <img src="assets/etabli.jpg" alt="Établi de rembourreur : tendeur à sangles, jute, ficelle, semences, et une bergère à demi dégarnie." loading="lazy">
          <figcaption data-en="The bench">L’établi</figcaption>
        </figure>
        <figure class="fig-sq rise">
          <img src="assets/ressorts.jpg" alt="Ressorts guindés à la ficelle sur des sangles de jute neuves." loading="lazy">
          <figcaption data-en="Springs, hand-tied">Ressorts guindés à la main</figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<section class="sunk" id="realisations">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="lbl" data-en="Recent work">Réalisations</span>
      <h2 data-en="Pieces that left the shop">Des pièces sorties de l’atelier</h2>
      <p class="kicker" data-en="Fabric and leather, antiques and modern pieces, and the occasional sleigh — all rebuilt at 7498 rue Saint-Hubert.">Tissu et cuir, antiquités et pièces modernes, et parfois un traîneau — tout refait au 7498, rue Saint-Hubert.</p>
    </div>
    <div class="work" data-stagger>
      <figure class="rise">
        <img src="assets/travaux/cuir-elda.jpg" alt="Fauteuil pivotant enveloppant, entièrement refait en cuir brun." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Swivel lounge chair · full-grain leather">Fauteuil pivotant · cuir pleine fleur</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/louis-xv-fleuri.jpg" alt="Fauteuil Louis XV recouvert d’un imprimé floral, galon clouté sur bois apparent." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Louis XV armchair · printed linen">Fauteuil Louis XV · lin imprimé</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/bergeres-bleues.jpg" alt="Paire de bergères à oreilles en tissu bleu à motif, bois laqué crème." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Pair of wing chairs">Paire de bergères à oreilles</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/art-deco-chevron.jpg" alt="Fauteuil art déco en noyer recouvert d’un tissé à chevrons multicolores." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Art deco tub chair · chevron weave">Fauteuil art déco · tissé à chevrons</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/fauteuil-tonneau.jpg" alt="Fauteuil tonneau à bois noirci sculpté, recouvert d’un tissé bleu à feuillage." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Barrel chair · carved ebonised frame">Fauteuil tonneau · bois sculpté noirci</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/paire-os-mouton.jpg" alt="Paire de fauteuils os-de-mouton recouverts d’un imprimé floral, bois clair." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Pair of os-de-mouton armchairs">Paire de fauteuils os-de-mouton</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/louis-xvi-velours.jpg" alt="Fauteuil Louis XVI recouvert d’un velours à motif floral vif." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Louis XVI armchair · painted velvet">Fauteuil Louis XVI · velours peint</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/rocking-cannage.jpg" alt="Chaise berçante en rotin dont le dossier et l’assise ont été recannés à la main." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Rattan rocker · re-caned by hand">Berçante en rotin · recannée à la main</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/chaise-corde-noire.jpg" alt="Chaise à barreaux laquée noir, assise tissée en corde de papier naturelle." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Ladder-back chair · woven paper cord">Chaise à barreaux · assise en corde de papier</figcaption>
      </figure>
      <figure class="rise">
        <img src="assets/travaux/traineau.jpg" alt="Traîneau ancien en bois cintré, assise refaite en cuir rouge à cannelures." loading="lazy" width="1000" height="1000">
        <figcaption data-en="Antique sleigh · red leather">Traîneau ancien · cuir rouge</figcaption>
      </figure>
    </div>
    <div class="endcta rise">
      <a class="btn" href="#soumission" data-en="Request an estimate">Demander une estimation</a>
    </div>
  </div>
</section>

<section class="sunk" id="cannage-teaser">
  <div class="wrap">
    <div class="rise" style="max-width:72ch">
      <div>
        <span class="lbl" data-en="Caning">Cannage</span>
        <h2 style="margin-top:12px" data-en="Hand-woven caning">Cannage tissé à la main</h2>
        <p class="muted" style="margin-top:18px" data-en="Cane threaded one hole at a time, sheet cane set into a spline groove, rush seats, Danish paper cord and wicker repair. Twenty mesh sizes and weaves are held in stock, with custom weaves available on order.">Cannage enfilé un trou à la fois, cannage en feuille posé en rainure, sièges de jonc, corde de papier danoise et réparation d’osier. Vingt maillages et tissages sont tenus en stock, et des tissages sur mesure peuvent être commandés.</p>
        <p class="muted" data-en="The spacing of the drilled holes identifies the mesh a chair was originally made with; matching it is what separates a repair from a patch.">L’espacement des trous percés indique le maillage d’origine d’une chaise; le respecter distingue une réparation d’une rustine.</p>
        <div class="endcta"><a class="btn ghost" href="cannage.html" data-en="The twenty weaves">Les vingt tissages</a></div>
      </div>
    </div>
  </div>
</section>

''').format(HERO=HERO, BIZ=BIZ, FIGS=FIGS) + sec('soumission')

page('index.html',
     'Opera Upholstering — Rembourrage, restauration et cannage · Montréal',
     'Atelier de rembourrage à Montréal depuis 1955, aujourd’hui rue Saint-Hubert. Restauration de meubles anciens, cannage, banquettes, têtes de lit.',
     HOME, statusbar=True)

# ═════════════════════════ SOUS-PAGES ═════════════════════════
# ═════════════════════════ À PROPOS ═════════════════════════
APROPOS = '''<section>
  <div class="wrap">
    <div class="sec-head rise">
      <span class="lbl" data-en="About">À propos</span>
      <h1 data-en="The shop on Saint-Hubert">L’atelier de la rue Saint-Hubert</h1>
      <p class="kicker" data-en="Three generations of customers have passed through the shop’s doors. The same trade, done the same way, now at 7498 rue Saint-Hubert.">Trois générations de clients ont passé la porte de l’atelier. Le même métier, fait de la même façon, aujourd’hui au 7498, rue Saint-Hubert.</p>
    </div>

    <div class="cols-2 rise">
      <div>
        <p class="muted" data-en="Rue Saint-Hubert once counted tailors and furriers by the dozen. Most of those trades have gone. Upholstery stayed, because a well-built chair is worth repairing and because someone has to know how.">La rue Saint-Hubert a compté des tailleurs et des fourreurs par dizaines. La plupart de ces métiers ont disparu. Le rembourrage est resté, parce qu’un fauteuil bien bâti mérite d’être réparé et parce qu’il faut bien que quelqu’un sache le faire.</p>
        <p class="muted" data-en="Everything is done on site: stripping, frame repair, webbing, springs, stuffing, sewing, caning and wood finishing. Nothing is sent out, which is why the estimate holds and the delay is ours to keep.">Tout se fait sur place : dégarnissage, réparation de structure, sangles, ressorts, bourrage, couture, cannage et finition du bois. Rien n’est envoyé ailleurs, et c’est pour ça que l’estimation tient et que le délai nous appartient.</p>
        <p class="muted" data-en="Customers come with a chair from a grandmother, a sofa that has held up for thirty years, or twelve restaurant banquettes that need to be back in service by Friday. The work is the same: open it, look, and rebuild it properly.">Les clients arrivent avec un fauteuil de grand-mère, un sofa qui a tenu trente ans, ou douze banquettes de restaurant à remettre en service pour vendredi. Le travail est le même : ouvrir, regarder, et refaire les choses comme il faut.</p>
      </div>
      <div class="cols" data-stagger style="gap:16px">
        <figure class="fig-sq rise">
          <img src="assets/etabli.jpg" alt="L’établi de l’atelier : tendeur à sangles, jute, ficelle, semences et une bergère à demi dégarnie." loading="lazy" width="1100" height="1100">
          <figcaption data-en="The bench">L’établi</figcaption>
        </figure>
        <figure class="fig-sq rise">
          <img src="assets/semences.jpg" alt="Mains plantant des semences d’acier bleui le long de la traverse d’un fauteuil." loading="lazy" width="1100" height="1100">
          <figcaption data-en="Tacks, set by hand">Semences, posées à la main</figcaption>
        </figure>
        <figure class="fig-sq rise">
          <img src="assets/passementerie.jpg" alt="Galon, cordonnet, frange, glands et clous de laiton sur une table de noyer." loading="lazy" width="1100" height="1100">
          <figcaption data-en="Trim and brass nails">Passementerie et clous de laiton</figcaption>
        </figure>
      </div>
    </div>

    <div class="cols rise" style="margin-top:clamp(30px,4vw,52px)">
      <div><h3 data-en="Since 1955">Depuis 1955</h3><p class="muted small" data-en="A trade practised without interruption, from one generation of customers to the next.">Un métier exercé sans interruption, d’une génération de clients à la suivante.</p></div>
      <div><h3 data-en="Everything under one roof">Tout sous un même toit</h3><p class="muted small" data-en="Upholstery, antique restoration, caning, wood finishing, commercial banquettes, pick-up and delivery.">Rembourrage, restauration d’antiquités, cannage, finition du bois, banquettes commerciales, cueillette et livraison.</p></div>
      <div><h3 data-en="French and English">Français et anglais</h3><p class="muted small" data-en="At the counter and on the phone, whichever you are more comfortable in.">Au comptoir et au téléphone, dans la langue qui vous convient.</p></div>
      <div><h3 data-en="Free estimates">Estimation gratuite</h3><p class="muted small" data-en="Send three photographs and a written figure comes back the next business day.">Envoyez trois photographies et un chiffre écrit revient le jour ouvrable suivant.</p></div>
    </div>

    <div class="endcta rise">
      <a class="btn" href="index.html#soumission" data-en="Request an estimate">Demander une estimation</a>
      <a class="btn ghost" href="tissus.html" data-en="Discover the fabrics">Découvrir les tissus</a>
    </div>
  </div>
</section>'''

page('a-propos.html',
     'À propos — Opera Upholstering, Montréal',
     'Rembourrage, restauration d’antiquités, cannage et finition du bois, tout sur place, au 7498, rue Saint-Hubert à Montréal.',
     APROPOS)

# ═════════════════════════ ADMIN ═════════════════════════
# Page interne : hors navigation, hors index, hors plan de site.
ADMIN_BODY = '''<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="lbl">Interne</span>
      <h1>Modifier le site</h1>
      <p class="kicker">Textes, coordonnées, heures, services et photographies. Enregistrez, décompressez le dossier par-dessus <code>site/</code>, relancez le build. Rien n’est envoyé d’ici : la page ne fait qu’écrire un fichier que vous récupérez.</p>
    </div>

    <div class="adm-bar">
      <span class="adm-state" id="state">Chargement…</span>
      <button class="adm-btn ghost" id="copy" type="button">Copier</button>
      <button class="adm-btn ghost" id="save" type="button" disabled>Enregistrer le dossier</button>
      <button class="adm-btn" id="publish" type="button">Publier en ligne</button>
    </div>

    <div class="adm-gate" id="gate" hidden>
      <div class="adm-gatebox">
        <span class="lbl">Accès</span>
        <p class="adm-note" style="margin:10px 0 16px">Le mot de passe est réglé sur l’hébergeur. Il n’est pas écrit dans cette page.</p>
        <input id="pass" type="password" autocomplete="current-password" placeholder="Mot de passe" aria-label="Mot de passe">
        <p class="adm-gatemsg" id="gatemsg"></p>
        <div style="display:flex;gap:9px;margin-top:14px">
          <button class="adm-btn" id="signin" type="button">Entrer</button>
          <button class="adm-btn ghost" id="gatecancel" type="button">Annuler</button>
        </div>
      </div>
    </div>

    <div id="tabs"></div>
    <div id="pane"></div>
    <textarea id="raw" hidden readonly aria-label="Contenu du fichier"></textarea>

    <h2 style="margin-top:44px">Mettre les changements en ligne</h2>
    <ol class="muted" style="max-width:70ch">
      <li><strong>Publier en ligne</strong> — le plus simple. Un mot de passe la première fois, puis les changements partent dans le dépôt et le site se reconstruit tout seul en une minute environ. Rien à décompresser, rien à taper dans un terminal.</li>
    </ol>
    <p class="muted small">Si l’hébergeur n’est pas encore configuré, la voie de secours reste ouverte :</p>
    <ol class="muted" style="max-width:70ch">
      <li>Enregistrer le dossier — vous obtenez <code>opera-contenu.zip</code>.</li>
      <li>Le décompresser par-dessus le dossier <code>site/</code>, en remplaçant ce qu’il propose. Il contient les textes et, s’il y en a, les photographies changées, déjà aux bonnes mesures et sous les bons noms.</li>
      <li>Dans le dossier <code>site/</code> : <code>python3 build.py</code></li>
      <li>Puis : <code>git add -A &amp;&amp; git commit -m "contenu" &amp;&amp; git push</code></li>
    </ol>
    <p class="muted small">Sans la dernière étape, les changements ne vivent que sur cet ordinateur.</p>

    <h2 style="margin-top:34px">Accès et protection</h2>
    <p class="muted" style="max-width:70ch">La page demande le mot de passe à l’entrée, vérifié par le serveur — le même que pour publier. Servie en local sans fonctions, elle s’ouvre librement : elle ne peut alors qu’écrire un dossier, et le contenu qu’elle montre est celui, déjà public, du site.</p>
    <p class="muted" style="max-width:70ch">Elle est tout de même exclue des moteurs de recherche (<code>noindex</code> et <code>robots.txt</code>) et absente du plan du site et du menu. Trois façons de la fermer davantage, de la plus sûre à la plus commode :</p>
    <div class="tablewrap" style="margin:16px 0 8px">
      <table>
        <thead><tr><th>Moyen</th><th>Comment</th><th>Solidité</th></tr></thead>
        <tbody>
          <tr><td>Ne pas la publier</td><td>Mettre <code>BUILD_ADMIN = False</code> en haut de <code>build.py</code>. Elle n’existe alors qu’ici, sur cet ordinateur, servie par <code>python3 -m http.server</code>.</td><td>Totale</td></tr>
          <tr><td>Mot de passe de l’hébergeur</td><td>Sur Netlify, une ligne dans <code>_headers</code>; sur Cloudflare, une règle Access; sur un serveur classique, un <code>.htaccess</code>. Le mot de passe est vérifié avant que la page ne parte.</td><td>Solide</td></tr>
          <tr><td>Mot de passe dans la page</td><td>Déconseillé : le code de la page est lisible par tous, donc le mot de passe aussi. Cela n’écarte que les curieux.</td><td>Apparente</td></tr>
        </tbody>
      </table>
    </div>
    <p class="muted small">Recommandation : garder <code>BUILD_ADMIN = False</code> pour la mise en ligne, et remettre <code>True</code> quand vous travaillez sur le site en local.</p>

    <h2 style="margin-top:34px">Essayer la connexion en local</h2>
    <p class="muted" style="max-width:70ch">Le serveur local ne sait qu’envoyer des fichiers : il n’exécute pas <code>api/login.js</code>, donc le mot de passe n’a rien à interroger et « Publier en ligne » ne peut pas aboutir. C’est normal, et le bouton le dit plutôt que d’échouer sans explication.</p>
    <div class="tablewrap" style="margin:14px 0 0">
      <table>
        <thead><tr><th>Pour</th><th>Lancer</th><th>Ce qui marche</th></tr></thead>
        <tbody>
          <tr><td>Écrire et relire</td><td><code>python3 serve.py</code></td><td>Tout l’éditeur, et « Enregistrer le dossier ».</td></tr>
          <tr><td>Essayer la connexion</td><td><code>vercel dev</code></td><td>Le mot de passe et la publication, avec les valeurs du fichier <code>.env</code>.</td></tr>
        </tbody>
      </table>
    </div>

    <h2 style="margin-top:34px">Ce qui ne se modifie pas ici</h2>
    <p class="muted" style="max-width:70ch">Les textes contenant des liens ou de la mise en forme restent dans <code>content.json</code>, et l’apparence dans <code>assets/site.css</code>. Ils se modifient dans un éditeur de texte. Un vrai panneau où l’on écrit tout depuis le navigateur, sans fichier à déplacer, demanderait un hébergement avec base de données — ce site est fait de fichiers immobiles, ce qui le rend rapide et gratuit à héberger.</p>
  </div>
</section>

<script src="assets/admin-zip.js"></script>
<script src="assets/admin.js?v={ADMINVER}"></script>'''.replace('{ADMINVER}', ver('assets/admin.js'))

if BUILD_ADMIN:
    page('admin.html', 'Admin — Opera Upholstering',
         'Page interne de gestion du site.', ADMIN_BODY, noindex=True)

page('tissus.html',
     'La bibliothèque de tissus — Opera Upholstering',
     'Dix maisons de tissus, des centaines de cartables : velours, bouclé, chenille, tissés, performance et extérieur. Réservez trois échantillons gratuits au comptoir.',
     sec('bibliotheque') + '\n' + sec('performance', 'sunk'))

page('savoir-faire.html',
     'Savoir-faire — comment ça marche · Opera Upholstering',
     'Les six étapes de l’atelier, ce qui décide du prix, et les questions qu’on reçoit le plus souvent.',
     sec('procede') + '\n' + sec('prix', 'sunk') + '\n' + sec('questions'))

page('cannage.html',
     'Cannage, roseau et jonc — Opera Upholstering',
     'Cannage tissé à la main ou en feuille, jonc, corde danoise et rotin. Vingt maillages en stock, tissages sur mesure en commande spéciale.',
     sec('cannage'))

