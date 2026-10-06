import joblib
import pandas as pd
from flask import jsonify
from flask import Flask, request, render_template

print("BIOMARKER APP IS RUNNING")
app = Flask(__name__)

# load model
saved = joblib.load("random_forest_best.pkl")
model = saved["model"]

@app.route("/")
def home():
    return render_template("bio_index.html")

@app.route("/predict", methods=["POST"])
def predict():

    data = pd.DataFrame([{
        "Age": int(request.form["age"]),
        "Gender": int(request.form["gender"]),
        "Heart rate": float(request.form["heartrate"]),
        "Systolic blood pressure": float(request.form["sysbp"]),
        "Diastolic blood pressure": float(request.form["diabp"]),
        "Blood sugar": float(request.form["sugar"]),
        "CK-MB": float(request.form["ckmb"]),
        "Troponin": float(request.form["troponin"])
    }])
    probability = model.predict_proba(data)[0][1]
    print("Biometric disease probability:", probability)

    prediction = model.predict(data)[0]

    result = "Heart Disease Detected" if prediction == 1 else "Normal"

   # return render_template("bio_index.html", prediction=result)
    
    return jsonify({
    "prediction": result,
    "probability": float(probability)
})

if __name__ == "__main__":
    app.run(debug=True,port=5001)