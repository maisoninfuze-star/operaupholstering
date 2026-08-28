/* ═══════════════════════════════════════════════════════════
   Éditeur de contenu · Opera Upholstering
   Charge data/site.json, laisse tout modifier, et rend un
   fichier prêt à remettre dans le dossier. Aucun mot de passe,
   aucune clé, rien n'est envoyé : la page ne fait qu'écrire un
   fichier que vous récupérez.
   ═══════════════════════════════════════════════════════════ */
(function(){
  'use strict';
  var DATA = null, DIRTY = false;
  var $ = function(s, r){ return (r||document).querySelector(s); };
  var el = function(tag, cls, txt){
    var n = document.createElement(tag);
    if(cls) n.className = cls;
    if(txt != null) n.textContent = txt;
    return n;
  };
  var JOURS = ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'];

  function touch(){
    DIRTY = true;
    $('#save').removeAttribute('disabled');
    $('#state').textContent = 'Modifications non enregistrées';
    $('#state').className = 'adm-state dirty';
  }

  /* un champ = un libellé + une zone de saisie liée à data[key] */
  function field(obj, key, label, opts){
    opts = opts || {};
    var wrap = el('label', 'adm-field');
    wrap.appendChild(el('span', 'adm-label', label));
    var input = document.createElement(opts.long ? 'textarea' : 'input');
    if(opts.long) input.rows = opts.rows || 3;
    input.value = obj[key] == null ? '' : obj[key];
    input.addEventListener('input', function(){ obj[key] = input.value; touch(); });
    wrap.appendChild(input);
    if(opts.hint) wrap.appendChild(el('span', 'adm-hint', opts.hint));
    return wrap;
  }

  function pair(obj, kfr, ken, label, opts){
    var row = el('div', 'adm-pair');
    row.appendChild(field(obj, kfr, label + ' · français', opts));
    row.appendChild(field(obj, ken, label + ' · english', opts));
    return row;
  }

  /* ── Réglages ─────────────────────────────────────────── */
  function paneReglages(){
    var p = el('div', 'adm-pane'), b = DATA.entreprise;
    p.appendChild(el('h2', null, 'Coordonnées'));
    p.appendChild(el('p', 'adm-note', 'Le téléphone et l’adresse apparaissent dans le bandeau, le pied de page, la page contact et les données que Google lit.'));
    var g = el('div', 'adm-grid');
    g.appendChild(field(b, 'telephone', 'Téléphone affiché'));
    g.appendChild(field(b, 'telephone_lien', 'Téléphone cliquable', {hint:'Format international, sans espaces : +15142704352'}));
    g.appendChild(field(b, 'adresse', 'Adresse'));
    g.appendChild(field(b, 'ville', 'Ville et code postal'));
    g.appendChild(field(b, 'ville_courte', 'Ville (bandeau)'));
    g.appendChild(field(b, 'fondation', 'Année de fondation'));
    p.appendChild(g);

    p.appendChild(el('h2', null, 'Heures d’ouverture'));
    p.appendChild(el('p', 'adm-note', 'Laisser vide pour un jour de fermeture. Le bandeau « ouvert / fermé » et le tableau de la page contact se recalculent tout seuls.'));
    var h = el('div', 'adm-hours');
    for(var d = 0; d < 7; d++){
      (function(d){
        var v = DATA.heures[String(d)];
        var row = el('div', 'adm-hrow');
        row.appendChild(el('span', 'adm-day', JOURS[d]));
        var o = el('input'), c = el('input');
        o.placeholder = 'ouvre'; c.placeholder = 'ferme';
        o.value = v ? v[0] : ''; c.value = v ? v[1] : '';
        function upd(){
          var a = o.value.trim(), z = c.value.trim();
          DATA.heures[String(d)] = (a && z) ? [a, z] : null;
          row.classList.toggle('closed', !(a && z));
          touch();
        }
        o.addEventListener('input', upd); c.addEventListener('input', upd);
        row.classList.toggle('closed', !v);
        row.appendChild(o); row.appendChild(el('span','adm-to','à')); row.appendChild(c);
        h.appendChild(row);
      })(d);
    }
    p.appendChild(h);
    return p;
  }

  /* ── Enseigne ─────────────────────────────────────────── */
  function paneEnseigne(){
    var p = el('div', 'adm-pane'), h = DATA.enseigne;
    p.appendChild(el('h2', null, 'La première page'));
    p.appendChild(el('p', 'adm-note', 'Ce que le visiteur lit avant tout le reste. Le logotype lui-même ne se change pas ici.'));
    p.appendChild(pair(h, 'surtitre_fr', 'surtitre_en', 'Ligne au-dessus du logo'));
    p.appendChild(pair(h, 'sous_titre_fr', 'sous_titre_en', 'Ligne sous le logo'));
    p.appendChild(pair(h, 'accroche_fr', 'accroche_en', 'Phrase en italique'));
    p.appendChild(pair(h, 'texte_fr', 'texte_en', 'Paragraphe', {long:true, rows:4}));
    p.appendChild(pair(h, 'bouton1_fr', 'bouton1_en', 'Premier bouton'));
    p.appendChild(pair(h, 'bouton2_fr', 'bouton2_en', 'Second bouton'));

    p.appendChild(el('h2', null, 'Les quatre chiffres'));
    p.appendChild(el('p', 'adm-note', 'Sous les boutons. Garder des chiffres qu’on peut défendre.'));
    DATA.chiffres.forEach(function(f, i){
      var box = el('div', 'adm-card');
      box.appendChild(el('span', 'adm-idx', 'Chiffre ' + (i + 1)));
      var g = el('div', 'adm-grid3');
      g.appendChild(field(f, 'valeur', 'Valeur'));
      g.appendChild(field(f, 'label_fr', 'Libellé · français'));
      g.appendChild(field(f, 'label_en', 'Libellé · english'));
      box.appendChild(g);
      p.appendChild(box);
    });
    return p;
  }

  /* ── Services ─────────────────────────────────────────── */
  function paneServices(){
    var p = el('div', 'adm-pane');
    p.appendChild(el('h2', null, 'Les travaux de l’atelier'));
    p.appendChild(el('p', 'adm-note', 'Chaque carte de la page d’accueil. La mention « sur demande » ne s’affiche que si elle est remplie — laisser vide pour ne rien afficher.'));
    var list = el('div', null); p.appendChild(list);

    function card(sv, i){
      var box = el('div', 'adm-card');
      var head = el('div', 'adm-cardhead');
      head.appendChild(el('span', 'adm-idx', 'Service ' + (i + 1)));
      var del = el('button', 'adm-del', 'Retirer');
      del.addEventListener('click', function(){
        if(!confirm('Retirer « ' + sv.fr.replace(/&amp;/g,'&') + ' » ?')) return;
        DATA.services.splice(DATA.services.indexOf(sv), 1);
        redraw(); touch();
      });
      head.appendChild(del); box.appendChild(head);
      box.appendChild(pair(sv, 'fr', 'en', 'Titre'));
      box.appendChild(pair(sv, 'desc_fr', 'desc_en', 'Description', {long:true}));
      box.appendChild(pair(sv, 'meta_fr', 'meta_en', 'Mention (facultative)'));
      return box;
    }
    function redraw(){
      list.innerHTML = '';
      DATA.services.forEach(function(sv, i){ list.appendChild(card(sv, i)); });
    }
    redraw();

    var add = el('button', 'adm-btn ghost', '＋ Ajouter un service');
    add.addEventListener('click', function(){
      DATA.services.push({fr:'Nouveau service', en:'New service',
        desc_fr:'', desc_en:'', meta_fr:'', meta_en:''});
      redraw(); touch();
    });
    p.appendChild(add);
    return p;
  }

  /* ── Photographies ────────────────────────────────────── */
  function paneImages(){
    var p = el('div', 'adm-pane');
    p.appendChild(el('h2', null, 'Les photographies'));
    p.appendChild(el('p', 'adm-note', 'Les images ne se téléversent pas depuis cette page : elles se remplacent dans le dossier, en gardant exactement le même nom de fichier. Le site les reprend au prochain build.'));
    var rows = [
      ['assets/hero.jpg', 'La grande image de la page d’accueil', '2000 × 1116'],
      ['assets/travaux/', 'Les pièces sorties de l’atelier — un fichier carré par pièce', '1000 × 1000'],
      ['assets/tissus/', 'Les étoffes de la page Les tissus', '1200 de côté'],
      ['assets/cannage/', 'Le travail de cannage', '1200 de côté'],
      ['assets/logo-opera.png', 'Le logotype', 'PNG transparent']
    ];
    var t = el('div', 'adm-files');
    rows.forEach(function(r){
      var row = el('div', 'adm-frow');
      row.appendChild(el('code', null, r[0]));
      row.appendChild(el('span', null, r[1]));
      row.appendChild(el('span', 'adm-dim', r[2]));
      t.appendChild(row);
    });
    p.appendChild(t);
    return p;
  }

  /* ── Enregistrer ──────────────────────────────────────── */
  function output(){ return JSON.stringify(DATA, null, 2); }

  function save(){
    var txt = output();
    var blob = new Blob([txt], {type:'application/json'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'site.json';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
    $('#state').textContent = 'Fichier enregistré — à remettre dans site/data/';
    $('#state').className = 'adm-state ok';
    DIRTY = false;
  }

  function copy(){
    var txt = output();
    function done(){
      $('#state').textContent = 'Copié — à coller dans site/data/site.json';
      $('#state').className = 'adm-state ok';
    }
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(done, fallback);
    } else fallback();
    function fallback(){
      var ta = $('#raw'); ta.hidden = false; ta.value = txt; ta.select();
      $('#state').textContent = 'Copiez le texte ci-dessous';
      $('#state').className = 'adm-state';
    }
  }

  /* ── Démarrage ────────────────────────────────────────── */
  var TABS = [
    ['Réglages', paneReglages],
    ['Enseigne', paneEnseigne],
    ['Services', paneServices],
    ['Photographies', paneImages]
  ];

  function boot(data){
    DATA = data;
    var tabs = $('#tabs'), body = $('#pane');
    TABS.forEach(function(t, i){
      var btn = el('button', 'adm-tab', t[0]);
      if(i === 0) btn.classList.add('on');
      btn.addEventListener('click', function(){
        [].forEach.call(tabs.children, function(c){ c.classList.remove('on'); });
        btn.classList.add('on');
        body.innerHTML = ''; body.appendChild(t[1]());
      });
      tabs.appendChild(btn);
    });
    body.appendChild(TABS[0][1]());
    $('#save').addEventListener('click', save);
    $('#copy').addEventListener('click', copy);
    window.addEventListener('beforeunload', function(e){
      if(DIRTY){ e.preventDefault(); e.returnValue = ''; }
    });
  }

  fetch('data/site.json?t=' + Date.now())
    .then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); })
    .then(boot)
    .catch(function(){
      $('#pane').innerHTML =
        '<p class="adm-note">Impossible de lire <code>data/site.json</code>. ' +
        'Cette page doit être ouverte à travers un serveur — ' +
        '<code>python3 -m http.server</code> depuis le dossier <code>site/</code> — ' +
        'et non par un double-clic sur le fichier.</p>';
    });
})();
