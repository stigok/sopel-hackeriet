# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module

def configure(config):
    pass

def setup(bot):
    pass

def shutdown(bot):
    pass

@module.commands('hackeriet')
def hello_world(bot, trigger):
    bot.say('Hackeriet is a community operated hackerspace in Oslo where people tinker with software, networks, art and hardware, learn from each other. https://hackeriet.no')
