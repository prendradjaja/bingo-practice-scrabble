#!/usr/bin/env python3

import pickle
from collections import defaultdict

word_frequencies_300k = defaultdict(int)
for i, line in enumerate(
    open('./data/enwiki-2023-04-13.txt').read().splitlines()
):
    if i >= 300_000:
        break
    word, frequency = line.split()
    word_frequencies_300k[word] = frequency

pickle.dump(word_frequencies_300k, open('./data/word_frequencies_300k.pickle', 'wb'))
