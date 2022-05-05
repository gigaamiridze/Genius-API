from flask import Flask, jsonify, request
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

# Artist's CRUD
@app.route("/artists", methods=["GET"])
def get_all():
    conn = db_connection()
    cur = conn.cursor()
    cursor = cur.execute("SELECT * FROM artists")
    artists = [
        dict(ID=row[0], name=row[1], surname=row[2], age=row[3], country=row[4])
        for row in cursor.fetchall()
    ]
    return jsonify(artists), 200

@app.route("/artist/<int:artist_id>", methods=["GET"])
def get_by_id(artist_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM artists WHERE ID = ?", (artist_id,))
    row = cur.fetchone()
    if row is not None:
        artist = [
            dict(ID=row[0], name=row[1], surname=row[2], age=row[3], country=row[4])
        ]
        return jsonify(artist), 200
    return {"msg": f"Artist with ID {artist_id} could not be found"}, 404

@app.route("/artist", methods=["POST"])
def create_artist():
    conn = db_connection()
    cur = conn.cursor()
    artist_data = "INSERT INTO artists (name, surname, age, country) VALUES (?, ?, ?, ?)"
    name = request.args.get("name")
    surname = request.args.get("surname")
    age = request.args.get("age")
    country = request.args.get("country")
    cur.execute(artist_data, (name, surname, age, country))
    conn.commit()
    return {"msg": f"Artist with ID {cur.lastrowid} created successfully"}, 201

@app.route("/artist/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM artists WHERE ID = ?", (artist_id,))
    conn.commit()
    return {"msg": f"Artist with ID {artist_id} has been deleted"}, 200

if __name__ == "__main__":
    create_tables()
    app.run(port=7777, debug=True)