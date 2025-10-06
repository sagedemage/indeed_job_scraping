"""Indeed Job Scraper Program"""

from bs4 import BeautifulSoup
from seleniumbase import SB
import pandas as pd
from pandas import DataFrame
import configparser
import logging


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    query = config["DEFAULT"]["Query"]
    location = config["DEFAULT"]["Location"]

    date_posted_in_days = config["DEFAULT"]["DatePostedInDays"]

    us_indeed_url = "https://www.indeed.com"

    df = pd.DataFrame(
        {
            "Job_Title": [],
            "Company": [],
            "Location": [],
            "Link": [],
        }
    )

    # job scraping
    url = (
        f"{us_indeed_url}/jobs?q={query}"
        f"&l={location}&fromage={date_posted_in_days}&start=0"
    )
    df, msg = scrap_indeed_jobs_page(url, us_indeed_url, df)
    print(msg)

    # Write scrap jobs to a CSV file
    df.to_csv("data/indeed_jobs.csv", index=False)


def scrap_indeed_jobs_page(
    url: str, us_indeed_url: str, df: DataFrame
) -> tuple[DataFrame, str]:
    html: str = ""

    with SB(uc=True, test=True, headless=True, locale="en") as sb:
        url = url
        sb.activate_cdp_mode(url)
        sb.sleep(10)
        # attempt to click the CAPTCHA checkbox if present
        sb.uc_gui_click_captcha()
        print(sb.get_page_title())
        sb.save_screenshot("website_screenshots/chromedriver_result.png")
        if sb.get_page_title() == "Just a moment...":
            return df, "Unable to load web page"
        html = sb.get_page_source()

    # scrap job data
    soup = BeautifulSoup(html, "lxml")

    job_count_element = soup.find(
        "div", {"class", "jobsearch-JobCountAndSortPane-jobCount"}
    )

    total_jobs = job_count_element.text
    print(f"{total_jobs} found")

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
        route = box.find("a", class_=lambda x: x and "JobTitle" in x).get(
            "href"
        )
        link = us_indeed_url + route
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

        logger.debug(f"job_title: {job_title}")
        logger.debug(f"company: {company}")
        logger.debug(f"location: {location}")
        logger.debug(f"link: {link}\n")

        job_box_data = pd.DataFrame(
            {
                "Job_Title": [job_title],
                "Company": [company],
                "Location": [location],
                "Link": [link],
            }
        )

        df = pd.concat([df, job_box_data], ignore_index=True)
        job_count += 1

    print(f"Scraped {job_count} jobs")

    return df, "Success"


if __name__ == "__main__":
    main()
