from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.orm import DeclarativeBase, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class DatasetMetadata(Base):
    __tablename__ = "dataset_metadata"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    contributors = mapped_column(JSON)
    title = mapped_column(String(255))
    institution = mapped_column(String(255))
    release_year = mapped_column(Integer)
    doi = mapped_column(String(100))
    dataset_type = mapped_column(String(50))
    version = mapped_column(String(10))
    keywords = mapped_column(JSON)
    contributor_roles = mapped_column(JSON)
    language = mapped_column(String(50))
    alternate_identifiers = mapped_column(JSON)
    related_publications = mapped_column(JSON)
    timeline = mapped_column(JSON)
    file_formats = mapped_column(JSON)
    dataset_size = mapped_column(String(50))
    licensing = mapped_column(String(100))
    funding_reference = mapped_column(JSON)
    collection_location = mapped_column(String(255))
    description = mapped_column(Text)
    processed = mapped_column(Text)
    system = mapped_column(Text)
    preprocessing = mapped_column(Text)
    numsubjects = mapped_column(Integer)
    studies = mapped_column(Text)
    experiment = mapped_column(Text)
    instruments = mapped_column(Text)
    Keys = mapped_column(Text)
    datapoints = mapped_column(Integer)
    bpms = mapped_column(Text)
    numbpms = mapped_column(Integer)
    updown = mapped_column(Text)
    movements = mapped_column(Text)
    movementskey = mapped_column(Text)
    prepost = mapped_column(Text)
    lprepost = mapped_column(Text)
    bow_stroke = mapped_column(Text)
    def __repr__(self):
        return f"DatasetMetadata(id={self.id}, title={self.title}, doi={self.doi})"
