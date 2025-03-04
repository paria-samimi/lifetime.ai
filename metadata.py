#For files (e.g., PDFs, images): Use pymediainfo, pdfminer, or Pillow.
#For custom metadata: Implement parsers or APIs to fetch metadata.
from pymediainfo import MediaInfo
file_path='/Users/pariasamimi/Documents/DM/ijerph-20-03169-with-cover'
def extract_metadata(file_path):
    media_info = MediaInfo.parse(file_path)
    metadata = {}
    for track in media_info.tracks:
        if track.track_type == "General":
            metadata["title"] = track.title
            metadata["creator"] = track.performer
            metadata["date"] = track.recorded_date
    return metadata
import psycopg2

def insert_metadata(metadata):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="saraneyo",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    query = """
    INSERT INTO metadata (title, creator, date)
    VALUES (%s, %s, %s);
    """
    cursor.execute(query, (metadata['title'], metadata['creator'], metadata['date']))
    conn.commit()
    cursor.close()
    conn.close()
