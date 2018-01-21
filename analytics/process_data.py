import pandas as pd
import numpy as np
import sys
import pickle
import argparse


def main(args):
    
    # load dataframe from csv
    urls_frame = pd.read_csv('datasets/data.csv')
    # subsample to balance good/bad classes
    urls_frame = urls_frame.iloc[:151286]
    # shuffle and subsample
    urls_frame = urls_frame.sample(frac=1).reset_index(drop=True)
    with open('datasets/df.pkl', 'wb') as f:
        pickle.dump(urls_frame, f)
    urls_frame = urls_frame.iloc[:args.num_samples]
    # truncate urls
    urls_frame = urls_frame.applymap(lambda v: v[:args.seq_len])

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
    for i in range(args.num_chars):
        indices[char_f[i][0]] = i
    
    # embed characters into numpy array
    url_array = np.zeros((args.seq_len, args.num_samples, args.num_chars+1))
    for i, url in enumerate(urls_frame['url']):
        for j, c in enumerate(url):
            url_array[j, i, indices.get(c, args.num_chars)] = 1
    
    # pickle data and index table
    with open('datasets/data.pkl', 'wb') as f:
        pickle.dump((url_array, label_array), f)
    
    with open('datasets/indices.pkl', 'wb') as f:
        pickle.dump(indices, f)


if __name__ == '__main__':
    # dataset size hyperparameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-samples', default=50000, type=int,
                        help='number of samples to fetch from dataset')
    parser.add_argument('--seq-len', default=100, type=int,
                        help='max sequence length to truncate to')
    parser.add_argument('--num-chars', default=50, type=int,
                        help='number of frequent characters to distinguish between')
    args = parser.parse_args()
    main(args)
