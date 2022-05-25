
from copy import deepcopy
from constants import print, show

ui_cards =     [[['5', 'diamonds'],
                 ['8', 'diamonds'],
                 ['jack', 'diamonds'],
                 ['ace', 'joker']],
                [['8', 'clubs'], ['9', 'clubs']],
                [['8', 'hearts'], ['9', 'hearts'], ['10', 'hearts']],
                [['2', 'spades'], ['4', 'spades'], ['5', 'spades']],
                [['5', 'hearts'], ['10', 'hearts']]]

# valid_cards = [[['2', 'spades'], ['8', 'diamonds'], ['10', 'hearts'], ['jack', 'diamonds']],
#                 [['ace', 'joker'], ['8', 'clubs'], ['9', 'clubs']],
#                 [['8', 'hearts'], ['9', 'hearts'], ['10', 'hearts']],
#                 [['4', 'spades'], ['5', 'spades']],
#                 [['5', 'diamonds'], ['5', 'hearts']]]

valid_cards = {'rest': {2: ['2', 'spades'], 8: ['8', 'diamonds'], 10: ['10', 'hearts'], 11: ['jack', 'diamonds']},
                'sequences': {'clubs-0': [['ace', 'joker'], ['8', 'clubs'], ['9', 'clubs']],
                            'hearts-0': [['8', 'hearts'], ['9', 'hearts'], ['10', 'hearts']],
                            'spades-0': [['4', 'spades'], ['5', 'spades']]},
                'sets': {5: {'cards': [['5', 'diamonds'], ['5', 'hearts']],
                            'suits': ['diamonds', 'hearts']}}}

def findMaximumCardNumber(p_ui_cards, p_sequence):
    max_cards = []
    for i, cards in enumerate(p_ui_cards):
        card_counter = 0
        max_card = [0, []]
        for j, card in enumerate(cards):
            for k, sequence_card in enumerate(p_sequence):
                if sequence_card == card:
                    card_counter += 1
                    max_card[0] = card_counter
                    max_card[1].append([i, j])
        if max_card[0] != 0:
            if max_cards != [] and max_cards[0] < max_card[0]:
                max_cards = max_card
            elif max_cards == []:
                max_cards = max_card
    return max_cards

# def splitCards(p_ui_cards, p_valid_cards, position)


def minimumSwaps(p_ui_cards, p_valid_cards):
    # """
    for sequence in p_valid_cards['sequences']:
        position = findMaximumCardNumber(p_ui_cards, p_valid_cards['sequences'][sequence])
        show(position)
    # """

    """
    for set in p_valid_cards['sets']:
        position = findMaximumCardNumber(p_ui_cards, p_valid_cards['sets'][set]['cards'])
        show(position)
    """

    return p_ui_cards


# print - ui_cards
response = minimumSwaps(deepcopy(ui_cards), valid_cards)
# print - response


