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

#TODO maybe create weights for all features instead of reusing?
# The rate at which to change the weights
learning_rate = 0.01

# The weight applied to the exit feature
exit_weight = -2

# The weight applied to the monster feature
monster_weight = 3

# The weight applied to the bomb feature
bomb_weight = 2

# The weight applied to the wall feature
wall_weight = -1

# Previous feature values (for updating weights)
p_exit = 0
p_monster = 0
p_bomb = 0
p_wall = 0

# Next move
nx = 0
ny = 0

class TestCharacter(CharacterEntity):
        
    def do(self, wrld):

        # ===============================
        # INITIALIZATION PHASE
        # ===============================
        # Initializes all variables and sets up world for testing

        print("\nUsing weights:")
        print("  exit: ", exit_weight, " monster: ", monster_weight, " bomb: ", bomb_weight,
              " wall: ", wall_weight)

        # TODO store in descent.txt
        # Gradient Descent percentage variable to decrease by set amount

        desc_file = open("../descent.txt", "r+")

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
            self.non_rand_action(self.x, self.y, wrld, True)

        else:
            self.non_rand_action(self.x, self.y, wrld, True)
            #self.random_action(wrld)

        pass

    def random_action(self, wrld):
        dx = random.randrange(-1, 2, 1)
        dy = random.randrange(-1, 2, 1)
        print("Random dx: ", dx)
        print("Random dy: ", dy)
        print("Making random move (", dx, ",", dy, ")")
        self.move(dx, dy)
        
        # Update next move
        global nx, ny
        nx = dx
        ny = dy
        
        # update previous feature values
        global p_exit, p_monster, p_bomb, p_wall
        p_exit = f.distance_to_exit(self.x, self.y, wrld)
        p_monster = f.distance_to_monster(self.x, self.y, wrld)
        p_bomb = f.distance_to_bomb(self.x, self.y, wrld)
        p_wall = f.next_to_wall(self.x, self.y, wrld)
        
        max_val_rand = self.non_rand_action(self.x, self.y, wrld, False)
        
        self.up_weights(wrld, max_val_rand)

    def non_rand_action(self, x, y, wrld, make_move):
        # Variable to hold the greatest value found when moving
        # max_action_value = float("-inf")
        max_action_value = float("-inf")
        max_action = (1, 0)

        # update previous feature values
        global p_exit, p_monster, p_bomb, p_wall
        p_exit = f.distance_to_exit(self.x, self.y, wrld)
        p_monster = f.distance_to_monster(self.x, self.y, wrld)
        p_bomb = f.distance_to_bomb(self.x, self.y, wrld)
        p_wall = f.next_to_wall(self.x, self.y, wrld)

        # Loop through all 8 moves using the copied char and decide which one to make
        # Loop through all the dx values
        for dx in range (-1, 2):
            # Loop through all the dy values
            for dy in range (-1, 2):
                print("=================================")
                print("SPACE (", dx, dy, ")")
                
                move_val = f.distance_to_exit(x+dx, y+dy, wrld) * exit_weight + f.distance_to_monster(x+dx, y+dy, wrld) * monster_weight + \
                f.distance_to_bomb(x+dx, y+dy, wrld) * bomb_weight + f.next_to_exit(x+dx, y+dy, wrld) * exit_weight + \
                f.next_to_monster(x+dx, y+dy, wrld) * monster_weight + f.next_to_wall(x+dx, y+dy, wrld) * wall_weight + \
                f.is_in_explosion(x+dx, y+dy, wrld) * bomb_weight
                if move_val > max_action_value:
                    max_action_value = move_val
                    max_action = (dx, dy)
                print("val: ", move_val)
                print("=================================")

        if make_move == True:
            print("Making move (", max_action[0], ",", max_action[1], ") with value ", max_action_value)
            self.move(max_action[0], max_action[1])
            # Update next move
            global nx, ny
            nx = max_action[0]
            ny = max_action[1]
            self.up_weights(wrld, max_action_value)
        
        else:
            return max_action_value
        
    # Update weights
    def up_weights(self, wrld, curr_value):
        
        reward = 0
        if f.distance_to_monster(self.x, self.y, wrld) == 0 or f.is_in_explosion(self.x, self.y, wrld) == 1:
            reward = -5000
        elif f.distance_to_exit(self.x, self.y, wrld) == 0:
            reward = 3000
            
        max_val_prime = self.non_rand_action(self.x + nx, self.y + ny, wrld, False)
        print("Next Move: ", nx, " ", ny)
        
        delta = reward + max_val_prime - curr_value
        print("PRIME: ", max_val_prime, ", CURRENT: ", curr_value)
        print("DELTA: ", delta)
        
        global exit_weight, monster_weight, bomb_weight, wall_weight
        
        # The weight applied to the exit feature
        exit_weight = exit_weight + learning_rate * delta * p_exit

        # The weight applied to the monster feature
        monster_weight = monster_weight + learning_rate * delta * p_monster
        
        # The weight applied to the bomb feature
        bomb_weight = bomb_weight + learning_rate * delta * p_bomb
        
        # The weight applied to the wall feature
        wall_weight = wall_weight + learning_rate * delta * p_wall

        