from game_model import Card
value_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
suit_value_array = [0,0,0,0,0]
def get_hand_rank(cards:[Card])->(int, [Card]):
    global value_array
    for c in cards:
        value_array[c.value] += 1
    checks = [check_RoyalFlush, check_StraightFlush, check_FourOfAKind, check_FullHouse, check_Flush]
    checks.extend([check_Straight, check_ThreeOfAKind, check_ThreeOfAKind, check_TwoPair, check_Pair, check_HighCard])
    for rank,check in enumerate(checks):
        rank_found, new_cards = check(cards)
        if rank_found: return (rank, new_cards)

def check_RoyalFlush(cards:[Card])->(bool, [Card]):
    if len(cards) < 5: return (False, cards)
    is_straight_flush, newCards = check_StraightFlush(cards)
    if is_straight_flush and cards[0].value == 14:
        return(True, newCards)
    return (False, newCards)
def check_StraightFlush(cards:[Card])->(bool, [Card]):#FIXME if a pair/TOAK exsists and a straight exsists, then this might fail
    if len(cards) < 5: return (False, cards)
    is_straight, newCards = check_Straight(cards)
    if is_straight:
        suit = cards[0].suit
        for c in cards[0:5]:
            if c.suit != suit:
                return (False, newCards)
    return (True, newCards)
def check_FourOfAKind(cards:[Card])->(bool, [Card]):
    if len(cards) < 4: return (False, cards)
    is_FOAK = False
    FOAK_value = 0
    for num_value in value_array:
        if num_value == 4:
            is_FOAK = True
            FOAK_value = value_array.index(4)
    if is_FOAK:
        new_cards = sorted([card for card in cards if card.value == FOAK_value], reverse=True)
        ROC = sorted([card for card in cards if card.value != FOAK_value], reverse=True)
        return (True, new_cards.extend(ROC))
    else:
        return (False, cards)

def check_FullHouse(cards:[Card])->(bool, [Card]):
    has_TOAK, cards = check_ThreeOfAKind(cards)
    if has_TOAK:
        new_cards = cards[0:3]

        has_Pair, cards = check_TwoPair(cards)
        if not has_Pair: has_Pair, cards = check_Pair(cards)
        if has_Pair:
            new_cards.extend(cards[0:2])
            ROC = [card for card in cards if card not in new_cards]
            new_cards.extend(ROC)
            return (True, new_cards)
    return (False, cards)

def check_Flush(cards:[Card])->(bool, [Card]):
    if len(cards) < 5: return (False, cards)
    global suit_value_array
    is_Flush = False
    flush_suit_value = None
    new_cards = []
    for card in cards:
        suit_value_array[card.suit.value] += 1
    for num_suit in suit_value_array:
        if num_suit >= 5:
            is_Flush = True
            flush_suit_value = suit_value_array.index(num_suit)
    if is_Flush:
        new_cards = sorted([card for card in cards if card.suit.value == flush_suit_value], reverse=True)
        ROC = sorted([card for card in cards if card.suit.value != flush_suit_value], reverse=True)
        return (True, new_cards.extend(ROC))

    return (False, cards)

def check_Straight(cards:[Card])->(bool, [Card]):
    global value_array
    if len(cards) < 5: return (False, cards)
    for index in range(len(value_array)-4):
        if value_array[index] >= 1:
            five_consecutive = True
            straight_values = [value_array[index]]
            for x in range(1,5):
                if value_array[index + x] >= 1:
                    straight_values.append(value_array[index + x])
                else:
                    five_consecutive = False
                    break
            if five_consecutive:
                new_cards = []
                for card in cards:
                    if card.value in straight_values:
                        new_cards.append(card)
                        straight_values.remove(card.value)
                new_cards.sort(reverse=True)
                new_cards.extend([card for card in cards if card not in new_cards])
                return (True, new_cards)
    if value_array[14]>=1: ##check special case where Ace is worth 1
        five_consecutive = True
        straight_values = []
        for x in range(1,5):
            if value_array[1 + x] >= 1:
                straight_values.append(value_array[1 + x])
            else:
                five_consecutive = False
                break
        if five_consecutive:
            new_cards = []
            for card in cards:
                if card.value in straight_values:
                    new_cards.append(card)
                    straight_values.remove(card.value)
            new_cards.sort(reverse=True)
            new_cards.extend([card for card in cards if card.value == 14])
            new_cards.extend([card for card in cards if card not in new_cards])
            return (True, new_cards)

    return (False, cards)


def check_ThreeOfAKind(cards:[Card])->(bool, [Card]):
    if len(cards) < 3: return (False, cards)
    global value_array
    is_TOAK = False
    TOAK_value = 0
    for num_value in value_array:
        if num_value == 3:
            is_TOAK = True
            TOAK_value = value_array.index(4)
    if is_TOAK:
        new_cards = sorted([card for card in cards if card.value == TOAK_value], reverse=True)
        ROC = sorted([card for card in cards if card.value != TOAK_value], reverse=True)
        return (True, new_cards.extend(ROC))
    else:
        return (False, cards)
def check_TwoPair(cards:[Card])->(bool, [Card]):
    if len(cards) < 4: return (False, cards)
    global value_array
    is_TwoPair = False
    num_pairs = 0
    pair_values = []
    for num_value in value_array:
        if num_value == 2:
            num_pairs += 1
            pair_values.append(value_array.index(num_value))
    if num_pairs == 2:
        new_cards = sorted([card for card in cards if card.value in pair_values], reverse=True)
        ROC = sorted([card for card in cards if card not in new_cards], reverse=True)
        return (True, new_cards.extend(ROC))
    else:
        return (False, cards)
def check_Pair(cards:[Card])->(bool, [Card]):
    if len(cards) < 2: return (False, cards)
    global value_array
    is_OnePair = False
    num_pairs = 0
    pair_values = []
    for num_value in value_array:
        if num_value == 2:
            num_pairs += 1
            pair_values.append(value_array.index(num_value))
    if num_pairs == 1:
        new_cards = sorted([card for card in cards if card.value in pair_values], reverse=True)
        ROC = sorted([card for card in cards if card.value not in pair_values], reverse=True)
        return (True, new_cards.extend(ROC))
    else:
        return (False, cards)
def check_HighCard(cards:[Card])->(bool, [Card]):
    return (True, sorted(cards, reverse=True))
