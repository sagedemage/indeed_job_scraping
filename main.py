from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import sys
import time

if __name__ == "__main__":
    url = "https://www.indeed.com/jobs?q=desktop+support&l=United+States"

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
    options.add_argument('--no-sandbox')
    
    # exclude the enable-automation default argument
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # disables the driver to install other chrome extensions
    options.add_experimental_option('useAutomationExtension', False)
    
    # Runs in headless mode
    options.add_argument("--headless")
    
    service = Service("C:\\chromedriver\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
    
    driver = webdriver.Chrome(
        options=options,
        service=service,
        keep_alive=True
    )
    
    # change the property of the navigator value for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
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

    # 10 seconds
    time.sleep(10)

    driver.get(url)
    driver.save_screenshot('website_screenshots/nowsecure.png')

    # 10 seconds
    time.sleep(10)

    # By.CLASS_NAME
    job_count_element = driver.find_element(
        By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount'
    )
    
    # 10 seconds
    time.sleep(10)
    
    total_jobs = job_count_element.find_element(By.XPATH, "./span").text
    print(f"{total_jobs} found")

    page_code = driver.page_source

    # print(page_code)
    print(driver.title)

    driver.close()

    with open("html_content/site.html", "w", encoding="utf-8") as f:
        f.write(str(page_code))
