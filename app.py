from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import Session
import os
from models import Base, DatasetMetadata  # Ensure models.py is correctly imported

app = Flask(__name__)
CORS(app)  # Allow Angular to communicate with Flask

#  Use Render's environment variable for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set! Please check your Render environment variables.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    Base.metadata.create_all(db.engine)

# ✅ Only One Function for "/submit-metadata"
@app.route("/submit-metadata", methods=["POST"])
def submit_metadata():
    data = request.json
    with Session(db.engine) as session:
        new_metadata = DatasetMetadata(**data)
        session.add(new_metadata)
        session.commit()

    return jsonify({"message": "Metadata submitted successfully!"})

# ✅ Retrieve metadata list
@app.route("/get-metadata", methods=["GET"])
def get_metadata():
    with Session(db.engine) as session:
        metadata_list = session.query(DatasetMetadata).all()
        result = [meta.__dict__ for meta in metadata_list]
        for r in result:
            r.pop("_sa_instance_state", None)  # Remove SQLAlchemy internal state

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=True)
