            if (cards.Count < 3)
                return false;

            // A run can only consist of cards with the same suit (or joker with the matching color)
            Card representiveCard = cards.GetFirstCard();
            if (representiveCard == null)
                return false;

            foreach (var card in cards)
            {
                if (!card.IsJoker())
                {
                    if (card.Suit != representiveCard.Suit)
                        return false;
                }
                else
                {
                    if (card.Color != representiveCard.Color)
                        return false;
                }
            }

            for (int i = 0; i < cards.Count - 1; i++)
            {
                // Ace can be the start of a run
                if (i == 0 && cards[i].Rank == Card.CardRank.ACE)
                {
                    // Run is only valid if next card is a TWO or a JOKER
                    if (cards[i + 1].Rank != Card.CardRank.TWO && !cards[i + 1].IsJoker())
                        return false;
                }
                // otherwise, rank has to increase by one
                else if (cards[i + 1].Rank != cards[i].Rank + 1 && !cards[i].IsJoker() && !cards[i + 1].IsJoker())
                    return false;
            }
            return true;
        }

        public bool CanFit(Card card, out Card Joker)
        {
            Joker = null;

            if (card.IsJoker())
                return card.Color == Color && Cards.Count < 14;

            var jokers = Cards.Where(c => c.IsJoker());

            if (card.Suit != Suit || (Cards.Count == 14 && !jokers.Any()))
                return false;

            // Check whether the new card replaces a joker
            foreach (var joker in jokers)
            {
                var jokerRank = CardUtil.GetJokerRank(Cards, Cards.IndexOf(joker));
                if (jokerRank == card.Rank)
                {
                    Joker = joker;
                    return true;
                }
            }