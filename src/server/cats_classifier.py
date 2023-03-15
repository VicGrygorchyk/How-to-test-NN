import torch
import torch.nn as nn


classes = {
    0: 'cat',
    1: 'dog'
}


class ImageNet(nn.Sequential):

    def __init__(self):
        super().__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.fc1 = nn.Linear(3 * 3 * 64, 16)
        self.fc2 = nn.Linear(16, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(out.size(0), -1)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        return out


def load_model(model_save_path):
    model_params = torch.load(model_save_path, map_location=torch.device('cpu'))
    model_loaded = ImageNet()
    model_loaded.load_state_dict(model_params)
    return model_loaded


def get_pred(model, image):
    with torch.no_grad():
        image = image.unsqueeze(0)
        pred = model(image)
        _, result = torch.max(pred, 1)

    print(f'Predicted {result}.')
    print(f'Predicted {classes[result.item()]}.')
    return classes[result.item()]
