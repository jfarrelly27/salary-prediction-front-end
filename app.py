import flask
from flask import request, render_template, redirect, url_for
from flask_cors import CORS
import requests

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "seasdad(*2sffcra01^23sdet"

CORS(app)

api_url = "http://127.0.0.1:5000"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/form", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return redirect(url_for("predict"))

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        form = request.form
        age = form["age"]
        gender = form["gender"]
        country = form["country"]
        highest_deg = form["highest_deg"]
        coding_exp = form["coding_exp"]
        title = form["title"]
        company_size = form["company_size"]

        salary_predict_variables = {
            "age": age,
            "gender": gender,
            "country": country,
            "highest_deg": highest_deg,
            "coding_exp": coding_exp,
            "title": title,
            "company_size": company_size,
        }

        url = api_url + f"/predict"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                url, json=salary_predict_variables, headers=headers
            )

            if response.status_code == 200:
                prediction = response.json()
                return render_template("index.html", prediction=prediction)

            else:
                error_message = f"Failed to get prediction, server responded with status code: {response.status_code}"
                return render_template("index.html", error=error_message)

        except requests.exceptions.RequestException as e:
            error_message = "Failed to make request to prediction API."
            return render_template("index.html", error=error_message)