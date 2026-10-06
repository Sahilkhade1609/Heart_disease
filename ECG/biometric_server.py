from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():

    age = float(request.form.get("age",0))
    heartrate = float(request.form.get("heartrate",0))
    sysbp = float(request.form.get("sysbp",0))
    diabp = float(request.form.get("diabp",0))
    sugar = float(request.form.get("sugar",0))
    ckmb = float(request.form.get("ckmb",0))
    troponin = float(request.form.get("troponin",0))

    # Simple rule-based risk calculation
    risk = 0

    if age > 50:
        risk += 0.2
    if heartrate > 100:
        risk += 0.15
    if sysbp > 140:
        risk += 0.15
    if sugar > 180:
        risk += 0.2
    if troponin > 0.4:
        risk += 0.3

    risk = min(risk,1)

    return jsonify({
        "probability": risk
    })


if __name__ == "__main__":
    app.run(port=5001)