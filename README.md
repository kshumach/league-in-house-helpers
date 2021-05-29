## Overview

This folder houses the Django server.

## Setup

### Python
1. You will need Python 3 Installed
2. Install [virtualenv](https://docs.python.org/3/tutorial/venv.html) (Optional)
3. Run `pip install -r dev-requirements.txt`. This will install all necessary packages.


### Docker
This repo uses docker to spin up a PostgreSQL server.

1. Install [Docker](https://docs.docker.com/get-docker/) according to your OS
2. `docker-compose up` will spin up any needed services. `docker-compose up -d` will run them in the background


### Dotenv
This project uses [python-dotenv](https://pypi.org/project/python-dotenv/) to read configurations for local development.

The project includes a `.env` file with defaults by default. Note that `settings.py` expect the `.env` file to live at `/backend/.env`.


### Code Style
This repo uses [black](https://black.readthedocs.io/en/stable/installation_and_usage.html) and [isort](https://pypi.org/project/isort/) to format code.

It is already installed as part of the project requirements but not run automatically or policed. Please remember to format.


## Run

1. Spin up the DB or any other needed services. Run `docker-compose up`.
2. Start the Django server `python manage.py runserver`.


## Resources

[Django](https://docs.djangoproject.com/en/3.1/intro/)
[Django-Rest-Framework](https://www.django-rest-framework.org/tutorial/quickstart/) (Api Layer)
[PostgreSQL]()