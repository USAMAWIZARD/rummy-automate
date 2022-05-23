from pprint import pprint
ranks = {'joker': 0, 'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace1': 14}

suits = ['spades', 'hearts', 'diamonds', 'clubs']

four_cards = True


hand_cards = [[['8', 'diamonds'], ['10', 'diamonds']], [['4', 'clubs'], ['king', 'clubs'], ['ace1', 'clubs']], [['8', 'hearts'], ['10', 'hearts'], ['5', 'hearts'], ['ace', 'hearts']], [['joker', 'spades'], ['8', 'spades'], ['queen', 'spades']], [['joker', None]]]

sequence_and_rest_cards = dict()

pprint(hand_cards)
