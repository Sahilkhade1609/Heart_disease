# from flask import Flask, request, jsonify, render_template
# import torch
# import torch.nn as nn
# from torchvision import transforms
# from PIL import Image
# import io
# import os

# app = Flask(__name__)

# # -------------------------------------------------
# # 1. Define Model (2 CLASSES)
# # -------------------------------------------------
# class ECG_CNN(nn.Module):
#     def __init__(self):
#         super(ECG_CNN, self).__init__()

#         self.conv_layers = nn.Sequential(
#             nn.Conv2d(3, 32, 3, padding=1),
#             nn.BatchNorm2d(32),
#             nn.ReLU(),
#             nn.MaxPool2d(2,2),

#             nn.Conv2d(32, 64, 3, padding=1),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.MaxPool2d(2,2),

#             nn.Conv2d(64, 128, 3, padding=1),
#             nn.BatchNorm2d(128),
#             nn.ReLU(),
#             nn.MaxPool2d(2,2),

#             nn.AdaptiveAvgPool2d((4,4))
#         )

#         self.fc_layers = nn.Sequential(
#             nn.Flatten(),
#             nn.Linear(128*4*4, 256),
#             nn.ReLU(),
#             nn.Dropout(0.5),
#             nn.Linear(256, 4)   # 4 classes
#         )

#     def forward(self, x):
#         x = self.conv_layers(x)
#         x = self.fc_layers(x)
#         return x


# # -------------------------------------------------
# # 2. Load Model
# # -------------------------------------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)

# model = ECG_CNN().to(device)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# model_path = os.path.join(BASE_DIR, "ecg_cnn_model.pth")

# model.load_state_dict(torch.load(model_path, map_location=device))
# model.eval()

# # -------------------------------------------------
# # 3. Class Names
# # -------------------------------------------------
# #classes = ['abnormal', 'normal']
# classes = ['AbnormalHB', 'Normal', 'historyofmi', 'mi']



# # -------------------------------------------------
# # 4. Image Transform (Same as training)
# # -------------------------------------------------
# transform = transforms.Compose([
#     transforms.Resize((96, 96)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5], [0.5])
# ])

# # -------------------------------------------------
# # 5. Routes
# # -------------------------------------------------

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"})

#     file = request.files['file']

#     image = Image.open(io.BytesIO(file.read())).convert("RGB")
#     image = transform(image)
#     image = image.unsqueeze(0).to(device)

#     with torch.no_grad():
#         outputs = model(image)
#         _, predicted = torch.max(outputs, 1)

#     result = classes[predicted.item()]
#     return jsonify({"prediction": result})


# # -------------------------------------------------
# # 6. Run Server
# # -------------------------------------------------
# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, request, jsonify, render_template
# import torch
# import torch.nn as nn
# from torchvision import transforms
# from PIL import Image
# import io
# import os

# app = Flask(__name__)

# class ECG_CNN(nn.Module):
#     def __init__(self):
#         super(ECG_CNN, self).__init__()
#         self.conv_layers = nn.Sequential(
#             nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2,2),
#             nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2,2),
#             nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(2,2),
#             nn.AdaptiveAvgPool2d((4,4))
#         )
#         self.fc_layers = nn.Sequential(
#             nn.Flatten(), nn.Linear(128*4*4, 256), nn.ReLU(), nn.Dropout(0.5), nn.Linear(256, 4)
#         )
#     def forward(self, x):
#         return self.fc_layers(self.conv_layers(x))

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = ECG_CNN().to(device)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# model.load_state_dict(torch.load(os.path.join(BASE_DIR, "ecg_cnn_model.pth"), map_location=device))
# model.eval()

# classes = ['AbnormalHB', 'Normal', 'historyofmi', 'mi']

# transform = transforms.Compose([
#     transforms.Resize((96, 96)), transforms.ToTensor(), transforms.Normalize([0.5], [0.5])
# ])

# suggestions = {
#     "Normal": {
#         "doctor": "No immediate consultation needed. Continue regular annual checkups.",
#         "diet": ["Maintain a balanced diet rich in fruits and vegetables", "Regular exercise (30 min/day)", "Keep sodium intake below 2300mg/day", "Stay hydrated with 8 glasses of water daily"]
#     },
#     "AbnormalHB": {
#         "doctor": "⚠️ Please consult a cardiologist within the next few days for further evaluation.",
#         "diet": ["Increase potassium-rich foods (bananas, spinach, sweet potatoes)", "Reduce caffeine and alcohol intake", "Eat omega-3 rich fish (salmon, mackerel) 2-3 times/week", "Avoid processed and high-sodium foods", "Consider magnesium supplements (consult doctor first)"]
#     },
#     "historyofmi": {
#         "doctor": "⚠️ Consult your cardiologist soon. Signs consistent with prior myocardial infarction detected.",
#         "diet": ["Follow a strict heart-healthy Mediterranean diet", "Limit saturated fats to less than 7% of daily calories", "Increase fiber intake (oats, beans, lentils)", "Eat antioxidant-rich berries and leafy greens daily", "Avoid trans fats and fried foods completely", "Consider CoQ10 and fish oil supplements (with doctor approval)"]
#     },
#     "mi": {
#         "doctor": "🚨 URGENT: Signs of myocardial infarction detected. Seek immediate medical attention or call emergency services.",
#         "diet": ["Follow cardiac rehabilitation dietary guidelines strictly", "Extremely low sodium diet (<1500mg/day)", "Small, frequent meals to reduce heart workload", "Increase soluble fiber (oats, flaxseed)", "Avoid all stimulants (caffeine, energy drinks)", "Anti-inflammatory foods: turmeric, ginger, green tea"]
#     }
# }

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"})
#     file = request.files['file']
#     image = Image.open(io.BytesIO(file.read())).convert("RGB")
#     image = transform(image).unsqueeze(0).to(device)

#     with torch.no_grad():
#         outputs = model(image)
#         probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
#         confidence, predicted = torch.max(probabilities, 1)

#     result = classes[predicted.item()]
#     conf_percent = round(confidence.item() * 100, 1)

#     all_probs = {classes[i]: round(probabilities[i].item() * 100, 1) for i in range(len(classes))}

#     return jsonify({
#         "prediction": result,
#         "confidence": conf_percent,
#         "all_probabilities": all_probs,
#         "suggestion": suggestions.get(result, {}),
#         "severity": "low" if result == "Normal" else ("critical" if result == "mi" else "moderate")
#     })

# if __name__ == '__main__':
#     app.run(debug=True)


    # import torch
    # import torch.nn as nn
    # import torch.nn.functional as F
    # from flask import Flask, request, jsonify, render_template
    # from torchvision import transforms
    # from PIL import Image

    # app = Flask(__name__)

    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print("Using device:", device)

    # # ---------------- MODEL ----------------
    # class ECG_CNN(nn.Module):
    #     def __init__(self):
    #         super(ECG_CNN, self).__init__()

    #         self.conv_layers = nn.Sequential(
    #             nn.Conv2d(3, 32, 3, padding=1),
    #             nn.BatchNorm2d(32),
    #             nn.ReLU(),
    #             nn.MaxPool2d(2,2),

    #             nn.Conv2d(32, 64, 3, padding=1),
    #             nn.BatchNorm2d(64),
    #             nn.ReLU(),
    #             nn.MaxPool2d(2,2),

    #             nn.Conv2d(64, 128, 3, padding=1),
    #             nn.BatchNorm2d(128),
    #             nn.ReLU(),
    #             nn.MaxPool2d(2,2),

    #             nn.AdaptiveAvgPool2d((4,4))
    #         )

    #         self.fc_layers = nn.Sequential(
    #             nn.Flatten(),
    #             nn.Linear(128*4*4, 256),
    #             nn.ReLU(),
    #             nn.Dropout(0.5),
    #             nn.Linear(256, 4)
    #         )

    #     def forward(self, x):
    #         x = self.conv_layers(x)
    #         x = self.fc_layers(x)
    #         return x

    # model = ECG_CNN().to(device)
    # model.load_state_dict(torch.load("ecg_cnn_model.pth", map_location=device))
    # model.eval()

    # print("Model loaded successfully ✅")

    # # ---------------- TRANSFORM ----------------
    # transform = transforms.Compose([
    #     transforms.Resize((96, 96)),
    #     transforms.ToTensor(),
    #     transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
    # ])

    # # IMPORTANT: must match training order
    # classes = ['AbnormalHB', 'Normal', 'historyofmi', 'mi']


    # # ---------------- ROUTES ----------------
    # @app.route("/")
    # def home():
    #     return render_template("index.html")


    # @app.route("/predict", methods=["POST"])
    # def predict():

    #     if "file" not in request.files:
    #         return jsonify({"error": "No file uploaded"}), 400

    #     file = request.files["file"]
    #     image = Image.open(file.stream).convert("RGB")
    #     image = transform(image).unsqueeze(0).to(device)

    #     with torch.no_grad():
    #         outputs = model(image)
    #         probabilities = F.softmax(outputs, dim=1)[0]

    #     confidence, predicted = torch.max(probabilities, 0)
    #     predicted_class = classes[predicted.item()]
    #     confidence_score = round(confidence.item() * 100, 2)

    #     # ---------- ALL PROBABILITIES ----------
    #     all_probs = {
    #         classes[i]: round(probabilities[i].item() * 100, 2)
    #         for i in range(len(classes))
    #     }

    #     # ---------- SEVERITY LOGIC ----------
    #     if predicted_class == "Normal":
    #         severity = "low"
    #     elif predicted_class == "AbnormalHB":
    #         severity = "moderate"
    #     elif predicted_class == "historyofmi":
    #         severity = "high"
    #     elif predicted_class == "mi":
    #         severity = "critical"
    #     else:
    #         severity = "unknown"



            

    #     # ---------- SUGGESTIONS ----------
    #     suggestions = {
    #         "Normal": {
    #             "doctor": "Your ECG appears normal. No urgent action needed.",
    #             "diet": [
    #                 "Maintain regular exercise",
    #                 "Eat balanced diet",
    #                 "Avoid excessive salt",
    #                 "Stay hydrated"
    #             ]
    #         },
    #         "AbnormalHB": {
    #             "doctor": "Irregular heartbeat detected. Consult a cardiologist for evaluation.",
    #             "diet": [
    #                 "Reduce caffeine intake",
    #                 "Avoid stress",
    #                 "Monitor blood pressure",
    #                 "Increase potassium-rich foods"
    #             ]
    #         },
    #         "historyofmi": {
    #             "doctor": "History of myocardial infarction detected. Regular cardiac checkups required.",
    #             "diet": [
    #                 "Low-fat diet",
    #                 "Avoid smoking",
    #                 "Limit cholesterol intake",
    #                 "Follow prescribed medications"
    #             ]
    #         },
    #         "mi": {
    #             "doctor": "Possible active myocardial infarction detected. Seek immediate medical attention.",
    #             "diet": [
    #                 "Strictly follow cardiologist advice",
    #                 "Avoid heavy physical activity",
    #                 "Take medications regularly",
    #                 "Maintain heart-healthy diet"
    #             ]
    #         }
    #     }

    #     return jsonify({
    #         "prediction": predicted_class,
    #         "confidence": confidence_score,
    #         "severity": severity,
    #         "all_probabilities": all_probs,
    #         "suggestion": suggestions[predicted_class]
    #     })


    # if __name__ == "__main__":
    #     app.run(debug=True)

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from flask import Flask, request, jsonify, render_template
# from torchvision import transforms
# from PIL import Image
# import requests
# from flask import jsonify

# app = Flask(__name__)

# # ---------------- DEVICE ----------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)

# # ---------------- MODEL ----------------
# class ECG_CNN(nn.Module):
#     def __init__(self):
#         super(ECG_CNN, self).__init__()

#         self.conv_layers = nn.Sequential(
#             nn.Conv2d(3, 32, 3, padding=1),
#             nn.BatchNorm2d(32),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),

#             nn.Conv2d(32, 64, 3, padding=1),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),

#             nn.Conv2d(64, 128, 3, padding=1),
#             nn.BatchNorm2d(128),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),

#             nn.AdaptiveAvgPool2d((4, 4))
#         )

#         self.fc_layers = nn.Sequential(
#             nn.Flatten(),
#             nn.Linear(128 * 4 * 4, 256),
#             nn.ReLU(),
#             nn.Dropout(0.5),
#             nn.Linear(256, 4)
#         )

#     def forward(self, x):
#         x = self.conv_layers(x)
#         x = self.fc_layers(x)
#         return x


# # ---------------- LOAD MODEL ----------------
# model = ECG_CNN().to(device)
# model.load_state_dict(torch.load("ecg_cnn_model.pth", map_location=device))
# model.eval()
# print("Model loaded successfully ✅")

# # ---------------- TRANSFORM ----------------
# transform = transforms.Compose([
#     transforms.Resize((96, 96)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
# ])

# #classes 
# classes = ['AbnormalHB', 'Normal', 'historyofmi', 'mi']

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/predict", methods=["POST"])
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["file"]
#     image = Image.open(file.stream).convert("RGB")
#     image = transform(image).unsqueeze(0).to(device)

#     # prediction time
#     with torch.no_grad():
#         outputs = model(image)
#         probabilities = F.softmax(outputs, dim=1)[0]

#     confidence, predicted = torch.max(probabilities, 0)
#     predicted_class = classes[predicted.item()]
#     confidence_score = round(confidence.item() * 100, 2)

#     # checking probabilities
#     all_probs = {
#         classes[i]: round(probabilities[i].item() * 100, 2)
#         for i in range(len(classes))
#     }
#     ecg_disease_prob = (
#     probabilities[0].item() +   # AbnormalHB
#     probabilities[2].item() +   # historyofmi
#     probabilities[3].item()     # mi
# )
#     bio_response = requests.post(
#     "http://127.0.0.1:5001/predict",
#     data={
#         "age": request.form["age"],
#         "gender": request.form["gender"],
#         "heartrate": request.form["heartrate"],
#         "sysbp": request.form["sysbp"],
#         "diabp": request.form["diabp"],
#         "sugar": request.form["sugar"],
#         "ckmb": request.form["ckmb"],
#         "troponin": request.form["troponin"]
#     }
# )

#     bio_data = bio_response.json()
#     bio_prob = bio_data["probability"]
        
#     final_prob = (0.7 * ecg_disease_prob) + (0.3 * bio_prob)

#     if final_prob > 0.6:
#         fusion_result = "Heart Disease Detected"
#     else:
#         fusion_result = "Normal"

#     #logic for prediction
#     if predicted_class == "Normal":
#         severity = "low"
#     elif predicted_class == "AbnormalHB":
#         severity = "moderate"
#     elif predicted_class == "historyofmi":
#         severity = "high"
#     elif predicted_class == "mi":
#         severity = "critical"
#     else:
#         severity = "unknown"

#     # giving suggestions
#     suggestions = {
#         "Normal": {
#             "doctor": "Your ECG appears normal. No urgent action needed.",
#             "diet": [
#                 "Maintain regular exercise",
#                 "Eat balanced diet",
#                 "Avoid excessive salt",
#                 "Stay hydrated"
#             ]
#         },
#         "AbnormalHB": {
#             "doctor": "Irregular heartbeat detected. Consult a cardiologist for evaluation.",
#             "diet": [
#                 "Reduce caffeine intake",
#                 "Avoid stress",
#                 "Monitor blood pressure",
#                 "Increase potassium-rich foods"
#             ]
#         },
#         "historyofmi": {
#             "doctor": "History of myocardial infarction detected. Regular cardiac checkups required.",
#             "diet": [
#                 "Low-fat diet",
#                 "Avoid smoking",
#                 "Limit cholesterol intake",
#                 "Follow prescribed medications"
#             ]
#         },
#         "mi": {
#             "doctor": "Possible active myocardial infarction detected. Seek immediate medical attention.",
#             "diet": [
#                 "Strictly follow cardiologist advice",
#                 "Avoid heavy physical activity",
#                 "Take medications regularly",
#                 "Maintain heart-healthy diet"
#             ]
#         }
#     }

#     # return jsonify({
#     #     "prediction": predicted_class,
#     #     "confidence": confidence_score,
#     #     "severity": severity,
#     #     "all_probabilities": all_probs,
#     #     "suggestion": suggestions[predicted_class]
#     # })
    
#     return jsonify({
#     "ecg_prediction": predicted_class,
#     "ecg_confidence": confidence_score,
#     "severity": severity,
#     "ecg_probabilities": all_probs,
#     "biometric_probability": bio_prob,
#     "fusion_result": fusion_result,
#     "suggestion": suggestions[predicted_class]
# })


# #main 
# if __name__ == "__main__":
#     app.run(debug=True)


#code without fusion 
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from flask import Flask, request, jsonify, render_template
# from torchvision import transforms
# from PIL import Image

# app = Flask(__name__)

# # ---------------- DEVICE ----------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)

# # ---------------- MODEL ----------------
# class ECG_CNN(nn.Module):
#     def __init__(self):
#         super(ECG_CNN, self).__init__()

#         self.conv_layers = nn.Sequential(
#             nn.Conv2d(3, 32, 3, padding=1),
#             nn.BatchNorm2d(32),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),

#             nn.Conv2d(32, 64, 3, padding=1),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),

#             nn.Conv2d(64, 128, 3, padding=1),
#             nn.BatchNorm2d(128),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),

#             nn.AdaptiveAvgPool2d((4, 4))
#         )

#         self.fc_layers = nn.Sequential(
#             nn.Flatten(),
#             nn.Linear(128 * 4 * 4, 256),
#             nn.ReLU(),
#             nn.Dropout(0.5),
#             nn.Linear(256, 4)
#         )

#     def forward(self, x):
#         x = self.conv_layers(x)
#         x = self.fc_layers(x)
#         return x


# # ---------------- LOAD MODEL ----------------
# model = ECG_CNN().to(device)
# model.load_state_dict(torch.load("ecg_cnn_model.pth", map_location=device))
# model.eval()
# print("Model loaded successfully ✅")


# # ---------------- TRANSFORM ----------------
# transform = transforms.Compose([
#     transforms.Resize((96, 96)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
# ])

# # IMPORTANT: must match training order
# classes = ['AbnormalHB', 'Normal', 'historyofmi', 'mi']


# # ---------------- ROUTES ----------------
# @app.route("/")
# def home():
#     return render_template("heartf.html")


# @app.route("/predict", methods=["POST"])
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["file"]
#     image = Image.open(file.stream).convert("RGB")
#     image = transform(image).unsqueeze(0).to(device)

#     # ---------------- PREDICTION ----------------
#     with torch.no_grad():
#         outputs = model(image)
#         probabilities = F.softmax(outputs, dim=1)[0]

#     confidence, predicted = torch.max(probabilities, 0)
#     predicted_class = classes[predicted.item()]
#     confidence_score = round(confidence.item() * 100, 2)

#     # ---------- ALL PROBABILITIES ----------
#     all_probs = {
#         classes[i]: round(probabilities[i].item() * 100, 2)
#         for i in range(len(classes))
#     }

#     # ---------- SEVERITY LOGIC ----------
#     if predicted_class == "Normal":
#         severity = "low"
#     elif predicted_class == "AbnormalHB":
#         severity = "moderate"
#     elif predicted_class == "historyofmi":
#         severity = "high"
#     elif predicted_class == "mi":
#         severity = "critical"
#     else:
#         severity = "unknown"

#     # ---------- SUGGESTIONS ----------
#     suggestions = {
#         "Normal": {
#             "doctor": "Your ECG appears normal. No urgent action needed.",
#             "diet": [
#                 "Maintain regular exercise",
#                 "Eat balanced diet",
#                 "Avoid excessive salt",
#                 "Stay hydrated"
#             ]
#         },
#         "AbnormalHB": {
#             "doctor": "Irregular heartbeat detected. Consult a cardiologist for evaluation.",
#             "diet": [
#                 "Reduce caffeine intake",
#                 "Avoid stress",
#                 "Monitor blood pressure",
#                 "Increase potassium-rich foods"
#             ]
#         },
#         "historyofmi": {
#             "doctor": "History of myocardial infarction detected. Regular cardiac checkups required.",
#             "diet": [
#                 "Low-fat diet",
#                 "Avoid smoking",
#                 "Limit cholesterol intake",
#                 "Follow prescribed medications"
#             ]
#         },
#         "mi": {
#             "doctor": "Possible active myocardial infarction detected. Seek immediate medical attention.",
#             "diet": [
#                 "Strictly follow cardiologist advice",
#                 "Avoid heavy physical activity",
#                 "Take medications regularly",
#                 "Maintain heart-healthy diet"
#             ]
#         }
#     }

#     return jsonify({
#         "prediction": predicted_class,
#         "confidence": confidence_score,
#         "severity": severity,
#         "all_probabilities": all_probs,
#         "suggestion": suggestions[predicted_class]
#     })


# # ---------------- MAIN ----------------
# if __name__ == "__main__":
#     app.run(debug=True)



import torch
import torch.nn as nn
import torch.nn.functional as F
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from torchvision import transforms
from PIL import Image
import requests
import mysql.connector
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "secret123"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shubham@072007",
    database="heart"
)

# ---------------- DEVICE ----------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


# ---------------- MODEL ----------------
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
            nn.Linear(256, 4)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x


# ---------------- LOAD MODEL ----------------
model = ECG_CNN().to(device)
model.load_state_dict(torch.load("ecg_cnn_model.pth", map_location=device))
model.eval()

print("Model loaded successfully.")


# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((96, 96)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])


# IMPORTANT: same order as training
classes = ['AbnormalHB', 'Normal', 'historyofmi', 'mi']


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("heartf.html")


@app.route("/predict", methods=["POST"])
def predict():

    # ---------- IMAGE CHECK ----------
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    image = Image.open(file.stream).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)


    # ---------------- ECG PREDICTION ----------------
    with torch.no_grad():
        outputs = model(image)
        probabilities = F.softmax(outputs, dim=1)[0]

    confidence, predicted = torch.max(probabilities, 0)

    predicted_class = classes[predicted.item()]
    confidence_score = round(confidence.item() * 100, 2)


    # ---------------- ALL PROBABILITIES ----------------
    all_probs = {
        classes[i]: round(probabilities[i].item() * 100, 2)
        for i in range(len(classes))
    }


    # ---------------- ECG DISEASE PROBABILITY ----------------
    ecg_disease_prob = (
        probabilities[0].item() +   # AbnormalHB
        probabilities[2].item() +   # historyofmi
        probabilities[3].item()     # mi
    )


    # ---------------- BIOMETRIC MODEL CALL ----------------
    try:

        bio_response = requests.post(
            "http://127.0.0.1:5001/predict",
            data={
                "age": request.form.get("age",0),
                "gender": request.form.get("gender",0),
                "heartrate": request.form.get("heartrate",0),
                "sysbp": request.form.get("sysbp",0),
                "diabp": request.form.get("diabp",0),
                "sugar": request.form.get("sugar",0),
                "ckmb": request.form.get("ckmb",0),
                "troponin": request.form.get("troponin",0)
            }
        )

        bio_data = bio_response.json()
        bio_prob = bio_data["probability"]

    except:
        bio_prob = 0
        print("Biometric server not running")


    # ---------------- FUSION MODEL ----------------
    final_prob = (0.7 * ecg_disease_prob) + (0.3 * bio_prob)


    if final_prob > 0.6:
        fusion_result = "Heart Disease Detected"
    else:
        fusion_result = "Normal"



    # ---------------- SEVERITY ----------------
    if predicted_class == "Normal":
        severity = "low"

    elif predicted_class == "AbnormalHB":
        severity = "moderate"

    elif predicted_class == "historyofmi":
        severity = "high"

    elif predicted_class == "mi":
        severity = "critical"

    else:
        severity = "unknown"



    # ---------------- SUGGESTIONS ----------------
    suggestions = {

        "Normal": {
            "doctor": "Your ECG appears normal. No urgent action needed.",
            "diet": [
                "Maintain regular exercise",
                "Eat balanced diet",
                "Avoid excessive salt",
                "Stay hydrated"
            ]
        },

        "AbnormalHB": {
            "doctor": "Irregular heartbeat detected. Consult a cardiologist for evaluation.",
            "diet": [
                "Reduce caffeine intake",
                "Avoid stress",
                "Monitor blood pressure",
                "Increase potassium-rich foods"
            ]
        },

        "historyofmi": {
            "doctor": "History of myocardial infarction detected. Regular cardiac checkups required.",
            "diet": [
                "Low-fat diet",
                "Avoid smoking",
                "Limit cholesterol intake",
                "Follow prescribed medications"
            ]
        },

        "mi": {
            "doctor": "Possible active myocardial infarction detected. Seek immediate medical attention.",
            "diet": [
                "Strictly follow cardiologist advice",
                "Avoid heavy physical activity",
                "Take medications regularly",
                "Maintain heart-healthy diet"
            ]
        }
    }



    # ---------------- RESPONSE ----------------
    return jsonify({

        "ecg_prediction": predicted_class,
        "ecg_confidence": confidence_score,
        "severity": severity,

        "ecg_probabilities": all_probs,

        "biometric_probability": bio_prob,
        "fusion_result": fusion_result,

        "suggestion": suggestions[predicted_class]
    })


@app.route("/heart_backend", methods=["GET", "POST"])
def heart_backend():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "userR":
            return user_register()

        elif action == "userL":
            return user_login()

    return render_template("heartf.html")

@app.route("/u_login")
def u_login():
    return render_template("login.html")

@app.route("/d_login")
def d_login():
    return render_template("d_login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("heart_backend"))


# -------- Register --------
def user_register():
    user_type = request.form.get("user_type", "").lower()
    email = request.form.get("regEmail")
    name = request.form.get("regName")
    password = request.form.get("regPass")
    cpassword = request.form.get("cregPass")

    if password != cpassword:
        flash("Password does not match")
        return redirect(url_for("heart_backend"))

    cursor = db.cursor()

    if user_type == "doctor":
        sql = "INSERT INTO doctor(type,name,email,password) VALUES (%s,%s,%s,%s)"
    else:
        sql = "INSERT INTO patient(type,name,email,password) VALUES (%s,%s,%s,%s)"

    cursor.execute(sql, (user_type, name, email, password))
    db.commit()
    cursor.close()

    flash("Registration successful")
    return redirect(url_for("heart_backend"))


# -------- Login --------
def user_login():
    user_type = request.form.get("user_type", "").lower()
    email = request.form.get("loginEmail")
    password = request.form.get("loginPassword")

    cursor = db.cursor(dictionary=True, buffered=True)

    if user_type == "doctor":
        sql = "SELECT * FROM doctor WHERE email=%s AND password=%s"
    else:
        sql = "SELECT * FROM patient WHERE email=%s AND password=%s"

    cursor.execute(sql, (email, password))
    result = cursor.fetchone()
    cursor.close()

    if result:
        if user_type == "doctor":
            return redirect(url_for("d_login"))
        else:
            return redirect(url_for("u_login"))
    else:
        flash("Invalid email or password")
    return redirect(url_for("heart_backend"))

# -------- AI Chatbot (Gemini) --------
genai.configure(api_key="AIzaSyDxexMP-WDEWzbof59M6EZO_VOxPaFHe08")
system_prompt = """
You are a professional cardiologist with expertise in heart and cardiovascular diseases.

Your role:
- Answer only questions related to the heart, blood vessels, blood pressure, and cardiovascular system.
- Provide medically accurate and scientifically correct information.
- If a question is not related to cardiology, politely say that you only answer heart and cardiovascular related questions.

Response style:
- Give clear, short, and concise answers (not very long).
- Explain medical conditions in very simple language so a non-medical person can understand.
- Avoid complex medical jargon unless necessary. If you use a medical term, briefly explain it.
- Do not format text with **bold**, asterisks, or special formatting symbols.
- Write in normal plain text.

Safety:
- Do not give dangerous or risky medical advice.
- Do not diagnose diseases with certainty.
- If symptoms sound serious (for example chest pain, fainting, severe breathlessness, irregular heartbeat, etc.), advise the person to seek medical help immediately.
- Encourage consulting a qualified doctor or cardiologist for proper diagnosis and treatment.

Tone:
- Be calm, supportive, and reassuring.
- Focus on education and awareness about heart health.
"""
chatbot_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_prompt
)
chat_session = chatbot_model.start_chat()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
         return jsonify({"error": "No message provided"}), 400
    
    user_msg = data["message"]
    try:
        response = chat_session.send_message(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print("Chatbot Error:", e)
        return jsonify({"error": "Failed to generate response"}), 500

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)