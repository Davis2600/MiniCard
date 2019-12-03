from card import Card


#1 card per line
def importDeck(filename):
    deckList = open(filename)
    text = deckList.read()
    lines = text.split('\n')
    deck = []
    deckStr = ''
    for line in lines:
        try:
            newcard = Card()
            newcard.createCardFromString(line)
            deck.append(newcard)
            if str(newcard) != '':
                deckStr += str(newcard)
                deckStr += ','
                

        except:
            raise Exception('Invalid Deck Format')
    deckStr = deckStr[0:-1]
    return deckStr

deck = importDeck('deckOne.txt')
print(deck)