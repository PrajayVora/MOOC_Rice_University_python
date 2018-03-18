# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cardlist1, cardlist2, exposed, state, turns
    turns = 0
    cardlist1 = range(8)
    cardlist2 = range(8)
    cardlist1.extend(cardlist2)
    exposed = [False] * 16
    state = 0
    random.shuffle(cardlist1)
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, card1, card2, turns
    global state
    x = 800//16
    y = pos[0]//x
    if exposed[y]:
        return
    else:
        exposed[y] = True
    if state == 0:
        card1 = y
        state = 1
    elif state == 1:
        card2 = y
        if cardlist1[card1] == cardlist1[card2]:
            card1 = y
        turns = turns + 1
        label.set_text('Turns = ' + str(turns))
        state = 2
    else:
        if cardlist1[card1] != cardlist1[card2]:
            exposed[card1] = False
            exposed[card2] = False
        card1 = y
        state = 1
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cardlist1, turns
    card_pos = 0
    
    for cards in cardlist1:
        canvas.draw_text(str(cards), [card_pos, 85], 100, 'White')
    
    for i in range(len(exposed)):
        if exposed[i] == False:
            canvas.draw_line([card_pos, 50], [card_pos+49, 50], 100, 'Green')
        else:
            canvas.draw_line([card_pos, 50], [card_pos+49, 50], 100, 'White')
            canvas.draw_text(str(cardlist1[i]), [card_pos, 85], 100, 'Black')
        card_pos = card_pos + 50
        label.set_text('Turns = ' + str(turns))
    
new_game()

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()