# indeed_job_scraping

A web scraping program written in Python. It is used to scrap the information of jobs in Indeed.

## Setup the Project

Download the ChromeDriver [here](https://developer.chrome.com/docs/chromedriver/downloads).

Copy the chromedriver.exe binary to the chromedriver_binary directory.

Create virtual environment
```
python -m venv .venv
```

Activate the virtual environment on Windows
```
.\.venv\Scripts\Activate.ps1
```

Install dependencies
```
pip install -r requirements.txt
```

## Run the Project

Run the job scraper program
```
python main.py
```

Run the app
```
flask --app app/main.py run
```

## Tools to Format and Lint the Codebase 

Format the codebase
```
black *.py app/*.py
```

Check the format of the codebase
```
black *.py app/*.py --check --diff
```

Lint the codebase
```
pylint main.py app/*.py
```

## Setup VSCode for Python

For Visual Studio Code to automatically use the virtual environment, the .\\.vscode\\settings.json should look like this
```
{
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.experiments.optOutFrom": ["pythonTerminalEnvVarActivation"]
}
```

## Generate the Default Pylint Config
Generate the default pylint config if needed
```
pylint --rcfile="" --generate-rcfile > .pylintrc
```

## Resources
- [The following extensions want to relaunch the terminal to contribute to its environment #24822 - microsoft/vscode-python GitHub repository](https://github.com/microsoft/vscode-python/issues/24822)
- [How to remove \xa0 from string in Python? - Stack Overflow](https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python)
- [Selenium headless: How to bypass Cloudflare detection using Selenium - Stack Overflow](https://stackoverflow.com/questions/68289474/selenium-headless-how-to-bypass-cloudflare-detection-using-selenium)
- [How to Modify Selenium navigator.webdriver to Avoid Anti-Bot Detection - zenrows](https://www.zenrows.com/blog/navigator-webdriver#how-to-modify-navigator-webdriver)
- [Chrome specific functionality - Selenium](https://www.selenium.dev/documentation/webdriver/browsers/chrome/)
- [List of Chromium Command Line Switches - Peter Beverloo](https://peter.sh/experiments/chromium-command-line-switches/)
- [Chrome Flags for Tooling - GoogleChrome/chrome-launcher repository](https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md)