import random

class UnoCard:
    '''represents an Uno card
    attributes:
      rank: int from 0 to 9
      color: string'''

    def __init__(self, rank, color):
        '''UnoCard(rank, color) -> UnoCard
        creates an Uno card with the given rank and color'''
        self.rank = rank
        self.color = color

    def __str__(self):
        '''str(Unocard) -> str'''
        return(str(self.color) + ' ' + str(self.rank))

    def is_match(self, other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not'''
        return (self.color == other.color) or (self.rank == other.rank)

class ActionCard(UnoCard):
    '''represents an Uno action card
    attributes:
      action: string, either 'skip', 'reverse', or 'drawTwo'
      color: string
    '''
    def __init__(self, action, color):
        '''ActionCard(action, color) -> ActionCard
        creates an Uno action card with the given action and color'''
        self.action = action
        self.color = color

    def __str__(self):
        '''str(ActionCard) -> str'''
        return(self.color + ' ' + self.action)

    def is_match(self, other):
        '''ActionCard.is_match(UnoCard) -> boolean
        returns True if the cards match in action or color, False if not'''
        return (self.color == other.color) or (self.action == other.action)

class WildCard(ActionCard):
    '''represents a Wild card
    attributes:
      action: string, either 'wild' or 'wildDrawFour'
    '''
    def __init__(self, action):
        '''WildCard(action) -> WildCard
        creates a Wild card with the given action'''
        self.action = action
        self.color = None  # Wild cards have no color initially

    def __str__(self):
        '''str(WildCard) -> str'''
        return self.action

    def is_match(self, other):
        '''WildCard.is_match(UnoCard) -> boolean
        returns True if the card is a Wild card, False if not'''
        return self.action in ['wild', 'wildDrawFour']

    def can_play(self, hand, top_card):
        '''WildCard.can_play(hand, top_card) -> boolean
        returns True if the Wild Draw Four card can be played, False if not.
        The card can be played if the player has no card whose color matches the top card.
        '''
        for card in hand:
            if card.color == top_card.color:
                return False
        return True

class UnoDeck:
    '''represents a deck of Uno cards
    attribute:
      deck: list of UnoCards'''

    def __init__(self):
        '''UnoDeck() -> UnoDeck
        creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0, color))  # one 0 of each color
            for i in range(2):
                for n in range(1, 10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(n, color))
            # add action cards
            for action in ['skip', 'reverse', 'drawTwo']:
                for i in range(2):
                    self.deck.append(ActionCard(action, color))
        # add wild cards
        for i in range(4):
            self.deck.append(WildCard('wild'))
        for i in range(4):
            self.deck.append(WildCard('wildDrawFour'))
        random.shuffle(self.deck)  # shuffle the deck

    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with '+str(len(self.deck)) + ' cards remaining.'

    def is_empty(self):
        '''UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise'''
        return len(self.deck) == 0

    def deal_card(self):
        '''UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)'''
        return self.deck.pop()

    def reset_deck(self, pile):
        '''UnoDeck.reset_deck(pile) -> None
        resets the deck from the pile'''
        if len(self.deck) != 0:
            return
        self.deck = pile.reset_pile() # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck

class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''

    def __init__(self, deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        card = deck.deal_card()
        self.pile = [card]  # all the cards in the pile

    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has ' + str(self.pile[-1]) + ' on top.'

    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]

    def add_card(self, card):
        '''UnoPile.add_card(card) -> None
        adds the card to the top of the pile'''
        self.pile.append(card)

    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck

class UnoPlayer:
    '''represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards'''

    def __init__(self, name, deck):
        '''UnoPlayer(name, deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self):
        '''UnoPlayer.get_name() -> str
        returns the player's name'''
        return self.name

    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def has_won(self):
        '''UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0

    def draw_card(self, deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card

    def play_card(self, card, pile):
        '''UnoPlayer.play_card(card, pile) -> None
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''

        self.hand.remove(card)
        pile.add_card(card)

    def take_turn(self, deck, pile, playerList, currentPlayerNum):
        '''UnoPlayer.take_turn(deck, pile) -> None
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        # print player info
        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        if len(matches) > 0:  # can play
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index + 1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            card_played = matches[choice - 1]
            self.play_card(card_played, pile)

            # handle action cards
            if isinstance(card_played, ActionCard):
                if card_played.action == 'skip':
                    print(f"{playerList[currentPlayerNum].get_name()}'s turn is skipped!")
                    currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
                elif card_played.action == 'reverse':
                    playerList.reverse()
                    print("Play order reversed!")
                    currentPlayerNum = (currentPlayerNum + 1) % len(playerList) # Need to account for reverse
                elif card_played.action == 'drawTwo':
                    next_player = (currentPlayerNum + 1) % len(playerList)
                    playerList[next_player].draw_card(deck)
                    playerList[next_player].draw_card(deck)
                    print(f"{playerList[next_player].get_name()} draws two cards!")
                    currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
            # handle wild cards
            elif isinstance(card_played, WildCard):
                if card_played.action == 'wild':
                    print("You played a Wild card. Choose a new color:")
                    for i, color in enumerate(['red', 'blue', 'green', 'yellow']):
                        print(f"{i+1}: {color}")
                    choice = 0
                    while choice < 1 or choice > 4:
                        choicestr = input("Enter your choice: ")
                        if choicestr.isdigit():
                            choice = int(choicestr)
                    card_played.color = ['red', 'blue', 'green', 'yellow'][choice - 1]
                    print(f"The new color is {card_played.color}")
                elif card_played.action == 'wildDrawFour':
                    if card_played.can_play(self.hand, topcard):
                        print("You played a Wild Draw Four card!")
                        next_player = (currentPlayerNum + 1) % len(playerList)
                        for _ in range(4):  # Draw 4 cards
                            playerList[next_player].draw_card(deck)
                        print(f"{playerList[next_player].get_name()} draws four cards and their turn is skipped.")
                        currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
                    else:
                        print("You can't play Wild Draw Four! You have a matching color card.")
                        currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)
            else:   # still can't play
                print("Sorry, you still can't play.")
            input("Press enter to continue.")
        return currentPlayerNum

def play_uno(numPlayers):
    '''play_uno(numPlayers) -> None
    plays a game of Uno with numPlayers'''
    # set up full deck and initial discard pile
    deck = UnoDeck()
    pile = UnoPile(deck)
    # set up the players
    playerList = [] #list must be mutable 
    for n in range(numPlayers):
        # get each player's name, then create an UnoPlayer
        if n == 0:
            name = "Computer"
            playerList.append(AIPlayer(name, deck))
        else:
            name = input('Player #' + str(n + 1) + ', enter your name: ')
            playerList.append(UnoPlayer(name,deck))
    # randomly assign who goes first
    currentPlayerNum = random.randrange(numPlayers)
    # play the game
    while True:
        # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')
        # take a turn
        if isinstance(playerList[currentPlayerNum], AIPlayer):
            currentPlayerNum = playerList[currentPlayerNum].take_turn(deck, pile, playerList, currentPlayerNum)
        else:
            currentPlayerNum = playerList[currentPlayerNum].take_turn(deck, pile, playerList, currentPlayerNum)
        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].get_name() + " wins!")
            print("Thanks for playing!")
            break
        # go to the next player
        currentPlayerNum = (currentPlayerNum + 1) % numPlayers

class AIPlayer(UnoPlayer):
    def __init__(self, name, deck):
        super().__init__(name, deck)

    def take_turn(self, deck, pile, playerList, currentPlayerNum):
        '''AIPlayer.take_turn(deck, pile) -> None
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''

        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        topcard = pile.top_card()

        # 1. Check for matching cards
        matches = [card for card in self.hand if card.is_match(topcard)]
        if matches:
            # Prioritize matching color, then rank
            matches.sort(key=lambda card: (card.color == topcard.color, card.rank), reverse=True)
            card_played = matches[0]
            self.play_card(card_played, pile)
            print(f"{self.name} played: {card_played}")
            # Handle action cards
            if isinstance(card_played, ActionCard):
                if card_played.action == 'skip':
                    print(f"{playerList[currentPlayerNum].get_name()}'s turn is skipped!")
                    currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
                elif card_played.action == 'reverse':
                    playerList.reverse()
                    print("Play order reversed!")
                    currentPlayerNum = (currentPlayerNum + 1) % len(playerList)  # Need to account for reverse
                elif card_played.action == 'drawTwo':
                    next_player = (currentPlayerNum + 1) % len(playerList)
                    playerList[next_player].draw_card(deck)
                    playerList[next_player].draw_card(deck)
                    print(f"{playerList[next_player].get_name()} draws two cards!")
                    currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
            # Handle wild cards
            elif isinstance(card_played, WildCard):
                if card_played.action == 'wild':
                    # Choose a random color
                    new_color = random.choice(['red', 'blue', 'green', 'yellow'])
                    card_played.color = new_color
                    print(f"The new color is {card_played.color}")
                elif card_played.action == 'wildDrawFour':
                    if card_played.can_play(self.hand, topcard):
                        next_player = (currentPlayerNum + 1) % len(playerList)
                        for _ in range(4):  # Draw 4 cards
                            playerList[next_player].draw_card(deck)
                        print(f"{playerList[next_player].get_name()} draws four cards and their turn is skipped.")
                        currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
                    else:
                        print("AI cannot play Wild Draw Four! It has a matching color card.")
                        currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
        else:
            # 2. Check for Wild Draw Four (if allowed)
            wild_draw_four_cards = [card for card in self.hand if card.action == 'wildDrawFour' and card.can_play(self.hand, topcard)]
            if wild_draw_four_cards:
                card_played = wild_draw_four_cards[0]
                self.play_card(card_played, pile)
                print(f"{self.name} played: {card_played}")

                # Choose a random color
                new_color = random.choice(['red', 'blue', 'green', 'yellow'])
                card_played.color = new_color
                print(f"The new color is {card_played.color}")

                next_player = (currentPlayerNum + 1) % len(playerList)
                for _ in range(4):
                    playerList[next_player].draw_card(deck)
                print(f"{playerList[next_player].get_name()} draws four cards and their turn is skipped.")
                currentPlayerNum = (currentPlayerNum + 1) % len(playerList)
            # 3. Check for Wild card (if allowed)
            elif [card for card in self.hand if card.action == 'wild']:
                wild_cards = [card for card in self.hand if card.action == 'wild']
                card_played = wild_cards[0]
                self.play_card(card_played, pile)
                print(f"{self.name} played: {card_played}")

                # Choose a random color
                new_color = random.choice(['red', 'blue', 'green', 'yellow'])
                card_played.color = new_color
                print(f"The new color is {card_played.color}")
            else:
                # 4. Draw a card if no playable card
                print("AI cannot play, drawing a card.")
                newcard = self.draw_card(deck)
                print(f"AI drew: {newcard}")
                if newcard.is_match(topcard):
                    self.play_card(newcard, pile)
                    print(f"AI played: {newcard}")
                else:
                    print("AI cannot play the drawn card.")
        return currentPlayerNum
