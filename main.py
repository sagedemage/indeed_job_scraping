"""Indeed Job Scraper Program"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchDriverException
import pandas as pd
from pandas import DataFrame
import time
import configparser
import logging
import os


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    query = config["DEFAULT"]["Query"]
    location = config["DEFAULT"]["Location"]

    date_posted_in_days = config["DEFAULT"]["DatePostedInDays"]

    us_indeed_url = "https://www.indeed.com"

    options = webdriver.ChromeOptions()

    chromedrvier_exe = ".\\chromedriver_binary\\chromedriver.exe"
    command = os.popen(f"{chromedrvier_exe} --version")
    out = command.read()

    version = "141.0.7390.54"

    if command.close() == None:
        output_list = out.split(" ")
        version = output_list[1]

    # Override the default user agent with a custom one
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
    options.add_argument(f"--user-agent={user_agent}")

    # start headless browser
    options.add_argument("--headless")

    # disables setting navigator.webdriver to true
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = webdriver.ChromeService(executable_path=chromedrvier_exe)

    df = pd.DataFrame(
        {
            "Job_Title": [],
            "Company": [],
            "Location": [],
            "Link": [],
        }
    )

    try:
        driver = webdriver.Chrome(service=service, options=options)

        # job scraping
        url = f"{us_indeed_url}/jobs?q={query}&l={location}&fromage={date_posted_in_days}&start=0"
        df, msg = scrap_indeed_jobs_page(driver, url, us_indeed_url, df)
        print(msg)

        driver.close()
    except NoSuchDriverException:
        print("NoSuchDriverException: Go to https://developer.chrome.com/docs/chromedriver/downloads. " \
        "Download the ChromeDriver and copy the chromedriver.exe binary to the " \
        "chromedriver_binary directory.")
        exit()

    # Write scrap jobs to a CSV file
    df.to_csv("data/indeed_jobs.csv", index=False)

def scrap_indeed_jobs_page(
    driver: WebDriver, url: str, us_indeed_url: str, df: DataFrame
) -> tuple[DataFrame, str]:
    driver.get(url)

    time.sleep(10)

    print(driver.title)

    driver.save_screenshot("website_screenshots/chromedriver_result.png")

    if driver.title == "Just a moment...":
        return df, "Unable to load web page"

    try:
        # Get the number of jobs
        job_count_element = driver.find_element(
            By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount"
        )

        total_jobs = job_count_element.find_element(By.XPATH, "./span").text
        print(f"{total_jobs} found")

    except NoSuchElementException as e:
        print(e)

    # scrap job data
    soup = BeautifulSoup(driver.page_source, "lxml")

    boxes = soup.find_all("div", class_="job_seen_beacon")

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="logs/scrap_jobs.log",
        filemode="w",
        encoding="utf-8",
        level=logging.DEBUG,
    )

    job_count = 0
    for box in boxes:
        # Job Title information
        link = box.find("a", class_=lambda x: x and "JobTitle" in x).get("href")
        link_full = us_indeed_url + link
        job_title = box.find(
            "a", class_=lambda x: x and "JobTitle" in x
        ).text.strip()

        # Replace the en dash with a dash
        job_title = job_title.replace("\u2013", "-")

        # Company information
        company = box.find("span", {"data-testid": "company-name"}).text.strip()

        # Replace e-grave with e
        company = company.replace("\u00e8", "e")

        # location information
        location_element = box.find("div", {"data-testid": "text-location"})
        location = location_element.text.strip()

        # replace non-brekaing space in Latin1 (ISO 8859-1) to a space
        location = location.replace("\xa0", " ")

        job_info = {
            "job_title": job_title,
            "company": company,
            "location": location,
            "link": link_full,
        }
        logger.debug(job_info)

        job_box_data = pd.DataFrame(
            {
                "Job_Title": [job_title],
                "Company": [company],
                "Location": [location],
                "Link": [link_full],
            }
        )

        df = pd.concat([df, job_box_data], ignore_index=True)
        job_count += 1

    print(f"Scraped {job_count} jobs")

    return df, "Success"


if __name__ == "__main__":
    main()
