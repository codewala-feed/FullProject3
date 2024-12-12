from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/register_event", methods=["GET", "POST"])
def register_event():
    return render_template("register_event.html")

app.run(debug=True)