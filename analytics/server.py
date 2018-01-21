from bottle import post, run, request
import pickle
import json

import torch
from torch.autograd import Variable

import numpy as np


def load_model():
    global indices
    global model
    
    with open('datasets/indices.pkl', 'rb') as f:
        indices = pickle.load(f)
    
    model = torch.load('models/char_rnn.pk')
    model = model.type(torch.FloatTensor)

@post('/predict')
def index():
    urls = request.json['urls']
    print(urls)
    predictions = predict(urls)
    return predictions

def predict(urls):
    global indices
    global model
    
    # hyperparameters -- optimally would have some way to share this with process_data.py
    num_samples = len(urls)
    seq_len = 100
    num_chars = 50
    
    # truncate to 100 length
    urls = [url[:seq_len] for url in urls]
    
    # embed characters into numpy array (transition later to scipy sparse matrix)
    url_array = np.zeros((seq_len, num_samples, num_chars+1))
    for i, url in enumerate(urls):
        for j, c in enumerate(url):
            url_array[j, i, indices.get(c, num_chars)] = 1
    
    # use trained model to make predictions about maliciousness of urls
    X = torch.Tensor(url_array)
    X_var = Variable(X)
    _, pred = model(X_var).max(1)
    pred = pred.data.numpy().tolist()
    print(pred)
    
    return json.dumps(pred)


if __name__ == '__main__':
    load_model()
    run(host='', port=8080)
