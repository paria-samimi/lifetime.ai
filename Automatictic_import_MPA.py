import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import json



# Connect to PostgreSQL
def get_connection():
    engine = create_engine(f'("postgresql://postgres:saraneyo@localhost:5432/postgres")')
    return engine.connect()


# Process files
filepath="/Users/pariasamimi/Downloads/MPA/MusikPhysioAnalysis"


# Process different file types
def process_file(filepath, connection):
    file_extension = os.path.splitext(filepath)[-1].lower()
    table_name = os.path.splitext(os.path.basename(filepath))[0]

    try:
        if file_extension == ".tsv":
            df = pd.read_csv("/Users/pariasamimi/Downloads/MPA/MusikPhysioAnalysis/00_VIOLIN/00_JOINT_ANGLE", sep='\t')
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
        elif file_extension == ".c3d":
            c3d = ezc3d.c3d(filepath)
            df = pd.DataFrame(c3d['data']['points'][0])
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
        elif file_extension == ".wav":
            y, sr = librosa.load(filepath, sr=None)
            df = pd.DataFrame({"Amplitude": y, "SamplingRate": [sr] * len(y)})
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
        elif file_extension == ".mat":
            mat = loadmat(filepath)
            for key, value in mat.items():
                if isinstance(value, (list, dict, pd.DataFrame)):
                    df = pd.DataFrame(value)
                    df.to_sql(f"{table_name}_{key}", con=connection, if_exists='replace', index=False)
        else:
            print(f"Unsupported file format: {file_extension}")
            return
        print(f"Processed {filepath} into table {table_name}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")


# Walk through the directory and process files
def import_data(directory):
    connection = get_connection()
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                process_file(filepath, connection)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


# Directory path containing the files
directory_path = "/Users/pariasamimi/Downloads/MPA/MusikPhysioAnalysis"
import_data(directory_path)
