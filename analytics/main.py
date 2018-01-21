import torch
import torch.nn as nn
import torch.optim as optim

import pickle
import sys
import argparse


def main():

    # load data and indices
    with open('datasets/data.pkl', 'rb') as f:
        url_array, label_array = pickle.load(f)

    with open('datasets/indices.pkl', 'rb') as f:
        indices = pickle.load(f)

    print(url_array.shape)


def train():
    pass




def row2vars(r):
    in_tensor = url2tensor(url, indices)
    out_tensor = torch.LongTensor(np.array([label]))
    return Variable(in_tensor), Variable(out_tensor)


if __name__ == '__main__':
    main()
