from flask import Flask
from flask import render_template
from datetime import datetime
from . import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/subject/<subject>")
def subject(subject=None):
    return render_template(
        "subject.html",
        subject=subject
    )