from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_stealth import stealth
import pandas as pd
from pandas import DataFrame
import sys
import time
import configparser
import logging


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    query = config["DEFAULT"]["Query"]
    locations_string = config["DEFAULT"]["Locations"]
    locations_string = locations_string.strip("\"")
    locations = locations_string.split(",")

    date_posted_in_days = config["DEFAULT"]["DatePostedInDays"]

    us_indeed_url = "https://www.indeed.com"

    options = webdriver.ChromeOptions()
    options.headless = True

    # starts the browser maximized
    options.add_argument("--start-maximized")

    # disables setting navigator.webdriver to true
    options.add_argument("--disable-blink-features=AutomationControlled")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    # Override the default user agent with a custom one
    options.add_argument(f"--user-agent={user_agent}")

    # disables the sandbox for all process types
    options.add_argument("--no-sandbox")

    # exclude the enable-automation default argument
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # disables the driver to install other chrome extensions
    options.add_experimental_option("useAutomationExtension", False)

    # Runs in headless mode
    options.add_argument("--headless")

    service = Service(
        "C:\\chromedriver\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    )

    driver = webdriver.Chrome(
        options=options, service=service, keep_alive=True)

    # change the property of the navigator value for webdriver to undefined
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    navigator_webdriver = driver.execute_script("return navigator.webdriver")

    if navigator_webdriver != None:
        print("Error: the navigator.webdriver flag should be disabled")
        sys.exit(1)

    """
    stealth(driver,
            user_agent = user_agent,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            #webdriver=False
        )
    """

    df = pd.DataFrame({"Job_Title": [],
                       "Company": [],
                       "Location": [],
                       "Salary_Amount": [],
                       "Salary_Type": [],
                       "Job_Type": [],
                       "Link": []})

    # ----- Start -----

    end = 20

    for location in locations:
        for i in range(0, end, 10):
            url = f"{us_indeed_url}/jobs?q={query}&l={location}&fromage={date_posted_in_days}&start={i}"
            df, end = scrap_indeed_jobs_page(driver, url, us_indeed_url, df)

            if end < 10 + 10*(i+1):
                break

    # ----- End -----

    # Write scrap jobs to a CSV file
    df.to_csv("data/indeed_jobs.csv", index=False)

    driver.close()


def scrap_indeed_jobs_page(driver: WebDriver, url: str, us_indeed_url: str, df: DataFrame) -> DataFrame:
    time.sleep(10)  # 10 seconds

    driver.get(url)

    time.sleep(10)

    # Get the number of jobs
    job_count_element = driver.find_element(
        By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount"
    )

    time.sleep(10)

    total_jobs = job_count_element.find_element(By.XPATH, "./span").text
    
    end_string = total_jobs.strip(" jobs")
    end = int(end_string)

    driver.save_screenshot("website_screenshots/chromedriver_result.png")
    print(f"{total_jobs} found")

    print(driver.title)

    # scrap job data
    job_types = ["Full-time", "Part-time", "Temp-to-hire", "Seasonal", "Per diem", "Freelance",
                 "Tenure track", "Contract", "Temporary", "Permanent", "Internship", "PRN", "Apprenticeship", "Volunteer"]

    soup = BeautifulSoup(driver.page_source, "lxml")

    boxes = soup.find_all("div", class_="job_seen_beacon")

    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="logs/scrap_jobs.log",
                        filemode="w", encoding="utf-8", level=logging.DEBUG)

    job_count = 0
    for box in boxes:
        # Job Title information
        link = box.find(
            "a", class_=lambda x: x and "JobTitle" in x).get("href")
        link_full = us_indeed_url + link
        job_title = box.find(
            "a", class_=lambda x: x and "JobTitle" in x).text.strip()

        # Replace the en dash with a dash
        job_title = job_title.replace(u'\u2013', u'-')

        # Company information
        company = box.find(
            "span", {"data-testid": "company-name"}).text.strip()
        
        # Replace e-grave with e
        company = company.replace("\u00E8", "e")

        # location information
        location_element = box.find("div", {"data-testid": "text-location"})
        location = location_element.text.strip()

        # replace non-brekaing space in Latin1 (ISO 8859-1) to a space
        location = location.replace(u'\xa0', u' ')

        # salary information
        salary_element = box.find(
            "div", class_=lambda x: x and "css-1a6kja7" in x)

        salary_amount = ""
        salary_type = ""
        if salary_element != None:
            salary_amount_element = salary_element.find(
                "h2", class_=lambda x: x and "mosaic-provider-jobcards-4n9q2y" in x
            )
            if salary_amount_element != None:
                salary_amount = salary_amount_element.text.strip()
            salary_type_element = salary_element.find(
                "span", class_=lambda x: x and "mosaic-provider-jobcards-140tz9m" in x
            )
            if salary_type_element != None:
                salary_type = salary_type_element.text.strip()

        # job type information
        job_meta_data_group_element = box.find(
            "div", class_=lambda x: x and "jobMetaDataGroup" in x
        )

        job_type = ""
        if job_meta_data_group_element != None:
            tap_item_gutter_element = job_meta_data_group_element.find(
                "ul", class_=lambda x: x and "tapItem-gutter" in x
            )
            if tap_item_gutter_element != None:
                meta_datas = tap_item_gutter_element.find_all(
                    "li", recursive=False)
                if len(meta_datas) != 0:
                    meta_data = meta_datas[0]
                    if meta_data != None:
                        done = False
                        meta_data_div_element = meta_data.find(
                            "div", class_=lambda x: x and "css-5ooe72" in x
                        )
                        if meta_data_div_element != None:
                            if meta_data_div_element.text.strip() in job_types:
                                job_type = meta_data_div_element.text.strip()
                                done = True

                        meta_data_div_element = meta_data.find(
                            "div", class_=lambda x: x and "css-48kbdx" in x
                        )
                        if meta_data_div_element != None:
                            if meta_data_div_element.text.strip() in job_types and done == False:
                                job_type = meta_data_div_element.text.strip()
                                done = True

                        meta_data_div_element = meta_data.find(
                            "div", class_=lambda x: x and "eu4oa1w0" in x
                        )
                        if meta_data_div_element != None:
                            if meta_data_div_element.text.strip() in job_types and done == False:
                                job_type = meta_data_div_element.text.strip()
                                done = True

        job_info = {
            "job_title": job_title,
            "company": company,
            "location": location,
            "salary_amount": salary_amount,
            "salary_type": salary_type,
            "job_type": job_type,
            "link": link_full
        }
        logger.debug(job_info)

        job_box_data = pd.DataFrame({"Job_Title": [job_title],
                                     "Company": [company],
                                     "Location": [location],
                                     "Salary_Amount": [salary_amount],
                                     "Salary_Type": [salary_type],
                                     "Job_Type": [job_type],
                                     "Link": [link_full]})

        df = pd.concat([df, job_box_data], ignore_index=True)
        job_count += 1

    print(f"Scraped {job_count} of {total_jobs}")

    with open("html_content/site.html", "w", encoding="utf-8") as f:
        f.write(str(driver.page_source))
    
    return df, end


if __name__ == "__main__":
    main()
