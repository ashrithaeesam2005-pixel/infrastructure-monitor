from flask import Blueprint, request, jsonify
import os
from utils.predict import predict_image

predict_bp = Blueprint("predict", __name__)

UPLOAD_FOLDER = "uploads"

@predict_bp.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    prediction = predict_image(filepath)

    return jsonify({
        "prediction": prediction
    })