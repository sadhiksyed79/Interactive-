from flask import Flask, render_template, session, redirect, url_for
from flask_pymongo import PyMongo
from routes.auth import auth_blueprint
from routes.places import places_blueprint
from routes.feedback import feedback_blueprint
from config import Config
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
app = Flask(__name__)
app.config.from_object(Config)

# Required for session handling (logout, login session, etc.)
app.secret_key = 'your_super_secret_key_here'  # Change this to something secure!

# Set up MongoDB with Flask-PyMongo
mongo = PyMongo(app)
app.mongo = mongo

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
app.register_blueprint(places_blueprint, url_prefix="/api/places")
app.register_blueprint(feedback_blueprint, url_prefix="/api/feedback")




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

# === Frontend Routes ===

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/places")
def places():
    return render_template("places.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/logout")
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('index'))  # Redirect to home page

# Optional test route
@app.route("/test-db")
def test_db():
    return "Direct test route is working!"


@app.route('/api/feedback/submit', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    rating = data.get('rating')
    feedback = data.get('feedback')
    username = data.get('username', 'Guest')

    if not rating or not feedback:
        return jsonify({"error": "Rating and feedback required."}), 400

    feedback_rec.insert_one({
        "username": username,
        "rating": int(rating),
        "feedback": feedback,
        "timestamp": datetime.utcnow()
    })

    return jsonify({"message": "Feedback submitted successfully!"}), 200

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
