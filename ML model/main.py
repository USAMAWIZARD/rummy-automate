from green_card_seprater import *
from pprint import pprint
from os import system
from valid_cards import getValidCards
from minimum_swaps import minimumSwaps

system('clear')
start = time()
path = "../without-binnary/1080x2340/19.png"
bottom_cards = get_cards_on_screen(path)
top_cards = openJokerDeckCard(path)

for cards in bottom_cards:
    for card in cards:
        if top_cards['joker_deck'] == 'JCard':
            if card[0] == 'ace':
                card[1] = 'joker'
        elif top_cards['joker_deck'] == card[0]:
            card[1] = 'joker'

top_cards['cards'] = bottom_cards
cards = top_cards
pprint(cards)
print("************")
valid_cards = getValidCards(cards['cards'], [cards['open_deck']['number'], cards['open_deck']['suit']])
pprint(valid_cards)
# minimumSwaps(cards['cards'], valid_cards)
# open_card = getOpenDeckCard(path, top_cards['position']['y'])
# print(open_card)
print(time() - start)



