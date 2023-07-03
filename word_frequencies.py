import pickle
import time

'''
word_frequencies_300k:
- A dictionary of the top 300K words in English by number of occurrences in English Wikipedia.
- Words are stored in lowercase.
- It is a defaultdict (so it can be queried for nonexistent words, which have 0 occurrences).
- It is ordered (requires Python 3.7+), so list(word_frequencies_300k)[0] is the most common word.
'''

word_frequencies_300k = pickle.load(open('./data/word_frequencies_300k.pickle', 'rb'))
