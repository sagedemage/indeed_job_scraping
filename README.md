# indeed_job_scraping

A web scraping program used to scrap the information of jobs in Indeed

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

Run the program
```
python main.py
```

For Visual Studio Code to automatically use the virtual environment, the .\\.vscode\\settings.json should look like this
```
{
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.experiments.optOutFrom": ["pythonTerminalEnvVarActivation"]
}
```

Run the backend server with
```
fastapi dev backend\main.py
```

## Resources
* [The following extensions want to relaunch the terminal to contribute to its environment #24822 - microsoft/vscode-python GitHub repository](https://github.com/microsoft/vscode-python/issues/24822)
* [How to remove \xa0 from string in Python? - Stack Overflow](https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python)