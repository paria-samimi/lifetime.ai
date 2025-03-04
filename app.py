from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import Session
import os
from models import Base, DatasetMetadata  # Ensure models.py is correctly imported

app = Flask(__name__)
CORS(app)  # Allow Angular to communicate with Flask

# ✅ Use Render's environment variable for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set! Please check your Render environment variables.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    Base.metadata.create_all(db.engine)

# ✅ Home Route (Prevents "Not Found" Error on Render)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Flask API is running!"})

# ✅ Submit Metadata (Single Optimized Route)
@app.route("/submit-metadata", methods=["POST"])
def submit_metadata():
    try:
        data = request.json
        with Session(db.engine) as session:
            new_metadata = DatasetMetadata(**data)
            session.add(new_metadata)
            session.commit()
        return jsonify({"message": "✅ Metadata submitted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ Retrieve Metadata List
@app.route("/get-metadata", methods=["GET"])
def get_metadata():
    try:
        with Session(db.engine) as session:
            metadata_list = session.query(DatasetMetadata).all()
            result = [{k: v for k, v in meta.__dict__.items() if k != "_sa_instance_state"} for meta in metadata_list]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=True)
