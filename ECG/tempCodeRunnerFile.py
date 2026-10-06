from flask import Flask, request, jsonify, render_template
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io
import os

app = Flask(__name__)

# -------------------------------------------------
# 1. Define Model (2 CLASSES)
# -------------------------------------------------
class ECG_CNN(nn.Module):
    def __init__(self):
        super(ECG_CNN, self).__init__()

        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2,2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2,2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2,2),

            nn.AdaptiveAvgPool2d((4,4))
        )

        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128*4*4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 4)   # 4 classes
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x


# -------------------------------------------------
# 2. Load Model
# -------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

model = ECG_CNN().to(device)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "ecg_cnn_model.pth")

model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# -------------------------------------------------
# 3. Class Names
# -------------------------------------------------
#classes = ['abnormal', 'normal']
classes = ['AbnormalHB', 'Normal', 'historyofmi', 'mi']



# -------------------------------------------------
# 4. Image Transform (Same as training)
# -------------------------------------------------
transform = transforms.Compose([
    transforms.Resize((96, 96)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# -------------------------------------------------
# 5. Routes
# -------------------------------------------------

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['file']

    image = Image.open(io.BytesIO(file.read())).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    result = classes[predicted.item()]
    return jsonify({"prediction": result})


# -------------------------------------------------
# 6. Run Server
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)