from glob import glob
from constants import *
from check import *
from copy import deepcopy
from math import ceil
from pprint import pprint

def findJoker(cards, suit=True):
    i = 0
    while i < len(cards):
        if isJoker(cards[i]):
            return jokerType(cards[i]) == suit
        i += 1
    return False

jokers = []
new_cards = []

def getJoker(suit = None):
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

def getSuit(p_cards):
    for p_card in p_cards:
        if not isJoker(p_card):
            return p_card[1]
    return 'joker'

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
        if difference > 2 or (joker_status and difference == 2):
            slice_end = i + 1
            temp = p_cards[slice_start:slice_end]
            separate_cards.append(temp)
            slice_start = slice_end
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
                if len(cards[i]) == 1:
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

def getLastSameSuitCount(p_suits, p_suit):
    counter = 0
    for suit in p_suits:
        suit_name = suit.split('-')[0]
        suit_count = suit.split('-')[1]
        suit_count = int(suit_count)
        if suit_name == p_suit:
            if suit_count > counter:
                counter = suit_count
    return counter

def groupSingleSequenceCards(p_cards):
    global sequence_and_rest_cards, four_cards
    cards = []
    single_cards = []
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
    sequence_cards = deepcopy(cards)
    separate_sequence = {}
    for sequence_card in sequence_cards:
        suit = getSuit(sequence_card)
        if suit + '-0' in separate_sequence:
            suit_count = getLastSameSuitCount(separate_sequence.keys(), suit) + 1
            separate_sequence[suit + '-' + str(suit_count)] = sequence_card
        else:
            separate_sequence[suit + '-0'] = sequence_card
    sequence_and_rest_cards['sequence'] = separate_sequence
    sequence_and_rest_cards['rest'] = deepcopy(single_cards)
    cards.append(single_cards)
    return cards

def setCards(p_cards):
	global ranks, deck
	temp_ranks = deepcopy(ranks)
	if 'ace1' in temp_ranks:
		temp_ranks['ace1'] = temp_ranks['ace']
	set_groups = {}
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
			if deck != [] and deck[1] not in set_groups[rank]['suits'] and checkIfCardRankExists(set_groups[rank]['cards'], temp_ranks[deck[0]]):
				set_groups[rank]['cards'].append(deck)
				set_groups[rank]['suits'].append(deck[1])
				deck = []
				continue
			joker = getJoker(set_groups[rank]['suits'][0])
			if joker != False:
				set_groups[rank]['cards'].append(joker)
			else:
				break
	
	return set_groups

def groupSingleSetCards(p_cards):
	global four_cards
	separate_sets = {'sets': {}, 'rest': {}}
	for rank in p_cards:
		if len(p_cards[rank]['cards']) > 1:
			if len(p_cards[rank]['cards']) > 3 and four_cards:
				four_cards = False
			separate_sets['sets'][rank] = p_cards[rank]
		else:
			separate_sets['rest'][rank] = p_cards[rank]['cards'][0]
	return separate_sets

def addDeckJokerSingleCard(p_cards):
    global jokers
    if jokers != []:
        if p_cards['rest'] == {}:
            i = 0
            limit = ceil(len(jokers) / 3)
            while i < limit:
                suit = getSuit(jokers)
                if suit + '-0' in p_cards['sequences']:
                    suit_count = getLastSameSuitCount(p_cards['sequences'].keys(), suit) + 1
                    p_cards['sequences'][suit + '-' + str(suit_count)] = jokers[:3]
                else:
                    p_cards['sequences'][suit + '-0'] = jokers[:3]
                del jokers[0:3]
                i += 1
            jokers = []
        else:
            temp_cards = deepcopy(p_cards)
            for rank in temp_cards['rest']:
                if jokers != []:
                    suit = temp_cards['rest'][rank][1]
                    suit_count = 0
                    if suit + '-0' in p_cards['sequences']:
                        suit_count = getLastSameSuitCount(p_cards['sequences'].keys(), suit) + 1
                    p_cards['sequences'][suit + '-' + str(suit_count)] = [temp_cards['rest'][rank]]
                    i = 0
                    while i < ceil(len(jokers) / 2):
                        p_cards['sequences'][suit + '-' + str(suit_count)].extend(jokers[:2])
                        del jokers[:2]
                        i += 1
                    del p_cards['rest'][rank]
                else:
                    break
    return p_cards

sequence_cards = sequenceCards(hand_cards)
sequence_cards = groupSingleSequenceCards(sequence_cards)
set_cards = setCards(sequence_and_rest_cards['rest'])
set_cards = groupSingleSetCards(set_cards)
sequence_and_set_cards = {'sequences': sequence_and_rest_cards['sequence']} | set_cards
sequence_and_set_cards = addDeckJokerSingleCard(sequence_and_set_cards)
pprint(sequence_and_set_cards)
