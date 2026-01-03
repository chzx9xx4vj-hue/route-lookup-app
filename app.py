from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Route Lookup App is running"

@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.json
    address = data.get("address", "")
    return jsonify({
        "address": address,
        "route": "TEST"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
