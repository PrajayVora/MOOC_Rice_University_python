# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_hand = []             # create Hand object

    def __str__(self):
        ans = 'Hand contains '
        for i in range(len(self.card_hand)):
            ans += str(self.card_hand[i]) + ' '
        return ans                  # return a string representation of a hand

    def add_card(self, card):
        self.card_hand.append(card)   	# add a card object to a hand

    def get_value(self):
        value = 0
        ace_flag = False
        for card in self.card_hand:
            if Card.get_rank(card) == 'A':
                ace_flag = True
            value += VALUES[card.get_rank()]

        if ace_flag  and value+10 <= 21:
            value += 10
        return(value)        
            
   
    def draw(self, canvas, pos):	# draw a hand on the canvas, use the draw method for cards
        OFFSET = 100
        if len(self.card_hand) > 6:
            OFFSET = 30
        elif len(self.card_hand) > 5:
            OFFSET = 80
        added_offset = 0
        for c in self.card_hand:
            c.draw(canvas, [pos[0]+added_offset, pos[1]]) 
            added_offset += OFFSET
        
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        self.pos_card = 0
        for suit in SUITS:
            for rank in RANKS:
                add_card = Card(suit, rank)
                self.deck.append(add_card)# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        self.pos_card -= 1
        return self.deck[self.pos_card]	# deal a card object from the deck
    
    def __str__(self):
        ans1 = 'Deck contains '
        for j in range(len(self.deck)):
            ans1 += str(self.deck[j]) + ' '
        return ans1       # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, deck
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print dealer_hand, player_hand
    in_play = True

def hit():
    global outcome, in_play, score
    outcome = None
    if not in_play:
        return
    
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
    
    if player_hand.get_value() > 21:
        outcome = 'You are busted'
        print outcome
        in_play = False
        score = score - 1
        print score
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, score, in_play
    if not in_play:
        return
    
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    if dealer_hand.get_value() > 21:
        outcome = 'Dealer is busted'
        print outcome
        score = score + 1
        print score
        
    if player_hand.get_value() < dealer_hand.get_value():
        outcome = 'Dealer wins'
        score = score - 1
        print outcome, score
    else:
        outcome = 'Player wins'
        score = score + 1
        print outcome, score
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global outcome, in_play
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", (100,100), 48,"Cyan", 'sans-serif')
    canvas.draw_text("Score "+str(score), (350, 100), 36, "Black", 'sans-serif' )
    canvas.draw_text("Dealer", (50, 200), 36, "Black", 'sans-serif')
    canvas.draw_text(str(outcome), (200, 200), 28, "Black", 'sans-serif')
    canvas.draw_text("Player", (50, 400), 36, "Black", 'sans-serif')
    if in_play:
        canvas.draw_text("Hit or Stand?", (220, 400), 30, "Black", 'sans-serif')
    else:
        canvas.draw_text("New Deal?", (220, 400), 30, "Black", 'sans-serif')
    
    dealer_hand.draw(canvas, (50,220))
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          (51+CARD_BACK_CENTER[0], 221+CARD_BACK_CENTER[1]) , CARD_SIZE)
    player_hand.draw(canvas, (50,420))


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric