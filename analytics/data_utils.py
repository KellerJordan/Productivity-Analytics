import torch
from torch.autograd import Variable
import numpy as np
import pandas as pd

num_chars = 50
seq_len = 100


# convert from character to 1-hot vector sequence
def hot2url(hot, indices):
    url = ''
    for j in range(seq_len):
        vec = hot[j]
        ind = np.argmax(vec)
        if vec[ind] > 0:
            for c in indices:
                if indices[c] == ind:
                    url += c
    return url

def url2hot(url, indices):
    hot = np.zeros((seq_len, num_chars+1))
    for j, c in enumerate(url):
        hot[j, indices.get(c, num_chars)] = 1
    return hot

# measure accuracy given ndarrays
def accuracy(model, data):
    url_array, labels_array = data
    num_samples = labels_array.shape[0]
    
    X = torch.Tensor(url_array)
    X_var = Variable(X)

    out = model(X_var)
    _, preds = out.data.max(1)
    preds = preds.numpy()
    
    if num_samples < 100:
        print(preds)
    
    return (preds == labels_array).sum() / num_samples
    print((preds == labels_array).sum() / num_samples)
