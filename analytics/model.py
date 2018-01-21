import torch
import torch.nn as nn

class CharRNN(nn.Module):

    def __init__(self):
        super(CharRNN, self).__init__()
        self.lstm = nn.LSTM(51, 100, 1)
        self.final = nn.Linear(100, 2)

    def forward(self, x):
        out, h = self.lstm(x)
        return self.final(out[-1])
