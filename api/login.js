import { authConfigured, passcodeMatches, mintSession, cookieHeader } from './_auth.js';

/** Fenêtre glissante en mémoire — suffisante contre le tâtonnement. */
const hits = new Map();
function tooMany(ip) {
  const now = Date.now(), win = 60_000, max = 8;
  const list = (hits.get(ip) || []).filter(t => now - t < win);
  list.push(now); hits.set(ip, list);
  return list.length > max;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'méthode' });
  if (!authConfigured()) {
    return res.status(503).json({
      error: "ADMIN_PASSCODE et ADMIN_SESSION_SECRET ne sont pas réglés sur l'hébergeur." });
  }
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'local';
  if (tooMany(ip)) return res.status(429).json({ error: 'Trop de tentatives. Attendez une minute.' });

  const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (!passcodeMatches(String(body.passcode || ''))) {
    return res.status(401).json({ error: 'Mot de passe incorrect.' });
  }
  const s = await mintSession();
  res.setHeader('Set-Cookie', cookieHeader(s.value, s.maxAge));
  return res.status(200).json({ ok: true });
}
