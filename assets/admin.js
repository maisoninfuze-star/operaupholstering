/* ═══════════════════════════════════════════════════════════
   Éditeur de contenu · Opera Upholstering
   Charge data/site.json, laisse tout modifier, et rend un
   fichier prêt à remettre dans le dossier. Aucun mot de passe,
   aucune clé, rien n'est envoyé : la page ne fait qu'écrire un
   fichier que vous récupérez.
   ═══════════════════════════════════════════════════════════ */
(function(){
  'use strict';
  var DATA = null, TXT = null, IMGS = null, DIRTY = false;
  var NEWIMG = {};   /* chemin -> Uint8Array du fichier redimensionné */
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


  /* ── Textes des pages ─────────────────────────────────── */
  var SECTION_NOMS = {
    atelier:'Accueil · l’atelier', bibliotheque:'Les tissus',
    performance:'Les tissus · tenue des étoffes', cannage:'Cannage',
    procede:'Savoir-faire · comment ça marche', prix:'Savoir-faire · le prix',
    questions:'Savoir-faire · questions', soumission:'Contact et soumission'
  };
  function paneTextes(){
    var p = el('div', 'adm-pane');
    p.appendChild(el('h2', null, 'Tous les textes des pages'));
    p.appendChild(el('p', 'adm-note', 'Chaque phrase du site, en français et en anglais. Les titres, les paragraphes, les questions, les cellules des tableaux. Ce qui contient des liens ou de la mise en forme n’apparaît pas ici et se modifie dans content.json.'));

    var pick = el('div', 'adm-seltabs');
    var host = el('div');
    Object.keys(TXT).forEach(function(key, i){
      var n = TXT[key].length;
      if(!n) return;
      var btn = el('button', 'adm-seltab', (SECTION_NOMS[key] || key) + ' · ' + n);
      if(i === 0) btn.classList.add('on');
      btn.addEventListener('click', function(){
        [].forEach.call(pick.children, function(c){ c.classList.remove('on'); });
        btn.classList.add('on'); draw(key);
      });
      pick.appendChild(btn);
    });
    function draw(key){
      host.innerHTML = '';
      TXT[key].forEach(function(t, i){
        var box = el('div', 'adm-card');
        box.appendChild(el('span', 'adm-idx', (SECTION_NOMS[key] || key) + ' · ' + (i + 1)));
        var isLong = (t.fr || '').length > 90;
        box.appendChild(pair(t, 'fr', 'en', 'Texte', {long:isLong, rows:isLong ? 3 : 2}));
        host.appendChild(box);
      });
    }
    p.appendChild(pick); p.appendChild(host);
    draw(Object.keys(TXT).filter(function(k){ return TXT[k].length; })[0]);
    return p;
  }

  /* ── Photographies ────────────────────────────────────── */
  function paneImages(){
    var p = el('div', 'adm-pane');
    p.appendChild(el('h2', null, 'Les photographies'));
    p.appendChild(el('p', 'adm-note', 'Choisissez une image : elle est recadrée et redimensionnée aux mesures exactes de son emplacement, puis rendue dans le dossier sous le même nom. L’originale n’est pas touchée tant que vous ne la remplacez pas.'));

    IMGS.forEach(function(im){
      var box = el('div', 'adm-imgrow');
      var thumb = el('img', 'adm-thumb');
      thumb.src = NEWIMG[im.chemin] ? NEWIMG[im.chemin].url : (im.chemin + '?t=' + Date.now());
      thumb.alt = '';
      box.appendChild(thumb);

      var meta = el('div', 'adm-imgmeta');
      meta.appendChild(el('span', 'adm-imgrole', im.role));
      meta.appendChild(el('code', null, im.chemin));
      meta.appendChild(el('span', 'adm-dim', im.largeur + ' × ' + im.hauteur + ' · ' + im.poids_ko + ' ko'));
      var status = el('span', 'adm-imgstate');
      if(NEWIMG[im.chemin]) { status.textContent = 'Remplacée'; status.classList.add('ok'); }
      meta.appendChild(status);
      box.appendChild(meta);

      var lab = el('label', 'adm-btn ghost adm-choose', 'Choisir une image');
      var inp = el('input'); inp.type = 'file'; inp.accept = 'image/*'; inp.hidden = true;
      inp.addEventListener('change', function(){
        var f = inp.files && inp.files[0];
        if(!f) return;
        status.textContent = 'Traitement…'; status.className = 'adm-imgstate';
        resize(f, im.largeur, im.hauteur, im.chemin, function(rec){
          NEWIMG[im.chemin] = rec;
          thumb.src = rec.url;
          status.textContent = 'Remplacée — ' + Math.round(rec.bytes.length / 1024) + ' ko';
          status.className = 'adm-imgstate ok';
          touch();
        });
      });
      lab.appendChild(inp);
      box.appendChild(lab);
      p.appendChild(box);
    });
    return p;
  }

  /* Recadre au centre puis redimensionne aux mesures de l'emplacement. */
  function resize(file, w, h, path, done){
    var img = new Image();
    img.onload = function(){
      var cv = document.createElement('canvas');
      cv.width = w; cv.height = h;
      var ctx = cv.getContext('2d');
      ctx.fillStyle = '#EEEBE2'; ctx.fillRect(0, 0, w, h);
      var s = Math.max(w / img.naturalWidth, h / img.naturalHeight);
      var dw = img.naturalWidth * s, dh = img.naturalHeight * s;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(img, (w - dw) / 2, (h - dh) / 2, dw, dh);
      var png = /\.png$/i.test(path);
      cv.toBlob(function(blob){
        blob.arrayBuffer().then(function(buf){
          done({ bytes: new Uint8Array(buf), url: URL.createObjectURL(blob) });
        });
      }, png ? 'image/png' : 'image/jpeg', png ? undefined : 0.82);
    };
    img.onerror = function(){ alert('Fichier image illisible.'); };
    img.src = URL.createObjectURL(file);
  }

  /* ── Enregistrer ──────────────────────────────────────── */
  function bytes(str){ return new TextEncoder().encode(str); }

  function save(){
    var files = [
      { name: 'data/site.json',   data: bytes(JSON.stringify(DATA, null, 2)) },
      { name: 'data/textes.json', data: bytes(JSON.stringify(TXT,  null, 2)) }
    ];
    Object.keys(NEWIMG).forEach(function(path){
      files.push({ name: path, data: NEWIMG[path].bytes });
    });
    var blob = window.makeZip(files);
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'opera-contenu.zip';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1500);
    var nImg = Object.keys(NEWIMG).length;
    $('#state').textContent = 'Dossier enregistré — 2 fichiers de texte'
      + (nImg ? ' et ' + nImg + ' image' + (nImg > 1 ? 's' : '') : '');
    $('#state').className = 'adm-state ok';
    DIRTY = false;
  }

  function copy(){
    var txt = JSON.stringify(DATA, null, 2);
    function done(){
      $('#state').textContent = 'Réglages copiés — à coller dans site/data/site.json';
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


  /* ── Publier en ligne ─────────────────────────────────────
     Passe par /api/save, qui vérifie le cookie signé puis commit
     dans le dépôt ; l'action GitHub relance build.py. Si les
     fonctions ne répondent pas (site servi en local, ou secrets non
     réglés), le bouton le dit et le .zip reste la voie de secours. */
  function b64(u8){
    var s = '', C = 0x8000;
    for(var i = 0; i < u8.length; i += C){
      s += String.fromCharCode.apply(null, u8.subarray(i, i + C));
    }
    return btoa(s);
  }

  function setBusy(on, msg){
    $('#publish').disabled = on;
    $('#save').disabled = on;
    if(msg){ $('#state').textContent = msg; $('#state').className = 'adm-state'; }
  }

  function publish(){
    var imgs = {};
    Object.keys(NEWIMG).forEach(function(p){ imgs[p] = b64(NEWIMG[p].bytes); });
    var n = Object.keys(imgs).length;
    setBusy(true, 'Publication…' + (n ? ' (' + n + ' image' + (n > 1 ? 's' : '') + ')' : ''));

    fetch('/api/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ site: DATA, textes: TXT, images: imgs })
    })
    .then(function(r){
      return r.text().then(function(t){
        var j = null; try { j = JSON.parse(t); } catch(e){}
        return { ok: r.ok, status: r.status, j: j, raw: t.slice(0, 200) };
      });
    })
    .then(function(res){
      setBusy(false);
      if(!res.ok){
        var m = errText(res.j) || res.raw || '';
        /* 401 seulement : rouvrir la boîte pour autre chose donnait
           l'impression que le mot de passe avait été refusé. */
        if(res.status === 401 && /session/i.test(m)) return gate(true);
        if(/protected|authenticate|sso/i.test(m)){
          m = 'Ce déploiement est protégé par Vercel. Ouvrez l’adresse de production (sans -git-…).';
        }
        $('#state').textContent = m ? ('Échec : ' + m) : ('Échec de la publication (' + res.status + ').');
        $('#state').className = 'adm-state dirty';
        return;
      }
      NEWIMG = {};
      DIRTY = false;
      $('#state').textContent = 'Publié — le site se reconstruit, comptez une minute.';
      $('#state').className = 'adm-state ok';
    })
    .catch(function(){
      setBusy(false);
      $('#state').textContent = 'Les fonctions ne répondent pas — utilisez « Enregistrer le dossier ».';
      $('#state').className = 'adm-state dirty';
    });
  }

  /* Écran de mot de passe. Affiché quand /api/save répond 401. */
  function gate(expired){
    var box = $('#gate');
    box.hidden = false;
    $('#gatemsg').textContent = expired ? 'Session expirée. Entrez le mot de passe.' : '';
    $('#pass').focus();
  }
  /* Un message d'erreur peut arriver de nous ({error:"…"}) ou d'un
     intermédiaire — Vercel renvoie {error:{message:"…"}} sur les
     déploiements de préproduction. On aplatit les deux. */
  function errText(j){
    if(!j) return '';
    var e = j.error;
    if(typeof e === 'string') return e;
    if(e && typeof e.message === 'string') return e.message;
    return '';
  }

  function signIn(){
    var pw = $('#pass').value;
    if(!pw) return;
    $('#gatemsg').textContent = 'Vérification…';

    /* Sans cela, une requête qui n'aboutit jamais laisse « Vérification… »
       à l'écran indéfiniment. */
    var done = false;
    var timer = setTimeout(function(){
      if(done) return;
      done = true;
      $('#gatemsg').textContent = 'Pas de réponse. Vérifiez que vous êtes bien sur l’adresse de production.';
    }, 12000);

    fetch('/api/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ passcode: pw })
    })
    .then(function(r){
      return r.text().then(function(t){
        var j = null;
        try { j = JSON.parse(t); } catch(e){}
        return { ok: r.ok, status: r.status, j: j, raw: t };
      });
    })
    .then(function(res){
      if(done) return; done = true; clearTimeout(timer);
      if(res.ok){
        $('#gatemsg').textContent = '';        /* sinon « Vérification… » reste collé */
        $('#gate').hidden = true;
        $('#pass').value = '';
        $('#state').textContent = 'Connecté.';   /* on distingue « mot de passe refusé » de « publication échouée » */
        $('#state').className = 'adm-state ok';
        publish();
        return;
      }
      var msg = errText(res.j);
      /* La protection de déploiement de Vercel intercepte avant nos
         fonctions : le mot de passe n'y est pour rien, l'adresse si. */
      if(/protected|authenticate|sso/i.test(msg + res.raw)){
        msg = 'Ce déploiement est protégé par Vercel. Ouvrez l’adresse de production (sans -git-…) pour vous connecter.';
      } else if(!msg){
        msg = 'Refusé (' + res.status + ').';
      }
      $('#gatemsg').textContent = msg;
    })
    .catch(function(){
      if(done) return; done = true; clearTimeout(timer);
      $('#gatemsg').textContent = 'Les fonctions ne répondent pas.';
    });
  }

  /* ── Démarrage ────────────────────────────────────────── */
  var TABS = [
    ['Réglages', paneReglages],
    ['Enseigne', paneEnseigne],
    ['Services', paneServices],
    ['Textes', paneTextes],
    ['Photographies', paneImages]
  ];

  /* Les adresses de préproduction (-git-…) passent par la protection
     Vercel : aucune connexion n'y aboutit, quel que soit le mot de
     passe. Plutôt que de le signaler et laisser essayer, on renvoie
     directement vers la production. */
  var PROD = 'https://operaupholstering.vercel.app';
  function isPreview(h){
    return /-git-/.test(h) || /^operaupholstering-[a-z0-9]{6,}/.test(h);
  }
  if(isPreview(location.hostname)){
    location.replace(PROD + location.pathname + location.search);
  }

  function boot(d, t, i){
    DATA = d; TXT = t; IMGS = i;
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
    var pub = $('#publish');
    if(pub) pub.addEventListener('click', function(){
      /* on tente directement : si la session manque, /api/save répond 401 */
      publish();
    });
    var sb = $('#signin');
    if(sb){
      sb.addEventListener('click', signIn);
      $('#pass').addEventListener('keydown', function(e){ if(e.key === 'Enter') signIn(); });
      $('#gatecancel').addEventListener('click', function(){ $('#gate').hidden = true; });
    }
    $('#copy').addEventListener('click', copy);
    window.addEventListener('beforeunload', function(e){
      if(DIRTY){ e.preventDefault(); e.returnValue = ''; }
    });
  }

  function get(u){
    return fetch(u + '?t=' + Date.now()).then(function(r){
      if(!r.ok) throw new Error(u + ' — ' + r.status);
      return r.json();
    });
  }
  Promise.all([get('data/site.json'), get('data/textes.json'), get('data/images.json')])
    .then(function(a){ boot(a[0], a[1], a[2]); })
    .catch(function(err){
      $('#pane').innerHTML =
        '<p class="adm-note">Impossible de lire les fichiers de contenu (' +
        String(err.message || err) + '). Cette page doit être ouverte à travers un ' +
        'serveur — <code>python3 -m http.server</code> depuis le dossier ' +
        '<code>site/</code> — et non par un double-clic sur le fichier.</p>';
    });
})();
