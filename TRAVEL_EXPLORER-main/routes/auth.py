from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

auth_blueprint = Blueprint('auth', __name__)


host = "bytexldb.com"
port = 5050
database = "db_43fkcgag8"
username = "user_43fkcgag8"
password = "p43fkcgag8"

connection_string = f"mongodb://{username}:{password}@{host}:{port}/{database}"
my_client = MongoClient(connection_string)
my_db = my_client[database]
login_cred = my_db['login']
feedback_rec = my_db["feedback"]


# ------------------- REGISTER -------------------
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required."}), 400

    # Check if user already exists
    existing_user = login_cred.find_one({"username": username,"email": email})

    if existing_user:
        return jsonify({"error": "Username or email already exists."}), 409

    # Hash the password and save user
    hashed_password = generate_password_hash(password)
    login_cred.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully!"}), 201


# ------------------- LOGIN -------------------
@auth_blueprint.route('/login', methods=['POST'])
def login():
    mongo = current_app.mongo
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username/email and password required."}), 400

    # Find user by username OR email
    user = login_cred.find_one({
        "$or": [{"username": username}, {"email": username}]
    })

    if user and check_password_hash(user["password"], password):
        return jsonify({
            "message": "Login successful!",
            "username": user["username"],
            "email": user["email"]
        }), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401


