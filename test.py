def fun1(cards):
	cards2 = cards.copy()
	cards2.remove(1)

def fun2(cards):
	cards.remove(2)
	fun3(cards)

def fun3(cards):
	cards.append(11)

cards = [3, 2, 5, 9, 1]
print(cards)
fun1(cards)
print(cards)
fun2(cards)
print(cards)