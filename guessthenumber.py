# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import math
import random


# helper function to start and restart the game
def new_game():
    global n
    n = 7
    global secret_number
    secret_number = random.randint(0, 100)
    print 'New Game'
    print 'The range is [0, 100)'
    print 'The number of guesses remaining', n
    print ' '

# define event handlers for control panel
def range100():
    global n
    n = 7
    global secret_number
    secret_number = random.randint(0, 100)
    print 'The range is [0, 100)'
    print 'The number of gusses remaining', n
    print ' '

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global n
    n = 10
    global secret_number
    secret_number = random.randint(0, 1000)
    print 'The range is [0, 1000)'
    print 'The number of gusses remaining', n
    print ' '
    
def input_guess(guess):
    global n
    n = n - 1
    global secret_number
    guess = int(guess)
    print 'The guess was', guess
    if guess < secret_number:
        print "Higher"
        print 'The number of guesses remaining', n
    elif guess > secret_number:
        print 'Lower'
        print 'The number of guesses remaining', n
    elif guess == secret_number:
        print 'Correct'
        print 'You Win!'
        print ' '
        new_game()
    else: print 'Invalid Guess'
    print ' '
    
    if n == 0:
        print 'You Lose!'
        new_game()
    
# create frame
f = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame
f.add_button('Range is [0, 100)', range100)
f.add_button('Range is [0, 1000)', range1000)
f.add_input('Enter a guess', input_guess, 200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
