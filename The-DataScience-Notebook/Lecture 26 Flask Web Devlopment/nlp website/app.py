from flask import Flask, render_template, request, redirect, session
from db import Database
import api

app = Flask(__name__)  # Create the Flask app instance
app.secret_key = 'your_secret_key'  # Needed for session management

dbo = Database()


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/preform_registerion", methods=["POST"])
def preform_registerion():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    response = dbo.insert(name, email, password)

    if response:
        return render_template("login.html", message="Registration Successful. Kindly login to proceed")
    else:
        return render_template("register.html", message="Already a member. Registration Failed")


@app.route("/perform_login", methods=["POST"])
def perform_login():
    email = request.form.get("email")
    password = request.form.get("password")

    response = dbo.search(email, password)
    if response == 1:
        session['logged_in'] = 1
        return redirect("/profile")
    else:
        return render_template("login.html", message="Invalid Credentials")


@app.route("/profile")
def profile():
    # Use session.get() to avoid KeyError if 'logged_in' is not set
    if session.get('logged_in') == 1:
        return render_template("profile.html")
    else:
        return render_template("login.html", message="Please login to proceed")


@app.route("/ner")
def ner():
    if session.get('logged_in') == 1:
        return render_template("ner.html")
    else:
        return render_template("login.html", message="Please login to proceed")


@app.route("/perform_ner", methods=["POST"])
def perform_ner():
    if session.get('logged_in') == 1:
        text = request.form.get("ner_text")
        entity_to_search = request.form.get("entity_to_search")
        
        response = api.ner(text, entity_to_search)
        
        result = ""
        for i in response['entities']:
            result += i['text'] + " : " + i['type'] + "\n"
        
        return render_template('ner.html', result=result)
    else:
        return render_template("login.html", message="Please login to proceed")


@app.route("/Abuse_Detection")
def Abuse_Detection():
    return "Abuse_Detection"


@app.route("/Sentiment_Analysis")
def sa():
    return "Sentiment Analysis"


if __name__ == "__main__":
    app.run(debug=True)
