class Board(object):
    SNAKE_ID = '3d2f2b54-6c65-402f-b1ea-75b72d2ccbfb'

    head_coords = []
    all_snake_coords = []
    food_coords = []
    gold_coords = []
    our_snake = None
    wall_coords = []
    b_height = 0
    b_width = 0

    def __init__(self, game_data):
        all_snake_coords = []
        our_snake = None
        for snk in game_data['snakes']:
            if snk['id'] == self.SNAKE_ID:
                our_snake = snk
            # Add all coordinates of the snake's body parts to the list of all snake coordinates
            for coord in snk['coords']:
                all_snake_coords.append(tuple(coord))

        self.our_snake = our_snake
        self.all_snake_coords = all_snake_coords
        self.food_coords = game_data['food']
        self.head_coords = our_snake['coords'][0]
        # Check if this is advanced mode and gold is included
        if 'gold' in game_data:
            self.gold_coords = game_data['gold']

        # Get the wall coordinates form the game_data key, plus all edges will be considered walls
        walls = []
        if 'walls' in game_data:
            for wall_coord in game_data['walls']:
                walls.append(tuple(wall_coord))
        # Board width and board height
        b_width = game_data['width']
        b_height = game_data['height']
        for x in xrange(b_width):
            # Northern x border:
            walls.append((-1, x))
            # Southern x border
            walls.append((b_height, x))
        for y in xrange(b_height):
            # Eastern y border:
            walls.append((y, b_width))
            # Western y border:
            walls.append((y, -1))
        self.wall_coords = walls
        self.b_height = b_height
        self.b_width = b_width

    def get_dangerous_coords(self):
        # All walls [borders of map are considered walls] + any snake body part are dangerous
        return self.wall_coords + self.all_snake_coords

    def get_safe_coords(self):
        all_board_coords = []
        for x in xrange(self.b_width):
            for y in xrange(self.b_height):
                all_board_coords.append((x, y))

        dangerous_coords = self.get_dangerous_coords()

        # Set difference!
        return list(set(all_board_coords) - set(dangerous_coords))

    def get_coords_for_direction(self, direction):
        '''
            params: direction, string of 'east', 'west', 'north', 'south'
        '''
        head = self.head_coords
        coords = None
        if direction == 'north':
            coords = [head[0], head[1] - 1]
        elif direction == 'south':
            coords = [head[0], head[1] + 1]
        elif direction == 'east':
            coords = [head[0] + 1, head[1]]
        elif direction == 'west':
            coords = [head[0] - 1, head[1]]

        return coords

    def get_safe_wander_direction(self):
        safe_coords = self.get_safe_coords()
        directions = [
            'north',
            'east',
            'west',
            'south'
        ]
        move = 'north'
        for direction in directions:
            coords_for_move = self.get_coords_for_direction(direction)
            if coords_for_move in safe_coords:
                move = direction

        print 'Get safe wander direction. Returning %s' % move
        return move

    def get_target_direction(self, target):
        move = None
        head_coords = self.head_coords
        safe_coords = self.get_safe_coords()
        # target is north
        if head_coords[1] > target[1]:
            if self.get_coords_for_direction('north') in safe_coords:
                move = 'north'
        # target is south
        if head_coords[1] < target[1]:
            if self.get_coords_for_direction('south') in safe_coords:
                move = 'south'
        # target is east
        if head_coords[0] < target[0]:
            if self.get_coords_for_direction('east') in safe_coords:
                move = 'east'
        # target is west
        if head_coords[0] > target[0]:
            if self.get_coords_for_direction('west') in safe_coords:
                move = 'west'

        print 'Get target direction. Returning %s' % move
        return move

    def get_coords_for_closest_food(self):
        if not self.food_coords:
            return None

        closest = {
            'distance': self.b_width + self.b_height + 1,
            'coords': None
        }

        for coords in self.food_coords:
            food_distance = abs(self.head_coords[0] - coords[0]) + abs(self.head_coords[1] - coords[1])
            if food_distance < closest['distance']:
                closest['distance'] = food_distance
                closest['coords'] = coords

        print 'Get coords for closest food. Returning %s' % closest[coords]
        return closest['coords']

    def get_coords_for_gold(self):
        print 'Get coords for gold. Returning %s' % self.gold_coords
        return self.gold_coords
