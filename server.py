import http.server
import os
import time

DIR = os.path.dirname(os.path.abspath(__file__))

LIVERELOAD_JS = b'''
<script>
(function() {
  var lastMod = Date.now();
  setInterval(function() {
    fetch('/__check__?t=' + lastMod).then(function(r) {
      if (r.status === 200) return r.text();
    }).then(function(t) {
      if (t && parseInt(t) > lastMod) { lastMod = parseInt(t); location.reload(); }
    });
  }, 1000);
})();
</script>
'''

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith('/__check__'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(int(time.time())).encode())
            return
        path = self.translate_path(self.path)
        if self.path.endswith('.html') and os.path.isfile(path):
            with open(path, 'rb') as f:
                content = f.read()
            content = content.replace(b'</head>', LIVERELOAD_JS + b'</head>')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        super().do_GET()

if __name__ == '__main__':
    print('  Servidor com live reload: http://localhost:8000')
    http.server.HTTPServer(('localhost', 8000), Handler).serve_forever()
