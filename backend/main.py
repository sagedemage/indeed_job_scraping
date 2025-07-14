from typing import Union
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

csv_file = "data/indeed_jobs.csv"


@app.get("/")
def read_root():
    return {"msg": "Hello World!"}


@app.get("/job-data")
def job_data():
    df = pd.read_csv(csv_file)

    # Replace NaN values with an empty string
    df = df.fillna("")

    job_titles_series = df["Job_Title"]
    companies_series = df["Company"]
    locations_series  = df["Location"]
    salary_amounts_series  = df["Salary_Amount"]
    salary_types_series  = df["Salary_Type"]
    job_types_series  = df["Job_Type"]
    links_series  = df["Link"]

    job_titles = job_titles_series.to_list()
    companies = companies_series.to_list()
    locations = locations_series.to_list()
    salary_amounts = salary_amounts_series.to_list()
    salary_types = salary_types_series.to_list()
    job_types = job_types_series.to_list()
    links = links_series.to_list()

    return {
        "job_titles": job_titles,
        "companies": companies,
        "locations": locations,
        "salary_amounts": salary_amounts,
        "salary_types": salary_types,
        "job_types": job_types,
        "links": links
    }
