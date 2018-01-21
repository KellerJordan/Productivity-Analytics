import pandas as pd
import numpy as np
import sys
import pickle
import argparse


def main():

    # dataset size hyperparameters
    num_samples = 50000
    seq_len = 100
    num_chars = 50

    # load dataframe from csv, shuffle, subsample, and truncate urls
    urls_frame = pd.read_csv('datasets/data.csv')
    urls_frame = urls_frame.sample(frac=1).reset_index(drop=True)
    urls_frame = urls_frame.iloc[:num_samples]
    urls_frame = urls_frame.applymap(lambda v: v[:seq_len])

    # convert good/bad to 0/1
    labels = [int(label == 'bad') for label in urls_frame['label']]
    label_array = np.array(labels)

    # create dict of char frequencies
    chars = {}
    for url in urls_frame['url']:
        for c in url:
            if c not in chars:
                chars[c] = 0
            chars[c] += 1

    # index 50 most frequent characters for one-hot vectorization
    char_f = sorted([(c, chars[c]) for c in chars], key=lambda v: -v[1])
    indices = {}
    for i in range(num_chars):
        indices[char_f[i][0]] = i
    
    # embed characters into numpy array (transition later to scipy sparse matrix)
    url_array = np.zeros((seq_len, num_samples, num_chars+1))
    for i, url in enumerate(urls_frame['url']):
        for j, c in enumerate(url):
            url_array[j, i, indices.get(c, num_chars)] = 1
    
    # pickle data and index table
    with open('datasets/data.pkl', 'wb') as f:
        pickle.dump((url_array, label_array), f)
    
    with open('datasets/indices.pkl', 'wb') as f:
        pickle.dump(indices, f)


if __name__ == '__main__':
    # TODO: add command line arguments
    main()
