#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os, sys, yaml

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        bits = urlparse(self.path)
        params = parse_qs(bits.query)

        if bits.path == '/chime':
            self.do_chime(params)
        else:
            self.send_response(404)
            self.end_headers()

    def do_chime(self, params):
        type_list = params.get('type', [])
        type = type_list[0] if type_list else None
        if type is None:
            self.send_response(400)
            self.end_headers()
            return

        chime = self.server.chimes.get(type)
        if chime is None:
            self.send_response(400)
            self.end_headers()
            return

        chime.play()
        self.send_response(200)
        self.end_headers()

def load_chimes(config, root):
    # Doesn't have to use pygame, we just need to return a
    # dictionary of chime objects with a play() method.
    import pygame

    mixer = config.get('mixer', {})
    pygame.mixer.pre_init(
        frequency=mixer.get('frequency', 0),
        size=mixer.get('size', 0),
        channels=mixer.get('channels', 0),
        buffer=mixer.get('buffer', 0)
    )
    pygame.init()

    chime_path = config.get('chime_path', root)
    chimes = {}
    for k, v in config.get('chimes', {}).items():
        chimes[k] = pygame.mixer.Sound(os.path.join(chime_path, v))

    return chimes

def run(config, chimes):
    server_address = ('', config.get('port', 8000))
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.config = config
    httpd.chimes = chimes

    httpd.serve_forever()

def run_with_config_file(config_file):
    with open(config_file, 'r') as s:
        config = yaml.safe_load(s)
        chimes = load_chimes(config, os.path.dirname(config_file))
        run(config, chimes)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run_with_config_file(sys.argv[1])
    else:
        print('Usage: {} <config_file>'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
