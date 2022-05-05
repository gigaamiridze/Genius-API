from flask import Flask
import sqlite3

DATABASE_NAME = "genius.sqlite"

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except Exception as error_message:
        print(error_message)
    return conn

def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS artists (
            ID INTEGER PRIMARY KEY UNIQUE,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            age INTEGER NOT NULL,
            country TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS songs (
            ID INTEGER PRIMARY KEY UNIQUE,
            album TEXT NOT NULL,
            song_name TEXT NOT NULL,
            song_style TEXT NOT NULL,
            BPM INTEGER NOT NULL,
            upload_date TEXT NOT NULL,
            artist_id INTEGER UNIQUE NOT NULL,
            FOREIGN KEY (artist_id) REFERENCES artists (ID)
        )"""
    ]
    conn = db_connection()
    cur = conn.cursor()
    for table in tables:
        cur.execute(table)

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome..."

if __name__ == "__main__":
    create_tables()
    app.run(port=7777, debug=True)