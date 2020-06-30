import http.server,
import os 
import json #
BaseHandler = http.server.BaseHTTPRequestHandler

blogs = [] 

class Handler(BaseHandler):
    def _set_headers(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()
    def do_GET(self):
        filename = self.path.split("/")[-1]
        if filename == "" : filename = "index.html"
        if os.access(filename, os.R_OK) and not os.path.isdir(filename):
            ext = filename.split(".")[-1]                       # Klijent zahteva fajl
            mode = "r"
            if ext in ["html","htm"]: content_type = "text/html"
            elif ext in ["txt","js","py","php"]: content_type = "text/plain"
            elif ext in ["css"]: content_type = "text/css"
            elif ext in ["ico","jpg","jpeg","png","gif"]:
                content_type = "image/x-icon"
                mode = "rb"
            content = open(filename, mode).read()
            if mode == "r": content = str.encode(content)
            self._set_headers(content_type)
            self.wfile.write(content)
        else:                                 # Ajax zahtev
            odgovor = {"metod":"GET", "path": self.path, "sadrzaj": ""}
            self._set_headers("text/json")
            self.wfile.write(str.encode(str(odgovor)))
    def do_POST(self):
        putanja = self.path
        metod = self.command
        if putanja == "/dodaj-blog":
            duzina_sadrzaja = int(self.headers['Content-Length'])
            sadrzaj = self.rfile.read(duzina_sadrzaja).decode("utf-8")
            blog = json.loads(sadrzaj)
            blogs.append(blog)
            self._set_headers("text/json")
            self.wfile.write(str.encode(json.dumps(blogs)))
        if putanja == "/view-blogs":
            self._set_headers("text/json")
            self.wfile.write(str.encode(json.dumps(blogs)))
try:
    httpd = http.server.HTTPServer(('',8888), Handler)
    print("Server startovan...port: 8888")
    httpd.serve_forever()
except:
    print("Server stopiran")
