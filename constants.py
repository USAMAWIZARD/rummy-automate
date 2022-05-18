ranks = {'joker': 0, 'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace1': 14}

suits = ['spades', 'hearts', 'diamonds', 'clubs']

four_cards = True

# deck = ['queen', 'clubs']
deck = ['8', 'diamonds']

hand_cards = [[['8', 'diamonds'], ['10', 'diamonds']], [['4', 'clubs'], ['king', 'clubs'], ['ace1', 'clubs']], [['8', 'hearts'], ['10', 'hearts'], ['5', 'hearts'], ['ace', 'hearts']], [['joker', 'spades'], ['8', 'spades'], ['queen', 'spades']], [['joker', None]]]

sequence_and_rest_cards = dict()

set_hand_cards = [['8', 'diamonds'], ['8', 'spades'], ['8', 'clubs'], ['8', 'diamonds'], ['2', 'diamonds'], ['2', 'spades'], ['joker', 'diamonds']]

# hand_cards = [[['2', 'clubs'], ['3', 'clubs'], ['4', 'clubs'], ['7', 'clubs'], ['8', 'clubs'], ['jack', 'clubs'], ['king', 'clubs'], ['ace1', 'clubs']]]

# hand_cards = [[['2', 'clubs'], ['3', 'clubs'], ['4', 'clubs'], ['7', 'clubs'], ['10', 'clubs'], ['8', 'clubs'], ['jack', 'clubs'], ['king', 'clubs'], ['ace1', 'clubs']]]

# hand_cards = [[['2', 'clubs'], ['3', 'clubs'], ['6', 'clubs'], ['8', 'clubs'], ['9', 'clubs'], ['jack', 'clubs'], ['king', 'clubs'], ['ace1', 'clubs']]]

# hand_cards = [[['king', 'clubs'], ['ace', 'clubs']]]

# hand_cards = [[['4', 'clubs'], ['king', 'clubs'], ['ace1', 'clubs']]]

#####
# hand_cards = [[['joker', 'diamonds'], ['joker', 'diamonds'], ['joker', 'hearts']]]

# hand_cards = [[['2', 'hearts'], ['joker', None], ['joker', 'spades']]]

hand_cards = [[['joker', None], ['2', 'clubs'], ['9', 'clubs'], ['joker', 'spades'], ['joker', 'diamonds']]]

# hand_cards = [[['2', 'spades'], ['3', 'spades']], [['2', 'hearts']], [['2', 'clubs']] , [['2', 'diamonds']]]

# hand_cards = [[['2', 'spades'], ['3', 'spades']], [['2', 'hearts']], [['2', 'clubs']]]

print(hand_cards)
