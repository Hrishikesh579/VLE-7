from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import time

START_TIME = time.time()
REQUEST_COUNT = 0

class AppHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global REQUEST_COUNT
        REQUEST_COUNT += 1

        if self.path == "/metrics":
            uptime = time.time() - START_TIME

            metrics = (
                "# HELP app_requests_total Total HTTP requests\n"
                "# TYPE app_requests_total counter\n"
                f"app_requests_total {REQUEST_COUNT}\n"
                "# HELP app_uptime_seconds Application uptime in seconds\n"
                "# TYPE app_uptime_seconds gauge\n"
                f"app_uptime_seconds {uptime:.2f}\n"
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.end_headers()
            self.wfile.write(metrics.encode())

        elif self.path == "/" or self.path == "/index.html":
            content = Path("/app/index.html").read_bytes()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content)

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    print("Starting VLE 7 application on port 8080")
    HTTPServer(("0.0.0.0", 8080), AppHandler).serve_forever()