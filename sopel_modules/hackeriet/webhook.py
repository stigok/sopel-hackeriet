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

@bottle.get("/webhook")
def show_hook_info():
    return 'Listening for webhook connections!'

#@bottle.post("/webhook")
#def webhook():
#    event = bottle.request.headers.get('X-GitHub-Event') or 'ping'
#
#    try:
#        payload = bottle.request.json
#    except:
#        return bottle.abort(400, 'Something went wrong!')
#
#    if event == 'ping':
#        channels = get_targets(payload['repository']['full_name'])
#        for chan in channels:
#            sopel_instance.msg(chan[0], '[{}] {}: {} (Your webhook is now enabled)'.format(
#                          fmt_repo(payload['repository']['name'], chan),
#                          fmt_name(payload['sender']['login'], chan),
#                          payload['zen']))
#        return '{"channels":' + json.dumps([chan[0] for chan in channels]) + '}'
#
#    payload['event'] = event
#
#    targets = get_targets(payload['repository']['full_name'])
#
#    for row in targets:
#        messages = get_formatted_response(payload, row)
#       # Write the formatted message(s) to the channel
#        for message in messages:
#            sopel_instance.msg(row[0], message)
#
#    return '{"channels":' + json.dumps([chan[0] for chan in targets]) + '}'
