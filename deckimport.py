from card import Card

def importDeck(filename):
    deckList = open(filename)
    text = deckList.read()
    lines = text.split('\n')
    deck = []
    deckStr = ''
    for line in lines:
        try:
            print(line)
            newcard = Card()
            newcard.createCardFromString(line)
            deck.append(newcard)
            if str(newcard) != '':
                deckStr += str(newcard)
                deckStr += ','
                

        except:
            raise Exception('Invalid Deck Format on line:', line)
    deckStr = deckStr[0:-1]
    return deckStr

deck = importDeck('deckOne.txt')
print(deck)