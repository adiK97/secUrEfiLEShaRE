from http.server import HTTPServer, SimpleHTTPRequestHandler

httpd = HTTPServer(('localhost', 4000), SimpleHTTPRequestHandler)
httpd.serve_forever()