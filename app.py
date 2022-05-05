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

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome..."

if __name__ == "__main__":
    app.run(port=7777, debug=True)