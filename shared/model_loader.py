import os
import joblib
import torch
import torch.nn as nn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- ECG CNN Architecture ----------------
class ECG_CNN(nn.Module):
    def __init__(self):
        super(ECG_CNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.AdaptiveAvgPool2d((4, 4))
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 4)  # 4 classes: AbnormalHB, Normal, historyofmi, mi
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

# ---------------- X-Ray SimpleCNN Architecture ----------------
class XRay_CNN(nn.Module):
    def __init__(self):
        super(XRay_CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 16 * 16, 2)  # 2 classes: Normal, Pneumonia/Cardiomegaly

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 32 * 16 * 16)
        x = self.fc1(x)
        return x

# ---------------- Model Loading Helpers ----------------
def load_biomarker_model():
    """Loads Random Forest model for Clinical Biomarkers."""
    paths = [
        os.path.join(BASE_DIR, "shared", "models", "random_forest_best.pkl"),
        os.path.join(BASE_DIR, "troponin-heart", "random_forest_best.pkl"),
        os.path.join(BASE_DIR, "XRAY", "random_forest_best.pkl")
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                saved = joblib.load(p)
                model = saved["model"] if isinstance(saved, dict) and "model" in saved else saved
                print(f"[Model Loader] Biomarker Random Forest model loaded from: {p}")
                return model
            except Exception as e:
                print(f"[Model Loader] Failed to load biomarker model from {p}: {e}")
    raise FileNotFoundError("Biomarker Random Forest model file (random_forest_best.pkl) not found!")

def load_ecg_model():
    """Loads PyTorch CNN model for ECG classification."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ECG_CNN().to(device)
    paths = [
        os.path.join(BASE_DIR, "shared", "models", "ecg_cnn_model.pth"),
        os.path.join(BASE_DIR, "ECG", "ecg_cnn_model.pth"),
        os.path.join(BASE_DIR, "ECG", "ecg_model.pth")
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                model.load_state_dict(torch.load(p, map_location=device))
                model.eval()
                print(f"[Model Loader] PyTorch ECG CNN model loaded from: {p}")
                return model, device
            except Exception as e:
                print(f"[Model Loader] Failed to load ECG model from {p}: {e}")
    print("[Model Loader Warning] ECG PyTorch model file not loaded, returning initialized eval model.")
    model.eval()
    return model, device

def load_xray_model():
    """Loads PyTorch CNN model for Chest X-Ray diagnostic analysis."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = XRay_CNN().to(device)
    paths = [
        os.path.join(BASE_DIR, "shared", "models", "xray_cnn.pth"),
        os.path.join(BASE_DIR, "XRAY", "xray_cnn.pth")
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                model.load_state_dict(torch.load(p, map_location=device))
                model.eval()
                print(f"[Model Loader] PyTorch X-Ray CNN model loaded from: {p}")
                return model, device
            except Exception as e:
                print(f"[Model Loader] Failed to load X-Ray model from {p}: {e}")
    print("[Model Loader Warning] X-Ray PyTorch model file not loaded, returning initialized eval model.")
    model.eval()
    return model, device
