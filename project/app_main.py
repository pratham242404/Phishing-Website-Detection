#importing required libraries

from flask import Flask, request, render_template
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from flask_cors import CORS  # Import CORS
from feature import FeatureExtraction


model = pickle.load(open("model1.pkl","rb"))


app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    print("URL is:\n", url)

    obj = FeatureExtraction(url)
    features = np.array(obj.getFeaturesList()).reshape(1, -1)

    prediction = int(model.predict(features)[0])  # Ensure JSON-serializable
    print("Prediction:", prediction)

    return jsonify({"prediction": prediction})  # -1 = Fake, 1 = Legit
if __name__ == "__main__":
    app.run(debug=True)