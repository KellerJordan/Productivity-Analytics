import pandas as pd

urls_frame = pd.read_csv('datasets/data.csv')
num_examples = len(urls_frame)
chars = {}
hi = 0
for url in urls_frame['url']:
    for c in url:
        if c not in chars:
            chars[c] = 0
        chars[c] += 1

# shuffle the dataframe
urls_frame = urls_frame.sample(frac=1).reset_index(drop=True)

# we will use 1-hot vectors for the top 100 chars
char_f = sorted([(c, chars[c]) for c in chars], key=lambda v: -v[1])
char_count = 100 # hyperparameter
indices = {}
for i in range(char_count):
    indices[char_f[i][0]] = i

char2index = lambda c: indices.get(c, 100)

