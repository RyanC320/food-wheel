# flask create web applicaiton
# jsonify convert data into JSON
# CORS allows frontend talk to backend
from flask import Flask, jsonify
from flask_cors import CORS

# create web app store in "app" variable
# CORS turn on
app = Flask(__name__)
CORS(app)

# List
foods = [
    "Pizza",
    "Sushi",
    "Burger",
    "Tacos",
    "Ramen",
    "Salad",
    "Pasta",
    "Fried Chicken"
]

# create route to get foods
@app.route("/foods")

def get_foods():
    return jsonify(foods)
# start the server running on port 5000
# debug, so that it will automatically restart when you make changes to the code
# port, so that it will run on port 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)