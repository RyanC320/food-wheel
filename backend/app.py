from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
import os
from flask import request

load_dotenv()  # reads variables from .env

app = Flask(__name__)
CORS(app)

# connect to the MYSQL database using the credentials from the .env file
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# @app.route, if user visits /foods, immediately call below function
@app.route("/foods")
def get_foods():
    # once connected, fet(access) the data from the database and return it as a JSON response
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) # create variable cursor to execute SQL instructions
    cursor.execute("SELECT name FROM restaurants_cache") # instruction to mySQL
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    names = [row["name"] for row in results]
    return jsonify(names)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

# @app.route, if users visits /feedback, immediately call below function
@app.route("/feedback", methods=["POST"])
def add_feedback():
    data = request.get_json() #read data from frontend in json format
    restaurant_name = data.get("restaurant_name")
    liked = data.get("liked")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (restaurant_name, liked) VALUES (%s, %s)",
        (restaurant_name, liked)
    )
    conn.commit() #Save insert data to database
    cursor.close()
    conn.close()

    return jsonify({"status": "success"}) #telling fronted its successful inserted

# Save record every time the wheel spin
@app.route("/spin", methods=["POST"])
def save_spin():
    data = request.get_json()
    restaurant_name = data.get("restaurant_name")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO spins (restaurant_name) VALUES (%s)",
        (restaurant_name,)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

# Returns the 10 most recent spins
@app.route("/history")
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT restaurant_name, spun_at FROM spin_history ORDER BY spun_at DESC LIMIT 10")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)