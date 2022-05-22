from green_card_seprater import *

start = time()
path = "../without-binnary/2.png"
# print(get_cards_on_screen(path))
# openJokerCard(path)
# openJokerDeckCard(path)
joker_name, position = openJokerDeckCard(path)

# getOpenDeckCard(path, position)

print(time() - start)