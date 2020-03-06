# This is necessary to find the main code
import math
import sys

sys.path.insert(0, '../bomberman')
from sensed_world import SensedWorld
import Features

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
        
        # The weight applied to the bomb feature
        bomb_weight = 2
        
        # The weight applied to the wall feature
        wall_weight = 1

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
                copied_char.move(dx, dy)
                move_val = Features.distance_to_exit(copied_char, copied_world) * exit_weight + Features.distance_to_monster(copied_char, copied_world) * monster_weight + \ 
                Features.distance_to_bomb(copied_char, copied_world) * bomb_weight + Features.next_to_exit(copied_char, copied_world) * exit_weight + \
                Features.next_to_monster(copied_char, copied_world) * monster_weight + Features.next_to_wall(copied_char, copied_world) * wall_weight + \
                Features.is_in_explosion(copied_char, copied_world) * bomb_weight

        self.move(max_action[0], max_action[1])

        print("================================================")
        print("exit distance: ", Features.distance_to_exit(wrld))
        print("monster distance: ", Features.distance_to_monster(wrld))
        print("bomb distance: ", Features.distance_to_bomb(wrld))
        print("next to exit: ", Features.next_to_exit(wrld))
        print("next to monster: ", Features.next_to_monster(wrld))
        print("next to wall: ", Features.next_to_wall(wrld))
        print("in explosion: ", Features.is_in_explosion(wrld))
        print("================================================")

        pass