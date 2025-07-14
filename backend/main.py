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

    rows = []
    for i in range(len(df.index)):
        rows.append(df.loc[i])

    return { "rows": rows }
