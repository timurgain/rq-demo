# Redis Queue demo based on Flask app

## Description

The project acquaints with the [Redis Queue](https://python-rq.org), a simple Python library for queueing jobs and processing them in the background with workers.

## Technologies

- Python3;
- Flask web-framework;
- Redis nosql database;
- Redis Queue library;
- Poetry virtual environment;
- HTML, CSS;
- Docker

## Installing with Docker

### Prerequisites
Install [Docker](https://docs.docker.com/get-docker/) on your computer.

Clone repository and navigate to the folder on a command line:
```
git clone ...
```
```
cd rq-demo/infrastructure
```

Build and start docker containers, then go to the url
```
docker compose up
```
```
http://127.0.0.1:5000/
```

## Installing as a standalone application

### Prerequisites
Install [Redis](https://redis.io) and [Python3](https://www.python.org) on your computer.
Use [Poetry](https://python-poetry.org) for virtual environment.

### Then go to a command line
Clone repository and navigate to the folder on a command line:
```
git clone ...
```
```
cd rq-demo/rq_demo
```

Install dependencies, run virtual environment
```
poetry install
```
```
poetry shell
```

Start Redis-server and check if Redis is working properly (response is PONG)
```
redis-server
```
```
redis-cli ping
```

## Launch, start tasks and monitoring

Proceed to rq-demo/rq_demo folder and run the app, then go to the url
```
cd rq_demo
```
```
poetry run flask run
```
```
http://127.0.0.1:5000/
```

And it's clearer to run the application in [VScode debug mode](https://code.visualstudio.com/docs/python/tutorial-flask#_run-the-app-in-the-debugger)
