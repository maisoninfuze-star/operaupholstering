/**
 * SESSION D'ADMINISTRATION — cookie signé, sans base de données.
 *
 * Repris du système de Naseeb, pas de celui de Meggie Perle : là-bas le
 * cookie vaut la chaîne « authenticated », que n'importe qui peut écrire
 * dans son navigateur. Ici le cookie porte une date d'expiration et une
 * signature HMAC de cette date. Sans ADMIN_SESSION_SECRET, aucun cookie
 * valide ne peut être fabriqué.
 *
 * Web Crypto plutôt que node:crypto : le même code tourne sur le runtime
 * Edge, où le module Node n'existe pas.
 */
export const SESSION_COOKIE = 'opera_admin';
const TTL_SECONDS = 60 * 60 * 8;          /* un quart de travail, pas un mois */
const enc = new TextEncoder();

const secret   = () => (process.env.ADMIN_SESSION_SECRET || '').trim();
const passcode = () => (process.env.ADMIN_PASSCODE || '').trim();

/** Le chemin par mot de passe n'existe que si les deux valeurs sont réglées. */
export const authConfigured = () => Boolean(secret() && passcode());

async function key() {
  return crypto.subtle.importKey('raw', enc.encode(secret()),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign', 'verify']);
}
const b64url = (buf) =>
  btoa(String.fromCharCode(...new Uint8Array(buf)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

/** `<expirationEnSecondes>.<hmac>` */
export async function mintSession() {
  const exp = String(Math.floor(Date.now() / 1000) + TTL_SECONDS);
  const sig = await crypto.subtle.sign('HMAC', await key(), enc.encode(exp));
  return { value: `${exp}.${b64url(sig)}`, maxAge: TTL_SECONDS };
}

export async function verifySession(value) {
  if (!value || !secret()) return false;
  const [exp, sig] = String(value).split('.');
  if (!exp || !sig) return false;
  if (Number(exp) * 1000 < Date.now()) return false;   /* périmé d'abord */
  const expected = await crypto.subtle.sign('HMAC', await key(), enc.encode(exp));
  return timingSafeEqual(b64url(expected), sig);
}

/**
 * Comparaison à temps constant. Un `===` s'arrête au premier octet qui
 * diffère, ce qui révèle la longueur du préfixe correct à qui sait
 * chronométrer la réponse.
 */
export function timingSafeEqual(x, y) {
  const a = enc.encode(String(x)), b = enc.encode(String(y));
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) {
    diff |= (a[i] ?? 0) ^ (b[i] ?? 0);
  }
  return diff === 0;
}

export function passcodeMatches(input) {
  const expected = passcode();
  if (!expected) return false;
  return timingSafeEqual(input, expected);
}

export function readCookie(req, name) {
  const raw = req.headers.cookie || '';
  const hit = raw.split(';').map(s => s.trim())
                 .find(s => s.startsWith(name + '='));
  return hit ? decodeURIComponent(hit.slice(name.length + 1)) : undefined;
}

export function cookieHeader(value, maxAge) {
  const bits = [
    `${SESSION_COOKIE}=${encodeURIComponent(value)}`,
    'Path=/', 'HttpOnly', 'SameSite=Lax', `Max-Age=${maxAge}`,
  ];
  if (process.env.VERCEL) bits.push('Secure');
  return bits.join('; ');
}
