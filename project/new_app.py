from flask import Flask, request, jsonify
import pickle
import numpy as np
import re
import tldextract

app = Flask(__name__)
model = pickle.load(open("dataset/XGBoostClassifier.pickle.dat", "rb"))

def extract_features(url):
    # Basic feature extraction according to your chart
    features = []

    features.append(1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}", url) else 0)  # Have_IP
    features.append(1 if "@" in url else 0)  # Have_At
    features.append(len(url))  # URL_Length
    features.append(url.count("/"))  # URL_Depth
    features.append(1 if "//" in url.replace("://", "", 1) else 0)  # Redirection
    features.append(1 if "https" in url.split("/")[0] else 0)  # https_Domain
    features.append(1 if "tinyurl" in url or "bit.ly" in url else 0)  # TinyURL
    features.append(1 if "-" in tldextract.extract(url).domain else 0)  # Prefix/Suffix
    features.append(1)  # DNS_Record (stub)
    features.append(0)  # Web_Traffic (stub)
    features.append(1)  # Domain_Age (stub)
    features.append(0)  # Domain_End (stub)
    features.append(0)  # iFrame (stub)
    features.append(0)  # Mouse_Over (stub)
    features.append(0)  # Right_Click (stub)
    features.append(0)  # Web_Forwards (stub)

    return np.array([features])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data.get("url")
    features = extract_features(url)
    prediction = model.predict(features)[0]
    return jsonify({"prediction": int(prediction)})

if __name__ == "__main__":
    app.run(debug=True)
