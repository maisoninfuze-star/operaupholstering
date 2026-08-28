/**
 * DEMANDE D'ESTIMATION — envoyée directement à l'atelier, photos
 * comprises, via Resend. Le destinataire suit la langue du site et
 * n'est jamais fourni par le client : un formulaire qui accepte un
 * destinataire arbitraire est un relais à pourriel.
 *
 * Sans RESEND_API_KEY, la fonction répond 503 et la page bascule sur
 * l'application de courriel du visiteur — rien ne se perd, seules les
 * photos redeviennent manuelles.
 */
const TO = {
  fr: (process.env.ESTIMATE_TO_FR || 'contact@operarembourrage.ca').trim(),
  en: (process.env.ESTIMATE_TO_EN || 'contact@operaupholstering.ca').trim(),
};
const FROM = (process.env.EMAIL_FROM || 'Opera Upholstering <onboarding@resend.dev>').trim();
const KEY  = () => (process.env.RESEND_API_KEY || '').trim();

/* fenêtre glissante en mémoire : 5 demandes par minute et par adresse */
const hits = new Map();
function tooMany(ip) {
  const now = Date.now(), list = (hits.get(ip) || []).filter(t => now - t < 60_000);
  list.push(now); hits.set(ip, list);
  return list.length > 5;
}

const esc = (s) => String(s || '').replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]));

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'méthode' });
  if (!KEY()) {
    return res.status(503).json({ error: "L'envoi direct n'est pas configuré (RESEND_API_KEY)." });
  }
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'local';
  if (tooMany(ip)) return res.status(429).json({ error: 'Trop de demandes. Attendez une minute.' });

  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (b.website) return res.status(200).json({ ok: true });           /* pot de miel : on sourit, on jette */
  if (!String(b.message || b.piece || '').trim() && !(b.photos || []).length) {
    return res.status(400).json({ error: 'La demande est vide.' });
  }

  const photos = (Array.isArray(b.photos) ? b.photos : []).slice(0, 6)
    .filter(p => p && typeof p.data === 'string' && p.data.length < 2_000_000)
    .map((p, i) => ({
      filename: String(p.name || `photo-${i + 1}.jpg`).replace(/[^\w.-]/g, '_').slice(0, 60),
      content: p.data,
    }));

  const lang = b.lang === 'en' ? 'en' : 'fr';
  const L = lang === 'en'
    ? { sub: 'Quote request', name: 'Name', contact: 'Contact', piece: 'Piece',
        msg: 'Description', sw: 'Swatches reserved', ph: 'photo(s) attached' }
    : { sub: 'Demande de soumission', name: 'Nom', contact: 'Coordonnées', piece: 'Pièce',
        msg: 'Description', sw: 'Échantillons réservés', ph: 'photo(s) jointe(s)' };

  const rows = [
    [L.name, b.name], [L.contact, b.contact], [L.piece, b.piece], [L.msg, b.message],
    [L.sw, (b.swatches || []).join(' · ')],
  ].filter(r => String(r[1] || '').trim());

  const html =
    `<div style="font-family:Georgia,serif;max-width:560px">` +
    rows.map(r => `<p style="margin:0 0 10px"><strong style="font-family:Arial,sans-serif;
      font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8A6A2A">${esc(r[0])}</strong><br>` +
      `${esc(r[1]).replace(/\n/g, '<br>')}</p>`).join('') +
    (photos.length ? `<p style="color:#6B6E74">${photos.length} ${L.ph}</p>` : '') +
    `</div>`;

  const contact = String(b.contact || '').trim();
  const payload = {
    from: FROM,
    to: [TO[lang]],
    subject: `${L.sub} — ${String(b.piece || '').trim().slice(0, 80) || 'rembourrage'}`,
    html,
    ...(photos.length ? { attachments: photos } : {}),
    ...(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact) ? { reply_to: contact } : {}),
  };

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${KEY()}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    const detail = await r.text().catch(() => '');
    return res.status(502).json({ error: `Envoi refusé (${r.status}) ${detail.slice(0, 140)}` });
  }
  return res.status(200).json({ ok: true });
}
