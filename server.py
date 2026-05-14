from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.parse
import os
import detector

class PhishingHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                url = data.get('url', '')
                
                if not url:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "URL is required"}).encode('utf-8'))
                    return
                
                # Call the detector logic
                result = detector.analyze_url(url)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    # Change directory to the static files so SimpleHTTPRequestHandler serves them
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'main', 'resources', 'static')
    os.chdir(static_dir)
    
    port = 8090
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, PhishingHandler)
    print(f"Starting Python server on http://127.0.0.1:{port}...")
    httpd.serve_forever()
