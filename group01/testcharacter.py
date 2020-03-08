# This is necessary to find the main code
import math
import sys

sys.path.insert(0, '../bomberman')
from sensed_world import SensedWorld
from features import Features
f = Features()

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
        exit_weight = 13
        adjacent_exit_weight = 100

        # The weight applied to the monster feature
        monster_weight = 4.9
        adjacent_monst_weight = 100
        
        # The weight applied to the bomb feature
        bomb_weight = 3
        explosion_weight = 3
        
        # The weight applied to the wall feature
        wall_weight = 1

        # Create copied version of current world to test on for each iteration
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
        max_action_value = float("-inf")
        max_action = [0, 0]

#        print("current coordinates: ", (copied_char.x, copied_char.y))

        # Loop through all 8 moves using the copied char and decide which one to make
        # Loop through all the dx values
        for dx in range(-1, 2):
            # Loop through all the dy values
            for dy in range(-1, 2):
                # Reset world to OG position and get the character from it
                copied_world = SensedWorld.from_world(wrld)
                copied_char = copied_world.me(self)

                # get the new coordinates of the intended move
                x = copied_char.x + dx
                y = copied_char.y + dy
                # booleans to check whether the move is possible
                out_bounds_x = x < 0 or x >= copied_world.width()
                out_bounds_y = y < 0 or y >= copied_world.height()

                # ignore moves that are not possible
                if out_bounds_x:
                    continue
                if out_bounds_y:
                    continue
                if copied_world.wall_at(x, y):
                    continue
                # don't stay in the same place if there is another possible move
                if copied_char.x == x and copied_char.y == y:
                    continue
                # move to the exit if it is there!
                if copied_world.exit_at(x, y):
                    self.move(dx, dy)
                    break

#                print("================================================")
#                print("TODO: CHECK (", dx, dy, ")")
                copied_char.move(dx, dy)
                # update copied world and character after the move
                copied_world, events = copied_world.next()
                copied_char = copied_world.me(self)

                # if the move causes the char to die, do not move there!
                if copied_char is None:
                    continue
                if f.distance_to_monster(copied_char, copied_world) == 0:
                    continue

                # reset the bomb weight in case it was previously changed
                bomb_weight = 2
                # if the distance from the bomberman to its bomb is within 4 spaces
                if f.distance_to_bomb(copied_char, copied_world) <= 4:
                    # get the coordinates of the bomb
                    coordinates = f.get_bomb_loc(copied_char, copied_world)
                    # if the bomberman is in line to get hit with an explosion
                    if copied_char.x == coordinates[0] or copied_char.y == coordinates[1]:
                        # greatly increase the bomb weight to signify bad move
                        bomb_weight = bomb_weight**3

                # reset the monster weight in case it was previously changed
                monster_weight = 4.9
                # if the monster is 6 or greater spaces away, decrease monster weight
                if f.distance_to_monster(copied_char, copied_world) >= 6:
                    monster_weight = 3
                # if the monster is 3 spaces away or less, halve the exit weight
                if f.distance_to_monster(copied_char, copied_world) <= 3:
                    exit_weight = exit_weight / 2
#                print("new character coordinates: ", (copied_char.x, copied_char.y))
#                print("bomb weight: ", bomb_weight)

                # evaluation of move value for each adjacent move
                exit_val = 1/(f.distance_to_exit(copied_char, copied_world)) * exit_weight
                monst_val = -1/(f.distance_to_monster(copied_char, copied_world)) * monster_weight
                bomb_val = -1/(1+f.distance_to_bomb(copied_char, copied_world)) * bomb_weight
                adjacent_exit_val = f.next_to_exit(copied_char, copied_world) * adjacent_exit_weight
                adjacent_monst_val = -f.next_to_monster(copied_char, copied_world) * adjacent_monst_weight
                # wall_val = 1/(1+f.next_to_wall(copied_char, copied_world)) * wall_weight
                explosion_val = 1/(1+f.is_in_explosion(copied_char, copied_world)) * explosion_weight

#                print("=======================")
#                print("exit value: ", 1/f.distance_to_exit(copied_char, copied_world) * exit_weight)
#                print("monster value: ", -1/(f.distance_to_monster(copied_char, copied_world)) * monster_weight)
#                print("bomb value: ", -1/(1+f.distance_to_bomb(copied_char, copied_world) * bomb_weight))
#                print("next to exit value: ", f.next_to_exit(copied_char, copied_world) * adjacent_exit_weight)
#                print("next to monster value: ", -f.next_to_monster(copied_char, copied_world) * adjacent_monst_weight)
#                print("next to wall value: ", 1/(1+f.next_to_wall(copied_char, copied_world)) * wall_weight)
#                print("in explosion value: ", 1/(1+f.is_in_explosion(copied_char, copied_world)) * explosion_weight)
#                print("=======================")

                move_val = exit_val + monst_val + bomb_val + adjacent_exit_val + adjacent_monst_val + explosion_val # + wall_val
                #print("total value: ", move_val)

                # store the greatest value move
                if move_val >= max_action_value:
                    max_action_value = move_val
                    max_action[0] = dx
                    max_action[1] = dy

#        print("best value: ", max_action_value)
#        print("x: ", max_action[0])
#        print("y: ", max_action[1])

        # if the bomberman is currently next to wall
        if f.next_to_wall(self, wrld):
            # since bombs diagonal to a wall do not hit them,
            # place a bomb if it is directly to the left or right of the wall
            if x-1 > 0:
                if wrld.wall_at(self.x-1, self.y):
                    self.place_bomb()
            if x+1 < wrld.width():
                if wrld.wall_at(self.x+1, self.y):
                    self.place_bomb()
            # place a bomb if it is directly to the upwards or downwards of the wall
            if y-1 > 0:
                if wrld.wall_at(self.x, self.y-1):
                    self.place_bomb()
            if y+1 < wrld.height():
                if wrld.wall_at(self.x, self.y+1):
                    self.place_bomb()
        # else, if the monster is getting close to the bomberman, place a bomb
        elif f.distance_to_monster(self, wrld) <= 4 and (self.y != 0 or self.x != 1):
            self.place_bomb()

        # if the bomberman is next to the exit, move there!
        if f.next_to_exit(self, wrld):
            for x in range(self.x - 1, self.x + 2):
                for y in range(self.y - 1, self.y + 2):
                    if 0 <= x < wrld.width() and 0 <= y < wrld.height():
                        if wrld.exit_at(x, y):
                            self.move(x, y)
                            continue
        # if not, make the move determined from the exploitation of weights
        else:
            self.move(max_action[0], max_action[1])

        pass
