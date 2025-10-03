# indeed_job_scraping

A web scraping program used to scrap the information of jobs in Indeed

## Setup the Project

Download the ChromeDriver [here](https://developer.chrome.com/docs/chromedriver/downloads).

Copy the chromedriver.exe binary to the chromedriver_binary directory.

Create virtual environment
```
python -m venv venv
```

Activate the virtual environment on Windows
```
.\venv\Scripts\Activate.ps1
```

Install dependencies
```
pip install -r requirements.txt
```

Install dependencies for the front-end server
```
cd frontend
npm install
```

## Run the Project

Run the program
```
python main.py
```

Run the backend server with
```
flask --app backend\main.py run
```

Run the front-end server
```
cd frontend
npm start
```

## Tools to Format and Lint the Codebase 

Format the codebase
```
black main.py backend/*.py
```

Lint the codebase
```
pylint main.py backend/*.py
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

## Resources
* [The following extensions want to relaunch the terminal to contribute to its environment #24822 - microsoft/vscode-python GitHub repository](https://github.com/microsoft/vscode-python/issues/24822)
* [How to remove \xa0 from string in Python? - Stack Overflow](https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python)