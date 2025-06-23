import hou

import torch
import torch.nn as nn
from torchvision import transforms
from torchvision import datasets
from PIL import Image

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_stack = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64*7*7, 128),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.conv_stack(x)
        return self.classifier(x)

def predict():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model = CNN().to(device)

    model_path = hou.pwd().parm("model_path").eval()
    loaded_model = torch.load(model_path)
    model.load_state_dict(loaded_model['model_state_dict'])
    class_names = loaded_model['class_names']
    
    model.eval()
    
    image_path = hou.pwd().parm("img_path").eval()
    image = Image.open(image_path).convert("L")
    
    transform = transforms.Compose([
        transforms.Resize((28,28)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    
    tensor_image = transform(image)
    input_tensor = tensor_image.unsqueeze(0).to(device)
    
    with torch.inference_mode():
        output = model(input_tensor)
        prediction = torch.argmax(output).item()
    
    print(f"Prediction index: {prediction}")
    print(f"Prediction: {class_names[prediction]}")