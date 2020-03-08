# This is necessary to find the main code
import math
import sys

sys.path.insert(0, '../bomberman')
from sensed_world import SensedWorld


# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class Features:
    # def __init__(self, CharacterEntity, World):
    #     self.CharacterEntity = CharacterEntity
    #     self.World = World
    
    # function to tell the distance of the agent to the exit
    def distance_to_exit(self, CharacterEntity, World):
        ex, ey = -1, -1
        cx = World.me(CharacterEntity).x
        cy = World.me(CharacterEntity).y
        for x in range(0, World.width()):
            for y in range(0, World.height()):
                if World.exit_at(x, y):
                    ex = x
                    ey = y
        if ex != -1 and ey != -1:
            dist_x = abs(ex - cx)
            dist_y = abs(ey - cy)
            return max(dist_x, dist_y)
        else:
            return -1
    
    # function to tell the distance of the agent to the CLOSEST monster
    def distance_to_monster(self, CharacterEntity, World):
        mx, my = 1000, 1000
        cx = World.me(CharacterEntity).x
        cy = World.me(CharacterEntity).y
        monsters = []
    
        # get the list of monster coordinates
        for x in range(0, World.width()):
            for y in range(0, World.height()):
                if World.monsters_at(x, y):
                    monsters.append((x, y))
    
        # find the maximum coordinate distance
        dist_x, dist_y, max_dist = 1000, 1000, 1000
        for i in range(len(monsters)):
            j = 1
            for coordinate in monsters[i]:
                if j == 1:
                    dist_x = abs(coordinate - cx)
                else:
                    dist_y = abs(coordinate - cy)
                j += 1
                if dist_x < mx or dist_y < my:
                    if max(dist_x, dist_y) < max(mx, my):
                        mx = dist_x
                        my = dist_y
                        max_dist = max(mx, my)
        if mx != 1000 and my != 1000:
            return max_dist
        else:
            return 10000
    
    # function to tell distance of an agent to a bomb
    def distance_to_bomb(self, CharacterEntity, World):
        bx = -1
        by = -1
        cx = World.me(CharacterEntity).x
        cy = World.me(CharacterEntity).y
        for x in range(0, World.width()):
            for y in range(0, World.height()):
                if World.bomb_at(x, y):
                    bx = x
                    by = y
        if bx != -1 and by != -1:
            dist_x = abs(bx - cx)
            dist_y = abs(by - cy)
            return max(dist_x, dist_y)
        else:
            return 10000
    
    # function to tell whether an agent is next to an exit
    def next_to_exit(self, CharacterEntity, World):
        dist = self.distance_to_exit(CharacterEntity, World)
        if dist == 1:
            return True
        else:
            return False
    
    # function to tell whether an agent is next to a monster
    def next_to_monster(self, CharacterEntity, World):
        dist = self.distance_to_monster(CharacterEntity, World)
        if dist == 1:
            return True
        else:
            return False
    
    # function to tell whether an agent is next to a wall
    # ToDo: Can Expand on this to return direction or placement of walls
    def next_to_wall(self, CharacterEntity, World):
        cx = World.me(CharacterEntity).x
        cy = World.me(CharacterEntity).y
        walls = []
        for x in range(cx-1, cx+2):
            for y in range(cy-1, cy+2):
                if 0 <= x < World.width() and 0 <= y < World.height():
                    if World.wall_at(x, y):
                        walls.append((x, y))
        if len(walls) != 0:
            return True
        else:
            return False
    
    # function to tell whether an agent is in a bomb explosion
    def is_in_explosion(self, CharacterEntity, World):
        cx = World.me(CharacterEntity).x
        cy = World.me(CharacterEntity).y
        explosions = []
        for x in range(0, World.width()):
            for y in range(0, World.height()):
                if World.explosion_at(x, y):
                    explosions.append((x, y))
        in_explosion = False
        if len(explosions) != 0:
            for coordinate in explosions:
                if coordinate[0] == cx and coordinate[1] == cy:
                    in_explosion = True
        return in_explosion
