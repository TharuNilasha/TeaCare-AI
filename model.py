import torch
import torch.nn as nn
import torchvision.models as models

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        residual = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        out = self.relu(out)
        return out

class CustomTeaNet(nn.Module):
    def __init__(self, num_classes=8):
        super(CustomTeaNet, self).__init__()
        self.in_channels = 32
        
        self.prep = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)
        )
        
        self.layer1 = self._make_layer(32, num_blocks=2, stride=1)
        self.layer2 = self._make_layer(64, num_blocks=2, stride=2)
        self.layer3 = self._make_layer(128, num_blocks=2, stride=2)
        self.layer4 = self._make_layer(256, num_blocks=2, stride=2)
        
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.4),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(128, num_classes)
        )

    def _make_layer(self, out_channels, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for s in strides:
            layers.append(ResidualBlock(self.in_channels, out_channels, s))
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.prep(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class TeaLeafClassifier(nn.Module):
    def __init__(self, num_classes=8, backbone='resnet18', pretrained=True):
        super(TeaLeafClassifier, self).__init__()
        self.backbone_name = backbone
        
        if backbone == 'resnet18' and pretrained:
            try:
                weights = models.ResNet18_Weights.DEFAULT
                base_model = models.resnet18(weights=weights)
                in_features = base_model.fc.in_features
                base_model.fc = nn.Sequential(
                    nn.Dropout(p=0.3),
                    nn.Linear(in_features, 256),
                    nn.ReLU(inplace=True),
                    nn.Dropout(p=0.2),
                    nn.Linear(256, num_classes)
                )
                self.model = base_model
            except Exception as e:
                print(f"Failed to load ResNet18 ({e}), falling back to CustomTeaNet.")
                self.model = CustomTeaNet(num_classes=num_classes)
        else:
            self.model = CustomTeaNet(num_classes=num_classes)

    def forward(self, x):
        return self.model(x)

def build_model(num_classes=8, backbone='resnet18', pretrained=True):
    return TeaLeafClassifier(num_classes=num_classes, backbone=backbone, pretrained=pretrained)

