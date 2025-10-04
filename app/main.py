"""Backend Server for serving job data"""

from flask import Flask
from flask import render_template
import pandas as pd

app = Flask(__name__)


def get_job_data(csv_file_path: str):
    """Get the jobs data from a CSV file"""
    df = pd.read_csv(csv_file_path)

    # Replace NaN values with an empty string
    df = df.fillna("")

    jobs_data = []
    for i in range(len(df.index)):
        jobs_data.append(df.loc[i].to_dict())

    return jobs_data


@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/jobs")
def jobs():
    jobs_csv_file = "data/indeed_jobs.csv"
    jobs_data = get_job_data(jobs_csv_file)
    return render_template(
        "jobs.html", title="Indeed Jobs", jobs_data=jobs_data
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="404 Page Not Found")
