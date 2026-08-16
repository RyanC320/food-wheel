from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()  # reads variables from .env

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route("/foods")
def get_foods():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM restaurants_cache")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    names = [row["name"] for row in results]
    return jsonify(names)

if __name__ == "__main__":
    app.run(debug=True, port=5000)