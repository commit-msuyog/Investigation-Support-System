import sqlite3

DATABASE_NAME = "detections.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detections(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        track_id INTEGER,

        name TEXT,

        confidence REAL,

        image_path TEXT,

        detected_time TEXT

    )
    """)

    conn.commit()
    conn.close()


def save_detection(
    track_id,
    name,
    confidence,
    image_path,
    detected_time
):
    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO detections
        (
            track_id,
            name,
            confidence,
            image_path,
            detected_time
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            track_id,
            name,
            confidence,
            image_path,
            detected_time
        )
    )

    conn.commit()
    conn.close()


create_database()