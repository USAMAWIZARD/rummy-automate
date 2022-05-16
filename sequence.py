from itertools import count
from constants import *
from check import *
from copy import deepcopy

def findJoker(cards, suit = True):
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
		return jokers[0]
	return False

def checkIfCardRankExists(cards, rank):
	i = 0
	while i < len(cards):
		if ranks[cards[i][0]] == rank:
			return True
		i += 1
	return False

def splitOnDifference(p_cards):
	slice_start = 0
	slice_end = 0
	separate_cards = []
	i = 0
	joker_status = False
	while i < (len(p_cards) - 1):
		difference = ranks[p_cards[i + 1][0]] - ranks[p_cards[i][0]]
		if difference == 2:
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
		copied_cards[i] = sorted(copied_cards[i], key = lambda x: ranks[x[0]])
		i += 1

	sequence_cards = deepcopy(copied_cards)
	i = 0
	while i < len(copied_cards):
		temp = splitOnDifference(sequence_cards[0])
		del sequence_cards[0]
		sequence_cards.extend(temp)
		i += 1
	
	return sequence_cards

# hand_cards = [['joker', 'spades'], ['4', 'spades'], ['joker', 'spades'], ['2', 'spades'], ['8', 'clubs'], ['ace', 'spades'], ['joker', 'spades']]
# hand_cards = [[['8', 'diamonds'], ['queen', 'diamonds']], [['4', 'clubs'], ['king', 'clubs'], ['ace', 'clubs']], [['8', 'hearts'], ['10', 'hearts'], ['5', 'hearts'], ['ace', 'hearts']], [['joker', 'spades'], ['8', 'spades'], ['queen', 'spades']], [['joker', None]]]
# hand_cards = [[['8', 'diamonds'], ['10', 'diamonds']], [['4', 'clubs'], ['king', 'clubs'], ['ace', 'clubs']], [['8', 'hearts'], ['10', 'hearts'], ['5', 'hearts'], ['ace', 'hearts']], [['joker', 'spades'], ['8', 'spades'], ['queen', 'spades']], [['joker', None]]]
hand_cards = [[['8', 'diamonds'], ['10', 'diamonds']], [['4', 'clubs'], ['king', 'clubs'], ['ace1', 'clubs']], [['8', 'hearts'], ['10', 'hearts'], ['5', 'hearts'], ['ace', 'hearts']], [['joker', 'spades'], ['8', 'spades'], ['queen', 'spades']], [['joker', None]]]
# print()
print(hand_cards)
print()
sorted_cards = sequenceCards(hand_cards)

# sorted_cards = splitOnDifference(hand_cards[0])
# print()
print(sorted_cards)
# print()
