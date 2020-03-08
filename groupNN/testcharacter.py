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
learning_rate = 0.2

# The weight applied to the exit feature
exit_weight = 6
adjacent_exit_weight = 100

# The weight applied to the monster feature
monster_weight = 3
adjacent_monst_weight = 100

# The weight applied to the bomb feature
bomb_weight = 2
explosion_weight = 10

# The weight applied to the wall feature
wall_weight = 0

# Previous feature values (for updating weights)
p_exit = 0
p_monster = 0
p_bomb = 0
p_wall = 0
p_adjacent_exit = 0
p_adjacent_monster = 0
p_explosion = 0

# Next move
nx = 0
ny = 0

class TestCharacter(CharacterEntity):
        
    def do(self, wrld):

        # ===============================
        # INITIALIZATION PHASE
        # ===============================
        # Initializes all variables and sets up world for testing
        
        # Read weights.txt
        weight_file = open("../weights.txt", "r")
        
        global exit_weight, monster_weight, bomb_weight, wall_weight, adjacent_exit_weight, adjacent_monst_weight, explosion_weight
        exit_weight = float(weight_file.readline())
        monster_weight = float(weight_file.readline())
        bomb_weight = float(weight_file.readline())
        wall_weight = float(weight_file.readline())
        adjacent_exit_weight = float(weight_file.readline())
        adjacent_monst_weight = float(weight_file.readline())
        explosion_weight = float(weight_file.readline())

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
            self.random_action(wrld)

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
        global p_exit, p_monster, p_bomb, p_wall, p_adjacent_exit, p_adjacent_monster, p_explosion
        p_exit = 1 / (1 + f.distance_to_exit(self.x, self.y, wrld))
        p_monster = -1 / (1 + f.distance_to_monster(self.x, self.y, wrld))
        p_bomb = -1 / (1 + f.distance_to_bomb(self.x, self.y, wrld))
        # p_wall = f.next_to_wall(self.x, self.y, wrld)
        p_adjacent_exit = f.next_to_exit(self.x, self.y, wrld)
        p_adjacent_monster = -f.next_to_monster(self.x, self.y, wrld)
        p_explosion = 1 / (1 + f.is_in_explosion(self.x, self.y, wrld))
        
        max_val_rand = self.non_rand_action(self.x, self.y, wrld, False)
        
        self.up_weights(wrld, max_val_rand)

    def non_rand_action(self, ix, iy, wrld, make_move):
        # Variable to hold the greatest value found when moving
        # max_action_value = float("-inf")
        max_action_value = float("-inf")
        max_action = [0, 0]

        # update previous feature values
        global p_exit, p_monster, p_bomb, p_wall, p_adjacent_exit, p_adjacent_monster, p_explosion
        p_exit = 1 / (1 + f.distance_to_exit(self.x, self.y, wrld))
        p_monster = -1 / (1 + f.distance_to_monster(self.x, self.y, wrld))
        p_bomb = -1 / (1 + f.distance_to_bomb(self.x, self.y, wrld))
        # p_wall = f.next_to_wall(self.x, self.y, wrld)
        p_adjacent_exit = f.next_to_exit(self.x, self.y, wrld)
        p_adjacent_monster = -f.next_to_monster(self.x, self.y, wrld)
        p_explosion = 1 / (1 + f.is_in_explosion(self.x, self.y, wrld))

        print("current coordinates: ", (self.x, self.y))

        # Loop through all 8 moves using the copied char and decide which one to make
        # Loop through all the dx values
        for dx in range(-1, 2):
            # Loop through all the dy values
            for dy in range(-1, 2):
                # Reset world to OG position and get the character from it
                # copied_world = SensedWorld.from_world(wrld)
                # copied_char = copied_world.me(self)

                x = ix + dx
                y = iy + dy
                out_bounds_x = x < 0 or x >= wrld.width()
                out_bounds_y = y < 0 or y >= wrld.height()

                # ignore moves that are not possible
                if out_bounds_x:
                    continue
                if out_bounds_y:
                    continue
                if self.x == x and self.y == y:
                    continue
                if wrld.wall_at(x, y):
                    continue

                # if the move causes the char to die, do not move there!
                if self is None:
                    continue

                print("new character coordinates: ", (x, y))

                # evaluation of move value for each adjacent move (+2 to each due to -1 return for some - avoid 1/0)
                exit_val = 1 / (1 + f.distance_to_exit(x, y, wrld)) * exit_weight
                monst_val = -1 / (1 + f.distance_to_monster(x, y, wrld)) * monster_weight
                bomb_val = -1 / (1 + f.distance_to_bomb(x, y, wrld)) * bomb_weight
                adjacent_exit_val = f.next_to_exit(x, y, wrld) * adjacent_exit_weight
                adjacent_monst_val = -f.next_to_monster(x, y, wrld) * adjacent_monst_weight
                # wall_val = 1/(1+f.next_to_wall(copied_char, copied_world)) * wall_weight
                print(f.is_in_explosion(x, y, wrld))
                explosion_val = 1 / (1 + f.is_in_explosion(x, y, wrld)) * explosion_weight

                print("=======================")
                print("exit value: ", 1 / (1 + f.distance_to_exit(x, y, wrld)) * exit_weight)
                print("monster value: ", -1 / (1 + (f.distance_to_monster(x, y, wrld))) * monster_weight)
                print("bomb value: ", -1 / (1 + f.distance_to_bomb(x, y, wrld) * bomb_weight))
                print("next to exit value: ", f.next_to_exit(x, y, wrld) * adjacent_exit_weight)
                print("next to monster value: ", -f.next_to_monster(x, y, wrld) * adjacent_monst_weight)
                print("next to wall value: ", 1 / (1 + f.next_to_wall(x, y, wrld)) * wall_weight)
                print("in explosion value: ", 1 / (1 + f.is_in_explosion(x, y, wrld)) * explosion_weight)
                print("=======================")

                move_val = exit_val + monst_val + bomb_val + adjacent_exit_val + adjacent_monst_val + explosion_val  # + wall_val
                print("total value: ", move_val)

                # store the greatest value move
                if move_val >= max_action_value:
                    max_action_value = move_val
                    max_action[0] = dx
                    max_action[1] = dy

        print("best value: ", max_action_value)
        print("x: ", max_action[0])
        print("y: ", max_action[1])
        global nx, ny
        nx = max_action[0]
        ny = max_action[1]

        if make_move == True:
            if f.next_to_wall(self.x, self.y, wrld):
                self.place_bomb()
            if f.next_to_exit(self.x, self.y, wrld):
                for x in range(self.x - 1, self.x + 2):
                    for y in range(self.y - 1, self.y + 2):
                        if 0 <= x < wrld.width() and 0 <= y < wrld.height():
                            if wrld.exit_at(x, y):
                                self.move(x, y)
                                continue
            else:
                self.move(max_action[0], max_action[1])
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
        
        delta = reward + max_val_prime - curr_value
        print("PRIME: ", max_val_prime, ", CURRENT: ", curr_value)
        print("DELTA: ", delta)
        
        global exit_weight, monster_weight, bomb_weight, wall_weight, adjacent_exit_weight, adjacent_monst_weight, explosion_weight
        
        # The weight applied to the exit feature
        exit_weight = exit_weight + learning_rate * delta * p_exit

        # The weight applied to the monster feature
        monster_weight = monster_weight + learning_rate * delta * p_monster
        
        # The weight applied to the bomb feature
        bomb_weight = bomb_weight + learning_rate * delta * p_bomb
        
        # The weight applied to the wall feature
        wall_weight = wall_weight + learning_rate * delta * p_wall

        # The weight applied to the adjacent exit feature
        adjacent_exit_weight = adjacent_exit_weight + learning_rate * delta * p_adjacent_exit

        # The weight applied to the adjacent monster feature
        adjacent_monst_weight = adjacent_monst_weight + learning_rate * delta * p_monster

        # The weight applied to the explosion feature
        explosion_weight = explosion_weight + learning_rate * delta * p_explosion
        
        # Store weights in txt file
        weight_file = open("../weights.txt", "r+")
        weight_file.seek(0)
        weight_file.write(str(exit_weight) + "\n")
        weight_file.write(str(monster_weight) + "\n")
        weight_file.write(str(bomb_weight) + "\n")
        weight_file.write(str(wall_weight) + "\n")
        weight_file.write(str(adjacent_exit_weight) + "\n")
        weight_file.write(str(adjacent_monst_weight) + "\n")
        weight_file.write(str(explosion_weight) + "\n")