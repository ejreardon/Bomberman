# This is necessary to find the main code
import math
import sys

from bomberman.sensed_world import SensedWorld

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# import numpy

class TestCharacter(CharacterEntity):

    def do(self, wrld):

        # ===============================
        # INITIALIZATION PHASE
        # ===============================
        # Initializes all variables and sets up world for testing

        # The rate at which to change the weights
        learning_rate = 0.2

        # The weight applied to the exit feature
        exit_weight = 3

        # The weight applied to the monster feature
        monster_weight = 4

        # Create copied version of current world to test on
        copied_world = SensedWorld.from_world(wrld)

        # Get the CharacterEntity obj from the copied world
        copied_char = copied_world.me(self)

        # ===============================
        # EXPLORATION PHASE
        # ===============================
        # Randomly make actions and change weights accordingly for set
        # amount of episodes

        # ===============================
        # EXPLOITATION PHASE
        # ===============================
        # Based on the weights taken from the exploration phase,
        # use them to find the best solution and make the move

        # Variable to hold the greatest value found when moving
        max_action_value = 0
        max_action = (1, 0)

        # Loop through all 8 moves using the copied char and decide which one to make
        # Loop through all the dx values
        for dx in range (-1, 2):
            # Loop through all the dy values
            for dy in range (-1, 2):
                print("TODO: CHECK (", dx, dy, ")")

        self.move(max_action[0], max_action[1])

        print("================================================")
        print("exit distance: ", self.distance_to_exit(wrld))
        print("monster distance: ", self.distance_to_monster(wrld))
        print("bomb distance: ", self.distance_to_bomb(wrld))
        print("exit distance: ", self.is_in_explosion(wrld))
        print("next to exit: ", self.next_to_exit(wrld))
        print("next to monster: ", self.next_to_monster(wrld))
        print("next to wall: ", self.next_to_wall(wrld))
        print("in explosion: ", self.is_in_explosion(wrld))
        print("================================================")

        pass

    # function to tell the distance of the agent to the exit
    def distance_to_exit(self, wrld):
        ex, ey = -1, -1
        cx = wrld.me(self).x
        cy = wrld.me(self).y
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.exit_at(x, y):
                    ex = x
                    ey = y
        if ex != -1 and ey != -1:
            dist_x = ex - cx
            dist_y = ey - cy
            return max(dist_x, dist_y)
        else:
            return -1

    # function to tell the distance of the agent to the CLOSEST monster
    def distance_to_monster(self, wrld):
        mx, my = 1000, 1000
        cx = wrld.me(self).x
        cy = wrld.me(self).y
        monsters = []

        # get the list of monster coordinates
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.monsters_at(x, y):
                    monsters.append((x, y))

        # find the maximum coordinate distance
        dist_x, dist_y, max_dist = 1000, 1000, 1000
        for i in range(len(monsters)):
            j = 1
            for coordinate in monsters[i]:
                if j == 1:
                    dist_x = coordinate - cx
                else:
                    dist_y = coordinate - cy
                j += 1
                if dist_x < mx or dist_y < my:
                    if max(dist_x, dist_y) < max(mx, my):
                        mx = dist_x
                        my = dist_y
                        max_dist = max(mx, my)
        if mx != 1000 and my != 1000:
            return max_dist
        else:
            return -1

    # function to tell distance of an agent to a bomb
    def distance_to_bomb(self, wrld):
        bx = -1
        by = -1
        cx = wrld.me(self).x
        cy = wrld.me(self).y
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.bomb_at(x, y):
                    bx = x
                    by = y
        if bx != -1 and by != -1:
            dist_x = bx - cx
            dist_y = by - cy
            return max(dist_x, dist_y)
        else:
            return -1

    # function to tell whether an agent is next to an exit
    def next_to_exit(self, wrld):
        dist = self.distance_to_exit(wrld)
        if dist == 1:
            return True
        else:
            return False

    # function to tell whether an agent is next to a monster
    def next_to_monster(self, wrld):
        dist = self.distance_to_monster(wrld)
        if dist == 1:
            return True
        else:
            return False

    # function to tell whether an agent is next to a wall
    # ToDo: Can Expand on this to return direction or placement of walls
    def next_to_wall(self, wrld):
        cx = wrld.me(self).x
        cy = wrld.me(self).y
        walls = []
        for x in range(cx-1, cx+1):
            for y in range(cy-1, cy+1):
                if 0 <= x < wrld.width() and 0 <= y < wrld.height():
                    if wrld.wall_at(x,y):
                        walls.append((x, y))
        if len(walls) != 0:
            return True
        else:
            return False

    # function to tell whether an agent is in a bomb explosion
    def is_in_explosion(self, wrld):
        cx = wrld.me(self).x
        cy = wrld.me(self).y
        explosions = []
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.explosion_at(x, y):
                    explosions.append((x, y))
        if len(explosions) != 0:
            if (cx, cy) in explosions:
                return True
        else:
            return False