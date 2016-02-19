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

    for snk in snakes:
        if snk['id'] == SNAKE_ID:
            snake = snk

    # If snake is hungry, priority is food
    # Only ever go for food or go for gold
    gold_priority = True
    if _snake_is_hungry(snake):
        gold_priority = False

    move = _get_best_move(data, snake, gold_priority)

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


def get_safe_directions(data, snake):
    # First element of snake is head
    head = snake['coords'][0]
    # All body part coordinates of snakes, including ours, are dangerous
    dangerous_coords = []
    for snk in data['snakes']:
        for coord in snk['coords']:
            dangerous_coords.append(coord)

    # Add list of walls to dangerous coords
    dangerous_coords += data['walls']
    print dangerous_coords
    # Get board height and board width
    b_height = data['height']
    b_width = data['width']

    is_safe = {
        'east': False,
        'west': False,
        'north': False,
        'south': False
    }
    # List of possible moves
    move_west = [head[0] - 1, head[1]]
    move_east = [head[0] + 1, head[1]]
    move_north = [head[0], head[1] - 1]
    move_south = [head[0], head[1] + 1]

    # Play out possible moves
    if move_west[0] >= 0 and move_west not in dangerous_coords:
        is_safe['west'] = True
    if move_north[1] >= 0 and move_north not in dangerous_coords:
        is_safe['north'] = True
    if move_east[0] <= b_width and move_east not in dangerous_coords:
        is_safe['east'] = True
    if move_south[1] <= b_height and move_south not in dangerous_coords:
        is_safe['south'] = True

    return is_safe


def _get_direction_to_target(data, snake, target_coords, head_position):
    is_safe = get_safe_directions(data, snake)
    move = None
    print is_safe
    if target_coords[0] < head_position[0] and is_safe['west']:
        move = 'west'
    if target_coords[0] > head_position[0] and is_safe['east']:
        move = 'east'
    if target_coords[1] < head_position[1] and is_safe['north']:
        move = 'north'
    if target_coords[1] > head_position[1] and is_safe['south']:
        move = 'south'
    print 'GOING %s' % move
    return move


def _get_best_move(data, snake, gold_priority):
    move = None
    no_gold = False
    # Check if gold is the priority but there isn't gold on the board
    if gold_priority:
        if not data['gold']:
            print 'Gold was priority but there was no gold, going for food'
            no_gold = True

    head_position = snake['coords'][0]
    # Priority is food
    if not gold_priority or no_gold:
        food_coords = data['food']
        # Find closest food
        try:
            if food_coords:
                distance_x = abs(head_position[0] - food_coords[0][0])
                distance_y = abs(head_position[1] - food_coords[0][1])
                # [TOTAL_DISTANCE, COORDS]
                closest = [distance_x + distance_y, food_coords[0]]
                # Don't check the first element since that is set to closest as default
                for coords in food_coords[1:]:
                    food_distance = abs(head_position[0] - coords[0]) + abs(head_position[1] - coords[1])
                    if food_distance < closest[0]:
                        print 'FOUND NEW CLOSEST FOOD'
                        closest = [food_distance, coords]
            else:
                print 'THERE WAS NO FOOD'
                raise Exception
        except Exception as e:
            print e
            # That list of food was was less than 1 food!
            gold_priority = True

        else:
            move = _get_direction_to_target(data, snake, closest[1], head_position)


    # Priority is gold
    if gold_priority and not no_gold:
        print 'GOING FOR GOLD!'
        gold_coord = data['gold'][0]
        move = _get_direction_to_target(data, snake, gold_coord, head_position)
    if not move:
        print 'DIDNT CHOOSE A MOVE, SO CHASING TAIL'
        # Chase tail
        beside_tail = [snake['coords'][-1][0] + 1, snake['coords'][-1][1] + 1]
        move = _get_direction_to_target(data, snake, beside_tail, head_position)


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
