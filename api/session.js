/**
 * La page d'édition demande le mot de passe À L'ENTRÉE : elle appelle
 * ce point avant d'afficher quoi que ce soit. Le cookie est vérifié
 * ici, côté serveur — un « déverrouillage » purement client se
 * contournerait dans la console.
 */
import { verifySession, readCookie, SESSION_COOKIE, authConfigured } from './_auth.js';

export default async function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'méthode' });
  if (!authConfigured()) {
    return res.status(503).json({ error: "ADMIN_PASSCODE et ADMIN_SESSION_SECRET ne sont pas réglés." });
  }
  const ok = await verifySession(readCookie(req, SESSION_COOKIE));
  return res.status(200).json({ authed: ok });
}
