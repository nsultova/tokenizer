import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from corpus import Corpus
from embedding.cbow import cbow_trainingdata_for_corpus

c_full = Corpus()
c = Corpus(c_full.corpus[3000:4000])

word_count = len(c.words())
context_size = 2


[X_raw,Y_raw] = cbow_trainingdata_for_corpus(c)

X = F.one_hot(torch.tensor(X_raw), num_classes = word_count).reshape((len(X_raw), 2*context_size*word_count))
Y =  F.one_hot(torch.tensor(Y_raw), num_classes = word_count).reshape((len(Y_raw), word_count))


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        #self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(512, 128)

    def forward(self, x):
        #x = self.dropout(x)
        x = self.fc(x)
        output = F.log_softmax(x, dim=1)
        return output

    
def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    #for batch_idx, (data, target) in enumerate(train_loader):

device = torch.device("cpu")

model = Net().to(device)

optimizer = optim.Adadelta(model.parameters())

train_loader = torch.utils.data.DataLoader(X)

args = {}
epoch = 1 
train(args, model, device, train_loader, optimizer, epoch)
