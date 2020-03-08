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
        exit_weight = 10
        adjacent_exit_weight = 100

        # The weight applied to the monster feature
        monster_weight = 2
        adjacent_monst_weight = 100
        
        # The weight applied to the bomb feature
        bomb_weight = 6
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

        print("current coordinates: ", (copied_char.x, copied_char.y))

        # Loop through all 8 moves using the copied char and decide which one to make
        # Loop through all the dx values
        for dx in range(-1, 2):
            # Loop through all the dy values
            for dy in range(-1, 2):
                # Reset world to OG position and get the character from it
                copied_world = SensedWorld.from_world(wrld)
                copied_char = copied_world.me(self)

                x = copied_char.x + dx
                y = copied_char.y + dy
                out_bounds_x = x < 0 or x >= copied_world.width()
                out_bounds_y = y < 0 or y >= copied_world.height()

                # ignore moves that are not possible
                if out_bounds_x:
                    continue
                if out_bounds_y:
                    continue
                if copied_char.x == x and copied_char.y == y:
                    continue
                if copied_world.wall_at(x, y):
                    continue
                if copied_world.exit_at(x, y):
                    self.move(dx, dy)
                    break

                print("================================================")
                print("TODO: CHECK (", dx, dy, ")")
                copied_char.move(dx, dy)
                # potentially update copied world and character?
                # fixes same values for each move but distorts sense of self coordinates
                copied_world, events = copied_world.next()
                copied_char = copied_world.me(self)

                # if the move causes the char to die, do not move there!
                if copied_char is None:
                    continue
                if f.distance_to_monster(copied_char, copied_world) == 0:
                    continue

                print("new character coordinates: ", (copied_char.x, copied_char.y))

                # evaluation of move value for each adjacent move (+2 to each due to -1 return for some - avoid 1/0)
                exit_val = 1/(f.distance_to_exit(copied_char, copied_world)) * exit_weight
                monst_val = -1/(f.distance_to_monster(copied_char, copied_world)) * monster_weight
                bomb_val = -1/(1+f.distance_to_bomb(copied_char, copied_world)) * bomb_weight
                adjacent_exit_val = f.next_to_exit(copied_char, copied_world) * adjacent_exit_weight
                adjacent_monst_val = -f.next_to_monster(copied_char, copied_world) * adjacent_monst_weight
                # wall_val = 1/(1+f.next_to_wall(copied_char, copied_world)) * wall_weight
                print(f.is_in_explosion(copied_char, copied_world))
                explosion_val = 1/(1+f.is_in_explosion(copied_char, copied_world)) * explosion_weight

                print("=======================")
                print("exit value: ", 1/f.distance_to_exit(copied_char, copied_world) * exit_weight)
                print("monster value: ", -1/(f.distance_to_monster(copied_char, copied_world)) * monster_weight)
                print("bomb value: ", -1/(1+f.distance_to_bomb(copied_char, copied_world) * bomb_weight))
                print("next to exit value: ", f.next_to_exit(copied_char, copied_world) * adjacent_exit_weight)
                print("next to monster value: ", -f.next_to_monster(copied_char, copied_world) * adjacent_monst_weight)
                print("next to wall value: ", 1/(1+f.next_to_wall(copied_char, copied_world)) * wall_weight)
                print("in explosion value: ", 1/(1+f.is_in_explosion(copied_char, copied_world)) * explosion_weight)
                print("=======================")

                move_val = exit_val + monst_val + bomb_val + adjacent_exit_val + adjacent_monst_val + explosion_val # + wall_val
                print("total value: ", move_val)

                # store the greatest value move
                if move_val >= max_action_value:
                    max_action_value = move_val
                    max_action[0] = dx
                    max_action[1] = dy

        print("best value: ", max_action_value)
        print("x: ", max_action[0])
        print("y: ", max_action[1])

        if f.next_to_wall(self, wrld):
            self.place_bomb()
        if f.next_to_exit(self, wrld):
            for x in range(self.x - 1, self.x + 2):
                for y in range(self.y - 1, self.y + 2):
                    if 0 <= x < wrld.width() and 0 <= y < wrld.height():
                        if wrld.exit_at(x, y):
                            self.move(x, y)
                            continue
        else:
            self.move(max_action[0], max_action[1])

        # print("================================================")
        # print("exit distance: ", f.distance_to_exit(copied_char, copied_world))
        # print("monster distance: ", f.distance_to_monster(copied_char, copied_world))
        # print("bomb distance: ", f.distance_to_bomb(copied_char, copied_world))
        # print("next to exit: ", f.next_to_exit(copied_char, copied_world))
        # print("next to monster: ", f.next_to_monster(copied_char, copied_world))
        # print("next to wall: ", f.next_to_wall(copied_char, copied_world))
        # print("in explosion: ", f.is_in_explosion(copied_char, copied_world))
        # print("================================================")

        pass
