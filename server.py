from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from collections import defaultdict, deque
import argparse

# Initialize message queues
queues = defaultdict(deque)


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        message = post_data.get('message')
        queue_alias = str(post_data.get('queue_alias', '0'))

        if message and len(queues[queue_alias]) < 100:
            queues[queue_alias].append(message)
            self.send_response(200)
        else:
            self.send_response(204)  # No Content
        self.end_headers()

    def do_GET(self):
        queue_alias = self.path.split('/')[-1] if self.path != '/' else '0'
        if queues[queue_alias]:
            message = queues[queue_alias].popleft()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'message': message}).encode())
        else:
            self.send_response(400)
            self.end_headers()

    def do_DELETE(self):
        global queues
        queues = defaultdict(deque)
        self.send_response(200)
        self.end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Message Exchanger Server')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    args = parser.parse_args()

    server_address = ('', args.port)
    httpd = HTTPServer(server_address, MessageHandler)
    print(f"Server running on port {args.port}")
    httpd.serve_forever()
