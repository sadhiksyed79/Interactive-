class Config:
    # MongoDB connection details (individual components)
    MONGO_HOST = "bytexldb.com"
    MONGO_PORT = 5050
    MONGO_DBNAME = "db_43fkcgag8"
    MONGO_USERNAME = "user_43fkcgag8"
    MONGO_PASSWORD = "p43fkcgag8"

    # Full MongoDB URI built from components
    MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}"

    # Flask config
    SECRET_KEY = "supersecretkey123"
    DEBUG = True
