import random
from itertools import chain, combinations
import time
import numpy as np
start=time.time()
print(start)
cards_grouping = []
ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9',
     '10', 'jack', 'queen', 'king']
suits = ['spades', 'hearts', 'diamonds', 'clubs']
def randomCard():
    return [ranks[int(random.random() * len(ranks))],
     suits[int(random.random() * len(suits))]]
def randomHand(hl):
    h = []
    while hl > 0:
        rc = randomCard()
        if rc in h:
            continue
        h.append(rc)
        hl -= 1
    return h
def lreversed(l):
    return [k for k in reversed(l)]
def rankOf(x):
    return x[0]
def nextRankOf(x):
    if x == 'king': return 'god'
    return ranks[ranks.index(x) + 1]
def suitOf(x):
    return x[1]
def scoreOf(x):
    if rankOf(x) in ['jack', 'queen', 'king']:
        return 10
    elif rankOf(x) == 'ace':
        return 1
    else:
        return ranks.index(rankOf(x)) + 1
def cards_diffrence():
    remaining=hand.copy()
    for i in hand:
        for j in cards_grouping:
            if i in j:
                remaining.remove(i)
    return remaining
def add_joker():
    remaining_cards=cards_diffrence()
    return remaining_cards
    # for i in range(len(remaining_cards)):
    #     card=remaining_cards[i]
mem = dict() # stores answer score
prev = dict() # stores previous state
cards = dict() # stores cards to get to prev state
def F(sz):
    tsz = tuple(sz)
    if tsz in mem:
        return mem[tsz]
    if sum(sz) == 0:
        mem[tsz] = 0
        return 0
    maxScore = 0
    maxPrev = None
    maxCards = None
    # Ignore one card in each set:
    for s in range(4):
        if sz[s] > 0:
            sz[s] = sz[s] - 1
            if maxScore < F(sz):
                maxScore = F(sz)
                maxPrev = tuple(sz)
                maxCards = None
            sz[s] = sz[s] + 1
    # Get ranks of last cards in each suit
    r = [None if sz[s] == 0 else hand[suitStarts[suits[s]] + sz[s] - 1][0] for s in range(4)]
    # Try to take all cards as a set except suit #i
    for i in range(0,5):
        canTake = True
        rank = None
        for j in range(0, 4):
            if j == i:
                continue
            if r[j] == None:
                canTake = False
            if rank != None and rank != r[j]:
                canTake = False
            rank = r[j]
        if canTake:
            curCards = []
            curScore = 0
            for j in range(0, 4):
                
                if j == i:
                    continue
                sz[j] = sz[j] - 1
                curCards.append([rank, suits[j]])
                curScore = curScore + scoreOf([rank, suits[j]])
            curScore = curScore + F(sz)
            if curScore > maxScore:
                maxScore = curScore
                maxPrev = tuple(sz)
                maxCards = curCards
            for j in range(0, 4):
                if j == i:
                    continue
                sz[j] = sz[j] + 1
    # Try to get streak in suit s
    for s in range(4):
        if sz[s] < 2:
            continue
        r = hand[suitStarts[suits[s]] + sz[s] - 1][0]
        curCards = [hand[suitStarts[suits[s]] + sz[s] - 1]]
        curScore = scoreOf(curCards[-1])
        for i in range(2,sz[s]+1):
            rr = hand[suitStarts[suits[s]] + sz[s] - i][0]
            if nextRankOf(rr) != r: # streak is broken
                break
            print("sdf")

            r = rr
            curCards.append(hand[suitStarts[suits[s]] + sz[s] - i])
            curScore += scoreOf(curCards[-1])
            if i >= 2:
                sz[s] -= i
                if maxScore < curScore+F(sz):
                    maxScore = curScore+F(sz)
                    maxPrev = tuple(sz)
                    maxCards = [_ for _ in reversed(curCards)]
                sz[s] += i
    mem[tsz] = maxScore
    prev[tsz] = maxPrev
    cards[tsz] = maxCards
    return maxScore
def Restore(sz):
    if sz == None or mem[sz] == 0:
        return
    Restore(prev[sz])
    if cards[sz]:
        cards_grouping.append(cards[sz])
# hand = [['5', 'spades'], ['8', 'spades'], ['jack', 'hearts'], ['5', 'hearts'], ['9', 'clubs'], ['king', 'diamonds'], ['6', 'spades'], ['9', 'spades'], ['7', 'spades'], ['2', 'clubs'], ['4', 'diamonds'], ['queen', 'hearts'], ['king', 'hearts'], ['2', 'spades'], ['7', 'clubs'], ['6', 'clubs'], ['6', 'hearts'], ['7', 'diamonds'], ['6', 'diamonds'], ['ace', 'diamonds']]
hand = [['2', 'spades'], ['5', 'hearts'], ['ace', 'diamonds'], ['4', 'diamonds'], ['7', 'diamonds'], ['king', 'diamonds'], ['2', 'clubs'], ['7', 'clubs'], ['9', 'clubs']]
hand.sort(key=lambda u: suits.index(u[1]) * 20 + ranks.index(u[0]))
suitStarts = dict()
suitStarts[suits[0]] = 0 #first card with given suit
for i in range(1, len(hand)):
    if hand[i-1][1] != hand[i][1]:
        suitStarts[hand[i][1]] = i
suitSize = dict()
last = len(hand)
for s in reversed(suits):
    suitSize[s] = last - suitStarts[s]
    last = suitStarts[s]
sz = [suitSize[s] for s in suits]
maxScore = F(sz)
#print(maxScore)
Restore(tuple(sz))
print(hand)
print()
print(cards_grouping)
print()
print(add_joker())
print(time.time()-start)