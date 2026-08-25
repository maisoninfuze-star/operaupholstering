
(function(){
"use strict";

/* ═══════ 1 · LANGUE ═══════════════════════════════ */
var LANG = 'fr';
var PLACEHOLDERS = {
  'q-piece': ['Fauteuil club, 6 chaises, banquette de 12 pi…','Club chair, 6 dining chairs, 12 ft banquette…'],
  'q-msg'  : ['Âge approximatif, ce qui ne va pas, si ça branle ou si ça s’affaisse, tissu souhaité, échéance…','Rough age, what is wrong, whether it wobbles or sags, fabric you have in mind, your deadline…']
};
function applyLang(lang){
  LANG = lang;
  document.querySelectorAll('[data-en]').forEach(function(el){
    if(!el.hasAttribute('data-fr')) el.setAttribute('data-fr', el.innerHTML);
    el.innerHTML = (lang === 'en') ? el.getAttribute('data-en') : el.getAttribute('data-fr');
  });
  Object.keys(PLACEHOLDERS).forEach(function(id){
    var el = document.getElementById(id);
    if(el) el.placeholder = PLACEHOLDERS[id][lang === 'en' ? 1 : 0];
  });
  document.documentElement.lang = lang;
  var bf = document.getElementById('btn-fr'), be = document.getElementById('btn-en');
  if(bf) bf.setAttribute('aria-pressed', String(lang === 'fr'));
  if(be) be.setAttribute('aria-pressed', String(lang === 'en'));
  try{ localStorage.setItem('opera-lang', lang); }catch(e){}
  renderFilters(); renderSwatches(); renderWeaves(); renderTray(); buildPieceSelect(); calc(); openState();
}
document.querySelectorAll('#btn-fr').forEach(function(b){ b.addEventListener('click', function(){ applyLang('fr'); }); });
document.querySelectorAll('#btn-en').forEach(function(b){ b.addEventListener('click', function(){ applyLang('en'); }); });
function t(fr, en){ return LANG === 'en' ? en : fr; }

/* ═══════ 2 · LA BIBLIOTHÈQUE ══════════════════════ */
/* Sélection représentative des collections en magasin.
   Les couleurs à l’écran sont approximatives. */
/* ── La bibliothèque ──────────────────────────────────────────
   Les collections ci-dessous sont celles tenues en magasin.
   Les coloris illustrent la gamme de chaque collection; ce ne
   sont pas des références de commande. ───────────────────── */
var TONES = {
  creme : [['Ivoire','Ivory','#EFE9DA'],['Crème','Cream','#E7DFCB'],['Écru','Écru','#DED5BE'],['Coquille','Shell','#E3DACB'],['Lin','Linen','#D9D0BB']],
  neutre: [['Avoine','Oat','#CFC1A2'],['Sable','Sand','#C9B896'],['Grège','Greige','#C4BAA6'],['Mastic','Putty','#B8AC92'],['Chanvre','Hemp','#BFB49B']],
  gris  : [['Perle','Pearl','#C3C1BA'],['Tourterelle','Dove','#B0AEA6'],['Étain','Pewter','#94958F'],['Ardoise','Slate','#74777C'],['Anthracite','Anthracite','#4A4C50']],
  vert  : [['Céladon','Celadon','#B4C3B0'],['Sauge','Sage','#A3AC92'],['Eucalyptus','Eucalyptus','#8B9B8A'],['Olive','Olive','#6D7048'],['Forêt','Forest','#33513F']],
  bleu  : [['Brume','Mist','#B7C3CC'],['Bleu de glace','Ice blue','#9FB0BE'],['Ardoise bleue','Blue slate','#54677A'],['Indigo','Indigo','#39456B'],['Marine','Navy','#2B3A55']],
  rouge : [['Terracotta','Terracotta','#A45B41'],['Brique','Brick','#96503F'],['Grenat','Garnet','#7E2231'],['Bordeaux','Bordeaux','#63202B'],['Rouille','Rust','#8E4A2E']],
  or    : [['Miel','Honey','#C89A4E'],['Ocre','Ochre','#B2843A'],['Safran','Saffron','#C4A24A'],['Bronze','Bronze','#8A6A24'],['Moutarde','Mustard','#A98B2E']],
  brun  : [['Noisette','Hazel','#A98A6B'],['Cognac','Cognac','#8B5A32'],['Tabac','Tobacco','#6F553A'],['Moka','Mocha','#57453A'],['Châtaigne','Chestnut','#7A5B44']],
  noir  : [['Charbon','Charcoal','#4A4844'],['Graphite','Graphite','#3E4145'],['Encre','Ink','#2E3033'],['Noir','Black','#26282C'],['Fusain','Coal','#37393C']]
};
var ALLFAM = ['creme','neutre','gris','vert','bleu','rouge','or','brun','noir'];
var WARM    = ['creme','neutre','brun','or','rouge'];
var COOL    = ['creme','neutre','gris','bleu','vert'];
var FULL    = ALLFAM;

/* nom, maison, texture, familles de couleurs, étiquettes */
var COLLECTIONS = [
  ['Majestic','Avant Garde','velours',FULL,['perf']],
  ['Splendid','Avant Garde','velours',FULL,['perf']],
  ['Playful','Avant Garde','motif',COOL,['perf']],
  ['Myriad','Avant Garde','motif',WARM,['perf']],
  ['Impression','Avant Garde','motif',COOL,['perf']],
  ['Camelot','Avant Garde','damas',WARM,[]],
  ['Delight','Avant Garde','tisse',FULL,['perf']],
  ['Eden','Avant Garde','tisse',COOL,['perf']],
  ['Mojo','Avant Garde','tisse',WARM,['perf']],
  ['Fusion','Avant Garde','tisse',FULL,['perf']],
  ['Identity','Avant Garde','tisse',COOL,['perf']],
  ['Network','Avant Garde','tisse',FULL,['perf']],
  ['Iconic','Avant Garde','tisse',WARM,['perf']],
  ['Studio II','Avant Garde','tisse',COOL,['perf']],
  ['Sensation','Avant Garde','chenille',WARM,['perf']],
  ['Melody','Avant Garde','chenille',COOL,['perf']],

  ['Affordable Lux','Ennis','boucle',['creme','neutre','gris','brun'],[]],
  ['Denali','Ennis','boucle',['creme','neutre','gris'],[]],
  ['Curated Lake House','Ennis','boucle',['creme','neutre','bleu'],[]],
  ['The Luxe Collection','Ennis','velours',FULL,[]],
  ['Marvel','Ennis','velours',WARM,[]],
  ['Scoop','Ennis','chenille',WARM,[]],
  ['Asher','Ennis','chenille',COOL,[]],
  ['Yates','Ennis','tisse',COOL,[]],
  ['Catalyst','Ennis','tisse',FULL,[]],
  ['Mixer','Ennis','tisse',FULL,[]],
  ['Comrade','Ennis','tisse',['gris','noir','bleu','vert'],['contrat']],
  ['Jeffery 2ᵉ éd.','Ennis','tisse',WARM,[]],
  ['Pace','Ennis','tisse',COOL,[]],
  ['Holistic','Ennis','tisse',['creme','neutre','vert','brun'],[]],
  ['Curated Town House','Ennis','tisse',['gris','bleu','noir','neutre'],[]],
  ['Felicity','Ennis','motif',WARM,[]],
  ['Our World','Ennis','motif',COOL,[]],
  ['Endurepel','Ennis','perf',FULL,['perf']],
  ['Self Expression','Ennis','perf',FULL,['perf']],
  ['Contract Vol. 1','Ennis','perf',['gris','noir','bleu','vert'],['contrat','perf']],
  ['Contract Vol. 2','Ennis','perf',['neutre','brun','or','rouge'],['contrat','perf']],

  ['Essentials','Charlotte','tisse',FULL,['vie']],
  ['Performance','Charlotte','perf',FULL,['perf','vie']],
  ['Crypton','Charlotte','perf',FULL,['perf','griffes','vie']],
  ['Crypton Revival','Charlotte','perf',COOL,['perf','griffes','vie']],
  ['Select Microsuède','Charlotte','suede',FULL,['griffes','vie']],
  ['Colors · Seaglass','Charlotte','tisse',['bleu','vert','gris'],['vie']],
  ['Colors · Adore','Charlotte','tisse',['rouge','brun','creme'],['vie']],
  ['Colors · Inspire','Charlotte','tisse',['gris','bleu','noir'],['vie']],
  ['Colors · Spring','Charlotte','tisse',['vert','creme','or'],['vie']],
  ['Colors · Gold','Charlotte','tisse',['or','brun','neutre'],['vie']],
  ['Outdoor Wovens','Charlotte','perf',['bleu','vert','neutre','gris'],['ext','perf']],
  ['Outdoor Prints','Charlotte','ext',['vert','bleu','creme'],['ext','perf']],

  ['Alpaga','Studio Tex','chenille',FULL,[]],
  ['Tambora','Elite','damas',WARM,[]],
  ['Versailles','Elite','damas',['or','rouge','creme','bleu'],[]],
  ['FA1030','BYC Tex','velours',['creme','neutre','vert','gris','bleu'],[]],
  ['Sunbrella','Sunbrella','tisse',['creme','neutre','bleu','vert','gris'],['ext','perf']],
  ['Sunbrella · Rayures','Sunbrella','raye',['creme','neutre','bleu'],['ext','perf']],
  ['Alta','Alta','tisse',FULL,[]],
  ['Bert Woll','Bert Woll','tisse',['gris','brun','vert','noir','neutre'],[]]
];

function shift(hex, amt){
  var n = parseInt(hex.slice(1), 16);
  var r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  function f(v){ return Math.max(0, Math.min(255, Math.round(v + (amt > 0 ? (255 - v) * amt : v * amt)))); }
  return '#' + ((1 << 24) + (f(r) << 16) + (f(g) << 8) + f(b)).toString(16).slice(1);
}

var SWATCHES = (function(){
  var out = [];
  COLLECTIONS.forEach(function(c){
    var name = c[0], house = c[1], tex = c[2], fams = c[3], tags = c[4];
    fams.forEach(function(fam, i){
      var tone = TONES[fam][i % TONES[fam].length];
      var s = { n:name, h:house, t:tex, c:tone[2], fam:fam, tags:tags,
                d:[tone[0], tone[1]] };
      if(tex === 'motif' || tex === 'damas' || tex === 'raye') s.c2 = shift(tone[2], .55);
      if(tex === 'ext'){ s.c = '#EDE8D6'; s.c2 = '#2F5A34'; s.c3 = '#7BA84C'; }
      out.push(s);
    });
  });
  return out;
})();

var HOUSES_F = [
  ['all','Toutes','All'],['Ennis','Ennis','Ennis'],['Charlotte','Charlotte','Charlotte'],
  ['Avant Garde','Avant Garde','Avant Garde'],['Studio Tex','Studio Tex','Studio Tex'],
  ['Elite','Elite','Elite'],['BYC Tex','BYC Tex','BYC Tex'],['Sunbrella','Sunbrella','Sunbrella'],
  ['Alta','Alta','Alta'],['Bert Woll','Bert Woll','Bert Woll']
];
var TEXTURES = [
  ['all','Toutes','All'],['velours','Velours','Velvet'],['boucle','Bouclé','Bouclé'],
  ['chenille','Chenille','Chenille'],['tisse','Tissés','Wovens'],['motif','Motifs','Patterns'],
  ['damas','Damassés','Damask'],['perf','Unis','Plains'],['suede','Microsuède','Microsuede'],
  ['ext','Imprimés ext.','Outdoor prints'],['raye','Rayures','Stripes']
];
var PERFS = [
  ['all','Toutes','All'],['perf','Anti-taches','Stain resistant'],['ext','Extérieur','Outdoor'],
  ['griffes','Résiste aux griffes','Claw resistant'],['contrat','Qualité contrat','Contract grade'],
  ['vie','Garantie à vie','Lifetime warranty']
];
var COLOURS = [
  ['all','Toutes','All'],['creme','Crème','Cream'],['neutre','Neutre','Neutral'],['gris','Gris','Grey'],
  ['vert','Vert','Green'],['bleu','Bleu','Blue'],['rouge','Rouge','Red'],['or','Or','Gold'],
  ['brun','Brun','Brown'],['noir','Noir','Black']
];
var state = { house:'all', texture:'all', perf:'all', colour:'all' };
var PAGE = 60, shownCount = PAGE;
var tray = [];
try{ tray = JSON.parse(localStorage.getItem('opera-tray') || '[]'); }catch(e){ tray = []; }
function saveTray(){ try{ localStorage.setItem('opera-tray', JSON.stringify(tray)); }catch(e){} }

function matches(s){
  if(state.house !== 'all' && s.h !== state.house) return false;
  if(state.texture !== 'all' && s.t !== state.texture) return false;
  if(state.perf !== 'all' && s.tags.indexOf(state.perf) < 0) return false;
  if(state.colour !== 'all' && s.fam !== state.colour) return false;
  return true;
}
function countFor(key, val){
  var saved = state[key], n;
  state[key] = val;
  n = SWATCHES.filter(matches).length;
  state[key] = saved;
  return n;
}
function renderFilterRow(id, defs, key){
  var box = document.getElementById(id);
  if(!box) return;
  box.innerHTML = '';
  defs.forEach(function(d){
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'pill';
    b.setAttribute('aria-pressed', String(state[key] === d[0]));
    var n = countFor(key, d[0]);
    b.innerHTML = t(d[1], d[2]) + '<span class="cnt">' + n + '</span>';
    if(n === 0 && d[0] !== 'all') b.disabled = true;
    b.addEventListener('click', function(){
      state[key] = d[0];
      shownCount = PAGE;
      renderFilters(); renderSwatches();
    });
    box.appendChild(b);
  });
}
function renderFilters(){
  if(!document.getElementById('f-texture')) return;
  renderFilterRow('f-house', HOUSES_F, 'house');
  renderFilterRow('f-texture', TEXTURES, 'texture');
  renderFilterRow('f-perf',    PERFS,    'perf');
  renderFilterRow('f-colour',  COLOURS,  'colour');
}
function badgeLabel(tag){
  var map = {perf:['Anti-taches','Stain resistant'], ext:['Extérieur','Outdoor'],
             griffes:['Griffes','Claw safe'], contrat:['Contrat','Contract'], vie:['Garantie à vie','Lifetime']};
  return map[tag] ? t(map[tag][0], map[tag][1]) : tag;
}
function clothStyle(s){
  var st = 'background-color:' + s.c + ';';
  if(s.c2) st += '--c2:' + s.c2 + ';';
  if(s.c3) st += '--c3:' + s.c3 + ';';
  return st;
}
function renderSwatches(){
  document.querySelectorAll('[data-swatchgrid]').forEach(renderSwatchGrid);
  var total = SWATCHES.filter(matches).length;
  var cn = document.getElementById('swcount');
  if(cn){
    var vis = Math.min(shownCount, total);
    cn.textContent = (vis < total ? vis + ' ' + t('sur','of') + ' ' + total : total + ' ' + t('coloris','colourways'));
  }
  var more = document.getElementById('loadmore');
  if(more){
    var left = total - shownCount;
    more.hidden = left <= 0;
    more.textContent = t('Voir 60 coloris de plus', 'Show 60 more colourways') + (left > 0 ? '  (' + left + ')' : '');
  }
}
function renderSwatchGrid(grid){
  var cap = grid.hasAttribute('data-paged') ? shownCount
          : parseInt(grid.getAttribute('data-limit') || '0', 10);
  var list = SWATCHES.filter(matches);
  if(cap > 0) list = list.slice(0, cap);
  grid.innerHTML = '';
  list.forEach(function(s, i){
    var key = s.n + '|' + s.d[0];
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'swatch';
    b.setAttribute('aria-pressed', String(tray.indexOf(key) >= 0));
    b.innerHTML =
      '<span class="cloth tx-' + s.t + '" style="' + clothStyle(s) + '"></span>' +
      '<span class="id"><b>' + s.n + '</b><i>' + s.h + '</i><em>' + t(s.d[0], s.d[1]) + '</em></span>' +
      '<span class="badges">' + s.tags.map(function(x){
        var cls = x === 'ext' ? 'badge ext' : (x === 'perf' || x === 'griffes' || x === 'vie' ? 'badge perf' : 'badge');
        return '<span class="' + cls + '">' + badgeLabel(x) + '</span>';
      }).join('') + '</span>';
    b.addEventListener('click', function(){ toggleTray(s, key, b); });
    b.style.setProperty('--s', Math.min(i * 18, 380) + 'ms');
    grid.appendChild(b);
  });
  requestAnimationFrame(function(){
    grid.querySelectorAll('.swatch').forEach(function(el){ el.classList.add('set'); });
  });
}
function toggleTray(s, key, btn){
  var i = tray.indexOf(key);
  if(i >= 0){ tray.splice(i, 1); }
  else {
    if(tray.length >= 3) tray.shift();
    tray.push(key);
  }
  saveTray();
  renderSwatches();
  renderTray();
}
function trayRecord(key){
  return SWATCHES.filter(function(s){ return s.n + '|' + s.d[0] === key; })[0];
}
function renderTray(){
  var box = document.getElementById('trayitems');
  var el  = document.getElementById('tray');
  if(!box || !el) return;
  box.innerHTML = '';
  tray.forEach(function(key){
    var s = trayRecord(key); if(!s) return;
    var chip = document.createElement('span');
    chip.className = 'tray-chip';
    chip.innerHTML = '<span class="mini tx-' + s.t + '" style="' + clothStyle(s) + '"></span>' +
                     '<span>' + s.n + ' · ' + t(s.d[0], s.d[1]) + '</span>' +
                     '<button type="button" aria-label="' + t('Retirer','Remove') + '">×</button>';
    chip.querySelector('button').addEventListener('click', function(){
      tray.splice(tray.indexOf(key), 1); saveTray(); renderSwatches(); renderTray();
    });
    box.appendChild(chip);
  });
  document.getElementById('traynote').textContent =
    tray.length >= 3 ? t('Plateau plein — trois échantillons.', 'Tray full — three swatches.')
                     : t('Jusqu’à trois échantillons, gratuits.', 'Up to three swatches, free.');
  el.classList.toggle('open', tray.length > 0);
  var f = document.getElementById('trayfield');
  var e = document.getElementById('trayecho');
  if(!f || !e) return;               /* le champ n'existe que sur la page d'accueil */
  if(tray.length){
    f.hidden = false;
    e.textContent = tray.map(function(k){
      var s = trayRecord(k); return s ? s.n + ' (' + s.h + ') — ' + t(s.d[0], s.d[1]) : '';
    }).join(' · ');
  } else { f.hidden = true; e.textContent = ''; }
}

/* ═══════ 3 · CANNAGE : LES MAILLAGES ══════════════ */
var WEAVES = [
  {n:'3/4" & 1" Mesh', k:'open',  s:26, d:['Trous très espacés','Widest hole spacing']},
  {n:'#107 5/8" Mesh', k:'open',  s:21, d:['Le plus courant','The most common']},
  {n:'#109 1/2" Mesh', k:'open',  s:17, d:['Chaises fines','Fine chair frames']},
  {n:'#110 7/16" Mesh',k:'open',  s:15, d:['Bergères et bras','Bergères and arms']},
  {n:'#111 3/8" Mesh', k:'open',  s:13, d:['Le plus serré','The tightest mesh']},
  {n:'BASS-1',         k:'close', s:9,  d:['Fibre de tilleul','Basswood fibre']},
  {n:'#402 Fine Close',k:'close', s:7,  d:['Tissage fin serré','Fine close weave']},
  {n:'#206 Medium Close',k:'close',s:11,d:['Tissage moyen','Medium close weave']},
  {n:'#207 5 mm Close',k:'close', s:13, d:['Cinq millimètres','Five millimetre']},
  {n:'403 & HERR-1',   k:'herr',  s:14, d:['Chevron','Herringbone']},
  {n:'TEA-1',          k:'close', s:8,  d:['Feuille de thé fine','Fine tea leaf']},
  {n:'TEA-4',          k:'herr',  s:10, d:['Feuille de thé chevron','Tea leaf herringbone']},
  {n:'Bamboo Tea',     k:'panel', s:16, d:['Bambou tressé','Woven bamboo']},
  {n:'X-Weave',        k:'close', s:6,  d:['Toile très fine','Very fine cloth weave']},
  {n:'Hick Panel',     k:'herr',  s:18, d:['Panneau tressé large','Wide woven panel']},
  {n:'Tatami',         k:'panel', s:24, d:['Latte japonaise','Japanese slat']},
  {n:'#1036 Wicker',   k:'close', s:12, d:['Osier','Wicker']},
  {n:'Radio Weave',    k:'close', s:9,  d:['Grille de radio ancienne','Vintage radio grille']},
  {n:'#506 Modern',    k:'open',  s:16, d:['Maille carrée moderne','Modern square mesh']},
  {n:'#807 Modern',    k:'open',  s:19, d:['Maille carrée large','Wide square mesh']}
];
function meshStyle(w){
  var s = w.s;
  if(w.k === 'open'){
    return 'background-image:' +
      'radial-gradient(circle at ' + (s/2) + 'px ' + (s/2) + 'px,rgba(40,28,12,.88) ' + (s*0.17) + 'px,transparent ' + (s*0.21) + 'px),' +
      'repeating-linear-gradient(0deg,rgba(96,66,26,.42) 0 ' + (s*0.2) + 'px,transparent ' + (s*0.2) + 'px ' + s + 'px),' +
      'repeating-linear-gradient(90deg,rgba(96,66,26,.42) 0 ' + (s*0.2) + 'px,transparent ' + (s*0.2) + 'px ' + s + 'px);' +
      'background-size:' + s + 'px ' + s + 'px,auto,auto;background-color:#DDB575;';
  }
  if(w.k === 'herr'){
    return 'background-image:' +
      'repeating-linear-gradient(45deg,rgba(120,84,36,.55) 0 ' + (s/2) + 'px,transparent ' + (s/2) + 'px ' + s + 'px),' +
      'repeating-linear-gradient(-45deg,rgba(255,238,206,.55) 0 ' + (s/2) + 'px,transparent ' + (s/2) + 'px ' + s + 'px);' +
      'background-color:#CFA260;';
  }
  if(w.k === 'panel'){
    return 'background-image:' +
      'repeating-linear-gradient(90deg,rgba(120,84,36,.5) 0 2px,transparent 2px ' + s + 'px),' +
      'repeating-linear-gradient(0deg,rgba(80,54,20,.28) 0 ' + s + 'px,rgba(255,240,210,.20) ' + s + 'px ' + (s*2) + 'px);' +
      'background-color:#C99C5C;';
  }
  return 'background-image:' +
    'repeating-linear-gradient(0deg,rgba(120,84,36,.48) 0 ' + (s/2) + 'px,transparent ' + (s/2) + 'px ' + s + 'px),' +
    'repeating-linear-gradient(90deg,rgba(255,240,210,.48) 0 ' + (s/2) + 'px,transparent ' + (s/2) + 'px ' + s + 'px);' +
    'background-color:#D2A566;';
}
function renderWeaves(){
  var g = document.getElementById('weavegrid');
  if(!g) return;
  g.innerHTML = '';
  WEAVES.forEach(function(w){
    var d = document.createElement('div');
    d.className = 'weave';
    d.innerHTML = '<div class="mesh" style="' + meshStyle(w) + '"></div>' +
                  '<div class="nm"><b>' + w.n + '</b><span>' + t(w.d[0], w.d[1]) + '</span></div>';
    g.appendChild(d);
  });
}

/* ═══════ 4 · ANATOMIE ═════════════════════════════ */
(function(){
  var anat = document.getElementById('anat');
  if(!anat) return;
  var groups = anat.querySelectorAll('.layer');
  function focusLayer(n){
    anat.classList.add('dim');
    groups.forEach(function(g){ g.classList.toggle('hot', g.getAttribute('data-layer') === String(n)); });
  }
  function clear(){ anat.classList.remove('dim'); groups.forEach(function(g){ g.classList.remove('hot'); }); }
  document.querySelectorAll('#anatlist button').forEach(function(b){
    var n = b.getAttribute('data-target');
    b.addEventListener('mouseenter', function(){ focusLayer(n); });
    b.addEventListener('focus',      function(){ focusLayer(n); });
    b.addEventListener('click',      function(){ focusLayer(n); });
    b.addEventListener('mouseleave', clear);
    b.addEventListener('blur',       clear);
  });
  groups.forEach(function(g){
    g.style.cursor = 'pointer';
    g.addEventListener('mouseenter', function(){ focusLayer(g.getAttribute('data-layer')); });
    g.addEventListener('mouseleave', clear);
  });
})();

/* ═══════ 5 · CALCULATEUR DE VERGES ════════════════ */
var PIECES = [
  {v:0.75, d:['Chaise de salle à manger — siège seulement','Dining chair — seat only']},
  {v:2,    d:['Chaise de salle à manger — siège et dossier','Dining chair — seat and back']},
  {v:1.5,  d:['Chaise d’appoint sans bras','Armless occasional chair']},
  {v:2.5,  d:['Chaise de bureau','Office chair']},
  {v:5,    d:['Fauteuil d’appoint','Accent armchair']},
  {v:7,    d:['Fauteuil club ou bergère','Club chair or bergère']},
  {v:8,    d:['Fauteuil inclinable','Recliner']},
  {v:2.5,  d:['Pouf ou ottomane','Ottoman or footstool']},
  {v:3,    d:['Banc ou bout de lit','Bench or bed-end']},
  {v:12,   d:['Causeuse deux places','Two-seat loveseat']},
  {v:16,   d:['Sofa trois places','Three-seat sofa']},
  {v:7,    d:['Sectionnel — par section','Sectional — per section']},
  {v:6,    d:['Tête de lit double (54 po)','Headboard, double (54 in)']},
  {v:8,    d:['Tête de lit queen','Headboard, queen']},
  {v:11,   d:['Tête de lit king','Headboard, king']},
  {v:1.75, d:['Banquette — par pied linéaire','Banquette — per linear foot']},
  {v:1.25, d:['Coussin de siège seul','Single seat cushion']},
  {v:1.5,  d:['Coussin d’extérieur — par coussin','Outdoor cushion — each']}
];
function buildPieceSelect(){
  var sel = document.getElementById('piece');
  if(!sel) return;
  var keep = sel.selectedIndex < 0 ? 10 : sel.selectedIndex;
  sel.innerHTML = '';
  PIECES.forEach(function(p, i){
    var o = document.createElement('option');
    o.value = i; o.textContent = t(p.d[0], p.d[1]);
    sel.appendChild(o);
  });
  sel.selectedIndex = keep;
}
function calc(){
  var sel = document.getElementById('piece');
  if(!sel) return;
  var idx = parseInt(sel.value || '10', 10);
  var p = PIECES[idx] || PIECES[10];
  var qty = Math.max(1, Math.min(40, parseInt(document.getElementById('qty').value || '1', 10)));
  var base = p.v * qty;
  var rows = [];
  rows.push([t('Base', 'Base') + ' × ' + qty, base.toFixed(2)]);
  var total = base;
  function add(cond, label, factor, flat){
    if(!cond) return;
    var delta = flat != null ? flat : total * factor;
    total += delta;
    rows.push([label, '+' + delta.toFixed(2)]);
  }
  add(document.getElementById('opt-repeat').checked,   t('Grand rapport de motif','Large pattern repeat'), 0.20);
  add(document.getElementById('opt-stripe').checked,   t('Raccord de rayures','Stripe matching'), 0.15);
  add(document.getElementById('opt-narrow').checked,   t('Laize de 45 po','45-inch width'), 0.20);
  add(document.getElementById('opt-skirt').checked,    t('Jupe','Skirt'), null, 2.5);
  add(document.getElementById('opt-contrast').checked, t('Passepoil contrastant','Contrast welting'), null, 1);
  var rounded = Math.ceil(total * 2) / 2;
  document.getElementById('yards').textContent = rounded.toFixed(1).replace('.0','').replace('.', t(',','.'));
  document.getElementById('unit').textContent = t(rounded > 1 ? 'verges' : 'verge', rounded > 1 ? 'yards' : 'yard');
  document.getElementById('calcnote').textContent = t(
    'Pour du tissu de 54 pouces, passepoil standard inclus, arrondi à la demi-verge supérieure. La coupe exacte se mesure sur votre pièce.',
    'For 54-inch goods, standard welting included, rounded up to the next half yard. The exact cut is measured off your piece.');
  var bd = document.getElementById('breakdown');
  bd.innerHTML = rows.map(function(r){ return '<div><span>' + r[0] + '</span><b>' + r[1] + '</b></div>'; }).join('') +
    '<div style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(243,237,225,.2)"><span>' +
    t('Arrondi','Rounded') + '</span><b>' + rounded.toFixed(1) + '</b></div>';
}
['piece','qty','opt-repeat','opt-stripe','opt-narrow','opt-skirt','opt-contrast'].forEach(function(id){
  var el = document.getElementById(id);
  if(el){ el.addEventListener('input', calc); el.addEventListener('change', calc); }
});

/* ═══════ 6 · HEURES D’OUVERTURE ═══════════════════ */
var HOURS = { 0:null, 1:[9,17], 2:[9,17], 3:[9,17], 4:[9,17], 5:[9,17], 6:[10,17] };
var DAYS_FR = ['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'];
var DAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
function montrealNow(){
  var s = new Date().toLocaleString('en-US', { timeZone: 'America/Toronto' });
  return new Date(s);
}
function fmt(h){ return LANG === 'en'
  ? (h > 12 ? (h - 12) + ' p.m.' : (h === 12 ? 'noon' : h + ' a.m.'))
  : h + ' h'; }
function openState(){
  var now = montrealNow(), day = now.getDay(), mins = now.getHours() * 60 + now.getMinutes();
  var today = HOURS[day], el = document.getElementById('openstate');
  if(!el) return;
  var open = !!today && mins >= today[0] * 60 && mins < today[1] * 60;
  var msg;
  if(open){
    msg = t('Ouvert — jusqu’à ' + fmt(today[1]), 'Open — until ' + fmt(today[1]));
  } else {
    var nxt = null;
    if(today && mins < today[0] * 60){
      nxt = day;
    } else {
      for(var i = 1; i <= 7; i++){
        var d = (day + i) % 7;
        if(HOURS[d]){ nxt = d; break; }
      }
    }
    var when = (nxt === day) ? t('aujourd’hui', 'today')
                             : (LANG === 'en' ? DAYS_EN[nxt] : DAYS_FR[nxt]);
    msg = t('Fermé — ouvre ' + when + ' à ' + fmt(HOURS[nxt][0]),
            'Closed — opens ' + when + ' at ' + fmt(HOURS[nxt][0]));
  }
  el.innerHTML = '<span class="dot ' + (open ? 'on' : 'off') + '"></span><b>' + msg + '</b>';
  document.querySelectorAll('#hourstable tr').forEach(function(tr){
    tr.classList.toggle('today', tr.getAttribute('data-day') === String(day));
  });
}

/* ═══════ 7 · SOUMISSION PAR COURRIEL ══════════════ */
var qf = document.getElementById('quoteform');
if(qf) qf.addEventListener('submit', function(e){
  e.preventDefault();
  var g = function(id){ return (document.getElementById(id).value || '').trim(); };
  var lines = [
    t('Nom', 'Name') + ' : ' + g('q-name'),
    t('Coordonnées', 'Contact') + ' : ' + g('q-contact'),
    t('Pièce', 'Piece') + ' : ' + g('q-piece'),
    '',
    g('q-msg')
  ];
  if(tray.length){
    lines.push('', t('Échantillons réservés', 'Swatches reserved') + ' : ' +
      tray.map(function(k){ var s = trayRecord(k); return s ? s.n + ' (' + s.h + ') — ' + t(s.d[0], s.d[1]) : ''; }).join(' · '));
  }
  lines.push('', t('(Trois photos jointes : la pièce, l’usure, une main pour l’échelle.)',
                   '(Three photos attached: the piece, the wear, a hand for scale.)'));
  var subject = t('Demande de soumission — ', 'Quote request — ') + (g('q-piece') || t('rembourrage', 'upholstery'));
  window.location.href = 'mailto:?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
});

/* ═══════ 8 · RÉVÉLATION AU DÉFILEMENT ═════════════ */
var MOTION = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── L'enseigne se parcourt au défilement ──────────────────
   Une séquence d'images plutôt qu'une vidéo : la lecture d'une
   vidéo dépend du décodage, des politiques de lecture et de la
   granularité des recherches, dont rien n'est garanti. Trente
   images préchargées se dessinent instantanément, partout.
   L'image de base reste visible tant que la toile n'est pas prête,
   et sous mouvement réduit elle reste seule. */
(function(){
  var stage = document.querySelector('.hero-stage');
  var cv    = document.querySelector('.hero-canvas');
  var base  = document.querySelector('.hero-base');
  if(!stage || !cv || !base) return;

  var N = 30, PAD = 2;
  var frames = [], loaded = 0, ready = false;
  var idx = -1, target = 0, shown = 0, raf = 0;

  function src(i){ return 'assets/seq/f_' + String(i + 1).padStart(PAD, '0') + '.jpg'; }

  var ctx = cv.getContext('2d', { alpha: false });
  function size(){
    var r = cv.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width  = Math.max(1, Math.round(r.width  * dpr));
    cv.height = Math.max(1, Math.round(r.height * dpr));
    draw(idx < 0 ? 0 : idx, true);
  }

  /* dessin « cover », aligné sur object-position 50% 45% */
  function draw(i, force){
    if(!ready && !force) return;
    var img = frames[i];
    if(!img || !img.complete || !img.naturalWidth) return;
    if(i === idx && !force) return;
    idx = i;
    var cw = cv.width, ch = cv.height;
    var s = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);
    var w = img.naturalWidth * s, h = img.naturalHeight * s;
    ctx.drawImage(img, (cw - w) / 2, (ch - h) * 0.45, w, h);
  }

  function progress(){
    var top = stage.offsetTop;
    var run = stage.offsetHeight - window.innerHeight;   /* la course utile */
    if(run <= 0) return 0;
    var y = (window.scrollY || window.pageYOffset) - top;
    return Math.max(0, Math.min(1, y / run));
  }

  /* Amorti : le rendu court après la cible au lieu d'y sauter,
     ce qui enlève la saccade d'un cran de molette. */
  function tick(){
    raf = 0;
    var d = target - shown;
    if(Math.abs(d) < 0.0015){ shown = target; }
    else { shown += d * 0.18; raf = requestAnimationFrame(tick); }
    draw(Math.round(shown * (N - 1)));
    var p = shown;
    var fade = p < 0.72 ? 1 : Math.max(0, 1 - (p - 0.72) / 0.24);
    stage.style.setProperty('--typeop', fade.toFixed(3));
    stage.classList.toggle('fading', p >= 0.72);
  }
  function onScroll(){
    target = progress();
    if(!raf) raf = requestAnimationFrame(tick);
    /* filet d'horloge : le rAF est gelé dans un onglet d'arrière-plan */
    if(!onScroll._t){
      onScroll._t = setTimeout(function(){ onScroll._t = 0; if(!raf){ shown = target; tick(); } }, 120);
    }
  }

  if(!MOTION){ return; }   /* mouvement réduit : l'image de base suffit */

  for(var i = 0; i < N; i++){
    (function(i){
      var im = new Image();
      im.decoding = 'async';
      im.onload = function(){
        if(++loaded === N){
          ready = true;
          size();
          cv.classList.add('on');
          onScroll();
        }
      };
      im.onerror = im.onload;
      im.src = src(i);
      frames[i] = im;
    })(i);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', size);
  document.addEventListener('visibilitychange', function(){
    if(document.visibilityState === 'visible'){ shown = target = progress(); tick(); }
  });
})();

/* ── entrées échelonnées ─────────────────────────────────── */
if(MOTION && 'IntersectionObserver' in window){
  var groups = new WeakMap();
  document.querySelectorAll('[data-stagger]').forEach(function(box){
    Array.prototype.slice.call(box.querySelectorAll(':scope > .rise')).forEach(function(el, i){
      groups.set(el, Math.min(i * 70, 420));
    });
  });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting) return;
      var d = groups.get(en.target) || 0;
      en.target.style.setProperty('--i', d + 'ms');
      en.target.classList.add('in');
      io.unobserve(en.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  document.querySelectorAll('.rise').forEach(function(el){ io.observe(el); });

  /* Filet permanent. L'observateur ne se déclenche pas dans un onglet
     d'arrière-plan, et une section restée à opacité zéro est une page
     blanche pour le visiteur : on balaie aussi au défilement. */
  var sweeping = 0;
  function sweep(){
    sweeping = 0;
    var vh = window.innerHeight;
    var left = document.querySelectorAll('.rise:not(.in)');
    for(var i = 0; i < left.length; i++){
      var r = left[i].getBoundingClientRect();
      if(r.top < vh * 1.15 && r.bottom > -vh * 0.5) left[i].classList.add('in');
    }
  }
  function onSweep(){ if(!sweeping) sweeping = setTimeout(sweep, 120); }
  window.addEventListener('scroll', onSweep, { passive: true });
  window.addEventListener('resize', onSweep, { passive: true });
  document.addEventListener('visibilitychange', sweep);
  setTimeout(sweep, 1200);
  setTimeout(sweep, 3000);
} else {
  document.querySelectorAll('.rise').forEach(function(el){ el.classList.add('in'); });
}

/* ── la coupe s'assemble de la structure vers le tissu ───── */
(function(){
  var stage = document.querySelector('.anat-stage');
  if(!stage) return;
  if(!MOTION || !('IntersectionObserver' in window)){ stage.classList.add('built'); return; }
  stage.querySelectorAll('.layer').forEach(function(g){
    var n = parseInt(g.getAttribute('data-layer'), 10) || 1;
    g.style.setProperty('--ld', ((10 - n) * 90) + 'ms');   /* 10 = le cadre, il monte en premier */
  });
  function build(){ stage.classList.add('built'); }
  var ob = new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ build(); ob.disconnect(); } });
  }, { threshold: .18 });
  ob.observe(stage);
  /* filet de sécurité : la coupe ne doit jamais rester invisible,
     même si l'observateur ne se déclenche pas (cadre hors écran, etc.) */
  setTimeout(function(){ if(!stage.classList.contains('built')){ ob.disconnect(); build(); } }, 2500);
})();

/* ── barre condensée + parallaxe de l'enseigne ───────────── */
(function(){
  var img = document.querySelector('.hero-media img');
  var ticking = false, lastScrolled = null;
  function frame(){
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    var scrolled = y > 24;
    if(scrolled !== lastScrolled){
      document.body.classList.toggle('scrolled', scrolled);
      lastScrolled = scrolled;
    }
    if(MOTION && img && y < window.innerHeight * 1.4){
      img.style.transform = 'translate3d(0,' + (y * 0.07).toFixed(1) + 'px,0)';
    }
  }
  function onScroll(){ if(!ticking){ ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  frame();
})();

/* ═══════ 9 · DÉMARRAGE ════════════════════════════ */
/* ── cycle de vie de l'ouverture ──────────────────────────── */
(function(){
  function go(){ document.body.classList.add('ready'); }
  var sp = document.getElementById('splash');
  var skip = document.documentElement.classList.contains('intro-skip');
  if(!sp || skip){
    if(sp) sp.remove();
    requestAnimationFrame(function(){ requestAnimationFrame(go); });
    /* rAF est throttlé dans un onglet d'arrière-plan : sans ce filet,
       l'enseigne resterait invisible au retour d'un visiteur. */
    setTimeout(go, 400);
    return;
  }
  if(location.hash === '#introhold'){ sp.classList.add('run', 'hold'); return; }

  var started = false;
  function start(){
    if(started) return;
    started = true;
    /* La session n'est marquée qu'au moment où l'ouverture est
       réellement jouée : un chargement en arrière-plan ne doit pas
       la consommer sans que personne ne l'ait vue. */
    try { sessionStorage.setItem('operaIntro', '1'); } catch(e){}
    sp.classList.add('run');
    setTimeout(go, 2300);                                  /* l'enseigne démarre juste avant la levée */
    setTimeout(function(){ sp.classList.add('done'); }, 2400);
    setTimeout(function(){ if(sp.parentNode) sp.remove(); }, 3400);
  }

  if(document.visibilityState === 'visible'){
    start();
  } else {
    document.addEventListener('visibilitychange', function onVis(){
      if(document.visibilityState === 'visible'){
        document.removeEventListener('visibilitychange', onVis);
        start();
      }
    });
  }

  setTimeout(function(){                                   /* filet absolu */
    var s = document.getElementById('splash');
    if(s){ s.remove(); document.body.classList.add('ready'); }
  }, 15000);
})();
document.querySelectorAll('#year').forEach(function(e){ e.textContent = montrealNow().getFullYear(); });
try{ var saved = localStorage.getItem('opera-lang'); if(saved === 'en'){ applyLang('en'); } }catch(e){}
buildPieceSelect();
renderFilters();
renderSwatches();
renderWeaves();
renderTray();
calc();
openState();
setInterval(openState, 60000);

var moreBtn = document.getElementById('loadmore');
if(moreBtn) moreBtn.addEventListener('click', function(){ shownCount += PAGE; renderSwatches(); });
})();
