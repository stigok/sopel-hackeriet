# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module
from sopel.config.types import StaticSection, ValidatedAttribute
from .webhook import setup_webhook, shutdown_webhook

from sopel import tools

class HackerietSection(StaticSection):
    secret    = ValidatedAttribute('secret', default=None)
    webhook   = ValidatedAttribute('webhook', bool, default=False)
    webhook_host = ValidatedAttribute('webhook_host', default='0.0.0.0')
    webhook_port = ValidatedAttribute('webhook_port', default='3334')

def configure(config):
    config.define_section('hackeriet', HackerietSection, validate=False)
    config.hackeriet.configure_setting('secret', 'Hackeriet API Client Secret')
    config.hackeriet.configure_setting('webhook', 'Enable webhook listener functionality')
    if config.hackeriet.webhook:
        config.hackeriet.configure_setting('webhook_host', 'Listen IP for incoming webhooks (0.0.0.0 for all IPs)')
        config.hackeriet.configure_setting('webhook_port', 'Listen port for incoming webhooks')

def setup(sopel):
    sopel.config.define_section('hackeriet', HackerietSection)
    if sopel.config.hackeriet.webhook:
        setup_webhook(sopel)

def shutdown(sopel):
    shutdown_webhook(sopel)

@module.commands('hackeriet')
def hello_world(bot, trigger):
    bot.say('Hackeriet is a community operated hackerspace in Oslo where people tinker with software, networks, art, hardware and to learn from each other. https://hackeriet.no')
