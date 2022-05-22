from green_card_seprater import *

start = time()
path = "../without-binnary/5.png"
# print(get_cards_on_screen("../without-binnary/2.png"))
# openJokerCard("../without-binnary/2.png")
# openJokerDeckCard("../without-binnary/2.png")
joker_name, position = openJokerDeckCard(path)

getOpenDeckCard(path, position)

print(time() - start)