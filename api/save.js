import { verifySession, readCookie, SESSION_COOKIE } from './_auth.js';
import { githubConfigured, commitFile, jsonToB64 } from './_github.js';

/** Seuls ces chemins sont accepté. Le reste du dépôt n'est pas joignable d'ici. */
const TEXT_OK = new Set(['data/site.json', 'data/textes.json']);
const IMG_DIR = /^assets\/(travaux|tissus|cannage)\/[a-z0-9-]+\.(jpg|png)$|^assets\/hero\.jpg$/;

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'méthode' });

  if (!(await verifySession(readCookie(req, SESSION_COOKIE)))) {
    return res.status(401).json({ error: 'Session expirée. Reconnectez-vous.' });
  }
  if (!githubConfigured()) {
    return res.status(503).json({ error: "GITHUB_TOKEN n'est pas réglé sur l'hébergeur." });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const { site, textes, images } = body;
  const done = [];

  try {
    if (site)   { await commitFile('site/data/site.json',   jsonToB64(site),
                    'Contenu : réglages et services'); done.push('data/site.json'); }
    if (textes) { await commitFile('site/data/textes.json', jsonToB64(textes),
                    'Contenu : textes des pages'); done.push('data/textes.json'); }

    for (const [path, b64] of Object.entries(images || {})) {
      if (!IMG_DIR.test(path)) {
        return res.status(400).json({ error: `Chemin d'image refusé : ${path}` });
      }
      await commitFile('site/' + path, b64, `Photographie : ${path.split('/').pop()}`);
      done.push(path);
    }
  } catch (e) {
    return res.status(502).json({ error: String(e.message || e), done });
  }
  return res.status(200).json({ ok: true, done });
}
