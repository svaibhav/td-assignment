from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    "<mongo connection string goes here>"
)
db = client["testdb"]
collection = db["formdata"]

@app.route("/api")
def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)


@app.route("/", methods=["GET", "POST"])
def form_page():
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        try:
            if not name or not email:
                raise Exception("Both fields are required")

            collection.insert_one({"name": name, "email": email})

            return redirect(url_for("success_page"))

        except Exception as e:
            error = str(e)

    return render_template("form.html", error=error)


@app.route("/success")
def success_page():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)

