from green_card_seprater import *
from pprint import pprint
from os import system

start = time()
path = "../without-binnary/1080x2340/19.png"
bottom_cards = get_cards_on_screen(path)
top_cards = openJokerDeckCard(path)
top_cards['cards'] = bottom_cards
cards = top_cards
system('clear')
pprint(cards)
# open_card = getOpenDeckCard(path, top_cards['position']['y'])
# print(open_card)
print(time() - start)