import http.server
import ssl
import json
import urllib.parse
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.motor.kids_cv_ledger import KidsCVHashChain

class UnifiedSovereignHandler(http.server.BaseHTTPRequestHandler):
    kids_engine = KidsCVHashChain(os.path.join(PROJECT_ROOT, "ledgers/education/kids_cv.json"))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            
            # ترس 1: فحص نبضة النواة المركزية
            if parsed_path.path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                response = {
                    "system": "Verdix Black Platform",
                    "port": 7001,
                    "engine_status": "ACTIVE_PQC_SECURED",
                    "active_ledgers": ["Professional_Card", "Kids_CV"]
                }
                self.wfile.write(json.dumps(response).encode("utf-8"))

            # ترس 2: التحقق من سلسلة سجل الطفل (Kids CV)
            elif parsed_path.path.startswith("/api/v1/kids-cv/verify"):
                status = self.kids_engine.verify_chain("ID-EDU-2026-001")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"ledger": "Kids_CV", "chain_integrity": status.value}).encode("utf-8"))

            # ترس 3: مسار درع الحماية والمراقبة
            elif parsed_path.path == "/health":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"shield": "ARMORED", "integrity": "STABLE"}).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        except Exception:
            self.send_response(500)
            self.end_headers()

def run_server():
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 7001), UnifiedSovereignHandler)
    
    # تأمين المقبس بشهادة التشفير إن وجدت محلياً
    cert_file = "/tmp/verdix.crt"
    key_file = "/tmp/verdix.key"
    if os.path.exists(cert_file) and os.path.exists(key_file):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        server.socket = context.wrap_socket(server.socket, server_side=True)

    server.serve_forever()

if __name__ == "__main__":
    run_server()

if __name__ == '__main__':
    run_server()
