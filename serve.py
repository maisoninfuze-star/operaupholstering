#!/usr/bin/env python3
"""Serveur local qui se comporte comme Vercel.

`python3 -m http.server` ne connaît que les chemins exacts : /admin
renvoie 404 alors que /admin.html fonctionne. En ligne, l'option
cleanUrls de Vercel accepte les deux. Ce script fait pareil ici, pour
que l'adresse tapée en local soit celle qui marchera en ligne.

    python3 serve.py            (port 8791)
    python3 serve.py 9000

Il ne sait toujours pas exécuter api/*.js — pour essayer la connexion
et la publication, il faut `vercel dev`.
"""
import sys, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8791


class CleanUrls(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        full = super().translate_path(path)
        if os.path.isdir(full) or os.path.exists(full):
            return full
        # /admin -> /admin.html, comme cleanUrls
        if not os.path.splitext(full)[1] and os.path.exists(full + '.html'):
            return full + '.html'
        return full

    def do_POST(self):
        if self.path.startswith('/api/'):
            self.send_response(501)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(
                b'{"error":"Ce serveur local ne peut pas executer les fonctions. '
                b'Utilisez vercel dev, ou le bouton Enregistrer le dossier."}')
            return
        self.send_error(405)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        if '404' in (fmt % args):
            sys.stderr.write('  404  %s\n' % (fmt % args))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f'  http://localhost:{PORT}/            le site')
    print(f'  http://localhost:{PORT}/admin       l\'éditeur')
    print('  (Ctrl-C pour arrêter)')
    ThreadingHTTPServer(('', PORT), CleanUrls).serve_forever()
