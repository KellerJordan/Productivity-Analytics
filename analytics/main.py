import pickle
import sys
import argparse

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable

import numpy as np

from model import CharRNN


def main(args):
    
    # configure GPU datatype
    use_gpu = torch.cuda.is_available()
    if not use_gpu:
        raise Exception('error: CUDA library unavailable')
        
    global gpu_dtype
    gpu_dtype = torch.cuda.FloatTensor
    
    # load train, val, test data
    with open(args.data_dir+'/data.pkl', 'rb') as f:
        url_array, label_array = pickle.load(f)
    
    # partition dataset (this must sum to <50K)
    num_train = 10000
    num_val = 2000
    num_test = 8000
    
    data_train = url_array[:, :num_train, :]
    labels_train = label_array[:num_train]
    data_val = url_array[:, num_train:num_train+num_val, :]
    labels_val = label_array[num_train:num_train+num_val]
    data_test = url_array[:, num_train+num_val:num_train+num_val+num_test, :]
    labels_test = label_array[num_train+num_val:num_train+num_val+num_test]
    
    # initialize model and configure for GPU
    model = CharRNN()
    model = model.type(gpu_dtype)
    
    # train model on training data, reporting accuracy on held out validation set
    train(model, (data_train, labels_train), (data_val, labels_val),
          args.num_epochs, args.batch_size)
    
    # convert model to CPU for use on GPU-less AWS instance
    model = model.type(torch.FloatTensor)
    
    # get test accuracy
    print('Final results on held-out test set: ')
    check_accuracy(model, (data_test, labels_test), use_gpu=False)
    
    # save model to disk for use in prediction
    path = 'models/char_rnn.pk'
    print('Saving model to %s' % path)
    torch.save(model, path)


def train(model, train, val, num_epochs, batch_size):
    data_train, labels_train = train
    num_train = data_train.shape[1]
    
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = optim.Adam(model.parameters())
    
    for epoch in range(num_epochs):
        print('Beginning epoch %d / %d' % (epoch+1, num_epochs))
        check_accuracy(model, val)
        
        for i in range(num_train//batch_size):
            indices = list(range(i*batch_size, (i+1)*batch_size))
            
            X = torch.Tensor(data_train[:, indices, :])
            y = torch.LongTensor(labels_train[indices])
            X_var = Variable(X.type(gpu_dtype))
            y_var = Variable(y.type(gpu_dtype).long())
            
            scores = model(X_var)
            loss = criterion(scores, y_var)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


def check_accuracy(model, data, use_gpu=True):
    url_array, label_array = data
    num_samples = label_array.shape[0]
    
    X = torch.Tensor(url_array)
    y = torch.LongTensor(label_array)
    if use_gpu:
        X_var = Variable(X.type(gpu_dtype))
    else:
        X_var = Variable(X)
    
    model.eval()
    scores = model(X_var)
    _, preds = scores.data.cpu().max(1)
    
    num_correct = (preds == y).sum()
    
    print('accuracy: ', num_correct / num_samples)
    # further metrics to monitor due to class imbalance
    print('true pos:', label_array.sum() / num_samples)
    print('pred pos:', preds.sum() / num_samples)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', default='./datasets', type=str,
                        help='path to datasets')
    parser.add_argument('--num-epochs', default=25, type=int,
                        help='number of epochs to train for')
    parser.add_argument('--batch-size', default=16, type=int,
                        help='size of each batch of urls')
    parser.add_argument('--print-every', default=100, type=int,
                        help='number of epochs between prints')
    parser.add_argument('--use-dropout', default=False, const=True, nargs='?',
                        help='whether to use dropout in network')
    parser.add_argument('--use-batchnorm', default=False, const=True, nargs='?',
                        help='whether to use batchnorm in network')

    args = parser.parse_args()
    main(args)
