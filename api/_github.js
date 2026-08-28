/**
 * Persistance par commit GitHub — repris de ghStore.ts (Meggie Perle).
 *
 * Le site est fait de fichiers statiques : « enregistrer » doit donc
 * devenir un commit. Le commit déclenche l'action qui relance build.py
 * et republie. Il faut un GITHUB_TOKEN à portée restreinte (Contents:
 * read/write sur ce dépôt seulement).
 */
const GH = {
  token:  (process.env.GITHUB_TOKEN  || '').trim(),
  repo:   (process.env.GITHUB_REPO   || 'maisoninfuze-star/operaupholstering').trim(),
  branch: (process.env.GITHUB_BRANCH || 'main').trim(),
};

export const githubConfigured = () => Boolean(GH.token);

const headers = () => ({
  Authorization: `Bearer ${GH.token}`,
  Accept: 'application/vnd.github+json',
  'X-GitHub-Api-Version': '2022-11-28',
  'Content-Type': 'application/json',
});

const b64 = (str) => Buffer.from(str, 'utf8').toString('base64');

async function readSha(path) {
  const r = await fetch(
    `https://api.github.com/repos/${GH.repo}/contents/${encodeURI(path)}?ref=${GH.branch}`,
    { headers: headers(), cache: 'no-store' });
  if (r.status === 404) return undefined;
  if (!r.ok) throw new Error(`lecture GitHub ${r.status}`);
  return (await r.json()).sha;
}

/** Écrit un fichier (texte ou base64 déjà encodé) et rend le sha du commit. */
export async function commitFile(path, contentB64, message) {
  for (let attempt = 1; ; attempt++) {
    const sha = await readSha(path);
    const r = await fetch(
      `https://api.github.com/repos/${GH.repo}/contents/${encodeURI(path)}`,
      { method: 'PUT', headers: headers(),
        body: JSON.stringify({ message, content: contentB64, branch: GH.branch,
                               ...(sha ? { sha } : {}) }) });
    if (r.ok) return;
    /* 409 : quelqu'un a écrit entre-temps — on relit le sha et on réessaie */
    if (r.status === 409 && attempt < 3) continue;
    const detail = await r.text().catch(() => '');
    throw new Error(`écriture GitHub ${r.status} ${detail.slice(0, 160)}`);
  }
}

export const jsonToB64 = (obj) => b64(JSON.stringify(obj, null, 2));
