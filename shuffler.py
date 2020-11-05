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
# deck = []
# letter = 1 # 'A'
# while len(deck) * 4 <= 50:
#    deck.append(card(str(letter)))
#    letter += 1

# Merge all the sublists into a single long list
tmp = []
for c in deck:
    tmp += c.makeList()
deck = tmp



def swap(a, b):
    return b, a

# https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#The_modern_algorithm
def yatesShuffle(deck):
    n = len(deck) - 2
    for i in range(0, n):
        j = random.randrange(i, len(deck))
        deck[i], deck[j] = swap(deck[i], deck[j])

# Shuffling algorithm which tries to ensure that we don't have pockets of the same card.
def shuffle(deck):
    # Actualy shuffle the deck
    yatesShuffle(deck)
    print("Post yates shuffle:\n", deck)

    # This loop finds elements next to eachother and tries to rerandomize them
    i = 1
    n = len(deck)
    # Variables which track the last index and how many times we have swapped that index
    iLast = -1
    iLastCount = 0
    while i < n:
        # If we have swapped the same index more than 10 times (say a deck is all the same card)
        # Give up on fixing the shuffle
        if iLastCount > 10:
            return

        # If there are two of the same element twice in a row
        if deck[i - 1] == deck[i]:
            # Apply a random offset to all of the swaps so they aren't exact
            offset = random.randrange(2, int(n / 10))
            if(offset == i): offset = max(offset + 2, n - 1) # If the offset is i make it bigger (maxing out at the total size of the deck)

            # Swap it to the other end of the deck (if we can)
            if((n - i) + offset < len(deck)):
                deck[i - 1], deck[(n - i) + offset] = swap(deck[i - 1], deck[(n - i) + offset])
            # If we can't swap it to the other end, swap it with the beginning
            else:
                deck[offset], deck[i] = swap(deck[offset], deck[i])

            # And scan the array again... tracking how many times we have swapped the same index
            if iLastCount and iLast == i:
                iLastCount += 1
            else:
                iLast = i
                iLastCount = 1
            # Scanning again means resetting current index to 1 (0 here since the next step increments)
            i = 0
        # Increment to the next loop itteration
        i += 1



print(len(deck))
print("Pre shuffle:\n", deck)
shuffle(deck)
print("Post shuffle:\n", deck)
print("\nHands:")

def sort(list):
    list.sort()
    return list
print(sort(deck[0:6]), sort(deck[7:13]), sort(deck[14:20]))
