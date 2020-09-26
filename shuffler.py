import random

class card:
    def __init__(self, name, count = 4):
        self.name = name
        self.count = count

    def makeList(self):
        out = []
        for i in range (0, self.count):
            out.append(self.name)
        return out

#deck = [card("A", 50)]
#deck = [card("A", 24), card("B", 26)]
#deck = [card("A", 16), card("B", 16), card("C", 17)]
deck = [card("A"), card("B"), card("C", 2), card("D", 2), card("C", 2), card("E", 10), card("F"), card("G"), card("H", 2), card("I", 2), card("J", 2), card("K", 8), card("L")]
#deck = []
#letter = 1 # 'A'
#while len(deck) * 4 <= 50:
#    deck.append(card(str(letter)))
#    letter += 1

tmp = []
for c in deck:
    tmp += c.makeList()
deck = tmp

def swap(a, b):
    tmp = a
    a = b
    b = tmp
    return a, b

def numericly(e):
    return int(e)

def sort(list):
    list.sort(key=numericly)
    return list

def yatesShuffle(deck):
    # https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#The_modern_algorithm
    n = len(deck) - 2
    for i in range(0, n):
        j = random.randrange(i, len(deck))
        deck[i], deck[j] = swap(deck[i], deck[j])

# Shuffling algorithm which tries to ensure that we don't have pockets of the same card.
def shuffle(deck):
    # Actualy shuffle the deck
    yatesShuffle(deck)

    i = 1
    iLast = []
    n = len(deck)
    while i < n:
        print(i," - ", iLast)
        if len(iLast) > 10:
            print(shuffle.count)
            shuffle.count = 0
            return
        #print(i)
        # If there are two of the same element twice in a row
        if deck[i - 1] == deck[i]:
            # Swap it to the other end of the deck (if we can)
            offset = random.randrange(2, int(n / 10))
            if((n - i) + offset < len(deck)):
                deck[i - 1], deck[(n - i) + offset] = swap(deck[i - 1], deck[(n - i) + offset])
            # If we can't swap it to the other end, swap it with the beginning
            else:
                deck[offset], deck[i] = swap(deck[offset], deck[i])
            # And scan the array again
            if len(iLast):
                if iLast[0] == i:
                    iLast.append(i)
                else:
                    iLast = [i]
            else: iLast.append(i)
            i = 0
            shuffle.count += 1
            # Bail if we have failed to find the perfect shuffle after we have retried for every card in the deck
            #shuffle.count += 1
            #if shuffle.count > len(deck):
            #    shuffle.count = 0
            #    return
        i+=1
    print(shuffle.count)
    shuffle.count = 0
# Set inital shuffle alteration count
shuffle.count = 0

#print(len(deck))
print("Pre shuffle:\n", deck)
shuffle(deck)
print("Post shuffle:\n", deck)
print(sort(deck[0:5]), sort(deck[6:11]), sort(deck[12:17]))
