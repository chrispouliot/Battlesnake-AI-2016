# -*- coding: utf-8 -*-

import bottle
import random
SNAKE_ID = '3d2f2b54-6c65-402f-b1ea-75b72d2ccbfb'


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
    snakes = data['snakes']
    snake = None

    for snake in snakes:
        if snake['id'] == SNAKE_ID:
            snake = snake

    # If snake is hungry, priority is food
    # Only ever go for food or go for gold
    gold_priority = True
    if _snake_is_hungry(snake):
        gold_priority = False

    move = _get_best_move(snake, gold_priority)

    response = {
        'move': move,
    }
    if data['turn'] % 4 == 0:
        response['taunt'] = _get_trump_taunt(snakes)

    return response


@bottle.post('/end')
def end():

    return {
        'taunt': _get_trump_taunt()
    }


def _snake_is_hungry(snake):
    return snake['health'] < 30


def _get_best_move(snake, gold_priority):
    return 'north'


def _get_trump_taunt(snakes=None):
    if not snakes:
        return 'I promise I will never be in a snake competition'

    # Dont make fun of ourselves..
    other_snakes = []
    for snake in snakes:
        if not snake['id'] == SNAKE_ID:
            other_snakes.append(snake)

    name = random.choice(other_snakes)['name']

    quotes = [
        'My net worth is many, many times that of %s' % name,
        'I want to see %s\'s birth certificate' % name
    ]

    return random.choice(quotes)


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080)
