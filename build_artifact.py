# -*- coding: utf-8 -*-
"""Fold the five pages into one self-contained file for preview/sharing.
Inlines CSS, JS and every image as a data URI, and adds a small view router.
Run:  python3 build_artifact.py
"""
import re, base64, pathlib, mimetypes

PAGES = [
    ('index',        'index.html',        'Accueil',      'Home'),
    ('a-propos',     'a-propos.html',     'À propos',     'About'),
    ('savoir-faire', 'savoir-faire.html', 'Savoir-faire', 'Craft'),
    ('cannage',      'cannage.html',      'Cannage',      'Caning'),
    ('tissus',       'tissus.html',       'Les tissus',   'Fabrics'),
]

def datauri(path):
    mt = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return 'data:%s;base64,%s' % (mt, base64.b64encode(pathlib.Path(path).read_bytes()).decode())

CACHE = {}
def inline_assets(html):
    for m in set(re.findall(r'(?:src|href)="(assets/[^"]+\.(?:jpg|jpeg|png|webp|mp4))"', html)):
        if m not in CACHE: CACHE[m] = datauri(m)
        html = html.replace('"%s"' % m, '"%s"' % CACHE[m])
    return html

views = []
for slug, fname, fr, en in PAGES:
    src = pathlib.Path(fname).read_text(encoding='utf-8')
    main = re.search(r'<main id="contenu">(.*?)\n</main>', src, re.S).group(1)
    # cross-page links become view switches
    for s2, f2, _, _ in PAGES:
        main = main.replace('href="%s#' % f2, 'data-goto="%s" href="#' % s2)
        main = main.replace('href="%s"' % f2, 'data-goto="%s" href="#%s"' % (s2, s2))
    if slug == 'index':
        main = main.replace('<section id="bibliotheque">', '<section id="bibliotheque-apercu">')
    views.append('<div class="view" id="view-%s"%s>%s\n</div>' % (slug, '' if slug == 'index' else ' hidden', main))

nav = '\n'.join(
    '      <a href="#%s" data-goto="%s"%s data-en="%s">%s</a>' % (s, s, ' aria-current="page"' if s == 'index' else '', en, fr)
    for s, f, fr, en in PAGES)

css = pathlib.Path('assets/site.css').read_text(encoding='utf-8')
js  = pathlib.Path('assets/site.js').read_text(encoding='utf-8')
logo = datauri('assets/logo-opera.png')

foot_src = pathlib.Path('index.html').read_text(encoding='utf-8')
footer = re.search(r'<footer>.*?</div>\n\n<script', foot_src, re.S).group(0)
footer = footer[:footer.rindex('<script')]
for s2, f2, _, _ in PAGES:
    footer = footer.replace('href="%s#' % f2, 'data-goto="%s" href="#' % s2)
    footer = footer.replace('href="%s"' % f2, 'data-goto="%s" href="#%s"' % (s2, s2))
footer = footer.replace('src="assets/logo-opera.png"', 'src="%s"' % logo)

statusbar = re.search(r'<div class="statusbar">.*?</div>\n</div>', foot_src, re.S).group(0)

ROUTER = """
<script>
(function(){
  var views = %s;
  function show(slug, frag){
    if(views.indexOf(slug) < 0) slug = 'index';
    views.forEach(function(v){
      var el = document.getElementById('view-' + v);
      if(el) el.hidden = (v !== slug);
    });
    document.querySelectorAll('[data-goto]').forEach(function(a){
      if(a.closest('.navlinks')){
        if(a.getAttribute('data-goto') === slug) a.setAttribute('aria-current','page');
        else a.removeAttribute('aria-current');
      }
    });
    var target = frag && document.getElementById(frag);
    if(target && !target.closest('[hidden]')) target.scrollIntoView({block:'start'});
    else window.scrollTo(0, 0);
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[data-goto]');
    if(!a) return;
    e.preventDefault();
    var href = a.getAttribute('href') || '';
    var frag = href.indexOf('#') === 0 ? href.slice(1) : '';
    var slug = a.getAttribute('data-goto');
    if(frag === slug) frag = '';
    show(slug, frag);
  });
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href^="#"]:not([data-goto])');
    if(!a) return;
    var id = a.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if(el && el.closest('[hidden]')){ e.preventDefault(); show('index', id); }
  });
})();
</script>
""" % repr([p[0] for p in PAGES]).replace("'", '"')

html = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Opera Upholstering</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..700&family=Jost:wght@300;400;500&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&display=swap">
<style>
%s
.view[hidden]{display:none}
</style>
<script>
(function(){
  var replay = location.hash === '#intro' || location.hash === '#introhold';
  var seen;
  try { seen = sessionStorage.getItem('operaIntro'); } catch (e) { seen = null; }
  if (!replay && (seen || matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    document.documentElement.classList.add('intro-skip');
  }
})();
</script>

<div class="splash" id="splash" aria-hidden="true">
  <div class="splash-lock">
    <img class="splash-mark" src="__MARK__" alt="" width="511" height="140">
    <span class="splash-rule"></span>
    <img class="splash-sub" src="__SUB__" alt="" width="511" height="30">
  </div>
</div>

<a class="skip" href="#contenu">Aller au contenu</a>
<header class="topbar">
  <div class="wrap bar">
    <a class="logo" href="#index" data-goto="index" aria-label="Opera Upholstering">
      <img src="%s" alt="Opera Upholstering">
    </a>
    <nav class="navlinks" aria-label="Principal">
%s
    </nav>
    <div class="navtools">
      <div class="langtog" role="group" aria-label="Langue / Language">
        <button type="button" id="btn-fr" aria-pressed="true">FR</button>
        <button type="button" id="btn-en" aria-pressed="false">EN</button>
      </div>
      <a class="btn" href="#soumission" data-en="Get a quote">Soumission</a>
    </div>
  </div>
</header>
%s
<main id="contenu">
%s
</main>

%s

<script>
%s
</script>
%s
""" % (css, logo, nav, statusbar, '\n'.join(views), footer, js, ROUTER)

html = html.replace('__MARK__', datauri('assets/logo-mark.png'))
html = html.replace('__SUB__', datauri('assets/logo-sub.png'))
html = inline_assets(html)
out = pathlib.Path('../opera-site-preview.html')
out.write_text(html, encoding='utf-8')
print('wrote', out, round(len(html.encode())/1024/1024, 2), 'MB')
