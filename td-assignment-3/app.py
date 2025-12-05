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


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    error = None

    if request.method == "POST":
        item_name = request.form.get("name")

        try:
            if not item_name:
                raise Exception("Item name is required")

            # Here you would typically insert the item into a database
            # For demonstration, we just return a success message
            return jsonify({"message": f"Item '{item_name}' added successfully!"})

        except Exception as e:
            error = str(e)

    return render_template("todo.html", error=error)

@app.route("/", methods=["GET", "POST"])
def form_page():
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        try:
            if not name or not description:
                raise Exception("Both fields are required")

            collection.insert_one({"name": name, "description": description})

            return redirect(url_for("success_page"))

        except Exception as e:
            error = str(e)

    return render_template("todo.html", error=error)


@app.route("/success")
def success_page():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)

