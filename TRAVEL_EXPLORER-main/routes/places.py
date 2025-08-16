# routes/places.py

from flask import Blueprint, request, jsonify

places_blueprint = Blueprint("places", __name__)

@places_blueprint.route("/favorite", methods=["POST"])
def add_to_favorites():
    mongo = request.app.mongo
    data = request.get_json()

    if not data.get("email") or not data.get("place"):
        return jsonify({"error": "Missing email or place"}), 400

    mongo.db.favorites.insert_one({
        "email": data["email"],
        "place": data["place"]
    })
    return jsonify({"message": "Place added to favorites"}), 201

@places_blueprint.route("/visited", methods=["POST"])
def add_to_visited():
    mongo = request.app.mongo
    data = request.get_json()

    if not data.get("email") or not data.get("place"):
        return jsonify({"error": "Missing email or place"}), 400

    mongo.db.visited.insert_one({
        "email": data["email"],
        "place": data["place"]
    })
    return jsonify({"message": "Place marked as visited"}), 201

@places_blueprint.route("/favorites/<email>", methods=["GET"])
def get_favorites(email):
    mongo = request.app.mongo
    places = list(mongo.db.favorites.find({"email": email}, {"_id": 0}))
    return jsonify(places)

@places_blueprint.route("/visited/<email>", methods=["GET"])
def get_visited(email):
    mongo = request.app.mongo
    places = list(mongo.db.visited.find({"email": email}, {"_id": 0}))
    return jsonify(places)
