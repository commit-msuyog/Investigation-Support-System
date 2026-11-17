import sqlite3

DATABASE_NAME = "detections.db"


def get_connection():
    """One place to open the DB. WAL + timeout stops 'database is locked'
    errors when app.py is writing while the dashboard is reading."""
    conn = sqlite3.connect(DATABASE_NAME, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detections(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER,
        person_id TEXT,
        name TEXT,
        confidence REAL,
        image_path TEXT,
        detected_time TEXT
    )
    """)

    # --- migration for databases created before person_id existed ---
    columns = [row[1] for row in cursor.execute("PRAGMA table_info(detections)")]
    if "person_id" not in columns:
        cursor.execute("ALTER TABLE detections ADD COLUMN person_id TEXT")

    # Old rows: known people keep their name as person_id.
    # Old unknown rows can't be merged (no face data), so each stays separate.
    cursor.execute("""
        UPDATE detections
        SET person_id = CASE
            WHEN name = 'Unknown' THEN 'Legacy_Unknown_' || id
            ELSE name
        END
        WHERE person_id IS NULL
    """)

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_detections_person ON detections(person_id)"
    )

    conn.commit()
    conn.close()


def save_detection(
    track_id,
    name,
    confidence,
    image_path,
    detected_time,
    person_id=None,
):
    if person_id is None:
        person_id = name

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO detections
        (track_id, person_id, name, confidence, image_path, detected_time)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (track_id, person_id, name, confidence, image_path, detected_time),
    )

    conn.commit()
    conn.close()


create_database()