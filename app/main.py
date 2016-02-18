# -*- coding: utf-8 -*-

import bottle
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#717171',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': _get_trump_taunt()
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data



    print data['snakes']



    response = {
        'move': 'north',
    }
    if data['turn'] % 4 == 0:
        response['taunt'] = _get_trump_taunt()

    return response


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': _get_trump_taunt()
    }


def _get_trump_taunt():
    quotes = [
        'Sometimes by losing a battle you find a new way to win the war.',
        'I\'m the No. 1 snake in New York, I\'m the biggest in Atlantic City, and maybe we\'ll keep it that way.',
        'Make battlesnake great again!',
        'We need a great snake',
        'I am the least racist person',
        'My net worth is many, many, many times Mitt Romney',
        'I promise I will never be in a snake competition',
        'BATTLESNAKE HAS ENOUGH PROBLEMS!',
        'Did you notice that snake was crying through half of the speech and I didn’t get angry?',
        'There\'s nobody bigger or better at snakes than I am',
        'I will be the greatest snake that God ever created.',
        'I will build a great snake – and nobody builds snakes better than me, believe me —and I\'ll build them very inexpensively.',
        'I think the only difference between me and the other candidates is that I\'m a snake',
        'I will build you ... one of the great snakes of the world.'
    ]
    return random.choice(quotes)


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080)
