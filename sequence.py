from operator import le
from constants import *
from check import *
from copy import deepcopy


def findJoker(cards, suit=True):
    i = 0
    while i < len(cards):
        if isJoker(cards[i]):
            return jokerType(cards[i]) == suit
        i += 1
    return False


jokers = []
new_cards = []


def getJoker(suit):
    global jokers
    if ["joker", suit] in jokers:
        jokers.remove(["joker", suit])
        return ["joker", suit]
    elif ["joker", None] in jokers:
        jokers.remove(["joker", None])
        return ["joker", None]
    elif jokers != []:
        joker = jokers[0]
        del jokers[0]
        return joker
    return False

def checkIfCardRankExists(cards, rank):
    i = 0
    while i < len(cards):
        if ranks[cards[i][0]] == rank:
            return True
        i += 1
    return False


def checkIfSuitSame(p_cards, suit):
    i = 0
    while i < len(p_cards):
        if not isJoker(p_cards[i]):
            if p_cards[i][1] == suit:
                return True
        i += 1
    return False


def splitOnDifference(p_cards):
    global deck
    slice_start = 0
    slice_end = 0
    separate_cards = []
    i = 0
    joker_status = False
    while i < (len(p_cards) - 1):
        difference = ranks[p_cards[i + 1][0]] - ranks[p_cards[i][0]]
        if difference == 2:
            if deck != [] and checkIfSuitSame(p_cards, deck[1]):
                if (ranks[p_cards[i][0]] + 1) == ranks[deck[0]]:
                    p_cards.insert((i + 1), deck)
                    i += 1
                    deck = []
                    continue
            joker = getJoker(p_cards[i][1])
            if joker != False:
                p_cards.insert((i + 1), joker)
                i += 1
            else:
                joker_status = True
        if difference > 2 or joker_status:
            slice_end = i + 1
            temp = p_cards[slice_start:slice_end]
            separate_cards.append(temp)
            slice_start = i + 1
        i += 1

    if slice_end < len(p_cards):
        temp = p_cards[slice_end:]
        separate_cards.append(temp)

    # Add joker if joker free and card length is 2
    i = 0
    while i < len(separate_cards):
        if len(separate_cards[i]) == 2:
            if deck != [] and checkIfSuitSame(separate_cards[i], deck[1]):
                if ranks['ace'] == ranks[deck[0]]:
                    if checkIfCardRankExists(separate_cards[i], ranks['king']) or (checkIfCardRankExists(separate_cards[i], ranks['joker']) and checkIfCardRankExists(separate_cards[i], ranks['queen'])):
                        deck[0] = 'ace1'
                        ranks['ace1'] = ranks['king'] + 1
                        separate_cards[i].append(deck)
                        deck = []
                        continue
                if (ranks[separate_cards[i][0][0]] - 1) == ranks[deck[0]]:
                    separate_cards[i] = [deck] + separate_cards[i]
                    deck = []
                    continue
                if (ranks[separate_cards[i][1][0]] + 1) == ranks[deck[0]]:
                    separate_cards[i].append(deck)
                    deck = []
                    continue
            joker = getJoker(separate_cards[i][0][1])
            if joker != False:
                if ranks[separate_cards[i][0][0]] == ranks['ace']:
                    separate_cards[i].append(joker)
                else:
                    separate_cards[i] = [joker] + separate_cards[i]
        i += 1
    return separate_cards


def sequenceCards(cards):
    global jokers, new_cards
    i = 0
    ace_counter = 1
    while i < len(cards):
        j = 0
        new_cards.append([])
        while j < len(cards[i]):
            if isJoker(cards[i][j]):
                jokers.append(cards[i][j])
                if j == (len(cards[i]) - 1):
                    new_cards.remove([])
            else:
                if ranks[cards[i][j][0]] == ranks['ace']:
                    if checkIfCardRankExists(cards[i], ranks['king']) or (checkIfCardRankExists(cards[i], ranks['joker']) and checkIfCardRankExists(cards[i], ranks['queen'])):
                        cards[i][j][0] = 'ace' + str(ace_counter)
                        ranks['ace' + str(ace_counter)] = ranks['king'] + 1
                        ace_counter += 1
                new_cards[i].append(cards[i][j])
            j += 1
        i += 1

    copied_cards = deepcopy(new_cards)
    i = 0
    while i < len(copied_cards):
        copied_cards[i] = sorted(copied_cards[i], key=lambda x: ranks[x[0]])
        i += 1

    sequence_cards = deepcopy(copied_cards)
    i = 0
    while i < len(copied_cards):
        temp = splitOnDifference(sequence_cards[0])
        del sequence_cards[0]
        sequence_cards.extend(temp)
        i += 1

    return sequence_cards


def groupSingleCards(p_cards):
    global sequence_and_rest_cards
    cards = []
    single_cards = []
    four_cards = True
    for card in p_cards:
        if len(card) == 1:
            single_cards.append(card[0])
        else:
            if len(card) > 3 and four_cards:
                cards.append(card[:4])
                if len(card[4:]) == 1:
                    single_cards.append(card[4:][0])
                elif len(card[4:]) > 1:
                    cards.append(card[4:])
                four_cards = False
            elif len(card) > 3:
                cards.append(card)
            else:
                cards.append(card)
    sequence_and_rest_cards['sequence'] = deepcopy(cards)
    sequence_and_rest_cards['rest'] = deepcopy(single_cards)
    cards.append(single_cards)
    return cards

def setCards(p_cards):
	global ranks, deck
	temp_ranks = deepcopy(ranks)
	if 'ace1' in temp_ranks:
		temp_ranks['ace1'] = temp_ranks['ace']
	set_groups = dict()
	i = 0
	while i < len(p_cards):
		if not isJoker(p_cards[i]):
			if ranks[p_cards[i][0]] in set_groups:
				if p_cards[i][1] not in set_groups[ranks[p_cards[i][0]]]['suits']:
					set_groups[ranks[p_cards[i][0]]]['cards'].append(p_cards[i])
					set_groups[ranks[p_cards[i][0]]]['suits'].append(p_cards[i][1])
			else:
				set_groups[ranks[p_cards[i][0]]] = {'suits': [p_cards[i][1]], 'cards': [p_cards[i]]}
		i += 1

	for rank in set_groups:
		if len(set_groups[rank]['cards']) == 2:
			if deck != [] and deck[1] not in set_groups[rank]['suits']:
				set_groups[rank]['cards'].append(deck)
				deck = []
				continue
			joker = getJoker(set_groups[rank]['suits'][0])
			if joker != False:
				set_groups[rank]['cards'].append(joker)
			else:
				break
	
	return set_groups

sequence_cards = sequenceCards(hand_cards)
sequence_cards = groupSingleCards(sequence_cards)

print(sequence_cards)

print()

set_cards = setCards(sequence_and_rest_cards['rest'])
# set_cards = setCards(set_hand_cards)

print(set_cards)

