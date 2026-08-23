# -*- coding: utf-8 -*-
"""Assemble the Opéra Rembourrage site from shared partials.
Run:  python3 build.py
"""
import json, re, pathlib

S = json.loads(pathlib.Path('content.json').read_text(encoding='utf-8'))

NAV = [
    ('index.html',        'Accueil',          'Home'),
    ('tissus.html',       'La bibliothèque',  'The library'),
    ('savoir-faire.html', 'Savoir-faire',     'Craft'),
    ('cannage.html',      'Cannage',          'Caning'),
    ('calculateur.html',  'Calculateur',      'Yardage'),
]

def head(title, desc):
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/logo-opera.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..700&family=Jost:wght@300;400;500&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&display=swap">
<link rel="stylesheet" href="assets/site.css">
'''

def header(current):
    links = []
    for href, fr, en in NAV:
        cur = ' aria-current="page"' if href == current else ''
        links.append(f'      <a href="{href}"{cur} data-en="{en}">{fr}</a>')
    links.append('      <a href="index.html#soumission" data-en="Contact">Contact</a>')
    return '''<a class="skip" href="#contenu" data-en="Skip to content">Aller au contenu</a>

<header class="topbar">
  <div class="wrap bar">
    <a class="logo" href="index.html" aria-label="Opera Upholstering — accueil">
      <img src="assets/logo-opera.png" alt="Opera Upholstering">
    </a>
    <nav class="navlinks" aria-label="Principal">
''' + '\n'.join(links) + '''
    </nav>
    <div class="navtools">
      <div class="langtog" role="group" aria-label="Langue / Language">
        <button type="button" id="btn-fr" aria-pressed="true">FR</button>
        <button type="button" id="btn-en" aria-pressed="false">EN</button>
      </div>
      <a class="btn" href="index.html#soumission" data-en="Get a quote">Soumission</a>
    </div>
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
        <h4 data-en="Services">Services</h4>
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
        <h4 data-en="Learn">Comprendre</h4>
        <p><a href="tissus.html" data-en="The fabric library">La bibliothèque de tissus</a><br>
        <a href="tissus.html#performance" data-en="Which cloth survives your household">Quel tissu survit à votre maison</a><br>
        <a href="savoir-faire.html" data-en="What is under the fabric">Ce qu’il y a sous le tissu</a><br>
        <a href="savoir-faire.html#glossaire" data-en="Glossary">Glossaire</a><br>
        <a href="calculateur.html" data-en="Yardage calculator">Calculateur de verges</a><br>
        <a href="calculateur.html#prix" data-en="What decides the price">Ce qui décide du prix</a><br>
        <a href="calculateur.html#questions" data-en="Questions">Questions</a></p>
      </div>
      <div>
        <h4 data-en="Served areas">Secteurs desservis</h4>
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

<script src="assets/site.js"></script>
'''

def page(filename, title, desc, body, statusbar=False):
    html = head(title, desc) + '\n' + header(filename) + (STATUSBAR if statusbar else '') + '\n<main id="contenu">\n' + body + '\n</main>\n\n' + FOOTER
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
 ('Têtes de lit sur mesure','Custom headboards',
  'Hauteur et forme sur mesure : unie, à cannelures ou capitonnée, fixée au mur ou au sommier.',
  'Height and shape made to measure: plain, channelled or deep-buttoned, wall or bed mounted.','2–4 semaines','2–4 weeks'),
 ('Coussins &amp; extérieur','Cushions &amp; outdoor',
  'Sunbrella et acryliques teints dans la masse, coupés au gabarit, fil de qualité marine.',
  'Sunbrella and solution-dyed acrylics, cut to template, marine-grade thread.','2–3 semaines','2–3 weeks'),
 ('Banquettes &amp; contrat','Banquettes &amp; contract',
  'Restaurants, cliniques et hôtellerie. Chiffré au pied linéaire, cotes d’abrasion et d’ignifugation vérifiées.',
  'Restaurants, clinics and hospitality. Quoted per linear foot, abrasion and fire ratings verified.','Sur soumission','Quoted'),
 ('Structure &amp; ressorts','Frames &amp; springs',
  'Traverses fendues, blocs de coin remplacés, sièges affaissés, mécanismes d’inclinaison entretenus.',
  'Cracked rails, corner blocks replaced, sagging seats, recliner mechanisms serviced.','Estimation gratuite','Free estimate'),
]

svc_cards = '\n'.join(
 '''      <article class="svc rise">
        <h3 data-en="%s">%s</h3>
        <p data-en="%s">%s</p>
        <div class="meta"><span data-en="Typical delay">Délai type</span><b data-en="%s">%s</b></div>
      </article>''' % (en, fr, den, dfr, men, mfr)
 for fr, en, dfr, den, mfr, men in SERVICES_SHORT)

HOME = '''<section class="hero" id="haut">
  <div class="hero-type">
    <span class="lbl" data-en="Plaza Saint-Hubert · Montréal">Plaza Saint-Hubert · Montréal</span>
    <h1 data-en="Seventy-one years at the same bench.">Soixante et onze ans au même établi.</h1>
    <p class="hero-sub" data-en="Upholstering · Restoration · Caning">Rembourrage · Restauration · Cannage</p>
    <p class="tagline" data-en="The frame is opened before any fabric is discussed.">On ouvre la structure avant de parler de tissu.</p>
    <p class="lede" data-en="Full reupholstery, antique restoration and hand caning at 7498 rue Saint-Hubert since 1955. Estimates are made from photographs and returned the next business day.">Rembourrage complet, restauration de meubles anciens et cannage tissé à la main, au 7498, rue Saint-Hubert depuis 1955. Les estimations se font sur photographies et reviennent le jour ouvrable suivant.</p>
    <div class="hero-cta">
      <a class="btn light" href="#soumission" data-en="Request an estimate">Demander une estimation</a>
      <a class="btn outline-light" href="tissus.html" data-en="The fabric library">La bibliothèque de tissus</a>
    </div>
    <div class="hero-figures">
      <div class="fig"><b>71</b><span data-en="years on Saint-Hubert">ans rue Saint-Hubert</span></div>
      <div class="fig"><b>58</b><span data-en="collections in stock">collections en magasin</span></div>
      <div class="fig"><b>20</b><span data-en="cane weaves">maillages de cannage</span></div>
      <div class="fig"><b>4,3</b><span data-en="Google · 47 reviews">Google · 47 avis</span></div>
    </div>
  </div>
  <div class="hero-photo">
    <img src="assets/bibliotheque.jpg" alt="La salle d’échantillons de l’atelier, du sol au plafond." loading="eager">
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
      <div class="cols" data-stagger style="gap:16px">
        <figure class="fig-tall rise">
          <img src="assets/etabli.jpg" alt="Établi de rembourreur : tendeur à sangles, jute, ficelle, semences, et une bergère à demi dégarnie." loading="lazy">
          <figcaption data-en="The bench">L’établi</figcaption>
        </figure>
        <figure class="fig-tall rise">
          <img src="assets/ressorts.jpg" alt="Ressorts guindés à la ficelle sur des sangles de jute neuves." loading="lazy">
          <figcaption data-en="Springs, hand-tied">Ressorts guindés à la main</figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<section id="bibliotheque">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="lbl" data-en="The library">La bibliothèque</span>
      <h2 data-en="The fabric library">La bibliothèque de tissus</h2>
      <p class="kicker" data-en="Nine houses, fifty-eight collections and several hundred sample books line the sample room, from performance velvet to marine acrylic. Any three swatches can be set aside at the counter, at no charge.">Neuf maisons, cinquante-huit collections et plusieurs centaines de cartables garnissent la salle d’échantillons, du velours performance à l’acrylique marine. Trois échantillons, quels qu’ils soient, peuvent être mis de côté au comptoir, sans frais.</p>
    </div>
    <div class="grid-swatch rise" data-swatchgrid data-limit="12"></div>
    <div class="endcta rise">
      <a class="btn" href="tissus.html" data-en="Browse the full library">Parcourir la bibliothèque</a>
      <a class="btn ghost" href="tissus.html#performance" data-en="Which cloth survives your household">Quel tissu survit à votre maison</a>
    </div>
  </div>
</section>

<section class="sunk" id="cannage-teaser">
  <div class="wrap">
    <div class="cols-2 rise">
      <figure class="fig-wide">
        <img src="assets/cannage.jpg" alt="Mains tissant le cannage à la main dans les trous percés d’un siège ancien." loading="lazy">
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
page('tissus.html',
     'La bibliothèque de tissus — Opera Upholstering',
     'Dix maisons de tissus, des centaines de cartables : velours, bouclé, chenille, tissés, performance et extérieur. Réservez trois échantillons gratuits au comptoir.',
     sec('bibliotheque') + '\n' + sec('performance', 'sunk'))

page('savoir-faire.html',
     'Savoir-faire — ce qu’il y a sous le tissu · Opera Upholstering',
     'La coupe d’un siège rembourré en dix couches, les six étapes de l’atelier, et le glossaire de vingt mots qui apparaissent sur une estimation.',
     sec('anatomie') + '\n' + sec('procede', 'sunk') + '\n' + sec('glossaire'))

page('cannage.html',
     'Cannage, roseau et jonc — Opera Upholstering',
     'Cannage tissé à la main ou en feuille, jonc, corde danoise et rotin. Vingt maillages en stock, tissages sur mesure en commande spéciale.',
     sec('cannage'))

page('calculateur.html',
     'Calculateur de verges et prix — Opera Upholstering',
     'Combien de tissu pour un sofa, un fauteuil ou six chaises ? Les allocations standards du métier, ce qui décide du prix, et les questions qu’on reçoit chaque semaine.',
     sec('calculateur') + '\n' + sec('prix', 'sunk') + '\n' + sec('questions'))
