from http.server import SimpleHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # If the root URL is requested, serve all.html
        if self.path == '/':
            self.path = '/src/all.html'
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), CORSRequestHandler)
    print("Serving on port 8000...")
    server.serve_forever()
