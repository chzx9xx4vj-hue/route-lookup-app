from flask import Flask, request, jsonify
import csv
import re

app = Flask(__name__)

ROUTES = []

def normalize_address(text):
    text = text.upper()
    replacements = {
        "WEST ": "W ",
        "EAST ": "E ",
        "NORTH ": "N ",
        "SOUTH ": "S ",
        "AVENUE": "AVE",
        "ROAD": "RD",
        "STREET": "ST",
        "COURT": "CT",
        "PLACE": "PL",
        "DRIVE": "DR",
        "LANE": "LN",
        "WAY": "WAY"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.strip()

def load_routes():
    global ROUTES
    with open("routes.csv", newline="") as f:
        reader = csv.DictReader(f)
        ROUTES = list(reader)

load_routes()

@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.json
    spoken = normalize_address(data.get("address", ""))

    match = re.match(r"(\\d+)\\s+(.*)", spoken)
    if not match:
        return jsonify({"error": "Invalid address"}), 400

    house = int(match.group(1))
    street = match.group(2)

    for r in ROUTES:
        if street == r["street"]:
            low = int(r["low"])
            high = int(r["high"])
            if low <= house <= high:
                return jsonify({"route": r["route"]})

    return jsonify({"route": "NOT FOUND"})

if __name__ == "__main__":
    app.run()
flask
gunicorn
street,low,high,route
W ALVARO RD,2500,2899,C002
W ALVARO RD,2900,3199,C015
W ALVARO RD,3800,4599,R037
W AVENIDA DEL PUEBLO,0,99999,C006
