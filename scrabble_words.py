north_american_words = []
for line in open('./data/NWL2020.txt').read().splitlines():
    north_american_words.append(line.split()[0].lower())
