# This is necessary to find the main code
import math
import random
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

        # TODO All weights retrieved from .txt file to hold data between games

        # The weight applied to the exit feature
        exit_weight = -200

        # The weight applied to the monster feature
        monster_weight = 4
        
        # The weight applied to the bomb feature
        bomb_weight = 2
        
        # The weight applied to the wall feature
        wall_weight = 1

        # Choose based on decreasing percentage random or best given moves
        # TODO Gradient Descent
        # TODO decreasing amount and amt of turns is retrieved from .txt file

        # Makes a random action
        # self.non_rand_action(wrld, exit_weight, bomb_weight, monster_weight, wall_weight)

        # Makes a non-random action
        self.random_action(wrld)

        pass

    def random_action(self, wrld):
        dx = random.randrange(-1, 2, 1)
        dy = random.randrange(-1, 2, 1)
        print("Random dx: ", dx)
        print("Random dy: ", dy)
        print("Making random move (", dx, ",", dy, ")")
        self.move(dx, dy)

    def non_rand_action(self, wrld, exit_weight, bomb_weight, monster_weight, wall_weight):
        # Variable to hold the greatest value found when moving
        max_action_value = float("-inf")
        max_action = (1, 0)

        # Loop through all 8 moves using the copied char and decide which one to make
        # Loop through all the dx values
        for dx in range (-1, 2):
            # Loop through all the dy values
            for dy in range (-1, 2):
                print("=================================")
                print("SPACE (", dx, dy, ")")
                move_val = f.distance_to_exit(dx, dy, wrld) * exit_weight + f.distance_to_monster(dx, dy, wrld) * monster_weight + \
                f.distance_to_bomb(dx, dy, wrld) * bomb_weight + f.next_to_exit(dx, dy, wrld) * exit_weight + \
                f.next_to_monster(dx, dy, wrld) * monster_weight + f.next_to_wall(dx, dy, wrld) * wall_weight + \
                f.is_in_explosion(dx, dy, wrld) * bomb_weight
                if move_val > max_action_value:
                    max_action_value = move_val
                    max_action = (dx, dy)
                print("val: ", move_val)
                print("=================================")

        print("Making move (", max_action[0], ",", max_action[1], ") with value ", max_action_value)
        self.move(max_action[0], max_action[1])