from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import Session
import os
from models import Base, DatasetMetadata  # Ensure models.py is correctly imported

app = Flask(__name__)
CORS(app)  # Allow Angular to communicate with Flask

# Use environment variable for database URL (Render provides this)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:saraneyo@localhost:5432/postgres")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    Base.metadata.create_all(db.engine)

# Route to check if API is working
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!"})

# Route to submit metadata
@app.route("/submit-metadata", methods=["POST"])
def submit_metadata():
    data = request.json
    with Session(db.engine) as session:
        new_metadata = DatasetMetadata(
            contributors=data.get("contributors"),
            title=data.get("title"),
            institution=data.get("institution"),
            release_year=data.get("release_year"),
            doi=data.get("doi"),
            dataset_type=data.get("dataset_type"),
            version=data.get("version"),
            keywords=data.get("keywords"),
            contributor_roles=data.get("contributor_roles"),
            language=data.get("language"),
            alternate_identifiers=data.get("alternate_identifiers"),
            related_publications=data.get("related_publications"),
            timeline=data.get("timeline"),
            file_formats=data.get("file_formats"),
            dataset_size=data.get("dataset_size"),
            licensing=data.get("licensing"),
            funding_reference=data.get("funding_reference"),
            collection_location=data.get("collection_location"),
            description=data.get("description"),
            processed=data.get("What kind of processed has been done on the dataset up to now?"),
            system=data.get("What kind of system has been used for collecting the dataset?"),
            preprocessing=data.get("What kind of preprocessing has been done?"),
            numsubjects=data.get("How many subjects do we have for this study?"),
            studies=data.get("What kind of studies could users do on the dataset in the future?"),
            experiment=data.get("What was the experiment question of this study?"),
            instruments=data.get("How many instruments did subjects used in this study?"),
            Keys=data.get("What Keys are used for this study?"),
            datapoints=data.get("How many datapoints do we have for this study?"),
            bpms=data.get("What does it mean bpms?"),
            numbpms=data.get("How many bpms for this study?"),
            updown=data.get("What does it mean up and down?"),
            movements=data.get("How many movements?"),
            movementskey=data.get("How many movement per keys?"),
            prepost=data.get("What kind of music is played and how many times for each pre and post measurement?"),
            lprepost=data.get("How long was Pre and Post measurements?"),
            bow_stroke=data.get("What does it mean bow_stroke?")
        )
        session.add(new_metadata)
        session.commit()

    return jsonify({"message": "Metadata submitted successfully!"})

# Route to retrieve metadata list
@app.route("/get-metadata", methods=["GET"])
def get_metadata():
    with Session(db.engine) as session:
        metadata_list = session.query(DatasetMetadata).all()
        result = [
            {
                "id": meta.id,
                "title": meta.title,
                "doi": meta.doi,
                "institution": meta.institution,
                "release_year": meta.release_year,
                "dataset_type": meta.dataset_type,
                "description": meta.description,
                "processed": meta.processed,
                "system": meta.system,
                "preprocessing": meta.preprocessing,
                "numsubjects": meta.numsubjects,
                "studies": meta.studies,
                "experiment": meta.experiment,
                "instruments": meta.instruments,
                "Keys": meta.Keys,
                "datapoints": meta.datapoints,
                "bpms": meta.bpms,
                "numbpms": meta.numbpms,
                "updown": meta.updown,
                "movements": meta.movements,
                "movementskey": meta.movementskey,
                "prepost": meta.prepost,
                "lprepost": meta.lprepost,
                "bow_stroke": meta.bow_stroke
            }
            for meta in metadata_list
        ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
