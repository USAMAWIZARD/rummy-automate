from constants import *

def isJoker (card):
    if 'joker' in card[0]: return True
    return False

def jokerType (card):
    return card[1] == None      # True for real joker and False for suit joker

def isValidSequence (cards):
    pure = True
    
    #   Check if group length is >= 3
    if len(cards) < 3:
        return False, None

    #   Check if all card suit is same
    i = 0
    while i < len(cards) - 1:
        # if cards[i][1] != cards[i + 1][1] and not isJoker(cards[i]) and not isJoker(cards[i + 1]):
        if not isJoker(cards[i]):
            if cards[i][1] != cards[i + 1][1] and not isJoker(cards[i + 1]):
                return False, None
        i += 1

    #   Check if joker has suit or not if without suit then only sequence if with suit but if it's count is more than 1 then return only sequence else pure sequence
    joker_counter = 0
    for card in cards:
        if isJoker(card):
            if not jokerType(card):
                if card[1] != cards[0][1]:
                    pure = False
                    break
                else:
                    if joker_counter >= 1:
                        pure = False
                        break
                    joker_counter += 1
                    pure = True
            else:
                pure = False
                break

    #   Check if first ace card is valid
    if ranks[cards[0][0]] == ranks['ace']:
        if ranks[cards[1][0]] != ranks['2'] and not isJoker(cards[1]):
            return False, None

    #   Check if last ace card is valid
    old_ace = ranks['ace']
    if ranks[cards[len(cards) - 1][0]] == ranks['ace']:
        ranks['ace'] = ranks['king'] + 1
        if ranks[cards[len(cards) - 2][0]] != ranks['king'] and not isJoker(cards[len(cards) - 2]):
            ranks['ace'] = old_ace
            return False, None

    #   Check if card ranks are in sequence
    joker_rank_counter = 0
    old_joker = ranks['joker']
    
    #   Find first number
    njoker_index = 0
    i = 0
    while i < len(cards):
        if not isJoker(cards[i]):
            joker_rank_counter = ranks[cards[i][0]] - 1
            njoker_index = i
            break
        i += 1
    
    #   Fill left side of first number jokers
    i = njoker_index - 1
    while i > -1:
        if isJoker(cards[i]):
            cards[i][0] = 'joker' + str(i)
            ranks['joker' + str(i)] = joker_rank_counter
        joker_rank_counter -= 1
        i -= 1
    
    #   Fill right side of first number jokers
    i = njoker_index
    while i < len(cards):
        if isJoker(cards[i]):
            cards[i][0] = 'joker' + str(i)
            ranks['joker' + str(i)] = joker_rank_counter
            if i != 0 and not isJoker(cards[i - 1]):
                joker_rank = ranks[cards[i - 1][0]]
                ranks['joker' + str(i)] = joker_rank + 1
                joker_rank_counter = joker_rank + 1
            joker_rank_counter += 1
        i += 1
    
    #   Check if all cards are in sequence
    i = 0
    while i < len(cards) - 1:
        if ranks[cards[i + 1][0]] != (ranks[cards[i][0]] + 1):
            ranks['ace'] = old_ace
            ranks['joker'] = old_joker
            return False, None
        i += 1
    ranks['ace'] = old_ace
    ranks['joker'] = old_joker
    return True, pure


def isValidSet (cards):
    #   Check group's length is 3 or 4 only
    if len(cards) < 3:
        return False

    #   Find first number
    set_first_number = 0
    i = 0
    while i < len(cards):
        if not isJoker(cards[i]):
            set_first_number = ranks[cards[i][0]]
            break
        i += 1
    
    #   Check if all cards have same ranks
    for card in cards:
        if not isJoker(card) and ranks[card[0]] != set_first_number:
            return False

    #   Check if all cards have unique suits
    set_suits = []
    for card in cards:
        if isJoker(card): continue
        if set_suits != [] and card[1] in set_suits:
            return False
        set_suits.append(card[1])

    return True


# hand_cards = [['4', 'spades'], ['joker', 'spades'], ['4', 'clubs'], ['joker', 'spades']]
# hand_cards = [['joker', 'spades'], ['ace', 'spades'], ['joker', 'spades'], ['3', 'spades'], ['joker', 'spades']]

# response = isValidSequence(hand_cards)
# response = isValidSet(hand_cards)

# print(response)

