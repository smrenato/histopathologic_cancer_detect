from torch import nn


class VGG16Extractor(nn.Module):
    def __init__(self, model):
        super(VGG16Extractor, self).__init__()
        self.features = model.features
        self.pooling = model.avgpool
        self.flatten = nn.Flatten()
        self.fc = model.classifier[0]

    def forward(self, x):
        out = nn.Sequential(self.features, self.pooling, self.flatten, self.fc)
        out = out(x)
        return out
