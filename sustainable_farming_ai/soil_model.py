import torch
import torch.nn as nn

class SimpleSoilCNN(nn.Module):
    def __init__(self, num_classes=4):
        super(SimpleSoilCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 32 * 32, 100),
            nn.ReLU(),
            nn.Linear(100, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# Instantiate model and save it
model = SimpleSoilCNN()
torch.save(model, "models/soil_cnn.pt")

print("✅ Dummy soil model saved as model/soil_cnn.pt")
