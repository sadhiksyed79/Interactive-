# routes/feedback.py

from flask import Blueprint, request, jsonify

feedback_blueprint = Blueprint("feedback", __name__)

@feedback_blueprint.route("/", methods=["POST"])
def submit_feedback():
    mongo = request.app.mongo
    data = request.get_json()

    if not data.get("email") or not data.get("message"):
        return jsonify({"error": "Missing email or message"}), 400

    mongo.db.feedback.insert_one({
        "email": data["email"],
        "message": data["message"]
    })
    return jsonify({"message": "Feedback submitted successfully"}), 201

@feedback_blueprint.route("/", methods=["GET"])
def get_all_feedback():
    mongo = request.app.mongo
    feedbacks = list(mongo.db.feedback.find({}, {"_id": 0}))
    return jsonify(feedbacks)
