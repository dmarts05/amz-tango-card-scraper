# Amazon Tango Card Scraper
![Version](https://img.shields.io/badge/Version-1.0.1-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.9-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Amazon Tango Card Scraper is a Python project that automates the process of scraping and redeeming Amazon Gift Card codes from Microsoft Rewards emails. The script is designed to extract Tango Cards from Gmail emails, retrieve the corresponding Amazon Gift Cards associated with those Tango Cards, automatically redeem the Amazon Gift Cards on Amazon (optional), and store the obtained codes in a file. Additionally, it offers the option to send the results to a Telegram bot chat.

## Table of Contents
* [Features](#features)
* [Configuration](#configuration)
* [Installation with Poetry (recommended)](#installation-with-poetry-recommended)
* [Installation with pip](#installation-with-pip)
* [Development Setup](#development-setup)
* [Contributing](#contributing)
* [License](#license)

## Features
* Scrape Tango Cards from Gmail emails.
* Retrieve associated Amazon Gift Cards from the extracted Tango Cards.
* Automatically redeem Amazon Gift Cards on Amazon.
* Store obtained codes in a file.
* Optional integration with a Telegram bot chat to receive the results.

## Configuration
Before running the script, make sure to configure the necessary settings in the `config.yaml` file. You can use the provided `config.example.yaml` file as a template.

## Installation with Poetry (recommended)
To set up the project, follow these steps:
1. Make sure you have [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) installed in your system.
2. It is highly recommended to set this Poetry configuration parameter to avoid multiple issues:
    ```bash
    poetry config virtualenvs.in-project true
    poetry config virtualenvs.prefer-active-python true
    ```
3. Clone the repository:
    ```bash
    git clone https://github.com/dmarts05/amz-tango-card-scraper.git
    ```
4. Navigate to the project directory:
    ```bash
    cd amz-tango-card-scraper
    ```
5. Install the project dependencies using Poetry:
    ```bash
    poetry install
    ```
    You might need [pyenv](https://github.com/pyenv/pyenv) to install the Python version specified in the `pyproject.toml` file. If that's the case, run `pyenv install 3.9` before running the previous command. Also, check out the [Poetry documentation about pyenv](https://python-poetry.org/docs/managing-environments/) for more information.
6. Activate the virtual environment:
    ```bash
    poetry shell
    ```
    This will activate the virtual environment so that you can run the script.
7. Configure the script by updating the `config.yaml` file with your specific information (as mentioned in the previous section).
8. Run the script:
    ```bash
    python -m amz_tango_card_scraper
    ```
    This will execute the script and start scraping and redeeming Amazon Gift Card codes from Microsoft Rewards emails.

## Installation with pip
This is an alternative installation method that uses pip instead of Poetry. It might not work as expected, so it is recommended to use the Poetry installation method instead. To set up the project, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/dmarts05/amz-tango-card-scraper.git
    ```
2. Navigate to the project directory:
    ```bash
    cd amz-tango-card-scraper
    ```
3. Install the project dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
    You might need [pyenv](https://github.com/pyenv/pyenv) to install the Python version specified in the `requirements.txt` file.
4. Configure the script by updating the `config.yaml` file with your specific information (as mentioned in the previous section).
5. Run the script:
    ```bash
    python -m amz_tango_card_scraper
    ```
    This will execute the script and start scraping and redeeming Amazon Gift Card codes from Microsoft Rewards emails. 

## Development Setup
If you want to contribute to the project or run the development environment, follow these additional steps:
1. Install the development dependencies:
    ```bash
    poetry install --with dev
    ```
2. Format the code:
    ```bash
    poetry run black amz_tango_card_scraper
    ```
3. Lint the code:
    ```bash
    poetry run flake8 amz_tango_card_scraper
    ```
4. Run static type checking:
    ```bash
    poetry run mypy amz_tango_card_scraper
    ```
5. Run the tests:
    ```bash
    poetry run pytest tests
    ```
    You can also run the tests with coverage:
    ```bash
    "poetry run pytest --cov=amz_tango_card_scraper --cov-report=xml tests"
    ```
6. Generate the documentation:
    ```bash
    cd docs && poetry run make html
    ```
7. Do everything at once (except for generating the documentation):
    ```bash
    poetry run pre-commit run --all-files
    ```
That's it! You now have the project set up and ready for development or execution.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). See the [LICENSE](LICENSE) file for details.