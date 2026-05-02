from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(str("""
        <html>
            <body>
                <h1>Hola Mundo desde Vercel!</h1>
                <p>Tu API Python está funcionando correctamente.</p>
            </body>
        </html>
        """).encode())
        return
