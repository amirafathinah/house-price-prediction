from pathlib import Path

import joblib
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "house_price_model.joblib"

model = joblib.load(MODEL_PATH)

# Ganti dengan origin frontend saat sudah di-deploy.
# Untuk tes lokal, kita izinkan localhost.
CORS(app, origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500"
])

FEATURES = [
    "Kamar Tidur",
    "Kamar Mandi",
    "Garasi",
    "Luas Tanah",
    "Luas Bangunan",
    "Kecamatan"
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "House Price Prediction API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request harus berupa JSON object."
        }), 400

    try:
        numeric_features = [
            "Kamar Tidur",
            "Kamar Mandi",
            "Garasi",
            "Luas Tanah",
            "Luas Bangunan"
        ]

        row = {}

        for feature in numeric_features:
            value = float(data[feature])

            if not pd.notna(value):
                raise ValueError("Nilai tidak valid.")

            row[feature] = value

        kecamatan = data["Kecamatan"]

        if not isinstance(kecamatan, str) or not kecamatan.strip():
            raise ValueError("Kecamatan harus diisi.")

        row["Kecamatan"] = kecamatan.strip()

        X = pd.DataFrame([row], columns=FEATURES)
        prediction = float(model.predict(X)[0])

        return jsonify({
            "predicted_price": prediction,
            "formatted_price": f"Rp {prediction:,.0f}"
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Periksa kembali semua input."
        }), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
