import os
import sys

# !!! IMPORTANTE !!!
# TROQUE "SEU_USUARIO" pelo seu nome de usuario do PythonAnywhere
# Exemplo: se seu site for "joao.pythonanywhere.com", coloque "joao"
USER = "SEU_USUARIO"

# Caminho onde seus arquivos estao no PythonAnywhere
DIR = "/home/{}/EliteStream".format(USER)

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    if path == '/':
        path = '/index.html'

    filepath = os.path.join(DIR, path.lstrip('/'))
    filepath = os.path.normpath(filepath)

    try:
        dentro = os.path.commonpath([DIR, filepath]) == DIR
    except ValueError:
        dentro = False

    if not dentro:
        start_response('403 Forbidden', [('Content-Type', 'text/plain')])
        return [b'Forbidden']

    if os.path.isfile(filepath):
        ext = os.path.splitext(filepath)[1].lower()
        mime = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.json': 'application/json',
            '.txt': 'text/plain',
        }.get(ext, 'application/octet-stream')

        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            start_response('200 OK', [('Content-Type', mime)])
            return [content]
        except Exception as e:
            start_response('500 Error', [('Content-Type', 'text/plain')])
            return [str(e).encode()]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Page not found: ' + filepath.encode()]
