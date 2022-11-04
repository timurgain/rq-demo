# Redis Queue demo based on Flask app

## Description

The project acquaints with the [Redis Queue](https://python-rq.org), a simple Python library for queueing jobs and processing them in the background with workers.

## Technologies

- Python3;
- Flask web-framework;
- Redis nosql database;
- Redis Queue library;
- Poetry virtual environment;

## Installation

### Prerequisites
Install [Redis](https://redis.io) and [Python3](https://www.python.org) on your computer. 
Use [Poetry](https://python-poetry.org) for virtual environment.
 
### Then go to a command line
Clone repository and navigate to folder on command line:
```
git clone ...
```
```
cd rq-demo
```

Install dependencies, run virtual environment, start Redis-server
```
poetry install && poetry shell
```
```
redis-server
```
Check if Redis is working properly, response will be PONG
```
redis-cli ping
```

## Launch

Proceed to rq-demo/rq_demo folder and run the app
```
cd rq_demo
```
```
poetry run flask run
```

Use these URLs for starting tasks
```
http://127.0.0.1:5000/start-low-priority-tasks/
```
```
http://127.0.0.1:5000/start-default-priority-tasks
```
```
http://127.0.0.1:5000/start-high-priority-tasks
```

And it's clearer to run the application in [VScode debug mode](https://code.visualstudio.com/docs/python/tutorial-flask#_run-the-app-in-the-debugger)


## Monitoring

...