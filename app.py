import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.prediction import PredictionPipeline

os.putenv("LANG", "en_US.UTF-8")
os.putenv("LC_ALL", "en_US.UTF-8")

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)

clApp = None

@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/train", methods=["GET", "POST"])
@cross_origin()
def trainRoute():
    os.system("dvc repro")
    return "Training done successfully!"

@app.route("/predict", methods=["POST"])
@cross_origin()
def predictRoute():
    global clApp

    if clApp is None:
        clApp = ClientApp()

    data = request.get_json(silent=True)

    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    image = data["image"]
    decodeImage(image, clApp.filename)

    result = clApp.classifier.predict()
    return jsonify({
        "prediction": result["prediction"],
        "status": "success"
    })

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=8080, debug=False)