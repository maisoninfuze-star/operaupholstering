# -*- coding: utf-8 -*-
"""Assemble the Opéra Rembourrage site from shared partials.
Run:  python3 build.py
"""
import json, re, pathlib

S = json.loads(pathlib.Path('content.json').read_text(encoding='utf-8'))

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
OG_IMAGE = SITE + 'assets/seq/f_30.jpg'

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
  "name": "Opera Upholstering",
  "alternateName": "Op\u00e9ra Rembourrage",
  "description": "Atelier de rembourrage, restauration de meubles anciens et cannage tiss\u00e9 \u00e0 la main, rue Saint-Hubert \u00e0 Montr\u00e9al depuis 1955.",
  "url": "https://operaupholstering.com/",
  "telephone": "+1-514-270-4352",
  "foundingDate": "1955",
  "priceRange": "$$",
  "image": "https://operaupholstering.com/assets/seq/f_30.jpg",
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

def head(title, desc, page):
    canon = SITE + ('' if page == 'index.html' else page)
    og = OG_IMAGE
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
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
      <a class="mm-tel" href="tel:+15142704352">(514) 270-4352</a>
    </nav>
  </div>
</header>
'''

STATUSBAR = '''<div class="statusbar">
  <div class="wrap bar">
    <span id="openstate"><span class="dot off"></span><b data-en="Hours below">Horaire ci-dessous</b></span>
    <span>7498 rue Saint-Hubert, Montréal</span>
    <a href="tel:+15142704352">(514) 270-4352</a>
    <span data-en="Service in French and English">Service en français et en anglais</span>
  </div>
</div>
'''

FOOTER = '''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="flogo"><img src="assets/logo-opera.png" alt="Opera Upholstering"></div>
        <p style="margin-top:16px;max-width:34ch" data-en="Upholstery, antique restoration and hand caning on Plaza Saint-Hubert since 1955.">Rembourrage, restauration d’antiquités et cannage tissé à la main sur la Plaza Saint-Hubert depuis 1955.</p>
        <p style="margin-top:14px"><a href="tel:+15142704352">(514) 270-4352</a><br>7498 rue Saint-Hubert<br>Montréal (Québec) H2R 2N3</p>
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
        <a href="savoir-faire.html#glossaire" data-en="Glossary">Glossaire</a><br>
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
      <span data-en="Est. 1955 · Plaza Saint-Hubert">Depuis 1955 · Plaza Saint-Hubert</span>
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
  <a class="btn light" href="tel:+15142704352" data-en="Call">Appeler</a>
  <a class="btn outline-light" href="index.html#soumission" data-en="Quote">Soumission</a>
</div>

<script src="assets/site.js?v={JSVER}"></script>
'''

def page(filename, title, desc, body, statusbar=False):
    footer = FOOTER.replace('{JSVER}', ver('assets/site.js'))
    html = head(title, desc, filename).replace('{PREPAINT}', PREPAINT) + '\n' + header(filename) + (STATUSBAR if statusbar else '') + '\n<main id="contenu">\n' + body + '\n</main>\n\n' + footer + '\n</body>\n</html>\n'
    pathlib.Path(filename).write_text(html, encoding='utf-8')
    print('wrote', filename, len(html), 'bytes')

def sec(sid, extra_class='', keep_id=None):
    """Re-wrap an extracted planche body as a plain section."""
    cls = ('section' + (' ' + extra_class if extra_class else '')).replace('section', '').strip()
    attrs = (' class="%s"' % cls) if cls else ''
    return '<section%s id="%s">%s\n</section>' % (attrs, keep_id or sid, S[sid])

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
for k in ('cannage','calculateur','prix','questions','anatomie','procede','glossaire','bibliotheque','performance'):
    S[k] = S[k].replace('href="#soumission"', 'href="index.html#soumission"')
print('sections loaded')

# ═════════════════════════ ACCUEIL ═════════════════════════
SERVICES_SHORT = [
 ('Fauteuils &amp; sofas','Armchairs &amp; sofas',
  'La pièce est dégarnie jusqu’à la structure. Sangles, ressorts et bourrage sont refaits avant la pose du tissu.',
  'The piece is stripped to the frame. Webbing, springs and stuffing are rebuilt before the cloth is fitted.','3–5 semaines','3–5 weeks'),
 ('Restauration d’antiquités','Antique restoration',
  'Sangles de jute, crin conservé, ressorts guindés à la main et semences sur les structures d’époque.',
  'Jute webbing, horsehair kept, hand-tied springs and tacks on period frames.','5–9 semaines','5–9 weeks'),
 ('Cannage &amp; rotin','Cane &amp; rattan',
  'Cannage tissé à la main, trou par trou, ou cannage en feuille posé en rainure. Vingt maillages en stock.',
  'Cane woven by hand, hole by hole, or sheet cane set into a spline groove. Twenty meshes in stock.','2–4 semaines','2–4 weeks'),
 ('Chaises de salle à manger','Dining chairs',
  'Traitées en lot et chiffrées par ensemble. Un tissu performance convient mieux à une salle à manger.',
  'Handled as a batch and priced by the set. A performance fabric suits a dining room better.','1–3 semaines','1–3 weeks'),
 ('Têtes de lit','Headboards',
  'Toute hauteur et toute forme : unie, à cannelures ou capitonnée, fixée au mur ou au sommier.',
  'Any height and any shape: plain, channelled or deep-buttoned, wall or bed mounted.','2–4 semaines','2–4 weeks'),
 ('Coussins &amp; extérieur','Cushions &amp; outdoor',
  'Sunbrella et acryliques teints dans la masse, coupés au gabarit, fil de qualité marine.',
  'Sunbrella and solution-dyed acrylics, cut to template, marine-grade thread.','2–3 semaines','2–3 weeks'),
 ('Banquettes &amp; contrat','Banquettes &amp; contract',
  'Restaurants, cliniques et hôtellerie. Chiffré au pied linéaire, cotes d’abrasion et d’ignifugation vérifiées.',
  'Restaurants, clinics and hospitality. Quoted per linear foot, abrasion and fire ratings verified.','Sur soumission','Quoted'),
 ('Structure &amp; ressorts','Frames &amp; springs',
  'Traverses fendues, blocs de coin remplacés, sièges affaissés, mécanismes d’inclinaison entretenus.',
  'Cracked rails, corner blocks replaced, sagging seats, recliner mechanisms serviced.','Estimation gratuite','Free estimate'),
 ('Cuir','Leather',
  'Cuir pleine fleur cousu et tendu à la main : fauteuils, banquettes, capitonnage et sièges d’auto anciens.',
  'Full-grain leather, sewn and stretched by hand: armchairs, banquettes, buttoning and vintage car seats.','4–7 semaines','4–7 weeks'),
 ('Décapage &amp; finition du bois','Wood stripping &amp; finishing',
  'Le bois apparent est décapé, poncé, teint et refini : vernis, huile ou cire, selon la pièce.',
  'Show-wood is stripped, sanded, stained and refinished — varnish, oil or wax, to suit the piece.','2–4 semaines','2–4 weeks'),
 ('Cueillette &amp; livraison','Pick-up &amp; delivery',
  'On vient chercher la pièce et on la rapporte, sur l’île de Montréal et en proche banlieue.',
  'We collect the piece and bring it back, across the island of Montreal and the near suburbs.','Sur demande','On request'),
]

svc_cards = '\n'.join(
 '''      <article class="svc rise">
        <h3 data-en="%s">%s</h3>
        <p data-en="%s">%s</p>
        <div class="meta"><span data-en="Typical delay">Délai type</span><b data-en="%s">%s</b></div>
      </article>''' % (en, fr, den, dfr, men, mfr)
 for fr, en, dfr, den, mfr, men in SERVICES_SHORT)

HOME = '''<section class="hero" id="haut">
  <div class="hero-media">
    <img class="hero-photo" src="assets/hero.jpg" alt="Un fauteuil pivotant en cuir brun, refait à l’atelier, dans une pièce sombre éclairée à la lampe." fetchpriority="high" width="2000" height="1116">
    <span class="hero-scrim"></span>
  </div>
  <div class="hero-type">
    <span class="lbl" data-en="Plaza Saint-Hubert · Montréal">Plaza Saint-Hubert · Montréal</span>
    <h1 data-en="Seventy-one years at the same bench.">Soixante et onze ans au même établi.</h1>
    <p class="hero-sub" data-en="Upholstering · Leather · Restoration · Caning">Rembourrage · Cuir · Restauration · Cannage</p>
    <p class="tagline" data-en="The frame is opened before any fabric is discussed.">On ouvre la structure avant de parler de tissu.</p>
    <p class="lede" data-en="Full reupholstery in fabric and leather, antique restoration and hand caning at 7498 rue Saint-Hubert since 1955. Estimates are made from photographs and returned the next business day.">Rembourrage complet en tissu et en cuir, restauration de meubles anciens et cannage tissé à la main, au 7498, rue Saint-Hubert depuis 1955. Les estimations se font sur photographies et reviennent le jour ouvrable suivant.</p>
    <div class="hero-cta">
      <a class="btn light" href="#soumission" data-en="Request an estimate">Demander une estimation</a>
      <a class="btn outline-light" href="#realisations" data-en="See the work">Voir les réalisations</a>
    </div>
    <div class="hero-figures">
      <div class="fig"><b>71</b><span data-en="years on Saint-Hubert">ans rue Saint-Hubert</span></div>
      <div class="fig"><b>58</b><span data-en="collections in stock">collections en magasin</span></div>
      <div class="fig"><b>20</b><span data-en="cane weaves">maillages de cannage</span></div>
      <div class="fig"><b>4,3</b><span data-en="Google · 47 reviews">Google · 47 avis</span></div>
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
      <p class="kicker" data-en="Photographed at 7498 rue Saint-Hubert. Fabric and leather, antiques and modern pieces, and the occasional sleigh.">Photographiées au 7498, rue Saint-Hubert. Tissu et cuir, antiquités et pièces modernes, et parfois un traîneau.</p>
    </div>
    <div class="cols work" data-stagger>
      <figure class="fig-sq rise">
        <img src="assets/travaux/cuir-elda.jpg" alt="Fauteuil pivotant enveloppant, entièrement refait en cuir brun." loading="lazy" width="1100" height="1100">
        <figcaption data-en="Swivel lounge chair · full-grain leather">Fauteuil pivotant · cuir pleine fleur</figcaption>
      </figure>
      <figure class="fig-sq rise">
        <img src="assets/travaux/louis-xv-fleuri.jpg" alt="Fauteuil Louis XV recouvert d’un imprimé floral, galon clouté sur bois apparent." loading="lazy" width="1100" height="1100">
        <figcaption data-en="Louis XV armchair · printed linen and nailhead trim">Fauteuil Louis XV · lin imprimé et galon clouté</figcaption>
      </figure>
      <figure class="fig-sq rise">
        <img src="assets/travaux/bergeres-bleues.jpg" alt="Paire de bergères à oreilles en tissu bleu à motif, bois laqué crème." loading="lazy" width="1100" height="1100">
        <figcaption data-en="Pair of wing chairs · lacquered show-wood">Paire de bergères à oreilles · bois laqué</figcaption>
      </figure>
      <figure class="fig-sq rise">
        <img src="assets/travaux/art-deco-chevron.jpg" alt="Fauteuil art déco en noyer recouvert d’un tissé à chevrons multicolores." loading="lazy" width="1100" height="1100">
        <figcaption data-en="Art deco tub chair · chevron weave">Fauteuil art déco · tissé à chevrons</figcaption>
      </figure>
      <figure class="fig-sq rise">
        <img src="assets/travaux/fauteuil-tonneau.jpg" alt="Fauteuil tonneau à bois noirci sculpté, recouvert d’un tissé bleu à feuillage." loading="lazy" width="1100" height="1100">
        <figcaption data-en="Barrel chair · carved ebonised frame">Fauteuil tonneau · bois sculpté noirci</figcaption>
      </figure>
      <figure class="fig-sq rise">
        <img src="assets/travaux/traineau.jpg" alt="Traîneau ancien en bois cintré, assise refaite en cuir rouge à cannelures." loading="lazy" width="1100" height="1100">
        <figcaption data-en="Antique sleigh · fluted red leather">Traîneau ancien · cuir rouge à cannelures</figcaption>
      </figure>
    </div>
    <div class="endcta rise">
      <a class="btn" href="#soumission" data-en="Request an estimate">Demander une estimation</a>
      <a class="btn ghost" href="tissus.html" data-en="Discover the fabrics">Découvrir les tissus</a>
    </div>
  </div>
</section>

<section class="sunk" id="cannage-teaser">
  <div class="wrap">
    <div class="cols-2 rise">
      <figure class="fig-wide">
        <img src="assets/travaux/rocking-cannage.jpg" alt="Chaise berçante en rotin recannée à la main à l’atelier." loading="lazy" width="1100" height="1100">
      </figure>
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

''' + sec('soumission')

page('index.html',
     'Opera Upholstering — Rembourrage, restauration et cannage · Montréal',
     'Atelier de rembourrage sur la Plaza Saint-Hubert depuis 1955. Restauration de meubles anciens, cannage, banquettes, têtes de lit. Des centaines de tissus en magasin.',
     HOME, statusbar=True)

# ═════════════════════════ SOUS-PAGES ═════════════════════════
# ═════════════════════════ À PROPOS ═════════════════════════
APROPOS = '''<section>
  <div class="wrap">
    <div class="sec-head rise">
      <span class="lbl" data-en="About">À propos</span>
      <h1 data-en="The shop on Saint-Hubert">L’atelier de la rue Saint-Hubert</h1>
      <p class="kicker" data-en="Opera has been upholstering furniture at 7498 rue Saint-Hubert since 1955. Same trade, same street, three generations of customers.">Opera rembourre des meubles au 7498, rue Saint-Hubert depuis 1955. Le même métier, la même rue, trois générations de clients.</p>
    </div>

    <div class="cols-2 rise">
      <div>
        <p class="muted" data-en="The shop opened when Plaza Saint-Hubert was still lined with tailors and furriers. Most of those trades have gone. Upholstery stayed, because a well-built chair is worth repairing and because someone has to know how.">L’atelier a ouvert quand la Plaza Saint-Hubert comptait encore des tailleurs et des fourreurs. La plupart de ces métiers ont disparu. Le rembourrage est resté, parce qu’un fauteuil bien bâti mérite d’être réparé et parce qu’il faut bien que quelqu’un sache le faire.</p>
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
      <div><h3 data-en="Since 1955">Depuis 1955</h3><p class="muted small" data-en="Seventy-one years at the same address, through the whole life of the Plaza and its marquee.">Soixante et onze ans à la même adresse, à travers toute la vie de la Plaza et de sa marquise.</p></div>
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
     'À propos — Opera Upholstering, rue Saint-Hubert depuis 1955',
     'Atelier de rembourrage au 7498, rue Saint-Hubert depuis 1955. Rembourrage, restauration d’antiquités, cannage et finition du bois, tout sur place.',
     APROPOS)

page('tissus.html',
     'La bibliothèque de tissus — Opera Upholstering',
     'Dix maisons de tissus, des centaines de cartables : velours, bouclé, chenille, tissés, performance et extérieur. Réservez trois échantillons gratuits au comptoir.',
     sec('bibliotheque') + '\n' + sec('performance', 'sunk'))

page('savoir-faire.html',
     'Savoir-faire — comment ça marche · Opera Upholstering',
     'Les six étapes de l’atelier, ce qui décide du prix, les questions courantes et le glossaire des mots qui apparaissent sur une estimation.',
     sec('procede') + '\n' + sec('prix', 'sunk') + '\n' + sec('questions') + '\n' + sec('glossaire', 'sunk'))

page('cannage.html',
     'Cannage, roseau et jonc — Opera Upholstering',
     'Cannage tissé à la main ou en feuille, jonc, corde danoise et rotin. Vingt maillages en stock, tissages sur mesure en commande spéciale.',
     sec('cannage'))

