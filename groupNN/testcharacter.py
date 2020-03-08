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

        weights_file = open("/Users/chrisbell/Dropbox/SeniorYear/CTerm/CS 4341/Projects/Bomberman3/groupNN/weights.txt", "r")

        # The rate at which to change the weights
        learning_rate = 0.2

        # All weights retrieved from .txt file to hold data between games

        # The weight applied to the exit feature
        exit_weight = int(weights_file.readline())

        # The weight applied to the monster feature
        monster_weight = int(weights_file.readline())
        
        # The weight applied to the bomb feature
        bomb_weight = int(weights_file.readline())
        
        # The weight applied to the wall feature
        wall_weight = int(weights_file.readline())

        # TODO Close after adjusting weights
        weights_file.close()

        print("\nUsing weights:")
        print("  exit: ", exit_weight, " monster: ", monster_weight, " bomb: ", bomb_weight,
              " wall: ", wall_weight)

        # TODO store in descent.txt
        # Gradient Descent percentage variable to decrease by set amount

        desc_file = open("/Users/chrisbell/Dropbox/SeniorYear/CTerm/CS 4341/Projects/Bomberman3/groupNN/descent.txt", "r+")

        grad_desc_perc = 10000

        # Amount to decrease the percentage by
        dec_amt = 1

        # Current percentage chance
        curr_desc = desc_file.readline()

        print("OLD VALUE: ", curr_desc)

        int_curr = int(curr_desc)
        new_total = int_curr + dec_amt
        desc_file.seek(0)
        desc_file.truncate()
        desc_file.write(str(new_total))
        # desc_file.seek(0)
        # print("NEW VALUE: ", desc_file.readline())
        desc_file.close()

        # Choose based on decreasing percentage random or best given moves
        # TODO Gradient Descent
        # TODO decreasing amount and amt of turns is retrieved from .txt file

        rand_choice = random.randrange(0, 10000, 1)

        if rand_choice <= int_curr:
            self.non_rand_action(wrld, exit_weight, bomb_weight, monster_weight, wall_weight)

        else:
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
        # max_action_value = float("-inf")
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