# This is necessary to find the main code
import math
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# import numpy

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        print("distance: ", self.distance_to_exit(wrld))
        pass

    # function to tell the distance of the agent to the exit
    def distance_to_exit(self, wrld):
        ex = -1
        ey = -1
        cx = wrld.me(self).x
        cy = wrld.me(self).y
        for x in range(0, wrld.width()):
            for y in range (0, wrld.height()):
                if wrld.exit_at(x, y):
                    ex = x
                    ey = y
        return math.sqrt(pow(ex-cx, 2) + pow(ey-cy, 2))

    # function to tell the distance of the agent to the CLOSEST monster
    def distance_to_monster(self, wrld):
        mx = -1
        my = -1
        cx = wrld.me(self).x
        cy = wrld.me(self).y
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.monsters_at(x, y):
                    mx = x
                    my = y
        return math.sqrt(pow(mx - cx, 2) + pow(my - cy, 2))

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
        return math.sqrt(pow(bx - cx, 2) + pow(by - cy, 2))

    # function to tell whether an agent is next to an exit
    def next_to_exit(self, wrld):
        dist = self.distance_to_exit(wrld)
        if dist != 0 and dist < 2:
            return True
        else:
            return False

    # function to tell whether an agent is next to a monster
    def next_to_monster(self, wrld):
        dist = self.distance_to_monster(wrld)
        if dist != 0 and dist < 2:
            return True
        else:
            return False

    # function to tell whether an agent is next to a wall
    def next_to_wall(self, wrld):
        pass

    # function to tell whether an agent is in a bomb explosion
    def is_in_explosion(self, wrld):
        pass
