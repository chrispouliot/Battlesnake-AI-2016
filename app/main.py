# -*- coding: utf-8 -*-

import bottle
import random
from board import Board
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
    return {
        'taunt': _get_trump_taunt()
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    snakes = data['snakes']
    snake = None

    for snk in snakes:
        if snk['id'] == SNAKE_ID:
            snake = snk

    board = Board(data)
    # If snake is hungry, priority is food. If no gold on board, go for food.
    # Only ever go for food or go for gold
    priority = 'gold'
    if _snake_is_hungry(snake) or not board.get_coords_for_gold():
        print 'Priority is food!'
        priority = 'food'
    # If priority is food but there isn't any food on board, get gold. If no gold either, just move
    if not priority == 'gold' and not board.get_coords_for_closest_food():
        if board.get_coords_for_gold():
            priority = 'gold'
        else:
            priority = 'wander'

    move = _get_best_move(board, priority)

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
    return snake['health'] < 25


def _get_direction_to_target(board, target_coords):
    # Get direction to target. Will return None if no safe block forward to target
    move = board.get_target_direction(target_coords)

    # If we haven't chosen a move, it means there were obstacles between us and the target. Wander!
    if not move:
        move = board.get_safe_wander_direction()

    return move


def _get_best_move(board, priority):
    if priority == 'food':
        move = _get_direction_to_target(board, board.get_coords_for_closest_food())
    elif priority == 'gold':
        move = _get_direction_to_target(board, board.get_coords_for_gold())
    else:
        # We wander!
        move = board.get_safe_wander_direction()

    return move


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
        'YOU\'RE FIRED!',
        'There should be a wall here!',
        'MAKE BATTLESNAKE GREAT AGAIN',
        'My net worth is many, many times that of %s\'s' % name,
        'I want to see %s\'s birth certificate' % name,
        'Did anyone notice %s was crying through my speech?' % name,
        'Why is %s playing basketball today' % name,
        'All of the snakes on the board flirted with me',
        'Global warming was invented by the mongooses'
    ]

    return random.choice(quotes)


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080)
