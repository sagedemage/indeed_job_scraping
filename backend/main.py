"""Backend Server for serving job data"""

from flask import Flask
from flask import render_template, url_for
import pandas as pd

app = Flask(__name__)

csv_file = "data/indeed_jobs.csv"


@app.get("/hello")
def read_root():
    return {"msg": "Hello World!"}


@app.get("/job-data")
def job_data():
    df = pd.read_csv(csv_file)

    # Replace NaN values with an empty string
    df = df.fillna("")

    rows = []
    for i in range(len(df.index)):
        rows.append(df.loc[i].to_dict())

    return {"rows": rows}

@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/jobs")
def jobs():
    return render_template("jobs.html", title="Indeed Jobs", jobs_data=["Frist Job", "Second Job"])
