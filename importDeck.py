from card import Card


#1 card per line
def importDeck(filename):
    deckList = open(filename)
    text = deckList.read()
    lines = text.split('\n')
    deck = []
    for line in lines:
        try:
            card = Card()
            card.createCardFromString(line)
            deck.append(card)
        except:
            raise Exception('Invalid Deck Format')
    return deck

