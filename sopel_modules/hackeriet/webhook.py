from __future__ import unicode_literals

from sopel import tools
from sopel.formatting import bold, color
from sopel.tools.time import get_timezone, format_time

from threading import Thread
import bottle
import json
import requests

# Because I'm a horrible person
sopel_instance = None

def setup_webhook(sopel):
    global sopel_instance
    sopel_instance = sopel
    host = sopel.config.hackeriet.webhook_host
    port = sopel.config.hackeriet.webhook_port

    base = StoppableWSGIRefServer(host=host, port=port)
    server = Thread(target=bottle.run, kwargs={'server': base})
    server.setDaemon(True)
    server.start()
    sopel.memory['hackeriet_webhook_server'] = base
    sopel.memory['hackeriet_webhook_thread'] = server

def shutdown_webhook(sopel):
    global sopel_instance
    sopel_instance = None
    if sopel.memory.contains('hackeriet_webhook_server'):
        print('Stopping hackeriet webhook server')
        sopel.memory['hackeriet_webhook_server'].stop()
        sopel.memory['hackeriet_webhook_thread'].join()
        print('Hackeriet webhook shutdown complete')

class StoppableWSGIRefServer(bottle.ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw):
                    pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

@bottle.get("/announce")
def show_hook_info():
    return 'Listening for webhook connections!'

@bottle.post("/announce")
def announce():
    event = bottle.request.headers.get('X-Announce-Event') or 'ping'

    try:
        payload = bottle.request.json
    except:
        return bottle.abort(400, 'Something went wrong!')

    if event = "ding":
        print("Channel: %s, username: %s, IP: %s") % (payload['channel'], payload['username'], payload['ip_address'])
        return dong 
 
    if event == 'ping':
        return 'pong'

    print(bottle.request)
    print(payload)
    return bottle.request
