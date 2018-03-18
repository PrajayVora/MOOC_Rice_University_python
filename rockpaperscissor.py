# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
import random

def name_to_number(name):
    if name == 'rock':
        rock = 0
        return rock
    elif name == 'Spock':
        Spock = 1
        return Spock
    elif name == 'paper':
        paper = 2
        return paper
    elif name == 'lizard':
        lizard = 3
        return lizard
    elif name == 'scissors':
        scissors = 4
        return scissors
    else:
        print 'no'

    # convert name to number using if/elif/else
    # don't forget to return the result!


def number_to_name(number):
    if number == 0:
        name = 'rock'
        return name
    elif number == 1:
        name = 'Spock'
        return name
    elif number == 2:
        name = 'paper'
        return name
    elif number == 3:
        name = 'lizard'
        return name
    elif number == 4:
        name = 'scissors'
        return name
    else: print 'no'
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    

def rpsls(player_choice): 
    
    # print a blank line to separate consecutive games
    print '\n'
    
    # print out the message for the player's choice
    print 'Players chooses', player_choice
    
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # print out the message for computer's choice
    print 'Computer chooses', comp_choice
    
    # compute difference of comp_number and player_number modulo five
    diff = (comp_number - player_number) % 5
    
    # use if/elif/else to determine winner, print winner message
    if diff == 1:
        print 'Computer wins!'
    elif diff  == 2:
        print 'Computer wins!'
    elif diff == 3:
        print 'Player wins!'
    elif diff == 4:
        print 'Player wins!'
    else:
        print "Player and computer tie!"
        
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


